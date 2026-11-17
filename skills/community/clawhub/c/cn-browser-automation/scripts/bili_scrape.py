#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B站排行榜抓取（免登录，DOM 极稳定，无 CSS-Module 哈希类）。

选择器已实跑核验（2026-08-06，见 references/sites.md）：排行榜 100 条一屏全渲染。

依赖: playwright（同 connect_chrome.py）
用法:
    python bili_scrape.py                         # 抓全站排行榜
    python bili_scrape.py --url "<某分区排行榜>"   # 抓指定分区
    python bili_scrape.py --launch --csv bili.csv
    python bili_scrape.py --port 9223 --out b.json
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cn_browser import scrape

BILI_JS = """() => [...document.querySelectorAll('li.rank-item')].map(el => {
  const a = el.querySelector('a.title');
  const cov = el.querySelector('img.cover');
  // 播放/弹幕在 .detail 内的 .data-box 里；第一个 .data-box 是 UP主(.up-name)，需跳过它取真正的播放量
  const boxes = [...el.querySelectorAll('.detail .data-box')].filter(b => !b.classList.contains('up-name'));
  const play = boxes[0] ? boxes[0].textContent.trim() : null;
  const danmaku = boxes[1] ? boxes[1].textContent.trim() : null;
  return {
    rank: (el.querySelector('i.num span') || {}).textContent?.trim() || el.getAttribute('data-rank'),
    title: a?.textContent?.trim(),
    url: 'https:' + (a?.getAttribute('href') || ''),
    up: (el.querySelector('.up-name') || {}).textContent?.trim(),
    cover: cov?.getAttribute('src') || cov?.getAttribute('data-src'),
    play: play,
    danmaku: danmaku
  };
})"""

DEFAULT_RANK = "https://www.bilibili.com/v/popular/rank/all"


def main():
    ap = argparse.ArgumentParser(description="B站排行榜抓取（免登录）")
    ap.add_argument("--url", default=DEFAULT_RANK, help="排行榜 URL，默认全站排行榜")
    ap.add_argument("--wait", default="li.rank-item", help="等待选择器")
    ap.add_argument("--port", type=int, default=9222, help="Chrome 远程调试端口")
    ap.add_argument("--launch", action="store_true", help="若 CDP 未开则启动独立 profile Chrome")
    ap.add_argument(
        "--user-data-dir",
        default=os.path.expanduser("~/.cn-browser-chrome-profile"),
        help="Chrome 用户数据目录（保存登录态）",
    )
    ap.add_argument("--out", default="bili_rank.json", help="输出 JSON 路径")
    ap.add_argument("--csv", default=None, help="同时输出 CSV 路径")
    args = ap.parse_args()

    scrape(
        url=args.url,
        js=BILI_JS,
        wait=args.wait,
        port=args.port,
        launch=args.launch,
        user_data_dir=args.user_data_dir,
        out_json=args.out,
        out_csv=args.csv,
    )


if __name__ == "__main__":
    main()
