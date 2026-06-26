import os
import re
from PIL import Image, ImageDraw, ImageFont

def clean_content(text):
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    lines = [l for l in text.split('\n') if not l.strip().startswith('#')]
    return "\n".join(lines).strip()

def render_polaroid_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#F0F0F0') # Light background
    draw = ImageDraw.Draw(img)
    
    # Polaroid Border
    border_w, border_h = 880, 1100
    border_x, border_y = (width - border_w) // 2, 80
    draw.rectangle([border_x, border_y, border_x+border_w, border_y+border_h], fill='#FFFFFF')
    
    # Inner Photo Area (Square)
    photo_w, photo_h = 780, 780
    photo_x, photo_y = (width - photo_w) // 2, border_y + 50
    draw.rectangle([photo_x, photo_y, photo_x+photo_w, photo_y+photo_h], fill='#EAEAEA') # Placeholder gray
    
    # Text in bottom border
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 80)
        hand_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 40)
    except:
        title_font = hand_font = ImageFont.load_default()

    title_clean = re.sub(r'[^\u0000-\uFFFF]', '', title)
    sub_clean = re.sub(r'[^\u0000-\uFFFF]', '', subtitle)
    
    # Title - Handwritten feel
    draw.text(((width - title_font.getlength(title_clean)) // 2, border_y + 880), title_clean, font=title_font, fill="#333333")
    draw.text(((width - hand_font.getlength(sub_clean)) // 2, border_y + 980), sub_clean, font=hand_font, fill="#666666")

    # Corner Stamp deco
    draw.ellipse([800, 50, 950, 200], outline="#CC0000", width=3)
    draw.text((830, 100), "XINA", font=hand_font, fill="#CC0000")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_polaroid_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#F0F0F0')
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([50, 50, 1030, 1390], fill='#FFFFFF')
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_header = ImageFont.truetype(font_path, 36)
        font_regular = ImageFont.truetype(font_path, 42)
    except:
        font_header = font_regular = ImageFont.load_default()

    draw.text((100, 100), page_info, font=font_header, fill="#999999")
    
    y, x = 200, 120
    for line in lines:
        clean_line = re.sub(r'[^\u0000-\uFFFF]', '', line)
        draw.text((x, y), clean_line, font=font_regular, fill="#333333")
        y += 75
        y += 35

    img.save(output_path)
    print(f"MEDIA:{output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5: sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    render_polaroid_cover(t, st, os.path.join(od, "polaroid_cover.png"))
