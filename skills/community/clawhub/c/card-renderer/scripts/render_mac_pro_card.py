import os
import re
from PIL import Image, ImageDraw, ImageFont

def strip_emojis(text):
    """Removes non-BMP characters (emojis)."""
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

def render_designer_cover(title, subtitle, output_path):
    width, height = 1080, 1440
    # 更加深邃、带有微弱径向渐变感的背景
    img = Image.new('RGB', (width, height), '#0A0A0E')
    draw = ImageDraw.Draw(img)
    
    # 模拟径向渐变 (在窗口中心加点微光)
    for r in range(600, 0, -10):
        alpha = int(20 * (1 - r/600))
        draw.ellipse([(width/2-r, 440-r), (width/2+r, 440+r)], fill=f'#1A1A2E{alpha:02x}')

    # macOS Window (更加精致的阴影和边框)
    win_w, win_h = 880, 540
    win_x, win_y = (width - win_w) // 2, 180
    
    # 多层阴影
    for i in range(1, 15):
        draw.rounded_rectangle([win_x-i, win_y-i, win_x+win_w+i, win_y+win_h+i], radius=25, outline='#000000', width=1)
    
    # 窗口主体
    draw.rounded_rectangle([win_x, win_y, win_x+win_w, win_y+win_h], radius=20, fill='#16161E')
    
    # 标题栏
    header_h = 50
    draw.rounded_rectangle([win_x, win_y, win_x+win_w, win_y+header_h+15], radius=20, fill='#24242E')
    draw.rectangle([win_x, win_y+header_h, win_x+win_w, win_y+header_h+15], fill='#24242E')
    
    # 控制按钮 (增加点渐变感)
    btn_colors = ['#FF5F56', '#FFBD2E', '#27C93F']
    for i, color in enumerate(btn_colors):
        draw.ellipse([win_x+25+i*35, win_y+15, win_x+25+i*35+24, win_y+15+24], fill=color)
    
    try:
        # 使用更为极客的字体，如果没有则回退
        code_font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 34)
    except:
        code_font = ImageFont.load_default()
        
    # 模拟真实的代码高亮 (更具美感的配色)
    code_lines = [
        ("import ", "#C678DD"), ("vibe", "#D19A66"),
        ("\n\n# 2026 文科生新素养", "#5C6370"),
        ("\nclass ", "#C678DD"), ("VibeCoder", "#E5C07B"), ("():", "#ABB2BF"),
        ("\n    def ", "#C678DD"), ("build_tool", "#61AFEF"), ("(self, idea):", "#ABB2BF"),
        ("\n        script = AI.write(idea)", "#98C379"),
        ("\n        script.run(local_files=True)", "#98C379"),
        ("\n        return ", "#C678DD"), ("'魔法生效✨'", "#98C379")
    ]
    
    cx, cy = win_x + 50, win_y + 110
    for text, color in code_lines:
        if text.startswith("\n"):
            cy += 50
            cx = win_x + 50
            text = text[1:]
        draw.text((cx, cy), strip_emojis(text), font=code_font, fill=color)
        cx += code_font.getlength(strip_emojis(text))
        
    # 文字区域 (更具设计感的排版)
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        title_font = ImageFont.truetype(font_path, 100)
        sub_font = ImageFont.truetype(font_path, 60)
        slogan_font = ImageFont.truetype(font_path, 32)
    except:
        title_font = sub_font = slogan_font = ImageFont.load_default()
        
    title_clean = strip_emojis(title)
    sub_clean = strip_emojis(subtitle)
    
    # 绘制主标题 (加一点字间距感)
    draw.text(((width - title_font.getlength(title_clean)) // 2, 860), title_clean, font=title_font, fill="#FFFFFF")
    
    # 绘制副标题 (使用更柔和的极客蓝)
    draw.text(((width - sub_font.getlength(sub_clean)) // 2, 1030), sub_clean, font=sub_font, fill="#79B8FF")
    
    # 装饰线
    line_w = 400
    draw.rectangle([(width-line_w)//2, 985, (width+line_w)//2, 988], fill="#333344")
    
    slogan = "Designed by MrQ × Xina"
    draw.text(((width - slogan_font.getlength(slogan)) // 2, 1320), slogan, font=slogan_font, fill="#444455")

    img.save(output_path)
    print(f"MEDIA:{output_path}")

def render_detail_page(title, lines, page_info, output_path):
    width, height = 1080, 1440
    img = Image.new('RGB', (width, height), '#0F0F12')
    draw = ImageDraw.Draw(img)
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    try:
        font_header = ImageFont.truetype(font_path, 36)
        font_regular = ImageFont.truetype(font_path, 42)
        font_footer = ImageFont.truetype(font_path, 30)
    except:
        font_header = font_regular = font_footer = ImageFont.load_default()

    draw.text((100, 80), page_info, font=font_header, fill="#555555")
    draw.rectangle([100, 140, 250, 145], fill='#58A6FF')
    
    y, x = 220, 100
    for line in lines:
        clean_line = strip_emojis(line)
        wrapped = get_wrapped_lines(clean_line, font_regular, width - 200)
        for w_line in wrapped:
            is_step = any(w_line.startswith(s) for s in ["1", "2", "3"])
            color = '#58A6FF' if is_step else '#FFFFFF'
            draw.text((x, y), w_line, font=font_regular, fill=color)
            y += 70
        y += 40

    slogan = "Designed by MrQ × Xina"
    draw.text(((width - font_footer.getlength(slogan)) // 2, 1320), slogan, font=font_footer, fill="#333333")
    img.save(output_path)
    print(f"MEDIA:{output_path}")

def paginate_content(text, font, content_width, max_y_start=220):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    pages, current_page, current_y = [], [], max_y_start
    for para in paragraphs:
        clean_para = strip_emojis(para)
        wrapped = get_wrapped_lines(clean_para, font, content_width)
        h = len(wrapped) * 70 + 40
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
    # Usage: python3 script.py "Title" "Subtitle" "content.txt" "output_dir"
    if len(sys.argv) < 5:
        print("Usage: python3 script.py <title> <subtitle> <content_path> <output_dir>")
        sys.exit(1)
        
    t, st, cp, od = sys.argv[1:5]
    if not os.path.exists(od): os.makedirs(od)
    
    render_designer_cover(t, st, os.path.join(od, "pro_cover.png"))
    
    with open(cp, 'r') as f:
        full_text = f.read()
    body_text = "\n".join([l for l in full_text.split('\n') if "标题" not in l and l.strip()])
    
    try:
        font_reg = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
    except:
        font_reg = ImageFont.load_default()
        
    pages = paginate_content(body_text, font_reg, 880)
    for i, p_lines in enumerate(pages):
        render_detail_page(t, p_lines, f"DEEP DIVE / {i+1} OF {len(pages)}", os.path.join(od, f"pro_detail_{i+1}.png"))
