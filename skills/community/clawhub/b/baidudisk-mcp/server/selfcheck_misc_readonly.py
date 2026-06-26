#!/usr/bin/env python3
"""Minimal self-check for readonly misc tools (category_info + image_gettags)."""

from __future__ import annotations

import json
import os
import tempfile
import urllib.parse
from typing import Any

import netdisk


class _FakeHTTPResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    def read(self) -> bytes:
        return self._raw

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


def _fake_urlopen(req: Any, timeout: int = 30) -> _FakeHTTPResponse:
    ua = req.get_header("User-Agent") or req.get_header("User-agent")
    if ua != "pan.baidu.com":
        raise AssertionError(f"unexpected User-Agent: {ua}")

    parsed = urllib.parse.urlparse(req.full_url)
    query = urllib.parse.parse_qs(parsed.query)

    if parsed.path == "/api/categoryinfo":
        category = int((query.get("category") or ["0"])[0])
        parent_path = (query.get("parent_path") or ["/"])[0]
        recursion = int((query.get("recursion") or ["0"])[0])

        if category == 3:
            # 形态一：info 为扁平 dict
            payload = {
                "errno": 0,
                "info": {
                    "category": category,
                    "parent_path": parent_path,
                    "recursion": recursion,
                    "count": 12,
                    "size": 345678,
                    "total": 12,
                },
            }
            return _FakeHTTPResponse(payload)

        if category == 4:
            # 形态二：info 为按 category key 的 dict
            payload = {
                "errno": 0,
                "info": {
                    "4": {
                        "count": 34,
                        "size": 987654,
                        "total": 34,
                    }
                },
            }
            return _FakeHTTPResponse(payload)

        raise AssertionError(f"unexpected category for selfcheck: {category}")

    if parsed.path == "/rest/2.0/xpan/imageproc":
        method = (query.get("method") or [""])[0]
        key = (query.get("key") or [""])[0]
        tag_type = int((query.get("type") or ["0"])[0])
        if method != "gettags" or key != "tag" or tag_type not in (1, 2):
            raise AssertionError(f"bad gettags query: {query}")

        payload = {
            "errno": 0,
            "list": [
                {
                    "tag_id": 100,
                    "tag_name": "旅行",
                    "count": 8,
                    "is_show": 1,
                    "is_search": 1,
                    "cover_fid": 123456,
                    "thumb": "https://example.com/thumb.jpg",
                    "ctime": 1700000000,
                    "mtime": 1700000100,
                    "status": 1,
                }
            ],
        }
        return _FakeHTTPResponse(payload)

    raise AssertionError(f"unexpected URL: {req.full_url}")


def run_selfcheck() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        token_file = tf.name
        json.dump({"access_token": "dummy-token", "default_dir": "/Openclaw"}, tf)

    orig_token_env = os.environ.get(netdisk.TOKEN_FILE_ENV)
    orig_urlopen = netdisk.urllib.request.urlopen

    try:
        os.environ[netdisk.TOKEN_FILE_ENV] = token_file
        netdisk.urllib.request.urlopen = _fake_urlopen

        category_flat_result = netdisk.category_info(category=3, parent_path="/", recursion=1)
        assert category_flat_result["status"] == "success", category_flat_result
        assert category_flat_result.get("count") == 12, category_flat_result
        assert category_flat_result.get("size") == 345678, category_flat_result
        assert category_flat_result.get("total") == 12, category_flat_result

        category_keyed_result = netdisk.category_info(category=4, parent_path="/", recursion=1)
        assert category_keyed_result["status"] == "success", category_keyed_result
        assert category_keyed_result.get("count") == 34, category_keyed_result
        assert category_keyed_result.get("size") == 987654, category_keyed_result
        assert category_keyed_result.get("total") == 34, category_keyed_result
        raw_info = category_keyed_result.get("raw_info")
        assert isinstance(raw_info, dict) and "4" in raw_info, category_keyed_result

        category_multi_result = netdisk.category_info_multi(
            categories=[3, 4],
            parent_path="/",
            recursion=1,
        )
        assert category_multi_result["status"] == "success", category_multi_result
        by_category = category_multi_result.get("by_category") or {}
        assert by_category.get("3", {}).get("count") == 12, category_multi_result
        assert by_category.get("4", {}).get("count") == 34, category_multi_result

        tag_result = netdisk.image_gettags(type=1)
        assert tag_result["status"] == "success", tag_result

        print("selfcheck_misc_readonly: PASS")
        print(
            json.dumps(
                {
                    "category_flat_count": category_flat_result.get("count"),
                    "category_keyed_count": category_keyed_result.get("count"),
                    "category_multi_count": len(category_multi_result.get("results", []) or []),
                    "tag_type": tag_result.get("type"),
                    "tag_count": tag_result.get("count"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        netdisk.urllib.request.urlopen = orig_urlopen
        if orig_token_env is None:
            os.environ.pop(netdisk.TOKEN_FILE_ENV, None)
        else:
            os.environ[netdisk.TOKEN_FILE_ENV] = orig_token_env
        if os.path.exists(token_file):
            os.remove(token_file)


if __name__ == "__main__":
    run_selfcheck()
