import os
import re
from PIL import Image, ImageDraw, ImageFont

def clean_content(text):
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    lines = [l for l in text.split('\n') if not l.strip().startswith('#')]
    return "\n".join(lines).strip()

def render_framed_minimal_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Elegant inner border
    margin = 80
    draw.rectangle([margin, margin, width-margin, height-margin], outline='#F0F0F0', width=2)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 100)
        sub_font = ImageFont.truetype(font_path, 55)
        deco_font = ImageFont.truetype(font_path, 32)
    except:
        title_font = sub_font = deco_font = ImageFont.load_default()

    title_clean = re.sub(r'[^\u0000-\uFFFF]', '', title)
    sub_clean = re.sub(r'[^\u0000-\uFFFF]', '', subtitle)
    
    # Top info
    draw.text((margin+50, margin+50), "STUDY LOG / VOL. 26", font=deco_font, fill="#CCCCCC")
    
    # Central text layout
    title_w = title_font.getlength(title_clean)
    draw.text(((width - title_w) // 2, 600), title_clean, font=title_font, fill="#2C3E50")
    
    sub_w = sub_font.getlength(sub_clean)
    draw.text(((width - sub_w) // 2, 750), sub_clean, font=sub_font, fill="#95A5A6")
    
    # Bottom deco
    draw.rectangle([(width-100)//2, 850, (width+100)//2, 855], fill="#000000")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5: sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    render_framed_minimal_cover(t, st, os.path.join(od, "framed_minimal_cover.png"))
