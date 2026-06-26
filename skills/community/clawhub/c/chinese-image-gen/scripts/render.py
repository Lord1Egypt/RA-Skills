#!/usr/bin/env python3
"""
中文竖屏图片生成器
用法: python3 render.py <html_file> <output.png> [width] [height]
"""
import sys
import time
from playwright.sync_api import sync_playwright

def render(html_content, output_path, width=750, height=1334):
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html_content)
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)  # 等 Google Fonts 加载
        page.screenshot(path=output_path)
        page.close()
        browser.close()
        print(f"✅ {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 render.py <html_file> <output.png> [width] [height]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output = sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 750
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1334
    
    with open(html_file, 'r') as f:
        html = f.read()
    
    render(html, output, w, h)
