#!/usr/bin/env python3
"""抖音爆款爬虫 - Python 版本

支持三种调用方式：
  1) nl     —— 自然语言一句话直接触发：python scraper.py nl "搜索一下海鲜视频"
  2) search —— 关键词搜索：             python scraper.py search --keyword 海鲜 --limit 10
  3) hot    —— 抖音热榜：               python scraper.py hot --limit 20

抓取实现：
  - 优先用 Playwright 真实访问 https://www.douyin.com/search/<keyword>
  - DOM 解析失败 / Playwright 不可用 / 被反爬 → 回退到本地演示数据，并在每条上标 mock=true
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

try:
    from playwright.sync_api import sync_playwright  # type: ignore
except Exception:  # pragma: no cover - optional dep
    sync_playwright = None  # type: ignore


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

@dataclass
class VideoData:
    title: str = ""
    description: str = ""
    author: str = ""
    play_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    url: str = ""
    tags: list[str] = field(default_factory=list)
    publish_time: str = ""
    mock: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d["tags"] = list(self.tags or [])
        return d


# ---------------------------------------------------------------------------
# 自然语言关键词提取
# ---------------------------------------------------------------------------

# 搜索动作词（前缀，倾向出现在句首）
ACTION_WORDS = [
    "搜索一下", "搜一下", "搜索", "搜一搜", "搜",
    "帮我搜", "帮我找", "帮我看一下", "帮我看看", "帮我",
    "找一下", "找一找", "找些", "找一些", "找",
    "看一下", "看一看", "看看", "看",
    "查一下", "查一查", "查",
    "来一些", "来点", "来",
    "给我看看", "给我",
]

# 平台 / 内容类型 / 修饰尾词
NOISE_TOKENS = [
    "抖音上的", "抖音里的", "抖音上", "抖音里", "抖音",
    "相关的", "相关", "之类的", "之类", "等等", "等",
    "的视频文案", "视频文案",
    "图文笔记", "图文", "笔记",
    "视频", "短视频",
    "文案",
    "内容",
    "爆款",
    "热门",
    "最近的", "最近",
    "一些",
]

HOT_BOARD_HINTS = ["热榜", "热门榜", "热门排行", "排行榜"]


def normalize(text: str) -> str:
    text = text.strip()
    # 去掉左右成对的引号 / 书名号 / 中文句末标点
    text = re.sub(r"[「」『』《》【】\[\]\"'`]+", "", text)
    text = re.sub(r"[，,。.!！?？\s]+$", "", text)
    return text.strip()


def extract_intent(sentence: str) -> dict:
    """从一句话里提取意图：{"command": "search"/"hot", "keyword": "...", "limit": N}"""
    s = normalize(sentence)
    if not s:
        return {"command": "hot", "keyword": "", "limit": 20}

    lower = s

    # 1) 是否在问热榜
    if any(h in lower for h in HOT_BOARD_HINTS):
        # "看看抖音热榜有什么" / "抖音美食热榜"
        # 先把动作词 / 平台词 / 那些语中词裁掉，再去抽 category
        cleaned = lower
        for w in sorted(ACTION_WORDS, key=len, reverse=True):
            if cleaned.startswith(w):
                cleaned = cleaned[len(w):]
                break
        for token in ["抖音上的", "抖音里的", "抖音上", "抖音里", "抖音"]:
            cleaned = cleaned.replace(token, "")
        cleaned = cleaned.strip("的 ，,。.!！?？")
        m = re.search(r"([\u4e00-\u9fa5A-Za-z0-9]{1,6})\s*热榜", cleaned)
        category = ""
        if m:
            cand = m.group(1)
            if cand and cand not in {"有什么", "看看", "看", "查", "找"}:
                category = cand
        return {"command": "hot", "keyword": "", "category": category, "limit": 20}

    # 2) 否则当作关键词搜索
    keyword = s

    # 砍掉前导动作词（取最长匹配）
    for w in sorted(ACTION_WORDS, key=len, reverse=True):
        if keyword.startswith(w):
            keyword = keyword[len(w):]
            break

    # 反复砍掉两端的 noise tokens
    changed = True
    while changed:
        changed = False
        for token in sorted(NOISE_TOKENS, key=len, reverse=True):
            if keyword.startswith(token):
                keyword = keyword[len(token):]
                changed = True
            if keyword.endswith(token):
                keyword = keyword[: -len(token)]
                changed = True
        keyword = keyword.strip("的 ，,。.!！?？")

    keyword = keyword.strip()

    # 3) 数量提取，例如 "搜 20 个" / "找 5 条" / "来5个"
    limit = 10
    m = re.search(r"(\d{1,3})\s*[个条只篇]", s)
    if m:
        limit = max(1, min(int(m.group(1)), 50))
        # 同时从 keyword 中去掉这个数量词
        keyword = re.sub(r"\d{1,3}\s*[个条只篇]", "", keyword).strip()

    if not keyword:
        # 提取失败：保底用整句去掉动作/平台词的结果，否则抛回 hot
        return {"command": "hot", "keyword": "", "category": "", "limit": limit}

    return {"command": "search", "keyword": keyword, "limit": limit}


# ---------------------------------------------------------------------------
# 爬虫核心
# ---------------------------------------------------------------------------

class DouyinScraper:
    def __init__(self, headless: bool = True, delay: float = 2.0):
        self.headless = headless
        self.delay = delay

    # --- mock fallback ---
    def _mock_search(self, keyword: str, limit: int) -> list[VideoData]:
        today = date.today().isoformat()
        return [
            VideoData(
                title=f"{keyword}相关视频 {i + 1}",
                description=f"这是关于{keyword}的示例描述",
                author=f"作者{i + 1}",
                play_count=10000 * (i + 1),
                like_count=1000 * (i + 1),
                comment_count=100 * (i + 1),
                share_count=50 * (i + 1),
                url=f"https://www.douyin.com/search/{keyword}",
                tags=[keyword, "热门"],
                publish_time=today,
                mock=True,
            )
            for i in range(min(limit, 10))
        ]

    def _mock_hot(self, category: str, limit: int) -> list[VideoData]:
        today = date.today().isoformat()
        label = category or "全部"
        return [
            VideoData(
                title=f"{label}热榜视频 {i + 1}",
                description=f"{label}分类示例热榜数据",
                author=f"热门作者{i + 1}",
                play_count=50000 * (i + 1),
                like_count=5000 * (i + 1),
                comment_count=500 * (i + 1),
                share_count=200 * (i + 1),
                url="https://www.douyin.com/hot",
                tags=["热榜", label],
                publish_time=today,
                mock=True,
            )
            for i in range(min(limit, 20))
        ]

    # --- real fetch (best-effort) ---
    def _real_search(self, keyword: str, limit: int) -> Optional[list[VideoData]]:
        if sync_playwright is None:
            return None
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(
                    f"https://www.douyin.com/search/{keyword}",
                    wait_until="domcontentloaded",
                    timeout=30000,
                )
                time.sleep(self.delay)
                # NOTE: 抖音搜索结果重度依赖登录与风控规避，这里仅尝试基础抽取
                items = page.evaluate(
                    """() => Array.from(document.querySelectorAll('a[href*="/video/"]'))
                        .slice(0, 30)
                        .map(a => ({
                            title: a.innerText.trim().slice(0, 80),
                            url: a.href,
                        }))
                        .filter(x => x.title)"""
                )
                browser.close()
                if not items:
                    return None
                today = date.today().isoformat()
                return [
                    VideoData(
                        title=it.get("title", ""),
                        url=it.get("url", ""),
                        tags=[keyword],
                        publish_time=today,
                    )
                    for it in items[:limit]
                ]
        except Exception as e:
            print(f"⚠️  Playwright 真实抓取失败：{e}", file=sys.stderr)
            return None

    def search(self, keyword: str, limit: int) -> list[VideoData]:
        real = self._real_search(keyword, limit)
        if real:
            return real
        return self._mock_search(keyword, limit)

    def hot(self, category: str, limit: int) -> list[VideoData]:
        # 真实热榜抽取同理强依赖登录，这里直接返回 mock
        return self._mock_hot(category, limit)


# ---------------------------------------------------------------------------
# 输出工具
# ---------------------------------------------------------------------------

def write_json(items: list[VideoData], output: Path) -> None:
    output.write_text(
        json.dumps([i.to_dict() for i in items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_csv(items: list[VideoData], output: Path) -> None:
    if not items:
        output.write_text("", encoding="utf-8")
        return
    fieldnames = list(items[0].to_dict().keys())
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            row = item.to_dict()
            row["tags"] = "|".join(row["tags"])
            writer.writerow(row)


def display(items: list[VideoData], header: str) -> None:
    print("=" * 72)
    print(header)
    print("=" * 72)
    if not items:
        print("(无结果)")
        return
    for idx, v in enumerate(items, 1):
        flag = " [mock]" if v.mock else ""
        print(f"{idx:>2}. {v.title}{flag}")
        if v.author:
            print(f"     作者: {v.author}")
        if v.play_count or v.like_count:
            print(
                f"     ▶️ {v.play_count:,}   👍 {v.like_count:,}   💬 {v.comment_count:,}"
            )
        if v.url:
            print(f"     🔗 {v.url}")
    print("=" * 72)
    if any(v.mock for v in items):
        print(
            "ℹ️  当前结果包含 mock=true 演示数据。要拿真实数据，请安装 Playwright"
            "+Chromium 并登录抖音后再运行。"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_nl(args: argparse.Namespace) -> int:
    sentence = args.sentence
    intent = extract_intent(sentence)
    print(f"💬 输入: {sentence}")
    print(f"🧠 解析: {intent}")
    scraper = DouyinScraper()
    if intent["command"] == "search":
        items = scraper.search(intent["keyword"], intent["limit"])
        display(items, f"🔍 抖音搜索结果：{intent['keyword']}")
    else:
        items = scraper.hot(intent.get("category", ""), intent["limit"])
        display(items, f"🔥 抖音热榜：{intent.get('category') or '全部'}")
    if args.output:
        out = Path(args.output)
        if args.format == "csv":
            write_csv(items, out)
        else:
            write_json(items, out)
        print(f"💾 已保存：{out}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    scraper = DouyinScraper()
    items = scraper.search(args.keyword, args.limit)
    display(items, f"🔍 抖音搜索结果：{args.keyword}")
    if args.output:
        out = Path(args.output)
        if args.format == "csv":
            write_csv(items, out)
        else:
            write_json(items, out)
        print(f"💾 已保存：{out}")
    return 0


def cmd_hot(args: argparse.Namespace) -> int:
    scraper = DouyinScraper()
    items = scraper.hot(args.category, args.limit)
    display(items, f"🔥 抖音热榜：{args.category or '全部'}")
    if args.output:
        out = Path(args.output)
        if args.format == "csv":
            write_csv(items, out)
        else:
            write_json(items, out)
        print(f"💾 已保存：{out}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音爆款爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    nl = sub.add_parser("nl", help="自然语言一句话触发搜索/热榜")
    nl.add_argument("sentence", help="例如 '搜索一下海鲜视频'")
    nl.add_argument("--output")
    nl.add_argument("--format", choices=["json", "csv"], default="json")
    nl.set_defaults(func=cmd_nl)

    search = sub.add_parser("search", help="关键词搜索")
    search.add_argument("--keyword", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--output")
    search.add_argument("--format", choices=["json", "csv"], default="json")
    search.set_defaults(func=cmd_search)

    hot = sub.add_parser("hot", help="抖音热榜")
    hot.add_argument("--category", default="")
    hot.add_argument("--limit", type=int, default=20)
    hot.add_argument("--output")
    hot.add_argument("--format", choices=["json", "csv"], default="json")
    hot.set_defaults(func=cmd_hot)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
