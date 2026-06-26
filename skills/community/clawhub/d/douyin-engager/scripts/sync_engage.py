# -*- coding: utf-8 -*-
"""
Douyin Auto Engager - 同步版本
"""
import time
import random
import json
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

# 配置
KEYWORD = "正念"
COMMENT = "每日正念帮你按下暂停键"
COUNT = 20
INTERVAL_MINUTES = 3
BROWSER_DATA = Path(r"C:\Users\User\.openclaw\workspace\skills\douyin-engager\browser_data")
LOG_FILE = Path(r"C:\Users\User\.openclaw\workspace\skills\douyin-engager\engage_log.json")

# 已完成的视频（之前用浏览器工具完成了2个）
completed = 2


def main():
    print("=" * 50)
    print(f"抖音自动互动脚本 (同步版)")
    print(f"关键词: {KEYWORD}")
    print(f"评论: {COMMENT}")
    print(f"目标: {COUNT} 个视频")
    print(f"间隔: {INTERVAL_MINUTES} 分钟")
    print(f"已完成: {completed} 个视频")
    print("=" * 50)
    
    BROWSER_DATA.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        print("\n启动浏览器...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA),
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="zh-CN"
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print("打开抖音...")
        page.goto("https://www.douyin.com", timeout=60000)
        time.sleep(3)
        
        # 检查登录状态
        print("检查登录状态...")
        try:
            avatar = page.query_selector('[class*="avatar"], [class*="user-info"]')
            if avatar:
                print("✅ 已登录")
            else:
                print("❌ 未登录，请在浏览器中扫码登录")
                for i in range(60):
                    time.sleep(2)
                    avatar = page.query_selector('[class*="avatar"], [class*="user-info"]')
                    if avatar:
                        print("✅ 登录成功!")
                        break
        except Exception as e:
            print(f"登录检查失败: {e}")
        
        time.sleep(2)
        
        # 搜索
        print(f"\n搜索关键词: {KEYWORD}")
        try:
            search_box = page.wait_for_selector('input[placeholder*="搜索"]', timeout=10000)
            search_box.click()
            search_box.fill(KEYWORD)
            page.keyboard.press("Enter")
            time.sleep(5)
            print("✅ 搜索完成")
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            input("按回车键关闭浏览器...")
            browser.close()
            return
        
        # 获取视频链接
        print("\n获取视频链接...")
        video_links = []
        
        for scroll in range(15):
            # 尝试多种选择器
            selectors = [
                'li a',
                'a[href*="/video/"]',
                'a[href*="/note/"]',
                '[data-e2e^="search"] a'
            ]
            
            for selector in selectors:
                try:
                    links = page.query_selector_all(selector)
                    for link in links:
                        href = link.get_attribute("href")
                        if href and ("/video/" in href or "/note/" in href):
                            if not href.startswith("http"):
                                href = "https://www.douyin.com" + href
                            if href not in video_links:
                                video_links.append(href)
                                print(f"  找到视频: {len(video_links)}")
                except:
                    pass
            
            if len(video_links) >= COUNT:
                break
            
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(1)
        
        video_links = video_links[:COUNT]
        print(f"\n共找到 {len(video_links)} 个视频链接")
        
        if not video_links:
            print("❌ 未找到视频链接!")
            print("\n尝试打印页面上的所有链接...")
            all_links = page.query_selector_all('a')
            print(f"页面上共有 {len(all_links)} 个链接")
            for i, link in enumerate(all_links[:20]):
                href = link.get_attribute("href")
                if href:
                    print(f"  {i+1}. {href[:80]}")
            
            input("\n按回车键关闭浏览器...")
            browser.close()
            return
        
        # 开始互动
        print("\n" + "=" * 50)
        print("开始互动...")
        print("=" * 50)
        
        results = []
        
        for idx, url in enumerate(video_links, 1):
            if idx <= completed:
                print(f"\n[{idx}/{len(video_links)}] 跳过（已完成）")
                continue
            
            print(f"\n[{idx}/{len(video_links)}] 处理视频: {url[:60]}...")
            
            video_page = browser.new_page()
            
            try:
                video_page.goto(url, timeout=30000)
                time.sleep(3)
                
                commented = False
                followed = False
                
                # 评论
                try:
                    comment_selectors = [
                        'textarea[placeholder*="评论"]',
                        'textarea[placeholder*="善语"]',
                        'textarea[placeholder*="说点什么"]'
                    ]
                    
                    for sel in comment_selectors:
                        try:
                            comment_box = video_page.wait_for_selector(sel, timeout=3000)
                            if comment_box:
                                comment_box.click()
                                comment_box.fill(COMMENT)
                                time.sleep(0.3)
                                video_page.keyboard.press("Enter")
                                time.sleep(1)
                                print(f"  ✅ 评论成功: {COMMENT}")
                                commented = True
                                break
                        except:
                            continue
                    
                    if not commented:
                        print(f"  ❌ 评论失败: 未找到评论框")
                except Exception as e:
                    print(f"  ❌ 评论失败: {str(e)[:50]}")
                
                # 关注
                try:
                    follow_btn = video_page.query_selector('button:has-text("关注"):not(:has-text("已关注"))')
                    if follow_btn:
                        follow_btn.click()
                        time.sleep(0.5)
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
                video_page.close()
            
            # 等待间隔
            if idx < len(video_links):
                wait_seconds = INTERVAL_MINUTES * 60 + random.randint(-30, 30)
                print(f"  ⏳ 等待 {wait_seconds // 60} 分 {wait_seconds % 60} 秒...")
                time.sleep(wait_seconds)
        
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
        print("🎉 互动完成!")
        print(f"评论成功: {log_data['commented']}/{log_data['total']}")
        print(f"关注成功: {log_data['followed']}/{log_data['total']}")
        print("=" * 50)
        
        input("\n按回车键关闭浏览器...")
        browser.close()


if __name__ == "__main__":
    main()
