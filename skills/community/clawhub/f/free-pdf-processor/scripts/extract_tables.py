#!/usr/bin/env python3
"""
PDF 表格提取脚本
用法: python extract_tables.py <pdf_path> [--output <output.xlsx>]
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz
    import pdfplumber
except ImportError:
    print("Error: Missing dependencies. Run: pip install pymupdf pdfplumber")
    sys.exit(1)


def extract_tables(pdf_path: str, output_path: str = None) -> list:
    """提取 PDF 表格数据"""
    tables_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            
            if tables:
                for table_idx, table in enumerate(tables):
                    if table:  # 过滤空表格
                        tables_data.append({
                            'page': page_num,
                            'table_index': table_idx + 1,
                            'data': table
                        })
                        print(f"第{page_num}页 - 表格{table_idx + 1}: {len(table)}行 x {len(table[0]) if table else 0}列")
    
    # 如果指定了输出路径，保存为 Excel
    if output_path:
        try:
            import pandas as pd
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for idx, table_info in enumerate(tables_data):
                    sheet_name = f"Page{table_info['page']}_Table{table_info['table_index']}"
                    df = pd.DataFrame(table_info['data'][1:], columns=table_info['data'][0])
                    df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            
            print(f"\n表格已保存到: {output_path}")
        except ImportError:
            print("Warning: pandas 未安装，仅输出原始数据")
    
    return tables_data


def main():
    parser = argparse.ArgumentParser(description='提取 PDF 表格')
    parser.add_argument('pdf_path', help='PDF 文件路径')
    parser.add_argument('--output', '-o', help='输出 Excel 文件路径')
    
    args = parser.parse_args()
    
    try:
        tables = extract_tables(args.pdf_path, args.output)
        print(f"\n共提取 {len(tables)} 个表格")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()