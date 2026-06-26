# -*- coding: utf-8 -*-
"""生成讲解配音"""

import argparse
import asyncio
import edge_tts

async def generate_narration(text, voice, rate, pitch, output):
    """生成语音"""
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        pitch=pitch
    )
    
    await communicate.save(output)
    print(f"音频已保存至: {output}")

def main():
    parser = argparse.ArgumentParser(description='生成讲解配音')
    parser.add_argument('--text', required=True, help='讲解脚本文本')
    parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural', 
                        help='语音名称 (默认: zh-CN-XiaoxiaoNeural)')
    parser.add_argument('--rate', default='+5%', help='语速调整 (默认: +5%)')
    parser.add_argument('--pitch', default='0Hz', help='音调调整 (默认: 0Hz)')
    parser.add_argument('--output', default='narration.mp3', help='输出文件')
    
    args = parser.parse_args()
    
    asyncio.run(generate_narration(
        args.text,
        args.voice,
        args.rate,
        args.pitch,
        args.output
    ))

if __name__ == "__main__":
    main()