#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
free-web-search v8.0.0

路由策略：仅按 IP 归属判断
  - IP 国内 → Bing CN（Playwright 全流程：开首页拿 cookies → 搜索框提交）
  - IP 国外 → DDG（Playwright 全流程：开首页拿 cookies → 搜索框提交）
  - 任一引擎为空时互相兜底

不做 query 改写，不做城市/意图识别，不做单域名排除重试，不做低质量过滤。
"""

import sys
import json
import time
import argparse
from urllib.parse import urlencode, quote, urlparse

# ==================== 强制UTF-8 ====================
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ==================== 配置 ====================
DEFAULT_MAX = 10
DEFAULT_FULL = 0
PW_TIMEOUT = 25000
HOME_TIMEOUT = 15000
FETCH_TIMEOUT = 15000

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)

BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
]

ROUTE_PATTERN = "**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,mp4,ico,webp,js.map}"

_browser = None
_playwright = None


def check_playwright():
    """检查 playwright 是否安装。未安装时给出安装提示并退出。"""
    try:
        import playwright  # noqa: F401
        return
    except ImportError:
        import os
        skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("\n[X] free-web-search 缺少依赖: playwright\n", file=sys.stderr)
        print("   一键安装（推荐）:", file=sys.stderr)
        print(f'     cd "{skill_root}" && bash scripts/setup.sh', file=sys.stderr)
        print("   Windows:", file=sys.stderr)
        print(f'     cd "{skill_root}"; powershell -File scripts/setup.ps1\n', file=sys.stderr)
        print("   手动安装:", file=sys.stderr)
        print(f'     cd "{skill_root}"', file=sys.stderr)
        print("     pip install playwright", file=sys.stderr)
        print("     playwright install chromium\n", file=sys.stderr)
        print("   详细文档: 见 SKILL.md「安装」章节\n", file=sys.stderr)
        sys.exit(2)


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("query", nargs="*")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX, dest="max_results")
    parser.add_argument("--full", type=int, default=DEFAULT_FULL)
    parser.add_argument("--region", default="auto", choices=["auto", "cn", "intl"],
                        help="区域覆盖（auto = IP 探测）")
    args = parser.parse_args()
    query = " ".join(args.query).strip()
    args.max_results = max(1, min(20, args.max_results))
    args.full = max(0, min(5, args.full))
    return query, args.max_results, args.full, args.region


def init_browser():
    global _browser, _playwright
    if _browser:
        return
    from playwright.sync_api import sync_playwright
    print("[DEBUG] 启动 Chromium...", file=sys.stderr)
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(headless=True, args=BROWSER_ARGS)
    print("[DEBUG] Chromium 已就绪", file=sys.stderr)


def close_browser():
    global _browser, _playwright
    try:
        if _browser:
            _browser.close()
            _browser = None
        if _playwright:
            _playwright.stop()
            _playwright = None
    except Exception:
        pass


def create_context(locale="zh-CN", accept_language="zh-CN,zh;q=0.9"):
    return _browser.new_context(
        locale=locale, user_agent=UA,
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080},
        device_scale_factor=1,
        timezone_id="Asia/Shanghai",
        has_touch=False, is_mobile=False, java_script_enabled=True,
        extra_http_headers={"Accept-Language": accept_language},
    )

# ==================== IP 归属探测 ====================
_in_china_cache = None


def detect_in_china():
    """三条并发探测，先返回的获胜。失败默认国外。"""
    global _in_china_cache
    if _in_china_cache is not None:
        return _in_china_cache

    import urllib.request
    import urllib.error

    def probe(url, timeout=3):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode('utf-8', errors='ignore'), resp.getcode()
        except Exception:
            return None, None

    # 中国 IP 探测
    for url in ('https://myip.ipip.net', 'https://cip.cc'):
        text, status = probe(url)
        if text and ('中国' in text or 'CN' in text.upper()):
            print(f"[地理] {url} → CN → 国内", file=sys.stderr)
            _in_china_cache = True
            return True

    # 国际 IP 探测
    import json as _json
    for url in ('https://ipinfo.io/json', 'https://ipapi.co/json/'):
        text, status = probe(url)
        if text:
            try:
                d = _json.loads(text)
                cc = str(d.get('country') or d.get('country_code') or '').upper()
                if cc:
                    print(f"[地理] {url} → {cc} → {'国内' if cc == 'CN' else '国外'}",
                          file=sys.stderr)
                    _in_china_cache = (cc == 'CN')
                    return _in_china_cache
            except Exception:
                pass

    # cn.bing.com 可达性
    _, status = probe('https://cn.bing.com')
    if status in (200, 301, 302):
        print(f"[地理] cn.bing.com → {status} → 国内", file=sys.stderr)
        _in_china_cache = True
        return True

    print("[地理] 检测失败，默认国外", file=sys.stderr)
    _in_china_cache = False
    return False

# ==================== Bing CN（Playwright 全流程：先访问首页拿 cookies → 搜索框提交） ====================
def search_bing(query, max_results):
    print(f"[Bing:pw] {query} | max={max_results}", file=sys.stderr)
    init_browser()
    out = []
    seen = set()
    ctx = create_context(locale="zh-CN", accept_language="zh-CN,zh;q=0.9")
    try:
        page = ctx.new_page()
        page.route(ROUTE_PATTERN, lambda r: r.abort())

        # 1) 先访问首页建立 session，拿 cookies
        try:
            page.goto("https://cn.bing.com/", timeout=HOME_TIMEOUT,
                      wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
        except Exception as e:
            print(f"[Bing:pw] 首页加载警告: {e}", file=sys.stderr)

        # 2) 通过搜索框提交（携带首页 cookies）
        try:
            search_box = page.query_selector("#sb_form_q")
            if search_box:
                search_box.click()
                search_box.fill(query)
                page.wait_for_timeout(300)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded", timeout=PW_TIMEOUT)
                page.wait_for_timeout(2000)
            else:
                page.goto("https://cn.bing.com/search?" + urlencode({"q": query}),
                          timeout=PW_TIMEOUT, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
        except Exception:
            page.goto("https://cn.bing.com/search?" + urlencode({"q": query}),
                      timeout=PW_TIMEOUT, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)

        raw = page.evaluate("""() => {
            const items = [];
            document.querySelectorAll('li.b_algo').forEach(el => {
                try {
                    const a = el.querySelector('h2 a');
                    const p = el.querySelector('.b_caption p, .b_algoSlug');
                    if (a && a.href && a.href.startsWith('http')) {
                        items.push({
                            title: (a.innerText || a.textContent || '').trim(),
                            url: a.href.trim(),
                            snippet: p ? (p.innerText || p.textContent || '').trim() : ''
                        });
                    }
                } catch(e) {}
            });
            return items;
        }""")

        for r in raw:
            url = r["url"]
            if r["title"] and url and url not in seen and len(r["title"]) > 3:
                seen.add(url)
                out.append({"title": r["title"], "url": url,
                            "snippet": r["snippet"], "content": ""})
        print(f"[Bing:pw] {len(out)} 条", file=sys.stderr)
    except Exception as e:
        print(f"[Bing:pw] 错误: {e}", file=sys.stderr)
    finally:
        try: ctx.close()
        except Exception: pass
    return out[:max_results]


# ==================== DDG（Playwright 全流程：先访问首页拿 cookies → 搜索框提交） ====================
def search_duckduckgo(query, max_results):
    print(f"[DDG:pw] {query}", file=sys.stderr)
    init_browser()
    out = []
    seen = set()
    ctx = create_context(locale="en-US", accept_language="en-US,en;q=0.9")
    try:
        page = ctx.new_page()
        page.route(ROUTE_PATTERN, lambda r: r.abort())

        # 1) 先访问首页建立 session
        try:
            page.goto("https://duckduckgo.com/", timeout=HOME_TIMEOUT,
                      wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
        except Exception as e:
            print(f"[DDG:pw] 首页加载警告: {e}", file=sys.stderr)

        # 2) 搜索框提交
        try:
            search_box = page.query_selector('input[name="q"]')
            if search_box:
                search_box.click()
                search_box.fill(query)
                page.wait_for_timeout(300)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded", timeout=PW_TIMEOUT)
                page.wait_for_timeout(2500)
            else:
                page.goto("https://duckduckgo.com/?q=" + quote(query),
                          timeout=PW_TIMEOUT, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
        except Exception:
            page.goto("https://duckduckgo.com/?q=" + quote(query),
                      timeout=PW_TIMEOUT, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

        raw = page.evaluate("""() => {
            const items = [];
            const seen = new Set();
            const add = (title, url, snippet) => {
                if (title && url && url.startsWith('http') && !seen.has(url)) {
                    seen.add(url);
                    items.push({title, url, snippet});
                }
            };
            const sels = [
                'article[data-testid="result"]',
                'li[data-layout="organic"]',
                '.result',
                '.web-result',
            ];
            for (const sel of sels) {
                document.querySelectorAll(sel).forEach(el => {
                    const a = el.querySelector('a[href^="http"]');
                    const t = el.querySelector('h2, [data-testid="result-title-a"], .result__a, .result__title');
                    const s = el.querySelector('[data-testid="result-snippet"], .result__snippet, .result__body');
                    if (a && t) add((t.innerText || t.textContent || '').trim(), a.href,
                                    s ? (s.innerText || s.textContent || '').trim() : '');
                });
                if (items.length > 0) break;
            }
            return items;
        }""")

        for r in raw:
            url = r["url"]
            if r["title"] and url and url not in seen and len(r["title"]) > 3:
                seen.add(url)
                out.append({"title": r["title"], "url": url,
                            "snippet": r["snippet"], "content": ""})
        print(f"[DDG:pw] {len(out)} 条", file=sys.stderr)
    except Exception as e:
        print(f"[DDG:pw] 错误: {e}", file=sys.stderr)
    finally:
        try: ctx.close()
        except Exception: pass
    return out[:max_results]


# ==================== 全文抓取 ====================
def fetch_full(url):
    start = time.time()
    print(f"[fetch] {url}", file=sys.stderr)
    init_browser()
    text = ""
    ctx = create_context()
    try:
        page = ctx.new_page()
        page.route(ROUTE_PATTERN, lambda r: r.abort())
        page.goto(url, timeout=FETCH_TIMEOUT, wait_until="domcontentloaded")
        page.wait_for_timeout(800)
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        text = page.evaluate("""() => {
            document.querySelectorAll('script,style,nav,header,footer,.ad,.ads,[class*="banner"],[id*="banner"],.sidebar,.comment,.popup,.modal,.cookie').forEach(e=>e.remove());
            for (const sel of ['article','main','.content','.post','.article','#content','#main','.entry-content','.post-content','[itemprop="articleBody"]']) {
                const m = document.querySelector(sel);
                if (m && m.innerText.length > 200) return m.innerText;
            }
            return document.body ? document.body.innerText : '';
        }""")
    except Exception as e:
        print(f"[fetch] 失败: {e}", file=sys.stderr)
    finally:
        try: ctx.close()
        except Exception: pass
    result = (text or "").strip()[:8000]
    print(f"[fetch] {len(result)}字 | {time.time() - start:.1f}s", file=sys.stderr)
    return result or "抓取失败"


# ==================== 主函数 ====================
def main():
    check_playwright()
    query, max_results, full, region = parse_args()
    if not query:
        print(json.dumps({"error": "no query"}, ensure_ascii=False))
        sys.exit(1)

    # 仅按 IP 归属判断（--region 仅为代理用户的手动覆盖）
    if region == "cn":
        in_china = True
    elif region == "intl":
        in_china = False
    else:
        in_china = detect_in_china()

    if in_china:
        print("[策略] IP 国内 → Bing CN", file=sys.stderr)
        results = search_bing(query, max_results)
        if not results:
            print("[策略] Bing 为空，兜底 → DDG", file=sys.stderr)
            results = search_duckduckgo(query, max_results)
    else:
        print("[策略] IP 国外 → DDG", file=sys.stderr)
        results = search_duckduckgo(query, max_results)
        if not results:
            print("[策略] DDG 为空，兜底 → Bing CN", file=sys.stderr)
            results = search_bing(query, max_results)

    # 全文抓取
    if full > 0 and results:
        for i in range(min(full, len(results))):
            results[i]["content"] = fetch_full(results[i]["url"])

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    finally:
        close_browser()
