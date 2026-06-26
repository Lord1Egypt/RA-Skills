#!/usr/bin/env python3
"""
XHS Publisher - HTML to Image Renderer
用法：python3 render_images.py <cards_dir> <output_dir>

将 cards_dir 中的所有 HTML 文件按文件名排序渲染为 1242×1660 PNG 图片。
"""
import os
import sys
import glob
from playwright.sync_api import sync_playwright

def render(cards_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    html_files = sorted(glob.glob(os.path.join(cards_dir, "*.html")))
    if not html_files:
        print(f"❌ 未找到 HTML 文件：{cards_dir}")
        sys.exit(1)

    print(f"📸 渲染 {len(html_files)} 张图片 → {output_dir}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_path in html_files:
            basename = os.path.splitext(os.path.basename(html_path))[0]
            output_path = os.path.join(output_dir, f"{basename}.png")
            page = browser.new_page(viewport={"width": 1242, "height": 1660})
            with open(html_path, "r", encoding="utf-8") as f:
                page.set_content(f.read(), wait_until="networkidle")
            page.screenshot(path=output_path, clip={"x": 0, "y": 0, "width": 1242, "height": 1660})
            page.close()
            print(f"  ✅ {basename}.png")
        browser.close()
    print(f"\n🦞 全部完成！共 {len(html_files)} 张")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python3 render_images.py <cards_dir> <output_dir>")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
