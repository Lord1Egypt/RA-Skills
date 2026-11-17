#!/usr/bin/env python3
"""Video generation: make footage that does not exist yet.

generate : text/image/first-last-frame/multi-reference -> new clip
extend   : continue an existing clip (seedance-2.0 only)
edit     : change a region of an existing clip (seedance-2.0 only)
"""

from __future__ import annotations

import argparse

from shared.client import add_async_flags, run_cli, submit_and_maybe_poll

GENERATE = "/openapi/v1/video/generate"
EXTEND = "/openapi/v1/video/extend"
EDIT = "/openapi/v1/video/edit"


def cmd_generate(client, args) -> dict:
    return submit_and_maybe_poll(client, GENERATE, {
        "prompt": args.prompt,
        "model": args.model,
        "ratio": args.ratio,
        "resolution": args.resolution,
        "duration": args.duration,
        "start_frame": args.start_frame,
        "end_frame": args.end_frame,
        "reference_images": args.reference_images,
        "reference_videos": args.reference_videos,
        "reference_audios": args.reference_audios,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_extend(client, args) -> dict:
    return submit_and_maybe_poll(client, EXTEND, {
        "video_url": args.video_url,
        "workspace_id": args.workspace_id,
        "prompt": args.prompt,
        "model": args.model,
        "ratio": args.ratio,
        "resolution": args.resolution,
        "duration": args.duration,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_edit(client, args) -> dict:
    return submit_and_maybe_poll(client, EDIT, {
        "video_url": args.video_url,
        "workspace_id": args.workspace_id,
        "prompt": args.prompt,
        "mask_url": args.mask_url,
        "reference_images": args.reference_images,
        "model": args.model,
        "ratio": args.ratio,
        "resolution": args.resolution,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_query(client, args) -> dict:
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


def _add_model_flags(sub) -> None:
    """duration / ratio / resolution accept different values per model -- see the reference doc."""
    sub.add_argument("--model", default="")
    sub.add_argument("--ratio", default="")
    sub.add_argument("--resolution", default="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo video generation")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="create a video from text and/or references")
    gen.add_argument("--prompt", required=True)
    gen.add_argument("--duration", type=int)
    gen.add_argument("--start-frame", default="", help="image url of the first frame")
    gen.add_argument("--end-frame", default="", help="image url of the last frame")
    gen.add_argument("--reference-images", nargs="*", default=[])
    gen.add_argument("--reference-videos", nargs="*", default=[])
    gen.add_argument("--reference-audios", nargs="*", default=[])
    gen.add_argument("--idempotency-key", default="")
    _add_model_flags(gen)
    add_async_flags(gen)

    ext = sub.add_parser("extend", help="continue an existing video")
    ext.add_argument("--video-url", default="")
    ext.add_argument("--workspace-id", default="", help="extend a previous result instead")
    ext.add_argument("--prompt", default="")
    ext.add_argument("--duration", type=int)
    ext.add_argument("--idempotency-key", default="")
    _add_model_flags(ext)
    add_async_flags(ext)

    edit = sub.add_parser("edit", help="edit a region of an existing video")
    edit.add_argument("--video-url", default="")
    edit.add_argument("--workspace-id", default="")
    edit.add_argument("--prompt", required=True)
    edit.add_argument("--mask-url", default="", help="white = area to change")
    edit.add_argument("--reference-images", nargs="*", default=[])
    edit.add_argument("--idempotency-key", default="")
    _add_model_flags(edit)
    add_async_flags(edit)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    query.add_argument("--timeout", type=float, default=900)
    query.add_argument("--interval", type=float, default=10)

    return parser


HANDLERS = {
    "generate": cmd_generate,
    "extend": cmd_extend,
    "edit": cmd_edit,
    "query": cmd_query,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
