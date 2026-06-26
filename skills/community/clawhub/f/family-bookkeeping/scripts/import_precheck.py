#!/usr/bin/env python3
import argparse
import csv
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests

CANONICAL_FIELDS = [
    "日期",
    "金额",
    "记账人",
    "一级类型",
    "二级类型",
    "备注",
    "收支类型",
    "支付平台",
    "导入来源",
    "流水号",
]

REPORT_DEFAULTS = {
    "app_token": "",
    "table_id": "",
    "fetched_existing": 0,
    "existing_with_txn": 0,
    "existing_with_fallback": 0,
    "input_rows": 0,
    "new_rows": 0,
    "duplicate_rows": 0,
    "skipped_blank_rows": 0,
}


@dataclass
class ExistingRecord:
    record_id: str
    fields: Dict
    txn_key: str = ""
    fallback_key: str = ""


def clean(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(str(item.get("name") or item.get("text") or item.get("id") or ""))
            else:
                parts.append(str(item))
        return " ".join(x.strip() for x in parts if str(x).strip())
    if isinstance(value, dict):
        return str(value.get("name") or value.get("text") or value.get("id") or "").strip()
    return str(value).strip().replace("\ufeff", "")


def normalize_amount(value) -> str:
    text = clean(value).replace(",", "").replace("¥", "").replace("￥", "")
    if not text:
        return ""
    try:
        amount = abs(Decimal(text))
    except InvalidOperation:
        try:
            import re
            m = re.search(r"-?\d+(?:\.\d+)?", text)
            if not m:
                return ""
            amount = abs(Decimal(m.group(0)))
        except Exception:
            return ""
    rendered = format(amount.normalize(), "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered


def normalize_date(value) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, (int, float)):
        # Feishu DateTime often returns ms timestamp
        try:
            ts = float(value)
            if ts > 10_000_000_000:
                ts /= 1000.0
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone()
            return dt.strftime("%Y-%m-%d")
        except Exception:
            return ""
    text = clean(value)
    if not text:
        return ""
    text = text.replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:19], fmt).strftime("%Y-%m-%d")
        except Exception:
            pass
    if len(text) >= 10:
        return text[:10]
    return text


def canonicalize_row(row: Dict) -> Dict[str, str]:
    return {
        "日期": normalize_date(row.get("日期")),
        "金额": normalize_amount(row.get("金额")),
        "记账人": clean(row.get("记账人")),
        "一级类型": clean(row.get("一级类型")),
        "二级类型": clean(row.get("二级类型")),
        "备注": clean(row.get("备注")),
        "收支类型": clean(row.get("收支类型")),
        "支付平台": clean(row.get("支付平台")),
        "导入来源": clean(row.get("导入来源")),
        "流水号": clean(row.get("流水号")),
    }


def row_is_blank(row: Dict[str, str]) -> bool:
    return not any(clean(v) for v in row.values())


def dedupe_keys(row: Dict[str, str]) -> Tuple[str, str]:
    txn = clean(row.get("流水号"))
    txn_key = f"txn:{txn}" if txn else ""
    fallback_key = "fallback:" + "|".join([
        clean(row.get("日期")),
        clean(row.get("金额")),
        clean(row.get("支付平台")),
        clean(row.get("备注")),
    ])
    return txn_key, fallback_key


