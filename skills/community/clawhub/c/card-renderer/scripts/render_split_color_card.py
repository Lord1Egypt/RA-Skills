import os
import re
from PIL import Image, ImageDraw, ImageFont

def clean_content(text):
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    lines = [l for l in text.split('\n') if not l.strip().startswith('#')]
    return "\n".join(lines).strip()

def render_split_color_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Large soft color shape behind title
    draw.rounded_rectangle([0, 300, 800, 1140], radius=50, fill='#F0F7FF') 
    
    # Large circle accent
    draw.ellipse([900, 100, 1100, 300], fill='#E3F2FD')

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 115)
        sub_font = ImageFont.truetype(font_path, 60)
        num_font = ImageFont.truetype(font_path, 180)
    except:
        title_font = sub_font = num_font = ImageFont.load_default()

    title_clean = re.sub(r'[^\u0000-\uFFFF]', '', title)
    sub_clean = re.sub(r'[^\u0000-\uFFFF]', '', subtitle)
    
    # Big serial number background
    draw.text((100, 350), "01", font=num_font, fill="#E1EFFF")
    
    # Title - Aligned inside the box
    draw.text((150, 600), title_clean[:6], font=title_font, fill="#0D47A1")
    if len(title_clean) > 6:
        draw.text((150, 750), title_clean[6:], font=title_font, fill="#0D47A1")
    
    draw.text((150, 950), sub_clean, font=sub_font, fill="#1976D2")
    
    # Footer
    draw.text((100, 1300), "KNOWLEDGE SERIES / 2026", font=ImageFont.truetype(font_path, 30), fill="#BBBBBB")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5: sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    render_split_color_cover(t, st, os.path.join(od, "split_color_cover.png"))
