#!/usr/bin/env python3
"""
视频剪辑核心脚本 - 基于moviepy v2 + ffmpeg
支持：剪切/合并/添加文字/添加音乐/变速/转场/字幕
"""
import json
import os
import sys
from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ============ 工具函数 ============

def load_video(path):
    """加载视频文件"""
    return VideoFileClip(path)

def get_info(path):
    """获取视频信息"""
    clip = VideoFileClip(path)
    info = {
        "duration": clip.duration,
        "width": clip.w,
        "height": clip.h,
        "fps": clip.fps,
        "size_mb": round(os.path.getsize(path) / (1024*1024), 1)
    }
    clip.close()
    return info

def trim(path, start, end, output=None):
    """裁剪视频片段"""
    clip = VideoFileClip(path)
    trimmed = clip.subclipped(start, end)
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_trimmed{ext}"
    trimmed.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    trimmed.close()
    return output

def merge_videos(paths, output="merged.mp4"):
    """合并多个视频"""
    clips = [VideoFileClip(p) for p in paths]
    final = concatenate_videoclips(clips, method="chain")
    final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    for c in clips:
        c.close()
    final.close()
    return output

def add_text_to_video(path, text, position="bottom", font_size=40, output=None):
    """给视频添加文字（中文字体支持）"""
    clip = VideoFileClip(path)
    
    def make_text_frame(t):
        img = Image.new("RGBA", (clip.w, int(clip.h * 0.12)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = None
        for f in ["C:\\Windows\\Fonts\\msyhbd.ttc", "C:\\Windows\\Fonts\\simhei.ttf"]:
            if os.path.exists(f):
                font = ImageFont.truetype(f, font_size)
                break
        
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        x = (img.width - tw) // 2
        y = (img.height - th) // 2
        # 阴影
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 180))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        return np.array(img)
    
    txt_clip = VideoClip(make_text_frame, duration=clip.duration)
    
    if position == "top":
        txt_clip = txt_clip.with_position(("center", 20))
    elif position == "bottom":
        txt_clip = txt_clip.with_position(("center", clip.h - clip.h*0.12 - 20))
    elif position == "center":
        txt_clip = txt_clip.with_position("center")
    
    final = CompositeVideoClip([clip, txt_clip])
    
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_texted{ext}"
    
    final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    final.close()
    return output

def add_music(path, music_path, volume=0.3, output=None):
    """添加背景音乐"""
    clip = VideoFileClip(path)
    music = AudioFileClip(music_path).with_effects([vfx.MultiplyVolume(volume)])
    
    # 如果音乐比视频短就循环
    if music.duration < clip.duration:
        music = music.loop(duration=clip.duration)
    else:
        music = music.subclipped(0, clip.duration)
    
    # 混音：原声 + 背景音乐
    original_audio = clip.audio.with_effects([vfx.MultiplyVolume(0.8)])
    final_audio = CompositeAudioClip([original_audio, music])
    final = clip.with_audio(final_audio)
    
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_music{ext}"
    
    final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    final.close()
    return output

def speed_change(path, factor=1.5, output=None):
    """变速"""
    clip = VideoFileClip(path)
    sped = clip.with_effects([vfx.MultiplySpeed(factor)])
    
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_speed{ext}"
    
    sped.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    sped.close()
    return output

def resize(path, width=None, height=None, output=None):
    """调整尺寸（竖屏/横屏转换）"""
    clip = VideoFileClip(path)
    
    if width and height:
        resized = clip.resized((width, height))
    elif width:
        resized = clip.resized(width=width)
    elif height:
        resized = clip.resized(height=height)
    else:
        return path
    
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_resized{ext}"
    
    resized.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    resized.close()
    return output

