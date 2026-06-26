# -*- coding: utf-8 -*-
"""
Douyin Auto Engager - 自动评论关注脚本
"""
import asyncio
import json
import random
import sys
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

# 配置
KEYWORD = "正念"
COMMENT = "每日正念帮你按下暂停键"
COUNT = 20
INTERVAL_MINUTES = 3
BROWSER_DATA = Path(r"C:\Users\User\.openclaw\workspace\skills\douyin-engager\browser_data")
LOG_FILE = Path(r"C:\Users\User\.openclaw\workspace\skills\douyin-engager\engage_log.json")

# 已完成的视频
completed = 2  # 已经手动完成了2个视频


async def main():
    print("=" * 50)
    print(f"抖音自动互动脚本")
    print(f"关键词: {KEYWORD}")
    print(f"评论: {COMMENT}")
    print(f"目标: {COUNT} 个视频")
    print(f"间隔: {INTERVAL_MINUTES} 分钟")
    print(f"已完成: {completed} 个视频")
    print("=" * 50)
    
    BROWSER_DATA.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        print("启动浏览器...")
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA),
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="zh-CN"
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        print("打开抖音...")
        await page.goto("https://www.douyin.com", timeout=60000)
        await asyncio.sleep(2)
        
        print("搜索关键词...")
        search_box = await page.wait_for_selector('input[placeholder*="搜索"]', timeout=10000)
        await search_box.click()
        await search_box.fill(KEYWORD)
        await page.keyboard.press("Enter")
        await asyncio.sleep(5)
        
        print("获取视频链接...")
        video_links = []
        
        # 滚动页面获取更多视频
        for scroll in range(10):
            # 获取所有视频链接
            links = await page.query_selector_all('li[data-e2e^="search-"] a, a[href*="/video/"], a[href*="/note/"]')
            for link in links:
                try:
                    href = await link.get_attribute("href")
                    if href:
                        if "/video/" in href or "/note/" in href:
                            if not href.startswith("http"):
                                href = "https://www.douyin.com" + href
                            if href not in video_links:
                                video_links.append(href)
                                print(f"  找到视频: {len(video_links)}")
                except:
                    pass
            
            if len(video_links) >= COUNT:
                break
            
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(1)
        
        video_links = video_links[:COUNT]
        print(f"共找到 {len(video_links)} 个视频链接")
        
        if not video_links:
            print("未找到视频链接!")
            await browser.close()
            return
        
        # 开始互动
        results = []
        
        for idx, url in enumerate(video_links, 1):
            if idx <= completed:
                print(f"[{idx}/{len(video_links)}] 跳过（已完成）")
                continue
            
            print(f"\n[{idx}/{len(video_links)}] 处理视频...")
            
            # 打开新标签页
            video_page = await browser.new_page()
            
            try:
                await video_page.goto(url, timeout=30000)
                await asyncio.sleep(3)
                
                commented = False
                followed = False
                
                # 评论
                try:
                    comment_box = await video_page.wait_for_selector(
                        'textarea[placeholder*="评论"], textarea[placeholder*="善语"]',
                        timeout=5000
                    )
                    await comment_box.click()
                    await comment_box.fill(COMMENT)
                    await asyncio.sleep(0.3)
                    await video_page.keyboard.press("Enter")
                    await asyncio.sleep(1)
                    print(f"  ✅ 评论成功")
                    commented = True
                except Exception as e:
                    print(f"  ❌ 评论失败: {str(e)[:50]}")
                
                # 关注
                try:
                    follow_btn = await video_page.query_selector('button:has-text("关注"):not(:has-text("已关注"))')
                    if follow_btn:
                        await follow_btn.click()
                        await asyncio.sleep(0.5)
                        print(f"  ✅ 关注成功")
                        followed = True
                    else:
                        print(f"  ⏭️ 已关注或未找到关注按钮")
                except Exception as e:
                    print(f"  ❌ 关注失败: {str(e)[:50]}")
                
                results.append({
                    "url": url,
                    "commented": commented,
                    "followed": followed
                })
                
            except Exception as e:
                print(f"  ❌ 处理失败: {str(e)[:50]}")
            
            finally:
                await video_page.close()
            
            # 等待间隔（最后一个不需要等待）
            if idx < len(video_links):
                wait_seconds = INTERVAL_MINUTES * 60 + random.randint(-30, 30)
                print(f"  ⏳ 等待 {wait_seconds // 60} 分 {wait_seconds % 60} 秒...")
                await asyncio.sleep(wait_seconds)
        
        # 保存日志
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "total": len(results) + completed,
            "commented": sum(1 for r in results if r["commented"]) + completed,
            "followed": sum(1 for r in results if r["followed"]) + completed,
            "results": results
        }
        
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 50)
        print("互动完成!")
        print(f"评论成功: {log_data['commented']}/{log_data['total']}")
        print(f"关注成功: {log_data['followed']}/{log_data['total']}")
        print("=" * 50)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
