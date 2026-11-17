#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn-browser-automation 公共模块：连接本机已登录 Chrome 并提取/导出数据。

复用 connect_chrome.py 的底层函数（Chrome 发现、CDP 启动、端口探测），
供各站点抓取脚本（xhs_scrape.py / tb_scrape.py / bili_scrape.py）调用，避免重复代码。

核心卖点：connect_over_cdp 复用用户本机 Chrome 的登录态（cookie / 会话），不重复登录。
"""
import csv
import json
import os
import sys
import time

# 让本模块被站点脚本 import 时，也能找到同目录的 connect_chrome.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connect_chrome import (  # noqa: E402
    cdp_base,
    chrome_bin,
    port_open,
    launch_chrome,
    ensure_playwright,
)

DEFAULT_PORT = 9222
DEFAULT_USER_DATA_DIR = os.path.expanduser("~/.cn-browser-chrome-profile")


def scrape(
    url,
    js,
    wait=None,
    port=DEFAULT_PORT,
    launch=False,
    user_data_dir=DEFAULT_USER_DATA_DIR,
    out_json=None,
    out_csv=None,
):
    """连接本机 Chrome，导航到 url，执行 js 提取，导出 JSON / CSV。

    - 复用已登录上下文（browser.contexts[0]），不新建干净上下文。
    - js 须为返回可 JSON 序列化值的箭头函数字符串，如 "() => document.title"。
    - 返回提取到的数据（通常是 list[dict]）。
    """
    ensure_playwright()
    if not port_open(port):
        if launch:
            launch_chrome(port, user_data_dir)
        else:
            sys.exit(
                f"CDP 端口 {port} 未开启。请用 --launch 启动，或参考 references/setup.md 手动启动 Chrome。"
            )

    from playwright.sync_api import sync_playwright  # 延迟导入，便于在无依赖时给出友好提示

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        # 复用已存在的上下文（含登录态），不要新建干净上下文
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        if wait:
            if wait.replace(".", "", 1).isdigit():
                time.sleep(float(wait))
            else:
                try:
                    page.wait_for_selector(wait, timeout=30000)
                except Exception:
                    pass  # 选择器可能已变，继续执行而非直接失败

        data = page.evaluate(js)
        browser.close()

    if out_json:
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        n = len(data) if isinstance(data, list) else "?"
        print(f"[cn-browser] 已写出 JSON: {out_json}  (共 {n} 条)")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))

    if out_csv and isinstance(data, list):
        _write_csv(out_csv, data)
        print(f"[cn-browser] 已写出 CSV: {out_csv}")

    return data


def _write_csv(path, rows):
    if not rows:
        print("[cn-browser] 无数据，跳过 CSV。")
        return
    # 列 = 所有 dict 的 key 并集，保持首个出现的顺序
    cols = []
    for r in rows:
        if isinstance(r, dict):
            for k in r.keys():
                if k not in cols:
                    cols.append(k)
    if not cols:
        print("[cn-browser] 记录非 dict，无法写 CSV，跳过。")
        return
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            if isinstance(r, dict):
                w.writerow(r)


# 让 cdp_base 在 import 时也可直接用（部分脚本可能引用）
__all__ = ["scrape", "cdp_base", "chrome_bin", "port_open", "launch_chrome", "DEFAULT_PORT"]
