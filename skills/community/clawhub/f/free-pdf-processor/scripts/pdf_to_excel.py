#!/usr/bin/env python3
"""
PDF 转 Excel 脚本
用法: python pdf_to_excel.py <pdf_path> <output.xlsx>
"""
import sys
import argparse
from pathlib import Path

try:
    import fitz
    import pdfplumber
    import pandas as pd
except ImportError as e:
    print(f"Error: Missing dependency. {e}")
    print("Run: pip install pymupdf pdfplumber pandas openpyxl")
    sys.exit(1)


def pdf_to_excel(pdf_path: str, output_path: str) -> bool:
    """将 PDF 转换为 Excel 文件"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # 第一页：提取所有文本作为备注
        doc = fitz.open(pdf_path)
        all_text = []
        
        for page_num, page in enumerate(doc, 1):
            text = page.get_text().strip()
            if text:
                all_text.append(f"=== 第 {page_num} 页 ===\n{text}")
        
        if all_text:
            df_text = pd.DataFrame({'PDF文本内容': all_text})
            df_text.to_excel(writer, sheet_name='文本内容', index=False)
        
        doc.close()
        
        # 其他页：提取表格
        sheet_index = 1
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                
                if tables:
                    for table_idx, table in enumerate(tables):
                        if table and len(table) > 1:
                            sheet_name = f"P{page_num}T{table_idx + 1}"
                            
                            # 处理表格数据
                            headers = table[0] if table else []
                            data = table[1:] if len(table) > 1 else []
                            
                            df = pd.DataFrame(data, columns=headers)
                            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
                            sheet_index += 1
        
        # 如果没有提取到任何表格，添加提示
        if sheet_index == 1:
            df_note = pd.DataFrame({'提示': ['此PDF未检测到表格数据，仅提取了文本内容']})
            df_note.to_excel(writer, sheet_name='说明', index=False)
    
    print(f"转换完成: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='PDF 转 Excel')
    parser.add_argument('pdf_path', help='输入 PDF 文件路径')
    parser.add_argument('output_path', help='输出 Excel 文件路径')
    
    args = parser.parse_args()
    
    try:
        pdf_to_excel(args.pdf_path, args.output_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
