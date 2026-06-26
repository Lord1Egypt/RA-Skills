#!/usr/bin/env python3
"""
Amber Url to Markdown - URL 转 Markdown 工具（V4.0 重构版）
支持可扩展的网站分类处理架构

架构说明：
- handlers/ 目录包含所有网站专用处理器
- 每个处理器继承自 BaseURLHandler，实现独立的抓取逻辑
- 支持轻松添加新的网站类型，互不影响

作者：小文
创建时间：2026-03-22
重构时间：2026-03-26
版本：V4.0
"""

import sys
import os
import re
from datetime import datetime
import time

# 添加路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 导入新架构的处理器
from handlers import get_handler, list_handlers

# 导入其他模块
from fetcher import fetch_dynamic_content
from parser import html_to_markdown, extract_title_from_html
from utils import (
    sanitize_title, format_timestamp, format_datetime,
    create_output_directories, download_image, save_markdown_file,
    create_logger, DEFAULT_OUTPUT_DIR
)


# ============================================================================
# 主抓取函数（使用新架构）
# ============================================================================

def fetch_url(url: str, output_dir: str = DEFAULT_OUTPUT_DIR, download_images: bool = True):
    """
    抓取 URL 并转换为 Markdown（V4.0 使用新处理器架构）
    
    Args:
        url: 目标 URL
        output_dir: 输出目录
        download_images: 是否下载图片
    
    Returns:
        dict: 抓取结果
        str: 错误信息
    """
    from playwright.sync_api import sync_playwright
    
    log = create_logger("Playwright")
    log("=" * 60, "START")
    
    # 1. 根据 URL 获取对应处理器
    handler = get_handler(url)
    log(f"网站类型：{handler.SITE_NAME} ({handler.SITE_TYPE})", "INFO")
    log(f"域名：{handler.DOMAIN}", "INFO")
    
    total_start = time.time()
    browser = None
    context = None
    page = None
    
    try:
        # 创建目录
        os.makedirs(output_dir, exist_ok=True)
        timestamp = format_timestamp()
        log(f"时间戳：{timestamp}", "INFO")
        
        # 图片目录
        images_dir = None
        if download_images:
            images_dir = os.path.join(output_dir, "images", f"knowledge_{timestamp}")
            os.makedirs(images_dir, exist_ok=True)
        
        with sync_playwright() as p:
            log("启动浏览器...", "BROWSER")
            
            # 2. 根据处理器配置启动浏览器
            if handler.should_use_persistent_context():
                # 持久化上下文（用于豆包等需要登录的网站）
                log(f"{handler.SITE_NAME}：使用持久化浏览器上下文", "BROWSER")
                user_data_dir = os.path.join(script_dir, f"{handler.SITE_TYPE}_user_data")
                os.makedirs(user_data_dir, exist_ok=True)
                
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=True,
                    user_agent=handler.config.get("headers", {}).get("User-Agent", "Mozilla/5.0"),
                    viewport={"width": 1920, "height": 1080},
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled",
                    ],
                    extra_http_headers=handler.get_headers(),
                )
                page = context.pages[0] if context.pages else context.new_page()
            else:
                # 标准模式
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled"
                    ]
                )
                
                context = browser.new_context(
                    user_agent=handler.config.get("headers", {}).get("User-Agent", "Mozilla/5.0"),
                    viewport={"width": 1920, "height": 1080},
                    extra_http_headers=handler.get_headers(),
                )
                
                page = context.new_page()
            
            log("页面创建成功", "BROWSER")
            
            # 3. 访问页面
            log(f"访问 URL...", "NAVIGATE")
            nav_start = time.time()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            nav_elapsed = time.time() - nav_start
            log(f"页面加载成功，耗时={nav_elapsed:.1f}s", "NAVIGATE")
            
            # 4. 等待渲染（如果需要）
            if handler.config.get("needs_js", False):
                log(f"等待页面渲染...", "NAVIGATE")
                try:
                    wait_timeout = handler.get_wait_timeout()
                    page.wait_for_load_state("networkidle", timeout=wait_timeout)
                    log("页面渲染完成（networkidle）", "NAVIGATE")
                except Exception as e:
                    log(f"networkidle 超时，使用固定等待：{str(e)[:50]}", "WARN")
                    time.sleep(handler.config.get("wait_time", 3))
            
            # 5. 反检测处理（如果需要）
            if handler.config.get("anti_detection", False):
                log("启用反检测模式...", "ANTI_DETECT")
                
                # 随机等待
                import random
                base_delay = handler.config.get("scroll_delay", 1.5)
                random_delay = base_delay + random.uniform(0.5, 1.5)
                log(f"随机等待 {random_delay:.1f}s...", "ANTI_DETECT")
                time.sleep(random_delay)
                
                # 滚动加载
                scroll_config = handler.get_scroll_config()
                if scroll_config["count"] > 0:
                    log(f"模拟滚动页面 ({scroll_config['count']}次)...", "ANTI_DETECT")
                    for i in range(scroll_config["count"]):
                        page.evaluate(f"window.scrollBy(0, {scroll_config['height']})")
                        time.sleep(scroll_config["delay"])
                    page.evaluate("window.scrollTo(0, 0)")
                    time.sleep(1)
                    log("滚动完成", "ANTI_DETECT")
            
            # 6. 使用处理器抓取内容
            log("抓取内容...", "FETCH")
            result = handler.fetch(page)
            
            if not result.success:
                browser.close() if browser else None
                return None, f"抓取失败：{result.error}"
            
            log(f"抓取成功：标题={result.title}, 文本={result.metadata.get('text_length', 0)}字符", "FETCH")
            
            # 7. 处理图片
            image_count = 0
            if download_images and result.images:
                log(f"处理 {len(result.images)} 张图片...", "IMAGE")
                for img_info in result.images:
                    image_count += 1
                    filename = f"img_{image_count:03d}.jpg"
                    save_path = os.path.join(images_dir, filename) if images_dir else None
                    relative_path = f"images/knowledge_{timestamp}/{filename}"
                    
                    log(f"  ↓ 图片 {image_count}: {img_info['alt']}", "IMAGE")
                    if download_image(img_info['src'], save_path):
                        # 替换 HTML 中的图片引用
                        result.html = result.html.replace(img_info['src'], relative_path)
            
            log(f"图片处理完成，共 {image_count} 张", "IMAGE")
            
            # 8. 转换为 Markdown
            log("转换为 Markdown...", "MARKDOWN")
            clean_text = html_to_markdown(result.html)
            log(f"Markdown 长度：{len(clean_text)}", "DEBUG")
            
            # 9. 保存文件
            safe_title = sanitize_title(result.title)
            output_file = os.path.join(output_dir, f"{safe_title}.md")
            log(f"保存文件：{output_file}", "SAVE")
            
            md_content = f"""# {result.title}

> 链接：{url}  
> 抓取时间：{format_datetime()}  
> 图片数量：{image_count} 张  
> 网站类型：{handler.SITE_NAME}  
> 抓取方案：Playwright 无头浏览器

---

{clean_text}
"""
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            log("文件保存成功", "SAVE")
            
            # 10. 关闭浏览器
            if browser:
                browser.close()
                log("浏览器已关闭", "BROWSER")
            else:
                log("持久化上下文，跳过 close", "BROWSER")
            
            total_elapsed = time.time() - total_start
            log(f"完成，耗时={total_elapsed:.1f}s", "COMPLETE")
            
            return {
                'success': True,
                'title': result.title,
                'file': output_file,
                'dir': output_dir,
                'images_dir': images_dir if download_images and image_count > 0 else None,
                'images': image_count,
                'word_count': len(clean_text),
                'elapsed': total_elapsed,
                'site_type': handler.SITE_TYPE,
            }, None
    
    except Exception as e:
        import traceback
        error_msg = f"{type(e).__name__}: {str(e)}"
        stack_trace = traceback.format_exc()
        log(f"失败：{error_msg}", "ERROR")
        log(f"堆栈：{stack_trace}", "ERROR")
        
        # 清理资源
        try:
            if browser:
                browser.close()
        except:
            pass
        
        return None, error_msg


