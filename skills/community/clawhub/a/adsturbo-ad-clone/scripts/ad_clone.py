#!/usr/bin/env python3
"""Ad cloning: study a reference video, then shoot your own version of it.

Quick clone (v1):
  analyze  : break a reference down into a prompt + shot list (clips capped at 12s)
  generate : produce a new video from that prompt
  inspect  : plain shot-by-shot analysis of any video, no generation

Editable clone (v2beta draft flow):
  draft-create  : analyse a reference (<=15s) into an editable draft, wait for it
  draft-get     : read a draft (lines, voices, reference slots, prompt, price)
  draft-preview : apply edits and see the rebuilt prompt + price -- free
  draft-submit  : apply the same edits and generate -- this charges credits
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from shared.client import AdsTurboError, add_async_flags, run_cli, submit_and_maybe_poll

ANALYZE = "/openapi/v1/adclone/analyze"
GENERATE = "/openapi/v1/adclone/generate"
INSPECT = "/openapi/v1/video/analyze"

DRAFT_CREATE = "/openapi/v2beta/adclone/create"
DRAFT_GET = "/openapi/v2beta/adclone/get"
DRAFT_PREVIEW = "/openapi/v2beta/adclone/preview"
DRAFT_SUBMIT = "/openapi/v2beta/adclone/submit"

GENERATE_DURATIONS = [4, 8, 12, 16, 20]
DRAFT_POLL_INTERVAL = 5
DRAFT_POLL_TIMEOUT = 600
DRAFT_DONE = {"completed", "failed", "not_found"}

# Reference image types the draft flow accepts; 4 ("other") is rejected for now.
REF_TYPES = {"product": 1, "person": 2, "scene": 3}


def cmd_analyze(client, args) -> dict:
    """Synchronous -- returns the prompt to feed into `generate`."""
    return client.post(ANALYZE, {
        "video_url": args.video_url,
        "clip_start": args.clip_start,
        "clip_end": args.clip_end,
    })


def cmd_generate(client, args) -> dict:
    return submit_and_maybe_poll(client, GENERATE, {
        "prompt": args.prompt,
        "video_url": args.video_url,
        "duration": args.duration,
        "ratio": args.ratio,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_inspect(client, args) -> dict:
    return submit_and_maybe_poll(client, INSPECT, {
        "video_url": args.video_url,
        "workspace_id": args.workspace_id,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_query(client, args) -> dict:
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


# ---------- v2beta draft flow ----------

def wait_for_draft(client, clone_id: str, timeout: float, interval: float) -> dict:
    """Poll `get` until the draft leaves `processing`."""
    started = time.time()
    while True:
        result = client.post(DRAFT_GET, {"clone_id": clone_id})
        status = result.get("status", "")
        if status == "failed":
            raise AdsTurboError(-1, result.get("message") or "draft analysis failed")
        if status in DRAFT_DONE:
            return result
        elapsed = time.time() - started
        if elapsed > timeout:
            raise TimeoutError(
                f"Draft still processing after {timeout:.0f}s. It is not lost -- "
                f"resume with: draft-get --clone-id {clone_id}"
            )
        stage = result.get("stage") or "processing"
        print(f"  {stage} {result.get('progress', 0)}% ... {elapsed:.0f}s elapsed", file=sys.stderr)
        time.sleep(interval)


def cmd_draft_create(client, args) -> dict:
    receipt = client.post(DRAFT_CREATE, {
        "video_url": args.video_url,
        "clip_start": args.clip_start,
        "clip_end": args.clip_end,
        "lang": args.lang,
        "idempotency_key": args.idempotency_key,
    })
    clone_id = receipt.get("clone_id", "")
    if args.no_wait or not clone_id:
        return receipt
    print(f"  draft created, clone_id={clone_id}", file=sys.stderr)
    return wait_for_draft(client, clone_id, args.timeout, args.interval)


def cmd_draft_get(client, args) -> dict:
    if args.wait:
        return wait_for_draft(client, args.clone_id, args.timeout, args.interval)
    return client.post(DRAFT_GET, {"clone_id": args.clone_id})


def parse_ref(spec: str) -> dict:
    """`TYPE[@SLOT_ID]=IMAGE_URL`, e.g. `person@subject_1=https://.../me.jpg`."""
    head, sep, image_url = spec.partition("=")
    if not sep or not image_url:
        raise AdsTurboError(-1, f"--ref must look like TYPE[@SLOT_ID]=IMAGE_URL, got {spec!r}")
    ref_type, _, slot_id = head.partition("@")
    type_code = REF_TYPES.get(ref_type.strip().lower())
    if type_code is None and ref_type.strip().isdigit():
        type_code = int(ref_type)
    if type_code not in REF_TYPES.values():
        raise AdsTurboError(-1, f"--ref type must be product, person or scene, got {ref_type!r}")
    return {"type": type_code, "slot_id": slot_id.strip(), "image_url": image_url.strip()}


def parse_line(spec: str) -> dict:
    """`LINE_ID=NEW TEXT`; an empty text mutes that line."""
    line_id, sep, text = spec.partition("=")
    if not sep or not line_id.strip():
        raise AdsTurboError(-1, f"--line must look like LINE_ID=NEW_TEXT, got {spec!r}")
    return {"id": line_id.strip(), "text": text}


def load_edits_json(raw: str) -> dict:
    """Inline JSON, or @path to a JSON file."""
    try:
        text = Path(raw[1:]).expanduser().read_text(encoding="utf-8") if raw.startswith("@") else raw
        edits = json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise AdsTurboError(-1, f"--edits-json is not valid JSON: {exc}") from exc
    if not isinstance(edits, dict):
        raise AdsTurboError(-1, "--edits-json must be a JSON object")
    return edits


def build_edits(args) -> dict:
    """Merge --edits-json with the convenience flags; flags win on conflict."""
    edits = load_edits_json(args.edits_json) if args.edits_json else {}
    if args.line:
        edits["lines"] = [parse_line(spec) for spec in args.line]
    if args.ref:
        edits["references"] = [
            {key: value for key, value in parse_ref(spec).items() if value}
            for spec in args.ref
        ]
    if args.prompt:
        edits["prompt"] = args.prompt
    return edits


def build_video(args) -> dict:
    video = {
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "duration": args.duration,
        "quantity": args.quantity,
    }
    return {key: value for key, value in video.items() if value}


def cmd_draft_preview(client, args) -> dict:
    return client.post(DRAFT_PREVIEW, {
        "clone_id": args.clone_id,
        "edits": build_edits(args) or None,
        "video": build_video(args) or None,
    })


def cmd_draft_submit(client, args) -> dict:
    receipt = client.post(DRAFT_SUBMIT, {
        "clone_id": args.clone_id,
        "edits": build_edits(args) or None,
        "video": build_video(args) or None,
        "callback_id": args.callback_id,
        "idempotency_key": args.idempotency_key,
    })
    workspace_ids = receipt.get("workspace_ids") or [receipt.get("workspace_id", "")]
    workspace_ids = [workspace_id for workspace_id in workspace_ids if workspace_id]
    if args.no_wait or not workspace_ids:
        return receipt
    print(f"  submitted, workspace_ids={workspace_ids}", file=sys.stderr)
    results = [
        client.poll(workspace_id, timeout=args.timeout, interval=args.interval)
        for workspace_id in workspace_ids
    ]
    return results[0] if len(results) == 1 else {"workspace_ids": workspace_ids, "results": results}


def add_edit_flags(sub) -> None:
    """Flags `draft-preview` and `draft-submit` share; send the same ones to both."""
    sub.add_argument("--clone-id", required=True)
    sub.add_argument("--line", action="append", default=[], metavar="LINE_ID=TEXT",
                     help="rewrite one line of dialogue; repeatable; empty text mutes the line")
    sub.add_argument("--ref", action="append", default=[], metavar="TYPE[@SLOT_ID]=IMAGE_URL",
                     help="reference image (product|person|scene); repeatable; this is the final set")
    sub.add_argument("--prompt", default="", help="override the whole prompt")
    sub.add_argument("--edits-json", default="", help="full `edits` object as JSON, or @file.json")
    sub.add_argument("--aspect-ratio", default="", help="see draft.gen_options; empty = default")
    sub.add_argument("--resolution", default="", help="see draft.gen_options; empty = default")
    sub.add_argument("--duration", type=int, default=0, help="4-15 seconds; 0 = source length")
    sub.add_argument("--quantity", type=int, default=0, help="videos to generate, 1-4")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo ad cloning")
    sub = parser.add_subparsers(dest="command")

    ana = sub.add_parser("analyze", help="turn a reference video into a prompt")
    ana.add_argument("--video-url", required=True)
    ana.add_argument("--clip-start", type=int, help="seconds; trim before analysing")
    ana.add_argument("--clip-end", type=int)

    gen = sub.add_parser("generate", help="shoot a new video from an analysed prompt")
    gen.add_argument("--prompt", required=True, help="usually the output of `analyze`")
    gen.add_argument("--video-url", default="", help="the reference, for style anchoring")
    gen.add_argument("--duration", type=int, choices=GENERATE_DURATIONS,
                     help="seconds; server default 12")
    gen.add_argument("--ratio", default="", help="aspect ratio; server default 9:16")
    gen.add_argument("--idempotency-key", default="")
    add_async_flags(gen)

    ins = sub.add_parser("inspect", help="shot-by-shot analysis, no generation")
    ins.add_argument("--video-url", default="")
    ins.add_argument("--workspace-id", default="")
    ins.add_argument("--idempotency-key", default="")
    add_async_flags(ins)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    query.add_argument("--timeout", type=float, default=900)
    query.add_argument("--interval", type=float, default=10)

    create = sub.add_parser("draft-create", help="analyse a reference (<=15s) into an editable draft")
    create.add_argument("--video-url", required=True)
    create.add_argument("--clip-start", type=float, help="seconds; both unset = whole video")
    create.add_argument("--clip-end", type=float)
    create.add_argument("--lang", default="", help="prompt language; default en, dialogue stays original")
    create.add_argument("--idempotency-key", default="")
    create.add_argument("--no-wait", action="store_true", help="return the clone_id without waiting")
    create.add_argument("--timeout", type=float, default=DRAFT_POLL_TIMEOUT)
    create.add_argument("--interval", type=float, default=DRAFT_POLL_INTERVAL)

    get = sub.add_parser("draft-get", help="read a draft")
    get.add_argument("--clone-id", required=True)
    get.add_argument("--wait", action="store_true", help="keep polling while it is processing")
    get.add_argument("--timeout", type=float, default=DRAFT_POLL_TIMEOUT)
    get.add_argument("--interval", type=float, default=DRAFT_POLL_INTERVAL)

    preview = sub.add_parser("draft-preview", help="rebuild prompt + price from edits, no charge")
    add_edit_flags(preview)

    submit = sub.add_parser("draft-submit", help="generate from the draft -- charges credits")
    add_edit_flags(submit)
    submit.add_argument("--idempotency-key", default="")
    add_async_flags(submit)

    return parser


HANDLERS = {
    "analyze": cmd_analyze,
    "generate": cmd_generate,
    "inspect": cmd_inspect,
    "query": cmd_query,
    "draft-create": cmd_draft_create,
    "draft-get": cmd_draft_get,
    "draft-preview": cmd_draft_preview,
    "draft-submit": cmd_draft_submit,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
