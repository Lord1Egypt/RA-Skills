#!/usr/bin/env python3
"""Offline self-check: retry(31034), pagination echo, path '..' guard."""

from __future__ import annotations

import json
import os
import tempfile
import urllib.parse
from typing import Any, Dict, List

import netdisk


class _FakeHTTPResponse:
    def __init__(self, payload: Dict[str, Any]) -> None:
        self._raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    def read(self) -> bytes:
        return self._raw

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class _DummyApiClient:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def __enter__(self) -> "_DummyApiClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class _FakeFileinfoApi:
    last_list_call: Dict[str, Any] = {}
    last_search_call: Dict[str, Any] = {}
    last_doclist_call: Dict[str, Any] = {}

    def __init__(self, _api_client: Any) -> None:
        pass

    def xpanfilelist(self, **kwargs: Any) -> Dict[str, Any]:
        _FakeFileinfoApi.last_list_call = dict(kwargs)
        return {
            "errno": 0,
            "has_more": 1,
            "list": [
                {
                    "server_filename": "a.txt",
                    "path": "/a.txt",
                    "isdir": 0,
                    "size": 1,
                    "fs_id": 100,
                }
            ],
        }

    def xpanfilesearch(self, **kwargs: Any) -> Dict[str, Any]:
        _FakeFileinfoApi.last_search_call = dict(kwargs)
        return {
            "errno": 0,
            "list": [
                {
                    "server_filename": "search-hit.txt",
                    "path": "/Openclaw/search-hit.txt",
                    "isdir": 0,
                    "size": 2,
                    "fs_id": 101,
                }
            ],
        }

    def xpanfiledoclist(self, **kwargs: Any) -> Dict[str, Any]:
        _FakeFileinfoApi.last_doclist_call = dict(kwargs)
        parent_path = kwargs.get("parent_path")
        payload = {
            "errno": 0,
            "info": [
                {
                    "server_filename": "doc.md",
                    "path": f"{parent_path}/doc.md",
                    "isdir": 0,
                    "size": 3,
                    "fs_id": 102,
                }
            ],
        }
        if parent_path != "/without-has-more":
            payload["has_more"] = 1
        return payload


