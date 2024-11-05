import pygame as p

# Initialize Pygame
p.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Chess Menu")

# Initial values for RGB sliders on both sides
red_value_left, green_value_left, blue_value_left = 0, 0, 0
red_value_right, green_value_right, blue_value_right = 0, 0, 0

# Slider properties
slider_x = 175
slider_width = 300
slider_height = 2
handle_radius = 10
square_size = 120

# Font
font_path1 = "../fonts/white_on_black/White On Black.ttf"
font_path2 = "../fonts/melted_monster/Melted Monster.ttf"
font_path3 = "../fonts/the_artisan_marker/The Artisan Marker.otf"

# Main loop
running = True
dragging_red_left = dragging_green_left = dragging_blue_left = False
dragging_red_right = dragging_green_right = dragging_blue_right = False

def draw_text_centered(screen, text, font_path, y_pos, font_size=30, color="#FFFFFF"):
    """Draws text centered at the given y-position."""
    font = p.font.Font(font_path, font_size)  # Load font with the specified size
    text_surface = font.render(text, True, p.Color(color))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(text_surface, text_rect)  # Draw at calculated x position for centering


def draw_text(screen, text, pos, font_size=30, color="#FFFFFF"):
    """Helper function to draw text on the screen."""
    font = p.font.Font(font_path3, font_size)
    text_surface = font.render(text, True, p.Color(color))
    screen.blit(text_surface, pos)

def draw_preview(screen, white_color, black_color):
    """Draws a 2x2 preview chessboard with specified colors."""
    
    preview_x, preview_y = WIDTH // 2 - square_size, 44 * HEIGHT // 100 - square_size

    # Define border colors
    top_border_color = (255, 165, 0)  # Orange
    bottom_border_color = (144, 238, 144)  # Light Green

    # Draw the top border
    p.draw.rect(screen, top_border_color, (preview_x - 5, preview_y - 5, square_size * 2 + 10, square_size + 5))
    # Draw the bottom border
    p.draw.rect(screen, bottom_border_color, (preview_x - 5, preview_y + square_size, square_size * 2 + 10, square_size + 5))

    # Draw the 2x2 preview board
    for row in range(2):
        for col in range(2):
            color = white_color if (row + col) % 2 == 0 else black_color
            p.draw.rect(screen, color, p.Rect(preview_x + col * square_size, preview_y + row * square_size, square_size, square_size))


def draw_slider(screen, position, value):
    # Draw slider background
    p.draw.rect(screen, (206, 206, 206), (position[0], position[1], slider_width, slider_height))
    # Calculate the x position of the slider handle
    handle_x = position[0] + (value / 255) * slider_width
    # Draw the handle as a circle
    p.draw.circle(screen, "yellow", (int(handle_x), position[1]), handle_radius)


def handle_slider_event(event, mouse_down, pos_x, rgb, mouse_pos):
    """Adjust RGB value based on slider interactions."""
    if mouse_down:
        x, y = mouse_pos
        for i, color in enumerate(['red', 'green', 'blue']):
            slider_y = 60 * HEIGHT // 100 + (i - 1) * 100
            if pos_x <= x <= pos_x + slider_width  and slider_y - 10 <= y <= slider_y + 10:
                rgb[i] = min(max(int((x - pos_x) / slider_width * 255), 0), 255)
                return True
    return False

def displayMenu(WIDTH, HEIGHT):
    screen = p.display.set_mode((WIDTH, HEIGHT))
    white_rgb = [255, 255, 255]  # Default white square color
    black_rgb = [128, 0, 250]  # Default black square color

    mouse_down = False  # Track if mouse is being held down

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                exit()
            elif e.type == p.KEYDOWN and e.key == p.K_RETURN:
                return tuple(white_rgb), tuple(black_rgb)

            # Mouse button down event to start dragging
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_down = True
                mouse_x, mouse_y = e.pos

            # Mouse button up event to stop dragging
            elif e.type == p.MOUSEBUTTONUP:
                mouse_down = False

            # Handle mouse motion for RGB adjustments if mouse is down
            elif e.type == p.MOUSEMOTION and mouse_down:
                mouse_x, mouse_y = e.pos

                if handle_slider_event(e, mouse_down, 20 * WIDTH // 100 - slider_width // 2, white_rgb, (mouse_x, mouse_y)):
                    continue
                elif handle_slider_event(e, mouse_down, 80 * WIDTH // 100 - slider_width // 2, black_rgb, (mouse_x, mouse_y)):
                    continue

        # Clear and redraw screen
        screen.fill(p.Color("#034668"))
        text_width = 300
        draw_text_centered(screen, "Choose Board Design", font_path1, 8 * HEIGHT // 100, font_size=65, color="#FFFFFF", )
        draw_text_centered(screen, "Press Enter to Continue",  font_path2, 95 * HEIGHT // 100 , font_size=25, color="#FFFFFF")


        # Draw RGB sliders and labels
        for i, color in enumerate([white_rgb, black_rgb]):
            label = "White Square RGB" if i == 0 else "Black Square RGB"
            draw_text(screen, label, (20 * WIDTH // 100 - slider_width // 2 if i == 0 else 80 * WIDTH // 100 - slider_width // 2, 30 * HEIGHT // 100), font_size=25, color="#FFFFFF")
            for j, color_component in enumerate(['Red', 'Green', 'Blue']):
                slider_color = (255, 0, 0) if j == 0 else (0, 255, 0) if j == 1 else (0, 0, 255)
                x_pos = 20 * WIDTH // 100 - slider_width // 2 if i == 0 else 80 * WIDTH // 100 - slider_width // 2
                y_pos = 60 * HEIGHT // 100 + (j - 1) * 100
                draw_text(screen, f"{color_component}", (x_pos, y_pos - 45), font_size=20, color="#FFFFFF")
                draw_slider(screen, (x_pos, y_pos), color[j])

        # Draw preview square
        draw_text(screen, "Preview :", (WIDTH// 2 - square_size, 19 * HEIGHT // 100), font_size=20, color="#FFFFFF")
        draw_preview(screen, p.Color(*white_rgb), p.Color(*black_rgb))

        p.display.flip()

if __name__ == "__main__":
    p.init()
    white_rgb, black_rgb = displayMenu(WIDTH, HEIGHT)
    p.quit()
