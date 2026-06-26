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

def get_font(font_paths, size):
    """Try to load the first available font from a list of paths."""
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def render_vintage_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#E8DCC4')
    draw = ImageDraw.Draw(img)
    
    # Paper texture
    import random
    for _ in range(4000):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        draw.point((x, y), fill='#D8CCB4')

    # Border frame
    draw.rectangle([40, 40, width-40, height-40], outline='#5D4037', width=6)
    draw.rectangle([60, 60, width-60, height-60], outline='#5D4037', width=2)

    # Font candidates for vintage feel (Serif fonts prefered)
    title_paths = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/PingFang.ttc"
    ]
    sub_paths = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc"
    ]
    type_paths = [
        "/System/Library/Fonts/Courier.dfont",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Monaco.ttf"
    ]

    # Increase font sizes significantly for impact
    title_font = get_font(title_paths, 120) 
    sub_font = get_font(sub_paths, 60)
    type_font = get_font(type_paths, 45)

    title_clean = strip_emojis(title)
    sub_clean = strip_emojis(subtitle)
    
    # Title - Wrapping and Centered
    max_line_width = 860
    wrapped_title = get_wrapped_lines(title_clean, title_font, max_line_width)
    
    # Calculate vertical start to center roughly in top half
    line_spacing = 140
    total_title_h = len(wrapped_title) * line_spacing
    y_start = 500 - (total_title_h // 2)
    
    for line in wrapped_title:
        line_w = title_font.getlength(line)
        draw.text(((width - line_w) // 2, y_start), line, font=title_font, fill="#2E1A16")
        y_start += line_spacing
    
    # Decorative line
    y_line = y_start + 60
    draw.line([(width//2-200, y_line), (width//2+200, y_line)], fill='#5D4037', width=4)

    # Subtitle
    y_sub = y_line + 80
    sub_w = sub_font.getlength(sub_clean)
    draw.text(((width - sub_w) // 2, y_sub), sub_clean, font=sub_font, fill="#5D4037")
    
    # Footer deco
    footer_text = "--- CLAW ARCHIVES / VOL. 2026 ---"
    footer_w = type_font.getlength(footer_text)
    draw.text(((width - footer_w) // 2, height-150), footer_text, font=type_font, fill="#8D6E63")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_vintage_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#F2E8D5')
    draw = ImageDraw.Draw(img)
    
    font_paths = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc"
    ]
    font_header = get_font(font_paths, 36)
    font_regular = get_font(font_paths, 45) # Bigger body text
    font_footer = get_font(font_paths, 32)

    draw.text((120, 100), page_info, font=font_header, fill="#795548")
    draw.line([120, 150, 960, 150], fill='#A1887F', width=3)
    
    y, x = 240, 120
    for line in lines:
        clean_line = strip_emojis(line)
        wrapped = get_wrapped_lines(clean_line, font_regular, width - 240)
        for w_line in wrapped:
            draw.text((x, y), w_line, font=font_regular, fill="#3E2723")
            y += 85
        y += 40

    footer_text = f"XINA ARCHIVES / {page_info}"
    draw.text(((width - font_footer.getlength(footer_text)) // 2, height - 100), footer_text, font=font_footer, fill="#BCAAA4")
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
    render_vintage_cover(t, st, os.path.join(od, "vintage_cover.png"))
    with open(cp, 'r') as f:
        full_text = f.read()
    body_text = "\n".join([l for l in full_text.split('\n') if "标题" not in l and l.strip()])
    try:
        font_reg = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
    except:
        font_reg = ImageFont.load_default()
    pages = paginate_content(body_text, font_reg, 840)
    for i, p_lines in enumerate(pages):
        render_vintage_detail(t, p_lines, f"ARCHIVE / {i+1} OF {len(pages)}", os.path.join(od, f"vintage_detail_{i+1}.png"))
