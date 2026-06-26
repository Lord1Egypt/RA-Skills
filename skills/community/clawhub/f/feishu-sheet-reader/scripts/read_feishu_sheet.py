#!/usr/bin/env python3
"""
Read data from a Feishu Sheet (电子表格) using the Feishu API.
Usage: python3 read_feishu_sheet.py <spreadsheet_token> <sheet_id> [range]
If sheet_id is omitted, reads the first sheet.
If range is omitted, reads the entire sheet.
"""
import sys
import json
import os
import subprocess
import re

def get_config():
    """Get feishu app credentials from gateway config file."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path) as f:
            config = json.load(f)
        feishu = config.get("channels", {}).get("feishu", {})
        accounts = feishu.get("accounts", {})
        account = accounts.get("default") or accounts.get("main") or {}
        app_id = account.get("appId", "")
        app_secret = account.get("appSecret", "")
        if app_id and app_secret:
            return app_id, app_secret
    except Exception:
        pass
    # Fallback: read from env or hardcoded demo credentials (update as needed)
    return os.environ.get("FEISHU_APP_ID", ""), os.environ.get("FEISHU_APP_SECRET", "")

def get_access_token(app_id, app_secret):
    """Get tenant access token from Feishu."""
    cmd = [
        "curl", "-s", "-X", "POST",
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"app_id": app_id, "app_secret": app_secret})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data.get("tenant_access_token", "")

def read_sheet(token, access_token, spreadsheet_token, sheet_id, range_str=None):
    """Read data from a Feishu sheet."""
    if range_str:
        range_param = f"{sheet_id}!{range_str}"
    else:
        range_param = sheet_id

    url = (
        f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets"
        f"/{spreadsheet_token}/values/{range_param}"
    )

    cmd = [
        "curl", "-s",
        "-H", f"Authorization: Bearer {access_token}",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    resp = json.loads(result.stdout)
    # Extract values from the nested valueRange structure
    if resp.get("code") == 0:
        value_range = resp.get("data", {}).get("valueRange", {})
        resp["data"]["values"] = value_range.get("values", [])
    return resp

def get_sheet_meta(token, access_token, spreadsheet_token):
    """Get sheet metadata to find sheet ID."""
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/query"
    cmd = [
        "curl", "-s",
        "-H", f"Authorization: Bearer {access_token}",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data

def format_value(v):
    if isinstance(v, dict):
        return v.get("formattedValue", str(v))
    if v is None:
        return ""
    return str(v)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 read_feishu_sheet.py <spreadsheet_token> [sheet_id] [range]")
        sys.exit(1)

    spreadsheet_token = sys.argv[1]
    sheet_id = sys.argv[2] if len(sys.argv) > 2 else None
    range_str = sys.argv[3] if len(sys.argv) > 3 else None

    app_id, app_secret = get_config()
    if not app_id or not app_secret:
        print("Error: Could not find Feishu app credentials in config.")
        sys.exit(1)

    access_token = get_access_token(app_id, app_secret)
    if not access_token:
        print("Error: Failed to get access token.")
        sys.exit(1)

    # If no sheet_id, get meta to find the first sheet
    if not sheet_id:
        meta = get_sheet_meta(None, access_token, spreadsheet_token)
        sheets = meta.get("data", {}).get("sheets", [])
        if not sheets:
            print("Error: No sheets found in spreadsheet.")
            sys.exit(1)
        sheet_id = sheets[0].get("sheet_id", "")
        print(f"(No sheet_id provided, using first sheet: {sheet_id})")

    data = read_sheet(None, access_token, spreadsheet_token, sheet_id, range_str)

    if data.get("code") != 0:
        print(f"Feishu API error: {data.get('msg')}")
        sys.exit(1)

    rows = data.get("data", {}).get("valueRange", {}).get("values", [])
    if not rows:
        print("(Sheet is empty)")
    else:
        # Print as markdown table
        for row in rows:
            formatted = [format_value(c) for c in row]
            print("\t".join(formatted))

if __name__ == "__main__":
    main()
