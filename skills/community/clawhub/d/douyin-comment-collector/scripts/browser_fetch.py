"""抖音评论采集 - 无头浏览器方案（可选，免登录尝试）。

思路：启动真实 Chromium 以「游客」身份打开视频页，抖音前端会自动算好
``a_bogus`` / ``msToken`` 并带完整浏览器指纹去调评论接口；本脚本只拦截
它发出的 ``comment/list`` 网络响应，把评论数据捞出来。签名、指纹、风控
全部交给浏览器，本脚本零参与 —— 这正是纯 HTTP 方案缺的那块拼图。

依赖（可选，未安装不影响默认纯 HTTP 路径）：
    pip install playwright
    playwright install chromium

适用场景：一次一个作品、非批量抓取。若游客态仍被风控（登录弹窗/滑块），
请改用 ``fetch_comments.py`` 的创作者接口 + 本人 cookie。
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from typing import Callable

# 脚本目录：用于自动发现登录助手生成的 cookie 文件
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COOKIE_FILE = os.path.join(_HERE, "douyin_cookie.json")

# Playwright add_cookies 只认这些键，其余（如 DrissionPage 的 expires 别名）会报
# "unexpected property"，统一裁剪 + 补 domain/path，避免注入失败。
_COOKIE_KNOWN_KEYS = {"name", "value", "domain", "path", "expires", "httpOnly", "secure", "sameSite", "url"}


def load_cookies_any(path: str) -> list:
    """兼容多种 cookie 文件格式，统一成 Playwright ``add_cookies`` 所需的 dict 列表。

    支持：
    - Playwright / DrissionPage 导出的 **JSON 列表**（含 name/value/domain/path）。
    - 单键 JSON（如 ``{"cookies": [...]}``）。
    - **纯字符串形态** ``name=value; name2=value2``：
      字符串本身无 domain/path，统一补 ``.douyin.com`` 通配域，使其对 www / creator 子域均生效。
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    if not raw:
        return []
    if raw[0] in "[{":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = data.get("cookies") or data.get("cookie_list") or []
        out = []
        for c in data:
            c = {k: v for k, v in c.items() if k in _COOKIE_KNOWN_KEYS}
            c.setdefault("domain", ".douyin.com")
            c.setdefault("path", "/")
            out.append(c)
        return out
    # 纯字符串：name=value; name2=value2 ...
    out = []
    for part in raw.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(), "domain": ".douyin.com", "path": "/"})
    return out

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # 未安装浏览器底座时给出清晰提示，而非堆栈
    sys.stderr.write(
        "缺少 playwright：无头浏览器方案不可用。\n"
        "请先执行：pip install playwright && playwright install chromium\n"
        "（不装也可继续使用默认纯 HTTP 创作者接口方案 fetch_comments.py）\n"
    )
    sys.exit(2)

from fetch_comments import write_output, resolve_aweme_id

logger = logging.getLogger(__name__)

