"""Video provider registry and orchestration."""

import os
import sys

from common import download_file, discover_providers, MEDIA_CACHE

PROVIDERS = discover_providers("video")


def run_video(args):
    if not args.prompt:
        sys.exit("Error: --prompt is required.")
    if not args.image:
        sys.exit("Error: --image is required.")

    api_key = args.api or os.environ.get("CLAWDESS_VIDEO_API", "")
    if not api_key:
        sys.exit("Error: --api or CLAWDESS_VIDEO_API required.")

    provider_name = (args.provider or "FAL").upper()
    if provider_name not in PROVIDERS:
        sys.exit(f"Unknown video provider: {provider_name}. Available: {', '.join(PROVIDERS)}")

    full_prompt = "" + args.prompt

    print(f"\nGenerating video with provider={provider_name}, prompt={full_prompt}")

    video_result = PROVIDERS[provider_name].generate(api_key, full_prompt, args.image)

    if not video_result:
        msg = "Error generating video."
        sys.exit(msg)

    if os.path.isfile(video_result):
        print(f"Video on the way. {video_result}")
    else:
        print(f"Video on the way. MEDIA: {video_result}")
    
    download_file(video_result, MEDIA_CACHE)
