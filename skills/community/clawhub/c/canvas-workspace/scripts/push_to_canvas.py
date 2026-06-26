"""Push an image URL to the canvas.

SECURITY MANIFEST:
- Environment variables accessed: CANVAS_SERVER
- External endpoints called: http://localhost:*/api/canvas/sync/gen_image, http://localhost:*/api/upload/image (local canvas only)
- Local files read: none
- Local files written: none

NOTE: 远程图片会先下载再通过本地上传接口推送，确保画布图片可被正常导出（避免跨域污染）。
"""
import argparse
import json
import os
import urllib.request
import uuid
from urllib.parse import urlparse

CANVAS_SERVER = os.environ.get("CANVAS_SERVER", "http://localhost:39301")


def _is_local_url(url: str) -> bool:
    """判断是否为本地服务器 URL"""
    parsed = urlparse(url)
    return parsed.netloc.startswith("localhost") or parsed.netloc.startswith("127.0.0.1")


def _download_and_upload(image_url: str) -> str:
    """下载远程图片并上传到本地服务器，返回本地 URL"""
    req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        image_data = resp.read()
        content_type = resp.headers.get("Content-Type", "image/png")

    ext = ".png"
    if "jpeg" in content_type or "jpg" in content_type:
        ext = ".jpg"
    elif "webp" in content_type:
        ext = ".webp"
    elif "gif" in content_type:
        ext = ".gif"

    filename = f"gen_{uuid.uuid4().hex[:12]}{ext}"
    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + image_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    upload_req = urllib.request.Request(
        f"{CANVAS_SERVER}/api/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(upload_req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("url", image_url)


def push_to_canvas(image_url: str, element_id: str | None = None) -> tuple[str, str]:
    """推送图片到画布，返回 (element_id, final_url)"""
    if not element_id:
        element_id = f"gen_{uuid.uuid4().hex[:12]}"

    final_url = image_url
    if not _is_local_url(image_url):
        try:
            final_url = _download_and_upload(image_url)
        except Exception as e:
            print(f"[push_to_canvas] 下载上传失败，使用原始 URL: {e}")

    payload = json.dumps({"url": final_url, "element_id": element_id}).encode("utf-8")
    req = urllib.request.Request(
        f"{CANVAS_SERVER}/api/canvas/sync/gen_image",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()
    return element_id, final_url


def main():
    parser = argparse.ArgumentParser(description="Push an image URL to the canvas")
    parser.add_argument("--url", required=True, help="Image URL to push")
    parser.add_argument("--id", default=None, help="Optional element id")
    args = parser.parse_args()

    element_id, final_url = push_to_canvas(args.url, args.id)
    print(json.dumps({"status": "ok", "url": args.url, "local_url": final_url, "element_id": element_id}))


if __name__ == "__main__":
    main()
