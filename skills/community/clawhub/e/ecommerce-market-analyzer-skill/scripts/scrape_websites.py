#!/usr/bin/env python3
"""
批量抓取电商网站首页截图 - 增强版（处理弹窗）
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

# 目标网站列表
WEBSITES = [
    "amazon.de",
    "kleinanzeigen.de",
    "ebay.de",
    "temu.com",
    "idealo.de",
    "otto.de",
    "markt.de",
    "aliexpress.com",
    "etsy.com",
    "mydealz.de",
    "lidl.de",
    "eventim.de",
    "thalia.de",
    "tchibo.de",
    "zalando.de",
    "shein.com",
    "bonprix.de",
    "vinted.de",
    "aboutyou.de",
    "ikea.com",
    "obi.de",
    "kaufland.de",
    "rewe.de",
    "mediamarkt.de",
    "shop-apotheke.com",
]


async def close_popups(page):
    """
    尝试关闭常见的弹窗
    """
    # 常见的弹窗关闭按钮选择器
    popup_selectors = [
        # Cookie 同意弹窗
        'button:has-text("Alle akzeptieren")',
        'button:has-text("Accept all")',
        'button:has-text("Akzeptieren")',
        'button:has-text("Alle annehmen")',
        'button:has-text("Einverstanden")',
        'button:has-text("Zustimmen")',
        'button:has-text("OK")',
        'button:has-text("Verstanden")',
        'button[id*="accept"]',
        'button[class*="accept"]',
        'button[id*="cookie"]',
        'button[class*="cookie"]',
        '#onetrust-accept-btn-handler',
        '.cookie-consent-accept',

        # 关闭按钮
        'button[aria-label*="close"]',
        'button[aria-label*="Close"]',
        'button[aria-label*="schließen"]',
        'button[aria-label*="Schließen"]',
        'button.close',
        'button[class*="close"]',
        '[class*="close-button"]',
        'button:has-text("×")',
        'button:has-text("✕")',

        # Newsletter/Newsletter弹窗
        'button:has-text("Nein")',
        'button:has-text("Später")',
        'button:has-text("Nicht jetzt")',
        'button:has-text("No thanks")',

        # 特定网站的选择器
        '.uc-deny-all-button',  # Kleinanzeigen
        '#sp_message_iframe_953358',  # 某些网站
        '[data-testid="uc-accept-all-button"]',
        '[data-testid="cookie-accept-all"]',
    ]

    # 尝试关闭弹窗
    for selector in popup_selectors:
        try:
            # 等待最多2秒，如果找到就点击
            button = page.locator(selector).first
            if await button.is_visible(timeout=2000):
                await button.click(timeout=2000)
                print(f"  ✓ 关闭弹窗: {selector}")
                await asyncio.sleep(1)  # 等待弹窗消失
                break
        except Exception:
            continue


async def handle_country_selector(page, url):
    """
    处理国家/语言选择器（如Vinted）
    """
    try:
        # Vinted - 选择德国
        if "vinted" in url:
            germany_selector = 'button:has-text("Germany")'
            if await page.locator(germany_selector).first.is_visible(timeout=3000):
                await page.locator(germany_selector).first.click()
                print(f"  ✓ 选择了德国地区")
                await asyncio.sleep(2)
    except Exception:
        pass


async def capture_homepage(browser, url: str, output_dir: Path):
    """抓取单个网站首页"""
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        locale="de-DE",  # 设置德语地区
        timezone_id="Europe/Berlin",  # 柏林时区
    )
    page = await context.new_page()

    try:
        print(f"正在访问: {url}")
        full_url = f"https://www.{url}" if not url.startswith("http") else url

        # 访问页面
        await page.goto(full_url, wait_until="domcontentloaded", timeout=60000)

        # 等待页面基本加载
        await asyncio.sleep(3)

        # 处理国家选择器
        await handle_country_selector(page, url)

        # 关闭弹窗
        await close_popups(page)

        # 再次尝试关闭可能的二级弹窗
        await asyncio.sleep(1)
        await close_popups(page)

        # 等待页面稳定
        await asyncio.sleep(2)

        # 截图
        screenshot_path = output_dir / f"{url}.png"
        await page.screenshot(
            path=str(screenshot_path),
            full_page=True,
            timeout=60000
        )
        print(f"✓ 已保存: {screenshot_path}")

        # 保存HTML
        html_content = await page.content()
        html_path = output_dir / f"{url}.html"
        html_path.write_text(html_content, encoding="utf-8")
        print(f"✓ 已保存HTML: {html_path}")

        return {"url": url, "status": "success"}

    except Exception as e:
        print(f"✗ 失败 {url}: {str(e)}")

        # 即使失败也尝试截图当前状态
        try:
            screenshot_path = output_dir / f"{url}_error.png"
            await page.screenshot(path=str(screenshot_path), timeout=10000)
            print(f"  保存了错误截图: {screenshot_path}")
        except:
            pass

        return {"url": url, "status": "failed", "error": str(e)}

    finally:
        await context.close()


async def main():
    """主函数"""
    # 创建输出目录
    output_dir = Path("screenshots_clean")
    output_dir.mkdir(exist_ok=True)

    print(f"开始抓取 {len(WEBSITES)} 个网站（处理弹窗版本）...")
    print("=" * 60)

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)

        results = []

        # 逐个抓取
        for url in WEBSITES:
            result = await capture_homepage(browser, url, output_dir)
            results.append(result)
            # 短暂延迟
            await asyncio.sleep(2)

        await browser.close()

    # 打印总结
    print("=" * 60)
    print("\n抓取完成！")
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = sum(1 for r in results if r["status"] == "failed")
    print(f"成功: {success_count}/{len(WEBSITES)}")
    print(f"失败: {failed_count}/{len(WEBSITES)}")

    if failed_count > 0:
        print("\n失败的网站:")
        for r in results:
            if r["status"] == "failed":
                print(f"  - {r['url']}: {r.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main())
