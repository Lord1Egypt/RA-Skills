#!/usr/bin/env python3
"""Readonly self-check for 4 official-aligned list capabilities."""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Tuple

import netdisk


def _assert_success(tool: str, result: Dict[str, Any]) -> Dict[str, Any]:
    if result.get("status") != "success":
        raise RuntimeError(f"{tool} 失败: {result.get('message', result)}")
    return result


def _call_video_with_fallback(
    parent_path: str,
    iphone_parent: str,
    openclaw_parent: str,
) -> Tuple[str, Dict[str, Any], List[Dict[str, Any]]]:
    attempts: List[Dict[str, Any]] = []

    candidates: List[str] = []
    for p in [parent_path, iphone_parent, openclaw_parent]:
        p = (p or "").strip() or "/"
        if p not in candidates:
            candidates.append(p)

    chosen_parent = candidates[0]
    chosen_result: Dict[str, Any] = {}

    for idx, parent in enumerate(candidates):
        result = _assert_success(
            "file_video_list_api",
            netdisk.file_video_list_api(
                parent_path=parent,
                recursion=1,
                page=1,
                num=3,
                order="time",
                desc=1,
                web=1,
            ),
        )

        attempts.append(
            {
                "parent_path": parent,
                "count": result.get("count"),
                "source_field": result.get("source_field"),
                "has_more": result.get("has_more"),
            }
        )

        chosen_parent = parent
        chosen_result = result

        count = int(result.get("count") or 0)
        if count > 0:
            break

        # 仅在首选路径为空时继续回退尝试
        if idx == 0 and parent == "/" and len(candidates) > 1:
            continue

        break

    return chosen_parent, chosen_result, attempts


def run_selfcheck() -> None:
    iphone_parent = (
        os.getenv("BAIDU_NETDISK_SELFCHECK_PARENT_IPHONE", "/来自：iPhone") or "/来自：iPhone"
    ).strip() or "/来自：iPhone"
    openclaw_parent = (
        os.getenv("BAIDU_NETDISK_SELFCHECK_PARENT_OPENCLAW", "/Openclaw") or "/Openclaw"
    ).strip() or "/Openclaw"
    video_parent = (os.getenv("BAIDU_NETDISK_SELFCHECK_PARENT_VIDEO", "/") or "/").strip() or "/"

    list_result = _assert_success(
        "file_list",
        netdisk.file_list(dir="/", limit=3, order="name", desc=0, start=0),
    )

    image_result = _assert_success(
        "file_image_list",
        netdisk.file_image_list(
            parent_path=iphone_parent,
            recursion=0,
            page=1,
            num=3,
            order="time",
            desc=1,
            web=1,
        ),
    )

    doc_result = _assert_success(
        "file_doc_list",
        netdisk.file_doc_list(
            parent_path=openclaw_parent,
            recursion=1,
            page=1,
            num=3,
            order="time",
            desc=1,
        ),
    )

    video_parent_used, video_result, video_attempts = _call_video_with_fallback(
        parent_path=video_parent,
        iphone_parent=iphone_parent,
        openclaw_parent=openclaw_parent,
    )

    print("selfcheck_lists_readonly: PASS")
    print(
        json.dumps(
            {
                "file_list": {
                    "dir": "/",
                    "limit": 3,
                    "count": list_result.get("count"),
                    "has_more": list_result.get("has_more"),
                },
                "file_image_list": {
                    "parent_path": iphone_parent,
                    "recursion": 0,
                    "page": 1,
                    "num": 3,
                    "order": "time",
                    "desc": 1,
                    "count": image_result.get("count"),
                    "source_field": image_result.get("source_field"),
                },
                "file_doc_list": {
                    "parent_path": openclaw_parent,
                    "recursion": 1,
                    "page": 1,
                    "num": 3,
                    "order": "time",
                    "desc": 1,
                    "count": doc_result.get("count"),
                    "source_field": doc_result.get("source_field"),
                },
                "file_video_list_api": {
                    "parent_path": video_parent_used,
                    "recursion": 1,
                    "page": 1,
                    "num": 3,
                    "order": "time",
                    "desc": 1,
                    "count": video_result.get("count"),
                    "source_field": video_result.get("source_field"),
                    "attempts": video_attempts,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        run_selfcheck()
    except Exception as exc:
        print(f"selfcheck_lists_readonly: FAIL - {exc}", file=sys.stderr)
        sys.exit(1)
