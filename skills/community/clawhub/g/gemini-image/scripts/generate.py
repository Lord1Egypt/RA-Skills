#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate or edit images using Gemini API with support for multiple reference images.

Usage:
    uv run generate.py --prompt "description" --output out.png
    uv run generate.py --prompt "combine these" -i ref1.png -i ref2.png --output out.png
    uv run generate.py --prompt "edit this" -i source.png --model gemini-2.5-flash-image --output out.png
"""

import argparse
import os
import sys
from pathlib import Path


MODELS = {
    "flash": "gemini-2.5-flash-image",           # Fast, simpler config
    "flash2": "gemini-3.1-flash-image-preview",  # Nano Banana 2 — best price/perf, thinking, text rendering
    "pro": "gemini-3-pro-image-preview",         # Full image_config support, highest quality
    "exp": "gemini-2.0-flash-exp",               # Experimental, good for edits
}

ASPECT_RATIOS = [
    "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4",
    "9:16", "16:9", "21:9",
    "4:1", "1:4", "8:1", "1:8",  # New in Nano Banana 2
]

# Default model
DEFAULT_MODEL = "pro"


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def main():
    parser = argparse.ArgumentParser(description="Generate images with Gemini (multiple references supported)")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt/instructions")
    parser.add_argument("--output", "-o", required=True, help="Output filename")
    parser.add_argument("--input-image", "-i", action="append", dest="inputs", help="Input image(s) - can repeat")
    parser.add_argument("--model", "-m", choices=list(MODELS.keys()), default=DEFAULT_MODEL,
                        help=f"Model: {', '.join(MODELS.keys())} (default: {DEFAULT_MODEL})")
    parser.add_argument("--resolution", "-r", choices=["512", "1K", "2K", "4K"], default="1K", help="Resolution (default: 1K, 512 for fast iterations)")
    parser.add_argument("--aspect-ratio", "-a", help="Aspect ratio e.g. '16:9', '1:1', '9:16'")
    parser.add_argument("--thinking", "-t", choices=["minimal", "high", "dynamic"], default=None, help="Thinking level (flash2/pro only, default: minimal)")
    parser.add_argument("--api-key", "-k", help="Gemini API key (or set GEMINI_API_KEY)")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key. Set GEMINI_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)

    # Validate aspect ratio
    if args.aspect_ratio and args.aspect_ratio not in ASPECT_RATIOS:
        print(f"Warning: '{args.aspect_ratio}' not in supported ratios: {', '.join(ASPECT_RATIOS)}", file=sys.stderr)

    # Warn if using features unsupported by model
    if args.model not in ("pro", "flash2") and (args.aspect_ratio or args.resolution != "1K"):
        print(f"Note: --aspect-ratio and --resolution only work with 'pro' and 'flash2' models", file=sys.stderr)
    if args.thinking and args.model not in ("pro", "flash2"):
        print(f"Note: --thinking only works with 'pro' and 'flash2' models", file=sys.stderr)

    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)
    model_name = MODELS[args.model]

    # Build contents: images first, then prompt
    contents = []

    if args.inputs:
        if len(args.inputs) > 14:
            print(f"Warning: {len(args.inputs)} images provided, max is 14. Using first 14.", file=sys.stderr)
            args.inputs = args.inputs[:14]

        for img_path in args.inputs:
            try:
                img = PILImage.open(img_path)
                contents.append(img)
                print(f"Loaded: {img_path}")
            except Exception as e:
                print(f"Error loading {img_path}: {e}", file=sys.stderr)
                sys.exit(1)

    contents.append(args.prompt)

    # Build config - pro and flash2 support full image_config
    config_kwargs = {"response_modalities": ["TEXT", "IMAGE"]}

    if args.model in ("pro", "flash2"):
        image_config_kwargs = {}
        if args.resolution:
            image_config_kwargs["image_size"] = args.resolution
        if args.aspect_ratio:
            image_config_kwargs["aspect_ratio"] = args.aspect_ratio
        if image_config_kwargs:
            config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    # Thinking level (flash2 and pro)
    if args.thinking and args.model in ("pro", "flash2"):
        thinking_map = {"minimal": "MINIMAL", "high": "HIGH", "dynamic": "DYNAMIC"}
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=thinking_map.get(args.thinking, "MINIMAL")
        )

    config = types.GenerateContentConfig(**config_kwargs)

    print(f"Generating with {model_name}...")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config,
        )

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image_saved = False
        for part in response.parts:
            if part.text is not None:
                print(f"Model: {part.text}")
            elif part.inline_data is not None:
                from io import BytesIO
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Save as PNG, handle RGBA
                if image.mode == "RGBA":
                    image.save(str(output_path), "PNG")
                elif image.mode == "RGB":
                    image.save(str(output_path), "PNG")
                else:
                    image.convert("RGB").save(str(output_path), "PNG")
                image_saved = True

        if image_saved:
            full_path = output_path.resolve()
            print(f"\nSaved: {full_path}")
            print(f"MEDIA: {full_path}")
        else:
            print("Error: No image in response", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
