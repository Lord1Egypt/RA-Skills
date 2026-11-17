#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抖音「账号主页作品抓取」CLI（在 douyin-comment-collector 上扩展而来）。

能力：给定抖音账号主页 URL / 短链 / 纯 sec_uid，抓取该账号发布的作品清单，
输出每个作品的标题（desc）与发布时间（create_time），并支持在本地按时间区间
（--since / --until）过滤。这正是「拉取指定账号在指定时间发布内容的标题和时间」。

实现思路（与 comment 的浏览器方案同构，签名/指纹/风控全交给真实浏览器）：
    启动真实 Chromium 打开账号主页 ``https://www.douyin.com/user/<sec_uid>``，
    抖音前端自动算好 a_bogus / msToken 并带完整指纹去调主页作品接口
    ``/aweme/v1/web/aweme/post/``；本脚本只拦截该网络响应，把 ``aweme_list``
    里的作品标题/时间/ID 抽出来。滚动主页触发翻页加载更多。

依赖（可选，与评论浏览器方案共享）：
    pip install playwright
    playwright install chromium

与评论采集的关系：
    - 评论接口：``/comment/list/`` → 抓「某视频的评论」
    - 作品接口：``/aweme/post/``   → 抓「某账号的作品列表」
    两者共用 login_helper.py 生成的 cookie（可越游客风控拿更多/更早的作品）。

约束：
    - 游客态能拿到公开作品，但可能被风控（登录弹窗）或只能拿到最近若干条；
      要拿更早/更全的作品，先运行 ``login_helper.py`` 登录（--cookie-file 自动读取）。
    - 「指定时间」是**本地过滤**：主页接口本身不提供时间区间参数，本脚本抓
      ``--limit`` 条后按 ``create_time`` 过滤 ``--since/--until`` 窗口。
      时间窗口越靠前，``--limit`` 需给得越大。
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 浏览器底座：与评论浏览器方案一致，未安装则给出清晰提示。
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.stderr.write(
        "缺少 playwright：主页作品抓取（浏览器方案）不可用。\n"
        "请先执行：pip install playwright && playwright install chromium\n"
    )
    sys.exit(2)

# 复用 browser_fetch 的 cookie 加载与登录态探测（幂等、无副作用）。
from browser_fetch import load_cookies_any, DEFAULT_COOKIE_FILE  # noqa: E402

logger = logging.getLogger("douyin-posts")

# 反 headless 检测（与评论方案一致）
_STEALTH_JS = (
    "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });\n"
    "try { window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {} }; } catch (e) {}\n"
)

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 输出字段（扁平化）。默认核心：标题 + 发布时间；--with-stats 追加互动数据。
BASE_FIELDS = ["aweme_id", "desc", "create_time", "publish_time", "type", "video_url"]
STAT_FIELDS = ["digg_count", "comment_count", "share_count", "collect_count", "play_count"]

TZ_CN = timezone(timedelta(hours=8))


# ----------------------------------------------------------------------
# 输入解析：主页 URL / 短链 / 纯 sec_uid
# ----------------------------------------------------------------------
def extract_sec_uid(text: str) -> str | None:
    """从主页链接或纯 sec_uid 中提取 sec_uid（用于日志/记录，非关键路径）。"""
    text = (text or "").strip()
    if not text:
        return None
    # 纯 sec_uid：抖音 sec_uid 通常以 MS4wLj 开头（base64）
    if re.fullmatch(r"MS4wLj[A-Za-z0-9_\-+=/]+", text):
        return text
    m = re.search(r"/user/([A-Za-z0-9_\-+=/]+)", text)
    if m:
        return m.group(1)
    return None


def normalize_target(url: str) -> str:
    """把输入规整成浏览器可直接打开的账号主页 URL。

    - 纯 sec_uid → ``https://www.douyin.com/user/<sec_uid>``
    - 主页完整 URL → 原样返回
    - 短链 ``v.douyin.com/xxx`` → 保留原样（浏览器会跟随重定向到主页）
    """
    url = (url or "").strip()
    if re.fullmatch(r"MS4wLj[A-Za-z0-9_\-+=/]+", url):
        return f"https://www.douyin.com/user/{url}"
    return url


