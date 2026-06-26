#!/usr/bin/env python3
"""
天眼查调试脚本 - 查看页面结构
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("错误: Playwright 未安装")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".due_diligence"
STORAGE_FILE = CONFIG_DIR / "tianyancha_storage.json"

def debug_search():
    """调试搜索页面"""
    
    storage_state = None
    if STORAGE_FILE.exists():
        with open(STORAGE_FILE, "r") as f:
            storage_state = json.load(f)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=['--disable-blink-features=AutomationControlled']
        )
        
        if storage_state:
            context = browser.new_context(
                storage_state=storage_state,
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
        else:
            context = browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
        
        page = context.new_page()
        
        # 访问天眼查首页
        print("1. 访问天眼查首页...")
        page.goto("https://www.tianyancha.com/", wait_until='networkidle', timeout=30000)
        time.sleep(3)
        
        # 检查登录状态
        print("\n2. 检查登录状态...")
        page.screenshot(path="/tmp/tianyancha_home.png")
        print("   截图已保存: /tmp/tianyancha_home.png")
        
        # 尝试查找搜索框
        print("\n3. 查找搜索框...")
        selectors = [
            'input[placeholder*="搜索"]',
            'input[placeholder*="公司"]',
            'input[placeholder*="查"]',
            '.search-input input',
            '#search-key',
            'input[name="key"]',
        ]
        
        found_selector = None
        for selector in selectors:
            try:
                elem = page.query_selector(selector)
                if elem:
                    print(f"   ✓ 找到搜索框: {selector}")
                    found_selector = selector
                    break
            except:
                continue
        
        if not found_selector:
            print("   ✗ 未找到搜索框，列出所有 input 元素:")
            inputs = page.query_selector_all('input')
            for i, inp in enumerate(inputs):
                try:
                    placeholder = inp.get_attribute('placeholder') or ''
                    name = inp.get_attribute('name') or ''
                    cls = inp.get_attribute('class') or ''
                    print(f"     [{i}] placeholder={placeholder}, name={name}, class={cls[:50]}")
                except:
                    pass
        
        # 输入搜索词
        if found_selector:
            print("\n4. 输入搜索词: 建元信托")
            page.fill(found_selector, "建元信托")
            time.sleep(1)
            
            # 尝试按回车或点击搜索按钮
            print("5. 提交搜索...")
            
            # 尝试按回车
            page.press(found_selector, 'Enter')
            time.sleep(5)
            
            # 截图搜索结果
            page.screenshot(path="/tmp/tianyancha_search.png")
            print("   截图已保存: /tmp/tianyancha_search.png")
            
            # 查看当前 URL
            print(f"\n6. 当前 URL: {page.url}")
            
            # 查找搜索结果
            print("\n7. 查找搜索结果...")
            result_selectors = [
                '.search-result-item',
                '[class*="search-result"]',
                '.company-item',
                '[class*="company-list"] a',
                'a[href*="/company/"]',
            ]
            
            for selector in result_selectors:
                try:
                    items = page.query_selector_all(selector)
                    if items:
                        print(f"   ✓ 找到 {len(items)} 个结果: {selector}")
                        for i, item in enumerate(items[:3]):
                            try:
                                text = item.inner_text()[:100]
                                href = item.get_attribute('href') or ''
                                print(f"     [{i}] {text[:50]}... -> {href[:50]}")
                            except:
                                pass
                        break
                except:
                    continue
            else:
                print("   ✗ 未找到搜索结果，查看页面内容:")
                content = page.content()
                print(f"   页面内容长度: {len(content)}")
                
                # 保存页面 HTML
                with open("/tmp/tianyancha_search.html", "w") as f:
                    f.write(content)
                print("   HTML 已保存: /tmp/tianyancha_search.html")
        
        print("\n调试完成，浏览器将在 10 秒后关闭...")
        time.sleep(10)
        
        browser.close()


if __name__ == "__main__":
    debug_search()
