import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def strip_emojis(text):
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

def get_wrapped_lines(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append("")
            continue
        current_line = ""
        for char in paragraph:
            w = font.getlength(current_line + char)
            if w <= max_width:
                current_line += char
            else:
                lines.append(current_line)
                current_line = char
        lines.append(current_line)
    return lines

def render_dreamy_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    # Soft mesh-like gradient (simulated)
    img = Image.new('RGB', (width, height), '#F0E5FF')
    draw = ImageDraw.Draw(img)
    
    # Draw some soft blurred blobs
    blob_layer = Image.new('RGBA', (width, height), (0,0,0,0))
    blob_draw = ImageDraw.Draw(blob_layer)
    blob_draw.ellipse([200, 200, 900, 900], fill=(160, 196, 255, 150)) # Blue
    blob_draw.ellipse([-200, 800, 600, 1600], fill=(255, 173, 212, 120)) # Pink
    blob_draw.ellipse([600, 0, 1200, 600], fill=(202, 255, 191, 100)) # Green
    
    blob_layer = blob_layer.filter(ImageFilter.GaussianBlur(radius=100))
    img.paste(blob_layer, (0,0), blob_layer)

    # Glassmorphism Box
    box_w, box_h = 900, 600
    box_x, box_y = (width - box_w) // 2, (height - box_h) // 2
    
    # White translucent box
    glass = Image.new('RGBA', (box_w, box_h), (255, 255, 255, 120))
    img.paste(glass, (box_x, box_y), glass)
    
    # Subtle border
    draw.rectangle([box_x, box_y, box_x+box_w, box_y+box_h], outline=(255, 255, 255, 180), width=2)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 100)
        sub_font = ImageFont.truetype(font_path, 60)
        deco_font = ImageFont.truetype(font_path, 30)
    except:
        title_font = sub_font = deco_font = ImageFont.load_default()

    title_clean = strip_emojis(title)
    sub_clean = strip_emojis(subtitle)
    
    draw.text(((width - title_font.getlength(title_clean)) // 2, box_y + 180), title_clean, font=title_font, fill="#4A4E69")
    draw.text(((width - sub_font.getlength(sub_clean)) // 2, box_y + 350), sub_clean, font=sub_font, fill="#9A8C98")
    
    # Decoration
    draw.text((box_x + 50, box_y + 50), "CREATIVE INSPIRATION", font=deco_font, fill="#C9ADA7")
    draw.text((box_x + box_w - 250, box_y + box_h - 80), "2026 EDITION", font=deco_font, fill="#C9ADA7")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_dreamy_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FDFDFF')
    draw = ImageDraw.Draw(img)
    
    # Side bar gradient deco
    draw.rectangle([0, 0, 15, height], fill='#A0C4FF')
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_header = ImageFont.truetype(font_path, 36)
        font_regular = ImageFont.truetype(font_path, 42)
        font_footer = ImageFont.truetype(font_path, 30)
    except:
        font_header = font_regular = font_footer = ImageFont.load_default()

    draw.text((100, 80), page_info, font=font_header, fill="#BDB2FF")
    
    y, x = 220, 100
    for line in lines:
        clean_line = strip_emojis(line)
        wrapped = get_wrapped_lines(clean_line, font_regular, width - 200)
        for w_line in wrapped:
            draw.text((x, y), w_line, font=font_regular, fill="#4A4E69")
            y += 75
        y += 40

    draw.text(((width - font_footer.getlength("DREAMY SERIES / XINA")) // 2, height - 100), "DREAMY SERIES / XINA", font=font_footer, fill="#D1D1D1")
    img.save(output_path)
    print(f"MEDIA:{output_path}")

def paginate_content(text, font, content_width, max_y_start=220):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    pages, current_page, current_y = [], [], max_y_start
    for para in paragraphs:
        clean_para = strip_emojis(para)
        wrapped = get_wrapped_lines(clean_para, font, content_width)
        h = len(wrapped) * 75 + 40
        if current_y + h > 1250:
            if current_page: pages.append(current_page)
            current_page, current_y = [para], max_y_start + h
        else:
            current_page.append(para)
            current_y += h
    if current_page: pages.append(current_page)
    return pages

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    render_dreamy_cover(t, st, os.path.join(od, "dreamy_cover.png"))
    with open(cp, 'r') as f:
        full_text = f.read()
    body_text = "\n".join([l for l in full_text.split('\n') if "标题" not in l and l.strip()])
    try:
        font_reg = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
    except:
        font_reg = ImageFont.load_default()
    pages = paginate_content(body_text, font_reg, 880)
    for i, p_lines in enumerate(pages):
        render_dreamy_detail(t, p_lines, f"VIBE CHECK / {i+1} OF {len(pages)}", os.path.join(od, f"dreamy_detail_{i+1}.png"))
