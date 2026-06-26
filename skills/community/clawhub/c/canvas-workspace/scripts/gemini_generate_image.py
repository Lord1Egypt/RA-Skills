"""Gemini 文生图脚本。通过 OpenAI 兼容 API 调用 Gemini 生图模型，返回图片并可选推送到画布。

SECURITY MANIFEST:
- Environment variables accessed: GEMINI_TEXT_IMAGE_API_KEY, GEMINI_TEXT_IMAGE_MODEL, GEMINI_BASE_URL, CANVAS_SERVER
- External endpoints called: https://api.mmw.ink/v1/chat/completions (Gemini API), http://localhost:*/api/canvas/sync/* (local canvas)
- Local files read: none
- Local files written: temporary image file (auto-deleted)
"""
import argparse
import base64
import json
import os
import tempfile
import urllib.request
import uuid

GEMINI_BASE_URL = os.environ.get("GEMINI_BASE_URL", "https://api.mmw.ink")
GEMINI_TEXT_IMAGE_API_KEY = os.environ.get("GEMINI_TEXT_IMAGE_API_KEY", "")
GEMINI_TEXT_IMAGE_MODEL = os.environ.get("GEMINI_TEXT_IMAGE_MODEL", "gemini-3.1-flash-image")
CANVAS_SERVER = os.environ.get("CANVAS_SERVER", "http://localhost:39301")


def generate_image(prompt: str, size: str | None = None) -> str:
    """调用 Gemini 兼容 API 生成图片，返回可访问的图片 URL 或 data URI。"""
    if not GEMINI_TEXT_IMAGE_API_KEY:
        raise RuntimeError("请设置环境变量 GEMINI_TEXT_IMAGE_API_KEY 后再使用 Gemini 文生图脚本")

    # 构建 OpenAI 兼容的 chat completion 请求
    url = f"{GEMINI_BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_TEXT_IMAGE_API_KEY}",
    }

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    body = {
        "model": GEMINI_TEXT_IMAGE_MODEL,
        "messages": messages,
        "stream": False,
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API 调用失败: {e.code} - {error_body}")

    # 解析响应，提取图片
    choices = result.get("choices", [])
    if not choices:
        raise RuntimeError(f"Gemini API 返回为空: {json.dumps(result, ensure_ascii=False)}")

    message = choices[0].get("message", {})

    # 尝试多种响应格式
    # 格式1: content 是字符串，可能包含 markdown 图片或 base64
    content = message.get("content", "")
    if isinstance(content, str):
        # 检查是否有 markdown 图片链接 ![...](url)
        import re
        md_match = re.search(r'!\[.*?\]\((https?://[^\s\)]+)\)', content)
        if md_match:
            return md_match.group(1)

        # 检查是否有裸 URL
        url_match = re.search(r'(https?://\S+\.(?:png|jpg|jpeg|webp|gif))', content, re.IGNORECASE)
        if url_match:
            return url_match.group(1)

    # 格式2: content 是列表（multimodal 格式）
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                if "image_url" in item:
                    img = item["image_url"]
                    if isinstance(img, dict):
                        return img.get("url", "")
                    return img
                if "image" in item:
                    return item["image"]

    # 格式3: 检查 message 中的 inline_data / parts（Gemini 原生格式适配）
    parts = message.get("parts", [])
    for part in parts:
        if isinstance(part, dict) and "inline_data" in part:
            inline = part["inline_data"]
            mime = inline.get("mime_type", "image/png")
            b64 = inline.get("data", "")
            if b64:
                # 上传到画布服务器获取 URL
                return _upload_base64_to_canvas(b64, mime)

    # 格式4: 如果 content 本身是 base64 编码的图片
    if isinstance(content, str) and len(content) > 1000:
        try:
            base64.b64decode(content[:100])
            return _upload_base64_to_canvas(content, "image/png")
        except Exception:
            pass

    raise RuntimeError(f"无法从 Gemini 响应中提取图片。响应: {json.dumps(result, ensure_ascii=False)[:500]}")


def _upload_base64_to_canvas(b64_data: str, mime_type: str) -> str:
    """将 base64 图片数据上传到画布服务器，返回可访问的 URL。"""
    ext = mime_type.split("/")[-1].replace("jpeg", "jpg")
    filename = f"gemini_{uuid.uuid4().hex[:8]}.{ext}"

    image_bytes = base64.b64decode(b64_data)

    # 用 multipart/form-data 上传
    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8") + image_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"{CANVAS_SERVER}/api/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("url", "")
    except Exception:
        # fallback: 返回 data URI
        return f"data:{mime_type};base64,{b64_data}"


def main():
    parser = argparse.ArgumentParser(description="Gemini 文生图（默认推送到画布）")
    parser.add_argument("--prompt", required=True, help="文生图提示词")
    parser.add_argument("--size", default=None, help="输出尺寸（预留，当前未使用）")
    args = parser.parse_args()

    image_url = generate_image(args.prompt, args.size)
    result = {"status": "ok", "url": image_url}

    try:
        from push_to_canvas import push_to_canvas
        element_id, local_url = push_to_canvas(image_url)
        result["pushed"] = True
        result["local_url"] = local_url
        result["element_id"] = element_id
    except Exception as e:
        result["pushed"] = False
        result["push_error"] = str(e)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
