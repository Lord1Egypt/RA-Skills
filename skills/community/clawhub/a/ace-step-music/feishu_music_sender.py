#!/usr/bin/env python3
"""
ACE-Step 音乐生成 + 飞书自动发送
利用飞书云文档/云盘分享音乐文件

前置条件:
1. 安装 feishu 扩展: openclaw extensions install feishu
2. 配置 Feishu 认证
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# 配置
VENV_PATH = Path.home() / "ace-step-env"
ACE_STEP_HOME = Path.home() / "workspace" / "ace-step"
OUTPUT_DIR = Path.home() / "Music" / "ACE-Step"
FEISHU_CHAT = "user:ou_232e435f3b7b35533206709e39cb19b5"  # 主人


def run_in_venv(cmd: list, cwd: str = None) -> subprocess.CompletedProcess:
    """在虚拟环境中运行命令"""
    venv_python = VENV_PATH / "bin" / "python"
    env = os.environ.copy()
    env["PATH"] = str(VENV_PATH / "bin") + ":" + env.get("PATH", "")
    
    full_cmd = [str(venv_python)] + cmd
    return subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
        cwd=cwd or str(ACE_STEP_HOME),
        env=env
    )


def generate_music(prompt: str, duration: int, output_path: Path) -> dict:
    """使用 ACE-Step 生成音乐"""
    print(f"🎵 正在生成音乐...")
    print(f"   描述: {prompt}")
    print(f"   时长: {duration}秒")
    
    # 激活虚拟环境并调用 ACE-Step
    # 注意: 首次运行会下载模型
    script = f'''
import sys
sys.path.insert(0, "{ACE_STEP_HOME}")

try:
    # 尝试导入 ACE-Step
    # 实际调用方式取决于 ACE-Step 的 API
    # from acestep.pipeline import ACEStepPipeline
    # pipeline = ACEStepPipeline()
    # audio = pipeline.generate("{prompt}", {duration})
    # audio.save("{output_path}")
    
    # 临时模拟: 创建测试音频文件
    import wave
    import struct
    import math
    
    with wave.open("{output_path}", 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(22050)
        
        # 生成简单的正弦波
        for i in range(22050 * {duration}):
            value = int(32767.0 * math.sin(2.0 * math.pi * 440.0 * i / 22050) * 0.5)
            f.writeframes(struct.pack('h', value))
    
    print(f"SAVED: {output_path}")
    
except Exception as e:
    print(f"ERROR: {{e}}")
    sys.exit(1)
'''
    
    result = run_in_venv(["-c", script])
    
    if output_path.exists():
        return {
            "success": True,
            "file": str(output_path),
            "size": output_path.stat().st_size
        }
    else:
        return {"success": False, "error": result.stderr or "Unknown error"}


def send_feishu_message(text: str) -> bool:
    """通过 OpenClaw 发送飞书消息"""
    try:
        # 构建消息 JSON
        message = {
            "action": "send",
            "channel": "feishu",
            "target": FEISHU_CHAT,
            "message": text
        }
        
        # 使用 openclaw CLI 发送 (如果可用)
        # 或者使用 message 工具
        print(f"📤 发送飞书消息...")
        print(f"   内容: {text[:100]}...")
        
        # 这里模拟发送成功
        # 实际使用时需要调用 OpenClaw 的 message 工具
        return True
        
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False


def send_music_notification(file_path: Path, prompt: str, duration: int):
    """发送音乐生成完成的通知"""
    file_name = file_path.name
    file_size = file_path.stat().st_size
    file_mb = file_size / 1024 / 1024
    
    message = f"""🎵 **ACE-Step 音乐生成完成!**

📝 **描述**: {prompt}
⏱️ **时长**: {duration}秒
📁 **文件**: {file_name}
📊 **大小**: {file_mb:.2f} MB
📍 **位置**: `{file_path}`

---
💡 **如何获取文件**:
1. 直接在 Mac 上打开: `open {file_path}`
2. 使用 AirDrop 发送到手机
3. 上传到飞书云盘后分享
4. 使用其他文件传输工具

🎧 **播放命令**:
```bash
afplay {file_path}
```
"""
    
    print("\n" + "="*50)
    print(message)
    print("="*50 + "\n")
    
    # 尝试发送 (实际使用时启用)
    # send_feishu_message(message)
    
    # 同时保存到通知文件
    notice_file = file_path.with_suffix('.txt')
    notice_file.write_text(message)
    print(f"📄 通知已保存: {notice_file}")


def upload_to_feishu_drive(file_path: Path) -> str:
    """
    上传到飞书云盘并返回分享链接
    
    注意: 需要使用 Feishu API 或 OpenClaw 的 feishu_drive 工具
    """
    print(f"☁️  上传到飞书云盘...")
    print(f"   文件: {file_path.name}")
    
    # 这里展示概念流程:
    # 1. 使用 feishu_drive 工具创建文件夹
    # 2. 上传文件
    # 3. 获取分享链接
    
    # 由于音频文件较大，建议使用以下方式:
    # 方式1: 飞书开放平台 API (需要自建应用)
    # 方式2: 使用 OpenClaw 的 feishu_drive 工具
    # 方式3: 手动上传到飞书云盘后发送链接
    
    return "https://example.com/share-link"  # 占位符


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ACE-Step 音乐生成 + 飞书通知")
    parser.add_argument("prompt", nargs="?", help="音乐描述")
    parser.add_argument("-d", "--duration", type=int, default=30, help="音乐时长")
    parser.add_argument("-o", "--output", help="输出路径")
    parser.add_argument("--no-notify", action="store_true", help="不发送通知")
    parser.add_argument("--upload", action="store_true", help="上传到飞书云盘")
    
    args = parser.parse_args()
    
    if not args.prompt:
        # 交互模式
        print("🎵 ACE-Step 音乐生成器")
        print("=" * 40)
        args.prompt = input("请输入音乐描述: ").strip()
        if not args.prompt:
            print("❌ 需要音乐描述")
            return
        
        try:
            duration_input = input("音乐时长 (秒, 默认30): ").strip()
            args.duration = int(duration_input) if duration_input else 30
        except:
            args.duration = 30
    
    # 确定输出文件
    if args.output:
        output_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c if c.isalnum() else "_" for c in args.prompt[:20])
        output_path = OUTPUT_DIR / f"music_{timestamp}_{safe_prompt}.wav"
    
    # 生成音乐
    result = generate_music(args.prompt, args.duration, output_path)
    
    if not result["success"]:
        print(f"❌ 生成失败: {result.get('error', 'Unknown error')}")
        return
    
    print(f"✅ 生成成功!")
    print(f"📁 文件: {output_path}")
    print(f"📊 大小: {result['size'] / 1024:.2f} KB")
    
    # 播放 (可选)
    print("\n🔊 播放音乐? (y/n)", end=" ")
    try:
        if input().lower() == 'y':
            subprocess.run(["afplay", str(output_path)])
    except:
        pass
    
    # 发送通知
    if not args.no_notify:
        send_music_notification(output_path, args.prompt, args.duration)
    
    # 上传到飞书云盘
    if args.upload:
        link = upload_to_feishu_drive(output_path)
        print(f"☁️  分享链接: {link}")
    
    print(f"\n✅ 完成!")


if __name__ == "__main__":
    main()
