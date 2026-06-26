#!/usr/bin/env python3
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

OPEN_API_BASE = "https://open.feishu.cn/open-apis"
DEFAULT_APP_TOKEN = os.getenv("FAMILY_BOOKKEEPING_APP_TOKEN", "")
DEFAULT_TABLE_ID = os.getenv("FAMILY_BOOKKEEPING_TABLE_ID", "")
SCRIPT_DIR = Path(__file__).resolve().parent
REPORT_SCRIPT = SCRIPT_DIR / "bookkeeping_report.py"


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

    def list_records(self, app_token: str, table_id: str, page_size: int = 500):
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
                raise RuntimeError(f"Failed to list records: {json.dumps(data, ensure_ascii=False)}")
            payload = data.get("data") or {}
            out.extend(payload.get("items") or [])
            if not payload.get("has_more"):
                break
            page_token = payload.get("page_token")
            if not page_token:
                break
        return out


def main():
    parser = argparse.ArgumentParser(description="Query the live family-bookkeeping Bitable and summarize it.")
    parser.add_argument("--app-token", default=DEFAULT_APP_TOKEN)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    parser.add_argument("--month")
    parser.add_argument("--bookkeeper", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--platform", default="")
    parser.add_argument("--income-expense", default="")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--recent", type=int, default=0, help="Return N most recent rows instead of summary")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        raise SystemExit("Need --app-id and --app-secret, or FEISHU_APP_ID / FEISHU_APP_SECRET in env")

    client = FeishuClient(args.app_id, args.app_secret)
    records = client.list_records(args.app_token, args.table_id)
    fields_rows = [r.get("fields", {}) for r in records]

    if args.recent > 0:
        def sort_key(row):
            v = row.get("日期")
            if isinstance(v, (int, float)):
                return float(v)
            return 0
        rows = sorted(fields_rows, key=sort_key, reverse=True)[:args.recent]
        print(json.dumps({"recent": rows}, ensure_ascii=False, indent=2))
        return

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as tmp:
        json.dump({"records": [{"fields": row} for row in fields_rows]}, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    cmd = [sys.executable, str(REPORT_SCRIPT), tmp_path, "--top", str(args.top)]
    if args.month:
        cmd.extend(["--month", args.month])
    if args.bookkeeper:
        cmd.extend(["--bookkeeper", args.bookkeeper])
    if args.category:
        cmd.extend(["--category", args.category])
    if args.platform:
        cmd.extend(["--platform", args.platform])
    if args.income_expense:
        cmd.extend(["--income-expense", args.income_expense])

    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        raise SystemExit(proc.returncode)
    print(proc.stdout)


if __name__ == "__main__":
    main()
