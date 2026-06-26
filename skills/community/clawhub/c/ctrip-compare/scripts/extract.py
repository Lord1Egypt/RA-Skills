#!/usr/bin/env python3
"""携程跟团游产品数据提取脚本（Playwright + CDP）"""
import asyncio
import re
import sys
import os
import io
import json
import time


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

async def extract_product(browser, url, day, output_dir):
    """提取单个产品的完整数据"""
    context = browser.contexts[0]
    page = await context.new_page()

    result = {
        "url": url,
        "product_id": "",
        "title": "",
        "departure_date": f"{day}号",
        "price": "",
        "score": "",
        "supplier": "",
        "itinerary": "",
        "error": ""
    }

    try:
        # 1. 打开页面（等待网络空闲，确保重定向完成）
        print(f"  [1/5] 打开页面: {url}")
        await page.goto(url, wait_until='networkidle', timeout=60000)
        await page.wait_for_selector('h1', timeout=15000)
        await page.wait_for_timeout(3000)  # 额外等待动态内容加载

        # 2. 点击出发日期获取真实价格
        print(f"  [2/5] 点击出发日期({day}号)")
        try:
            # 找到日期元素并点击
            date_elements = await page.query_selector_all('.date_num')
            for el in date_elements:
                text = (await el.inner_text()).strip()
                if text == str(day):
                    await el.click()
                    await page.wait_for_timeout(3000)
                    break
        except Exception as e:
            print(f"       点击日期失败: {e}，使用默认价格")

        # 3. 获取完整页面文本
        print(f"  [3/5] 获取页面文本")
        body_text = await page.evaluate("document.body.innerText")

        # 4. 从全文中提取字段
        print(f"  [4/5] 解析字段")

        # 标题
        h1 = await page.query_selector('h1')
        if h1:
            result['title'] = (await h1.inner_text()).strip()

        # 产品ID - 从URL或页面提取
        pid_match = re.search(r'/p(\d+)', url)
        if pid_match:
            result['product_id'] = pid_match.group(1)
        else:
            id_match = re.search(r'编号：(\d+)', body_text)
            if id_match:
                result['product_id'] = id_match.group(1)

        # 价格 - 多种模式匹配
        price_patterns = [
            r'¥?(\d{3,5})/人起',
            r'(\d{3,5})\s*/\s*人起',
            r'(\d{3,5})\s*元/人',
            r'总价.*?(\d{3,5})',
        ]
        for pattern in price_patterns:
            m = re.search(pattern, body_text)
            if m:
                result['price'] = m.group(1)
                break

        # 评分
        score_match = re.search(r'([\d.]+)分.*?(\d+)条点评', body_text)
        if score_match:
            result['score'] = f"{score_match.group(1)}/{score_match.group(2)}条"

        # 供应商
        supplier_match = re.search(r'供应商\s*\n?\s*(.+?)[\n,，]', body_text)
        if supplier_match:
            result['supplier'] = supplier_match.group(1).strip()

        # 5. 提取行程（图文行程模式）
        print(f"  [5/5] 提取行程")
        itinerary_items = await page.query_selector_all('DIV.daily_itinerary_item')
        if itinerary_items:
            itinerary_parts = []
            for i, item in enumerate(itinerary_items):
                text = (await item.inner_text()).strip()
                # 清理多余空白
                text = re.sub(r'\n{3,}', '\n\n', text)
                itinerary_parts.append(f"=== Day {i+1} ===\n{text}")
            result['itinerary'] = '\n\n'.join(itinerary_parts)
        else:
            # 尝试日历行程模式
            calendar_rows = await page.query_selector_all('TR.js_scheduleItemCalendar')
            if calendar_rows:
                itinerary_parts = []
                for i, row in enumerate(calendar_rows):
                    text = (await row.inner_text()).strip()
                    itinerary_parts.append(f"=== Day {i+1} ===\n{text}")
                result['itinerary'] = '\n\n'.join(itinerary_parts)
            else:
                result['itinerary'] = "未找到行程数据"

        # 保存文件
        filename = os.path.join(output_dir, f"p{result['product_id']}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"===== p{result['product_id']} =====\n")
            f.write(f"标题: {result['title']}\n")
            f.write(f"产品ID: {result['product_id']}\n")
            f.write(f"出发日期: {result['departure_date']}\n")
            f.write(f"价格: ¥{result['price']}/人\n")
            f.write(f"评分: {result['score']}\n")
            f.write(f"供应商: {result['supplier']}\n")
            f.write(f"URL: {result['url']}\n")
            f.write(f"\n{result['itinerary']}\n")

        print(f"  ✓ 已保存: p{result['product_id']}.txt (¥{result['price']}/人)")
        result['success'] = True

    except Exception as e:
        result['error'] = str(e)
        result['success'] = False
        print(f"  ✗ 提取失败: {e}")
    finally:
        await page.close()

    return result


async def main():
    if len(sys.argv) < 4:
        print("用法: python extract.py <出发日期> <输出目录> <url1> [url2] ...")
        print("示例: python extract.py 30 ~/ctrip/ctrip_20260430_云南/raw https://vacations.ctrip.com/tour/detail/p30642209s34")
        sys.exit(1)

    day = int(sys.argv[1])
    output_dir = sys.argv[2]
    urls = sys.argv[3:]

    os.makedirs(output_dir, exist_ok=True)

    print(f"=== 携程产品提取 ===")
    print(f"出发日期: {day}号")
    print(f"产品数量: {len(urls)}")
    print(f"输出目录: {output_dir}")
    print()

    # 获取 WebSocket URL
    import urllib.request
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=5)
        info = json.loads(resp.read())
        ws_url = info['webSocketDebuggerUrl']
    except Exception as e:
        print(f"✗ 无法连接到浏览器CDP: {e}")
        print("  请确保 Chromium 系浏览器（Chrome/Edge/Brave）已启动且带 --remote-debugging-port=9222 参数")
        sys.exit(1)

    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)

        results = []
        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] 处理中...")
            r = await extract_product(browser, url, day, output_dir)
            results.append(r)
            if i < len(urls) - 1:
                await asyncio.sleep(1)  # URL之间短暂等待

    # 汇总
    print()
    print("=== 提取完成 ===")
    success = sum(1 for r in results if r.get('success'))
    failed = sum(1 for r in results if not r.get('success'))
    print(f"成功: {success}  失败: {failed}")
    for r in results:
        status = "✓" if r.get('success') else "✗"
        print(f"  {status} p{r['product_id']}: ¥{r['price']}/人 - {r['title'][:30]}...")


if __name__ == '__main__':
    asyncio.run(main())