def run_selfcheck() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        token_file = tf.name
        json.dump({"access_token": "dummy-token", "default_dir": "/Openclaw"}, tf)

    counters = {
        "search_retry_ok": 0,
        "search_retry_fail": 0,
        "recent_list": 0,
    }
    sleep_calls: List[float] = []

    def _fake_sleep(seconds: float) -> None:
        sleep_calls.append(float(seconds))

    def _fake_urlopen(req: Any, timeout: int = 30) -> _FakeHTTPResponse:
        parsed = urllib.parse.urlparse(req.full_url)
        query = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/rest/2.0/xpan/imageproc":
            method = (query.get("method") or [""])[0]
            if method == "search":
                keyword = (query.get("keyword") or [""])[0]
                if keyword == "retry-ok":
                    counters["search_retry_ok"] += 1
                    if counters["search_retry_ok"] < 3:
                        return _FakeHTTPResponse(
                            {
                                "errno": 31034,
                                "errmsg": "hit rate limit",
                                "suggested_backoff_s": 0.01,
                            }
                        )
                    return _FakeHTTPResponse({"errno": 0, "list": [], "has_more": 0})

                if keyword == "retry-fail":
                    counters["search_retry_fail"] += 1
                    return _FakeHTTPResponse(
                        {
                            "errno": 31034,
                            "errmsg": "still rate limited",
                            "suggested_backoff_s": 0.02,
                        }
                    )

                raise AssertionError(f"unexpected keyword for search selfcheck: {keyword}")

            raise AssertionError(f"unexpected imageproc method: {method}")

        if parsed.path == "/rest/2.0/xpan/multimedia":
            method = (query.get("method") or [""])[0]
            if method != "recentlist":
                raise AssertionError(f"unexpected multimedia method: {method}")

            counters["recent_list"] += 1
            return _FakeHTTPResponse(
                {
                    "errno": 0,
                    "cursor": "cursor-123",
                    "has_more": 1,
                    "list": [{"path": "/x.jpg", "fs_id": 1}],
                }
            )

        raise AssertionError(f"unexpected URL in selfcheck: {req.full_url}")

    orig_token_env = os.environ.get(netdisk.TOKEN_FILE_ENV)
    orig_urlopen = netdisk.urllib.request.urlopen
    orig_sleep = netdisk.time.sleep
    orig_api_client = netdisk.openapi_client.ApiClient
    orig_fileinfo_api = netdisk.fileinfo_api.FileinfoApi

    try:
        os.environ[netdisk.TOKEN_FILE_ENV] = token_file
        netdisk.urllib.request.urlopen = _fake_urlopen
        netdisk.time.sleep = _fake_sleep
        netdisk.openapi_client.ApiClient = _DummyApiClient
        netdisk.fileinfo_api.FileinfoApi = _FakeFileinfoApi

        # 1) errno=31034 触发重试并最终成功
        retry_ok = netdisk.image_search(search_type=2, keyword="retry-ok", start=11, limit=13)
        assert retry_ok["status"] == "success", retry_ok
        assert counters["search_retry_ok"] == 3, counters
        assert retry_ok.get("start") == 11 and retry_ok.get("limit") == 13, retry_ok

        # 2) errno=31034 重试耗尽后，error envelope 带 retryable/backoff
        retry_fail = netdisk.image_search(search_type=2, keyword="retry-fail", start=0, limit=3)
        assert retry_fail["status"] == "error", retry_fail
        assert counters["search_retry_fail"] == 3, counters
        assert retry_fail.get("retryable") is True, retry_fail
        assert float(retry_fail.get("suggested_backoff_s") or 0) > 0, retry_fail

        # 3) 分页参数回显（recent_list / file_list）
        recent = netdisk.recent_list(category=3, start=17, limit=19, resolution="off")
        assert recent["status"] == "success", recent
        assert recent.get("start") == 17 and recent.get("limit") == 19, recent
        assert recent.get("cursor") == "cursor-123", recent

        file_list_result = netdisk.file_list(dir="/", start=5, limit=7, order="name", desc=0)
        assert file_list_result["status"] == "success", file_list_result
        assert file_list_result.get("start") == 5 and file_list_result.get("limit") == 7, file_list_result
        assert _FakeFileinfoApi.last_list_call.get("start") == "5", _FakeFileinfoApi.last_list_call
        assert int(_FakeFileinfoApi.last_list_call.get("limit") or 0) == 7, _FakeFileinfoApi.last_list_call

        # 4) search 回显 page/num/recursion
        search_result = netdisk.search(
            keyword="demo",
            dir="/Openclaw",
            recursion=0,
            page=3,
            num=4,
        )
        assert search_result["status"] == "success", search_result
        assert search_result.get("page") == 3, search_result
        assert search_result.get("num") == 4, search_result
        assert search_result.get("recursion") == 0, search_result
        assert _FakeFileinfoApi.last_search_call.get("page") == "3", _FakeFileinfoApi.last_search_call
        assert _FakeFileinfoApi.last_search_call.get("num") == "4", _FakeFileinfoApi.last_search_call
        assert _FakeFileinfoApi.last_search_call.get("recursion") == "0", _FakeFileinfoApi.last_search_call

        # 5) file_doc_list 回显 has_more（有值时为 bool，缺失时稳定为 False）
        doclist_with_has_more = netdisk.file_doc_list(parent_path="/Openclaw", page=2, num=5)
        assert doclist_with_has_more["status"] == "success", doclist_with_has_more
        assert doclist_with_has_more.get("page") == 2, doclist_with_has_more
        assert doclist_with_has_more.get("num") == 5, doclist_with_has_more
        assert doclist_with_has_more.get("has_more") is True, doclist_with_has_more

        doclist_without_has_more = netdisk.file_doc_list(parent_path="/without-has-more", page=1, num=2)
        assert doclist_without_has_more["status"] == "success", doclist_without_has_more
        assert "has_more" in doclist_without_has_more, doclist_without_has_more
        assert doclist_without_has_more.get("has_more") is False, doclist_without_has_more

        # 6) 路径归一化显式拒绝 '..' 路径段
        for bad in ("..", "../x", "/..", "/a/../b"):
            try:
                netdisk._normalize_dir(bad)
                raise AssertionError(f"_normalize_dir should reject: {bad}")
            except ValueError:
                pass

        try:
            netdisk._join_path("/Openclaw", "../escape")
            raise AssertionError("_join_path should reject parent traversal")
        except ValueError:
            pass

        print("selfcheck_retry_pagination_path: PASS")
        print(
            json.dumps(
                {
                    "retry_ok_attempts": counters["search_retry_ok"],
                    "retry_fail_attempts": counters["search_retry_fail"],
                    "recent_calls": counters["recent_list"],
                    "sleep_calls": sleep_calls,
                    "file_list_start": file_list_result.get("start"),
                    "file_list_limit": file_list_result.get("limit"),
                    "search_page": search_result.get("page"),
                    "search_num": search_result.get("num"),
                    "search_recursion": search_result.get("recursion"),
                    "doclist_has_more_present": doclist_with_has_more.get("has_more"),
                    "doclist_has_more_missing": doclist_without_has_more.get("has_more"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        netdisk.urllib.request.urlopen = orig_urlopen
        netdisk.time.sleep = orig_sleep
        netdisk.openapi_client.ApiClient = orig_api_client
        netdisk.fileinfo_api.FileinfoApi = orig_fileinfo_api
        if orig_token_env is None:
            os.environ.pop(netdisk.TOKEN_FILE_ENV, None)
        else:
            os.environ[netdisk.TOKEN_FILE_ENV] = orig_token_env
        if os.path.exists(token_file):
            os.remove(token_file)


if __name__ == "__main__":
    run_selfcheck()
