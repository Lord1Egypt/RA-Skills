#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""query_crowd_task.py - 查询人群任务状态。凭证自动加载。"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent))
from dmp_api_client import DmpClient, ensure_ok
from auth import add_auth_args

TASK_LIST_PATH = "/audience/manage/taskList"


def main():
    ap = argparse.ArgumentParser()
    add_auth_args(ap)
    ap.add_argument("--audience-ids", required=True, nargs="+")
    args = ap.parse_args()

    ids: List[int] = []
    for x in args.audience_ids:
        try:
            ids.append(int(str(x).strip()))
        except (ValueError, TypeError):
            raise SystemExit(f"非法 audienceId: {x}")

    client = DmpClient.from_config(ak=args.ak, sk=args.sk, base_url=args.base_url)
    resp = client.post(TASK_LIST_PATH, {"audienceIds": ids})
    ensure_ok(resp)

    out = []
    status_map = {0: "失败", 1: "成功", 2: "等待中", 3: "计算中"}
    for item in resp.get("data", []) or []:
        st = item.get("audienceStatus")
        out.append({
            "audienceId": item.get("audienceId"),
            "audienceName": item.get("audienceName"),
            "audienceStatus": st,
            "audienceStatusText": status_map.get(st, f"未知({st})"),
            "audienceAmount": item.get("audienceAmount") if st == 1 else None,
            "createTime": item.get("createTime"),
            "taskLog": item.get("taskLog") if st == 0 else None,
        })
    print(json.dumps({"ok": True, "data": out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
