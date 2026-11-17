#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""create_combined_crowd.py - 创建组合人群。凭证自动加载。"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dmp_api_client import DmpClient, ensure_ok
from auth import add_auth_args

CREATE_PATH = "/audience/manage/combine/create"


def load_json_arg(s):
    s = s.strip()
    if s.startswith("[") or s.startswith("{"):
        return json.loads(s)
    with open(s, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    add_auth_args(ap)
    ap.add_argument("--brand-id", nargs="+", default=None, help="可选：品牌ID/名称列表；不传则按默认不传")

    ap.add_argument("--name", required=True)
    ap.add_argument("--track-type", required=True, choices=["MOBILE", "PC", "OTT"])
    ap.add_argument("--id-types", required=True, nargs="+")
    ap.add_argument("--data", required=True, help="data规则：JSON字符串或JSON文件路径")
    args = ap.parse_args()

    data_rules = load_json_arg(args.data)
    if not isinstance(data_rules, list) or len(data_rules) == 0:
        raise SystemExit("data 必须为非空 list")

    # 兼容：若用户/上游给出brandId则透传；未给则按默认不传
    body = {"name": args.name, "trackType": args.track_type, "idTypes": args.id_types, "data": data_rules}
    try:
        if hasattr(args, 'brand_id') and args.brand_id:
            body["brandId"] = args.brand_id
    except Exception:
        pass

    client = DmpClient.from_config(ak=args.ak, sk=args.sk, base_url=args.base_url)
    resp = client.post(CREATE_PATH, body)
    ensure_ok(resp)
    audience_id = (resp.get("data") or {}).get("audienceId")

    print(json.dumps({"ok": True, "audienceId": audience_id, "name": args.name}, ensure_ascii=False))


if __name__ == "__main__":
    main()