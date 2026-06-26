#!/usr/bin/env python3
"""
获取微信公众号文章内容（增强版）
支持下载图片到本地，并在 Markdown 中使用相对路径

Usage: python3 fetch_wx_article.py <wechat_article_url> [--output-dir <dir>]
"""

import sys
import os
import re
import hashlib
from datetime import datetime
import requests


def download_image(img_url: str, save_path: str, timeout: int = 10) -> bool:
    """
    下载图片到本地
    
    Args:
        img_url: 图片 URL
        save_path: 保存路径
        timeout: 下载超时时间（秒）
    
    Returns:
        是否下载成功
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://mp.weixin.qq.com/",
        }
        response = requests.get(img_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"⚠️ 图片下载失败：{str(e)[:80]}")
        return False


def fetch_wx_article(url: str, output_dir: str = None, images_dir: str = None, download_images: bool = True):
    """
    获取微信公众号文章内容（增强版）
    
    Args:
        url: 微信公众号文章链接
        output_dir: MD 文件输出目录（默认在当前目录创建 articles 文件夹）
        images_dir: 图片目录（默认为 output_dir/images/knowledge_时间戳）
        download_images: 是否下载图片
    
    Returns:
        dict: 包含文件路径、标题等信息
    """
    from scrapling.fetchers import Fetcher
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
    import re
    
    print(f"[INFO] 使用 Scrapling 方案（增强版）")
    start_time = datetime.now()
    
    # 创建输出目录
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "articles")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建图片目录：output_dir/images/knowledge_时间戳
    if images_dir is None:
        # 生成时间戳用于图片目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        images_dir = os.path.join(output_dir, "images", f"knowledge_{timestamp}")
        if download_images:
            os.makedirs(images_dir, exist_ok=True)
    else:
        # 如果传入了 images_dir，从中提取时间戳部分，确保图片引用路径一致
        if download_images:
            os.makedirs(images_dir, exist_ok=True)
        # 从 images_dir 路径提取时间戳：例如 /xxx/images/knowledge_20260324_082951 → 20260324_082951
        match = re.search(r'knowledge_(\d{8}_\d{6})', images_dir)
        if match:
            timestamp = match.group(1)
        else:
            # 如果提取失败，使用当前时间戳（但这种情况不应该发生）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"[WARN] 无法从 images_dir 提取时间戳，使用新的时间戳：{timestamp}")
    
    try:
        # 获取网页内容
        print(f"[INFO] 获取网页内容：{url[:80]}...")
        page = Fetcher.get(url)
        
        # Scrapling 的 Response 对象可能没有 status_code，使用 hasattr 检查
        if hasattr(page, 'status_code') and page.status_code != 200:
            raise Exception(f"HTTP {page.status_code}")
        
        # 获取 HTML 内容
        html_content = getattr(page, 'html_content', None) or getattr(page, 'text', None) or str(page)
        
        if not html_content:
            raise Exception("无法获取 HTML 内容")
        
        print(f"[INFO] 获取成功，HTML 长度：{len(html_content)}")
        
        # 解析 HTML
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 提取标题
        title = None
        
        # 尝试多种方式提取标题
        # 1. 从 title 标签
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text().strip()
        
        # 2. 从 h1 或 h2 标签（微信公众号通常使用）
        if not title:
            for tag_name in ["h1", "h2"]:
                h_tag = soup.find(tag_name)
                if h_tag:
                    title = h_tag.get_text().strip()
                    break
        
        # 3. 从 meta 标签
        if not title:
            meta_title = soup.find("meta", property="og:title")
            if meta_title and meta_title.get("content"):
                title = meta_title.get("content").strip()
        
        # 4. 从第一个强化的文本
        if not title:
            strong_tag = soup.find("strong")
            if strong_tag:
                title = strong_tag.get_text().strip()[:50]
        
        if not title:
            title = "微信文章"
        
        # 清理标题（去除多余空格和换行）
        title = re.sub(r'\s+', ' ', title)[:100]
        
        print(f"[INFO] 标题：{title}")
        
        # 查找正文
        content_element = soup.find(id="js_content") or soup.find(class_="rich_media_content")
        
        if not content_element:
            # 如果没有找到正文，使用整个页面
            content_element = soup.find("body") or soup
        
        # 移除无关标签
        for tag in content_element.find_all(["script", "style", "iframe", "noscript"]):
            tag.decompose()
        
        # 处理图片
        image_count = 0
        if download_images:
            print(f"[INFO] 处理图片...")
            for img_tag in content_element.find_all("img"):
                image_count += 1
                alt = img_tag.get("alt") or img_tag.get("data-img-title") or "图片"
                src = img_tag.get("data-src") or img_tag.get("src") or img_tag.get("data-original")
                
                if not src or not src.startswith("http"):
                    img_tag.decompose()
                    continue
                
                # 生成文件名
                filename = f"img_{image_count:03d}.jpg"
                save_path = os.path.join(images_dir, filename)
                # 图片引用使用相对路径：images/knowledge_时间戳/img_001.jpg
                relative_path = f"images/knowledge_{timestamp}/{filename}"
                
                # 下载图片
                print(f"  ↓ 图片 {image_count}: {filename}")
                if download_image(src, save_path):
                    # 替换为 Markdown 格式
                    img_tag.replace_with(f"![{alt}]({relative_path})\n\n")
                else:
                    # 下载失败，保留原链接
                    img_tag.replace_with(f"![{alt}]({src})\n\n")
            
            print(f"[INFO] 图片处理完成，共 {image_count} 张")
        
        # 转换为 Markdown
        print(f"[INFO] 转换为 Markdown...")
        clean_html = str(content_element)
        
        # 优化 HTML：将微信的 """ 转换为标准代码块标签
        print(f"[INFO] 优化 HTML 代码块格式...")
        content_soup = BeautifulSoup(clean_html, 'html.parser')
        
        # 查找所有包含 """ 的 span 标签
        quote_spans = []
        for span in content_soup.find_all('span'):
            if span.get_text(strip=True) == '"""':
                quote_spans.append(span)
        
        # 成对处理 """ 标签
        if len(quote_spans) >= 2:
            print(f"[INFO] 发现 {len(quote_spans)} 个代码块标记，转换为标准格式")
            # 每两个 """ 为一对，包裹中间的内容
            for i in range(0, len(quote_spans) - 1, 2):
                start_span = quote_spans[i]
                end_span = quote_spans[i + 1]
                
                # 收集两个 """ 之间的所有内容
                content_elements = []
                current = start_span.next_sibling
                while current and current != end_span:
                    content_elements.append(current)
                    current = current.next_sibling
                
                # 创建 pre><code 标签包裹内容
                if content_elements:
                    code_wrapper = content_soup.new_tag('pre')
                    code_inner = content_soup.new_tag('code')
                    code_wrapper.append(code_inner)
                    
                    # 将内容移动到 code 标签内
                    for elem in content_elements:
                        if hasattr(elem, 'extract'):
                            code_inner.append(elem.extract())
                        else:
                            code_inner.append(content_soup.new_string(str(elem)))
                    
                    # 替换起始 """ 为 pre 标签，删除结束 """
                    start_span.replace_with(code_wrapper)
                    end_span.extract()
        
        clean_html = str(content_soup)
        
        # 使用 markdownify 转换
        markdown_text = md(
            clean_html, 
            heading_style="ATX", 
            bullets="-", 
            strip=['section', 'span', 'div'], 
            escape_underscores=False, 
            escape_misc=False,
            code_language='text'
        )
        
        # 后处理：移除空的代码块行
        markdown_text = re.sub(r'```\s*\n\s*```', '', markdown_text)
        
        # 清理空行
        lines = [line.strip() for line in markdown_text.splitlines() if line.strip()]
        markdown_text = '\n\n'.join(lines)
        
        # 生成最终内容
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md_content = f"""# {title}

> 链接：{url}  
> 抓取时间：{timestamp_str}  
> 图片数量：{image_count} 张  
> 抓取方案：Scrapling（增强版）

---

{markdown_text}
"""
        
        # 保存文件 - 直接保存在 output_dir 下
        safe_title = re.sub(r'[^\w\u4e00-\u9fff\-_.]', '_', title)[:50]
        output_file = os.path.join(output_dir, f"{safe_title}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"[INFO] 保存成功：{output_file}")
        print(f"[INFO] 完成，耗时：{elapsed:.1f}秒")
        
        return {
            'success': True,
            'title': title,
            'file': output_file,
            'dir': output_dir,
            'images_dir': images_dir if download_images and image_count > 0 else None,
            'images': image_count,
            'word_count': len(markdown_text),
            'elapsed': elapsed
        }
    
    except Exception as e:
        print(f"[ERROR] 抓取失败：{type(e).__name__}: {str(e)[:100]}")
        return {
            'success': False,
            'error': f"{type(e).__name__}: {str(e)}"
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="获取微信公众号文章内容（增强版）")
    parser.add_argument("url", help="微信公众号文章链接")
    parser.add_argument("--output-dir", "-o", help="输出目录（默认在当前目录创建 articles 文件夹）")
    parser.add_argument("--no-images", action="store_true", help="不下载图片")
    
    args = parser.parse_args()
    
    if not args.url.startswith("http"):
        print("Error: 请提供有效的文章链接（以 http 或 https 开头）")
        sys.exit(1)
    
    result = fetch_wx_article(
        args.url,
        output_dir=args.output_dir,
        download_images=not args.no_images
    )
    
    if result['success']:
        print("\n✅ 抓取成功！")
        print(f"📄 标题：{result['title']}")
        print(f"📊 字数：{result['word_count']}")
        print(f"🖼️ 图片：{result['images']} 张")
        print(f"⏱️ 耗时：{result['elapsed']:.1f}秒")
        print(f"📂 目录：{result['dir']}")
    else:
        print(f"\n❌ 抓取失败：{result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
