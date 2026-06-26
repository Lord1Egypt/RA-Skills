#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timezone
from typing import List, Dict

import requests

OPEN_API_BASE = "https://open.feishu.cn/open-apis"
DEFAULT_APP_TOKEN = os.getenv("FAMILY_BOOKKEEPING_APP_TOKEN", "")
DEFAULT_TABLE_ID = os.getenv("FAMILY_BOOKKEEPING_TABLE_ID", "")


def clean(v):
    return "" if v is None else str(v).strip()


def fmt_date(v):
    if isinstance(v, (int, float)):
        ts = float(v)
        if ts > 10_000_000_000:
            ts /= 1000.0
        return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime("%Y-%m-%d")
    return clean(v)[:10]


class FeishuClient:
    def __init__(self, app_id: str, app_secret: str, timeout: int = 30):
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self._token = None

    def _tenant_access_token(self):
        if self._token:
            return self._token
        url = f"{OPEN_API_BASE}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={"app_id": self.app_id, "app_secret": self.app_secret}, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(data)
        self._token = data["tenant_access_token"]
        return self._token

    def _headers(self):
        return {"Authorization": f"Bearer {self._tenant_access_token()}", "Content-Type": "application/json; charset=utf-8"}

    def list_records(self, app_token: str, table_id: str, page_size: int = 500) -> List[Dict]:
        out = []
        page_token = None
        while True:
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            url = f"{OPEN_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
            resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise RuntimeError(data)
            payload = data.get("data") or {}
            out.extend(payload.get("items") or [])
            if not payload.get("has_more"):
                break
            page_token = payload.get("page_token")
            if not page_token:
                break
        return out


def sort_key(rec):
    v = (rec.get("fields") or {}).get("日期")
    if isinstance(v, (int, float)):
        return float(v)
    return 0


def main():
    parser = argparse.ArgumentParser(description="List recent bookkeeping records")
    parser.add_argument("--app-token", default=DEFAULT_APP_TOKEN)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if not args.app_id or not args.app_secret:
        raise SystemExit("Need FEISHU_APP_ID / FEISHU_APP_SECRET")
    client = FeishuClient(args.app_id, args.app_secret)
    records = client.list_records(args.app_token, args.table_id)
    records = sorted(records, key=sort_key, reverse=True)[:args.limit]
    out = []
    for r in records:
        f = r.get("fields") or {}
        out.append({
            "record_id": r.get("record_id") or r.get("id"),
            "日期": fmt_date(f.get("日期")),
            "金额": clean(f.get("金额")),
            "一级类型": clean(f.get("一级类型")),
            "二级类型": clean(f.get("二级类型")),
            "备注": clean(f.get("备注")),
            "支付平台": clean(f.get("支付平台")),
            "收支类型": clean(f.get("收支类型")),
            "记账人": clean(f.get("记账人")),
        })
    print(json.dumps({"recent": out}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
