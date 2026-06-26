#!/usr/bin/env python3
"""Minimal readonly self-check for file_image_list (imagelist)."""

from __future__ import annotations

import json
import os
import sys

import netdisk


def _run_case(parent_path: str, recursion: int, page: int, num: int) -> dict:
    result = netdisk.file_image_list(
        parent_path=parent_path,
        recursion=recursion,
        page=page,
        num=num,
    )
    if result.get("status") != "success":
        raise RuntimeError(
            f"file_image_list 失败: parent_path={parent_path}, "
            f"message={result.get('message', result)}"
        )

    return {
        "parent_path": parent_path,
        "recursion": recursion,
        "page": page,
        "num": num,
        "count": result.get("count"),
        "has_more": result.get("has_more"),
        "source_field": result.get("source_field"),
    }


def run_selfcheck() -> None:
    iphone_parent = (
        os.getenv("BAIDU_NETDISK_SELFCHECK_PARENT_IPHONE", "/来自：iPhone") or "/来自：iPhone"
    ).strip() or "/来自：iPhone"
    openclaw_parent = (
        os.getenv("BAIDU_NETDISK_SELFCHECK_PARENT_OPENCLAW", "/Openclaw") or "/Openclaw"
    ).strip() or "/Openclaw"

    case_iphone = _run_case(parent_path=iphone_parent, recursion=0, page=1, num=3)
    case_openclaw = _run_case(parent_path=openclaw_parent, recursion=1, page=1, num=3)

    print("selfcheck_image_recent_readonly: PASS")
    print(
        json.dumps(
            {
                "cases": [case_iphone, case_openclaw],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        run_selfcheck()
    except Exception as exc:
        print(f"selfcheck_image_recent_readonly: FAIL - {exc}", file=sys.stderr)
        sys.exit(1)
