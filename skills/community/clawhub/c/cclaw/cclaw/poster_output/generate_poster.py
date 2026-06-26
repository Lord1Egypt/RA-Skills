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
    draw.text((x, y), char, fill=(0, 255, 136, 30), font=None)

# Load the profile photo
photo_path = r'C:\Users\tiger\Desktop\狼人杀\狼人杀头像(1).jpg'
if os.path.exists(photo_path):
    photo = Image.open(photo_path)
    # Resize to fit in circle
    photo_size = 400
    photo = photo.resize((photo_size, photo_size), Image.Resampling.LANCZOS)
    
    # Create circular mask
    mask = Image.new('L', (photo_size, photo_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
    
    # Apply circular crop
    photo_circle = Image.new('RGBA', (photo_size, photo_size), (0, 0, 0, 0))
    photo_circle.paste(photo, (0, 0))
    photo_circle.putalpha(mask)
    
    # Add cyan border
    border_size = photo_size + 16
    border = Image.new('RGBA', (border_size, border_size), (0, 212, 255, 255))
    border_mask = Image.new('L', (border_size, border_size), 0)
    border_draw = ImageDraw.Draw(border_mask)
    border_draw.ellipse((0, 0, border_size, border_size), fill=255)
    border.putalpha(border_mask)
    
    # Paste border then photo
    border_x = (WIDTH - border_size) // 2
    border_y = 120
    img.paste(border, (border_x, border_y), border)
    img.paste(photo_circle, (border_x + 8, border_y + 8), photo_circle)
    
    # Add glow effect
    glow = Image.new('RGBA', (border_size + 60, border_size + 60), (0, 212, 255, 40))
    glow_mask = Image.new('L', (border_size + 60, border_size + 60), 0)
    glow_draw = ImageDraw.Draw(glow_mask)
    glow_draw.ellipse((0, 0, border_size + 60, border_size + 60), fill=255)
    glow.putalpha(glow_mask)
    glow = glow.filter(ImageFilter.GaussianBlur(20))
    img.paste(glow, (border_x - 30, border_y - 30), glow)

# Try to load fonts, fallback to default if not available
try:
    # Try system fonts
    font_name_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 120)
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 72)
    font_hook = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 48)
    font_brand = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
except:
    font_name_large = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_hook = ImageFont.load_default()
    font_brand = ImageFont.load_default()

# Draw actor name "DIEGO"
name_text = "DIEGO"
name_bbox = draw.textbbox((0, 0), name_text, font=font_name_large)
name_width = name_bbox[2] - name_bbox[0]
name_x = (WIDTH - name_width) // 2
name_y = 580
draw.text((name_x, name_y), name_text, fill='#ffffff', font=font_name_large)

# Draw title "AI打败了程序员"
title_text = "AI打败了程序员"
try:
    # Try to use a font that supports Chinese
    font_title_cn = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 72)
except:
    font_title_cn = font_title
title_bbox = draw.textbbox((0, 0), title_text, font=font_title_cn)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2
title_y = 730
draw.text((title_x, title_y), title_text, fill='#00d4ff', font=font_title_cn)

# Draw divider line
line_y = 860
draw.line([(WIDTH//2 - 100, line_y), (WIDTH//2 + 100, line_y)], fill='#ff6b6b', width=3)

# Draw hook line in a box
hook_text = '"35岁，一个Bug都没修好的人生"'
try:
    font_hook_cn = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 42)
except:
    font_hook_cn = font_hook

# Calculate text size for box
hook_bbox = draw.textbbox((0, 0), hook_text, font=font_hook_cn)
hook_width = hook_bbox[2] - hook_bbox[0]
hook_height = hook_bbox[3] - hook_bbox[1]

# Draw box background
box_padding = 50
box_x = (WIDTH - hook_width - box_padding * 2) // 2
box_y = 950
box_width = hook_width + box_padding * 2
box_height = hook_height + box_padding * 2

# Draw box with left border
draw.rectangle([(box_x, box_y), (box_x + box_width, box_y + box_height)], 
               fill=(255, 255, 255, 13), outline=None)
draw.line([(box_x, box_y), (box_x, box_y + box_height)], fill='#ff6b6b', width=4)

# Draw hook text
hook_text_x = box_x + box_padding
hook_text_y = box_y + box_padding - 10
draw.text((hook_text_x, hook_text_y), hook_text, fill='#ffffff', font=font_hook_cn)

# Draw brand at bottom
brand_text = "CCLAW 喜剧龙虾"
try:
    font_brand_cn = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
except:
    font_brand_cn = font_brand
brand_bbox = draw.textbbox((0, 0), brand_text, font=font_brand_cn)
brand_width = brand_bbox[2] - brand_bbox[0]
brand_x = (WIDTH - brand_width) // 2
brand_y = HEIGHT - 100
draw.text((brand_x, brand_y), brand_text, fill=(255, 255, 255, 100), font=font_brand_cn)

# Add decorative brackets
bracket_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 200)
draw.text((50, 200), "{", fill=(0, 212, 255, 20), font=bracket_font)
draw.text((WIDTH - 150, HEIGHT - 500), "}", fill=(0, 212, 255, 20), font=bracket_font)

# Save the poster
output_path = r'C:\Users\tiger\.qclaw\workspace\cclaw\poster_output\diego_standup_poster.png'
img.save(output_path, 'PNG', quality=95)
print(f"Poster saved to: {output_path}")