# 反 headless 检测：覆盖 navigator.webdriver，并伪造 chrome 运行时对象。
_STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
try { window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {} }; } catch (e) {}
"""

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _make_response_handler(comments: list, seen: set, last_cursor: dict) -> Callable:
    """返回一个 Playwright response 回调：命中 comment 接口就抽取 comments。

    注意：必须用 ``response.text()`` + ``json.loads``，而不是直接 ``response.json()``。
    Playwright 的 ``response.json()`` 在遇到非标准 Content-Type / 压缩编码时会静默抛异常，
    导致整页评论被吞掉（实测踩坑）。``text()`` 更鲁棒。
    """

    def handler(response) -> None:
        url = response.url
        if "/comment/list/" not in url:
            return
        try:
            data = json.loads(response.text())
        except Exception:
            return
        if not isinstance(data, dict):
            return
        # 记录分页游标，供主循环判断是否需要继续滚动加载
        if data.get("has_more") is not None:
            last_cursor["has_more"] = data.get("has_more")
            last_cursor["cursor"] = data.get("cursor") or last_cursor.get("cursor")
        for c in data.get("comments") or []:
            cid = c.get("cid") or c.get("id") or c.get("aweme_id")
            if cid and cid not in seen:
                seen.add(cid)
                # 字段归一化：接口原始返回 user/digg_count，对外统一为
                # author/like_count，便于下游消费（实测游客态同样含这两个字段，
                # 之前展示成「?」是测试脚本用错 key 名所致，并非真缺失）
                u = c.get("user") or {}
                c["author"] = u.get("nickname") if isinstance(u, dict) else None
                c["like_count"] = c.get("digg_count")
                comments.append(c)

    return handler


def fetch_with_browser(
    url: str,
    *,
    max_scrolls: int = 20,
    scroll_pause: int = 1200,
    timeout: int = 60000,
    headless: bool = True,
    cookie_file: str | None = None,
) -> list:
    """用真实 Chromium 打开视频页并拦截评论响应。

    支持两种身份：
    - 游客态（``cookie_file=None``）：免登录，但抖音会弹「评论墙」，
      通常只能拿到前 ~14-20 条样本评论。
    - 登录态（``cookie_file`` 指向 login_helper 生成的文件）：注入真实
      cookie，通常能越过评论墙拿到更多/全部评论。

    Args:
        url: 视频完整 URL / 短链 / 数字 aweme_id。
        max_scrolls: 最大滚动加载次数（每次滚动尝试触发更多评论）。
        scroll_pause: 每次滚动后等待毫秒。
        timeout: 页面加载超时（毫秒）。
        headless: 是否无头；False 可肉眼观察是否被风控弹窗拦截。
        cookie_file: 登录态 cookie 文件路径（playwright cookie 列表格式）；
            None 表示游客态。

    Returns:
        评论 dict 列表（已归一化：text/author/like_count/cid...）。
    """
    # 短链/数字先解析成稳定 video 页 URL，减少分享中转页干扰
    try:
        aweme_id = resolve_aweme_id(url)
        target = f"https://www.douyin.com/video/{aweme_id}"
    except Exception:
        target = url  # 解析失败就直接用原始链接（浏览器会跟随重定向）

    comments: list = []
    seen: set = set()
    last_cursor: dict = {"has_more": True, "cursor": None}
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
        # 登录态：注入 cookie 文件（login_helper 生成），越过评论墙
        if cookie_file and os.path.exists(cookie_file):
            try:
                cookies = load_cookies_any(cookie_file)
                if not cookies:
                    raise ValueError("cookie 文件为空或无法解析")
                context.add_cookies(cookies)
                logger.info("已注入登录态 cookie：%s（%d 条）", cookie_file, len(cookies))
            except Exception as exc:
                logger.warning("cookie 文件读取失败，回退游客态：%s", exc)
        context.add_init_script(_STEALTH_JS)
        page = context.new_page()
        page.on("response", _make_response_handler(comments, seen, last_cursor))

        logger.info("浏览器打开 %s", target)
        # 抖音页面有持续轮询/长连接，networkidle 永不触发 → 用 domcontentloaded + 固定等待
        page.goto(target, wait_until="domcontentloaded", timeout=timeout)
        page.wait_for_timeout(3000)  # 等初始评论异步加载

        prev = len(comments)
        no_new = 0
        for i in range(max_scrolls):
            # 抖音评论区是「无限滚动」：把评论容器与窗口都滚到底，触发下一页 comment/list 请求。
            # 实测关键：必须同时滚 .parent-route-container / .comment-mainContent 与 window，
            # 单滚容器不会触发翻页（抖音按窗口与容器双重滚动信号加载）。
            try:
                page.evaluate(
                    "() => {"
                    "  const c = document.querySelector('.parent-route-container') || document.querySelector('.route-scroll-container');"
                    "  if (c) c.scrollTop = c.scrollHeight;"
                    "  const cm = document.querySelector('.comment-mainContent');"
                    "  if (cm) cm.scrollTop = cm.scrollHeight;"
                    "  window.scrollTo(0, document.body.scrollHeight);"
                    "}"
                )
            except Exception:
                page.mouse.wheel(0, 2500)  # 兜底：整窗滚动
            page.wait_for_timeout(scroll_pause)
            now = len(comments)
            # 服务端明确无更多则提前结束（避免空转）
            if last_cursor.get("has_more") == 0:
                logger.info("服务端返回 has_more=0，评论已抓完（%d 条）", now)
                break
            if now == prev:
                no_new += 1
                if no_new >= 3:  # 连续 3 轮无新增，视为到底
                    logger.info("连续 %d 轮无新增评论，停止滚动（已抓 %d 条）", no_new, now)
                    break
            else:
                no_new = 0
                prev = now
            if (i + 1) % 5 == 0:
                logger.info("已滚动 %d 次，累计 %d 条评论", i + 1, now)
        browser.close()
    return comments


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="browser_fetch",
        description="抖音评论采集（无头浏览器·游客态·免登录尝试）：URL/转发链接 → 评论 JSON/CSV",
    )
    p.add_argument("url", help="抖音视频完整URL / 短链转发链接(v.douyin.com) / 纯数字 aweme_id")
    p.add_argument("--max-scrolls", type=int, default=20, help="最大滚动加载次数（默认20）")
    p.add_argument("--scroll-pause", type=int, default=1200, help="每次滚动后等待毫秒（默认1200）")
    p.add_argument("--timeout", type=int, default=60000, help="页面加载超时毫秒（默认60000）")
    p.add_argument("--no-headless", action="store_true", help="关闭无头（可肉眼观察是否被风控弹窗拦截）")
    p.add_argument("--format", choices=["json", "csv"], default="json", help="输出格式")
    p.add_argument("--output", help="输出文件路径（缺省打印到 stdout）")
    p.add_argument(
        "--cookie-file", default=None,
        help="登录态 cookie 文件路径（由 login_helper.py 生成）；缺省自动探测 scripts/douyin_cookie.json",
    )
    p.add_argument("--analyze", action="store_true", help="附带 jieba 分词 + 停用词词频分析")
    p.add_argument("--top-n", type=int, default=50, help="词频分析返回前 N 个词（默认50）")
    p.add_argument("--stopwords", help="自定义停用词文件路径（每行一个词）")
    p.add_argument("--min-word-len", type=int, default=2, help="词频分析最小词长（默认2）")
    p.add_argument("-v", "--verbose", action="store_true", help="打印调试日志")
    return p


def main(argv=None) -> int:
    args = build_argparser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    # cookie 文件：显式 > 自动探测 scripts/douyin_cookie.json > 游客态
    cookie_file = args.cookie_file
    if not cookie_file and os.path.exists(DEFAULT_COOKIE_FILE):
        cookie_file = DEFAULT_COOKIE_FILE
    if cookie_file:
        logger.info("使用登录态 cookie：%s", cookie_file)
    else:
        logger.warning(
            "未检测到 cookie 文件 → 游客态抓取：抖音会弹「评论墙」，通常仅返回前 ~14-20 条。"
            "如需更多评论，请先运行 python login_helper.py 登录后抓取。"
        )
    try:
        comments = fetch_with_browser(
            args.url,
            max_scrolls=args.max_scrolls,
            scroll_pause=args.scroll_pause,
            timeout=args.timeout,
            headless=not args.no_headless,
            cookie_file=cookie_file,
        )
    except Exception as exc:
        logger.error("浏览器采集失败：%s", exc)
        return 1

    if not comments:
        logger.warning(
            "未采集到评论。游客态可能被风控（登录弹窗/滑块验证）。"
            "建议运行 python login_helper.py 登录后重试（--cookie-file 会自动读取）。"
        )
        write_output([], args.format, args.output)
        return 0

    write_output(comments, args.format, args.output)

    if args.analyze:
        try:
            from analyze import analyze_comments
            words = analyze_comments(
                [c.get("text", "") for c in comments if c.get("text")],
                top_n=args.top_n,
                stopwords_path=args.stopwords,
                min_len=args.min_word_len,
            )
            base = args.output or "comments.csv"
            analyze_path = base.rsplit(".", 1)[0] + ".analyze.json"
            with open(analyze_path, "w", encoding="utf-8") as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            logger.info("词频分析 -> %s", analyze_path)
        except Exception as exc:
            logger.warning("词频分析跳过：%s", exc)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
