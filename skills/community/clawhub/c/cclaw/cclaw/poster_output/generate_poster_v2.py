from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Poster dimensions (1080x1920 - 9:16 vertical)
WIDTH = 1080
HEIGHT = 1920

# Create base image with gradient background
img = Image.new('RGB', (WIDTH, HEIGHT), '#0a0a0f')
draw = ImageDraw.Draw(img)

# Create gradient background
for y in range(HEIGHT):
    # Gradient from dark blue-black to deep blue
    r = int(10 + (22-10) * y / HEIGHT)
    g = int(10 + (33-10) * y / HEIGHT)
    b = int(15 + (62-15) * y / HEIGHT)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add subtle code pattern in background
import random
random.seed(42)
code_chars = '01{}[]();=<>/\\'
for _ in range(500):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    char = random.choice(code_chars)
    draw.text((x, y), char, fill=(0, 100, 80), font=None)

# Load fonts - try multiple options for Chinese support
def load_font(size, bold=False):
    font_paths = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

font_name_large = load_font(110, bold=True)
font_title = load_font(64, bold=True)
font_hook = load_font(40)
font_brand = load_font(22)

# Load the profile photo
photo_path = r'C:\Users\tiger\Desktop\狼人杀\狼人杀头像(1).jpg'
photo_y = 120
if os.path.exists(photo_path):
    try:
        photo = Image.open(photo_path)
        # Convert to RGB if necessary
        if photo.mode in ('RGBA', 'P'):
            photo = photo.convert('RGB')
        
        # Resize to fit in circle
        photo_size = 380
        photo = photo.resize((photo_size, photo_size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new('L', (photo_size, photo_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
        
        # Add cyan border
        border_size = photo_size + 16
        border = Image.new('RGB', (border_size, border_size), (0, 212, 255))
        border_mask = Image.new('L', (border_size, border_size), 0)
        border_draw = ImageDraw.Draw(border_mask)
        border_draw.ellipse((0, 0, border_size, border_size), fill=255)
        
        # Create a temporary image for compositing
        temp = Image.new('RGB', (border_size, border_size), (10, 10, 15))
        temp.paste(border, (0, 0), border_mask)
        
        # Paste photo in center
        photo_circle = Image.new('RGB', (photo_size, photo_size), (10, 10, 15))
        photo_circle.paste(photo, (0, 0), mask)
        temp.paste(photo_circle, (8, 8), mask)
        
        # Add glow effect
        glow = Image.new('RGBA', (border_size + 80, border_size + 80), (0, 212, 255, 60))
        glow_mask = Image.new('L', (border_size + 80, border_size + 80), 0)
        glow_draw = ImageDraw.Draw(glow_mask)
        glow_draw.ellipse((0, 0, border_size + 80, border_size + 80), fill=255)
        glow.putalpha(glow_mask)
        glow = glow.filter(ImageFilter.GaussianBlur(30))
        
        # Paste glow first
        glow_x = (WIDTH - border_size - 80) // 2
        img.paste(glow, (glow_x, photo_y - 40), glow)
        
        # Paste photo with border
        border_x = (WIDTH - border_size) // 2
        img.paste(temp, (border_x, photo_y))
        
    except Exception as e:
        print(f"Error loading photo: {e}")
        # Draw placeholder circle
        border_x = (WIDTH - 400) // 2
        draw.ellipse([(border_x, photo_y), (border_x + 400, photo_y + 400)], 
                    fill=(0, 212, 255), outline=None)
else:
    print(f"Photo not found: {photo_path}")

# Draw actor name "DIEGO"
name_text = "DIEGO"
name_bbox = draw.textbbox((0, 0), name_text, font=font_name_large)
name_width = name_bbox[2] - name_bbox[0]
name_x = (WIDTH - name_width) // 2
name_y = 580
draw.text((name_x, name_y), name_text, fill='#ffffff', font=font_name_large)

# Draw title "AI打败了程序员"
title_text = "AI打败了程序员"
title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2
title_y = 720
draw.text((title_x, title_y), title_text, fill='#00d4ff', font=font_title)

# Draw divider line
line_y = 840
draw.line([(WIDTH//2 - 100, line_y), (WIDTH//2 + 100, line_y)], fill='#ff6b6b', width=3)

# Draw hook line in a box
hook_text = '"35岁，一个Bug都没修好的人生"'
hook_bbox = draw.textbbox((0, 0), hook_text, font=font_hook)
hook_width = hook_bbox[2] - hook_bbox[0]
hook_height = hook_bbox[3] - hook_bbox[1]

# Draw box background
box_padding = 40
box_x = max(50, (WIDTH - hook_width - box_padding * 2) // 2)
box_y = 920
box_width = min(WIDTH - 100, hook_width + box_padding * 2)
box_height = hook_height + box_padding * 2 + 20

# Draw semi-transparent box
draw.rectangle([(box_x, box_y), (box_x + box_width, box_y + box_height)], 
               fill=(255, 255, 255, 30), outline=None)
# Draw left border
draw.line([(box_x, box_y), (box_x, box_y + box_height)], fill='#ff6b6b', width=4)

# Draw hook text centered
hook_text_x = box_x + (box_width - hook_width) // 2
hook_text_y = box_y + (box_height - hook_height) // 2 - 5
draw.text((hook_text_x, hook_text_y), hook_text, fill='#ffffff', font=font_hook)

# Draw brand at bottom
brand_text = "CCLAW 喜剧龙虾"
brand_bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
brand_width = brand_bbox[2] - brand_bbox[0]
brand_x = (WIDTH - brand_width) // 2
brand_y = HEIGHT - 100
draw.text((brand_x, brand_y), brand_text, fill=(200, 200, 200), font=font_brand)

# Add decorative brackets
try:
    bracket_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 180)
except:
    bracket_font = ImageFont.load_default()
draw.text((40, 180), "{", fill=(0, 212, 255), font=bracket_font)
draw.text((WIDTH - 120, HEIGHT - 450), "}", fill=(0, 212, 255), font=bracket_font)

# Save the poster
output_path = r'C:\Users\tiger\.qclaw\workspace\cclaw\poster_output\diego_standup_poster_v2.png'
img.save(output_path, 'PNG', quality=95)
print(f"Poster saved to: {output_path}")
