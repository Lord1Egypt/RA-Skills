#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portable FOFA batch search CLI.

Features:
- Interactive mode and no-interactive mode.
- Auto paging with /search/next fallback to /search/all?page.
- Export CSV and optional JSON.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import locale
import re
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests


DEFAULT_BASE_URL = "https://fofa.info"
DEFAULT_FIELDS = "host,ip,port,protocol,title"
DEFAULT_PAGE_SIZE = 10000
MAX_PAGE_SIZE = 10000


class FofaError(Exception):
    def __init__(self, message: str):
        self.message = message
        self.code = self._extract_error_code(message)
        super().__init__(message)

    @staticmethod
    def _extract_error_code(error_message: str) -> Optional[int]:
        matched = re.search(r"\[(-?\d+)\]", error_message or "")
        if matched:
            return int(matched.group(1))
        return None


def encode_query(query: str) -> str:
    return base64.b64encode(query.encode("utf-8")).decode("utf-8")


def get_shell_language() -> str:
    lang = locale.getlocale()[0]
    if not lang:
        try:
            lang = locale.getdefaultlocale()[0]  # fallback for old envs
        except Exception:
            lang = None
    return lang or "en"


class FofaClient:
    def __init__(self, key: str, base_url: str = DEFAULT_BASE_URL, timeout: int = 30):
        self.key = key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.lang = "zh-CN" if get_shell_language().startswith("zh") else "en"

        if not self.key:
            raise FofaError("FOFA key is empty")

    def _request(self, path: str, params: Optional[Dict] = None, retries: int = 3) -> Dict:
        url = f"{self.base_url}{path}"
        request_params = dict(params or {})
        request_params["key"] = self.key
        request_params["lang"] = self.lang

        last_error = None
        for _ in range(retries):
            try:
                resp = self.session.get(url, params=request_params, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                if data.get("error"):
                    raise FofaError(data.get("errmsg") or "FOFA API error")
                return data
            except (requests.RequestException, ValueError, FofaError) as exc:
                last_error = exc
                time.sleep(1)
        raise FofaError(f"Request failed: {last_error}")

    def search(self, query: str, fields: str, page: int, size: int) -> Dict:
        return self._request(
            "/api/v1/search/all",
            {
                "qbase64": encode_query(query),
                "fields": fields,
                "page": page,
                "size": size,
            },
        )

    def search_next(self, query: str, fields: str, size: int, next_token: str = "") -> Dict:
        params = {
            "qbase64": encode_query(query),
            "fields": fields,
            "size": size,
        }
        if next_token:
            params["next"] = next_token
        return self._request("/api/v1/search/next", params)

    def can_use_next(self) -> bool:
        try:
            self.search_next("bad=query", fields="ip", size=1)
        except FofaError as exc:
            return exc.code == 820000
        return False


def _prompt_required(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required.")


def _prompt_int(prompt: str, default: int, minimum: int, maximum: int) -> int:
    while True:
        raw = input(f"{prompt} (default {default}): ").strip()
        if not raw:
            return default
        if not raw.isdigit():
            print("Please input an integer.")
            continue
        value = int(raw)
        if value < minimum or value > maximum:
            print(f"Please input {minimum} ~ {maximum}.")
            continue
        return value


def _rows_to_dicts(rows: Iterable[List], fields: List[str]) -> Iterable[Dict]:
    for row in rows:
        item = {}
        for idx, field in enumerate(fields):
            item[field] = row[idx] if idx < len(row) else ""
        yield item


def save_csv(path: Path, records: List[Dict], fields: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in records:
            writer.writerow(item)


def save_json(path: Path, records: List[Dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def fetch_all(
    client: FofaClient,
    query: str,
    fields: str,
    max_records: int,
    page_size: int,
) -> Tuple[List[Dict], int, int]:
    field_list = [x.strip() for x in fields.split(",") if x.strip()]
    all_records: List[Dict] = []
    total_size = 0
    consumed_fpoint = 0

    use_next = client.can_use_next()
    print(f"[mode] {'search/next' if use_next else 'search/all?page'}")

    if use_next:
        next_token = ""
        while len(all_records) < max_records:
            remain = max_records - len(all_records)
            size = min(page_size, remain)
            resp = client.search_next(query=query, fields=fields, size=size, next_token=next_token)
            rows = resp.get("results", [])
            if not rows:
                break
            all_records.extend(list(_rows_to_dicts(rows, field_list)))
            total_size = resp.get("size", total_size)
            consumed_fpoint += int(resp.get("consumed_fpoint", 0))
            next_token = resp.get("next", "")
            print(f"[progress] {len(all_records)}/{max_records}")
            if len(rows) < size:
                break
    else:
        page = 1
        while len(all_records) < max_records:
            remain = max_records - len(all_records)
            size = min(page_size, remain)
            resp = client.search(query=query, fields=fields, page=page, size=size)
            rows = resp.get("results", [])
            if not rows:
                break
            all_records.extend(list(_rows_to_dicts(rows, field_list)))
            total_size = resp.get("size", total_size)
            consumed_fpoint += int(resp.get("consumed_fpoint", 0))
            print(f"[progress] page={page}, got={len(all_records)}/{max_records}")
            if len(rows) < size:
                break
            page += 1

    if len(all_records) > max_records:
        all_records = all_records[:max_records]

    return all_records, total_size, consumed_fpoint


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FOFA portable batch search CLI")
    parser.add_argument("--key", help="FOFA API key")
    parser.add_argument("--query", help="FOFA query string")
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help=f"fields list, default: {DEFAULT_FIELDS}")
    parser.add_argument("--max-records", type=int, default=1000, help="max records to fetch")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help=f"page size (1-{MAX_PAGE_SIZE})")
    parser.add_argument("--output-file", default="fofa_results.csv", help="csv output file path")
    parser.add_argument("--json-output", action="store_true", help="also export json")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"fofa base url, default: {DEFAULT_BASE_URL}")
    parser.add_argument("--no-interactive", action="store_true", help="do not ask input interactively")
    return parser


def gather_args(args: argparse.Namespace) -> argparse.Namespace:
    if args.no_interactive:
        if not args.key or not args.query:
            raise FofaError("In --no-interactive mode, --key and --query are required")
        return args

    print("=== FOFA Portable Search CLI ===")
    args.key = args.key or _prompt_required("FOFA key: ")
    args.query = args.query or _prompt_required("FOFA query: ")
    if args.fields == DEFAULT_FIELDS:
        custom_fields = input(f"fields (default {DEFAULT_FIELDS}): ").strip()
        if custom_fields:
            args.fields = custom_fields
    args.max_records = _prompt_int("max records", args.max_records, 1, 1_000_000)
    args.page_size = _prompt_int("page size", args.page_size, 1, MAX_PAGE_SIZE)
    if args.output_file == "fofa_results.csv":
        output = input("csv output filename (default fofa_results.csv): ").strip()
        if output:
            args.output_file = output
    if not args.json_output:
        args.json_output = input("also export JSON? (y/N): ").strip().lower() == "y"
    return args


def main() -> None:
    parser = build_parser()
    args = gather_args(parser.parse_args())

    client = FofaClient(key=args.key, base_url=args.base_url)
    records, total, consumed = fetch_all(
        client=client,
        query=args.query,
        fields=args.fields,
        max_records=args.max_records,
        page_size=args.page_size,
    )

    if not records:
        print("[done] no data found.")
        return

    csv_path = Path(args.output_file)
    field_list = [x.strip() for x in args.fields.split(",") if x.strip()]
    save_csv(csv_path, records, field_list)
    print(f"[done] csv saved: {csv_path.resolve()}")

    json_path = None
    if args.json_output:
        json_path = csv_path.with_suffix(".json")
        save_json(json_path, records)
        print(f"[done] json saved: {json_path.resolve()}")

    result = {
        "query": args.query,
        "mode": "next_or_page_auto",
        "fofa_total": total,
        "exported": len(records),
        "consumed_fpoint": consumed,
        "csv_file": str(csv_path.resolve()),
        "json_file": str(json_path.resolve()) if json_path else None,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
