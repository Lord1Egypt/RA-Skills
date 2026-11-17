#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链接净化：去除不影响跳转的追踪/上下文参数，只保留有效部分（Hard Rule 3）。

用法：
  python link_clean.py "https://weixin.sogou.com/link?url=xxx&type=2&query=%E8%85%BE...&token=null"
  python link_clean.py URL1 URL2 ...          # 多条
  python link_clean.py --stdin < urls.txt     # 从stdin逐行读

规则（全部经 2026-08 实测验证）：
1. 搜狗微信链接：截断到 url=<签名串> 为止——type/query/token 不参与跳转
   （跳转由签名串服务端解析；query 还泄漏检索动作，属元信息）
   ⚠️ 注意：截断后的搜狗链仍是双层临时签名（微信 src=11 签名数小时过期），
   只可用于核验期内容读取，不得写入交付物（见 SKILL.md Hard Rule 4/6）
2. 通用追踪参数：utm_*、from、spm、share_token、isappinstalled、src、source_id 等整组删除
3. token=null 等空值参数一律删除
4. 其余参数保留（可能参与跳转，不赌）
"""
import argparse
import json
import sys
import urllib.parse

TRACK_KEYS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "from", "spm", "share_token", "isappinstalled", "src", "source_id",
    "share_medium", "chksm", "scene", "subscene", "clicktime",
    "sessionid", "enterid", "pos", "abtest", "x5referer",
}

EMPTY_VALUES = {"", "null", "none", "0"}


def clean(url: str) -> str:
    url = url.strip().strip("<>").rstrip('.,;，。；)')
    p = urllib.parse.urlsplit(url)

    # 搜狗微信特例：只保留 url= 签名串
    if "sogou.com/link" in (p.netloc + p.path):
        m = urllib.parse.parse_qs(p.query, keep_blank_values=True)
        if "url" in m:
            return f"{p.scheme}://{p.netloc}{p.path}?url={m['url'][0]}"
        return url

    if not p.query:
        return url

    kept = []
    for kv in p.query.split("&"):
        if not kv or "=" not in kv:
            continue
        k, _, v = kv.partition("=")
        if k.lower() in TRACK_KEYS:
            continue
        if v.lower() in EMPTY_VALUES:
            continue
        kept.append(kv)

    query = "&".join(kept)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, query, p.fragment))


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean URLs: keep only jump-relevant parts")
    ap.add_argument("urls", nargs="*", help="待净化 URL")
    ap.add_argument("--stdin", action="store_true", help="从 stdin 逐行读取")
    a = ap.parse_args()

    urls = a.urls if a.urls else (sys.stdin.read().splitlines() if a.stdin else [])
    out = []
    for u in urls:
        u = u.strip()
        if not u or u.startswith("#"):
            continue
        c = clean(u)
        out.append({"original": u, "cleaned": c, "changed": u != c})

    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
