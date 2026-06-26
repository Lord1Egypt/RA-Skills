import os
import re
from PIL import Image, ImageDraw, ImageFont

def clean_content(text):
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    lines = [l for l in text.split('\n') if not l.strip().startswith('#')]
    return "\n".join(lines).strip()

def render_magazine_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Large Number 01 Deco
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        big_num_font = ImageFont.truetype(font_path, 400)
        title_font = ImageFont.truetype(font_path, 130)
        sub_font = ImageFont.truetype(font_path, 60)
        deco_font = ImageFont.truetype(font_path, 32)
    except:
        big_num_font = title_font = sub_font = deco_font = ImageFont.load_default()

    draw.text((100, 100), "2026", font=big_num_font, fill="#F2F2F2")
    
    # Vertical Line
    draw.rectangle([100, 500, 115, 1000], fill='black')
    
    title_clean = re.sub(r'[^\u0000-\uFFFF]', '', title)
    sub_clean = re.sub(r'[^\u0000-\uFFFF]', '', subtitle)
    
    # Asymmetric Bold Title
    draw.text((160, 600), title_clean[:4], font=title_font, fill="black")
    if len(title_clean) > 4:
        draw.text((160, 750), title_clean[4:], font=title_font, fill="black")
    
    draw.text((160, 950), sub_clean, font=sub_font, fill="#666666")
    
    # Page deco
    draw.text((100, 1300), "XINA / MAGAZINE ISSUE NO. 1", font=deco_font, fill="black")
    draw.line([100, 1350, 980, 1350], fill='black', width=3)

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_magazine_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_header = ImageFont.truetype(font_path, 48)
        font_regular = ImageFont.truetype(font_path, 42)
    except:
        font_header = font_regular = ImageFont.load_default()

    draw.text((100, 100), page_info, font=font_header, fill="black")
    draw.rectangle([100, 170, 300, 180], fill='black')
    
    y, x = 250, 100
    for line in lines:
        clean_line = re.sub(r'[^\u0000-\uFFFF]', '', line)
        draw.text((x, y), clean_line, font=font_regular, fill="#333333")
        y += 80
        y += 30

    img.save(output_path)
    print(f"MEDIA:{output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5: sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    render_magazine_cover(t, st, os.path.join(od, "magazine_cover.png"))
