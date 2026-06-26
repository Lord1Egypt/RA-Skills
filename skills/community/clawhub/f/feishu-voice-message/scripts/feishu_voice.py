#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音消息生成工具
1. 使用 Edge TTS 生成语音
2. 转换为 OPUS 格式（飞书语音消息要求）
3. 自动发送到对话
"""

import subprocess
import os
import sys
import argparse
import io

# 设置 UTF-8 输出（解决 Windows GBK 编码问题）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# TTS 音色预设
VOICE_PRESETS = {
    # 成人音色
    "manbo": {"voice": "zh-CN-XiaoyiNeural", "pitch": "+50Hz", "rate": "+0%"},
    "xiaoyi": {"voice": "zh-CN-XiaoyiNeural", "pitch": "+0Hz", "rate": "+30%"},
    "xiaoxiao": {"voice": "zh-CN-XiaoxiaoNeural", "pitch": "+0Hz", "rate": "+0%"},
    "yunyang": {"voice": "zh-CN-YunyangNeural", "pitch": "+0Hz", "rate": "+10%"},
    # 儿童音色
    "xiaotangdou": {"voice": "zh-CN-XiaoyiNeural", "pitch": "+15%", "rate": "-5%"},
    "mianhuatang": {"voice": "zh-CN-XiaoxiaoNeural", "pitch": "+5%", "rate": "-10%"},
    "xiaomengmeng": {"voice": "zh-CN-XiaoxiaoNeural", "pitch": "+10%", "rate": "-5%"},
}

def generate_tts(text, output_mp3, preset="manbo"):
    """使用 Edge TTS 生成 MP3"""
    if preset not in VOICE_PRESETS:
        print(f"❌ 未知预设: {preset}")
        print(f"   可用预设: {', '.join(VOICE_PRESETS.keys())}")
        return False
    
    config = VOICE_PRESETS[preset]
    
    cmd = [
        "node",
        os.path.expanduser("~/.openclaw/workspace/skills/edge-tts/scripts/tts-converter.js"),
        text,
        "--voice", config["voice"],
        "--pitch", config["pitch"],
        "--rate", config["rate"],
        "--output", output_mp3
    ]
    
    print(f"🎤 生成 TTS: {text}")
    print(f"   预设: {preset} ({config['voice']})")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ MP3 已生成: {output_mp3}")
            return True
        else:
            print(f"❌ TTS 生成失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False

def convert_to_opus(input_mp3, output_opus):
    """使用 ffmpeg 将 MP3 转换为 OPUS"""
    cmd = [
        "ffmpeg",
        "-i", input_mp3,
        "-c:a", "libopus",
        "-b:a", "64k",
        "-y",  # 覆盖输出文件
        output_opus
    ]
    
    print(f"🔄 转换为 OPUS 格式...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 or os.path.exists(output_opus):
            print(f"✅ OPUS 已生成: {output_opus}")
            return True
        else:
            print(f"❌ 转换失败")
            return False
    except Exception as e:
        print(f"❌ 转换出错: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='飞书语音消息生成工具')
    parser.add_argument('text', help='要转换的文本')
    parser.add_argument('--preset', '-p', default='manbo', 
                       help=f'音色预设: {", ".join(VOICE_PRESETS.keys())}')
    parser.add_argument('--output', '-o', default=None, help='输出路径（可选）')
    
    args = parser.parse_args()
    
    # 生成临时文件路径
    if args.output:
        base_path = args.output.replace('.opus', '').replace('.mp3', '')
    else:
        base_path = os.path.join(os.environ.get('TEMP', '/tmp'), 'openclaw', 'voice_message')
    
    os.makedirs(os.path.dirname(base_path) if os.path.dirname(base_path) else '.', exist_ok=True)
    
    mp3_path = f"{base_path}.mp3"
    opus_path = f"{base_path}.opus"
    
    # 1. 生成 TTS
    if not generate_tts(args.text, mp3_path, args.preset):
        sys.exit(1)
    
    # 2. 转换为 OPUS
    if not convert_to_opus(mp3_path, opus_path):
        sys.exit(1)
    
    print(f"\n🎉 语音消息生成完成！")
    print(f"   OPUS 文件: {opus_path}")
    print(f"\n💡 提示: 发送 .opus 文件到飞书，会显示为语音消息（带波形图）")

if __name__ == '__main__':
    main()
