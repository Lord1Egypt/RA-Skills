#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""连接本机已登录 Chrome（CDP），导航到目标页并可选执行 JS 提取数据。

核心卖点：复用用户本机 Chrome 的登录态（cookie / 会话），不需要重新登录。

依赖:
    pip install playwright -i https://mirrors.tencent.com/pypi/simple/
    # connect_over_cdp 不需要下载 chromium，但保险起见可跑: playwright install chromium

用法:
    python connect_chrome.py https://www.xiaohongshu.com
    python connect_chrome.py "https://item.taobao.com/item.htm?id=xxx" \
        --js "() => ({title: document.title, notes: document.querySelectorAll('.note-item').length})" \
        --wait ".note-item" --out out.json
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request

DEFAULT_PORT = 9222


def cdp_base(port: int) -> str:
    return f"http://127.0.0.1:{port}"


def chrome_bin() -> str | None:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\EDY\AppData\Local\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium")


def port_open(port: int) -> bool:
    try:
        urllib.request.urlopen(f"{cdp_base(port)}/json/version", timeout=1)
        return True
    except Exception:
        return False


def launch_chrome(port: int, user_data_dir: str) -> None:
    bin_path = chrome_bin()
    if not bin_path:
        sys.exit("未找到 Chrome，请先安装 Google Chrome。")
    os.makedirs(user_data_dir, exist_ok=True)
    cmd = [
        bin_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    subprocess.Popen(cmd)
    for _ in range(40):
        if port_open(port):
            return
        time.sleep(0.5)
    sys.exit("Chrome 启动超时，请检查是否被占用或路径错误。")


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        sys.exit(
            "缺少依赖 playwright。请运行:\n"
            "  pip install playwright -i https://mirrors.tencent.com/pypi/simple/\n"
            "（connect_over_cdp 不需要下载 chromium，但保险起见可再跑: playwright install chromium）"
        )


def main() -> None:
    ap = argparse.ArgumentParser(description="连接本机已登录 Chrome 并提取页面数据")
    ap.add_argument("url", help="目标页面 URL")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT, help="Chrome 远程调试端口")
    ap.add_argument(
        "--js",
        help='页面内执行的 JS 表达式，须返回可 JSON 序列化的值，如 "() => document.title"',
    )
    ap.add_argument("--wait", default=None, help="等待的选择器(如 '.note-item')或秒数(如 '5')")
    ap.add_argument("--out", default=None, help="输出 JSON 文件路径，默认打印到 stdout")
    ap.add_argument("--launch", action="store_true", help="若 CDP 端口未开，尝试启动本机 Chrome")
    ap.add_argument(
        "--user-data-dir",
        default=os.path.expanduser("~/.cn-browser-chrome-profile"),
        help="Chrome 用户数据目录（保存登录态），默认 ~/.cn-browser-chrome-profile",
    )
    args = ap.parse_args()

    if not port_open(args.port):
        if args.launch:
            launch_chrome(args.port, args.user_data_dir)
        else:
            sys.exit(
                f"CDP 端口 {args.port} 未开启。请用 --launch 启动，或参考 references/setup.md 手动启动 Chrome。"
            )

    sync_playwright = ensure_playwright()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{args.port}")
        # 复用已存在的上下文（含登录态），不要新建干净上下文
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=60000)

        if args.wait:
            if args.wait.replace(".", "", 1).isdigit():
                time.sleep(float(args.wait))
            else:
                try:
                    page.wait_for_selector(args.wait, timeout=30000)
                except Exception:
                    pass  # 选择器可能变了，继续执行而非直接失败

        if args.js:
            result = page.evaluate(args.js)
        else:
            result = {"title": page.title(), "url": page.url}

        browser.close()

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"已写出: {args.out}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
