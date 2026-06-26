#!/usr/bin/env python3
import sys
import argparse
import os
import requests
from minimax_client import MinimaxClient, get_standard_path


def main():
    parser = argparse.ArgumentParser(description="Generate image using MiniMax image-01")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--model", default="image-01", help="Model name (image-01 or image-01-live)")
    parser.add_argument("--ratio", default="1:1", help="Aspect ratio")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(client.get_budget_report(args.model))
    if args.estimate:
        sys.exit(0)

    data = {
        "model": args.model,
        "prompt": args.prompt,
        "aspect_ratio": args.ratio,
        "n": 1,
        "response_format": "url"
    }

    print(f"Generating image: {args.prompt}...")
    resp = client.post("image_generation", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["image_urls"][0]
        target_dir, filename_base = get_standard_path("IMG", project=args.project, prompt_slug=args.prompt, output_dir=args.output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.jpg")

        img_data = requests.get(url).content
        with open(filepath, 'wb') as f:
            f.write(img_data)

        client.print_saved_result(filepath, "Image", project=args.project)
        print(f"MEDIA:{filepath}")
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    main()
