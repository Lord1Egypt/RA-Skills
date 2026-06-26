#!/usr/bin/env python3
"""
arXiv PDF/LaTeX 下载器
用法:
  python download_arxiv.py <arxiv-id-or-url> [output_dir]
  python download_arxiv.py 2301.12345
  python download_arxiv.py https://arxiv.org/abs/2301.12345
  python download_arxiv.py 2301.12345 --latex  # 下载 LaTeX 源码
"""

import os
import re
import sys
import argparse
import urllib.request
import urllib.error
from pathlib import Path


def parse_arxiv_id(identifier: str) -> str:
    """从 URL 或 ID 中提取 arXiv ID"""
    # 匹配 URLs like https://arxiv.org/abs/2301.12345
    url_pattern = r'arxiv\.org/(?:abs|pdf|ps)/([\d\.]+)'
    match = re.search(url_pattern, identifier)
    if match:
        return match.group(1)
    
    # 匹配纯 ID，如 2301.12345 或 arXiv:2301.12345
    id_pattern = r'(?:arXiv:)?(\d{4}\.\d{4,5})(v\d+)?'
    match = re.search(id_pattern, identifier)
    if match:
        return match.group(1)
    
    return identifier


def get_pdf_url(arxiv_id: str) -> str:
    """获取 PDF 下载 URL"""
    # 尝试新版本 URL（2019年后的 ID 格式）
    if '.' in arxiv_id and int(arxiv_id.split('.')[0]) >= 1900:
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    # 旧版本格式
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def get_latex_url(arxiv_id: str) -> str:
    """获取 LaTeX 源码下载 URL"""
    return f"https://arxiv.org/e-print/{arxiv_id}"


def download_file(url: str, output_path: Path, max_retries: int = 3) -> bool:
    """下载文件，支持重试"""
    for attempt in range(max_retries):
        try:
            print(f"下载: {url}")
            print(f"保存到: {output_path}")
            
            # 设置请求头模拟浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            request = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(request, timeout=60) as response:
                content = response.read()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(content)
                
                size = len(content) / (1024 * 1024)
                print(f"✅ 下载完成! 文件大小: {size:.2f} MB")
                return True
                
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP 错误 {e.code}: {e.reason}")
            if attempt < max_retries - 1:
                print(f"重试 {attempt + 1}/{max_retries}...")
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            if attempt < max_retries - 1:
                print(f"重试 {attempt + 1}/{max_retries}...")
    
    return False


def main():
    parser = argparse.ArgumentParser(description='arXiv 文件下载器')
    parser.add_argument('identifier', help='arXiv ID 或 URL')
    parser.add_argument('output_dir', nargs='?', default='.', help='输出目录 (默认: 当前目录)')
    parser.add_argument('--latex', action='store_true', help='下载 LaTeX 源码而不是 PDF')
    parser.add_argument('--name', type=str, help='自定义输出文件名')
    
    args = parser.parse_args()
    
    # 解析 ID
    arxiv_id = parse_arxiv_id(args.identifier)
    print(f"📄 识别到 arXiv ID: {arxiv_id}")
    
    # 确定输出路径
    output_dir = Path(args.output_dir).expanduser().resolve()
    
    if args.name:
        if args.latex:
            ext = '.tar.gz'
        else:
            ext = '.pdf'
        filename = args.name if args.name.endswith(ext) else args.name + ext
    else:
        filename = f"{arxiv_id}.tar.gz" if args.latex else f"{arxiv_id}.pdf"
    
    output_path = output_dir / filename
    
    # 下载
    url = get_latex_url(arxiv_id) if args.latex else get_pdf_url(arxiv_id)
    success = download_file(url, output_path)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()