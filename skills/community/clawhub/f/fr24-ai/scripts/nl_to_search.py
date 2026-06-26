#!/usr/bin/env python3
"""自然语言 -> 待确认搜索 payload。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from output_export import failure_envelope, parse_user_view, wrap_envelope  # noqa: E402
from query_parser import _format_summary, build_payload_from_intent, parse_simple_text  # noqa: E402
from search_refinement import apply_refinement  # noqa: E402

_ROOT = Path(__file__).resolve().parent.parent
PENDING = _ROOT / ".cache" / "pending_search.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["parse", "build", "refine"])
    parser.add_argument("--text", default="")
    parser.add_argument("--intent-file", default="")
    parser.add_argument(
        "--payload-file",
        default=str(PENDING),
        help="refine 时读取的上次搜索条件（默认 .cache/pending_search.json）",
    )
    args = parser.parse_args()

    if args.command == "refine":
        pending_path = Path(args.payload_file)
        if not pending_path.is_file():
            print(
                json.dumps(
                    failure_envelope("refine", "未找到上次搜索条件，请先完成行程解析与搜索。"),
                    ensure_ascii=False,
                    indent=2,
                )
            )
            sys.exit(1)
        base = json.loads(pending_path.read_text(encoding="utf-8"))
        payload, note, err = apply_refinement(base, args.text)
        if err:
            print(json.dumps(failure_envelope("refine", err), ensure_ascii=False, indent=2))
            sys.exit(1)
        trip = "RT" if len(payload.get("searchLegs") or []) >= 2 else "OW"
        summary = _format_summary(payload, trip, payload.get("preferences", {}).get("stops") == 0)
        action = "refine"
        user_message = (
            f"已更新搜索条件：{note}。将为您重新搜索（消耗 1 次演示配额）。"
            if note
            else "已更新搜索条件，将为您重新搜索。"
        )
    elif args.command == "parse":
        payload, summary, err = parse_simple_text(args.text)
        action = "parse"
        user_message = "解析成功，请确认下方行程；确认后将为您搜索航班。"
    else:
        intent = json.loads(Path(args.intent_file).read_text(encoding="utf-8"))
        payload, summary, err = build_payload_from_intent(intent)
        action = "parse"
        user_message = "解析成功，请确认下方行程；确认后将为您搜索航班。"

    if err:
        print(json.dumps(failure_envelope(action, err), ensure_ascii=False, indent=2))
        sys.exit(1)

    PENDING.parent.mkdir(parents=True, exist_ok=True)
    PENDING.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    user_view = parse_user_view(summary, payload)
    out = wrap_envelope(
        action=action,
        status="success",
        user_view=user_view,
        agent_only={"payload": payload, "payloadFile": str(PENDING)},
        message=user_message,
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
