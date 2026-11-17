#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""淘宝商品列表抓取。首页"猜你喜欢"免登录即可渲染；搜索结果页需登录态才填充。

选择器已实跑核验（2026-08-06，见 references/sites.md）。

依赖: playwright（同 connect_chrome.py）
用法:
    python tb_scrape.py                      # 抓首页猜你喜欢（免登录）
    python tb_scrape.py --search "手机"        # 搜商品（需登录态才有数据）
    python tb_scrape.py --launch --csv tb.csv
    python tb_scrape.py --port 9223 --out t.json
"""
import argparse
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cn_browser import scrape

TB_HOME_JS = """() => [...document.querySelectorAll('.tb-pick-content-item')].map(el => ({
  nid: el.getAttribute('data-nid'),
  title: (el.querySelector('.info-wrapper-title-text') || el.querySelector('.info-wrapper-title') || {}).textContent?.trim(),
  price: (el.querySelector('.price-value') || {}).textContent?.trim(),
  url: 'https:' + (el.querySelector('a.item-link')?.getAttribute('href') || '')
}))"""

DEFAULT_HOME = "https://www.taobao.com"


def main():
    ap = argparse.ArgumentParser(description="淘宝商品列表抓取")
    ap.add_argument("--search", default=None, help="搜索关键词（需登录态才出数据）")
    ap.add_argument("--wait", default=".tb-pick-content-item", help="等待选择器")
    ap.add_argument("--port", type=int, default=9222, help="Chrome 远程调试端口")
    ap.add_argument("--launch", action="store_true", help="若 CDP 未开则启动独立 profile Chrome")
    ap.add_argument(
        "--user-data-dir",
        default=os.path.expanduser("~/.cn-browser-chrome-profile"),
        help="Chrome 用户数据目录（保存登录态）",
    )
    ap.add_argument("--out", default="tb_items.json", help="输出 JSON 路径")
    ap.add_argument("--csv", default=None, help="同时输出 CSV 路径")
    args = ap.parse_args()

    if args.search:
        url = "https://s.taobao.com/search?q=" + urllib.parse.quote(args.search, safe="")
        print("[淘宝] 提示：搜索页需复用登录态（--launch 或已登录 Chrome）才有数据；空骨架则说明未登录。")
    else:
        url = DEFAULT_HOME
        print("[淘宝] 提示：首页猜你喜欢免登录即可抓到真实商品卡。")

    scrape(
        url=url,
        js=TB_HOME_JS,
        wait=args.wait,
        port=args.port,
        launch=args.launch,
        user_data_dir=args.user_data_dir,
        out_json=args.out,
        out_csv=args.csv,
    )


if __name__ == "__main__":
    main()