def add_subtitles(path, subtitles, output=None):
    """
    添加字幕
    subtitles: [{"start":秒, "end":秒, "text":"文字"}, ...]
    """
    clip = VideoFileClip(path)
    
    font = None
    for f in ["C:\\Windows\\Fonts\\msyhbd.ttc", "C:\\Windows\\Fonts\\simhei.ttf"]:
        if os.path.exists(f):
            font = ImageFont.truetype(f, 36)
            break
    
    def make_sub_frame(t):
        img = Image.new("RGBA", (clip.w, int(clip.h * 0.08)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for sub in subtitles:
            if sub["start"] <= t < sub["end"]:
                bbox = draw.textbbox((0, 0), sub["text"], font=font)
                x = (img.width - (bbox[2]-bbox[0])) // 2
                y = (img.height - (bbox[3]-bbox[1])) // 2
                draw.text((x+2, y+2), sub["text"], font=font, fill=(0, 0, 0, 180))
                draw.text((x, y), sub["text"], font=font, fill=(255, 255, 255, 255))
                break
        
        return np.array(img)
    
    txt_clip = VideoClip(make_sub_frame, duration=clip.duration)
    txt_clip = txt_clip.with_position(("center", clip.h - clip.h*0.08 - 10))
    
    final = CompositeVideoClip([clip, txt_clip])
    
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_subtitle{ext}"
    
    final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    final.close()
    return output

def extract_audio(path, output=None):
    """提取音频"""
    clip = VideoFileClip(path)
    if not output:
        name, _ = os.path.splitext(path)
        output = f"{name}.mp3"
    clip.audio.write_audiofile(output, logger=None)
    clip.close()
    return output

def replace_audio(path, audio_path, output=None):
    """替换音频"""
    clip = VideoFileClip(path)
    new_audio = AudioFileClip(audio_path)
    if new_audio.duration > clip.duration:
        new_audio = new_audio.subclipped(0, clip.duration)
    final = clip.with_audio(new_audio)
    
    if not output:
        name, ext = os.path.splitext(path)
        output = f"{name}_reaud{ext}"
    
    final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
    clip.close()
    final.close()
    return output

def create_talk_video(text, duration=5, width=1080, height=1920, output="talk_video.mp4"):
    """生成纯文字讲解视频"""
    def make_frame(t):
        img = Image.new("RGB", (width, height), (26, 26, 46))
        draw = ImageDraw.Draw(img)
        
        font = None
        for f in ["C:\\Windows\\Fonts\\msyhbd.ttc", "C:\\Windows\\Fonts\\simhei.ttf"]:
            if os.path.exists(f):
                font = ImageFont.truetype(f, 50)
                break
        
        # 居中换行
        lines = []
        line = ""
        for char in text:
            bbox = draw.textbbox((0, 0), line + char, font=font)
            if bbox[2] - bbox[0] > width * 0.8:
                lines.append(line)
                line = char
            else:
                line += char
        lines.append(line)
        
        total_h = len(lines) * 70
        start_y = (height - total_h) // 2
        
        for i, l in enumerate(lines):
            bbox = draw.textbbox((0, 0), l, font=font)
            x = (width - (bbox[2]-bbox[0])) // 2
            draw.text((x, start_y + i*70), l, font=font, fill=(255, 255, 255))
        
        return np.array(img)
    
    clip = VideoClip(make_frame, duration=duration)
    clip.write_videofile(output, fps=15, codec="libx264", audio=False, logger=None)
    clip.close()
    return output

# ============ CLI入口 ============
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "commands": {
                "info": "python video_editor.py info <path>",
                "trim": "python video_editor.py trim <path> <start_sec> <end_sec> [output]",
                "merge": "python video_editor.py merge [path1 path2 ...] -o merged.mp4",
                "text": "python video_editor.py text <path> <文字> [position] [output]",
                "music": "python video_editor.py music <video> <audio> [volume] [output]",
                "speed": "python video_editor.py speed <path> <factor> [output]",
                "resize": "python video_editor.py resize <path> --width 1080 --height 1920",
                "subtitles": "python video_editor.py subtitles <path> <subtitles.json> [output]",
                "audio": "python video_editor.py audio <path> [output.mp3]",
                "replace_audio": "python video_editor.py replace_audio <video> <audio> [output]",
                "talk": "python video_editor.py talk <文字> [duration] [output]"
            }
        }, ensure_ascii=False))
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "info" and len(sys.argv) >= 3:
            print(json.dumps(get_info(sys.argv[2])))
        
        elif cmd == "trim" and len(sys.argv) >= 5:
            out = trim(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5] if len(sys.argv) > 5 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "merge":
            paths = [a for a in sys.argv[2:] if not a.startswith("-o=")]
            output = "merged.mp4"
            for a in sys.argv[2:]:
                if a.startswith("-o="):
                    output = a[3:]
            out = merge_videos(paths, output)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "text" and len(sys.argv) >= 4:
            pos = sys.argv[4] if len(sys.argv) >= 5 else "bottom"
            out = add_text_to_video(sys.argv[2], sys.argv[3], pos, 
                                   output=sys.argv[5] if len(sys.argv) >= 6 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "music" and len(sys.argv) >= 4:
            vol = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.3
            out = add_music(sys.argv[2], sys.argv[3], vol, 
                          output=sys.argv[5] if len(sys.argv) >= 6 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "speed" and len(sys.argv) >= 4:
            out = speed_change(sys.argv[2], float(sys.argv[3]), 
                             output=sys.argv[4] if len(sys.argv) >= 5 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "resize" and len(sys.argv) >= 3:
            w = None; h = None
            for a in sys.argv[3:]:
                if a.startswith("--width="): w = int(a[8:])
                if a.startswith("--height="): h = int(a[9:])
            out = resize(sys.argv[2], w, h)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "subtitles" and len(sys.argv) >= 4:
            with open(sys.argv[3], 'r') as f:
                subs = json.load(f)
            out = add_subtitles(sys.argv[2], subs,
                              output=sys.argv[4] if len(sys.argv) >= 5 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "audio" and len(sys.argv) >= 3:
            out = extract_audio(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "replace_audio" and len(sys.argv) >= 4:
            out = replace_audio(sys.argv[2], sys.argv[3],
                              output=sys.argv[4] if len(sys.argv) >= 5 else None)
            print(json.dumps({"output": out, "ok": True}))
        
        elif cmd == "talk" and len(sys.argv) >= 3:
            dur = float(sys.argv[3]) if len(sys.argv) >= 4 else 5
            out = create_talk_video(sys.argv[2], dur, 
                                  output=sys.argv[4] if len(sys.argv) >= 5 else "talk_video.mp4")
            print(json.dumps({"output": out, "ok": True}))
        
        else:
            print(json.dumps({"error": f"未知命令或参数不足: {cmd}"}))
            
    except Exception as e:
        print(json.dumps({"error": str(e)}))
