#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书笔记列表抓取（探索页 / 搜索页），复用本机 Chrome 登录态。

选择器已实跑核验（2026-08-06，见 references/sites.md）。

依赖: playwright（同 connect_chrome.py）
用法:
    python xhs_scrape.py                      # 抓探索页笔记列表
    python xhs_scrape.py --search "护肤"       # 抓搜索结果（需登录态更佳）
    python xhs_scrape.py --url "<某个笔记列表页>"
    python xhs_scrape.py --launch --csv xhs.csv   # 启动独立 profile 并导出 CSV
    python xhs_scrape.py --port 9223 --out x.json
"""
import argparse
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cn_browser import scrape

XHS_JS = """() => [...document.querySelectorAll('.note-item')].map(el => ({
  noteId: el.getAttribute('data-note-id'),
  title: (el.querySelector('.title') || {}).textContent?.trim(),
  author: (el.querySelector('.name') || {}).textContent?.trim(),
  likeCount: (el.querySelector('.count') || {}).textContent?.trim(),
  cover: (el.querySelector('.cover img') || {}).getAttribute?.('src'),
  url: 'https://www.xiaohongshu.com' + (el.querySelector('a.cover')?.getAttribute('href') || '')
}))"""

DEFAULT_EXPLORE = "https://www.xiaohongshu.com/explore"


def main():
    ap = argparse.ArgumentParser(description="小红书笔记列表抓取（需登录态更佳）")
    ap.add_argument("--url", default=None, help="直接指定页面 URL（覆盖 --search）")
    ap.add_argument("--search", default=None, help="搜索关键词，自动拼接搜索页 URL")
    ap.add_argument("--wait", default=".note-item", help="等待选择器，默认 .note-item")
    ap.add_argument("--port", type=int, default=9222, help="Chrome 远程调试端口")
    ap.add_argument("--launch", action="store_true", help="若 CDP 未开则启动独立 profile Chrome")
    ap.add_argument(
        "--user-data-dir",
        default=os.path.expanduser("~/.cn-browser-chrome-profile"),
        help="Chrome 用户数据目录（保存登录态）",
    )
    ap.add_argument("--out", default="xhs_notes.json", help="输出 JSON 路径")
    ap.add_argument("--csv", default=None, help="同时输出 CSV 路径")
    args = ap.parse_args()

    if args.url:
        url = args.url
    elif args.search:
        url = "https://www.xiaohongshu.com/search_result?keyword=" + urllib.parse.quote(
            args.search, safe=""
        )
    else:
        url = DEFAULT_EXPLORE

    scrape(
        url=url,
        js=XHS_JS,
        wait=args.wait,
        port=args.port,
        launch=args.launch,
        user_data_dir=args.user_data_dir,
        out_json=args.out,
        out_csv=args.csv,
    )


if __name__ == "__main__":
    main()
