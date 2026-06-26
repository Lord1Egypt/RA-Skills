#!/usr/bin/env python3
"""China Vision - Analyze images using Qwen2.5-VL-72B via SiliconFlow API.

Usage:
  python3 vision.py --image /path/to/image.jpg --prompt "Describe this image"
  python3 vision.py --url https://example.com/photo.jpg --prompt "What is this?"
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "Qwen/Qwen2.5-VL-72B-Instruct"


def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_mime_type(image_path):
    ext = image_path.lower().split(".")[-1]
    mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "gif": "image/gif",
        "bmp": "image/bmp",
    }
    return mime_map.get(ext, "image/jpeg")


def call_siliconflow(api_key, image_data_url_or_url, prompt, max_tokens=2048):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url_or_url
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
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
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return f"API error: {e.code} - {error_body}"
    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="China Vision - Image analysis")
    parser.add_argument("--image", help="Path to local image file")
    parser.add_argument("--url", help="URL of image to analyze")
    parser.add_argument("--prompt", required=True, help="Analysis prompt")
    parser.add_argument("--max-tokens", type=int, default=2048, help="Max response tokens")
    args = parser.parse_args()

    if not args.image and not args.url:
        print("error: --image or --url is required")
        sys.exit(1)

    api_key = os.environ.get("SILICONFLOW_API_KEY", "")
    if not api_key:
        print("error: SILICONFLOW_API_KEY not set")
        print("Get your API key at: https://cloud.siliconflow.cn")
        sys.exit(1)

    if args.image:
        if not os.path.exists(args.image):
            print(f"error: image not found: {args.image}")
            sys.exit(1)
        b64 = get_image_base64(args.image)
        mime = get_mime_type(args.image)
        image_source = f"data:{mime};base64,{b64}"
    else:
        image_source = args.url

    result = call_siliconflow(api_key, image_source, args.prompt, args.max_tokens)
    print(result)


if __name__ == "__main__":
    main()