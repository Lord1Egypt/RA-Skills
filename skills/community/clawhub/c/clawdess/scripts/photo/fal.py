"""FAL photo provider (Bytedance Seedream v5 Lite) — async queue."""

import json

from common import api_post, poll_for_url


def generate(api_key, prompt, image_url):
    payload = {
        "image_urls": [image_url],
        "prompt": prompt,
        "image_size": {"width": 1080, "height": 1920},
        "num_images": 1,
        "output_format": "png",
    }
    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    code, body = api_post("https://queue.fal.run/fal-ai/bytedance/seedream/v5/lite/edit", headers, payload)
    request_id = body.get("request_id")
    if not request_id:
        print(f"FAL submit failed ({code}): {json.dumps(body)[:500]}")
        return None
    print(f"FAL submitted ({code}): request_id={request_id}")
    return poll_for_url(
        f"https://queue.fal.run/fal-ai/bytedance/requests/{request_id}",
        {"Authorization": f"Key {api_key}"},
    )
