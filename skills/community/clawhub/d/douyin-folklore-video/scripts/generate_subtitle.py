"""
生成同步字幕脚本
根据配音时长精确计算每句字幕时间
"""

import os
import sys


def generate_subtitle(duration, story_text, output_dir, pause=0.25):
    """
    生成同步字幕
    
    Args:
        duration: 配音时长（秒）
        story_text: 故事文案
        output_dir: 输出目录
        pause: 句间停顿（秒）
    
    Returns:
        str: 字幕文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 按行分割
    lines = [l.strip() for l in story_text.split('\n') if l.strip()]
    
    # 计算有效说话时间
    total_pause = pause * (len(lines) - 1)
    effective_duration = duration - total_pause
    
    # 根据字符数分配时间
    total_chars = sum(len(l) for l in lines)
    time_per_char = effective_duration / total_chars
    
    # 生成SRT字幕
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    
    srt_content = ""
    current_time = 0.0
    
    for i, line in enumerate(lines, 1):
        char_count = len(line)
        line_duration = char_count * time_per_char
        
        start_time = current_time
        end_time = current_time + line_duration
        
        srt_content += f"{i}\n"
        srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        srt_content += f"{line}\n\n"
        
        current_time = end_time + pause
    
    # 保存
    subtitle_path = os.path.join(output_dir, 'subtitle.srt')
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    return subtitle_path


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python generate_subtitle.py <duration> <story_text> <output_dir>')
        sys.exit(1)
    
    duration = float(sys.argv[1])
    story_text = sys.argv[2]
    output_dir = sys.argv[3]
    
    path = generate_subtitle(duration, story_text, output_dir)
    print(f"字幕已生成: {path}")