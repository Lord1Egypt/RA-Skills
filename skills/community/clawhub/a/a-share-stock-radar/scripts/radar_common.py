#!/usr/bin/env python3
"""
radar_common —— 股票雷达公共库（stdlib only）

提供：工作区定位、形态常量、交易日志读写、健壮 HTTP（带 Referer + 镜像轮换 + 退避重试）。
被 trading-desk/scripts/* 复用。
"""
import json
import os
import time
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# 4 大短线形态（playbook）+ 兜底
PATTERNS = ["N字爆发", "平台突破VCP", "一阳穿三阴", "竞价异动", "其他"]

EM_HOSTS = (
    "push2.eastmoney.com",
    "1.push2.eastmoney.com",
    "7.push2.eastmoney.com",
    "82.push2.eastmoney.com",
    "push2delay.eastmoney.com",
)


def ws_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", ".."))


def journal_path():
    return os.path.join(ws_root(), "trading", "journal", "trades.json")


def load_journal():
    p = journal_path()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_journal(rows):
    p = journal_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def http_get(url, referer=None, timeout=12, retries=3, encoding="utf-8"):
    """GET with browser UA + optional Referer + backoff retries."""
    last = None
    for attempt in range(retries):
        try:
            headers = {"User-Agent": UA, "Accept": "*/*"}
            if referer:
                headers["Referer"] = referer
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode(encoding, "ignore")
        except Exception as e:
            last = e
            time.sleep(0.5 * (attempt + 1))
    raise last


def http_json(url, referer=None, timeout=12, retries=3):
    return json.loads(http_get(url, referer=referer, timeout=timeout, retries=retries))


def em_json(path_query, timeout=12):
    """Eastmoney push2 JSON with mirror-host rotation."""
    last = None
    for host in EM_HOSTS:
        try:
            return http_json("https://{}/{}".format(host, path_query),
                             referer="https://quote.eastmoney.com/", timeout=timeout, retries=2)
        except Exception as e:
            last = e
    raise last


def tencent_quote_symbol(code6):
    return ("sh" if code6.startswith("6") else "sz") + code6


def sina_symbol(code6, prefix=True):
    return ("sh" if code6.startswith("6") else "sz") + code6
