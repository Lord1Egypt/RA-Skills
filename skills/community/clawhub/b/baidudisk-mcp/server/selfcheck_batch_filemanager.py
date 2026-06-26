#!/usr/bin/env python3
"""Minimal self-check for batch filemanager tools (no delete calls)."""

from __future__ import annotations

import json
import os
import tempfile
from typing import Any, Dict, List

import netdisk


class _DummyApiClient:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def __enter__(self) -> "_DummyApiClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class _FakeFilemanagerApi:
    calls: List[Dict[str, Any]] = []

    def __init__(self, _api_client: Any) -> None:
        pass

    def filemanagermove(self, access_token: str, _async: int, filelist: str, ondup: str) -> Dict[str, Any]:
        items = json.loads(filelist)
        self.calls.append({"op": "move", "count": len(items), "ondup": ondup, "async": _async})
        return {"errno": 0, "taskid": f"mv-{len(self.calls)}", "info": [{"ok": len(items)}]}

    def filemanagercopy(self, access_token: str, _async: int, filelist: str, ondup: str) -> Dict[str, Any]:
        items = json.loads(filelist)
        self.calls.append({"op": "copy", "count": len(items), "ondup": ondup, "async": _async})
        return {"errno": 0, "taskid": f"cp-{len(self.calls)}", "info": [{"ok": len(items)}]}

    def filemanagerrename(self, access_token: str, _async: int, filelist: str) -> Dict[str, Any]:
        items = json.loads(filelist)
        self.calls.append({"op": "rename", "count": len(items), "async": _async})
        return {"errno": 0, "taskid": f"rn-{len(self.calls)}", "info": [{"ok": len(items)}]}


def _build_move_copy_items(total: int) -> List[Dict[str, Any]]:
    return [
        {
            "src_path": f"/Openclaw/inbox/file-{i:02d}.txt",
            "dest_dir": "/Openclaw/archive",
        }
        for i in range(total)
    ]


def _build_rename_items(total: int) -> List[Dict[str, Any]]:
    return [
        {
            "path": f"/Openclaw/archive/file-{i:02d}.txt",
            "new_name": f"file-{i:02d}-renamed.txt",
        }
        for i in range(total)
    ]


def run_selfcheck() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        token_file = tf.name
        json.dump({"access_token": "dummy-token", "default_dir": "/Openclaw"}, tf)

    orig_token_env = os.environ.get(netdisk.TOKEN_FILE_ENV)
    orig_api_client = netdisk.openapi_client.ApiClient
    orig_filemanager_api = netdisk.filemanager_api.FilemanagerApi

    try:
        os.environ[netdisk.TOKEN_FILE_ENV] = token_file
        netdisk.openapi_client.ApiClient = _DummyApiClient
        netdisk.filemanager_api.FilemanagerApi = _FakeFilemanagerApi

        move_items = _build_move_copy_items(10)
        copy_items = _build_move_copy_items(2)
        rename_items = _build_rename_items(10)

        move_result = netdisk.file_move_batch(
            items=move_items,
            ondup="fail",
            async_mode=1,
            chunk_size=10,
            dry_run=False,
            allow_dest_prefixes=["/Openclaw"],
        )
        assert move_result["status"] == "success", move_result
        assert move_result["summary"]["ok_items_est"] == 10, move_result

        copy_fail_result = netdisk.file_copy_batch(
            items=copy_items,
            ondup="fail",
            async_mode=1,
            chunk_size=100,
            dry_run=False,
            allow_dest_prefixes=["/Openclaw"],
        )
        assert copy_fail_result["status"] == "success", copy_fail_result

        copy_newcopy_result = netdisk.file_copy_batch(
            items=copy_items,
            ondup="newcopy",
            async_mode=1,
            chunk_size=100,
            dry_run=False,
            allow_dest_prefixes=["/Openclaw"],
        )
        assert copy_newcopy_result["status"] == "success", copy_newcopy_result

        rename_result = netdisk.file_rename_batch(
            items=rename_items,
            async_mode=1,
            chunk_size=100,
            dry_run=False,
        )
        assert rename_result["status"] == "success", rename_result
        assert rename_result["summary"]["ok_items_est"] == 10, rename_result

        print("selfcheck_batch_filemanager: PASS")
        print(
            json.dumps(
                {
                    "move_summary": move_result["summary"],
                    "copy_fail_summary": copy_fail_result["summary"],
                    "copy_newcopy_summary": copy_newcopy_result["summary"],
                    "rename_summary": rename_result["summary"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        netdisk.openapi_client.ApiClient = orig_api_client
        netdisk.filemanager_api.FilemanagerApi = orig_filemanager_api
        if orig_token_env is None:
            os.environ.pop(netdisk.TOKEN_FILE_ENV, None)
        else:
            os.environ[netdisk.TOKEN_FILE_ENV] = orig_token_env
        if os.path.exists(token_file):
            os.remove(token_file)


if __name__ == "__main__":
    run_selfcheck()
