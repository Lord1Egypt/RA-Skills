#!/usr/bin/env python3
"""
将 Markdown 转换为 PDF（优化版）
使用 WeasyPrint + Google Fonts 解决中文显示问题
"""

import os
import sys
import subprocess
import markdown
from pathlib import Path

def generate_html_from_markdown(md_path: str, html_path: str) -> bool:
    """将 Markdown 转换为带中文支持的 HTML"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换为 HTML
        html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # 使用 Google Fonts 的 Noto Sans SC 中文字体
        html_full = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

body {
    font-family: 'Noto Sans SC', 'SimHei', 'Microsoft YaHei', sans-serif;
    font-size: 11px;
    line-height: 1.6;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    color: #333;
}

h1 {
    color: #1a365d;
    font-size: 20px;
    font-weight: 700;
    border-bottom: 2px solid #3182ce;
    padding-bottom: 10px;
    margin-top: 20px;
}

h2 {
    color: #2c5282;
    font-size: 16px;
    font-weight: 500;
    margin-top: 18px;
    margin-bottom: 10px;
}

h3 {
    color: #2d3748;
    font-size: 14px;
    font-weight: 500;
    margin-top: 14px;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10px;
}

th, td {
    border: 1px solid #cbd5e0;
    padding: 8px 12px;
    text-align: left;
}

th {
    background: #edf2f7;
    font-weight: 500;
    color: #2d3748;
}

tr:nth-child(even) {
    background: #f7fafc;
}

blockquote {
    background: #f7fafc;
    border-left: 4px solid #3182ce;
    padding: 10px 15px;
    margin: 10px 0;
    font-size: 10px;
    color: #4a5568;
}

hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 20px 0;
}

em {
    color: #718096;
    font-size: 10px;
}

strong {
    font-weight: 500;
}

code {
    background: #edf2f7;
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 9px;
}

/* 图片宽度限制 - A4页面适配 */
img {
    max-width: 100%;
    width: auto;
    height: auto;
    display: block;
    margin: 15px auto;
    page-break-inside: avoid;
}

/* K线图特殊处理 */
img[src*="chart"] {
    max-width: 95%;
    max-height: 400px;
    object-fit: contain;
}

/* 投资亮点风险标记 */
p:has(+ p:contains("✅")),
p:contains("✅") {
    color: #38a169;
}

p:contains("⚠️") {
    color: #dd6b20;
}

@media print {
    body {
        padding: 15px;
        max-width: 170mm; /* A4有效宽度 */
    }
    h1 {
        font-size: 18px;
    }
    h2 {
        font-size: 14px;
    }
    img {
        max-width: 160mm; /* 打印时图片宽度 */
    }
}
</style>
</head>
<body>
""" + html_body + """
</body>
</html>
"""
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_full)
        
        print(f"HTML saved: {html_path}")
        return True
        
    except Exception as e:
        print(f"HTML generation error: {e}")
        return False

def generate_pdf_weasyprint(html_path: str, pdf_path: str) -> bool:
    """使用 WeasyPrint 生成 PDF"""
    try:
        from weasyprint import HTML, CSS
        
        # 使用网络字体
        HTML(html_path).write_pdf(pdf_path)
        
        print(f"PDF saved: {pdf_path}")
        return True
        
    except Exception as e:
        print(f"WeasyPrint error: {e}")
        return False

def generate_pdf_pypdf(html_path: str, pdf_path: str) -> bool:
    """使用 wkhtmltopdf 作为备选"""
    try:
        result = subprocess.run(
            ['wkhtmltopdf', '--encoding', 'utf-8', html_path, pdf_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"PDF saved via wkhtmltopdf: {pdf_path}")
            return True
        else:
            print(f"wkhtmltopdf error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("wkhtmltopdf not installed")
        return False

def generate_pdf(md_path: str, pdf_path: str) -> str:
    """主函数：生成 PDF"""
    if not os.path.exists(md_path):
        print(f"Markdown file not found: {md_path}")
        return ""
    
    html_path = md_path.replace('.md', '.html')
    
    # Step 1: 生成 HTML
    if not generate_html_from_markdown(md_path, html_path):
        return ""
    
    # Step 2: 生成 PDF
    if generate_pdf_weasyprint(html_path, pdf_path):
        return pdf_path
    
    # 备选方案
    if generate_pdf_pypdf(html_path, pdf_path):
        return pdf_path
    
    print("PDF generation failed, HTML available at: " + html_path)
    return ""

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_pdf.py <markdown_file> <output_pdf>")
        sys.exit(1)
    
    md_path = sys.argv[1]
    pdf_path = sys.argv[2]
    
    result = generate_pdf(md_path, pdf_path)
    if result:
        print(f"Success: {result}")
    else:
        print("Failed to generate PDF")

if __name__ == "__main__":
    main()