import os
import re
import random
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

def draw_cyber_grid(draw, width, height):
    grid_size = 60
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill='#1A1A1A', width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill='#1A1A1A', width=1)

def render_cyber_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#050505')
    draw = ImageDraw.Draw(img)
    
    draw_cyber_grid(draw, width, height)
    
    # Corner brackets
    padding = 60
    bw, bh = 100, 100
    draw.line([(padding, padding), (padding+bw, padding)], fill='#FF00FF', width=4)
    draw.line([(padding, padding), (padding, padding+bh)], fill='#FF00FF', width=4)
    
    draw.line([(width-padding-bw, padding), (width-padding, padding)], fill='#00FFFF', width=4)
    draw.line([(width-padding, padding), (width-padding, padding+bh)], fill='#00FFFF', width=4)

    draw.line([(padding, height-padding), (padding+bw, height-padding)], fill='#00FFFF', width=4)
    draw.line([(padding, height-padding-bh), (padding, height-padding)], fill='#00FFFF', width=4)

    draw.line([(width-padding-bw, height-padding), (width-padding, height-padding)], fill='#FF00FF', width=4)
    draw.line([(width-padding, height-padding-bh), (width-padding, height-padding)], fill='#FF00FF', width=4)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    mono_font_path = "/System/Library/Fonts/Monaco.ttf"
    
    try:
        title_font = ImageFont.truetype(font_path, 110)
        sub_font = ImageFont.truetype(font_path, 65)
        mono_font = ImageFont.truetype(mono_font_path, 30)
    except:
        title_font = sub_font = mono_font = ImageFont.load_default()

    title_clean = strip_emojis(title)
    sub_clean = strip_emojis(subtitle)
    
    # Glitch effect for title
    draw.text(((width - title_font.getlength(title_clean)) // 2 + 5, 505), title_clean, font=title_font, fill="#FF00FF")
    draw.text(((width - title_font.getlength(title_clean)) // 2 - 5, 495), title_clean, font=title_font, fill="#00FFFF")
    draw.text(((width - title_font.getlength(title_clean)) // 2, 500), title_clean, font=title_font, fill="#FFFFFF")
    
    # Bar indicator
    draw.rectangle([200, 680, 880, 685], fill="#FF00FF")
    draw.rectangle([200, 680, 400, 685], fill="#00FFFF")

    # Subtitle
    draw.text(((width - sub_font.getlength(sub_clean)) // 2, 750), sub_clean, font=sub_font, fill="#00FFFF")
    
    # Scanline deco
    for i in range(0, height, 10):
        draw.line([(0, i), (width, i)], fill=(255, 255, 255, 10), width=1)

    # Status deco
    draw.text((100, height-150), "SYSTEM STATUS: OPTIMAL", font=mono_font, fill="#FF00FF")
    draw.text((100, height-110), "CONNECTION: SECURE [XINA_V1.0]", font=mono_font, fill="#00FFFF")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_cyber_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#080808')
    draw = ImageDraw.Draw(img)
    draw_cyber_grid(draw, width, height)
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    mono_font_path = "/System/Library/Fonts/Monaco.ttf"
    try:
        font_header = ImageFont.truetype(mono_font_path, 36)
        font_regular = ImageFont.truetype(font_path, 42)
        font_footer = ImageFont.truetype(mono_font_path, 30)
    except:
        font_header = font_regular = font_footer = ImageFont.load_default()

    draw.text((100, 80), f">>> {page_info}", font=font_header, fill="#00FFFF")
    draw.line([100, 140, 980, 140], fill='#FF00FF', width=2)
    
    y, x = 220, 100
    for line in lines:
        clean_line = strip_emojis(line)
        wrapped = get_wrapped_lines(clean_line, font_regular, width - 200)
        for w_line in wrapped:
            if any(w_line.startswith(s) for s in ["1", "2", "3"]):
                draw.text((x, y), w_line, font=font_regular, fill="#00FFFF")
            else:
                draw.text((x, y), w_line, font=font_regular, fill="#FFFFFF")
            y += 75
        y += 35

    draw.text((width - 450, height - 100), "ENCRYPTED BY XINA", font=font_footer, fill="#FF00FF")
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
    render_cyber_cover(t, st, os.path.join(od, "cyber_cover.png"))
    with open(cp, 'r') as f:
        full_text = f.read()
    body_text = "\n".join([l for l in full_text.split('\n') if "标题" not in l and l.strip()])
    try:
        font_reg = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
    except:
        font_reg = ImageFont.load_default()
    pages = paginate_content(body_text, font_reg, 880)
    for i, p_lines in enumerate(pages):
        render_cyber_detail(t, p_lines, f"DATA_LOG / {i+1} OF {len(pages)}", os.path.join(od, f"cyber_detail_{i+1}.png"))
