# -*- coding: utf-8 -*-
"""
基金定期报告投资策略提取脚本
用法: python 基金报告提取.py --code 006567 --name "中泰星元"
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
import akshare as ak
import pandas as pd
import requests
import pdfplumber
import fitz
import re
import os
import time
import shutil

def get_announcements(code):
    """获取基金公告列表"""
    df = ak.fund_announcement_report_em(symbol=code)
    return df

def extract_with_pymupdf(pdf_content):
    """使用PyMuPDF提取（文本型PDF）"""
    doc = fitz.open(stream=pdf_content, filetype='pdf')
    full_text = ''
    for page in doc:
        html = page.get_text('html')
        codes = re.findall(r'&#x([0-9a-fA-F]+);', html)
        for c in codes:
            try:
                full_text += chr(int(c, 16))
            except:
                pass
    return full_text

def extract_with_pdfplumber(pdf_file):
    """使用pdfplumber提取（扫描版PDF）"""
    with pdfplumber.open(pdf_file) as pdf:
        all_text = ''
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + '\n'
    return all_text

def extract_strategy_section(full_text):
    """提取投资策略部分"""
    content_parts = []
    
    # 关键词变体
    keywords = [
        '4.4 报告期内基金的投资策略和运作分析',
        '报告期内基金的投资策略和运作分析',
        '4.4 报告期内基金的投资策略和运作分析',
    ]
    
    for kw in keywords:
        if kw in full_text:
            idx1 = full_text.find(kw)
            idx2 = full_text.find('4.5', idx1)
            if idx2 == -1:
                idx2 = full_text.find('4.6', idx1)
            if idx2 == -1:
                idx2 = idx1 + 2500
            section = full_text[idx1:idx2].strip()
            if len(section) > 50:
                content_parts.append(section)
            break
    
    return '\n\n'.join(content_parts)

def process_reports(code, name, output_dir):
    """处理基金报告"""
    print(f'获取公告列表: {code}')
    df = get_announcements(code)
    
    # 筛选定期报告
    keywords = ['年度报告', '中期报告', '季度报告']
    df_reports = df[df['公告标题'].str.contains('|'.join(keywords), na=False)].copy()
    df_reports = df_reports.sort_values('公告日期')
    
    print(f'找到 {len(df_reports)} 份定期报告')
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for idx, row in df_reports.iterrows():
        report_id = row['报告ID']
        date = row['公告日期']
        
        pdf_url = f'http://pdf.dfcfw.com/pdf/H2_{report_id}_1.pdf'
        
        try:
            resp = requests.get(pdf_url, timeout=30)
            if len(resp.content) < 5000:
                continue
            
            # 保存临时文件
            with open('temp.pdf', 'wb') as f:
                f.write(resp.content)
            
            # 尝试两种提取方式
            full_text = None
            
            # 方法1: pdfplumber
            try:
                full_text = extract_with_pdfplumber('temp.pdf')
            except:
                pass
            
            # 方法2: PyMuPDF
            if not full_text or len(full_text) < 100:
                try:
                    full_text = extract_with_pymupdf(resp.content)
                except:
                    pass
            
            if full_text and len(full_text) > 100:
                content = extract_strategy_section(full_text)
                if len(content) > 100:
                    filename = f'{output_dir}/{date}.txt'
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'OK: {date} ({len(content)} chars)')
                    count += 1
            
            os.remove('temp.pdf')
            time.sleep(1)
            
        except Exception as e:
            print(f'Error: {date} - {e}')
    
    print(f'\n完成! 成功提取 {count} 份报告')
    
    # 生成汇总文件
    create_summary(output_dir, name, code)

def create_summary(output_dir, name, code):
    """生成汇总文件"""
    files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
    files.sort()
    
    output = []
    output.append('='*80)
    output.append(f'{name}投资策略和运作分析汇总')
    output.append(f'基金代码: {code}')
    output.append('='*80)
    output.append('')
    
    for f in files:
        with open(f'{output_dir}/{f}', 'r', encoding='utf-8') as file:
            content = file.read()
        output.append(f'--- {f} ---')
        output.append(content)
        output.append('')
    
    summary_file = f'{name}_投资策略汇总.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f'汇总文件: {summary_file}')

def main():
    parser = argparse.ArgumentParser(description='提取基金定期报告投资策略')
    parser.add_argument('--code', required=True, help='基金代码')
    parser.add_argument('--name', required=True, help='基金名称')
    
    args = parser.parse_args()
    
    output_dir = f'reports_{args.code}'
    process_reports(args.code, args.name, output_dir)

if __name__ == '__main__':
    main()
