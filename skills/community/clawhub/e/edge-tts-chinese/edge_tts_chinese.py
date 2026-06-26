#!/usr/bin/env python3
"""
Edge TTS 中文转语音
将中文文章转换为语音音频（仅限中文）
"""

import argparse
import asyncio
import sys
import os
import edge_tts


async def text_to_speech(text: str, voice: str, output: str) -> str:
    """将文本转换为语音"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)
    return output


def main():
    parser = argparse.ArgumentParser(description='Edge TTS 中文转语音')
    parser.add_argument('--text', '-t', help='直接输入中文文章内容')
    parser.add_argument('--voice', '-v', default='zh-CN-XiaoxiaoNeural',
                        help='语音名称 (默认: zh-CN-XiaoxiaoNeural)')
    parser.add_argument('--output', '-o', default='/tmp/edge_tts_chinese.mp3',
                        help='输出文件路径 (默认: /tmp/edge_tts_chinese.mp3)')
    parser.add_argument('--file', '-f', help='从文件读取中文文章')

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("请输入中文文章内容（输入完成后按 Ctrl+D 结束）：")
        text = sys.stdin.read()

    if not text.strip():
        print("错误：文章内容不能为空")
        sys.exit(1)

    print(f"正在生成音频...")
    print(f"字数：{len(text)} 字符")
    print(f"语音：{args.voice}")

    output_path = asyncio.run(text_to_speech(text, args.voice, args.output))

    size = os.path.getsize(output_path)
    duration_estimate = size / 16000  # 粗略估算

    print(f"✅ 完成：{output_path}")
    print(f"文件大小：{size / 1024:.1f} KB")
    print(f"预计时长：约 {duration_estimate:.0f} 秒")


if __name__ == "__main__":
    main()
