#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from canvas_claw.client import CanvasClawClient
from canvas_claw.config import load_runtime_config
from canvas_claw.media import materialize_many
from canvas_claw.model_registry import resolve_model
from canvas_claw.output import save_result_bundle
from canvas_claw.tasks import build_video_request, submit_and_poll


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate videos with AI-video-agent")
    parser.add_argument("--prompt", required=True, help="Video prompt")
    parser.add_argument("--catalog-key", help="Model catalog key")
    parser.add_argument("--model", dest="catalog_key_alias", help="Alias for --catalog-key")
    parser.add_argument("--first-frame", help="First frame URL or local file path")
    parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio")
    parser.add_argument("--resolution", default="720p", help="Video resolution")
    parser.add_argument("--duration", type=int, default=8, help="Video duration")
    parser.add_argument("--generate-audio", action="store_true", help="Generate audio when supported")
    parser.add_argument("--output-dir", default="./output", help="Output directory")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    catalog_key = args.catalog_key or args.catalog_key_alias
    capability = "video-animate" if args.first_frame else "video-create"
    config = load_runtime_config()
    client = CanvasClawClient(config)
    model = resolve_model(capability=capability, catalog_key=catalog_key)

    image_urls = materialize_many(client, [args.first_frame], "image") if args.first_frame else []
    payload = build_video_request(
        prompt=args.prompt,
        capability=capability,
        provider=model.provider,
        model_id=model.model_id,
        image_urls=image_urls,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
        duration=args.duration,
        generate_audio=args.generate_audio,
    )
    payload["meta"]["catalog_key"] = model.catalog_key

    result = submit_and_poll(
        client,
        payload=payload,
        poll_interval=config.poll_interval,
        timeout=config.timeout,
    )
    metadata_path = save_result_bundle(
        output_dir=Path(args.output_dir),
        result=result,
        kind="video",
        metadata={
            "capability": capability,
            "catalog_key": model.catalog_key,
            "provider": model.provider,
            "model_id": model.model_id,
            "prompt": args.prompt,
        },
    )
    print(f"Saved video results to {metadata_path.parent}")


if __name__ == "__main__":
    main()
