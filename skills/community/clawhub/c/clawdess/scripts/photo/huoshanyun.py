"""Huoshanyun photo provider (Doubao Seedream 4.5)."""

import json

from common import api_post, extract_url


def generate(api_key, prompt, image_url):
    payload = {
        "model": "doubao-seedream-4-5-251128",
        "image": image_url,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "1440x2560",
        "stream": False,
        "watermark": True,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    code, body = api_post("https://ark.cn-beijing.volces.com/api/v3/images/generations", headers, payload)
    print(f"Huoshanyun response ({code}): {json.dumps(body)[:500]}")
    url = extract_url(body)
    if url and url.endswith(".png"):
        return url
    return None
