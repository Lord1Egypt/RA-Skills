#!/usr/bin/env python3
"""课件自动生产线主构建脚本
用法: python3 build.py --input 文案.txt --output 课件视频.mp4
"""
import sys, os, json, subprocess, re, tempfile, argparse

def parse_args():
    parser = argparse.ArgumentParser(description='课件自动生产线')
    parser.add_argument('--input', '-i', required=True, help='文案路径')
    parser.add_argument('--output', '-o', default='output.mp4', help='输出视频路径')
    parser.add_argument('--style', default='dark', choices=['dark', 'light', 'gradient'])
    parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural')
    parser.add_argument('--digital-human', default=None, help='数字人照片路径')
    parser.add_argument('--width', type=int, default=1920)
    parser.add_argument('--height', type=int, default=1080)
    return parser.parse_args()

def analyze_script(path):
    """分析文案，分页"""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    
    # 按段落分页
    paragraphs = [p.strip() for p in re.split(r'\n\n+', text) if p.strip()]
    
    pages = []
    for p in paragraphs:
        lines = p.split('\n')
        code_blocks = []
        normal_lines = []
        in_code = False
        code_buf = []
        
        for line in lines:
            if line.startswith('```'):
                if in_code:
                    code_blocks.append('\n'.join(code_buf))
                    code_buf = []
                    in_code = False
                else:
                    in_code = True
                continue
            if in_code:
                code_buf.append(line)
            else:
                normal_lines.append(line)
        
        if code_blocks:
            pages.append(('code', '\n'.join(normal_lines[:2]), '\n'.join(code_blocks)))
        elif normal_lines:
            title = normal_lines[0] if normal_lines else ''
            content = '\n'.join(normal_lines[1:]) if len(normal_lines)>1 else title
            pages.append(('bullet', title, content))
    
    return pages

