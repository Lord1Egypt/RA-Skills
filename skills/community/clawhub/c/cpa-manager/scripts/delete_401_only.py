#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def get_arg_or_env(value, env_name):
    return value or os.environ.get(env_name, "")


def headers(token):
    return {"Authorization": f"Bearer {token}"}


def extract_name(item):
    return item.get("name") or item.get("label") or item.get("account") or item.get("email") or item.get("id")


def main():
    ap = argparse.ArgumentParser(description="Delete only 401 accounts from exported JSON")
    ap.add_argument("--base-url")
    ap.add_argument("--token")
    ap.add_argument("--input", required=True)
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    base_url = get_arg_or_env(args.base_url, "CPA_BASE_URL")
    token = get_arg_or_env(args.token, "CPA_TOKEN")
    if not base_url or not token:
        print("Missing --base-url/CPA_BASE_URL or --token/CPA_TOKEN", file=sys.stderr)
        return 2

    items = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(items, list):
        print("Input JSON must be a list", file=sys.stderr)
        return 2

    names = [extract_name(x) for x in items]
    names = [x for x in names if x]
    print(f"about to delete 401 accounts: {len(names)}")
    if names[:10]:
        for s in names[:10]:
            print(f"  - {s}")
    if not args.yes:
        answer = input("Type DELETE to continue: ").strip()
        if answer != "DELETE":
            print("aborted")
            return 1

    ok = 0
    failed = []
    for name in names:
        url = f"{base_url.rstrip('/')}/v0/management/auth-files?name={urllib.parse.quote(name, safe='')}"
        req = urllib.request.Request(url, headers=headers(token), method="DELETE")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8", "ignore")
                data = json.loads(raw) if raw else {}
                if resp.status == 200 and isinstance(data, dict) and data.get("status") == "ok":
                    ok += 1
                else:
                    failed.append({"name": name, "status": resp.status, "body": raw[:300]})
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")
            failed.append({"name": name, "status": e.code, "body": body[:300]})
        except Exception as e:
            failed.append({"name": name, "status": None, "body": repr(e)[:300]})

    summary = {"requested": len(names), "deleted": ok, "failed": len(failed), "failures": failed[:20]}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 3


if __name__ == "__main__":
    raise SystemExit(main())
