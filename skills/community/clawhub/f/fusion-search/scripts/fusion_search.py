#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fusion_search.py — Fusion Search 主入口
融合 Playwright + stealth.js 反爬 + 16引擎智能路由
"""

import json
import sys
import time
import re
import argparse
from urllib.parse import urlparse, urlencode, quote

from playwright.sync_api import sync_playwright

from engines import ENGINES, ENGINE_COOLDOWN
from router import route_query, build_engine_url
from scorer import (
    score_result, score_results, get_dominant_domain,
    rewrite_query, merge_and_deduplicate,
    filter_low_quality, LOW_QUALITY_DOMAINS
)


# ── 浏览器单例 ──
_browser = None
_playwright = None
_last_request_time = 0.0
_engine_last_used = {}
MIN_REQUEST_INTERVAL = 3.0


def init_browser():
    global _browser, _playwright
    if _browser:
        return _browser
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--disable-extensions',
            '--disable-background-networking',
            '--disable-sync',
            '--metrics-recording-only',
            '--disable-default-apps',
            '--no-first-run',
            '--disable-component-extensions-with-background-pages',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-site-isolation-trials',
            '--disable-web-security',
            '--allow-running-insecure-content',
        ]
    )
    return _browser


def close_browser():
    global _browser, _playwright
    if _browser:
        try:
            _browser.close()
        except Exception:
            pass
        _browser = None
    if _playwright:
        try:
            _playwright.stop()
        except Exception:
            pass
        _playwright = None


def get_stealth_js():
    """读取内联 stealth.js"""
    import os
    js_path = os.path.join(os.path.dirname(__file__), "stealth.js")
    with open(js_path, "r", encoding="utf-8") as f:
        return f.read()


def throttle():
    """请求节流 ≥ 3s"""
    global _last_request_time
    gap = MIN_REQUEST_INTERVAL - (time.time() - _last_request_time)
    if gap > 0:
        time.sleep(gap)
    _last_request_time = time.time()


def engine_cooldown(name):
    """引擎切换冷却 ≥ 2s"""
    last = _engine_last_used.get(name, 0)
    gap = ENGINE_COOLDOWN - (time.time() - last)
    if gap > 0:
        time.sleep(gap)
    _engine_last_used[name] = time.time()


def extract_results(page, engine_name, count=10):
    """使用引擎的 DOM 选择器解析搜索结果"""
    cfg = ENGINES.get(engine_name)
    if not cfg:
        return []

    selector = cfg.get("selector", "")
    title_sel = cfg.get("title_sel", "")
    snippet_sel = cfg.get("snippet_sel", "")

    if not selector:
        return []

    results = []
    try:
        items = page.query_selector_all(selector)
        for item in items[:count]:
            try:
                # Title
                title_el = item.query_selector(title_sel) if title_sel else None
                if not title_el:
                    continue
                title = title_el.inner_text().strip()
                href = title_el.get_attribute("href") or ""

                # URL 处理（相对路径补全）
                url = href
                if url.startswith("/"):
                    parsed = urlparse(cfg["url"])
                    url = f"{parsed.scheme}://{parsed.netloc}{url}"
                elif not url.startswith("http"):
                    continue

                # Snippet
                snippet_el = item.query_selector(snippet_sel) if snippet_sel else None
                snippet = snippet_el.inner_text().strip() if snippet_el else ""

                results.append({
                    "title": title[:200],
                    "url": url,
                    "snippet": snippet[:300],
                    "content": "",
                    "engine": engine_name,
                })
            except Exception:
                continue
    except Exception:
        pass

    return results


def fetch_full_content(page, url, timeout=8000):
    """全文抓取"""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        time.sleep(1.5)
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

        # 删除干扰元素
        page.evaluate("""() => {
            for (const s of document.querySelectorAll(
                'script, style, nav, header, footer, .ad, .sidebar, ' +
                '.comment, .popup, .modal, .cookie, .advertisement, ' +
                'noscript, iframe, .related, .recommend, .share'
            )) s.remove();
        }""")

        # 优先找主要内容区域
        content = page.evaluate("""() => {
            const main = document.querySelector('article, main, .content, ' +
                '.post, .article, #content, #main, .entry-content, ' +
                '.post-content, [role="main"]');
            if (main) return main.innerText;
            return document.body ? document.body.innerText : '';
        }""")

        content = re.sub(r'\s+', ' ', content).strip()
        return content[:8000]
    except Exception:
        return ""


def search_engine_with_playwright(browser, engine_name, query, count=10,
                                   freshness=None,
                                   max_retries=2, timeout=30):
    """使用 Playwright 搜索单个引擎"""
    engine_cooldown(engine_name)
    throttle()

    ctx = None
    page = None
    results = []

    try:
        ctx = browser.new_context(
            locale="zh-CN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080},
            device_scale_factor=1,
            timezone_id="Asia/Shanghai",
            has_touch=False,
            is_mobile=False,
            java_script_enabled=True,
        )

        # 注入 stealth.js
        stealth_js = get_stealth_js()
        if stealth_js:
            ctx.add_init_script(stealth_js)

        page = ctx.new_page()

        # 拦截无用资源
        page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,mp4,ico,webp,js.map}",
                    lambda route: route.abort())

        # 构建 URL
        url = build_engine_url(engine_name, query, count=count,
                               freshness=freshness)

        # 搜索
        for attempt in range(max_retries + 1):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(2)
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass

                results = extract_results(page, engine_name, count=count)

                # 0结果检测 + 退避
                if len(results) == 0 and attempt < max_retries:
                    wait = 5 * (attempt + 1)
                    time.sleep(wait)
                    continue

                break
            except Exception as e:
                if attempt < max_retries:
                    time.sleep(5 * (attempt + 1))
                    continue
                print(f"[WARN] {engine_name} error: {e}", file=sys.stderr)
                return []

    except Exception as e:
        print(f"[WARN] {engine_name} browser error: {e}", file=sys.stderr)
        return []
    finally:
        if page:
            try:
                page.close()
            except Exception:
                pass
        if ctx:
            try:
                ctx.close()
            except Exception:
                pass

    return results


def _fetch_full_for_results(browser, results, count):
    """在最终合并结果上执行全文抓取（后置）"""
    if not results or count <= 0:
        return
    ctx = None
    page = None
    try:
        ctx = browser.new_context(
            locale="zh-CN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
        )
        stealth_js = get_stealth_js()
        if stealth_js:
            ctx.add_init_script(stealth_js)
        page = ctx.new_page()
        page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,mp4,ico,webp,js.map}",
                    lambda route: route.abort())
        for i, r in enumerate(results[:count]):
            content = fetch_full_content(page, r["url"], timeout=10000)
            if content:
                results[i]["content"] = content
    except Exception as e:
        print(f"[WARN] Full content fetch error: {e}", file=sys.stderr)
    finally:
        if page:
            try:
                page.close()
            except Exception:
                pass
        if ctx:
            try:
                ctx.close()
            except Exception:
                pass


def search(query, max_results=10, full_content=0, engine="auto",
           filter_low_quality_flag=True, rewrite=True,
           freshness=None, max_retries=2, timeout=30):
    """
    主搜索函数

    参数：
        query: 搜索关键词
        max_results: 最大返回结果数 (1-20)
        full_content: 前N条全文抓取 (0-5)
        engine: auto/baidu/bing_cn/google/duckduckgo/brave/sogou
        filter_low_quality_flag: 过滤低质量域名
        rewrite: 自动改写query
        freshness: hour/day/week/month/year
        max_retries: 单引擎最大重试
        timeout: 超时秒数

    返回：
        [{title, url, snippet, content, engine, score}]
    """
    route = route_query(query, engine=engine, max_results=max_results,
                        freshness=freshness)
    engine_chain = route["chain"]
    target_full = route.get("full", full_content)

    if rewrite:
        q_rewritten, rewrite_reason = rewrite_query(query)
        if rewrite_reason:
            print(f"[INFO] Query rewrite: '{query}' -> '{q_rewritten}' ({rewrite_reason})",
                  file=sys.stderr)
            query = q_rewritten

    browser = init_browser()

    all_results = []
    used_query = query

    for attempt in range(3):  # 外层重试（改写/排除）
        all_results = []

        for eng in engine_chain:
            if eng == "wolframalpha":
                continue

            eng_results = search_engine_with_playwright(
                browser, eng, used_query, count=max_results + len(all_results),
                freshness=freshness,
                max_retries=max_retries, timeout=timeout
            )
            all_results.append(eng_results)

            # ★ 主引擎（chain[0]）有足够结果 → 跳过剩余引擎
            if eng == engine_chain[0] and len(eng_results) >= max_results * 0.5:
                break

        # 合并去重
        merged = merge_and_deduplicate(all_results, max_results=max_results)

        # 质量评分
        avg_score = score_results(merged) if merged else 0.0

        # 单域名集中检测
        dom, dom_count, total = get_dominant_domain(merged)
        if dom and total > 3 and dom_count > total * 0.5 and attempt == 0:
            # 排除集中域名重试
            excluded = [dom]
            for eng in engine_chain:
                if eng not in ["google", "wolframalpha", "duckduckgo"]:
                    continue
                excl_query = used_query + " " + " ".join(
                    f"-site:{d}" for d in excluded
                )
                eng_results = search_engine_with_playwright(
                    browser, eng, excl_query, count=max_results,
                    freshness=freshness,
                    max_retries=1, timeout=timeout
                )
                all_results.append(eng_results)
            merged = merge_and_deduplicate(all_results, max_results=max_results)
            break

        # 低分改写重试
        if avg_score < 0.45 and attempt == 0 and rewrite:
            q_rewritten2, _ = rewrite_query(used_query)
            if q_rewritten2 and q_rewritten2 != used_query:
                used_query = q_rewritten2
                print(f"[INFO] Low quality ({avg_score:.2f}), retry with: '{used_query}'",
                      file=sys.stderr)
                continue

        break

    # 过滤低质量域名
    if filter_low_quality_flag:
        merged = filter_low_quality(merged, do_filter=True)

    # 质量分重排序
    for r in merged:
        if "score" not in r:
            r["score"] = score_result(r)
    merged.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    # 后置全文抓取（只在最终结果上执行）
    effective_full = target_full or full_content
    if effective_full > 0 and merged:
        _fetch_full_for_results(browser, merged, effective_full)

    return merged[:max_results]


def search_simple(query, max_results=10, full_content=0, engine="auto"):
    """简化的搜索接口"""
    return search(
        query=query,
        max_results=max_results,
        full_content=full_content,
        engine=engine,
    )


# ── CLI ──
def main():
    parser = argparse.ArgumentParser(description="Fusion Search - 16引擎融合搜索")
    parser.add_argument("query", type=str, help="搜索关键词")
    parser.add_argument("--max", type=int, default=10, help="最大返回结果数 (1-20)")
    parser.add_argument("--full", type=int, default=0, help="前N条全文 (0-5)")
    parser.add_argument("--engine", type=str, default="auto",
                        help="搜索引擎: auto/baidu/bing_cn/google/duckduckgo/brave/sogou")
    parser.add_argument("--no-filter", action="store_true", help="禁用低质量域名过滤")
    parser.add_argument("--no-rewrite", action="store_true", help="禁用query改写")
    parser.add_argument("--freshness", type=str, default=None,
                        help="时效: hour/day/week/month/year")
    parser.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    try:
        results = search(
            query=args.query,
            max_results=min(args.max, 20),
            full_content=min(args.full, 5),
            engine=args.engine,
            filter_low_quality_flag=not args.no_filter,
            rewrite=not args.no_rewrite,
            freshness=args.freshness,
        )

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            if not results:
                print("⚠️ No results found.")
                return
            for i, r in enumerate(results, 1):
                score = r.get("score", 0.0)
                print(f"{i}. [{r['engine']}] {r['title']} (评分: {score:.2f})")
                print(f"   {r['url']}")
                print(f"   {r['snippet'][:100]}...")
                if r.get("content"):
                    print(f"   [全文: {len(r['content'])}字]")
                print()
            print(f"--- {len(results)} results ---")
    finally:
        close_browser()


if __name__ == "__main__":
    main()