# ----------------------------------------------------------------------
# 时间过滤
# ----------------------------------------------------------------------
def parse_time(s: str, end_of_day: bool = False) -> datetime:
    """解析 ``YYYY-MM-DD`` 或 ``YYYY-MM-DD HH:MM[:SS]`` 为本地(+8)naive datetime。

    ``end_of_day=True``（--until 且只给日期）→ 当天 23:59:59。
    """
    s = (s or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        t = datetime.strptime(s, "%Y-%m-%d")
        if end_of_day:
            t = t.replace(hour=23, minute=59, second=59)
        return t
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"无法解析时间：{s!r}（支持 YYYY-MM-DD 或 YYYY-MM-DD HH:MM[:SS]）")


def to_ts(dt: datetime) -> int:
    """本地 naive datetime → UTC 秒时间戳（create_time 同口径）。"""
    return int(dt.replace(tzinfo=TZ_CN).timestamp())


def fmt_ts(ts) -> str:
    """UTC 秒时间戳 → 可读时间字符串（+8）。"""
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts), tz=TZ_CN).strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError, OSError):
        return ""


# ----------------------------------------------------------------------
# 作品字段抽取
# ----------------------------------------------------------------------
def flatten_post(a: dict) -> dict:
    """从 aweme_list 单条作品提取核心字段。"""
    stats = a.get("statistics") or {}
    is_image = bool(a.get("images"))  # 图文 vs 视频
    return {
        "aweme_id": a.get("aweme_id"),
        "desc": a.get("desc", ""),
        "create_time": a.get("create_time"),
        "publish_time": fmt_ts(a.get("create_time")),
        "type": "image" if is_image else "video",
        "video_url": (
            f"https://www.douyin.com/note/{a.get('aweme_id')}"
            if is_image
            else f"https://www.douyin.com/video/{a.get('aweme_id')}"
        ),
        "digg_count": stats.get("digg_count"),
        "comment_count": stats.get("comment_count"),
        "share_count": stats.get("share_count"),
        "collect_count": stats.get("collect_count"),
        "play_count": stats.get("play_count"),
    }


def _make_post_handler(posts: list, seen: set) -> "callable":
    """返回 Playwright response 回调：命中主页作品接口就抽取 aweme_list。"""

    def handler(response) -> None:
        url = response.url
        if "/aweme/post/" not in url:
            return
        try:
            data = json.loads(response.text())
        except Exception:
            return
        if not isinstance(data, dict):
            return
        for a in data.get("aweme_list") or []:
            if not isinstance(a, dict):
                continue
            aweme_id = a.get("aweme_id")
            if not aweme_id or aweme_id in seen:
                continue
            seen.add(aweme_id)
            posts.append(flatten_post(a))

    return handler


