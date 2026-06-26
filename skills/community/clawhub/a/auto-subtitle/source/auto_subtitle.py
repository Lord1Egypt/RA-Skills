#!/usr/bin/env python3
"""
video-transcriber - 视频自动字幕生成器
批量为视频生成字幕文件（SRT/VTT），结合视频帧提取和语音转文字
"""

import os
import sys
import argparse
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

VERSION = "1.0.0"
BACKUP_DIR = ".video_subtitle_generator_backup"
LOG_FILE = ".video_subtitle_generator_log.json"

try:
    from openai import OpenAI
except ImportError:
    print("❌ 错误：未安装 openai 库，请运行：pip install openai")
    sys.exit(1)

def check_ffmpeg():
    """检查 ffmpeg 是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_files(directory, extensions, recursive=False):
    """获取目录下所有视频文件"""
    video_extensions = {ext.lower() for ext in extensions}
    video_files = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                ext = Path(file).suffix.lower().lstrip('.')
                if ext in video_extensions:
                    video_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                ext = Path(file).suffix.lower().lstrip('.')
                if ext in video_extensions:
                    video_files.append(os.path.join(directory, file))
    
    return sorted(video_files)

def extract_audio(video_path, temp_dir):
    """从视频中提取音频"""
    audio_path = os.path.join(temp_dir, f"{Path(video_path).stem}.wav")
    
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-y", audio_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        print(f"    ❌ 音频提取失败：{e}")
        return None

def transcribe_audio(audio_path, client, args):
    """使用 OpenAI Whisper API 转录音频"""
    try:
        with open(audio_path, "rb") as audio_file:
            kwargs = {
                "model": "whisper-1",
                "file": audio_file,
                "response_format": "verbose_json"
            }
            
            if args.language:
                kwargs["language"] = args.language
            if args.task:
                kwargs["task"] = args.task
            if args.prompt:
                kwargs["prompt"] = args.prompt
            
            transcript = client.audio.transcriptions.create(**kwargs)
            return transcript
    except Exception as e:
        print(f"    ❌ 转录失败：{e}")
        return None

def format_srt(segments):
    """格式化为 SRT 字幕"""
    srt_content = ""
    for i, seg in enumerate(segments, 1):
        start = timedelta(seconds=seg["start"])
        end = timedelta(seconds=seg["end"])
        start_str = str(start).replace('.', ',')[:12]
        end_str = str(end).replace('.', ',')[:12]
        text = seg["text"].strip()
        srt_content += f"{i}\n{start_str} --> {end_str}\n{text}\n\n"
    return srt_content

def format_vtt(segments):
    """格式化为 VTT 字幕"""
    vtt_content = "WEBVTT\n\n"
    for seg in segments:
        start = timedelta(seconds=seg["start"])
        end = timedelta(seconds=seg["end"])
        start_str = str(start)[:12]
        end_str = str(end)[:12]
        text = seg["text"].strip()
        vtt_content += f"{start_str} --> {end_str}\n{text}\n\n"
    return vtt_content

def backup_files(files, backup_dir):
    """备份文件"""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_backup_dir = os.path.join(backup_dir, timestamp)
    os.makedirs(session_backup_dir)
    
    backup_map = {}
    for file_path in files:
        if os.path.exists(file_path):
            rel_path = os.path.relpath(file_path)
            backup_path = os.path.join(session_backup_dir, rel_path)
            backup_subdir = os.path.dirname(backup_path)
            if not os.path.exists(backup_subdir):
                os.makedirs(backup_subdir, exist_ok=True)
            shutil.copy2(file_path, backup_path)
            backup_map[file_path] = backup_path
    
    return session_backup_dir, backup_map

def save_log(session_backup_dir, backup_map, operations):
    """保存操作日志"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "session_backup_dir": session_backup_dir,
        "backup_map": backup_map,
        "operations": operations
    }
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def undo_last_operation():
    """撤销上次操作"""
    if not os.path.exists(LOG_FILE):
        print("❌ 没有找到操作日志，无法撤销")
        return False
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    session_backup_dir = log_data.get("session_backup_dir")
    backup_map = log_data.get("backup_map", {})
    
    if not os.path.exists(session_backup_dir):
        print(f"❌ 备份目录不存在：{session_backup_dir}")
        return False
    
    print(f"🔄 正在撤销上次操作...")
    restored_count = 0
    for original_path, backup_path in backup_map.items():
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, original_path)
            print(f"  ✅ 已恢复：{original_path}")
            restored_count += 1
    
    print(f"\n🎉 撤销完成！共恢复 {restored_count} 个文件")
    return True