def load_rows(path: str) -> List[Dict[str, str]]:
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list of rows")
        return [canonicalize_row(x) for x in data]
    if p.suffix.lower() == ".csv":
        with open(p, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return [canonicalize_row(row) for row in reader]
    raise ValueError("Unsupported input type. Use normalized .json or .csv")


class FeishuBitableClient:
    def __init__(self, app_id: str, app_secret: str, timeout: int = 30):
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self.base = "https://open.feishu.cn/open-apis"
        self._tenant_access_token: Optional[str] = None

    def _headers(self) -> Dict[str, str]:
        if not self._tenant_access_token:
            self._tenant_access_token = self._get_tenant_access_token()
        return {
            "Authorization": f"Bearer {self._tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def _get_tenant_access_token(self) -> str:
        url = f"{self.base}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={"app_id": self.app_id, "app_secret": self.app_secret}, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"Failed to get tenant access token: {data}")
        return data["tenant_access_token"]

    def list_records(self, app_token: str, table_id: str, page_size: int = 500) -> Iterable[Dict]:
        page_token = None
        while True:
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            url = f"{self.base}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
            resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise RuntimeError(f"Failed to list records: {data}")
            items = (((data.get("data") or {}).get("items")) or [])
            for item in items:
                yield item
            has_more = ((data.get("data") or {}).get("has_more")) or False
            if not has_more:
                break
            page_token = (data.get("data") or {}).get("page_token")
            if not page_token:
                break


def build_existing_index(records: Iterable[Dict]) -> Tuple[List[ExistingRecord], Dict[str, List[ExistingRecord]], Dict[str, List[ExistingRecord]]]:
    all_records: List[ExistingRecord] = []
    by_txn: Dict[str, List[ExistingRecord]] = {}
    by_fallback: Dict[str, List[ExistingRecord]] = {}
    for record in records:
        fields = canonicalize_row(record.get("fields") or {})
        if row_is_blank(fields):
            continue
        txn_key, fallback_key = dedupe_keys(fields)
        item = ExistingRecord(record_id=record.get("record_id") or record.get("recordId") or record.get("id") or "", fields=fields, txn_key=txn_key, fallback_key=fallback_key)
        all_records.append(item)
        if txn_key:
            by_txn.setdefault(txn_key, []).append(item)
        by_fallback.setdefault(fallback_key, []).append(item)
    return all_records, by_txn, by_fallback


def write_csv(path: Path, rows: List[Dict[str, str]], extra_fields: Optional[List[str]] = None) -> None:
    fields = list(CANONICAL_FIELDS)
    if extra_fields:
        fields.extend(extra_fields)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def main():
    parser = argparse.ArgumentParser(description="Compare normalized bill rows against existing Feishu Bitable records and split new vs duplicate rows.")
    parser.add_argument("input", help="Normalized .json or .csv")
    parser.add_argument("--app-token", required=True, help="Feishu Bitable app token")
    parser.add_argument("--table-id", required=True, help="Feishu Bitable table id")
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""), help="Feishu app id (or FEISHU_APP_ID env)")
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""), help="Feishu app secret (or FEISHU_APP_SECRET env)")
    parser.add_argument("--output-dir", required=True, help="Directory for report outputs")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        raise SystemExit("Need --app-id and --app-secret, or FEISHU_APP_ID / FEISHU_APP_SECRET in env")

    input_rows = load_rows(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    client = FeishuBitableClient(args.app_id, args.app_secret)
    existing_raw = list(client.list_records(args.app_token, args.table_id))
    existing_rows, existing_by_txn, existing_by_fallback = build_existing_index(existing_raw)

    report = dict(REPORT_DEFAULTS)
    report.update({
        "app_token": args.app_token,
        "table_id": args.table_id,
        "fetched_existing": len(existing_raw),
        "existing_nonblank": len(existing_rows),
        "existing_with_txn": len(existing_by_txn),
        "existing_with_fallback": len(existing_by_fallback),
        "input_rows": len(input_rows),
    })

    new_rows: List[Dict[str, str]] = []
    duplicate_rows: List[Dict[str, str]] = []

    for row in input_rows:
        if row_is_blank(row):
            report["skipped_blank_rows"] += 1
            continue
        txn_key, fallback_key = dedupe_keys(row)
        matches: List[ExistingRecord] = []
        match_basis = ""
        if txn_key and txn_key in existing_by_txn:
            matches = existing_by_txn[txn_key]
            match_basis = "流水号"
        elif fallback_key in existing_by_fallback:
            matches = existing_by_fallback[fallback_key]
            match_basis = "fallback"

        if matches:
            duplicate_rows.append({
                **row,
                "重复依据": match_basis,
                "命中记录ID": ",".join(x.record_id for x in matches if x.record_id),
            })
        else:
            new_rows.append(row)

    report["new_rows"] = len(new_rows)
    report["duplicate_rows"] = len(duplicate_rows)

    write_csv(out_dir / "new_records.csv", new_rows)
    write_csv(out_dir / "duplicate_records.csv", duplicate_rows, extra_fields=["重复依据", "命中记录ID"])
    (out_dir / "import_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
