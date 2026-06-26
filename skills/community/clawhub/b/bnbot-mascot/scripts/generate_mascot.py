#!/usr/bin/env python3
"""
BNBOT Mascot Generator - Generate mascot images in consistent style using reference images.

Uses Gemini's image understanding to match the style of existing reference images,
then applies green-screen chromakey for transparent output.

Usage:
    from generate_mascot import generate_mascot

    # Generate with auto-selected reference
    result = generate_mascot(
        action="waving hello cheerfully",
        output_path="mascot_wave.png",
    )

    # Generate with specific reference
    result = generate_mascot(
        action="holding a golden trophy",
        output_path="mascot_trophy.png",
        reference="full-body-front",
    )
"""

import os
import sys
import base64
import io
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

# Import chromakey from sibling skill
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "transparent-image-gen" / "scripts"))
from chromakey_despill import chromakey_with_despill

SKILL_DIR = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_DIR / "references"

# Available reference images
REFERENCES = {
    "logo-head-claws": {
        "file": "logo-head-claws.png",
        "desc": "Head + claws only, no body. Best for logo/icon generation.",
    },
    "full-body-front": {
        "file": "full-body-front.png",
        "desc": "Full body, front-facing, symmetric pose, claws raised.",
    },
    "full-body-side": {
        "file": "full-body-side.png",
        "desc": "Full body, playful side pose, one claw raised.",
    },
    "full-body-action": {
        "file": "full-body-action.png",
        "desc": "Full body, action pose, LED heart eye, dynamic.",
    },
    "full-body-cute": {
        "file": "full-body-cute.png",
        "desc": "Full body, cute pose, CRT TV head, winking smile.",
    },
}

# Character description - the core identity
CHARACTER_IDENTITY = (
    "This is BNBOT's mascot character - a lobster robot (Lobster Bot). "
    "Key features that MUST be preserved exactly: "
    "1. HEAD: Retro golden TV/monitor with dark screen, LED pixel face "
    "   (pink/red pixel HEART left eye, golden pixel DASH right eye, pixel smirk mouth). "
    "2. ANTENNA: Two metal antenna with golden ball tips on top of the TV head. "
    "3. CLAWS: Golden lobster claws with gear details at joints (mechanical but not overly complex). "
    "4. BODY (if full body): Red-orange lobster body, chibi proportions. "
    "5. STYLE: Cartoon vector, cel-shaded, thick bold outlines, vibrant colors, sticker art quality. "
    "6. COLORS: Golden amber frame (#FFD700), dark screen, pink heart eye (#FF4466), "
    "   red-orange body (#E85D3A). "
)

GREEN_SCREEN_SUFFIX = (
    "The background MUST be a solid, flat, uniform chromakey green color (#00FF00). "
    "NO variation, NO gradients, NO shadows on the background. "
    "The character should have a thin white outline to separate from the green. "
    "CRITICAL: The character must NOT contain ANY green colors. "
    "Use gold, red, silver, black, white, pink, orange colors only. "
)