def main():
    parser = argparse.ArgumentParser(
        description=f"video-subtitle-generator v{VERSION} - 视频自动字幕生成器"
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="要处理的目录（默认：当前目录）"
    )
    parser.add_argument(
        "--language", "-l",
        help="音频语言（ISO 639-1 格式，如 zh, en, ja）"
    )
    parser.add_argument(
        "--task", "-t",
        choices=["transcribe", "translate"],
        help="任务类型：transcribe（转录）或 translate（翻译）"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["srt", "vtt"],
        default="srt",
        help="字幕格式（默认：srt）"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="提示词，帮助提高识别准确率"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="递归处理子文件夹"
    )
    parser.add_argument(
        "--preview", "-P",
        action="store_true",
        help="预览模式，不实际生成文件"
    )
    parser.add_argument(
        "--undo", "-u",
        action="store_true",
        help="撤销上次操作"
    )
    parser.add_argument(
        "--output-dir",
        help="输出目录（不与视频同目录）"
    )
    parser.add_argument(
        "--extensions",
        default="mp4,avi,mov,mkv,webm",
        help="要处理的文件扩展名，逗号分隔（默认：mp4,avi,mov,mkv,webm）"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"video-subtitle-generator v{VERSION}"
    )
    
    args = parser.parse_args()
    
    # 撤销操作
    if args.undo:
        undo_last_operation()
        return
    
    # 检查 ffmpeg
    if not check_ffmpeg():
        print("❌ 错误：未找到 ffmpeg，请先安装 ffmpeg")
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   macOS: brew install ffmpeg")
        sys.exit(1)
    
    # 检查 API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 OPENAI_API_KEY 环境变量")
        print("   请运行：export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    # 获取视频文件
    extensions = [ext.strip() for ext in args.extensions.split(',')]
    video_files = get_video_files(args.directory, extensions, args.recursive)
    
    if not video_files:
        print(f"❌ 在目录 '{args.directory}' 中没有找到视频文件")
        return
    
    print(f"🎬 找到 {len(video_files)} 个视频文件\n")
    
    # 预览模式
    if args.preview:
        print("📋 预览模式 - 以下是将要进行的操作：\n")
        for file_path in video_files:
            print(f"  • {os.path.relpath(file_path)}")
            subtitle_path = f"{os.path.splitext(file_path)[0]}.{args.format}"
            print(f"    → 生成字幕：{os.path.relpath(subtitle_path)}")
            if args.language:
                print(f"    - 语言：{args.language}")
            if args.task:
                print(f"    - 任务：{args.task}")
            print()
        print("💡 去掉 --preview 参数来执行实际操作")
        return
    
    # 创建临时目录
    temp_dir = os.path.join(args.directory, ".video_subtitle_generator_temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # 确定需要备份的文件（已存在的字幕文件）
    files_to_backup = []
    for video_path in video_files:
        subtitle_path = f"{os.path.splitext(video_path)[0]}.{args.format}"
        if os.path.exists(subtitle_path):
            files_to_backup.append(subtitle_path)
    
    # 备份文件
    if files_to_backup:
        print(f"💾 正在备份 {len(files_to_backup)} 个已有字幕文件...")
        session_backup_dir, backup_map = backup_files(files_to_backup, BACKUP_DIR)
        print(f"   备份位置：{session_backup_dir}\n")
    else:
        session_backup_dir = None
        backup_map = {}
    
    # 处理视频
    print("🔧 正在处理视频...\n")
    operations = []
    success_count = 0
    
    for i, video_path in enumerate(video_files, 1):
        rel_path = os.path.relpath(video_path)
        print(f"[{i}/{len(video_files)}] 处理：{rel_path}")
        
        # 提取音频
        print("    提取音频...")
        audio_path = extract_audio(video_path, temp_dir)
        if not audio_path:
            operations.append({
                "video": video_path,
                "success": False,
                "error": "音频提取失败"
            })
            continue
        
        # 转录音频
        print("    语音转文字...")
        transcript = transcribe_audio(audio_path, client, args)
        if not transcript:
            operations.append({
                "video": video_path,
                "success": False,
                "error": "转录失败"
            })
            os.remove(audio_path)
            continue
        
        # 生成字幕
        segments = [{"start": s.start, "end": s.end, "text": s.text} for s in transcript.segments]
        
        if args.format == "srt":
            subtitle_content = format_srt(segments)
        else:
            subtitle_content = format_vtt(segments)
        
        # 确定输出路径
        if args.output_dir:
            rel_video = os.path.relpath(video_path, args.directory)
            output_path = os.path.join(args.output_dir, f"{os.path.splitext(rel_video)[0]}.{args.format}")
            output_subdir = os.path.dirname(output_path)
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir, exist_ok=True)
        else:
            output_path = f"{os.path.splitext(video_path)[0]}.{args.format}"
        
        # 保存字幕
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(subtitle_content)
        
        operations.append({
            "video": video_path,
            "subtitle": output_path,
            "success": True,
            "segments": len(segments)
        })
        
        success_count += 1
        print(f"    ✅ 成功！生成 {len(segments)} 条字幕 → {os.path.relpath(output_path)}")
        
        # 清理临时音频文件
        os.remove(audio_path)
    
    # 清理临时目录
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # 保存日志
    if session_backup_dir:
        save_log(session_backup_dir, backup_map, operations)
    
    # 总结
    print(f"\n{'='*60}")
    print(f"📊 处理完成！")
    print(f"   成功：{success_count}/{len(video_files)}")
    
    if session_backup_dir:
        print(f"\n💡 如需撤销，运行：{os.path.basename(__file__)} --undo")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
