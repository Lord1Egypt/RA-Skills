#!/usr/bin/env python3
"""Generate images via Perchance unofficial endpoints.

Primary path:
  1) GET /verifyUser -> extract userKey
  2) POST /generate
  3) GET /downloadTemporaryImage

Usage:
  python perchance_generate.py --prompt "isometric office" --out ./out.png
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

import requests

BASE = "https://image-generation.perchance.org/api"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def _resolution(shape: str) -> str:
    table = {
        "portrait": "512x768",
        "square": "768x768",
        "landscape": "768x512",
    }
    if shape not in table:
        raise ValueError(f"Invalid shape: {shape}")
    return table[shape]


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "*/*"})
    return s


def _extract_user_key(html: str) -> str | None:
    m = re.search(r'"userKey":"([^"]+)"', html)
    return m.group(1) if m else None


def generate_perchance(
    *,
    prompt: str,
    out_path: Path,
    shape: str = "square",
    negative_prompt: str = "",
    guidance: float = 7.0,
    retries: int = 3,
    timeout: int = 45,
) -> dict:
    s = _session()
    last_err = None

    for attempt in range(1, retries + 1):
        try:
            verify = s.get(
                f"{BASE}/verifyUser",
                params={"thread": 0, "__cacheBust": random.random()},
                timeout=timeout,
            )
            verify.raise_for_status()
            key = _extract_user_key(verify.text)
            if not key:
                raise RuntimeError("userKey not found in verifyUser response")

            payload = {
                "generatorName": "ai-image-generator",
                "channel": "ai-text-to-image-generator",
                "subChannel": "public",
                "prompt": prompt,
                "negativePrompt": negative_prompt,
                "seed": -1,
                "resolution": _resolution(shape),
                "guidanceScale": guidance,
            }
            params = {
                "userKey": key,
                "requestId": f"aiImageCompletion{random.randint(1, 2**30)}",
                "__cacheBust": random.random(),
            }

            gen = s.post(f"{BASE}/generate", params=params, json=payload, timeout=timeout)
            gen.raise_for_status()
            data = gen.json()
            image_id = data["imageId"]

            dl = s.get(
                f"{BASE}/downloadTemporaryImage",
                params={"imageId": image_id},
                timeout=timeout,
            )
            dl.raise_for_status()

            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(dl.content)

            return {
                "ok": True,
                "provider": "perchance-unofficial",
                "path": str(out_path),
                "bytes": len(dl.content),
                "meta": data,
            }
        except Exception as e:  # noqa: BLE001
            last_err = str(e)
            if attempt < retries:
                time.sleep(min(8, 2 * attempt))

    return {
        "ok": False,
        "provider": "perchance-unofficial",
        "error": last_err or "unknown error",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shape", default="square", choices=["portrait", "square", "landscape"])
    ap.add_argument("--negative", default="")
    ap.add_argument("--guidance", type=float, default=7.0)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=45)
    args = ap.parse_args()

    out = Path(args.out).expanduser().resolve()

    res = generate_perchance(
        prompt=args.prompt,
        out_path=out,
        shape=args.shape,
        negative_prompt=args.negative,
        guidance=args.guidance,
        retries=max(1, args.retries),
        timeout=max(5, args.timeout),
    )

    print(json.dumps(res, ensure_ascii=False))
    return 0 if res.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
