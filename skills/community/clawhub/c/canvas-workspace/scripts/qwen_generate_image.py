"""Qwen 文生图案例脚本。直接返回 Qwen 结果 URL，可选推送到画布；不上传 OSS。

SECURITY MANIFEST:
- Environment variables accessed: QWEN_TEXT_IMAGE_API_KEY, QWEN_TEXT_IMAGE_MODEL, QWEN_BASE_URL, CANVAS_SERVER
- External endpoints called: https://dashscope.aliyuncs.com/api/v1 (Qwen API), http://localhost:*/api/canvas/sync/* (local canvas)
- Local files read: none
- Local files written: none
"""
import argparse
import json
import os
import urllib.request
import uuid

QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")
QWEN_TEXT_IMAGE_API_KEY = os.environ.get("QWEN_TEXT_IMAGE_API_KEY", "")
QWEN_TEXT_IMAGE_MODEL = os.environ.get("QWEN_TEXT_IMAGE_MODEL", "qwen-image-2.0-pro")
CANVAS_SERVER = os.environ.get("CANVAS_SERVER", "http://localhost:39301")


def generate_image(prompt: str, size: str | None = None) -> str:
    if not QWEN_TEXT_IMAGE_API_KEY:
        raise RuntimeError("请设置环境变量 QWEN_TEXT_IMAGE_API_KEY 后再使用 Qwen 文生图脚本")

    from dashscope import MultiModalConversation
    import dashscope

    dashscope.base_http_api_url = QWEN_BASE_URL

    kwargs = {
        "api_key": QWEN_TEXT_IMAGE_API_KEY,
        "model": QWEN_TEXT_IMAGE_MODEL,
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "stream": False,
        "n": 1,
        "watermark": False,
        "prompt_extend": True,
    }
    if size:
        kwargs["size"] = size

    response = MultiModalConversation.call(**kwargs)

    status_code = getattr(response, "status_code", None) or response.get("status_code")
    if status_code != 200:
        code = getattr(response, "code", None) or response.get("code", "")
        message = getattr(response, "message", None) or response.get("message", "")
        raise RuntimeError(f"Qwen 文生图调用失败: {code} - {message}")

    output = getattr(response, "output", None) or response.get("output", {})
    choices = getattr(output, "choices", None) or output.get("choices", [])
    if not choices:
        raise RuntimeError("Qwen 文生图返回为空")

    message = choices[0].get("message", {})
    content = message.get("content", [])
    for item in content:
        if "image" in item:
            return item["image"]

    raise RuntimeError("Qwen 文生图返回中没有图片 URL")


def main():
    parser = argparse.ArgumentParser(description="Qwen 文生图（默认推送到画布）")
    parser.add_argument("--prompt", required=True, help="文生图提示词")
    parser.add_argument("--size", default=None, help="输出尺寸，如 1024*1024")
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
