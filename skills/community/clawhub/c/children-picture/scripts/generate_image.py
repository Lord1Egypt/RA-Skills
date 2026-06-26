#!/usr/bin/env python3
# /// script
# requires-python = ">=3.7"
# dependencies = [
#     "openai",
# ]
# ///
"""
Generate images using Baidu's ERNIE-Image API.

Usage:
    python generate_image.py --prompt "your image description" --filename "output.png" [--resolution 1024x1024] [--api-key KEY]
"""
import argparse
import os
import sys
from pathlib import Path
import base64
from openai import OpenAI

def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    # Try multiple env var names for compatibility
    for key in ["ERNIE-Image_API_KEY", "ERNIE_Image_API_KEY", "BAIDU_API_KEY"]:
        value = os.environ.get(key)
        if value:
            return value
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using ERNIE-Image"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1024x1024", "1376x768", "1264x848", "1200x896", "896x1200", "848x1264", "768x1376"],
        default="1024x1024",
        help="Output resolution: 1024x1024, 1376x768, 1264x848, 1200x896, 896x1200, 848x1264, 768x1376"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides ERNIE-Image_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set  ERNIE-Image_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)



    # Initialise client
    client = OpenAI(api_key=api_key,
                    base_url="https://aistudio.baidu.com/llm/lmapi/v3",
                    )

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_resolution = args.resolution

    contents = args.prompt
    print(f"Generating image with resolution {output_resolution}...")

    try:
        img = client.images.generate(
                model="ERNIE-Image-Turbo",
                prompt=contents,
                size=output_resolution,
                response_format="b64_json",
            )

        # Process response and convert to PNG
        image_bytes = base64.b64decode(img.data[0].b64_json)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"Image saved to {output_path}")

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
