import os
import re
from PIL import Image, ImageDraw, ImageFont

def clean_content(text):
    """Removes emojis and lines starting with # (hashtags)."""
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    lines = [l for l in text.split('\n') if not l.strip().startswith('#')]
    return "\n".join(lines).strip()

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

def render_vscode_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#1E1E1E')
    draw = ImageDraw.Draw(img)
    
    # VS Code Sidebar (activity bar)
    draw.rectangle([0, 0, 80, height], fill='#333333')
    draw.rectangle([80, 0, 320, height], fill='#252526') # Side bar
    
    # Explorer text
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        small_font = ImageFont.truetype(font_path, 24)
        draw.text((100, 40), "EXPLORER", font=small_font, fill="#BBBBBB")
        draw.text((120, 100), "v xina_project", font=small_font, fill="#FFFFFF")
        draw.text((140, 150), "{} content.md", font=small_font, fill="#519ABA")
        draw.text((140, 200), "{} card.py", font=small_font, fill="#DAA520")
    except: pass

    # Editor Tab
    draw.rectangle([320, 0, 600, 50], fill='#1E1E1E')
    draw.rectangle([600, 0, 1080, 50], fill='#2D2D2D')
    
    # Code Content Area
    title_clean = re.sub(r'[^\u0000-\uFFFF]', '', title)
    sub_clean = re.sub(r'[^\u0000-\uFFFF]', '', subtitle)
    
    try:
        title_font = ImageFont.truetype(font_path, 85)
        mono_font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 36)
    except:
        title_font = mono_font = ImageFont.load_default()

    # Mock Code Line numbers
    for i in range(1, 25):
        draw.text((340, 80 + i*45), str(i), font=mono_font, fill="#858585")

    # Title as Code
    draw.text((420, 150), "// Title: " + title_clean, font=mono_font, fill="#6A9955")
    draw.text((420, 250), "const", font=mono_font, fill="#569CD6")
    draw.text((550, 250), "Subject", font=mono_font, fill="#4FC1FF")
    draw.text((710, 250), "=", font=mono_font, fill="#D4D4D4")
    draw.text((750, 250), f"'{sub_clean}';", font=mono_font, fill="#CE9178")

    draw.text((420, 350), "function", font=mono_font, fill="#569CD6")
    draw.text((620, 350), "InitVibe()", font=mono_font, fill="#DCDCAA")
    draw.text((850, 350), "{", font=mono_font, fill="#D4D4D4")
    
    # Massive Title in the middle
    draw.text(((width + 320 - title_font.getlength(title_clean)) // 2, 700), title_clean, font=title_font, fill="#FFFFFF")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_vscode_detail(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#1E1E1E')
    draw = ImageDraw.Draw(img)
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_header = ImageFont.truetype(font_path, 36)
        font_regular = ImageFont.truetype(font_path, 42)
        mono_font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 30)
    except:
        font_header = font_regular = mono_font = ImageFont.load_default()

    draw.text((100, 50), f"// {page_info}", font=mono_font, fill="#6A9955")
    
    y, x = 150, 100
    for line in lines:
        clean_line = re.sub(r'[^\u0000-\uFFFF]', '', line)
        wrapped = get_wrapped_lines(clean_line, font_regular, width - 200)
        for w_line in wrapped:
            draw.text((x, y), w_line, font=font_regular, fill="#D4D4D4")
            y += 75
        y += 40

    draw.text((width - 400, height - 80), "TERMINAL: COMPLETED", font=mono_font, fill="#89D185")
    img.save(output_path)
    print(f"MEDIA:{output_path}")

def paginate_content(text, font, content_width, max_y_start=220):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    pages, current_page, current_y = [], [], max_y_start
    for para in paragraphs:
        clean_para = re.sub(r'[^\u0000-\uFFFF]', '', para)
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
    if len(sys.argv) < 5: sys.exit(1)
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    
    render_vscode_cover(t, st, os.path.join(od, "vscode_cover.png"))
    
    with open(cp, 'r') as f:
        full_text = f.read()
    body_text = clean_content(full_text)
    
    try:
        font_reg = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
    except:
        font_reg = ImageFont.load_default()
        
    pages = paginate_content(body_text, font_reg, 880)
    for i, p_lines in enumerate(pages):
        render_vscode_detail(t, p_lines, f"FILE: detail_{i+1}.md / {i+1} OF {len(pages)}", os.path.join(od, f"vscode_detail_{i+1}.png"))
