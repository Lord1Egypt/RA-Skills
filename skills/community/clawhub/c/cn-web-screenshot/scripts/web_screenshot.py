#!/usr/bin/env python3
"""
网页截图工具 - 捕获网页截图
"""
import sys
import json
import os
from datetime import datetime

def take_screenshot(url, output_path=None, full_page=True, viewport=None, wait_time=2000):
    """截取网页"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # 设置视口
            if viewport == 'mobile':
                viewport_size = {'width': 375, 'height': 667}
            elif viewport == 'tablet':
                viewport_size = {'width': 768, 'height': 1024}
            else:
                viewport_size = {'width': 1280, 'height': 720}
            
            page = browser.new_page(viewport=viewport_size)
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(wait_time)
            
            # 生成输出路径
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f'/tmp/screenshot_{timestamp}.png'
            
            # 截图
            page.screenshot(path=output_path, full_page=full_page)
            
            browser.close()
            
            return {
                'success': True,
                'path': output_path,
                'url': url,
                'full_page': full_page
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供URL'}, ensure_ascii=False))
        return
    
    url = sys.argv[1]
    full_page = True
    viewport = None
    output_path = None
    wait_time = 2000
    
    # 解析参数
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ['--viewport', '-v'] and i + 1 < len(args):
            viewport = args[i + 1]
            i += 2
        elif arg in ['--partial', '-p']:
            full_page = False
            i += 1
        elif arg in ['--output', '-o'] and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif arg in ['--wait', '-w'] and i + 1 < len(args):
            wait_time = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    # 确保URL有协议
    if not url.startswith('http'):
        url = 'https://' + url
    
    # 截图
    result = take_screenshot(url, output_path, full_page, viewport, wait_time)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
