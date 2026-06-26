#!/usr/bin/env python3
"""DashScope image generation helper (OpenAI compatible-mode).

Uses: https://dashscope.aliyuncs.com/compatible-mode/v1
Model: qwen-image-max

Inputs:
  - prompt text
Outputs:
  - writes image to --out (png/jpg depending on API)

Security:
  - prefers API key from env: DASHSCOPE_API_KEY
  - can pass --api-key but that may end up in shell history

Example:
  DASHSCOPE_API_KEY=... ./dashscope_image_gen.py --prompt "a cute robot" --out robot.png
"""

import argparse
import base64
import json
import os
import sys
import urllib.request

DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen-image-max"


def _post_json(url: str, payload: dict, headers: dict, timeout: int = 120):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return resp.getcode(), body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True, help="Output image path")
    ap.add_argument("--size", default=None, help="Optional: e.g. 1024x1024 (if supported)")
    ap.add_argument("--n", type=int, default=1, help="Number of images (if supported)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--api-key", default=None, help="Avoid; prefer env DASHSCOPE_API_KEY")
    args = ap.parse_args()

    api_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")

    # Fallback: read from OpenClaw config if present (keeps secrets out of shell history).
    if not api_key:
        try:
            cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            api_key = (
                cfg.get("models", {})
                .get("providers", {})
                .get("dashscope", {})
                .get("apiKey")
            )
        except Exception:
            api_key = None

    if not api_key:
        print(
            "Missing API key. Set DASHSCOPE_API_KEY, pass --api-key, or configure models.providers.dashscope.apiKey in ~/.openclaw/openclaw.json.",
            file=sys.stderr,
        )
        sys.exit(2)

    # OpenAI Images API compatible payload (best-effort).
    # If DashScope uses a different schema, the server will return a helpful error.
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
    }
    if args.size:
        payload["size"] = args.size
    if args.seed is not None:
        payload["seed"] = args.seed

    url = args.base_url.rstrip("/") + "/images/generations"
    code, body = _post_json(
        url,
        payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=180,
    )

    if code >= 400:
        print(f"HTTP {code} from {url}", file=sys.stderr)
        print(body, file=sys.stderr)
        sys.exit(1)

    try:
        j = json.loads(body)
    except Exception:
        print("Non-JSON response:", file=sys.stderr)
        print(body, file=sys.stderr)
        sys.exit(1)

    data = (j.get("data") or [])
    if not data:
        print("No image data returned:", file=sys.stderr)
        print(json.dumps(j, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    item = data[0]
    if "b64_json" in item and item["b64_json"]:
        raw = base64.b64decode(item["b64_json"])
        with open(args.out, "wb") as f:
            f.write(raw)
        print(args.out)
        return

    if "url" in item and item["url"]:
        # Download the URL
        img_url = item["url"]
        try:
            with urllib.request.urlopen(img_url, timeout=180) as resp:
                raw = resp.read()
            with open(args.out, "wb") as f:
                f.write(raw)
            print(args.out)
            return
        except Exception as e:
            print(f"Failed to download image url: {img_url}", file=sys.stderr)
            print(str(e), file=sys.stderr)
            sys.exit(1)

    print("Unsupported response format:", file=sys.stderr)
    print(json.dumps(j, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
