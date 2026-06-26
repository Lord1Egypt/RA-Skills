#!/usr/bin/env python3
"""
AlphaShop Text API — unified CLI for 3 text processing endpoints.

Commands:
  translate           大模型文本翻译
  selling-point       生成商品多语言卖点
  title               生成商品多语言标题

Auth: env ALPHASHOP_ACCESS_KEY / ALPHASHOP_SECRET_KEY (JWT HS256).
"""
import sys
import os
import json
import time
import argparse
import requests
import jwt

BASE_URL = "https://api.alphashop.cn"


# ── Auth ─────────────────────────────────────────────────────────────────────

def get_token():
    ak = os.environ.get("ALPHASHOP_ACCESS_KEY", "").strip()
    sk = os.environ.get("ALPHASHOP_SECRET_KEY", "").strip()
    if not ak or not sk:
        print("Error: Set ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY env vars.", file=sys.stderr)
        sys.exit(1)
    now = int(time.time())
    token = jwt.encode({"iss": ak, "exp": now + 1800, "nbf": now - 5}, sk, algorithm="HS256", headers={"alg": "HS256"})
    return token if isinstance(token, str) else token.decode("utf-8")


def call_api(path: str, body: dict) -> dict:
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {get_token()}"}
    try:
        r = requests.post(url, json=body, headers=headers, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        try:
            print(f"Response: {r.text}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_translate(args):
    body = {
        "sourceLanguage": args.source_lang,
        "targetLanguage": args.target_lang,
        "sourceTextList": args.texts,
    }
    print(json.dumps(call_api("/ai.text.translate/1.0", body), ensure_ascii=False, indent=2))


def cmd_selling_point(args):
    body = {
        "productName": args.product_name,
        "productCategory": args.category,
        "targetLanguage": args.target_lang,
    }
    if args.keywords:
        body["productKeyword"] = args.keywords
    if args.spec:
        body["itemSpec"] = args.spec
    if args.description:
        body["productDescription"] = args.description
    print(json.dumps(call_api("/ai.text.generateMultiLanguageSellingPoint/1.0", body), ensure_ascii=False, indent=2))


def cmd_title(args):
    body = {
        "productName": args.product_name,
        "productCategory": args.category,
        "targetLanguage": args.target_lang,
        "generateCounts": args.count,
    }
    if args.keywords:
        body["productKeyword"] = args.keywords
    if args.spec:
        body["itemSpec"] = args.spec
    if args.description:
        body["productDescription"] = args.description
    print(json.dumps(call_api("/ai.text.generateMultiLanguageTitle/1.0", body), ensure_ascii=False, indent=2))


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AlphaShop Text API CLI")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    # -- translate --
    p = sub.add_parser("translate", help="大模型文本翻译")
    p.add_argument("--source-lang", required=True, help="源语种 ISO code（未知可传 auto）")
    p.add_argument("--target-lang", required=True, help="目标语种 ISO code")
    p.add_argument("--texts", nargs="+", required=True, help="待翻译文本列表（最多50个）")
    p.set_defaults(func=cmd_translate)

    # -- selling-point --
    p = sub.add_parser("selling-point", help="生成商品多语言卖点")
    p.add_argument("--product-name", required=True, help="商品名称（≤500字符）")
    p.add_argument("--category", required=True, help="商品类目")
    p.add_argument("--target-lang", required=True, help="目标语言代码")
    p.add_argument("--keywords", nargs="+", help="SEO关键词或卖点词")
    p.add_argument("--spec", help="商品属性（键1: 值1, 键2: 值2）")
    p.add_argument("--description", help="商品详细描述")
    p.set_defaults(func=cmd_selling_point)

    # -- title --
    p = sub.add_parser("title", help="生成商品多语言标题")
    p.add_argument("--product-name", required=True, help="商品名称（10~500字符）")
    p.add_argument("--category", required=True, help="商品类目")
    p.add_argument("--target-lang", required=True, help="目标语言代码")
    p.add_argument("--count", type=int, default=1, help="生成数量 1-6（默认1）")
    p.add_argument("--keywords", nargs="+", help="SEO关键词或卖点词")
    p.add_argument("--spec", help="商品属性")
    p.add_argument("--description", help="商品详细描述")
    p.set_defaults(func=cmd_title)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
