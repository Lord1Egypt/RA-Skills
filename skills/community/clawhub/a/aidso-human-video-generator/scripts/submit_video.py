#!/usr/bin/env python3
"""Submit an AIDSO digital-human video generation task."""

from __future__ import annotations

import argparse
import math
import sys
from typing import Any, Dict

from _aidso import AidsoError, api_base_url, ensure_api_key, json_request, print_json


POINT_BLOCK_SIZE = 42


def count_script_chars(text: str) -> int:
    return len(text.strip())


def estimate_points(text: str, *, preview: bool = False) -> int:
    if preview:
        return 0
    char_count = count_script_chars(text)
    return math.ceil(char_count / POINT_BLOCK_SIZE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an AIDSO digital-human video task.")
    parser.add_argument("--text", help="Final script text to drive the digital-human video.")
    parser.add_argument("--desc", required=True, help="Digital human requirements and generation prompt.")
    parser.add_argument(
        "--subtitle",
        choices=["on", "off"],
        default="on",
        help="Whether to generate subtitles. Defaults to on.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Submit a preview task using the fixed text '测试' instead of the final script.",
    )
    parser.add_argument(
        "--confirm-points",
        type=int,
        help="Required before full generation. Must equal the estimate returned by --estimate-only.",
    )
    parser.add_argument(
        "--estimate-only",
        action="store_true",
        help="Return the estimated points for full generation without submitting.",
    )
    parser.add_argument(
        "--env",
        choices=["prod"],
        default="prod",
        help="AIDSO API environment. Only production is supported.",
    )
    args = parser.parse_args()

    try:
        text = "测试" if args.preview else args.text
        if not text:
            raise AidsoError("Provide --text, or pass --preview to generate a short preview task.")
        script_chars = count_script_chars(text)
        required_points = estimate_points(text, preview=args.preview)
        estimate_payload = {"is_preview": True} if args.preview else {"required_points": required_points}
        if args.estimate_only:
            print_json(estimate_payload)
            return 0
        if not args.preview and args.confirm_points is None:
            print_json(
                {
                    **estimate_payload,
                    "action_required": "Ask the user to confirm the estimated points before submitting.",
                    "next_step": f"Rerun with --confirm-points {required_points} after user confirmation.",
                }
            )
            return 4
        if args.confirm_points is not None and args.confirm_points != required_points:
            raise AidsoError(
                f"Point confirmation mismatch: expected {required_points}, got {args.confirm_points}. "
                "Reconfirm the cost with the user before submitting."
            )
        api_key = ensure_api_key()
        payload: Dict[str, Any] = {
            "text": text,
            "desc": args.desc,
            "subtitle": args.subtitle,
            "aspect_ratio": "Portrait",
        }

        url = f"{api_base_url(args.env)}/openapi/skills/gen_digital_human_video"
        response = json_request("POST", url, api_key=api_key, payload=payload, timeout=120)
        if response.data.get("code") != 200:
            raise AidsoError(f"Video task submission failed: {response.data}")
        task_id = response.data.get("data")
        if not isinstance(task_id, str) or not task_id:
            raise AidsoError(f"Submission succeeded but taskId was missing: {response.data}")
        print_json(
            {
                "taskId": task_id,
                "msg": response.data.get("msg", "success"),
            }
        )
        return 0
    except AidsoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
