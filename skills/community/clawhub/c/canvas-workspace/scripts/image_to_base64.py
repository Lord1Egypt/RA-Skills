"""将图片地址转换为 base64 data URL。

支持网络 URL 和本地文件路径。

SECURITY MANIFEST:
- Environment variables accessed: none
- External endpoints called: 用户指定的图片 URL（仅下载）
- Local files read: 用户指定的本地图片文件
- Local files written: none
"""
import argparse
import base64
import json
import mimetypes
import os
import urllib.request


def image_to_base64(image_path: str) -> str:
    """将图片地址转换为 base64 data URL。
    
    Args:
        image_path: 图片地址，支持网络 URL 或本地文件路径
        
    Returns:
        base64 data URL，格式为 data:image/xxx;base64,...
    """
    if image_path.startswith("data:"):
        return image_path

    if image_path.startswith(("http://", "https://")):
        req = urllib.request.Request(image_path, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type", "image/png")
            if ";" in content_type:
                content_type = content_type.split(";")[0].strip()
    elif os.path.isfile(image_path):
        mime_type, _ = mimetypes.guess_type(image_path)
        content_type = mime_type or "image/png"
        with open(image_path, "rb") as f:
            data = f.read()
    else:
        raise RuntimeError(f"无法识别的图片路径: {image_path}")

    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{content_type};base64,{encoded}"


def main():
    parser = argparse.ArgumentParser(description="将图片地址转换为 base64 data URL")
    parser.add_argument("--path", required=True, help="图片地址（网络 URL 或本地文件路径）")
    args = parser.parse_args()

    try:
        result = image_to_base64(args.path)
        print(json.dumps({"status": "ok", "base64": result}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
