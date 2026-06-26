#!/usr/bin/env python3
"""
Accounting skill for OpenClaw.
智能记账助手 — 记账、查账、查询账本/账户/分类/经手人/关联企业。
"""

import sys
import json
import os
import urllib.request
import urllib.parse
import urllib.error
sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_BASE = "https://api.caiwu888.cn"

def get_config():
    token = os.getenv("ACCOUNTING_API_TOKEN")
    if not token:
        print("Error: ACCOUNTING_API_TOKEN must be set in environment.", file=sys.stderr)
        sys.exit(1)
    return DEFAULT_BASE, token

def request_post(base, token, path, body):
    url = f"{base}{path}"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={
            "Authorization": token,
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {"error": "http_error", "status_code": e.code, "body": body_text}
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

def request_get(base, token, path, params=None):
    url = f"{base}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url, method="GET",
        headers={"Authorization": token},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {"error": "http_error", "status_code": e.code, "body": body_text}
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

def unwrap(result):
    if isinstance(result, dict) and "error" in result:
        return result
    if isinstance(result, dict) and result.get("code") is not None and result.get("code") != 0:
        return {"error": "api_error", "code": result.get("code"), "message": result.get("msg", result.get("message", ""))}
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result

# ── 业务命令 ──

def cmd_add(base, token, req):
    if not req.get("ledgerName"):
        return {"error": "missing_param", "message": "ledgerName is required"}
    if not req.get("amount") or req["amount"] <= 0:
        return {"error": "invalid_param", "message": "amount must be > 0"}
    if not req.get("transactionType"):
        return {"error": "missing_param", "message": "transactionType is required (SHOURU/ZHICHU/YINGSHOU/YINGFU)"}
    tt = req["transactionType"].upper()
    if tt in ("YINGSHOU", "YINGFU") and not req.get("dueDate"):
        return {"error": "missing_param", "message": f"dueDate is required when transactionType={tt}"}
    return unwrap(request_post(base, token, "/agent/accounting/add", req))

def cmd_query(base, token, req):
    if not req.get("ledgerName"):
        return {"error": "missing_param", "message": "ledgerName is required"}
    return unwrap(request_post(base, token, "/agent/accounting/query", req))

def cmd_ledgers(base, token):
    return unwrap(request_get(base, token, "/agent/accounting/ledgers"))

def cmd_accounts(base, token, req):
    name = req.get("ledgerName", "") if req else ""
    params = {"ledgerName": name} if name else None
    return unwrap(request_get(base, token, "/agent/accounting/accounts", params))

def cmd_categories(base, token, req):
    t = (req.get("type", "") if req else "")
    if not t:
        return {"error": "missing_param", "message": "type is required (SHOURU/ZHICHU/YINGSHOU/YINGFU or 收入/支出/应收/应付)"}
    return unwrap(request_get(base, token, "/agent/accounting/categories", {"type": t}))

def cmd_handlers(base, token):
    return unwrap(request_get(base, token, "/agent/accounting/handlers"))

def cmd_companies(base, token):
    return unwrap(request_get(base, token, "/agent/accounting/companies"))

# ── 入口 ──

COMMANDS = {
    "add":        {"fn": cmd_add,        "need_body": True,  "desc": "记账（新增交易）"},
    "query":      {"fn": cmd_query,      "need_body": True,  "desc": "查账（查询流水）"},
    "ledgers":    {"fn": cmd_ledgers,    "need_body": False, "desc": "查账本列表"},
    "accounts":   {"fn": cmd_accounts,   "need_body": True,  "desc": "查记账账户"},
    "categories": {"fn": cmd_categories, "need_body": True,  "desc": "查收支分类"},
    "handlers":   {"fn": cmd_handlers,   "need_body": False, "desc": "查经手人"},
    "companies":  {"fn": cmd_companies,  "need_body": False, "desc": "查关联企业"},
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        lines = ["Usage: accounting.py <command> [json_body]\n", "Commands:"]
        for k, v in COMMANDS.items():
            body_hint = " '<json>'" if v["need_body"] else ""
            lines.append(f"  {k:<12}{body_hint:<12} # {v['desc']}")
        print("\n".join(lines), file=sys.stderr)
        sys.exit(1)

    base, token = get_config()
    cmd = sys.argv[1].lower()

    if cmd not in COMMANDS:
        print(f"Error: unknown command '{cmd}'. Available: {', '.join(COMMANDS)}", file=sys.stderr)
        sys.exit(1)

    spec = COMMANDS[cmd]
    req = None

    if spec["need_body"]:
        if len(sys.argv) < 3:
            if cmd in ("accounts", "categories"):
                pass
            else:
                print(f"Error: JSON body is required for '{cmd}'.", file=sys.stderr)
                sys.exit(1)
        if len(sys.argv) >= 3:
            try:
                raw = sys.argv[2]
                # Handle single-quoted JSON from shell
                if raw.startswith("'") and raw.endswith("'"):
                    raw = raw[1:-1]
                req = json.loads(raw)
            except json.JSONDecodeError as e:
                # Try reading from file if JSON parsing fails
                try:
                    with open(sys.argv[2], 'r', encoding='utf-8') as f:
                        req = json.load(f)
                except:
                    print(f"JSON parse error: {e}", file=sys.stderr)
                    sys.exit(1)

    if spec["need_body"]:
        result = spec["fn"](base, token, req)
    else:
        result = spec["fn"](base, token)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
