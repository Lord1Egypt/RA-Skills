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
from canvas_claw.tasks import build_image_request, submit_and_poll


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate images with AI-video-agent")
    parser.add_argument("--prompt", required=True, help="Image prompt")
    parser.add_argument("--catalog-key", help="Model catalog key")
    parser.add_argument("--model", dest="catalog_key_alias", help="Alias for --catalog-key")
    parser.add_argument("--reference-image", action="append", default=[], help="Reference image URL or file path")
    parser.add_argument("--aspect-ratio", default="1:1", help="Aspect ratio")
    parser.add_argument("--resolution", default="2K", help="Resolution or quality")
    parser.add_argument("--output-dir", default="./output", help="Output directory")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    catalog_key = args.catalog_key or args.catalog_key_alias
    capability = "image-remix" if args.reference_image else "image-create"
    config = load_runtime_config()
    client = CanvasClawClient(config)
    model = resolve_model(capability=capability, catalog_key=catalog_key)

    image_urls = materialize_many(client, args.reference_image, "image") if args.reference_image else []
    payload = build_image_request(
        prompt=args.prompt,
        capability=capability,
        task_type=model.task_type,
        provider=model.provider,
        model_id=model.model_id,
        image_urls=image_urls,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
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
        kind="image",
        metadata={
            "capability": capability,
            "catalog_key": model.catalog_key,
            "provider": model.provider,
            "model_id": model.model_id,
            "prompt": args.prompt,
        },
    )
    print(f"Saved image results to {metadata_path.parent}")


if __name__ == "__main__":
    main()
