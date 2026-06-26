#!/usr/bin/env python3
"""China Doc OCR - Document OCR using SiliconFlow API.

Supports: PaddleOCR-VL-1.5, DeepSeek-OCR, Qwen2.5-VL.
Usage:
  python3 ocr.py --image /path/to/image.jpg --prompt "Convert to markdown"
  python3 ocr.py --pdf /path/to/document.pdf
  python3 ocr.py --url https://example.com/image.jpg
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"

MODELS = {
    "paddleocr": "PaddlePaddle/PaddleOCR-VL-1.5",
    "deepseek": "Pro/deepseek-ai/DeepSeek-V3",
    "qwen": "Qwen/Qwen2.5-VL-72B-Instruct",
}


def get_file_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_mime_type(file_path):
    ext = file_path.lower().split(".")[-1]
    mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "pdf": "application/pdf",
    }
    return mime_map.get(ext, "image/jpeg")


def call_siliconflow(api_key, model, image_source, prompt, max_tokens=4096):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_source,
                            "detail": "high"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "max_tokens": max_tokens,
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        SILICONFLOW_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return f"API error: {e.code} - {error_body}"
    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="China Doc OCR")
    parser.add_argument("--image", help="Path to local image file")
    parser.add_argument("--pdf", help="Path to local PDF file")
    parser.add_argument("--url", help="URL of image/PDF to OCR")
    parser.add_argument("--prompt", default="Convert the document to markdown.",
                        help="OCR prompt")
    parser.add_argument("--model", choices=["paddleocr", "deepseek", "qwen"],
                        default="paddleocr", help="OCR model to use")
    parser.add_argument("--max-tokens", type=int, default=4096,
                        help="Max response tokens")
    args = parser.parse_args()

    if not args.image and not args.pdf and not args.url:
        print("error: --image, --pdf, or --url is required")
        sys.exit(1)

    api_key = os.environ.get("SILICONFLOW_API_KEY", "")
    if not api_key:
        print("error: SILICONFLOW_API_KEY not set")
        print("Get your API key at: https://cloud.siliconflow.cn")
        sys.exit(1)

    model = MODELS[args.model]

    if args.image:
        if not os.path.exists(args.image):
            print(f"error: file not found: {args.image}")
            sys.exit(1)
        b64 = get_file_base64(args.image)
        mime = get_mime_type(args.image)
        image_source = f"data:{mime};base64,{b64}"
    elif args.pdf:
        if not os.path.exists(args.pdf):
            print(f"error: file not found: {args.pdf}")
            sys.exit(1)
        b64 = get_file_base64(args.pdf)
        image_source = f"data:application/pdf;base64,{b64}"
    else:
        image_source = args.url

    result = call_siliconflow(api_key, model, image_source, args.prompt, args.max_tokens)
    print(result)


if __name__ == "__main__":
    main()