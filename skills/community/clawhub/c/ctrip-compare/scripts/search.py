#!/usr/bin/env python3
"""携程跟团游搜索页产品URL提取脚本（Playwright + CDP）"""
import asyncio
import argparse
import io
import json
import os
import re
import sys
import urllib.request


def _ensure_utf8_output():
    """确保 stdout/stderr 使用 UTF-8 编码，兼容 Windows/Linux/macOS"""
    for name in ('stdout', 'stderr'):
        stream = getattr(sys, name)
        if hasattr(stream, 'buffer') and hasattr(stream, 'encoding'):
            try:
                stream.write('\u2713')
                stream.flush()
            except (UnicodeEncodeError, UnicodeDecodeError):
                setattr(sys, name, io.TextIOWrapper(
                    stream.buffer, encoding='utf-8', errors='replace'
                ))


_ensure_utf8_output()


async def extract_product_ids(page):
    """从页面提取所有产品ID（优先从 data-track-product-id，备选从 a 标签）"""
    # 方式1：从产品卡片的 data-track-product-id 属性提取
    ids = await page.eval_on_selector_all(
        '[data-track-product-id]',
        'els => els.map(el => el.getAttribute("data-track-product-id"))'
    )
    if ids:
        return [pid for pid in ids if pid and pid.isdigit()]

    # 方式2：备选，从链接中提取
    links = await page.eval_on_selector_all(
        'a[href*="/detail/p"]',
        'els => els.map(el => el.href)'
    )
    product_ids = []
    for href in links:
        match = re.search(r'/detail/p(\d+)', href)
        if match:
            product_ids.append(match.group(1))
    return product_ids


async def scroll_to_load(page, max_products=100):
    """滚动页面确保所有产品卡片渲染，返回产品ID列表"""
    seen = set()
    no_new_rounds = 0
    max_no_new_rounds = 3

    print("开始加载产品...")

    while no_new_rounds < max_no_new_rounds and len(seen) < max_products:
        before = len(seen)

        # 提取当前可见的产品ID
        ids = await extract_product_ids(page)
        for pid in ids:
            seen.add(pid)

        new_count = len(seen) - before

        if new_count == 0:
            # 尝试滚动触发更多加载
            await page.evaluate('window.scrollBy(0, window.innerHeight * 0.6)')
            await page.wait_for_timeout(2000)
            no_new_rounds += 1
            print(f"  加载中... 当前 {len(seen)} 个产品（无新增 {no_new_rounds}/{max_no_new_rounds}）")
        else:
            no_new_rounds = 0
            print(f"  加载中... 当前 {len(seen)} 个产品（+{new_count}）")

        if len(seen) >= max_products:
            print(f"  已达上限 {max_products}，停止")
            break

    return list(seen)


async def main():
    parser = argparse.ArgumentParser(description='携程搜索页产品URL提取')
    parser.add_argument('url', help='携程搜索列表页URL')
    parser.add_argument('--max', type=int, default=100, help='最多提取产品数（默认100，上限100）')
    args = parser.parse_args()

    max_products = min(args.max, 100)

    # 连接浏览器CDP
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=5)
        info = json.loads(resp.read())
        ws_url = info['webSocketDebuggerUrl']
    except Exception as e:
        print(f"✗ 无法连接到浏览器CDP: {e}")
        print("  请确保 Chromium 系浏览器（Chrome/Edge/Brave）已启动且带 --remote-debugging-port=9222 参数")
        sys.exit(2)

    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        page = await context.new_page()

        print(f"=== 携程搜索结果提取 ===")
        print(f"搜索页: {args.url}")
        print(f"上限: {max_products}")
        print()

        try:
            print("正在打开搜索页...")
            await page.goto(args.url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(5000)  # 等待动态内容充分加载

            # 加载并提取产品ID
            product_ids = await scroll_to_load(page, max_products)

        except Exception as e:
            print(f"✗ 提取失败: {e}")
            sys.exit(1)
        finally:
            await page.close()

    # 拼接产品URL并输出
    urls = [f"https://vacations.ctrip.com/travel/detail/p{pid}" for pid in product_ids]

    print()
    print(f"=== 提取完成 ===")
    print(f"找到产品: {len(urls)} 个")
    print()
    for url in urls:
        print(url)


if __name__ == '__main__':
    asyncio.run(main())
