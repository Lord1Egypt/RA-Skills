#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
import urllib.request

DEFAULT_BASE = "http://127.0.0.1:9377"


def request(base, method, path, params=None, body=None, headers=None, timeout=40):
    url = base.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {"ok": True}


def add_common(parser):
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--timeout", type=int, default=40)


def main():
    ap = argparse.ArgumentParser(description="Minimal camofox-browser REST helper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("health")
    add_common(p)

    p = sub.add_parser("open")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--session", default="default")
    p.add_argument("--url", required=True)

    p = sub.add_parser("list")
    add_common(p)
    p.add_argument("--user", required=True)

    p = sub.add_parser("wait")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--wait-for-network", action="store_true")
    p.add_argument("--ms", type=int, default=10000)

    p = sub.add_parser("snapshot")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--format", default="text")
    p.add_argument("--offset", type=int, default=0)

    p = sub.add_parser("click")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--ref")
    p.add_argument("--selector")

    p = sub.add_parser("type")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--ref")
    p.add_argument("--selector")
    p.add_argument("--text", required=True)
    p.add_argument("--mode", choices=["fill", "keyboard"], default="fill")
    p.add_argument("--delay", type=int, default=30)
    p.add_argument("--submit", action="store_true")

    p = sub.add_parser("press")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--key", required=True)

    p = sub.add_parser("scroll")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--direction", default="down")
    p.add_argument("--amount", type=int, default=500)

    p = sub.add_parser("navigate")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--url", required=True)

    p = sub.add_parser("evaluate")
    add_common(p)
    p.add_argument("--user", required=True)
    p.add_argument("--tab", required=True)
    p.add_argument("--expression", required=True)

    args = ap.parse_args()

    try:
        if args.cmd == "health":
            out = request(args.base, "GET", "/health", timeout=args.timeout)
        elif args.cmd == "open":
            out = request(args.base, "POST", "/tabs", body={"userId": args.user, "sessionKey": args.session, "url": args.url}, timeout=args.timeout)
        elif args.cmd == "list":
            out = request(args.base, "GET", "/tabs", params={"userId": args.user}, timeout=args.timeout)
        elif args.cmd == "wait":
            out = request(args.base, "POST", f"/tabs/{args.tab}/wait", body={"userId": args.user, "timeout": args.ms, "waitForNetwork": args.wait_for_network}, timeout=args.timeout)
        elif args.cmd == "snapshot":
            out = request(args.base, "GET", f"/tabs/{args.tab}/snapshot", params={"userId": args.user, "format": args.format, "offset": args.offset}, timeout=args.timeout)
        elif args.cmd == "click":
            body = {"userId": args.user}
            if args.ref:
                body["ref"] = args.ref
            if args.selector:
                body["selector"] = args.selector
            out = request(args.base, "POST", f"/tabs/{args.tab}/click", body=body, timeout=args.timeout)
        elif args.cmd == "type":
            body = {
                "userId": args.user,
                "text": args.text,
                "mode": args.mode,
                "delay": args.delay,
                "submit": args.submit,
            }
            if args.ref:
                body["ref"] = args.ref
            if args.selector:
                body["selector"] = args.selector
            out = request(args.base, "POST", f"/tabs/{args.tab}/type", body=body, timeout=args.timeout)
        elif args.cmd == "press":
            out = request(args.base, "POST", f"/tabs/{args.tab}/press", body={"userId": args.user, "key": args.key}, timeout=args.timeout)
        elif args.cmd == "scroll":
            out = request(args.base, "POST", f"/tabs/{args.tab}/scroll", body={"userId": args.user, "direction": args.direction, "amount": args.amount}, timeout=args.timeout)
        elif args.cmd == "navigate":
            out = request(args.base, "POST", f"/tabs/{args.tab}/navigate", body={"userId": args.user, "url": args.url}, timeout=args.timeout)
        elif args.cmd == "evaluate":
            out = request(args.base, "POST", f"/tabs/{args.tab}/evaluate", body={"userId": args.user, "expression": args.expression}, timeout=args.timeout)
        else:
            raise ValueError(f"unknown command: {args.cmd}")
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
