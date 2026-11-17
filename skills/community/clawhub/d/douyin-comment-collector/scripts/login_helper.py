#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抖音 Cookie 获取助手 —— 免开发者工具，普通人也能用。

为什么需要它
------------
抓评论有两条路：
1. 无头浏览器「游客态」：免登录，但抖音会弹「评论墙」，通常只能拿到前 ~14-20 条。
2. 「登录态」抓取：注入真实 cookie，通常能越过评论墙拿到更多/全部评论。

登录态需要 cookie，但让普通人去按 F12 打开控制台、手动复制那串又长又臭的
cookie 字符串，既不友好又极易复制不全。本助手改用「看得见」的真实浏览器：
你用手机抖音扫码（或账号密码）像平时一样登录，登录成功后它自动把 cookie
存成文件，后续抓取脚本直接读取 —— 全程零控制台操作。

用法
----
    python login_helper.py                      # 默认登 creator.douyin.com，存 douyin_cookie.json + .txt
    python login_helper.py --output my.json    # 指定保存路径
    python login_helper.py --domain www.douyin.com   # 仅消费者端登录（一般用不到）

- creator.douyin.com（默认）：登录态 cookie 落在 .douyin.com 通配域，
  对浏览器抓取(www.douyin.com)与纯 HTTP 创作者接口都生效 —— 不要用 www.douyin.com/login，
  实测消费者端 passport 会直出 JSON 错误且登录态域不匹配。
- 若只想给纯 HTTP 创作者接口用，仍可用 --domain creator.douyin.com（默认即此）。

依赖：playwright（安装器自带：python install.py --with-browser）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # 未装浏览器底座时给出清晰提示，而非堆栈
    sys.stderr.write(
        "缺少 playwright：无法启动登录浏览器。\n"
        "请先安装浏览器底座：python install.py --with-browser\n"
    )
    sys.exit(2)

_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT = os.path.join(_HERE, "douyin_cookie.json")

# 这些 cookie 之一出现即视为已登录（覆盖抖音主站常见登录态字段）
_LOGIN_COOKIES = ("sessionid_ss", "sid_guard", "sid_tt", "sessionid", "uid_tt")


def _is_logged_in(cookies: list) -> bool:
    names = {c.get("name") for c in cookies}
    return any(n in names for n in _LOGIN_COOKIES)


def run(domain: str, output: str, timeout: int = 180) -> int:
    url = f"https://{domain}/"
    print("=" * 60)
    print("        抖音 Cookie 获取助手（免开发者工具）")
    print("=" * 60)
    print("  步骤：")
    print("    1) 浏览器会打开抖音登录页（看得见，可操作）")
    print("    2) 用手机抖音「扫一扫」或账号密码正常登录（和平时一样）")
    print("    3) 登录成功后会自动保存 cookie，无需打开任何控制台")
    print("=" * 60)
    print(f"\n正在打开 {url} …（请在本机弹出的浏览器窗口中登录）\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 必须可见，否则无法扫码/输密码
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        deadline = time.time() + timeout
        logged = False
        while time.time() < deadline:
            cookies = context.cookies()
            if _is_logged_in(cookies):
                logged = True
                break
            remain = int(deadline - time.time())
            print(f"\r  等待登录中…（还剩 {remain}s，登录后自动保存）", end="", flush=True)
            time.sleep(2)

        print()
        if not logged:
            print("⚠️ 等待超时仍未检测到登录态，未保存 cookie。请重试并确保登录成功。")
            browser.close()
            return 1

        cookies = context.cookies()
        out_dir = os.path.dirname(os.path.abspath(output))
        os.makedirs(out_dir, exist_ok=True)
        # ① JSON 列表（playwright 注入格式，浏览器抓取 --cookie-file 自动读取）
        with open(output, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        # ② 字符串形态（可直接喂 HTTP 模式 --cookie）
        txt_path = os.path.splitext(output)[0] + ".txt"
        cookie_str = "; ".join(f"{c.get('name')}={c.get('value')}" for c in cookies if c.get("name"))
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(cookie_str)
        browser.close()

    print(f"✅ 已保存 {len(cookies)} 条 cookie：")
    print(f"   - JSON ：{output}（浏览器抓取 --cookie-file 自动读取）")
    print(f"   - 字符串：{txt_path}（可直接喂 HTTP 模式：--cookie \"$(cat {txt_path})\"）")
    return 0


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="login_helper",
        description="抖音 Cookie 获取助手（免开发者工具：扫码/账号密码登录后自动存 cookie）",
    )
    p.add_argument(
        "--domain", default="creator.douyin.com",
        help="登录域名：creator.douyin.com(默认,登录态对浏览器/HTTP均生效) / "
             "www.douyin.com(消费者端,一般用不到)",
    )
    p.add_argument("--output", default=DEFAULT_OUTPUT, help=f"cookie 保存路径（默认 {DEFAULT_OUTPUT}）")
    p.add_argument("--timeout", type=int, default=180, help="等待登录的秒数（默认180）")
    return p


def main(argv=None) -> int:
    args = build_argparser().parse_args(argv)
    return run(args.domain, args.output, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
