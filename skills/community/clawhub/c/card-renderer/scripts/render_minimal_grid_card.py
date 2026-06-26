import os
import re
from PIL import Image, ImageDraw, ImageFont

def clean_content(text):
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    lines = [l for l in text.split('\n') if not l.strip().startswith('#')]
    return "\n".join(lines).strip()

def render_minimal_grid_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Subtle dot grid background
    dot_spacing = 40
    for x in range(dot_spacing, width, dot_spacing):
        for y in range(dot_spacing, height, dot_spacing):
            draw.point((x, y), fill='#E0E0E0')

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 110)
        sub_font = ImageFont.truetype(font_path, 50)
        tag_font = ImageFont.truetype(font_path, 30)
    except:
        title_font = sub_font = tag_font = ImageFont.load_default()

    title_clean = re.sub(r'[^\u0000-\uFFFF]', '', title)
    sub_clean = re.sub(r'[^\u0000-\uFFFF]', '', subtitle)
    
    # Badge
    draw.rounded_rectangle([100, 100, 300, 150], radius=25, fill='#F5F5F5', outline='#EEEEEE', width=2)
    draw.text((125, 110), "KNOWLEDGE", font=tag_font, fill='#999999')
    
    # Title - Precise alignment
    draw.text((100, 400), title_clean[:8], font=title_font, fill="#212121")
    if len(title_clean) > 8:
        draw.text((100, 530), title_clean[8:], font=title_font, fill="#212121")
    
    draw.rectangle([100, 700, 200, 708], fill='#007AFF') # Accented line
    
    draw.text((100, 750), sub_clean, font=sub_font, fill="#757575")
    
    img.save(output_path)
    print(f"MEDIA:{output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5: sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    render_minimal_grid_cover(t, st, os.path.join(od, "minimal_grid_cover.png"))
