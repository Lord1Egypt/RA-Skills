#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
import urllib.request

BASE = "https://xn--dtr.tw"
DISPLAY_BASE = "https://呵.tw"


def request_json(url: str, method: str = "GET", payload: dict | None = None):
    data = None
    headers = {"User-Agent": "Little7-hotw-skill/1.0", "Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def cmd_shorten(args):
    q = urllib.parse.urlencode({k: v for k, v in {"url": args.url, "slug": args.slug}.items() if v})
    print(json.dumps(request_json(f"{BASE}/api/create?{q}"), ensure_ascii=False, indent=2))


def cmd_create_paste(args):
    if args.stdin:
        content = sys.stdin.read()
    else:
        content = args.content
    if not content:
        raise SystemExit("content required (use --content or --stdin)")
    payload = {"content": content}
    for key in ["title", "format", "summary", "parent_slug"]:
        value = getattr(args, key)
        if value:
            payload[key] = value
    if args.tags:
        payload["tags"] = args.tags
    print(json.dumps(request_json(f"{BASE}/api/paste/create", method="POST", payload=payload), ensure_ascii=False, indent=2))


def cmd_resolve(args):
    print(json.dumps(request_json(f"{BASE}/api/resolve/{urllib.parse.quote(args.slug)}"), ensure_ascii=False, indent=2))


def cmd_meta(args):
    print(json.dumps(request_json(f"{BASE}/api/meta/{urllib.parse.quote(args.slug)}"), ensure_ascii=False, indent=2))


def cmd_chain(args):
    print(json.dumps(request_json(f"{BASE}/api/chain/{urllib.parse.quote(args.slug)}"), ensure_ascii=False, indent=2))


def cmd_find(args):
    q = urllib.parse.urlencode({"tag": args.tag, "limit": args.limit})
    print(json.dumps(request_json(f"{BASE}/api/paste/find?{q}"), ensure_ascii=False, indent=2))


def cmd_qr(args):
    path = f"/qr/p/{args.slug}" if args.is_paste else f"/qr/{args.slug}"
    print(json.dumps({"qr_url": f"{DISPLAY_BASE}{path}"}, ensure_ascii=False, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description="Use 呵.tw for token-saving agent handoff")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("shorten")
    s.add_argument("url")
    s.add_argument("--slug")
    s.set_defaults(func=cmd_shorten)

    s = sub.add_parser("create-paste")
    s.add_argument("--content")
    s.add_argument("--stdin", action="store_true")
    s.add_argument("--title")
    s.add_argument("--format")
    s.add_argument("--summary")
    s.add_argument("--parent-slug", dest="parent_slug")
    s.add_argument("--tag", dest="tags", action="append")
    s.set_defaults(func=cmd_create_paste)

    s = sub.add_parser("resolve")
    s.add_argument("slug")
    s.set_defaults(func=cmd_resolve)

    s = sub.add_parser("meta")
    s.add_argument("slug")
    s.set_defaults(func=cmd_meta)

    s = sub.add_parser("chain")
    s.add_argument("slug")
    s.set_defaults(func=cmd_chain)

    s = sub.add_parser("find")
    s.add_argument("tag")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_find)

    s = sub.add_parser("qr")
    s.add_argument("slug")
    s.add_argument("--is-paste", action="store_true")
    s.set_defaults(func=cmd_qr)
    return p


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
