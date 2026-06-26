#!/usr/bin/env python3
"""
faster-whisper 转录命令行工具
基于 CTranslate2 后端的高性能语音转文字
"""

import sys
import json
import argparse
from pathlib import Path

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("错误: 未安装 faster-whisper", file=sys.stderr)
    print("请运行安装脚本: ./setup.sh", file=sys.stderr)
    sys.exit(1)


def check_cuda_available():
    """检查 CUDA 是否可用并返回设备信息。"""
    try:
        import torch
        if torch.cuda.is_available():
            return True, torch.cuda.get_device_name(0)
        return False, None
    except ImportError:
        return False, None


def main():
    parser = argparse.ArgumentParser(
        description="使用 faster-whisper 转录音频文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基本中文转录
  %(prog)s 音频文件.mp3 --language zh
  
  # 使用 GPU 加速
  %(prog)s 音频文件.mp3 --device cuda --compute-type float16
  
  # 英文转录，包含词级时间戳
  %(prog)s 音频文件.mp3 --language en --word-timestamps
  
  # 快速 CPU 转录
  %(prog)s 音频文件.mp3 --device cpu --compute-type int8 --model distil-large-v3
  
  # 输出到文件
  %(prog)s 音频文件.mp3 --output 转录结果.txt

支持格式: mp3, wav, m4a, flac, ogg, webm
        """
    )
    parser.add_argument(
        "audio",
        metavar="音频文件",
        help="音频文件路径 (支持 mp3, wav, m4a, flac, ogg, webm)"
    )
    parser.add_argument(
        "-m", "--model",
        default="large-v3-turbo",
        metavar="模型名称",
        help="使用的 Whisper 模型 (默认: large-v3-turbo)。选项: tiny, base, small, medium, large-v3, large-v3-turbo, distil-large-v3, distil-medium.en"
    )
    parser.add_argument(
        "-l", "--language",
        default="zh",
        metavar="语言代码",
        help="语言代码，如 zh, en, es, fr (如果省略则自动检测)"
    )
    parser.add_argument(
        "--word-timestamps",
        action="store_true",
        help="在输出中包含词级时间戳"
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        metavar="N",
        help="束搜索大小；值越高越准确但越慢 (默认: 5)"
    )
    parser.add_argument(
        "--vad",
        action="store_true",
        help="启用语音活动检测以跳过静音部分"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="以 JSON 格式输出完整转录结果，包含分段和元数据"
    )
    parser.add_argument(
        "-o", "--output",
        metavar="输出文件",
        help="将转录结果写入文件而不是标准输出"
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["auto", "cpu", "cuda"],
        help="计算设备: auto (自动检测GPU), cpu, 或 cuda (默认: cpu)"
    )
    parser.add_argument(
        "--compute-type",
        default="auto",
        choices=["auto", "int8", "float16", "float32"],
        help="量化类型: auto, int8 (快速CPU), float16 (GPU), float32 (默认: auto)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="抑制进度和状态消息"
    )

    args = parser.parse_args()

    # 验证音频文件
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"错误: 未找到音频文件: {args.audio}", file=sys.stderr)
        sys.exit(1)

    # 自动检测设备和计算类型
    device = args.device
    compute_type = args.compute_type

    cuda_available, gpu_name = check_cuda_available()

    if device == "auto":
        if cuda_available:
            device = "cuda"
        else:
            device = "cpu"
            # 如果没有 CUDA 但未明确请求 CPU，则发出警告
            if not args.quiet:
                print("⚠️  未检测到 CUDA — 使用 CPU（速度会较慢！）", file=sys.stderr)
                print("   要启用 GPU: pip install torch --index-url https://download.pytorch.org/whl/cu121", file=sys.stderr)
                print("   或重新运行: ./setup.sh", file=sys.stderr)
                print("", file=sys.stderr)

    if compute_type == "auto":
        # 根据设备优化
        if device == "cuda":
            compute_type = "float16"  # GPU 最佳选择
        else:
            compute_type = "int8"  # CPU 最佳选择（4倍加速）

    if not args.quiet:
        if device == "cuda" and gpu_name:
            print(f"正在加载模型: {args.model} ({device}, {compute_type}) 在 {gpu_name} 上", file=sys.stderr)
        else:
            print(f"正在加载模型: {args.model} ({device}, {compute_type})", file=sys.stderr)

    # 加载模型
    try:
        model = WhisperModel(
            args.model,
            device=device,
            compute_type=compute_type
        )
    except Exception as e:
        print(f"加载模型时出错: {e}", file=sys.stderr)
        sys.exit(1)

    # 转录
    try:
        if not args.quiet:
            print(f"正在转录: {audio_path.name}", file=sys.stderr)

        segments, info = model.transcribe(
            str(audio_path),
            language=args.language if args.language != "auto" else None,
            beam_size=args.beam_size,
            word_timestamps=args.word_timestamps,
            vad_filter=args.vad
        )

        if not args.quiet:
            print(f"检测到语言: {info.language} (概率: {info.language_probability:.2f})", file=sys.stderr)

        # 收集结果
        full_text = ""
        segments_list = []

        for segment in segments:
            segment_text = segment.text.strip()
            full_text += segment_text + " "
            
            segment_dict = {
                "start": segment.start,
                "end": segment.end,
                "text": segment_text
            }
            
            if args.word_timestamps and segment.words:
                segment_dict["words"] = [
                    {
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    }
                    for word in segment.words
                ]
            
            segments_list.append(segment_dict)
            
            # 如果不是 JSON 输出，则实时显示
            if not args.json and not args.quiet:
                print(f"[{segment.start:.2f} --> {segment.end:.2f}] {segment_text}")

        full_text = full_text.strip()

        # 输出结果
        if args.json:
            result = {
                "text": full_text,
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "segments": segments_list,
                "model": args.model,
                "device": device,
                "compute_type": compute_type
            }
            output_text = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            output_text = full_text

        # 写入文件或输出到控制台
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            if not args.quiet:
                print(f"✓ 转录结果已保存到: {args.output}", file=sys.stderr)
        else:
            print(output_text)

        if not args.quiet:
            print(f"✓ 转录完成！时长: {info.duration:.1f}秒", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n✗ 转录被用户中断", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"转录时出错: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()