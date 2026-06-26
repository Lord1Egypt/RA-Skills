#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List, Optional

import requests

OPEN_API_BASE = "https://open.feishu.cn/open-apis"
DEFAULT_APP_TOKEN = os.getenv("FAMILY_BOOKKEEPING_APP_TOKEN", "")
DEFAULT_TABLE_ID = os.getenv("FAMILY_BOOKKEEPING_TABLE_ID", "")


def clean(v):
    return "" if v is None else str(v).strip()


def date_str(v):
    if isinstance(v, (int, float)):
        ts = float(v)
        if ts > 10_000_000_000:
            ts /= 1000.0
        return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime("%Y-%m-%d")
    return clean(v)[:10]


def date_ms(text: str):
    if not text:
        return None
    t = text.replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return int(datetime.strptime(t[:19], fmt).timestamp() * 1000)
        except Exception:
            pass
    return None


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

    def update_record(self, app_token: str, table_id: str, record_id: str, fields: Dict):
        url = f"{OPEN_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        resp = requests.put(url, headers=self._headers(), json={"fields": fields}, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(data)
        return data


def normalize_amount_text(v: str) -> str:
    t = clean(v).replace(',', '')
    if not t:
        return ''
    try:
        d = Decimal(t)
        s = format(d.normalize(), 'f')
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s
    except Exception:
        return t


def record_matches(fields: Dict, note_keyword: str, on_date: str, amount: str):
    if note_keyword and note_keyword not in clean(fields.get("备注")):
        return False
    if on_date and date_str(fields.get("日期")) != on_date:
        return False
    if amount and normalize_amount_text(fields.get("金额")) != normalize_amount_text(amount):
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Update one bookkeeping record (MVP)")
    parser.add_argument("--app-token", default=DEFAULT_APP_TOKEN)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    parser.add_argument("--note-keyword", default="")
    parser.add_argument("--on-date", default="")
    parser.add_argument("--amount", default="")
    parser.add_argument("--set-amount", default="")
    parser.add_argument("--set-note", default="")
    parser.add_argument("--set-cat1", default="")
    parser.add_argument("--set-cat2", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        raise SystemExit("Need FEISHU_APP_ID / FEISHU_APP_SECRET")

    client = FeishuClient(args.app_id, args.app_secret)
    records = client.list_records(args.app_token, args.table_id)
    matches = [r for r in records if record_matches(r.get("fields") or {}, args.note_keyword, args.on_date, args.amount)]

    if not matches:
        raise SystemExit("No matching record found")
    if len(matches) > 1:
        preview = []
        for r in matches[:10]:
            f = r.get("fields") or {}
            preview.append({
                "record_id": r.get("record_id") or r.get("id"),
                "日期": date_str(f.get("日期")),
                "金额": clean(f.get("金额")),
                "备注": clean(f.get("备注")),
            })
        print(json.dumps({"multiple_matches": preview}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    target = matches[0]
    target_id = target.get("record_id") or target.get("id")
    patch = {}
    if args.set_amount:
        patch["金额"] = float(Decimal(args.set_amount))
    if args.set_note:
        patch["备注"] = args.set_note
    if args.set_cat1:
        patch["一级类型"] = args.set_cat1
    if args.set_cat2:
        patch["二级类型"] = args.set_cat2

    if args.dry_run:
        print(json.dumps({"record_id": target_id, "patch": patch}, ensure_ascii=False, indent=2))
        return

    result = client.update_record(args.app_token, args.table_id, target_id, patch)
    print(json.dumps({"updated": True, "record_id": target_id, "patch": patch, "result": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
