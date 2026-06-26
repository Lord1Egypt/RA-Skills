#!/usr/bin/env python3
"""
音视频转文字脚本
使用 OpenAI Whisper 进行语音识别

用法:
    python transcribe.py <输入文件> [输出文件] [选项]

选项:
    --model <模型名>     选择模型：tiny, base, small, medium, large (默认：base)
    --language <语言>    指定语言代码，如 zh, en, ja (默认：自动检测)
    --output-format     输出格式：txt, srt, vtt, json (默认：txt)
    --device <设备>      运行设备：cpu, cuda (默认：cpu)

依赖:
    pip install openai-whisper ffmpeg-python
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path


def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing = []
    
    try:
        import whisper
    except ImportError:
        missing.append("openai-whisper")
    
    try:
        import ffmpeg
    except ImportError:
        missing.append("ffmpeg-python")
    
    if missing:
        print(f"错误：缺少依赖项：{', '.join(missing)}")
        print(f"请运行：pip install {' '.join(missing)}")
        sys.exit(1)
    
    # 检查 ffmpeg 是否安装
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误：ffmpeg 未安装")
        print("请安装 ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: 从 https://ffmpeg.org/download.html 下载")
        sys.exit(1)


def extract_audio(input_file, temp_audio="/tmp/audio_extract.wav"):
    """从视频文件中提取音频"""
    try:
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1",
            "-y", temp_audio
        ], check=True, capture_output=True)
        return temp_audio
    except subprocess.CalledProcessError as e:
        print(f"音频提取失败：{e.stderr.decode()}")
        sys.exit(1)


def transcribe(audio_file, model_name="base", language=None, device="cpu"):
    """执行语音识别"""
    import whisper
    
    print(f"加载模型：{model_name}...")
    model = whisper.load_model(model_name, device=device)
    
    print("开始转录...")
    options = {}
    if language:
        options["language"] = language
    
    result = model.transcribe(audio_file, **options)
    return result


def format_output(result, output_format="txt", output_file=None):
    """格式化输出结果"""
    if output_format == "txt":
        text = result["text"]
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"文本已保存到：{output_file}")
        else:
            print(text)
        return text
    
    elif output_format == "srt":
        srt_content = ""
        for i, segment in enumerate(result["segments"], 1):
            start = format_time_srt(segment["start"])
            end = format_time_srt(segment["end"])
            text = segment["text"].strip()
            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(srt_content)
            print(f"SRT 字幕已保存到：{output_file}")
        else:
            print(srt_content)
        return srt_content
    
    elif output_format == "vtt":
        vtt_content = "WEBVTT\n\n"
        for segment in result["segments"]:
            start = format_time_vtt(segment["start"])
            end = format_time_vtt(segment["end"])
            text = segment["text"].strip()
            vtt_content += f"{start} --> {end}\n{text}\n\n"
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(vtt_content)
            print(f"VTT 字幕已保存到：{output_file}")
        else:
            print(vtt_content)
        return vtt_content
    
    elif output_format == "json":
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"JSON 结果已保存到：{output_file}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    
    else:
        print(f"不支持的输出格式：{output_format}")
        sys.exit(1)


def format_time_srt(seconds):
    """将秒数转换为 SRT 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_time_vtt(seconds):
    """将秒数转换为 VTT 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def main():
    parser = argparse.ArgumentParser(description="音视频转文字工具")
    parser.add_argument("input", help="输入的音视频文件路径")
    parser.add_argument("output", nargs="?", help="输出文件路径（可选）")
    parser.add_argument("--model", default="base", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper 模型大小（默认：base）")
    parser.add_argument("--language", help="语言代码，如 zh, en, ja（默认：自动检测）")
    parser.add_argument("--output-format", default="txt",
                        choices=["txt", "srt", "vtt", "json"],
                        help="输出格式（默认：txt）")
    parser.add_argument("--device", default="cpu",
                        choices=["cpu", "cuda"],
                        help="运行设备（默认：cpu）")
    parser.add_argument("--keep-audio", action="store_true",
                        help="保留临时音频文件")
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误：文件不存在：{args.input}")
        sys.exit(1)
    
    # 检查依赖
    check_dependencies()
    
    # 确定输出文件
    if args.output:
        output_file = args.output
    else:
        base_name = Path(args.input).stem
        ext = args.output_format
        output_file = f"{base_name}.{ext}"
    
    # 检查是否需要提取音频
    input_ext = Path(args.input).suffix.lower()
    audio_extensions = [".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"]
    
    if input_ext in audio_extensions:
        audio_file = args.input
    else:
        print("检测到视频文件，正在提取音频...")
        audio_file = extract_audio(args.input)
    
    try:
        # 执行转录
        result = transcribe(
            audio_file,
            model_name=args.model,
            language=args.language,
            device=args.device
        )
        
        # 输出结果
        format_output(result, args.output_format, output_file)
        
    finally:
        # 清理临时文件
        if audio_file != args.input and not args.keep_audio:
            try:
                os.remove(audio_file)
            except:
                pass


if __name__ == "__main__":
    main()