# ============================================================================
# 辅助函数
# ============================================================================

def print_result(result: dict):
    """打印抓取结果"""
    print(f"📄 标题：{result['title']}")
    print(f"📊 字数：{result['word_count']}")
    print(f"🖼️ 图片：{result['images']} 张")
    print(f"⏱️ 耗时：{result['elapsed']:.1f}秒")
    print(f"📂 目录：{result['dir']}")
    print(f"📝 文件：{result['file']}")


def show_handlers():
    """显示所有已注册的处理器"""
    print("\n已注册的 URL 处理器：")
    print("=" * 60)
    handlers = list_handlers()
    for h in handlers:
        print(f"  {h['name']:25} ({h['type']:10}) → {h['domain']}")
    print("=" * 60)
    print(f"共 {len(handlers)} 个处理器\n")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 amber_url_to_markdown.py <URL> [输出目录]")
        print("\n示例:")
        print("  python3 amber_url_to_markdown.py https://mp.weixin.qq.com/s/xxx")
        print("  python3 amber_url_to_markdown.py https://www.doubao.com/thread/xxx")
        print("\n查看所有支持的处理器:")
        print("  python3 amber_url_to_markdown.py --handlers")
        sys.exit(1)
    
    if sys.argv[1] == "--handlers":
        show_handlers()
        sys.exit(0)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR
    
    print("\n" + "=" * 60)
    print("Amber Url to Markdown - URL 转 Markdown 工具 (V4.0)")
    print("=" * 60)
    print(f"\n目标链接：{url}\n")
    
    result, error = fetch_url(url, output_dir)
    
    if result:
        print("\n✅ 抓取成功")
        print_result(result)
        return result
    else:
        print(f"\n❌ 抓取失败：{error}")
        return None


if __name__ == "__main__":
    main()
