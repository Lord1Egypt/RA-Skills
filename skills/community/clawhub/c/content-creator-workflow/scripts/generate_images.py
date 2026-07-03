"""Image generation helper built on the OpenAI DALL-E 3 API.

Generates a single image (or a batch from a prompts file) and saves the
results to a configurable output directory.
"""

import os
import sys
import time
from typing import Dict, List, Optional

import requests
from openai import OpenAI, OpenAIError

DEFAULT_OUTPUT_DIR = os.environ.get(
    "CONTENT_CREATOR_OUTPUT_DIR", os.path.join(os.getcwd(), "generated")
)
IMAGE_MODEL = "dall-e-3"
DOWNLOAD_TIMEOUT_SECONDS = 60
MAX_FILENAME_LEN = 50


class ImageGenerationError(RuntimeError):
    """Raised when an image cannot be generated or downloaded."""


def _get_client() -> OpenAI:
    """Return an OpenAI client, failing clearly if the API key is missing."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ImageGenerationError(
            "OPENAI_API_KEY environment variable is not set."
        )
    return OpenAI(api_key=api_key)


def _safe_filename(prompt: str) -> str:
    """Build a filesystem-safe, collision-resistant filename from a prompt."""
    cleaned = "".join(
        ch for ch in prompt if ch.isalnum() or ch in (" ", "-", "_")
    ).strip()[:MAX_FILENAME_LEN].replace(" ", "_")
    if not cleaned:
        cleaned = "image"
    return f"{cleaned}_{int(time.time())}.png"


def generate_image(
    prompt: str,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid",
) -> Dict[str, str]:
    """Generate a single image from a prompt and save it to disk.

    Args:
        prompt: The text prompt to generate from.
        output_dir: Directory where the PNG is written (created if missing).
        size: Image size supported by DALL-E 3.
        quality: ``standard`` or ``hd``.
        style: ``vivid`` or ``natural``.

    Returns:
        A dict with ``image_path``, ``revised_prompt`` and ``original_prompt``.

    Raises:
        ImageGenerationError: If the prompt is empty, the API fails, or the
            generated image cannot be downloaded/saved.
    """
    if not prompt or not prompt.strip():
        raise ImageGenerationError("Prompt must be a non-empty string.")

    client = _get_client()
    print(f"Generating image for prompt: {prompt[:50]}...")

    try:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1,
        )
    except OpenAIError as exc:
        raise ImageGenerationError(f"Image generation API failed: {exc}") from exc

    if not response.data:
        raise ImageGenerationError("API returned no image data.")

    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt or prompt

    try:
        download = requests.get(image_url, timeout=DOWNLOAD_TIMEOUT_SECONDS)
        download.raise_for_status()
    except requests.RequestException as exc:
        raise ImageGenerationError(f"Failed to download generated image: {exc}") from exc

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, _safe_filename(prompt))
    with open(output_path, "wb") as handle:
        handle.write(download.content)

    print(f"Image saved to {output_path}")
    print(f"Revised prompt used: {revised_prompt}")

    return {
        "image_path": output_path,
        "revised_prompt": revised_prompt,
        "original_prompt": prompt,
    }


def batch_generate(prompts_file: str) -> List[Dict[str, str]]:
    """Generate images for every non-empty line in a prompts file.

    Args:
        prompts_file: Path to a UTF-8 text file with one prompt per line.

    Returns:
        A list of result dicts for prompts that succeeded.

    Raises:
        ImageGenerationError: If the prompts file does not exist.
    """
    if not os.path.isfile(prompts_file):
        raise ImageGenerationError(f"Prompts file not found: {prompts_file!r}")

    with open(prompts_file, "r", encoding="utf-8") as handle:
        prompts = [line.strip() for line in handle if line.strip()]

    results: List[Dict[str, str]] = []
    for prompt in prompts:
        try:
            results.append(generate_image(prompt))
        except ImageGenerationError as exc:
            print(f"Skipping prompt due to error: {exc}")
    return results


def main() -> None:
    """CLI entry point: single-prompt or batch image generation."""
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python generate_images.py <prompt>       - Generate single image")
        print("  python generate_images.py <prompts.txt>  - Batch generate from file")
        sys.exit(1)

    arg = sys.argv[1]
    try:
        if os.path.isfile(arg):
            batch_generate(arg)
        else:
            generate_image(arg)
    except ImageGenerationError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