# ----------------------------------------------------------------------
# 浏览器抓取
# ----------------------------------------------------------------------
def fetch_posts(
    target: str,
    *,
    max_scrolls: int = 30,
    scroll_pause: int = 1500,
    timeout: int = 60000,
    headless: bool = True,
    cookie_file: str | None = None,
    limit: int = 0,
    since_ts: int | None = None,
    until_ts: int | None = None,
) -> list:
    """打开账号主页，滚动加载并拦截作品接口，返回作品列表（已本地过滤）。

    Args:
        target: 账号主页 URL 或 sec_uid。
        limit: 最大抓取作品条数（0=不设上限，抓到滚动停止为止）。
        since_ts / until_ts: 本地时间过滤窗口（UTC 秒）。None 表示不限制该端。
    """
    url = normalize_target(target)
    sec_uid = extract_sec_uid(target)
    if sec_uid:
        logger.info("解析到 sec_uid=%s", sec_uid)

    posts: list = []
    seen: set = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            user_agent=_UA,
            viewport={"width": 1440, "height": 900},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        if cookie_file and os.path.exists(cookie_file):
            try:
                cookies = load_cookies_any(cookie_file)
                if cookies:
                    context.add_cookies(cookies)
                    logger.info("已注入登录态 cookie：%s（%d 条）", cookie_file, len(cookies))
                else:
                    logger.warning("cookie 文件为空，回退游客态")
            except Exception as exc:
                logger.warning("cookie 读取失败，回退游客态：%s", exc)
        context.add_init_script(_STEALTH_JS)
        page = context.new_page()
        page.on("response", _make_post_handler(posts, seen))

        logger.info("浏览器打开 %s", url)
        # 抖音页面有持续轮询/长连接，networkidle 永不触发 → domcontentloaded + 等待首屏数据
        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        # 登录态下首次 aweme/post 响应可能延迟 ~9s（游客态更快，但游客态通常空体）。
        # 先等到捕获到第一条作品，或达到 initial_wait 上限，避免首屏数据未到就提前滚动/退出。
        initial_wait_ms = 15000
        waited = 0
        step = 500
        while not posts and waited < initial_wait_ms:
            page.wait_for_timeout(step)
            waited += step
        logger.info("首屏等待 %dms，已捕获 %d 条作品", waited, len(posts))

        prev = len(posts)
        no_new = 0
        for i in range(max_scrolls):
            # 主页作品是双列网格 + 无限滚动：把主滚动容器与 window 都滚到底触发下一页 post 请求。
            try:
                page.evaluate(
                    "() => {"
                    "  const c = document.querySelector('.route-scroll-container') "
                    "         || document.querySelector('.parent-route-container') "
                    "         || document.scrollingElement;"
                    "  if (c) c.scrollTop = c.scrollHeight;"
                    "  window.scrollTo(0, document.body.scrollHeight);"
                    "}"
                )
            except Exception:
                page.mouse.wheel(0, 3000)  # 兜底：整窗滚动
            page.wait_for_timeout(scroll_pause)
            now = len(posts)
            if limit and now >= limit:
                logger.info("已达 limit=%d，停止滚动", limit)
                break
            if now == prev:
                no_new += 1
                if no_new >= 5:  # 连续 5 轮无新增，视为到底/被风控
                    logger.info("连续 %d 轮无新增作品，停止滚动（已抓 %d 条）", no_new, now)
                    break
            else:
                no_new = 0
                prev = now
            if (i + 1) % 5 == 0:
                logger.info("已滚动 %d 次，累计 %d 条作品", i + 1, now)
        browser.close()

    # 本地时间窗口过滤 + limit 截断
    if since_ts is not None or until_ts is not None:
        filtered = []
        for item in posts:
            ts = item.get("create_time")
            if ts is None:
                continue  # 缺失时间戳的作品不纳入时间过滤
            ts = int(ts)
            if since_ts is not None and ts < since_ts:
                continue
            if until_ts is not None and ts > until_ts:
                continue
            filtered.append(item)
        logger.info("时间过滤 [%s, %s]：%d -> %d 条",
                    fmt_ts(since_ts) or "-∞", fmt_ts(until_ts) or "+∞",
                    len(posts), len(filtered))
        posts = filtered
    if limit:
        posts = posts[:limit]
    return posts


# ----------------------------------------------------------------------
# 输出
# ----------------------------------------------------------------------
def write_posts(posts: list, fmt: str, path: str | None, with_stats: bool) -> None:
    fields = BASE_FIELDS + (STAT_FIELDS if with_stats else [])
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for item in posts:
            w.writerow({k: item.get(k, "") for k in fields})
        out = buf.getvalue()
    else:
        out = json.dumps(posts, ensure_ascii=False, indent=2)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        logger.info("已写入 %d 条作品 -> %s", len(posts), path)
    else:
        print(out)


