#!/usr/bin/env python3
"""Image creation and retouching.

create       : text to image, or edit an image by passing image_urls (v1, sync-capable)
cutout       : remove the background
ecommerce    : product photo set -- hero banner, lifestyle, detail, material, ...
poster       : campaign poster from an event brief
erase        : remove watermarks / objects, optionally mask-guided
upscale      : raise resolution
"""

from __future__ import annotations

import argparse

from shared.client import add_async_flags, run_cli, submit_and_maybe_poll

CREATE = "/openapi/v1/img/create"
CUTOUT = "/openapi/v2beta/image/cutout"
ECOMMERCE = "/openapi/v2beta/image/ecommerce"
POSTER = "/openapi/v2beta/image/poster"
ERASER = "/openapi/v2beta/image/magic-eraser"
ENHANCE = "/openapi/v2beta/image/enhance"


def cmd_create(client, args) -> dict:
    """Empty image_urls means text-to-image; non-empty means edit those images."""
    return client.post(CREATE, {
        "prompt": args.prompt,
        "image_urls": args.image_urls,
        "model": args.model,
        "ratio": args.ratio,
        "resolution": args.resolution,
        "sync_mod": not args.async_mode,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    })


def cmd_cutout(client, args) -> dict:
    return submit_and_maybe_poll(client, CUTOUT, {
        "method": "rm_background",
        "image_url": args.image_url,
        "output_format": args.output_format,
        "resolution": args.resolution,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_ecommerce(client, args) -> dict:
    """methods picks which shots to produce; omit it for the default hero banner."""
    return submit_and_maybe_poll(client, ECOMMERCE, {
        "methods": args.methods,
        "user_input": args.user_input,
        "product_info": args.product_info,
        "reference_image_urls": args.reference_image_urls,
        "language": args.language,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_poster(client, args) -> dict:
    return submit_and_maybe_poll(client, POSTER, {
        "method": args.method,
        "event_info": args.event_info,
        "reference_image_urls": args.reference_image_urls,
        "language": args.language,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_erase(client, args) -> dict:
    return submit_and_maybe_poll(client, ERASER, {
        "method": "inpainting",
        "image_url": args.image_url,
        "mask_url": args.mask_url,
        "instruction": args.instruction,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "quantity": args.quantity,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_upscale(client, args) -> dict:
    return submit_and_maybe_poll(client, ENHANCE, {
        "method": "upscale",
        "image_url": args.image_url,
        "scale": args.scale,
        "resolution": args.resolution,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_query(client, args) -> dict:
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


def _add_common(sub) -> None:
    sub.add_argument("--resolution", default="")
    sub.add_argument("--workspace-id", default="")
    sub.add_argument("--idempotency-key", default="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo image creation")
    sub = parser.add_subparsers(dest="command")

    create = sub.add_parser("create", help="text to image, or edit existing images")
    create.add_argument("--prompt", required=True)
    create.add_argument("--image-urls", nargs="*", default=[], help="pass these to edit them")
    create.add_argument("--model", default="")
    create.add_argument("--ratio", default="")
    create.add_argument("--resolution", default="")
    create.add_argument("--async-mode", action="store_true", help="return a workspace_id instead of waiting")
    create.add_argument("--callback-id", default="")
    create.add_argument("--idempotency-key", default="")

    cut = sub.add_parser("cutout", help="remove the background")
    cut.add_argument("--image-url", required=True)
    cut.add_argument("--output-format", default="", help="e.g. png")
    _add_common(cut)
    add_async_flags(cut)

    ecom = sub.add_parser("ecommerce", help="product photo set")
    ecom.add_argument("--reference-image-urls", nargs="*", default=[], help="product shots")
    ecom.add_argument("--methods", nargs="*", default=[],
                      help="hero_banner lifestyle_scene how_to_use close_detail material brand_closing")
    ecom.add_argument("--user-input", default="", help="what you want emphasised")
    ecom.add_argument("--product-info", default="")
    ecom.add_argument("--language", default="")
    ecom.add_argument("--aspect-ratio", default="")
    _add_common(ecom)
    add_async_flags(ecom)

    poster = sub.add_parser("poster", help="campaign poster")
    poster.add_argument("--event-info", required=True, help="what the poster is announcing")
    poster.add_argument("--reference-image-urls", nargs="*", default=[])
    poster.add_argument("--method", default="")
    poster.add_argument("--language", default="")
    poster.add_argument("--aspect-ratio", default="")
    _add_common(poster)
    add_async_flags(poster)

    erase = sub.add_parser("erase", help="remove watermark or object")
    erase.add_argument("--image-url", required=True)
    erase.add_argument("--mask-url", default="", help="white = area to erase")
    erase.add_argument("--instruction", default="", help="what to erase, in words")
    erase.add_argument("--aspect-ratio", default="")
    erase.add_argument("--quantity", type=int, help="how many variants")
    _add_common(erase)
    add_async_flags(erase)

    up = sub.add_parser("upscale", help="raise resolution")
    up.add_argument("--image-url", required=True)
    up.add_argument("--scale", type=int, help="e.g. 2 or 4")
    _add_common(up)
    add_async_flags(up)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    query.add_argument("--timeout", type=float, default=900)
    query.add_argument("--interval", type=float, default=10)

    return parser


HANDLERS = {
    "create": cmd_create,
    "cutout": cmd_cutout,
    "ecommerce": cmd_ecommerce,
    "poster": cmd_poster,
    "erase": cmd_erase,
    "upscale": cmd_upscale,
    "query": cmd_query,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
