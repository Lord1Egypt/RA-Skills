#!/usr/bin/env python3
"""
Herdsman image-to-image (img2img) script.

For style transfer, full repaint, and similar scenarios.
"""

import argparse
import json
import os
import sys
from datetime import datetime

from herdsman_client import HerdsmanAPIError, HerdsmanClient, prepare_media_input


def default_output_dir() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "outputs"))
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def auto_output_path(index: int) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(default_output_dir(), f"img2img_{timestamp}_{index + 1}.png")


def normalize_image_input(value: str) -> str:
    return prepare_media_input(value, default_mime_type="image/png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Herdsman img2img")
    parser.add_argument("prompt", help="Generation prompt")
    parser.add_argument("--model", required=True, help="Model ID")
    parser.add_argument("--image", required=True, help="Input image: local path, URL, or data URL")
    parser.add_argument("--size", default="1024x1024", help="Output size")
    parser.add_argument("--n", type=int, default=1, help="Number of outputs")
    parser.add_argument("--steps", type=int, help="Sampling steps")
    parser.add_argument("--cfg-scale", type=float, help="CFG scale")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="Herdsman API base URL")
    parser.add_argument("--api-key", default="", help="Optional API Key")
    parser.add_argument("--output", "-o", help="Single image output file path")
    parser.add_argument("--format", choices=["url", "b64_json"], default="url", help="Response format")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    parser.add_argument("--auto-save", action="store_true", help="Auto save to outputs/")
    parser.add_argument("--download", action="store_true", help="Download file if URL is returned")
    args = parser.parse_args()

    try:
        image = normalize_image_input(args.image)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    client = HerdsmanClient(base_url=args.base_url, api_key=args.api_key, timeout=120)

    try:
        result = client.img2img(
            model=args.model,
            image=image,
            prompt=args.prompt,
            size=args.size,
            n=args.n,
            response_format=args.format,
            steps=args.steps,
            cfg_scale=args.cfg_scale,
        )
    except HerdsmanAPIError as exc:
        print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    data = result.get("data", [])
    if not data:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    for index, item in enumerate(data):
        target_path = args.output if len(data) == 1 else None
        if not target_path and args.auto_save:
            target_path = auto_output_path(index)

        if item.get("b64_json"):
            if target_path:
                saved = client.save_base64_file(item["b64_json"], target_path)
                print(f"Image {index + 1} saved: {saved}")
            else:
                print(f"Image {index + 1} returned b64_json, consider using --auto-save or --output")
            continue

        url = item.get("url", "")
        if not url:
            print(f"Image {index + 1} returned empty")
            continue

        if target_path and (args.download or args.auto_save):
            try:
                saved = client.download_to_file(url, target_path, timeout=120)
                print(f"Image {index + 1} downloaded: {saved}")
            except HerdsmanAPIError as exc:
                print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Image {index + 1} URL: {url}")


if __name__ == "__main__":
    main()