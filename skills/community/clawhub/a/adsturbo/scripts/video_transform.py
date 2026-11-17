#!/usr/bin/env python3
"""Video transformation: same footage, something inside it swapped out.

character-swap : replace the person on screen with another
motion-control : drive a still portrait with the motion of a reference video
translate      : re-voice the video in another language
"""

from __future__ import annotations

import argparse

from shared.client import add_async_flags, run_cli, submit_and_maybe_poll

CHARACTER_SWAP = "/openapi/v1/video/character-swap"
MOTION_CONTROL = "/openapi/v1/video/motion-control"
TRANSLATE = "/openapi/v1/video/translate"


def cmd_character_swap(client, args) -> dict:
    return submit_and_maybe_poll(client, CHARACTER_SWAP, {
        "video_url": args.video_url,
        "image_url": args.image_url,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_motion_control(client, args) -> dict:
    return submit_and_maybe_poll(client, MOTION_CONTROL, {
        "video_url": args.video_url,
        "image_url": args.image_url,
        "prompt": args.prompt,
        "negative_prompt": args.negative_prompt,
        "mode": args.mode,
        "character_orientation": args.character_orientation,
        "keep_original_sound": args.keep_original_sound,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_translate(client, args) -> dict:
    return submit_and_maybe_poll(client, TRANSLATE, {
        "video_url": args.video_url,
        "target_lang": args.target_lang,
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
    parser = argparse.ArgumentParser(description="AdsTurbo video transformation")
    sub = parser.add_subparsers(dest="command")

    swap = sub.add_parser("character-swap", help="replace the person on screen")
    _add_source_flags(swap)
    swap.add_argument("--image-url", required=True, help="portrait of the new character")
    add_async_flags(swap)

    motion = sub.add_parser("motion-control", help="drive a portrait with reference motion")
    _add_source_flags(motion)
    motion.add_argument("--image-url", required=True, help="the portrait to animate")
    motion.add_argument("--prompt", default="")
    motion.add_argument("--negative-prompt", default="")
    motion.add_argument("--mode", default="")
    motion.add_argument("--character-orientation", default="")
    motion.add_argument("--keep-original-sound", action="store_true")
    add_async_flags(motion)

    tr = sub.add_parser("translate", help="re-voice the video in another language")
    _add_source_flags(tr)
    tr.add_argument("--target-lang", required=True, help="e.g. en / ja / es")
    add_async_flags(tr)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    query.add_argument("--timeout", type=float, default=900)
    query.add_argument("--interval", type=float, default=10)

    return parser


HANDLERS = {
    "character-swap": cmd_character_swap,
    "motion-control": cmd_motion_control,
    "translate": cmd_translate,
    "query": cmd_query,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
