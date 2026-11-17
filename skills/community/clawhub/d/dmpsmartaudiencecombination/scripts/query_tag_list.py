#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""query_tag_list.py

拉取明日DMP标签列表（tag/list），并做最小过滤与结构化输出。

凭证自动加载优先级：命令行参数 → 环境变量 → ~/.mingdata_dmp_credentials
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dmp_api_client import DmpClient, ensure_ok
from auth import add_auth_args

TAG_LIST_PATH = "/tag/list"


def normalize_tags(raw_tags):
    out = []
    for t in raw_tags or []:
        out.append({
            "tagId": t.get("tagId"),
            "tagName": t.get("tagName"),
            "parentId": t.get("parentId"),
            "tagType": t.get("tagType"),
            "isDirectory": t.get("isDirectory"),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    add_auth_args(ap)
    # 兼容旧参数：--tag-type（单选）
    ap.add_argument("--tag-type", type=int, choices=[1, 3], default=None, help="1=明略 3=合作伙伴（兼容旧用法，单选）")
    # 新参数：--tag-types（多选，默认同时拉取1+3）
    ap.add_argument("--tag-types", type=int, choices=[1, 3], nargs="+", default=None, help="可多选：1=明略 3=合作伙伴；不填则默认同时拉取1和3")
    ap.add_argument("--only-leaf", action="store_true", help="只保留 isDirectory=1 的可用标签")
    ap.add_argument("--out", required=True, help="输出JSON路径")
    args = ap.parse_args()

    client = DmpClient.from_config(ak=args.ak, sk=args.sk, base_url=args.base_url)

    # 处理tagType输入优先级：tag-types > tag-type > 默认[1,3]
    if args.tag_types:
        tag_types = list(dict.fromkeys(args.tag_types))
    elif args.tag_type is not None:
        tag_types = [args.tag_type]
    else:
        tag_types = [1, 3]

    all_tags = []
    for tt in tag_types:
        params = {"tagType": int(tt)}
        resp = client.get(TAG_LIST_PATH, params=params)
        ensure_ok(resp)
        all_tags.extend(normalize_tags(resp.get("data", [])))

    # 去重：同tagId优先保留（默认按先明略后合作伙伴的顺序）
    dedup = {}
    for t in all_tags:
        tid = t.get("tagId")
        if tid is None:
            continue
        if tid not in dedup:
            dedup[tid] = t

    tags = list(dedup.values())

    if args.only_leaf:
        tags = [t for t in tags if t.get("isDirectory") == 1]

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)

    print(json.dumps({"ok": True, "tagTypes": tag_types, "total": len(tags), "out": args.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
