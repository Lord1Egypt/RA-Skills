#!/usr/bin/env python3
"""
PDF解析脚本 - 用于提取企业诊断报告PDF中的文本内容

功能：
- 支持URL和本地文件路径输入
- 提取PDF中的文本内容
- 支持输出到文件或控制台

依赖：
- PyMuPDF (fitz): PDF解析
- requests: HTTP请求
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("错误：未安装PyMuPDF库，请执行: pip install PyMuPDF==1.23.26")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("错误：未安装requests库，请执行: pip install requests==2.31.0")
    sys.exit(1)


def download_pdf(url: str, save_path: str) -> str:
    """
    从URL下载PDF文件
    
    Args:
        url: PDF文件的URL地址
        save_path: 本地保存路径
        
    Returns:
        保存的文件路径
        
    Raises:
        Exception: 下载失败时抛出异常
    """
    try:
        print(f"正在下载PDF文件: {url[:50]}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=60, stream=True)
        response.raise_for_status()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 保存文件
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"PDF文件已保存至: {save_path}")
        return save_path
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"下载PDF失败: {str(e)}")


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    从PDF文件中提取文本内容
    
    Args:
        pdf_path: PDF文件的本地路径
        
    Returns:
        提取的文本内容
        
    Raises:
        Exception: 解析失败时抛出异常
    """
    try:
        print(f"正在解析PDF文件: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        text_content = []
        
        # 遍历每一页
        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text()
            
            if text.strip():
                text_content.append(f"--- 第 {page_num + 1} 页 ---\n{text}")
        
        full_text = "\n\n".join(text_content)
        print(f"PDF解析完成，共 {page_count} 页，提取文本长度: {len(full_text)} 字符")
        
        # 关闭文档
        doc.close()
        
        return full_text
        
    except Exception as e:
        raise Exception(f"解析PDF失败: {str(e)}")


def is_url(path: str) -> bool:
    """判断输入是否为URL"""
    return path.startswith('http://') or path.startswith('https://')


def main():
    parser = argparse.ArgumentParser(
        description='PDF报告解析工具 - 提取PDF文件中的文本内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 解析URL的PDF文件并输出到控制台
  python pdf_parser.py --url "https://example.com/report.pdf"
  
  # 解析URL的PDF文件并保存到文件
  python pdf_parser.py --url "https://example.com/report.pdf" --output "./output/report.txt"
  
  # 解析本地PDF文件
  python pdf_parser.py --url "./reports/report.pdf" --output "./output/report.txt"
        """
    )
    
    parser.add_argument(
        '--url',
        required=True,
        help='PDF文件的URL地址或本地文件路径（必填）'
    )
    
    parser.add_argument(
        '--output',
        default=None,
        help='提取内容的保存路径（选填，不指定则输出到控制台）'
    )
    
    args = parser.parse_args()
    
    try:
        # 判断输入类型
        if is_url(args.url):
            # URL输入：下载PDF
            temp_dir = "/tmp/pdf_downloads"
            os.makedirs(temp_dir, exist_ok=True)
            
            # 生成简短文件名（避免文件名过长问题）
            import hashlib
            url_hash = hashlib.md5(args.url.encode()).hexdigest()[:12]
            filename = f"report_{url_hash}.pdf"
            
            pdf_path = os.path.join(temp_dir, filename)
            pdf_path = download_pdf(args.url, pdf_path)
        else:
            # 本地文件路径
            pdf_path = args.url
            if not os.path.exists(pdf_path):
                print(f"错误：文件不存在: {pdf_path}")
                sys.exit(1)
        
        # 提取文本
        text = extract_text_from_pdf(pdf_path)
        
        # 输出结果
        if args.output:
            # 保存到文件
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"文本内容已保存至: {args.output}")
        else:
            # 输出到控制台
            print("\n" + "="*60)
            print("提取的文本内容：")
            print("="*60 + "\n")
            print(text)
        
        return 0
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
