#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF财报文本提取工具
提取PDF文件中的文本内容，保留表格结构
"""

import sys
import json
import pdfplumber
from pathlib import Path


def extract_pdf_text(pdf_path: str) -> dict:
    """
    提取PDF文件中的文本内容
    
    Args:
        pdf_path: PDF文件路径
        
    Returns:
        dict: 包含提取的文本和元数据
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    result = {
        "filename": pdf_path.name,
        "pages": [],
        "tables": [],
        "full_text": ""
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            result["total_pages"] = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages, 1):
                # 提取页面文本
                text = page.extract_text() or ""
                
                # 提取表格
                tables = page.extract_tables()
                
                page_data = {
                    "page_number": i,
                    "text": text,
                    "tables_count": len(tables)
                }
                
                result["pages"].append(page_data)
                result["full_text"] += f"\n--- Page {i} ---\n{text}\n"
                
                # 保存表格数据
                for j, table in enumerate(tables):
                    result["tables"].append({
                        "page": i,
                        "table_index": j,
                        "data": table
                    })
                    
    except Exception as e:
        result["error"] = str(e)
        
    return result


def save_extracted_data(data: dict, output_path: str = None):
    """
    保存提取的数据到文件
    
    Args:
        data: 提取的数据字典
        output_path: 输出文件路径（可选）
    """
    if output_path is None:
        # 默认输出到同名.json文件
        base_name = Path(data["filename"]).stem
        output_path = f"{base_name}_extracted.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 同时保存纯文本版本
    text_output = output_path.replace('.json', '.txt')
    with open(text_output, 'w', encoding='utf-8') as f:
        f.write(data["full_text"])
    
    return output_path, text_output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_pdf.py <pdf文件路径>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    try:
        print(f"正在提取: {pdf_file}")
        data = extract_pdf_text(pdf_file)
        
        json_path, txt_path = save_extracted_data(data)
        
        print(f"[OK] 提取完成")
        print(f"  总页数: {data.get('total_pages', 0)}")
        print(f"  表格数: {len(data['tables'])}")
        print(f"  JSON输出: {json_path}")
        print(f"  文本输出: {txt_path}")
        
    except Exception as e:
        print(f"[ERROR] 提取失败: {e}")
        sys.exit(1)
