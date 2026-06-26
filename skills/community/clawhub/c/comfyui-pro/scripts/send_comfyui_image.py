#!/usr/bin/env python3
"""
ComfyUI 飞书图片发送工具
使用 OpenClaw message 工具发送图片（文件附件形式）
"""

import sys
import subprocess
from pathlib import Path

def send_image_via_openclaw(image_path: str, target: str, caption: str = ""):
    """
    使用 OpenClaw message 工具发送图片
    
    Args:
        image_path: 图片路径
        target: 目标用户 ID
        caption: 图片说明
    """
    cmd = [
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", f"user:{target}",
        "--media", image_path
    ]
    
    if caption:
        cmd.extend(["--message", caption])
    
    print(f"[CMD] {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        print(f"[OK] 图片已发送")
        if result.stdout:
            print(f"[OUT] {result.stdout}")
        return True
    else:
        print(f"[ERR] 发送失败")
        if result.stderr:
            print(f"[ERR] {result.stderr}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python send_comfyui_image.py <图片路径> <用户 ID> [说明文字]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    target = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else ""
    
    if not Path(image_path).exists():
        print(f"[ERR] 文件不存在")
        sys.exit(1)
    
    success = send_image_via_openclaw(image_path, target, caption)
    sys.exit(0 if success else 1)
