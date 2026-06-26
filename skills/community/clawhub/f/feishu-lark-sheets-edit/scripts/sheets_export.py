#!/usr/bin/env python3
"""Export Lark/Feishu Sheets ranges to JSON or CSV.

- Reads appId/appSecret from ~/.openclaw/openclaw.json (OpenClaw config)
- Fetches tenant_access_token
- Calls Sheets OpenAPI values_batch_get

Usage examples:
  python3 sheets_export.py --url "https://.../sheets/<token>?sheet=<id>" --range "Sheet1!A1:D50" --csv out.csv
  python3 sheets_export.py --token <token> --range "<sheetId>!A1:Z200" --json out.json

Notes:
- Range format accepted by the API typically looks like: "{sheetId}!A1:Z200" or "{sheetTitle}!A1:Z200".
- If you only have the sheet id from URL (?sheet=xxx), try using that as the left part.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

OPENCLAW_CONFIG = os.environ.get(
    "OPENCLAW_CONFIG",
    os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json"),
)


def _read_openclaw_feishu_config(path: str = OPENCLAW_CONFIG) -> tuple[str, str, str]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    feishu = (cfg.get("channels") or {}).get("feishu") or {}
    app_id = feishu.get("appId")
    app_secret = feishu.get("appSecret")
    domain = feishu.get("domain") or "feishu"  # "lark" or "feishu"

    if not app_id or not app_secret:
        raise RuntimeError(
            f"Missing channels.feishu.appId/appSecret in {path}. "
            "Run `openclaw configure` or set OPENCLAW_CONFIG."
        )

    return app_id, app_secret, domain


def _base_url(domain: str) -> str:
    domain = (domain or "").lower().strip()
    if domain == "lark":
        return "https://open.larksuite.com"
    return "https://open.feishu.cn"


def _http_json(method: str, url: str, headers: dict[str, str] | None = None, body: dict | None = None):
    data = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method.upper())
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:2000]}")


def _get_tenant_access_token(app_id: str, app_secret: str, base: str) -> str:
    url = base + "/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    j = _http_json("POST", url, body=payload)

    if j.get("code") != 0:
        # Do NOT print secrets.
        raise RuntimeError(f"Failed to get tenant_access_token: code={j.get('code')} msg={j.get('msg')}")

    token = (j.get("tenant_access_token") or "").strip()
    if not token:
        raise RuntimeError("tenant_access_token missing in response")
    return token


def _extract_spreadsheet_token(url: str) -> str | None:
    # e.g. https://xxx.larksuite.com/sheets/YOUR_SPREADSHEET_TOKEN?sheet=v8Yh4e
    m = re.search(r"/sheets/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else None


def _values_batch_get(spreadsheet_token: str, ranges: list[str], access_token: str, base: str) -> dict:
    if not ranges:
        raise ValueError("At least one --range is required")

    endpoint = base + f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_get"
    query = urllib.parse.urlencode({"ranges": ranges}, doseq=True)
    url = endpoint + "?" + query
    j = _http_json("GET", url, headers={"Authorization": f"Bearer {access_token}"})

    if j.get("code") != 0:
        raise RuntimeError(f"values_batch_get failed: code={j.get('code')} msg={j.get('msg')}")
    return j


def _flatten_values_batch(values_batch: dict) -> list[dict]:
    # Expected shape: { data: { valueRanges: [ { range: "...", values: [[...], ...] }, ... ] } }
    data = values_batch.get("data") or {}
    vrs = data.get("valueRanges") or data.get("value_ranges") or []
    out = []
    for vr in vrs:
        out.append({
            "range": vr.get("range"),
            "values": vr.get("values") or [],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="Lark/Feishu sheet URL")
    ap.add_argument("--token", help="Spreadsheet token (the part after /sheets/)")
    ap.add_argument("--range", dest="ranges", action="append", default=[], help="Range, repeatable. Example: 'v8Yh4e!A1:Z200' or 'Sheet1!A1:D50'")
    ap.add_argument("--json", dest="json_path", help="Write raw API output (normalized) to JSON")
    ap.add_argument("--csv", dest="csv_path", help="Write CSV (only when exactly one range is returned)")
    args = ap.parse_args()

    spreadsheet_token = args.token
    if not spreadsheet_token and args.url:
        spreadsheet_token = _extract_spreadsheet_token(args.url)

    if not spreadsheet_token:
        raise SystemExit("Missing spreadsheet token. Provide --token or --url containing /sheets/<token>.")

    app_id, app_secret, domain = _read_openclaw_feishu_config()
    base = _base_url(domain)

    access_token = _get_tenant_access_token(app_id, app_secret, base)
    batch = _values_batch_get(spreadsheet_token, args.ranges, access_token, base)
    normalized = {
        "spreadsheet_token": spreadsheet_token,
        "fetched_at": int(time.time()),
        "valueRanges": _flatten_values_batch(batch),
    }

    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as f:
            json.dump(normalized, f, ensure_ascii=False, indent=2)

    if args.csv_path:
        vrs = normalized["valueRanges"]
        if len(vrs) != 1:
            raise SystemExit("--csv requires exactly one --range (or at least one range that returns a single valueRange)")
        values = vrs[0]["values"]
        with open(args.csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            for row in values:
                w.writerow(row)

    if not args.json_path and not args.csv_path:
        # Print a compact preview to stdout
        vrs = normalized["valueRanges"]
        print(f"OK: {spreadsheet_token} ranges={len(vrs)}")
        for vr in vrs:
            vals = vr.get("values") or []
            print(f"- {vr.get('range')}: rows={len(vals)}")
            if vals:
                preview = vals[:3]
                print("  preview:")
                for r in preview:
                    print("   ", r)


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            body = ""
        print(f"HTTPError: {e.code} {e.reason} url={e.url}\n{body[:2000]}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
