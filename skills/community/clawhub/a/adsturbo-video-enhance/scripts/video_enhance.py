#!/usr/bin/env python3
"""Video clean-up: same footage, better condition. Nothing in frame changes meaning.

upscale        : raise resolution (v1 line)
remove-object  : erase watermarks / logos / props (v1 line)
subtitle       : burn in or translate subtitles
enhance        : v2beta upscale line, accepts explicit resolution
erase          : v2beta erase line, adds `rm_subtitle` (strip burnt-in subtitles)
"""

from __future__ import annotations

import argparse

from shared.client import add_async_flags, run_cli, submit_and_maybe_poll

UPSCALE = "/openapi/v1/video/upscale"
INPAINT = "/openapi/v1/video/inpaint"
SUBTITLE = "/openapi/v1/video/subtitle"
V2_ENHANCE = "/openapi/v2beta/video/enhance"
V2_ERASER = "/openapi/v2beta/video/magic-eraser"


def cmd_upscale(client, args) -> dict:
    return submit_and_maybe_poll(client, UPSCALE, {
        "video_url": args.video_url,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_remove_object(client, args) -> dict:
    return submit_and_maybe_poll(client, INPAINT, {
        "video_url": args.video_url,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_subtitle(client, args) -> dict:
    return submit_and_maybe_poll(client, SUBTITLE, {
        "video_url": args.video_url,
        "source_language": args.source_language,
        "translate_language": args.translate_language,
        "subtitle_format": args.subtitle_format,
        "style_type": args.style_type,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_enhance(client, args) -> dict:
    """v2beta upscale: same job as `upscale`, but resolution/duration are explicit."""
    return submit_and_maybe_poll(client, V2_ENHANCE, {
        "method": "upscale",
        "video_url": args.video_url,
        "resolution": args.resolution,
        "duration": args.duration,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_erase(client, args) -> dict:
    """v2beta erase. method=inpainting removes objects, rm_subtitle strips burnt-in text."""
    return submit_and_maybe_poll(client, V2_ERASER, {
        "method": args.method,
        "video_url": args.video_url,
        "duration": args.duration,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_query(client, args) -> dict:
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


def _add_source_flags(sub) -> None:
    sub.add_argument("--video-url", default="")
    sub.add_argument("--workspace-id", default="", help="reuse a previous result as input")
    sub.add_argument("--idempotency-key", default="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo video clean-up")
    sub = parser.add_subparsers(dest="command")

    up = sub.add_parser("upscale", help="raise resolution / 4K")
    _add_source_flags(up)
    add_async_flags(up)

    rm = sub.add_parser("remove-object", help="erase watermark, logo or prop")
    _add_source_flags(rm)
    add_async_flags(rm)

    sub_cmd = sub.add_parser("subtitle", help="add or translate subtitles")
    _add_source_flags(sub_cmd)
    sub_cmd.add_argument("--source-language", default="")
    sub_cmd.add_argument("--translate-language", default="")
    sub_cmd.add_argument("--subtitle-format", default="")
    sub_cmd.add_argument("--style-type", default="")
    add_async_flags(sub_cmd)

    enh = sub.add_parser("enhance", help="v2beta upscale with explicit resolution")
    _add_source_flags(enh)
    enh.add_argument("--resolution", default="", help="e.g. 2k / 4k")
    enh.add_argument("--duration", type=int, help="source length in seconds, for pricing")
    add_async_flags(enh)

    era = sub.add_parser("erase", help="v2beta erase, incl. burnt-in subtitle removal")
    _add_source_flags(era)
    era.add_argument("--method", default="inpainting", choices=["inpainting", "rm_subtitle"])
    era.add_argument("--duration", type=int)
    add_async_flags(era)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    query.add_argument("--timeout", type=float, default=900)
    query.add_argument("--interval", type=float, default=10)

    return parser


HANDLERS = {
    "upscale": cmd_upscale,
    "remove-object": cmd_remove_object,
    "subtitle": cmd_subtitle,
    "enhance": cmd_enhance,
    "erase": cmd_erase,
    "query": cmd_query,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
