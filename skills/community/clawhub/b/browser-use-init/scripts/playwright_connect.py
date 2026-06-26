"""
playwright_connect.py - 用 Playwright 直连 CDP Chrome 执行页面操作

当 browser-use Agent + LLM 效果不佳时，用此脚本直接操作页面。
适合：提取页面内容、截图、填表单等确定性操作。

环境变量配置:
    CDP_PORT    CDP 调试端口（默认 9222）

用法示例（在代码中引入）:
    from playwright_connect import get_page
    page = await get_page()
    await page.goto("https://example.com")
    text = await page.inner_text("body")

或直接运行演示:
    python playwright_connect.py --url https://www.example.com --screenshot output.png
"""

import asyncio, sys, io, urllib.request, json, argparse, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DEFAULT_PORT = int(os.getenv("CDP_PORT", "9222"))


def get_ws_url(port=None):
    p = port or DEFAULT_PORT
    resp = urllib.request.urlopen(f"http://localhost:{p}/json/version", timeout=3)
    return json.loads(resp.read())["webSocketDebuggerUrl"]


async def get_page(port=None):
    """返回 (playwright, browser, page) 三元组，调用方负责清理"""
    from playwright.async_api import async_playwright
    ws_url = get_ws_url(port)
    pw = await async_playwright().start()
    browser = await pw.chromium.connect_over_cdp(ws_url)
    context = browser.contexts[0]
    page = context.pages[0] if context.pages else await context.new_page()
    return pw, browser, page


async def demo(url: str, screenshot: str = None):
    pw, browser, page = await get_page()
    try:
        print(f"[*] 导航到: {url}")
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=10000)

        title = await page.title()
        cur_url = page.url
        print(f"[OK] 标题: {title}")
        print(f"[OK] URL: {cur_url}")

        if screenshot:
            await page.screenshot(path=screenshot)
            print(f"[OK] 截图已保存: {screenshot}")
    finally:
        await pw.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Playwright 直连 Chrome CDP 演示")
    parser.add_argument("--url", default="https://www.example.com", help="要访问的网址")
    parser.add_argument("--screenshot", default=None, help="截图输出路径")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                       help=f"CDP 调试端口（默认来自 $CDP_PORT 环境变量或 {DEFAULT_PORT}）")
    args = parser.parse_args()
    asyncio.run(demo(args.url, args.screenshot))
