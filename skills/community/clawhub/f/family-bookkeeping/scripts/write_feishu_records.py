#!/usr/bin/env python3
import argparse
import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests

OPEN_API_BASE = "https://open.feishu.cn/open-apis"
DEFAULT_APP_TOKEN = os.getenv("FAMILY_BOOKKEEPING_APP_TOKEN", "")
DEFAULT_TABLE_ID = os.getenv("FAMILY_BOOKKEEPING_TABLE_ID", "")


def clean(v):
    return "" if v is None else str(v).strip()


def normalize_date_to_ms(value: str) -> Optional[int]:
    text = clean(value)
    if not text:
        return None
    text = text.replace("/", "-")
    candidates = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
    for fmt in candidates:
        try:
            dt = datetime.strptime(text[:19], fmt)
            return int(dt.timestamp() * 1000)
        except Exception:
            pass
    return None


def normalize_number(value: str):
    text = clean(value).replace(",", "").replace("¥", "").replace("￥", "")
    if not text:
        return None
    try:
        return float(text)
    except Exception:
        return None


def primary_title(row: Dict[str, str]) -> str:
    date = clean(row.get("日期"))[:10]
    direction = clean(row.get("收支类型")) or "交易"
    amount = clean(row.get("金额"))
    note = clean(row.get("备注"))
    category = "/".join([x for x in [clean(row.get("一级类型")), clean(row.get("二级类型"))] if x])
    tail = note or category or clean(row.get("支付平台")) or "账目"
    if len(tail) > 30:
        tail = tail[:30] + "…"
    return " ".join(x for x in [date, direction, amount, tail] if x)


def load_rows(path: str) -> List[Dict[str, str]]:
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list")
        return data
    if p.suffix.lower() == ".csv":
        with open(p, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError("Unsupported input type; expected .json or .csv")


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
            raise RuntimeError(f"Failed to get tenant access token: {data}")
        self._token = data["tenant_access_token"]
        return self._token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self._tenant_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def list_fields(self, app_token: str, table_id: str):
        url = f"{OPEN_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        resp = requests.get(url, headers=self._headers(), timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"List fields failed: {json.dumps(data, ensure_ascii=False)}")
        return ((data.get("data") or {}).get("items")) or []

    def create_record(self, app_token: str, table_id: str, fields: Dict):
        url = f"{OPEN_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        resp = requests.post(url, headers=self._headers(), json={"fields": fields}, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"Create record failed: {json.dumps(data, ensure_ascii=False)}")
        return data


def row_to_feishu_fields(row: Dict[str, str], primary_field_name: str = "家庭记账") -> Dict:
    out = {
        primary_field_name: primary_title(row),
        "一级类型": clean(row.get("一级类型")) or None,
        "二级类型": clean(row.get("二级类型")) or None,
        "导入来源": clean(row.get("导入来源")) or None,
        "备注": clean(row.get("备注")) or None,
        "记账人": clean(row.get("记账人")) or None,
        "流水号": clean(row.get("流水号")) or None,
    }

    amount = normalize_number(row.get("金额"))
    if amount is not None:
        out["金额"] = amount

    date_ms = normalize_date_to_ms(row.get("日期"))
    if date_ms is not None:
        out["日期"] = date_ms

    pay_platform = clean(row.get("支付平台"))
    if pay_platform:
        out["支付平台"] = pay_platform

    income_expense = clean(row.get("收支类型"))
    if income_expense:
        out["收支类型"] = income_expense

    return {k: v for k, v in out.items() if v not in (None, "")}


def main():
    parser = argparse.ArgumentParser(description="Write bookkeeping rows directly into Feishu Bitable.")
    parser.add_argument("input", help="Rows to write (.json or .csv)")
    parser.add_argument("--app-token", default=DEFAULT_APP_TOKEN)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    parser.add_argument("--dry-run", action="store_true", help="Render payloads only, do not write")
    parser.add_argument("--limit", type=int, help="Only process first N rows")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        raise SystemExit("Need --app-id and --app-secret, or FEISHU_APP_ID / FEISHU_APP_SECRET in env")

    rows = load_rows(args.input)
    if args.limit:
        rows = rows[:args.limit]

    client = FeishuClient(args.app_id, args.app_secret)
    fields = client.list_fields(args.app_token, args.table_id)
    primary_field_name = next((f.get("field_name") for f in fields if f.get("is_primary")), "家庭记账")
    payloads = [row_to_feishu_fields(row, primary_field_name=primary_field_name) for row in rows]

    if args.dry_run:
        print(json.dumps({
            "count": len(payloads),
            "primary_field_name": primary_field_name,
            "payloads": payloads
        }, ensure_ascii=False, indent=2))
        return

    results = []
    for payload in payloads:
        results.append(client.create_record(args.app_token, args.table_id, payload))

    print(json.dumps({"written": len(results)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
