#!/usr/bin/env python3
"""Write / update Lark/Feishu Sheets via OpenAPI.

Complement to sheets_export.py (read-only). This script provides:
- Write cell values to a range (single or batch)
- Add a new sheet tab
- Clone an existing sheet's values into a new sheet
- List all sheet tabs in a spreadsheet

Usage examples:

  # Write a single range
  python3 sheets_write.py write \
    --token YOUR_SPREADSHEET_TOKEN \
    --range 'SheetId!A1:C2' \
    --values '[["a","b","c"],["d","e","f"]]'

  # Write from a JSON file (array of arrays)
  python3 sheets_write.py write \
    --token YOUR_SPREADSHEET_TOKEN \
    --range 'SheetId!A1:C2' \
    --values-file data.json

  # Batch write multiple ranges
  python3 sheets_write.py batch-write \
    --token YOUR_SPREADSHEET_TOKEN \
    --batch '[{"range":"Sheet1!A1:B1","values":[["x","y"]]},{"range":"Sheet1!A2:B2","values":[["1","2"]]}]'

  # List all sheet tabs
  python3 sheets_write.py list-sheets \
    --token YOUR_SPREADSHEET_TOKEN

  # Add a new sheet tab
  python3 sheets_write.py add-sheet \
    --token YOUR_SPREADSHEET_TOKEN \
    --title 'NewSheet'

  # Clone an existing sheet's values into a new sheet
  python3 sheets_write.py clone-sheet \
    --token YOUR_SPREADSHEET_TOKEN \
    --source-sheet-id abc123 \
    --title 'ClonedSheet' \
    --clone-range 'A1:Z200'

Notes:
- Reads appId/appSecret from ~/.openclaw/openclaw.json (OpenClaw config).
- Range format: "{sheetId}!A1:Z200" or "{sheetTitle}!A1:Z200".
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import Any

OPENCLAW_CONFIG = os.environ.get(
    "OPENCLAW_CONFIG",
    os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json"),
)


# ── HTTP / Auth helpers ──────────────────────────────────────────────

def _http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: Any | None = None,
    timeout: int = 60,
) -> dict:
    data = None
    h: dict[str, str] = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=h, method=method.upper())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:2000]}")


def _read_feishu_cfg(path: str = OPENCLAW_CONFIG) -> tuple[str, str, str]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    feishu = (cfg.get("channels") or {}).get("feishu") or {}
    app_id = feishu.get("appId")
    app_secret = feishu.get("appSecret")
    domain = (feishu.get("domain") or "feishu").lower().strip()
    if not app_id or not app_secret:
        raise RuntimeError(
            f"Missing channels.feishu.appId/appSecret in {path}. "
            "Run `openclaw configure` or set OPENCLAW_CONFIG."
        )
    return app_id, app_secret, domain


def _base_url(domain: str) -> str:
    return (
        "https://open.larksuite.com" if domain == "lark" else "https://open.feishu.cn"
    )


def _tenant_token(app_id: str, app_secret: str, base: str) -> str:
    j = _http_json(
        "POST",
        base + "/open-apis/auth/v3/tenant_access_token/internal",
        body={"app_id": app_id, "app_secret": app_secret},
    )
    if j.get("code") != 0:
        raise RuntimeError(
            f"tenant_access_token failed: code={j.get('code')} msg={j.get('msg')}"
        )
    return j["tenant_access_token"]


def _extract_spreadsheet_token(url: str) -> str | None:
    m = re.search(r"/sheets/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else None


def _auth_header(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


# ── Sheets API wrappers ─────────────────────────────────────────────

def sheets_query(
    spreadsheet_token: str, access_token: str, base: str
) -> list[dict]:
    """List all sheet tabs in a spreadsheet."""
    url = base + f"/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query"
    j = _http_json("GET", url, headers=_auth_header(access_token))
    if j.get("code") != 0:
        raise RuntimeError(
            f"sheets/query failed: code={j.get('code')} msg={j.get('msg')}"
        )
    data = j.get("data") or {}
    return data.get("sheets") or data.get("items") or []


def values_batch_get(
    spreadsheet_token: str, ranges: list[str], access_token: str, base: str
) -> dict:
    """Read cell values for one or more ranges."""
    endpoint = (
        base
        + f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_get"
    )
    query = urllib.parse.urlencode({"ranges": ranges}, doseq=True)
    j = _http_json("GET", endpoint + "?" + query, headers=_auth_header(access_token))
    if j.get("code") != 0:
        raise RuntimeError(
            f"values_batch_get failed: code={j.get('code')} msg={j.get('msg')}"
        )
    return j


def values_batch_update(
    spreadsheet_token: str,
    value_ranges: list[dict],
    access_token: str,
    base: str,
    value_input_option: str = "USER_ENTERED",
) -> dict:
    """Write cell values for one or more ranges.

    Each item in value_ranges: {"range": "SheetId!A1:B2", "values": [["a","b"],["c","d"]]}
    """
    endpoint = (
        base
        + f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_update"
    )
    j = _http_json(
        "POST",
        endpoint,
        headers=_auth_header(access_token),
        body={"valueRanges": value_ranges, "valueInputOption": value_input_option},
    )
    if j.get("code") != 0:
        raise RuntimeError(
            f"values_batch_update failed: code={j.get('code')} msg={j.get('msg')}"
        )
    return j


def add_sheet(
    spreadsheet_token: str, title: str, access_token: str, base: str
) -> str:
    """Create a new sheet tab and return its sheetId."""
    endpoint = (
        base
        + f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update"
    )
    body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
    j = _http_json("POST", endpoint, headers=_auth_header(access_token), body=body)
    if j.get("code") != 0:
        raise RuntimeError(
            f"addSheet failed: code={j.get('code')} msg={j.get('msg')}"
        )
    # Try to extract sheetId from response
    replies = (j.get("data") or {}).get("replies") or []
    for r in replies:
        props = (r.get("addSheet") or {}).get("properties") or r.get("properties") or {}
        sid = props.get("sheetId") or props.get("sheet_id")
        if sid:
            return sid
    # Fallback: re-query by title
    sheets = sheets_query(spreadsheet_token, access_token, base)
    for s in sheets:
        if (s.get("title") or "").strip() == title:
            return s.get("sheet_id") or s.get("sheetId")
    raise RuntimeError("Could not resolve new sheetId after addSheet")


def clone_sheet(
    spreadsheet_token: str,
    source_sheet_id: str,
    new_title: str,
    access_token: str,
    base: str,
    clone_range: str = "A1:Z200",
) -> str:
    """Create a new sheet tab and copy values from an existing sheet."""
    new_sheet_id = add_sheet(spreadsheet_token, new_title, access_token, base)

    src_range = f"{source_sheet_id}!{clone_range}"
    data = values_batch_get(spreadsheet_token, [src_range], access_token, base)
    value_ranges = (data.get("data") or {}).get("valueRanges") or []
    vals = (value_ranges[0].get("values") if value_ranges else []) or []

    if vals:
        # Determine the write range from cloned data dimensions
        num_rows = len(vals)
        max_cols = max(len(row) for row in vals) if vals else 1
        # Convert column number to letter(s)
        end_col = ""
        c = max_cols
        while c > 0:
            c, remainder = divmod(c - 1, 26)
            end_col = chr(65 + remainder) + end_col
        dest_range = f"{new_sheet_id}!A1:{end_col}{num_rows}"
        values_batch_update(
            spreadsheet_token,
            [{"range": dest_range, "values": vals}],
            access_token,
            base,
        )

    return new_sheet_id


# ── CLI subcommands ──────────────────────────────────────────────────

def cmd_list_sheets(args, access_token: str, base: str):
    sheets = sheets_query(args.spreadsheet_token, access_token, base)
    result = []
    for s in sheets:
        result.append(
            {
                "sheet_id": s.get("sheet_id") or s.get("sheetId"),
                "title": s.get("title"),
                "index": s.get("index"),
            }
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_write(args, access_token: str, base: str):
    if args.values_file:
        with open(args.values_file, "r", encoding="utf-8") as f:
            values = json.load(f)
    elif args.values:
        values = json.loads(args.values)
    else:
        raise SystemExit("Provide --values (JSON string) or --values-file (path)")

    if not isinstance(values, list):
        raise SystemExit("Values must be a JSON array of arrays, e.g. [[\"a\",\"b\"],[\"c\",\"d\"]]")

    values_batch_update(
        args.spreadsheet_token,
        [{"range": args.range, "values": values}],
        access_token,
        base,
    )
    print(json.dumps({"ok": True, "range": args.range, "rows": len(values)}, ensure_ascii=False))


def cmd_batch_write(args, access_token: str, base: str):
    if args.batch_file:
        with open(args.batch_file, "r", encoding="utf-8") as f:
            batch = json.load(f)
    elif args.batch:
        batch = json.loads(args.batch)
    else:
        raise SystemExit("Provide --batch (JSON string) or --batch-file (path)")

    if not isinstance(batch, list):
        raise SystemExit("Batch must be a JSON array of {range, values} objects")

    values_batch_update(args.spreadsheet_token, batch, access_token, base)
    print(
        json.dumps(
            {"ok": True, "ranges_updated": len(batch)},
            ensure_ascii=False,
        )
    )


def cmd_add_sheet(args, access_token: str, base: str):
    sheet_id = add_sheet(args.spreadsheet_token, args.title, access_token, base)
    print(json.dumps({"ok": True, "sheet_id": sheet_id, "title": args.title}, ensure_ascii=False))


def cmd_clone_sheet(args, access_token: str, base: str):
    sheet_id = clone_sheet(
        args.spreadsheet_token,
        args.source_sheet_id,
        args.title,
        access_token,
        base,
        clone_range=args.clone_range,
    )
    print(
        json.dumps(
            {
                "ok": True,
                "sheet_id": sheet_id,
                "title": args.title,
                "cloned_from": args.source_sheet_id,
            },
            ensure_ascii=False,
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="Write / update Lark/Feishu Sheets via OpenAPI"
    )
    parser.add_argument(
        "--url", help="Lark/Feishu sheet URL (extracts spreadsheet token automatically)"
    )
    parser.add_argument("--token", dest="token_arg", help="Spreadsheet token directly")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")

    sub = parser.add_subparsers(dest="command", required=True)

    # list-sheets
    sub.add_parser("list-sheets", help="List all sheet tabs")

    # write
    p_write = sub.add_parser("write", help="Write values to a single range")
    p_write.add_argument("--range", required=True, help="Target range, e.g. 'SheetId!A1:C2'")
    p_write.add_argument("--values", help='JSON array of arrays, e.g. \'[["a","b"],["c","d"]]\'')
    p_write.add_argument("--values-file", help="Path to JSON file containing values array")

    # batch-write
    p_batch = sub.add_parser("batch-write", help="Batch write multiple ranges")
    p_batch.add_argument("--batch", help='JSON array of {range, values} objects')
    p_batch.add_argument("--batch-file", help="Path to JSON file containing batch array")

    # add-sheet
    p_add = sub.add_parser("add-sheet", help="Add a new sheet tab")
    p_add.add_argument("--title", required=True, help="New sheet title")

    # clone-sheet
    p_clone = sub.add_parser("clone-sheet", help="Clone an existing sheet into a new tab")
    p_clone.add_argument("--source-sheet-id", required=True, help="Source sheet ID to clone from")
    p_clone.add_argument("--title", required=True, help="New sheet title")
    p_clone.add_argument("--clone-range", default="A1:Z200", help="Range to copy (default: A1:Z200)")

    args = parser.parse_args()

    # Resolve spreadsheet token
    spreadsheet_token = args.token_arg
    if not spreadsheet_token and args.url:
        spreadsheet_token = _extract_spreadsheet_token(args.url)
    if not spreadsheet_token:
        raise SystemExit(
            "Missing spreadsheet token. Provide --token or --url containing /sheets/<token>."
        )
    args.spreadsheet_token = spreadsheet_token

    # Auth
    app_id, app_secret, domain = _read_feishu_cfg()
    base = _base_url(domain)
    access_token = _tenant_token(app_id, app_secret, base)

    if args.dry_run:
        print(f"[dry-run] command={args.command} token={spreadsheet_token}")
        return

    # Dispatch
    handlers = {
        "list-sheets": cmd_list_sheets,
        "write": cmd_write,
        "batch-write": cmd_batch_write,
        "add-sheet": cmd_add_sheet,
        "clone-sheet": cmd_clone_sheet,
    }
    handlers[args.command](args, access_token, base)


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            pass
        print(
            f"HTTPError: {e.code} {e.reason} url={e.url}\n{body[:2000]}",
            file=sys.stderr,
        )
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
