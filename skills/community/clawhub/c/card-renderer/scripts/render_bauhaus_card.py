import os
import re
from PIL import Image, ImageDraw, ImageFont

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

def render_bauhaus_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#F4F4F4')
    draw = ImageDraw.Draw(img)
    
    # Bauhaus Shapes
    draw.rectangle([0, 0, 300, 300], fill='#E63946') # Red square
    draw.ellipse([780, 1140, 1080, 1440], fill='#FFB703') # Yellow circle
    draw.polygon([(0, 1440), (0, 1140), (300, 1440)], fill='#1D3557') # Blue triangle
    
    # Heavy Lines
    draw.line([0, 400, 1080, 400], fill='black', width=15)
    draw.line([400, 0, 400, 400], fill='black', width=15)
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 120)
        sub_font = ImageFont.truetype(font_path, 70)
        num_font = ImageFont.truetype(font_path, 200)
    except:
        title_font = sub_font = num_font = ImageFont.load_default()

    title_clean = strip_emojis(title)
    sub_clean = strip_emojis(subtitle)
    
    # Asymmetric text placement
    draw.text((450, 450), title_clean[:6], font=title_font, fill="black")
    if len(title_clean) > 6:
        draw.text((100, 600), title_clean[6:], font=title_font, fill="black")
    
    draw.text((100, 850), sub_clean, font=sub_font, fill="#1D3557")
    
    # 2026 deco
    draw.text((600, 100), "2026", font=num_font, fill="#DDDDDD")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_bauhaus_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, 50, height], fill='#E63946')
    draw.rectangle([width-50, 0, width, height], fill='#1D3557')
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_header = ImageFont.truetype(font_path, 40)
        font_regular = ImageFont.truetype(font_path, 42)
        font_footer = ImageFont.truetype(font_path, 30)
    except:
        font_header = font_regular = font_footer = ImageFont.load_default()

    draw.text((100, 80), page_info, font=font_header, fill="black")
    draw.line([100, 130, 400, 130], fill='#FFB703', width=10)
    
    y, x = 220, 100
    for line in lines:
        clean_line = strip_emojis(line)
        wrapped = get_wrapped_lines(clean_line, font_regular, width - 250)
        for w_line in wrapped:
            draw.text((x, y), w_line, font=font_regular, fill="black")
            y += 75
        y += 35

    draw.text((100, height - 100), "BAUHAUS X XINA", font=font_footer, fill="#999999")
    img.save(output_path)
    print(f"MEDIA:{output_path}")

def paginate_content(text, font, content_width, max_y_start=220):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    pages, current_page, current_y = [], [], max_y_start
    for para in paragraphs:
        clean_para = strip_emojis(para)
        wrapped = get_wrapped_lines(clean_para, font, content_width)
        h = len(wrapped) * 75 + 35
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
    render_bauhaus_cover(t, st, os.path.join(od, "bauhaus_cover.png"))
    with open(cp, 'r') as f:
        full_text = f.read()
    body_text = "\n".join([l for l in full_text.split('\n') if "标题" not in l and l.strip()])
    try:
        font_reg = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
    except:
        font_reg = ImageFont.load_default()
    pages = paginate_content(body_text, font_reg, 830)
    for i, p_lines in enumerate(pages):
        render_bauhaus_detail(t, p_lines, f"STRUCTURE / {i+1} OF {len(pages)}", os.path.join(od, f"bauhaus_detail_{i+1}.png"))
