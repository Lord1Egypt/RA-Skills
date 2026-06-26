"""Photo provider registry and orchestration."""

import os
import sys

from common import download_file, discover_providers, MEDIA_CACHE

PROVIDERS = discover_providers("photo")


def run_photo(args):
    if not args.prompt:
        sys.exit("Error: --prompt is required.")
    if not args.image:
        sys.exit("Error: --image is required.")

    api_key = args.api or os.environ.get("CLAWDESS_PHOTO_API", "")
    if not api_key:
        sys.exit("Error: --api or CLAWDESS_PHOTO_API required.")

    provider_name = (args.provider or "FAL").upper()
    if provider_name not in PROVIDERS:
        sys.exit(f"Unknown photo provider: {provider_name}. Available: {', '.join(PROVIDERS)}")

    print(f"Editing reference image with prompt: {args.prompt}")

    image_url = PROVIDERS[provider_name].generate(api_key, args.prompt, args.image)

    if not image_url:
        msg = "Error generating image."
        sys.exit(msg)
    else:
        print(f"Image on the way. MEDIA: {image_url}")

    download_file(image_url, MEDIA_CACHE)