def _load_api_key() -> str:
    key = os.environ.get("GOOGLE_AI_API_KEY")
    if key:
        return key
    env_path = Path("/Users/jacklee/Projects/BNBOT/.env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("GOOGLE_AI_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("GOOGLE_AI_API_KEY not found")


def _load_reference_image(name: str) -> Image.Image:
    """Load a reference image by name."""
    if name not in REFERENCES:
        raise ValueError(f"Unknown reference: {name}. Available: {list(REFERENCES.keys())}")
    path = REFERENCES_DIR / REFERENCES[name]["file"]
    if not path.exists():
        raise FileNotFoundError(f"Reference image not found: {path}")
    return Image.open(path).convert("RGBA")


def _image_to_part(img: Image.Image, max_size: int = 512):
    """Convert PIL Image to Gemini Part, resized for efficiency."""
    from google.genai import types

    # Resize for API efficiency
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    raw = buf.getvalue()

    return types.Part(inline_data=types.Blob(mime_type="image/png", data=raw))


def generate_mascot(
    action: str,
    output_path: str | Path | None = None,
    reference: str = "full-body-front",
    background: str = "transparent",
    model: str = "gemini-3-pro-image-preview",
    max_retries: int = 3,
    **despill_kwargs,
) -> Image.Image:
    """Generate a BNBOT mascot image in consistent style.

    Args:
        action: What the character is doing (e.g., "waving hello", "holding a coin").
        output_path: Optional path to save the result PNG.
        reference: Which reference image to use. Options:
            - "logo-head-claws": Head + claws only (for icons)
            - "full-body-front": Front facing full body
            - "full-body-side": Side pose full body
            - "full-body-action": Action pose
            - "full-body-cute": Cute pose
        background: "transparent" (default), "black", or "white".
        model: Gemini model ID.
        max_retries: Retry count for rate limits.
        **despill_kwargs: Extra args for chromakey_with_despill().

    Returns:
        RGBA PIL Image.
    """
    from google import genai
    from google.genai import types

    api_key = _load_api_key()
    client = genai.Client(api_key=api_key)

    # Load reference image
    ref_img = _load_reference_image(reference)
    ref_part = _image_to_part(ref_img)

    # Build prompt
    is_logo = reference == "logo-head-claws"

    prompt_text = (
        f"Generate a new image of this EXACT same character in a different pose/action. "
        f"{CHARACTER_IDENTITY} "
        f"The character is: {action}. "
    )

    if is_logo:
        prompt_text += (
            "IMPORTANT: Show ONLY the head and claws, NO body, NO legs, NO tail. "
        )

    prompt_text += (
        "1:1 square aspect ratio. "
        "Match the EXACT same art style, line thickness, coloring, and character design "
        "as the reference image. "
        "Style: bold cartoon vector, cel-shaded, thick outlines, vibrant colors, "
        "premium mascot sticker art. "
    )

    prompt_text += GREEN_SCREEN_SUFFIX

    # Build content with reference image + text prompt
    contents = [
        ref_part,
        types.Part(text=prompt_text),
    ]

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                ),
            )

            for part in response.candidates[0].content.parts:
                if (
                    part.inline_data
                    and part.inline_data.mime_type
                    and part.inline_data.mime_type.startswith("image/")
                ):
                    raw = part.inline_data.data
                    if isinstance(raw, str):
                        raw = base64.b64decode(raw)

                    gen_img = Image.open(io.BytesIO(raw))

                    # Apply chromakey for transparent background
                    result = chromakey_with_despill(gen_img, **despill_kwargs)

                    # Apply background if requested
                    if background == "black":
                        bg = Image.new("RGBA", result.size, (0, 0, 0, 255))
                        result = Image.alpha_composite(bg, result)
                    elif background == "white":
                        bg = Image.new("RGBA", result.size, (255, 255, 255, 255))
                        result = Image.alpha_composite(bg, result)

                    if output_path:
                        output_path = Path(output_path)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        result.save(output_path, "PNG")

                    return result

            raise RuntimeError("No image found in model response")

        except Exception as e:
            err = str(e)
            if any(code in err for code in ("503", "UNAVAILABLE", "429")):
                wait = 15 * (attempt + 1)
                print(f"Rate limited, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise

    raise RuntimeError(f"Failed after {max_retries} retries")


def list_references():
    """Print available reference images."""
    print("Available references:")
    for name, info in REFERENCES.items():
        exists = "✓" if (REFERENCES_DIR / info["file"]).exists() else "✗"
        print(f"  [{exists}] {name}: {info['desc']}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python generate_mascot.py <action> <output.png> [reference]")
        print('Example: python generate_mascot.py "waving hello" wave.png full-body-front')
        print()
        list_references()
        sys.exit(1)

    action = sys.argv[1]
    output = sys.argv[2]
    ref = sys.argv[3] if len(sys.argv) > 3 else "full-body-front"

    print(f"Generating: {action} (ref: {ref})")
    result = generate_mascot(action, output_path=output, reference=ref)
    print(f"Saved: {output} ({result.size[0]}x{result.size[1]})")
