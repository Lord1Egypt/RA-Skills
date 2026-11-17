#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""context-token-budget — Token/上下文预算守护（fail-closed 门禁）。
痛点：AI 上下文超限/积分烧光。理论根基：LGD 三律·有门禁。Usage:
  python budget.py <file-or-text> [--limit N] [--json]"""
import argparse, json, math, os, sys, hashlib

# 简易估算：英文 ~4 chars/token，中文 ~1.5 chars/token，代码 ~3.5 chars/token
def estimate_tokens(text):
    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other = len(text) - cjk
    return int(cjk / 1.5 + other / 4)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="file path or text")
    p.add_argument("--limit", type=int, default=8000, help="token budget")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if os.path.isfile(a.input):
        text = open(a.input, encoding="utf-8", errors="replace").read()
    else:
        text = a.input
    tokens = estimate_tokens(text)
    used_pct = round(tokens / a.limit * 100, 1)
    verdict = "PASS" if tokens <= a.limit else "FAIL"
    sha = hashlib.sha256(text.encode()).hexdigest()[:8]
    res = {"tokens": tokens, "limit": a.limit, "used_pct": used_pct,
           "verdict": verdict, "sha256_8": sha,
           "fail_closed": True, "advice": "trim context or raise --limit" if verdict == "FAIL" else "within budget"}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"tokens={tokens} limit={a.limit} used={used_pct}% {verdict} (sha {sha})")
        print("advice:", res["advice"])
    return 0 if verdict == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
