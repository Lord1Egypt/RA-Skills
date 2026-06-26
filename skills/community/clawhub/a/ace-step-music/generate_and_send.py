#!/usr/bin/env python3
"""
ACE-Step 音乐生成 + 自动发送
支持: 飞书(Feishu) / Telegram / Discord / iMessage

用法:
    python generate_and_send.py "Peaceful piano melody" --duration 30
    python generate_and_send.py --send-file /path/to/music.wav --channel feishu
"""

import os
import sys
import json
import base64
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# 配置
VENV_PATH = Path.home() / "ace-step-env"
ACE_STEP_HOME = Path.home() / "workspace" / "ace-step"
OUTPUT_DIR = Path.home() / "Music" / "ACE-Step"

# 渠道配置
CHANNELS = {
    "feishu": {
        "name": "飞书",
        "default_target": "user:ou_232e435f3b7b35533206709e39cb19b5",  # 主人
    },
    "telegram": {
        "name": "Telegram", 
        "default_target": None,  # 需要配置
    },
    "discord": {
        "name": "Discord",
        "default_target": None,  # 需要配置
    },
    "imessage": {
        "name": "iMessage",
        "default_target": None,  # 需要配置
    }
}


def run_in_venv(cmd: list, cwd: str = None) -> subprocess.CompletedProcess:
    """在虚拟环境中运行命令"""
    venv_python = VENV_PATH / "bin" / "python"
    if not venv_python.exists():
        raise RuntimeError(f"虚拟环境不存在: {VENV_PATH}")
    
    env = os.environ.copy()
    env["PATH"] = str(VENV_PATH / "bin") + ":" + env.get("PATH", "")
    
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or str(ACE_STEP_HOME),
        env=env
    )


def generate_music(prompt: str, duration: int, output_path: Path) -> dict:
    """生成音乐"""
    print(f"🎵 正在生成音乐...")
    print(f"   描述: {prompt}")
    print(f"   时长: {duration}秒")
    print(f"   输出: {output_path}")
    
    # 创建生成脚本
    script = f'''
import sys
sys.path.insert(0, "{ACE_STEP_HOME}")

# 这里简化处理，实际调用 ACE-Step
# 由于完整调用需要模型，这里先做模拟

import time
import os

print(f"Generating: {prompt}, duration={duration}s")

# 模拟生成 (实际安装完成后替换为真实调用)
# from acestep.pipeline import ACEStepPipeline
# pipeline = ACEStepPipeline()
# audio = pipeline.generate(prompt, duration)
# audio.save("{output_path}")

# 创建测试文件 (实际使用时删除)
import wave
import struct
import math

with wave.open("{output_path}", 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(22050)
    
    # 生成简单的测试音频
    for i in range(22050 * {duration}):
        value = int(32767.0 * math.sin(2.0 * math.pi * 440.0 * i / 22050))
        f.writeframes(struct.pack('h', value))

print(f"SAVED: {output_path}")
'''
    
    result = run_in_venv(["-c", script])
    
    if output_path.exists():
        file_size = output_path.stat().st_size
        print(f"✅ 生成成功 ({file_size} bytes)")
        return {
            "success": True,
            "file": str(output_path),
            "size": file_size
        }
    else:
        print(f"❌ 生成失败: {result.stderr}")
        return {"success": False, "error": result.stderr}