def generate_tts(text, voice, output):
    """生成TTS配音"""
    subprocess.run([
        "edge-tts", "--voice", voice,
        "--text", text,
        "--write-media", output
    ], check=True, timeout=120)
    
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", output],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def generate_subtitles(text, duration_sec, output):
    """生成字幕"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    total_chars = sum(len(l) for l in lines)
    
    with open(output, 'w', encoding='utf-8') as f:
        current_time = 0.0
        for i, line in enumerate(lines, 1):
            line_dur = max(2.0, (len(line) / max(total_chars, 1)) * duration_sec)
            end = min(current_time + line_dur, duration_sec)
            
            def ts(t):
                h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t%1)*1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
            f.write(f"{i}\n{ts(current_time)} --> {ts(end)}\n{line}\n\n")
            current_time = end

def generate_slides(pages, out_dir):
    """生成幻灯片"""
    # 导入video-craft-pro的zh-slides
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'video-craft-pro', 'scripts'))
    
    try:
        from zh_slides import make_slides
    except ImportError:
        # 内置简易版
        from PIL import Image, ImageDraw, ImageFont
        
        FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        
        if not os.path.exists(FONT):
            FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
            FONT_B = FONT
        
        def make_slides(out, slides):
            W, H = 1920, 1080
            BG, ACCENT, WHITE, GRAY = (15,15,30), (100,200,255), (230,230,240), (100,100,120)
            
            ft_big = ImageFont.truetype(FONT_B, 76)
            ft_bold = ImageFont.truetype(FONT_B, 60)
            ft_reg = ImageFont.truetype(FONT, 32)
            ft_code = ImageFont.truetype(FONT, 24)
            
            os.makedirs(out, exist_ok=True)
            
            for idx, (ctype, title, content) in enumerate(slides):
                img = Image.new('RGB', (W, H), BG)
                d = ImageDraw.Draw(img)
                
                if ctype == 'title':
                    d.text((W//2, H//2-60), title, fill=WHITE, font=ft_big, anchor="mm")
                    d.text((W//2, H//2+50), content, fill=GRAY, font=ft_reg, anchor="mm")
                elif ctype == 'bullet':
                    d.text((80, 40), title, fill=ACCENT, font=ft_bold)
                    d.line([(80,95),(400,95)], fill=ACCENT, width=2)
                    for i, line in enumerate(content.split('\n')):
                        d.text((100, 150+i*45), line, fill=WHITE, font=ft_reg)
                elif ctype == 'code':
                    d.text((80, 40), title, fill=ACCENT, font=ft_bold)
                    d.line([(80,95),(400,95)], fill=ACCENT, width=2)
                    lines = content.split('\n')
                    h = len(lines)*30+30
                    d.rectangle([80,140,1840,140+h], fill=(20,25,45), outline=(40,50,80))
                    for i, line in enumerate(lines):
                        c = ACCENT if line.strip().startswith('#') else WHITE
                        d.text((100, 150+i*30), line, fill=c, font=ft_code)
                
                img.save(os.path.join(out, f"slide_{idx:02d}.png"))
            return len(slides)
    
    # 转换pages格式为slides
    slides_config = []
    for ptype, title, content in pages:
        if ptype == 'code':
            slides_config.append(('code', title, content))
        else:
            slides_config.append(('bullet', title, content))
    
    n = make_slides(out_dir, slides_config)
    return n

def compose_video(slides_dir, audio_path, output_path, duration):
    """合成最终视频"""
    # 生成concat文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# concat\n")
        slides = sorted(os.listdir(slides_dir))
        total = len(slides)
        slide_dur = duration / total
        
        for s in slides:
            f.write(f"file '{os.path.join(slides_dir, s)}'\n")
            f.write(f"duration {slide_dur}\n")
        f.write(f"file '{os.path.join(slides_dir, slides[-1])}'\n")
        concat_file = f.name
    
    slides_video = output_path + ".slides.mp4"
    
    # 生成幻灯片视频
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264", "-preset", "medium",
        "-crf", "23", "-pix_fmt", "yuv420p",
        "-r", "10",
        slides_video
    ], check=True, capture_output=True)
    
    # 裁剪到音频长度
    slides_trim = output_path + ".trim.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", slides_video,
        "-t", str(duration), "-c", "copy",
        slides_trim
    ], check=True, capture_output=True)
    
    # 合成最终视频
    subprocess.run([
        "ffmpeg", "-y",
        "-i", slides_trim,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v",
        "-map", "1:a",
        output_path
    ], check=True, capture_output=True)
    
    # 清理
    os.unlink(concat_file)
    os.unlink(slides_video)
    os.unlink(slides_trim)
    
    return output_path

def main():
    args = parse_args()
    print(f"📖 读取文案: {args.input}")
    
    # 1. 分析文案
    pages = analyze_script(args.input)
    print(f"📄 分页: {len(pages)}页")
    
    # 2. 提取所有文本用于TTS
    full_text = open(args.input, encoding='utf-8').read()
    # 去掉代码块标记
    full_text_clean = re.sub(r'```.*?\n', '', full_text)
    full_text_clean = re.sub(r'\n```', '', full_text_clean)
    full_text_clean = re.sub(r'^#+\s*', '', full_text_clean, flags=re.MULTILINE)
    
    with tempfile.TemporaryDirectory() as tmp:
        # 3. 生成TTS
        audio_path = os.path.join(tmp, "audio.mp3")
        print(f"🎤 生成配音 ({args.voice})...")
        duration = generate_tts(full_text_clean[:2000], args.voice, audio_path)  # edge-tts限制
        print(f"   时长: {duration:.0f}秒")
        
        # 4. 生成字幕
        srt_path = os.path.join(tmp, "subtitles.srt")
        generate_subtitles(full_text_clean, duration, srt_path)
        print(f"📝 字幕生成")
        
        # 5. 生成幻灯片
        slides_dir = os.path.join(tmp, "slides")
        n = generate_slides(pages, slides_dir)
        print(f"🖼️  幻灯片: {n}张")
        
        # 6. 合成视频
        print(f"🎬 合成视频...")
        compose_video(slides_dir, audio_path, args.output, duration)
        
        # 7. 数字人（可选）
        if args.digital_human:
            print(f"👤 数字人驱动: {args.digital_human}")
            print("   (飞影数字人MCP待配置时启用)")
        
        sz = os.path.getsize(args.output)
        print(f"✅ 课件视频完成! {sz/1024/1024:.1f}MB, {duration:.0f}秒")

if __name__ == '__main__':
    main()