def analyze_distribution(posts: list) -> dict:
    """按天聚合作品数，返回时间分布统计（供 ``--analyze`` 使用）。

    返回结构：
        post_count（作品总数）、first_publish_time / last_publish_time（最早/最晚发布，+8）、
        daily_distribution（按 YYYY-MM-DD 倒序的 [{"date", "count"}]）。
    """
    from collections import defaultdict
    by_day: dict = defaultdict(int)
    for it in posts:
        ts = it.get("create_time")
        by_day[fmt_ts(ts)[:10] if ts is not None else "unknown"] += 1
    dist = [
        {"date": d, "count": c}
        for d, c in sorted(by_day.items(), reverse=True)
    ]
    times = [int(it["create_time"]) for it in posts if it.get("create_time") is not None]
    return {
        "post_count": len(posts),
        "first_publish_time": fmt_ts(min(times)) if times else "",
        "last_publish_time": fmt_ts(max(times)) if times else "",
        "daily_distribution": dist,
    }


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fetch_posts",
        description="抖音账号主页作品抓取：主页URL/短链/sec_uid → 作品标题+发布时间（JSON/CSV），"
                    "支持 --since/--until 时间区间过滤",
    )
    p.add_argument("url", help="抖音账号主页 URL / 短链转发链接(v.douyin.com) / 纯 sec_uid")
    p.add_argument("--since", default=None,
                   help="仅保留该时间（含）之后发布的作品；格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM[:SS]")
    p.add_argument("--until", default=None,
                   help="仅保留该时间（含）之前发布的作品；格式同上（只给日期=当天 23:59:59）")
    p.add_argument("--limit", type=int, default=0,
                   help="最多抓取的作品条数（0=不设上限，滚动到底为止；时间窗口越早给越大）")
    p.add_argument("--max-scrolls", type=int, default=30, help="最大滚动加载次数（默认30）")
    p.add_argument("--scroll-pause", type=int, default=1500, help="每次滚动后等待毫秒（默认1500）")
    p.add_argument("--timeout", type=int, default=60000, help="页面加载超时毫秒（默认60000）")
    p.add_argument("--no-headless", action="store_true", help="关闭无头（可肉眼观察是否被风控弹窗拦截）")
    p.add_argument("--cookie-file", default=None,
                   help="登录态 cookie 文件路径（由 login_helper.py 生成）；缺省自动探测 scripts/douyin_cookie.json")
    p.add_argument("--with-stats", action="store_true",
                   help="额外输出互动数据（点赞/评论/分享/收藏/播放）")
    p.add_argument("--analyze", action="store_true",
                   help="附带按天时间分布统计（作品数按 YYYY-MM-DD 聚合，配 --output 时写到 .analyze.json）")
    p.add_argument("--format", choices=["json", "csv"], default="json", help="输出格式")
    p.add_argument("--output", help="输出文件路径（缺省打印到 stdout）")
    p.add_argument("-v", "--verbose", action="store_true", help="打印调试日志")
    return p


def main(argv=None) -> int:
    args = build_argparser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    # 时间窗口解析
    try:
        since_ts = to_ts(parse_time(args.since)) if args.since else None
        until_ts = to_ts(parse_time(args.until, end_of_day=True)) if args.until else None
    except ValueError as exc:
        logger.error("%s", exc)
        return 2
    if since_ts and until_ts and since_ts > until_ts:
        logger.error("--since 晚于 --until，窗口无效")
        return 2

    # cookie 文件：显式 > 自动探测 scripts/douyin_cookie.json > 游客态
    cookie_file = args.cookie_file
    if not cookie_file and os.path.exists(DEFAULT_COOKIE_FILE):
        cookie_file = DEFAULT_COOKIE_FILE
    if cookie_file:
        logger.info("使用登录态 cookie：%s", cookie_file)
    else:
        logger.warning(
            "未检测到 cookie 文件 → 游客态抓取：可能被风控或只能拿到最近若干条作品。"
            "要拿更早/更全的作品，请先运行 python login_helper.py 登录（--cookie-file 自动读取）。"
        )

    try:
        posts = fetch_posts(
            args.url,
            max_scrolls=args.max_scrolls,
            scroll_pause=args.scroll_pause,
            timeout=args.timeout,
            headless=not args.no_headless,
            cookie_file=cookie_file,
            limit=args.limit,
            since_ts=since_ts,
            until_ts=until_ts,
        )
    except Exception as exc:
        logger.error("主页作品抓取失败：%s", exc)
        return 1

    if not posts:
        logger.warning(
            "未抓到作品。常见原因：① 游客态被风控（登录弹窗/滑块）→ 先 login_helper.py 登录；"
            "② 该账号无作品/主页链接无效；③ 时间窗口内无作品。"
        )
        write_posts([], args.format, args.output, args.with_stats)
        return 0

    # 按发布时间倒序（最新在前），方便查看
    posts.sort(key=lambda x: int(x.get("create_time") or 0), reverse=True)

    # 可选：按天时间分布统计
    if args.analyze:
        result = analyze_distribution(posts)
        result["sec_uid"] = extract_sec_uid(args.url)
        if args.output:
            write_posts(posts, args.format, args.output, args.with_stats)
            base, _ = os.path.splitext(args.output)
            ana_path = base + ".analyze.json"
            with open(ana_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info("时间分布统计已写入 %s", ana_path)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            logger.info("未指定 --output，作品列表未落盘；仅输出时间分布统计")
        return 0

    write_posts(posts, args.format, args.output, args.with_stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
