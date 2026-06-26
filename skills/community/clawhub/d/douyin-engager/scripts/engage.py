#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Douyin Engager - 抖音自动互动脚本
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import argparse
import asyncio
import json
import random
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("请先安装 playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

BROWSER_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "douyin-engager" / "browser_data"
DOUYIN_URL = "https://www.douyin.com"
LOG_FILE = Path.home() / ".openclaw" / "workspace" / "skills" / "douyin-engager" / "engage_log.json"


async def close_popups(page):
    """关闭各种弹窗"""
    popup_selectors = [
        '[class*="login"] [class*="close"]',
        '[class*="login"] svg',
        'button[aria-label*="close"]',
        '[class*="modal"] [class*="close"]',
    ]
    for selector in popup_selectors:
        try:
            elements = await page.query_selector_all(selector)
            for el in elements:
                try:
                    await el.click(timeout=500)
                    print("  关闭弹窗...")
                    await asyncio.sleep(0.3)
                except:
                    pass
        except:
            pass
    await page.keyboard.press("Escape")
    await asyncio.sleep(0.2)


async def wait_for_login(page):
    """等待登录"""
    print("等待登录...")
    print("请在浏览器中扫码登录抖音账号")
    
    await close_popups(page)
    
    login_indicators = [
        '[class*="avatar"]',
        '[class*="user-info"]',
        'button[class*="publish"]',
    ]
    
    for attempt in range(120):
        for selector in login_indicators:
            try:
                el = await page.query_selector(selector)
                if el and await el.is_visible():
                    print("检测到登录状态!")
                    return True
            except:
                pass
        await asyncio.sleep(5)
        if attempt % 12 == 0 and attempt > 0:
            print(f"  仍在等待登录... ({attempt // 12} 分钟)")
    
    return False


async def search_videos(page, keyword):
    """搜索视频"""
    print(f"搜索关键词: {keyword}")
    
    await close_popups(page)
    
    search_selectors = [
        'input[placeholder*="搜索"]',
        'input[placeholder*="搜你感兴趣"]',
        '[class*="search"] input[type="text"]',
    ]
    
    search_input = None
    for selector in search_selectors:
        try:
            search_input = await page.wait_for_selector(selector, timeout=5000)
            if search_input:
                break
        except:
            continue
    
    if not search_input:
        print("未找到搜索框")
        return False
    
    await search_input.click()
    await search_input.fill("")
    await asyncio.sleep(0.2)
    await search_input.fill(keyword)
    await asyncio.sleep(0.3)
    await page.keyboard.press("Enter")
    
    print("等待搜索结果...")
    await asyncio.sleep(3)
    await close_popups(page)
    
    return True


async def get_video_links(page, count):
    """获取视频链接"""
    print(f"获取视频链接 (目标: {count})...")
    
    videos = []
    
    # 使用正确的选择器获取视频卡片中的链接
    for scroll in range(10):
        # 获取 li 元素中的视频链接
        elements = await page.query_selector_all('li a[href*="/video/"], div.search-result-card a[href*="/video/"]')
        for el in elements:
            try:
                href = await el.get_attribute("href")
                if href and "/video/" in href:
                    if not href.startswith("http"):
                        href = "https://www.douyin.com" + href
                    if href not in [v["url"] for v in videos]:
                        videos.append({"url": href})
                        print(f"  找到视频: {len(videos)}")
            except:
                pass
        
        if len(videos) >= count:
            break
        
        await page.evaluate("window.scrollBy(0, 2000)")
        await asyncio.sleep(2)
    
    print(f"  共找到 {len(videos)} 个视频链接")
    return videos[:count]


async def engage_on_video(context, url, comment):
    """对单个视频互动"""
    result = {"url": url, "commented": False, "followed": False, "error": None}
    page = None
    
    try:
        page = await context.new_page()
        await page.goto(url, timeout=30000)
        await asyncio.sleep(3)
        await close_popups(page)
        
        # 关注 - 先点关注
        follow_selectors = [
            'button:has-text("关注")',
        ]
        
        for selector in follow_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    text = await btn.inner_text()
                    if "已关注" not in text and "关注" in text:
                        await btn.click()
                        await asyncio.sleep(1)
                        result["followed"] = True
                        print(f"    关注成功")
                        break
            except:
                continue
        
        # 评论 - 点击评论入口
        try:
            comment_placeholder = await page.query_selector('[class*="comment-input-inner-container"], .GXmFLge7')
            if comment_placeholder:
                await comment_placeholder.click()
                await asyncio.sleep(1)
        except:
            pass
        
        # 评论 - 输入评论
        comment_selectors = [
            'combobox',
            'textarea',
            '[contenteditable="true"]',
        ]
        
        comment_input = None
        for selector in comment_selectors:
            try:
                comment_input = await page.wait_for_selector(selector, timeout=3000)
                if comment_input:
                    break
            except:
                continue
        
        if comment_input:
            await comment_input.click()
            await comment_input.fill(comment)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Enter")
            await asyncio.sleep(1)
            result["commented"] = True
            print(f"    评论成功")
        
    except Exception as e:
        result["error"] = str(e)[:50]
    finally:
        if page:
            try:
                await page.close()
            except:
                pass
    
    return result


def log_results(results):
    """保存日志"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "commented": sum(1 for r in results if r["commented"]),
        "followed": sum(1 for r in results if r["followed"]),
        "results": results
    }
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


async def main(keyword, comments, count, interval, test_mode):
    """主函数"""
    print("=" * 50)
    print("Douyin Engager - 抖音自动互动助手")
    print("=" * 50)
    print(f"关键词: {keyword}")
    print(f"视频数: {count}")
    print(f"间隔: {interval} 分钟")
    print(f"评论: {comments[0]}")
    print("=" * 50)
    
    BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        print("启动浏览器...")
        
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="zh-CN",
        )
        
        pages = browser.pages
        page = pages[0] if pages else await browser.new_page()
        
        print("打开抖音...")
        await page.goto(DOUYIN_URL, timeout=60000)
        await asyncio.sleep(2)
        
        if test_mode:
            print("\n测试模式: 浏览器已启动")
            print("请扫码登录，登录后按回车键关闭...")
            input()
            await browser.close()
            return
        
        await wait_for_login(page)
        await search_videos(page, keyword)
        
        videos = await get_video_links(page, count)
        
        if not videos:
            print("未找到视频")
            await browser.close()
            return
        
        print(f"\n找到 {len(videos)} 个视频，开始互动...\n")
        
        results = []
        for i, video in enumerate(videos, 1):
            print(f"[{i}/{len(videos)}] 处理视频...")
            
            comment = random.choice(comments)
            result = await engage_on_video(browser, video["url"], comment)
            results.append(result)
            
            status = []
            if result["commented"]:
                status.append("评论")
            if result["followed"]:
                status.append("关注")
            print(f"    结果: {', '.join(status) if status else '无操作'}")
            
            if i < len(videos):
                wait_time = interval * 60 + random.randint(-30, 30)
                print(f"    等待 {wait_time // 60} 分 {wait_time % 60} 秒...\n")
                await asyncio.sleep(wait_time)
        
        log_results(results)
        
        commented = sum(1 for r in results if r["commented"])
        followed = sum(1 for r in results if r["followed"])
        
        print("\n" + "=" * 50)
        print("互动完成!")
        print(f"评论成功: {commented}/{count}")
        print(f"关注成功: {followed}/{count}")
        print("=" * 50)
        
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抖音自动互动助手")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--comments", required=True, help="评论内容")
    parser.add_argument("--count", type=int, default=20, help="操作次数")
    parser.add_argument("--interval", type=int, default=3, help="间隔分钟数")
    parser.add_argument("--test", action="store_true", help="测试模式")
    
    args = parser.parse_args()
    comments_list = [c.strip() for c in args.comments.split("|") if c.strip()]
    
    if not comments_list:
        print("请提供评论内容")
        sys.exit(1)
    
    asyncio.run(main(args.keyword, comments_list, args.count, args.interval, args.test))
