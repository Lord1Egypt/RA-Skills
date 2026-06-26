#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将包含LaTeX公式的HTML文件通过Edge无头模式转为PDF
公式使用MathJax渲染，保证PDF中公式是真正的数学符号
"""

import os
import sys
import subprocess
import time
import argparse

def check_prerequisites():
    """检查依赖"""
    # 检查Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    edge_path = None
    for p in edge_paths:
        if os.path.isfile(p):
            edge_path = p
            break
    
    return edge_path

def html_to_pdf(html_path, output_path=None, timeout_seconds=30):
    """
    将HTML转为PDF（Edge无头模式）
    
    Args:
        html_path: HTML文件路径或file:// URL
        output_path: 输出PDF路径（默认同目录同名.pdf）
        timeout_seconds: MathJax渲染等待时间（秒）
    
    Returns:
        PDF文件路径
    """
    edge_path = check_prerequisites()
    
    # 处理输入路径
    if not html_path.startswith("file://"):
        abs_path = os.path.abspath(html_path)
        file_url = "file:///" + abs_path.replace("\\", "/")
    else:
        file_url = html_path
        abs_path = html_path.replace("file:///", "")
    
    # 处理输出路径
    if not output_path:
        base = os.path.splitext(abs_path)[0]
        output_path = base + ".pdf"
    
    output_path = os.path.abspath(output_path)
    
    # 构建命令
    cmd = [
        edge_path,
        "--headless=new",
        f"--virtual-time-budget={timeout_seconds * 1000}",
        f"--print-to-pdf={output_path}",
        "--no-margins",
        "--disable-gpu",
        "--disable-software-rasterizer",
        file_url
    ]
    
    print(f"正在生成PDF...")
    print(f"  来源: {file_url}")
    print(f"  输出: {output_path}")
    print(f"  超时: {timeout_seconds}s")
    
    # 执行
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout_seconds + 10
    )
    
    # 检查是否生成成功
    if os.path.isfile(output_path):
        file_size = os.path.getsize(output_path)
        print(f"  OK! 文件大小: {file_size / 1024:.1f} KB")
        return output_path
    else:
        print(f"  ERROR: 文件未生成")
        return None

def verify_pdf_formulas_rendered(pdf_path):
    """
    验证PDF中的公式是否已渲染（不含原始LaTeX代码）
    
    Args:
        pdf_path: PDF文件路径
    
    Returns:
        (bool, str): (是否已渲染, 描述信息)
    """
    try:
        import fitz  # pymupdf
    except ImportError:
        return True, "无法验证（无pymupdf库）"
    
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    # 检查LaTeX原始代码关键词
    latex_patterns = [
        r'\frac', r'\sqrt', r'\lim', r'\sum', r'\int', 
        r'\dfrac', r'\to', r'\infty', r'\ge', r'\le',
        r'\\\[', r'\\\(', r'$$', r'\cdot'
    ]
    
    found = []
    for pattern in latex_patterns:
        if pattern in full_text:
            found.append(pattern)
    
    if found:
        return False, f"发现未渲染的LaTeX代码: {', '.join(found)}"
    else:
        return True, "公式已渲染，无原始LaTeX代码"

def main():
    parser = argparse.ArgumentParser(description="HTML(含LaTeX公式)→PDF 转换工具")
    parser.add_argument("html_file", help="输入HTML文件路径或file:// URL")
    parser.add_argument("-o", "--output", help="输出PDF路径（可选）")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="MathJax渲染等待时间（秒，默认30）")
    parser.add_argument("--verify", action="store_true", help="验证后确认公式已渲染")
    
    args = parser.parse_args()
    
    # 转换
    output = html_to_pdf(args.html_file, args.output, args.timeout)
    
    if not output:
        print("转换失败！")
        return 1
    
    # 验证
    if args.verify:
        rendered, msg = verify_pdf_formulas_rendered(output)
        print(f"  验证: {msg}")
        if not rendered:
            print("  ⚠️ 建议增加 --timeout 参数或检查HTML中的MathJax配置")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())