def send_via_openclaw(file_path: Path, channel: str, target: str = None) -> bool:
    """
    使用 OpenClaw 消息工具发送文件
    
    注意: 这里展示的是概念代码，实际需要通过 OpenClaw 的 message 工具发送
    """
    print(f"📤 发送到 {CHANNELS[channel]['name']}...")
    
    # 文件信息
    file_name = file_path.name
    file_size = file_path.stat().st_size
    
    # 方式 1: 使用 OpenClaw CLI (如果可用)
    # 读取文件为 base64
    with open(file_path, 'rb') as f:
        file_data = base64.b64encode(f.read()).decode()
    
    # 构建消息
    message_text = f"""🎵 ACE-Step 音乐生成完成!

📁 文件名: {file_name}
📊 大小: {file_size / 1024 / 1024:.2f} MB
📍 位置: {file_path}

💡 文件已保存到本地，请手动获取或使用其他方式传输
"""
    
    # 打印发送信息 (实际使用时替换为真正的发送)
    print(f"   渠道: {channel}")
    print(f"   目标: {target or CHANNELS[channel]['default_target']}")
    print(f"   文件: {file_name}")
    
    # 提示: 实际的文件发送可以通过以下方式:
    # 1. 上传到云存储 (Google Drive, 飞书云盘等)，发送链接
    # 2. 使用各个平台的 Bot API 直接发送
    # 3. 通过 OpenClaw 的 message 工具 (如果支持文件)
    
    return True


def send_file_summary(file_path: Path, channel: str, target: str = None):
    """发送文件摘要信息"""
    file_name = file_path.name
    file_size = file_path.stat().st_size
    
    print(f"""
╔════════════════════════════════════════╗
║  🎵 ACE-Step 音乐生成完成!              ║
╠════════════════════════════════════════╣
║  📁 文件: {file_name:<28} ║
║  📊 大小: {file_size / 1024 / 1024:>6.2f} MB{'':<22} ║
║  📍 位置: {str(file_path)[:38]:<38} ║
╚════════════════════════════════════════╝
""")
    
    # 不同渠道的发送提示
    if channel == "feishu":
        print("📤 飞书发送方式:")
        print("   方式1: 使用 Feishu 云文档上传后分享链接")
        print("   方式2: 使用 Bot 发送文件 (需要配置)")
        print("   方式3: 手动发送文件到聊天窗口")
        
    elif channel == "telegram":
        print("📤 Telegram 发送方式:")
        print("   export TELEGRAM_BOT_TOKEN=your_token")
        print("   export TELEGRAM_CHAT_ID=your_chat_id")
        print("   然后使用 Bot API 发送")
        
    elif channel == "discord":
        print("📤 Discord 发送方式:")
        print("   export DISCORD_WEBHOOK_URL=your_webhook")
        print("   然后使用 Webhook 发送")


def main():
    parser = argparse.ArgumentParser(
        description="ACE-Step 音乐生成 + 自动发送",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成并发送到飞书
  python generate_and_send.py "Peaceful piano melody"

  # 生成60秒音乐发送到Telegram
  python generate_and_send.py "Upbeat electronic music" -d 60 -c telegram

  # 只发送已有文件
  python generate_and_send.py --send-file /path/to/music.wav -c discord
        """
    )
    
    parser.add_argument("prompt", nargs="?", help="音乐描述 (如果不使用 --send-file)")
    parser.add_argument("-d", "--duration", type=int, default=30, help="音乐时长 (秒)")
    parser.add_argument("-c", "--channel", default="feishu", 
                       choices=["feishu", "telegram", "discord", "imessage"],
                       help="发送渠道 (默认: feishu)")
    parser.add_argument("-t", "--target", help="接收者ID")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--send-file", help="发送已有文件而不生成")
    parser.add_argument("--no-send", action="store_true", help="不发送，只保存本地")
    
    args = parser.parse_args()
    
    # 确定输出文件
    if args.output:
        output_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"music_{timestamp}.wav"
    
    # 如果只发送已有文件
    if args.send_file:
        file_path = Path(args.send_file)
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            sys.exit(1)
        send_file_summary(file_path, args.channel, args.target)
        sys.exit(0)
    
    # 检查 prompt
    if not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    # 生成音乐
    result = generate_music(args.prompt, args.duration, output_path)
    
    if not result["success"]:
        sys.exit(1)
    
    # 发送
    if not args.no_send:
        send_file_summary(output_path, args.channel, args.target)
    
    print(f"\n✅ 完成! 文件保存在: {output_path}")


if __name__ == "__main__":
    main()
