#!/usr/bin/env python3
"""
淘宝/1688商品图片下载器
支持通过浏览器下载商品主图和详情图
"""

import argparse
import os
import re
import sys
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote

def sanitize_filename(name: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除或替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '_', name)
    # 限制长度
    return name[:100] if len(name) > 100 else name

def download_image(url: str, save_path: str, headers: dict = None) -> bool:
    """下载单张图片"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.taobao.com/'
        }
    
    try:
        # 处理URL协议
        if url.startswith('//'):
            url = 'https:' + url
        
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"  下载失败: {url[:50]}... - {e}")
        return False

def extract_images_from_html(html_content: str, base_url: str) -> dict:
    """从HTML内容中提取图片URL"""
    images = {
        'main': [],
        'detail': []
    }
    
    # 主图匹配模式（淘宝/1688常见格式）
    main_patterns = [
        r'data-imgs[\'"]?\s*:\s*[\'"]?([^\'">\s,]+)',
        r'auctionImages[\'"]?\s*:\s*[\'"]?([^\'">\s,]+)',
        r'"mainPicUrl"\s*:\s*"([^"]+)"',
        r'"picUrl"\s*:\s*"([^"]+)"',
        r'data-src="([^"]*\.(jpg|jpeg|png|webp)[^"]*)"',
    ]
    
    # 详情图匹配模式
    detail_patterns = [
        r'(https?://[^"\'>\s]+?(?:alicdn|taobaocdn|1688)[^"\'>\s]*?\.(?:jpg|jpeg|png|webp)[^"\'>\s]*)',
        r'(//[^"\'>\s]+?(?:alicdn|taobaocdn|1688)[^"\'>\s]*?\.(?:jpg|jpeg|png|webp)[^"\'>\s]*)',
    ]
    
    for pattern in main_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            url = match if isinstance(match, str) else match[0]
            if url and url not in images['main']:
                images['main'].append(url)
    
    for pattern in detail_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            url = match if isinstance(match, str) else match[0]
            if url and url not in images['main'] and url not in images['detail']:
                images['detail'].append(url)
    
    return images

def download_from_url(url: str, output_dir: str, include_detail: bool = True) -> dict:
    """
    从URL下载商品图片（需要配合浏览器使用）
    
    Args:
        url: 商品页面URL
        output_dir: 输出目录
        include_detail: 是否下载详情图
    
    Returns:
        下载结果统计
    """
    result = {
        'url': url,
        'main_images': 0,
        'detail_images': 0,
        'failed': 0,
        'output_dir': output_dir
    }
    
    print(f"\n{'='*50}")
    print(f"正在处理: {url}")
    print(f"输出目录: {output_dir}")
    print('='*50)
    
    return result

def main():
    parser = argparse.ArgumentParser(
        description='淘宝/1688商品图片下载器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载单个商品图片
  python download_images.py --url "https://detail.1688.com/offer/123456.html" --output ./images
  
  # 使用JSON配置（由Agent生成）
  python download_images.py --config /tmp/download_config.json
"""
    )
    
    parser.add_argument('--url', help='商品页面URL')
    parser.add_argument('--name', help='商品名称（用于命名文件夹）')
    parser.add_argument('--output', '-o', default='~/Downloads/taobao_images', help='输出目录')
    parser.add_argument('--detail', action='store_true', default=True, help='下载详情图')
    parser.add_argument('--no-detail', action='store_true', help='不下载详情图')
    parser.add_argument('--config', help='JSON配置文件路径')
    parser.add_argument('--images', help='图片URL列表文件（每行一个URL）')
    
    args = parser.parse_args()
    
    # 处理输出目录
    output_dir = Path(args.output).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 如果提供了图片URL列表，直接下载
    if args.images:
        urls_file = Path(args.images)
        if not urls_file.exists():
            print(f"错误: 图片列表文件不存在: {args.images}")
            sys.exit(1)
        
        urls = [line.strip() for line in urls_file.read_text().split('\n') if line.strip()]
        print(f"从文件读取到 {len(urls)} 个图片URL")
        
        success = 0
        for i, url in enumerate(urls, 1):
            ext = '.jpg'
            if '.png' in url.lower():
                ext = '.png'
            elif '.webp' in url.lower():
                ext = '.webp'
            
            save_path = output_dir / f"image_{i:03d}{ext}"
            print(f"[{i}/{len(urls)}] 下载中...")
            if download_image(url, str(save_path)):
                success += 1
        
        print(f"\n完成! 成功: {success}/{len(urls)}")
        return
    
    if args.config:
        import json
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"错误: 配置文件不存在: {args.config}")
            sys.exit(1)
        
        config = json.loads(config_path.read_text())
        print(f"加载配置: {config}")
    
    if args.url:
        download_from_url(args.url, str(output_dir), include_detail=args.detail)
    else:
        print("请提供 --url 或 --config 或 --images 参数")
        parser.print_help()

if __name__ == '__main__':
    main()