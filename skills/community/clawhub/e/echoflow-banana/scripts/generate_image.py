#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.25.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate or edit images using EchoFlow API with Nano Banana Pro (Gemini 3 Pro Image).

EchoFlow API: https://api.echoflow.cn/
Model: gemini-3.1-flash-image-preview (default), gemini-3-pro-image-preview

Usage:
    # Generate image
    uv run generate_image.py --prompt "your image description" --filename "output.png"

    # Edit image (single)
    uv run generate_image.py --prompt "edit instructions" --filename "output.png" -i "/path/input.png"

    # Multi-image composition (up to 14 images)
    uv run generate_image.py --prompt "combine these into one scene" --filename "output.png" -i img1.png -i img2.png

    # With custom resolution
    uv run generate_image.py --prompt "sunset" --filename "sunset.png" --resolution 2K

Security notes:
    - API key is read ONLY from ECHOFLOW_API_KEY env var or --api-key argument.
    - No fallback to OPENAI_API_KEY or GEMINI_API_KEY.
    - Do NOT pass --api-base to untrusted hosts; your API key will be sent there.
    - Prefer ECHOFLOW_API_KEY env var over --api-key to avoid key exposure in process list.
"""

import argparse
import base64
import os
import re
import sys
from io import BytesIO
from pathlib import Path


def get_api_key(provided_key: str | None) -> str | None:
    """
    Get API key from --api-key argument first, then ECHOFLOW_API_KEY env var only.
    No fallback to OPENAI_API_KEY or GEMINI_API_KEY to avoid unintended credential use.
    """
    if provided_key:
        return provided_key
    return os.environ.get("ECHOFLOW_API_KEY")


def load_image_as_base64(image_path: str) -> str:
    """Load an image file and return base64 encoded string."""
    from PIL import Image as PILImage

    with PILImage.open(image_path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def extract_image_from_markdown(content: str) -> bytes | None:
    """Extract image data from markdown format: ![image](data:image/jpeg;base64,...)"""
    pattern = r'!\[.*?\]\(data:image/[^;]+;base64,([A-Za-z0-9+/=]+)\)'
    match = re.search(pattern, content)
    if match:
        return base64.b64decode(match.group(1))
    return None


def save_image(image_data: bytes, output_path: Path) -> None:
    """Save image bytes to file as PNG."""
    from PIL import Image as PILImage

    image = PILImage.open(BytesIO(image_data))
    if image.mode == 'RGBA':
        rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
        rgb_image.save(str(output_path), 'PNG')
    elif image.mode == 'RGB':
        image.save(str(output_path), 'PNG')
    else:
        image.convert('RGB').save(str(output_path), 'PNG')


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using EchoFlow API with Nano Banana Pro (Gemini 3 Pro Image)"
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
        "--input-image", "-i",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image path(s) for editing/composition. Can be specified multiple times (up to 14 images)."
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="Output resolution: 1K (default), 2K, or 4K"
    )
    parser.add_argument(
        "--model", "-m",
        default="gemini-3.1-flash-image-preview",
        help="Model name (default: gemini-3.1-flash-image-preview). Alt: gemini-3-pro-image-preview"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="EchoFlow API key. Prefer ECHOFLOW_API_KEY env var to avoid key exposure in process list."
    )
    parser.add_argument(
        "--api-base",
        default="https://api.echoflow.cn/v1",
        help=(
            "API base URL (default: https://api.echoflow.cn/v1). "
            "WARNING: your API key is sent to this host. Do NOT use untrusted endpoints."
        )
    )

    args = parser.parse_args()

    # Get API key — only ECHOFLOW_API_KEY, no silent fallback to other keys
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Set the ECHOFLOW_API_KEY environment variable, or pass --api-key.", file=sys.stderr)
        print("  Windows: $env:ECHOFLOW_API_KEY = 'sk-...'", file=sys.stderr)
        print("  Linux/macOS: export ECHOFLOW_API_KEY='sk-...'", file=sys.stderr)
        sys.exit(1)

    import httpx
    from PIL import Image as PILImage

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images if provided (up to 14 supported by Nano Banana Pro)
    input_images = []
    output_resolution = args.resolution

    if args.input_images:
        if len(args.input_images) > 14:
            print(f"Error: Too many input images ({len(args.input_images)}). Maximum is 14.", file=sys.stderr)
            sys.exit(1)

        max_input_dim = 0
        for img_path in args.input_images:
            try:
                b64_data = load_image_as_base64(img_path)
                input_images.append(b64_data)
                print(f"Loaded input image: {img_path}")

                with PILImage.open(img_path) as img:
                    width, height = img.size
                    max_input_dim = max(max_input_dim, width, height)
            except Exception as e:
                print(f"Error loading input image '{img_path}': {e}", file=sys.stderr)
                sys.exit(1)

        # Auto-detect resolution from largest input dimension
        if args.resolution == "1K" and max_input_dim > 0:
            if max_input_dim >= 3000:
                output_resolution = "4K"
            elif max_input_dim >= 1500:
                output_resolution = "2K"
            else:
                output_resolution = "1K"
            print(f"Auto-detected resolution: {output_resolution} (from max input dimension {max_input_dim}px)")

    # Build message content
    msg_content: list | str
    if input_images:
        msg_content = []
        for b64_data in input_images:
            msg_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64_data}"}
            })
        msg_content.append({"type": "text", "text": args.prompt})
        img_count = len(input_images)
        print(f"Processing {img_count} image{'s' if img_count > 1 else ''} with resolution {output_resolution}...")
    else:
        msg_content = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    request_body = {
        "model": args.model,
        "messages": [{"role": "user", "content": msg_content}],
        "response_modalities": ["TEXT", "IMAGE"],
        "image_config": {"image_size": output_resolution}
    }

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = httpx.post(
            f"{args.api_base}/chat/completions",
            headers=headers,
            json=request_body,
            timeout=120.0
        )

        if response.status_code != 200:
            print(f"Error: API returned status {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            sys.exit(1)

        result = response.json()
        choice = result.get("choices", [{}])[0]
        message = choice.get("message", {})
        content_str = message.get("content", "")

        image_saved = False

        # 1. EchoFlow returns image as markdown: ![image](data:image/jpeg;base64,...)
        if content_str:
            print(f"Model response: {content_str[:80]}...")
            image_data = extract_image_from_markdown(content_str)
            if image_data:
                save_image(image_data, output_path)
                image_saved = True

        # 2. Gemini-style parts with inline_data
        if not image_saved:
            for part in message.get("parts", []):
                if "inline_data" in part:
                    raw = part["inline_data"].get("data", b"")
                    image_data = base64.b64decode(raw) if isinstance(raw, str) else raw
                    save_image(image_data, output_path)
                    image_saved = True
                    break

        # 3. OpenAI images API style: data[].b64_json
        if not image_saved:
            for item in result.get("data", []):
                if "b64_json" in item:
                    save_image(base64.b64decode(item["b64_json"]), output_path)
                    image_saved = True
                    break

        if image_saved:
            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
            print(f"MEDIA: {full_path}")
        else:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
