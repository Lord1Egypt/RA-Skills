#!/usr/bin/env python3
"""
上传图片到 ImgURL 图床，返回公网 URL
用法：python3 upload_image.py <图片路径>
"""

import sys
import json
import urllib.request
import urllib.error
import os

IMGURL_UID = os.environ.get("IMGURL_UID", "rrbhyq")
IMGURL_TOKEN = os.environ.get("IMGURL_TOKEN", "sk-Um9dYCP0yGsGUjER3jH88T3ybd1S0n2GgByDOyfq8zISWi6H604qtGn7N3Bza")
IMGURL_API = "https://www.imgurl.org/api/v2/upload"


def upload_image(image_path: str) -> str:
    """上传图片到 ImgURL，返回公网直链 URL"""
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"

    with open(image_path, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(image_path)

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="uid"\r\n\r\n'
        f"{IMGURL_UID}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="token"\r\n\r\n'
        f"{IMGURL_TOKEN}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        IMGURL_API,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 200:
                url = result["data"]["url"]
                return url
            else:
                print(f"❌ 上传失败: {result}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误 {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 upload_image.py <图片路径>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}", file=sys.stderr)
        sys.exit(1)

    print(f"📤 上传图片: {image_path}")
    url = upload_image(image_path)
    print(f"✅ 上传成功: {url}")
    print(url)  # 最后一行输出纯 URL，方便其他脚本捕获
