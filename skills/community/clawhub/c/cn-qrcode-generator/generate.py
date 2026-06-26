#!/usr/bin/env python3
"""中文二维码生成器 - Google Chart API（qrserver.com）"""
import sys
import os
import json
import argparse
import urllib.parse
import subprocess

DEFAULT_OUTPUT = os.path.expanduser("~/Downloads/qrcode.png")

def generate_qr(text, output=DEFAULT_OUTPUT, size=300,
                fg_color="000000", bg_color="FFFFFF"):
    """生成二维码图片（Google Chart API，国内外均稳定）"""
    if not text.startswith("http"):
        text = "https://" + text

    # Google Chart API (qrserver.com) - 全球最稳定的免费QR API
    encoded = urllib.parse.quote(text)
    url = (
        f"https://api.qrserver.com/v1/create-qr-code/"
        f"?size={size}x{size}"
        f"&data={encoded}"
        f"&color={fg_color}"
        f"&bgcolor={bg_color}"
        f"&margin=1"
    )

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    try:
        cmd = ["curl", "-s", "--max-time", "15", "-L", "-o", output, url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=18)
        if os.path.exists(output) and os.path.getsize(output) > 100:
            return {"text": text, "file": os.path.abspath(output),
                    "size": size, "api": "qrserver.com", "status": "ok"}
        else:
            return {"text": text, "file": None, "error": "空响应或文件过小",
                    "status": "failed", "curl_stderr": r.stderr[:200]}
    except Exception as e:
        return {"text": text, "file": None, "error": str(e), "status": "failed"}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="二维码生成器")
    p.add_argument("text", help="二维码内容（URL或文本）")
    p.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="输出文件路径")
    p.add_argument("--size", "-s", type=int, default=300, help="二维码尺寸（像素）")
    p.add_argument("--fg", default="000000", help="前景色HEX")
    p.add_argument("--bg", default="FFFFFF", help="背景色HEX")
    args = p.parse_args()

    result = generate_qr(args.text, args.output, args.size, args.fg, args.bg)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "ok" else 1)
