"""Voice provider registry and orchestration."""

import os
import sys

from common import discover_providers

PROVIDERS = discover_providers("voice")


def run_voice(args):
    api_key = args.api or os.environ.get("CLAWDESS_VOICE_API", "")
    if not api_key:
        sys.exit("Error: --api or CLAWDESS_VOICE_API required.")
    if not args.prompt:
        sys.exit("Error: --prompt is required.")

    provider_name = (args.provider or "ALIYUN").upper()
    if provider_name not in PROVIDERS:
        sys.exit(f"Unknown voice provider: {provider_name}. Available: {', '.join(PROVIDERS)}")

    print(f"\nGenerating voice: {args.prompt}")

    voice_url = PROVIDERS[provider_name].generate(api_key, args.prompt)

    if not voice_url:
        msg = "Error generating Voice."
        sys.exit(msg)
    else:
        print(f"Voice on the way. MEDIA: {voice_url}")
