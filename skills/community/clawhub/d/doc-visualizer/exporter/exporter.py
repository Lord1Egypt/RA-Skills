"""
导出器 - 将HTML转换为PDF和长图
"""

import os
import sys
import time

def export_pdf_and_screenshot(html_path: str, output_dir: str) -> dict:
    """
    使用playwright将HTML导出为PDF和长图
    返回: {"pdf": path, "png": path}
    """
    from playwright.sync_api import sync_playwright
    
    html_abs = os.path.abspath(html_path)
    html_url = f"file:///{html_abs.replace(chr(92), '/')}"
    
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_page(viewport={"width": 1280, "height": 900})
        
        page.goto(html_url, wait_until="networkidle")
        time.sleep(1.5)
        
        # PDF导出
        pdf_path = os.path.join(output_dir, os.path.basename(html_path).replace(".html", ".pdf"))
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )
        
        # 长图截图
        png_path = os.path.join(output_dir, os.path.basename(html_path).replace(".html", "_fullpage.png"))
        page.screenshot(path=png_path, full_page=True)
        
        b.close()
    
    return {"pdf": pdf_path, "png": png_path}
