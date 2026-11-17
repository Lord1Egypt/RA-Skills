#!/usr/bin/env python3
"""Generate an image via the OpenRouter chat-completions image API.

Used by the custom-infographic opencode skill (baoyu layout × style system by
宝玉 (JimLiu), ported & customized by j3ffyang). Reads the assembled prompt
from a text file and writes the generated image (base64 data URL or remote
URL) to --output. Requires OPENROUTER_API_KEY in the environment.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-3.1-flash-image"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate an image via OpenRouter")
    ap.add_argument("--prompt", required=True, help="path to the prompt text file")
    ap.add_argument("--output", required=True, help="output image path (e.g. infographic.png)")
    ap.add_argument("--aspect", default="1:1", help="aspect ratio, e.g. 16:9, 9:16, 1:1, 3:4")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter image-capable model id")
    ap.add_argument("--size", default=None, help="optional image size: 0.5K, 1K, 2K or 4K")
    args = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("error: OPENROUTER_API_KEY is not set", file=sys.stderr)
        return 1

    with open(args.prompt, "r", encoding="utf-8") as f:
        prompt = f.read()

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": args.aspect},
    }
    if args.size:
        payload["image_config"]["image_size"] = args.size

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/negtivspace/ai-thoughts",
            "X-Title": "custom-infographic opencode skill",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"error: HTTP {e.code}: {body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"error: {e.reason}", file=sys.stderr)
        return 1

    try:
        message = data["choices"][0]["message"]
        images = message.get("images") or []
    except (KeyError, IndexError):
        print("error: unexpected response: " + json.dumps(data)[:500], file=sys.stderr)
        return 1

    if not images:
        print("error: no images in response: " + json.dumps(data)[:500], file=sys.stderr)
        return 1

    url = images[0].get("image_url", {}).get("url", "")
    if not url:
        print("error: no image_url in first image entry: " + json.dumps(images[0])[:500], file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    if url.startswith("data:"):
        raw = base64.b64decode(url.split(",", 1)[1])
        with open(args.output, "wb") as f:
            f.write(raw)
    else:
        try:
            with urllib.request.urlopen(url) as r:
                with open(args.output, "wb") as f:
                    f.write(r.read())
        except urllib.error.URLError as e:
            print(f"error: failed to download image: {e.reason}", file=sys.stderr)
            return 1

    print(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
