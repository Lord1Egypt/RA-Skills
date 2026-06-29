#!/usr/bin/env python3
"""
GEO 视频拼接 + 混音脚本
将所有生成的短视频拼接为一条，并添加背景音乐
"""

import subprocess
import os
import sys
import glob
import argparse
from pathlib import Path

def get_video_duration(filepath):
    """用 ffprobe 获取视频时长（秒）"""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    import json
    info = json.loads(result.stdout)
    return float(info['format']['duration'])

def generate_bgm(duration, output_path):
    """用 ffmpeg lavfi 生成简单的正弦波背景音乐"""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', f'sine=frequency=440:duration={duration}',
        '-af', 'volume=0.15,afade=t=in:st=0:d=2,afade=t=out:st={start}:d=2'.format(
            duration=duration, start=max(0, duration-2)
        ),
        output_path
    ]
    print(f"生成背景音乐: {output_path}")
    subprocess.run(cmd, capture_output=True)

def concat_videos(video_files, output_path):
    """拼接多个视频文件"""
    # 生成 concat list 文件
    list_file = output_path.parent / 'concat-list.txt'
    with open(list_file, 'w', encoding='utf-8') as f:
        for vf in video_files:
            f.write(f"file '{Path(vf).as_posix()}'\n")
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', str(list_file),
        '-c', 'copy',
        str(output_path)
    ]
    print(f"拼接视频: {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"拼接失败: {result.stderr}")
        return False
    return True

def mix_audio(video_path, bgm_path, output_path):
    """将背景音乐混入视频"""
    duration = get_video_duration(str(video_path))
    fade_out_start = max(0, duration - 2)
    
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-i', str(bgm_path),
        '-filter_complex',
        f'[1:a]volume=0.15,afade=t=in:st=0:d=2,afade=t=out:st={fade_out_start}:d=2[bgm];'
        f'[0:a][bgm]amix=inputs=2:duration=first[aout]',
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-shortest',
        str(output_path)
    ]
    print(f"混音: {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"混音失败: {result.stderr}")
        return False
    return True

def compress_video(input_path, output_path):
    """压缩视频（用于平台上传）"""
    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_path),
        '-c:v', 'libx264', '-crf', '26', '-preset', 'medium',
        '-c:a', 'aac', '-b:a', '128k',
        str(output_path)
    ]
    print(f"压缩视频: {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"压缩失败: {result.stderr}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='GEO 视频拼接+混音工具')
    parser.add_argument('--input-dir', default='doubao-output',
                        help='输入视频目录（默认: douba-output）')
    parser.add_argument('--output', default='doubao-output/geo-final-combined.mp4',
                        help='输出文件路径')
    parser.add_argument('--skip-bgm', action='store_true',
                        help='跳过背景音乐生成')
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    # 查找所有 geo-video-*.mp4 文件
    video_files = sorted(input_dir.glob('geo-video-*.mp4'))
    if not video_files:
        print(f"❌ 未找到视频文件: {input_dir}/geo-video-*.mp4")
        sys.exit(1)
    
    print(f"找到 {len(video_files)} 个视频文件:")
    for vf in video_files:
        dur = get_video_duration(str(vf))
        print(f"  - {vf.name} ({dur:.1f}s)")
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Step 1: 拼接视频
    concat_path = output_path.parent / 'geo-final-concat.mp4'
    if not concat_videos(video_files, concat_path):
        sys.exit(1)
    print(f"✅ 拼接完成: {concat_path}")
    
    # Step 2: 生成背景音乐
    if not args.skip_bgm:
        total_duration = get_video_duration(str(concat_path))
        bgm_path = output_path.parent / 'bgm.wav'
        generate_bgm(total_duration, str(bgm_path))
        print(f"✅ 背景音乐生成: {bgm_path}")
        
        # Step 3: 混音
        if not mix_audio(concat_path, bgm_path, output_path):
            sys.exit(1)
        print(f"✅ 混音完成: {output_path}")
        
        # Step 4: 压缩
        sm_path = output_path.parent / 'geo-final-combined-sm.mp4'
        if not compress_video(output_path, sm_path):
            print("⚠️ 压缩失败，但完整版可用")
        else:
            print(f"✅ 压缩完成: {sm_path}")
    else:
        # 跳过 BGM，直接压缩拼接后的视频
        if not compress_video(concat_path, output_path):
            print("⚠️ 压缩失败")
        else:
            print(f"✅ 完成（无BGM）: {output_path}")
    
    print("\n🎉 全部完成！")
    print(f"最终文件: {output_path}")
    sm_path = output_path.parent / 'geo-final-combined-sm.mp4'
    if sm_path.exists():
        print(f"压缩版: {sm_path}")

if __name__ == '__main__':
    main()
