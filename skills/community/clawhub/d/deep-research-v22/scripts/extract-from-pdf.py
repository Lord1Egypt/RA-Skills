#!/usr/bin/env python3
"""
功能：从PDF全文中结构化提取数据，填充来源卡片
用法：python3 extract-from-pdf.py <card_id> <pdf_url>
"""

import sys
import json
import re
import urllib.request
import tempfile
import os

# 尝试导入pdfplumber
try:
    import pdfplumber
    PDF_PARSER = 'pdfplumber'
except ImportError:
    import pdftotext
    PDF_PARSER = 'pdftotext'

def download_pdf(url, timeout=30):
    """下载PDF到临时文件"""
    if not url or url == 'N/A':
        return None
    
    # 处理URL编码
    url = url.strip()
    if not url.startswith('http'):
        return None
    
    try:
        print(f"  下载: {url[:60]}...")
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            
            # 创建临时文件
            fd, path = tempfile.mkstemp(suffix='.pdf')
            os.write(fd, data)
            os.close(fd)
            print(f"  保存: {path}")
            return path
    except Exception as e:
        print(f"  下载失败: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """从PDF提取文本"""
    text = ""
    try:
        if PDF_PARSER == 'pdfplumber':
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            with open(pdf_path, 'rb') as f:
                pdf = pdftotext.PDF(f)
                text = "\n\n".join(pdf)
    except Exception as e:
        print(f"  解析失败: {e}")
        return ""
    return text

def extract_structured_data(text, card_id):
    """从文本中提取结构化数据"""
    # 简化版提取 - 实际项目中可以用更复杂的LLM提示
    result = {
        'sample_size': None,
        'main_result': None,
        'cost_impact': None,
        'time_range': None,
        'confidence_interval': None,
        'p_value': None,
        'quote': None
    }
    
    # 提取样本量
    sample_patterns = [
        r'(\d{1,3}(?:,\d{3})*)\s*(?:patients|subjects|participants|samples)',
        r'n\s*=\s*(\d{1,3}(?:,\d{3})*)',
        r'(\d{1,3}(?:,\d{3})*)\s*cases?'
    ]
    for pattern in sample_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['sample_size'] = match.group(1)
            break
    
    # 提取主要结果 (百分比)
    percent_patterns = [
        r'(\d+\.?\d*)%\s*(?:reduction|decrease|increase|savings|improvement)',
        r'(?:reduced|decreased|increased)\s*(?:by\s*)?(\d+\.?\d*)%',
        r'(\d+\.?\d*)%\s*(?:accuracy|sensitivity|specificity|AUC)'
    ]
    for pattern in percent_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['main_result'] = match.group(1) + '%'
            break
    
    # 提取成本影响
    cost_patterns = [
        r'\$(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:savings|per\s*patient|per\s*person)',
        r'saved\s*(\d+(?:,\d{3})*)\s*',
    ]
    for pattern in cost_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['cost_impact'] = '$' + match.group(1)
            break
    
    # 提取置信区间
    ci_patterns = [
        r'95%\s*CI\s*[\[\(]([^)\]]+)[\]\)]',
        r'confidence\s*interval\s*[\[\(]([^)\]]+)[\]\)]'
    ]
    for pattern in ci_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['confidence_interval'] = '95% CI [' + match.group(1) + ']'
            break
    
    # 提取p值
    p_patterns = [
        r'p\s*[=<]\s*(\d+\.?\d*)',
        r'p-value\s*[=<]\s*(\d+\.?\d*)'
    ]
    for pattern in p_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            pval = match.group(1)
            result['p_value'] = 'p' + ('<' if '=' not in pattern else '=') + pval
            break
    
    # 提取原文引用（第一段有意义的内容，50+字）
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 50]
    if lines:
        # 找到第一段摘要或介绍
        for line in lines[:5]:
            if any(x in line.lower() for x in ['abstract', 'introduction', 'background', 'method', 'result', 'conclusion']):
                result['quote'] = line[:300]  # 限制长度
                break
        if not result['quote'] and lines:
            result['quote'] = lines[0][:300]
    
    return result

def main():
    if len(sys.argv) < 3:
        print("用法: python3 extract-from-pdf.py <card_id> <pdf_url>")
        print("示例: python3 extract-from-pdf.py card-001 https://arxiv.org/pdf/xxx.pdf")
        sys.exit(1)
    
    card_id = sys.argv[1]
    pdf_url = sys.argv[2]
    
    print(f"=== 处理卡片: {card_id} ===")
    
    # 1. 下载PDF
    pdf_path = download_pdf(pdf_url)
    if not pdf_path:
        print("❌ 无法下载PDF")
        sys.exit(1)
    
    # 2. 提取文本
    print("  提取文本...")
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("❌ 无法提取文本")
        os.unlink(pdf_path)
        sys.exit(1)
    
    print(f"  提取到 {len(text)} 字符")
    
    # 3. 结构化提取
    print("  结构化提取...")
    data = extract_structured_data(text, card_id)
    
    # 4. 输出结果
    print("\n=== 提取结果 ===")
    for key, value in data.items():
        if value:
            print(f"  {key}: {value}")
    
    # 5. 保存为JSON
    output_file = f"/tmp/{card_id}_extracted.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n结果保存到: {output_file}")
    
    # 清理临时文件
    os.unlink(pdf_path)
    print("✅ 完成")

if __name__ == '__main__':
    main()
