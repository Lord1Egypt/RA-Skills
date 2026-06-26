#!/usr/bin/env python3
"""
上市公司"一页纸"简报生成主流程（优化版 v5）
完整财务数据表格 + 公司详细信息
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from fetch_company_data import main as fetch_data
from generate_chart import generate_kline_chart
from generate_markdown_v6 import generate_markdown_report
from generate_pdf import generate_pdf

def create_onepager(stock_code: str, output_dir: str = None) -> dict:
    """创建上市公司"一页纸"简报"""
    
    if not output_dir:
        output_dir = os.path.expanduser(
            f"~/.openclaw/workspace/temp/onepager_{stock_code.replace('.', '_')}"
        )
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 文件路径
    data_file = os.path.join(output_dir, "data.json")
    chart_file = os.path.join(output_dir, "chart.png")
    md_file = os.path.join(output_dir, f"{stock_code.replace('.', '_')}_简报.md")
    pdf_file = os.path.join(output_dir, f"{stock_code.replace('.', '_')}_简报.pdf")
    
    print(f"=== 开始生成 {stock_code} 简报 ===")
    print(f"输出目录: {output_dir}")
    
    # Step 1: 获取完整数据
    print("\n[1/4] 获取公司数据...")
    data = fetch_data(stock_code)
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"数据保存: {data_file}")
    
    # 数据验证
    financial = data.get('financial_data', {})
    valid_years = sum(1 for y in financial.get('annual', {}) 
                     if financial['annual'][y].get('revenue'))
    
    kline = data.get('kline_data', {})
    
    print(f"\n数据统计:")
    print(f"  - 财务数据: {valid_years} 年有效")
    print(f"  - K线数据: {kline.get('data_count', 0)} 条")
    print(f"  - 新闻数据: {len(data.get('news', []))} 条")
    
    # Step 2: 生成K线图
    print("\n[2/4] 生成K线图...")
    chart_result = ""
    
    if kline and kline.get('dates') and len(kline['dates']) >= 10:
        try:
            company_name = data.get('basic_info', {}).get('company_name', stock_code)
            chart_result = generate_kline_chart(
                kline,
                chart_file,
                title=f"{company_name} - 近10年月K线"
            )
            print(f"K线图保存: {chart_result}")
        except Exception as e:
            print(f"图表生成失败: {e}")
    else:
        print(f"K线数据不足 ({kline.get('data_count', 0)} 条)")
    
    # Step 3: 生成 Markdown
    print("\n[3/4] 生成 Markdown 报告...")
    md_content = generate_markdown_report(data, chart_result, md_file)
    print(f"Markdown 保存: {md_file}")
    
    # Step 4: 转换 PDF
    print("\n[4/4] 转换 PDF...")
    pdf_result = generate_pdf(md_file, pdf_file)
    
    if pdf_result:
        print(f"PDF 保存: {pdf_result}")
    else:
        print("PDF 转换失败")
    
    print(f"\n=== 简报生成完成 ===")
    
    return {
        "stock_code": stock_code,
        "company_name": data.get('basic_info', {}).get('company_name'),
        "data_path": data_file,
        "chart_path": chart_result,
        "markdown_path": md_file,
        "html_path": md_file.replace('.md', '.html'),
        "pdf_path": pdf_result,
        "output_dir": output_dir,
        "financial_years": valid_years,
        "kline_months": kline.get('data_count', 0),
        "news_count": len(data.get('news', [])),
        "sources_used": data.get('sources_used', []),
    }

def main():
    parser = argparse.ArgumentParser(description='生成上市公司一页纸简报（完整财务数据）')
    parser.add_argument("stock_code", help="股票代码（如 600519.SH, 000001.SZ）")
    parser.add_argument("-o", "--output", help="输出目录", default=None)
    
    args = parser.parse_args()
    
    result = create_onepager(args.stock_code, args.output)
    
    # 输出结果摘要
    print("\n=== 输出文件 ===")
    print(f"数据: {result['data_path']}")
    print(f"图表: {result['chart_path']}")
    print(f"Markdown: {result['markdown_path']}")
    print(f"PDF: {result['pdf_path']}")
    
    print("\n=== JSON Result ===")
    result_json = {k: v for k, v in result.items() if k != 'markdown_content'}
    print(json.dumps(result_json, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()