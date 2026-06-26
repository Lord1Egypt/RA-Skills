#!/usr/bin/env python3
"""Offline self-check: search echo + doclist has_more stability."""

from __future__ import annotations

import json
import os
import tempfile
from typing import Any, Dict

import netdisk


class _DummyApiClient:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def __enter__(self) -> "_DummyApiClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class _FakeFileinfoApi:
    last_search_call: Dict[str, Any] = {}
    last_doclist_call: Dict[str, Any] = {}

    def __init__(self, _api_client: Any) -> None:
        pass

    def xpanfilesearch(self, **kwargs: Any) -> Dict[str, Any]:
        _FakeFileinfoApi.last_search_call = dict(kwargs)
        return {
            "errno": 0,
            "list": [
                {
                    "server_filename": "hit.txt",
                    "path": "/Openclaw/hit.txt",
                    "isdir": 0,
                    "size": 1,
                    "fs_id": 201,
                }
            ],
        }

    def xpanfiledoclist(self, **kwargs: Any) -> Dict[str, Any]:
        _FakeFileinfoApi.last_doclist_call = dict(kwargs)
        parent_path = kwargs.get("parent_path")
        payload: Dict[str, Any] = {
            "errno": 0,
            "info": [
                {
                    "server_filename": "doc-a.md",
                    "path": f"{parent_path}/doc-a.md",
                    "isdir": 0,
                    "size": 1,
                    "fs_id": 202,
                }
            ],
        }
        if parent_path != "/doc-no-flag":
            payload["has_more"] = "1"
        return payload


def run_selfcheck() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        token_file = tf.name
        json.dump({"access_token": "dummy-token", "default_dir": "/Openclaw"}, tf)

    orig_token_env = os.environ.get(netdisk.TOKEN_FILE_ENV)
    orig_api_client = netdisk.openapi_client.ApiClient
    orig_fileinfo_api = netdisk.fileinfo_api.FileinfoApi

    try:
        os.environ[netdisk.TOKEN_FILE_ENV] = token_file
        netdisk.openapi_client.ApiClient = _DummyApiClient
        netdisk.fileinfo_api.FileinfoApi = _FakeFileinfoApi

        search_result = netdisk.search(
            keyword="keyword",
            dir="/Openclaw",
            recursion=1,
            page=9,
            num=11,
        )
        assert search_result["status"] == "success", search_result
        assert search_result.get("page") == 9, search_result
        assert search_result.get("num") == 11, search_result
        assert search_result.get("recursion") == 1, search_result
        assert _FakeFileinfoApi.last_search_call.get("page") == "9", _FakeFileinfoApi.last_search_call
        assert _FakeFileinfoApi.last_search_call.get("num") == "11", _FakeFileinfoApi.last_search_call
        assert _FakeFileinfoApi.last_search_call.get("recursion") == "1", _FakeFileinfoApi.last_search_call

        doc_with_flag = netdisk.file_doc_list(parent_path="/Openclaw", page=3, num=4)
        assert doc_with_flag["status"] == "success", doc_with_flag
        assert doc_with_flag.get("page") == 3, doc_with_flag
        assert doc_with_flag.get("num") == 4, doc_with_flag
        assert doc_with_flag.get("has_more") is True, doc_with_flag

        doc_without_flag = netdisk.file_doc_list(parent_path="/doc-no-flag", page=1, num=2)
        assert doc_without_flag["status"] == "success", doc_without_flag
        assert "has_more" in doc_without_flag, doc_without_flag
        assert doc_without_flag.get("has_more") is False, doc_without_flag

        print("selfcheck_search_doclist_echo: PASS")
        print(
            json.dumps(
                {
                    "search": {
                        "page": search_result.get("page"),
                        "num": search_result.get("num"),
                        "recursion": search_result.get("recursion"),
                    },
                    "doc_with_has_more": doc_with_flag.get("has_more"),
                    "doc_without_has_more": doc_without_flag.get("has_more"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
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
