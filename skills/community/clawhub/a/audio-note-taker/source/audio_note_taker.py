#!/usr/bin/env python3
"""
Audio Note Taker - 智能语音笔记助手
将录音自动转成结构化文字笔记
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("❌ 需要安装 openai 包: pip install openai>=1.0.0")
    sys.exit(1)


def transcribe_audio(audio_path: str, language: str = "auto", model: str = "whisper-1"):
    """使用 OpenAI Whisper API 转录音频"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language if language != "auto" else None,
            response_format="text"
        )
    return transcript


def generate_notes(
    transcript: str,
    title: str,
    detect_speakers: bool = False,
    summarize: bool = False,
    extract_action_items: bool = False
) -> str:
    """生成结构化笔记（简单版）"""
    notes = []

    # 标题
    notes.append(f"# {title}")
    notes.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    notes.append("")

    # 如果开启摘要（需要 LLM，这里先实现基本版）
    if summarize or extract_action_items:
        notes.append("## 📝 智能摘要")
        notes.append("*（需配置 GPT 模型，当前版本暂未启用）*")
        notes.append("")

    # 完整转录
    notes.append("## 📄 完整转录")
    notes.append("```text")
    notes.append(transcript)
    notes.append("```")

    return "\n".join(notes)


def main():
    parser = argparse.ArgumentParser(
        description="语音笔记助手 - 录音自动转文字并整理成结构化笔记"
    )
    parser.add_argument("input", help="音频文件路径")
    parser.add_argument("--title", help="笔记标题", default=None)
    parser.add_argument("--language", default="auto", help="音频语言（en, zh, auto 等）")
    parser.add_argument("--output", help="输出文件路径", default=None)
    parser.add_argument("--detect-speakers", action="store_true", help="识别说话人（需额外配置）")
    parser.add_argument("--summarize", action="store_true", help="生成摘要（需 OPENAI_API_KEY）")
    parser.add_argument("--extract-action-items", action="store_true", help="提取行动项")
    parser.add_argument("--model", default="whisper-1", help="Whisper 模型名称")
    parser.add_argument("--format", default="markdown", choices=["markdown", "txt", "json"], help="输出格式")

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)

    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 未设置 OPENAI_API_KEY 环境变量")
        print("   请设置: export OPENAI_API_KEY='your-key'")
        print("   或配置 ~/.openclaw/openclaw.json")
        sys.exit(1)

    # 生成标题
    if not args.title:
        audio_name = Path(args.input).stem
        args.title = f"语音笔记 - {audio_name}"

    # 转录音频
    print(f"🎤 正在转录音频: {args.input} ...")
    try:
        transcript = transcribe_audio(args.input, args.language, args.model)
        print(f"✅ 转写完成，共 {len(transcript)} 字符")
    except Exception as e:
        print(f"❌ 转写失败: {e}")
        sys.exit(1)

    # 生成笔记
    print("📝 正在生成结构化笔记...")
    notes = generate_notes(
        transcript=transcript,
        title=args.title,
        detect_speakers=args.detect_speakers,
        summarize=args.summarize,
        extract_action_items=args.extract_action_items
    )

    # 输出文件
    output_path = args.output or f"{Path(args.input).stem}_notes.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(notes)

    print(f"✅ 笔记已保存: {output_path}")
    print(f"   预览:\n{notes[:500]}...")


if __name__ == "__main__":
    main()
