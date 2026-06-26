#!/usr/bin/env python3
"""
报销助手 - 凭证文件命名工具
用法: python rename_files.py
"""

import os
import shutil
from datetime import datetime

# 报销凭证目录
OUTPUT_DIR = "报销助手/报销凭证"

def rename_file(src_path, date, location, amount, file_type, ext):
    """
    重命名凭证文件
    格式: 日期-地点-金额-资料类型.扩展名
    
    会做两件事：
    1. 将原文件重命名（原地改名）
    2. 复制一份到报销凭证目录
    """
    filename = f"{date}-{location}-{amount}-{file_type}{ext}"
    
    # 1. 原文件重命名（原地改名）
    src_dir = os.path.dirname(src_path)
    renamed_path = os.path.join(src_dir, filename)
    shutil.move(src_path, renamed_path)
    
    # 2. 复制到报销凭证目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dst_path = os.path.join(OUTPUT_DIR, filename)
    shutil.copy(renamed_path, dst_path)
    
    return dst_path

def generate_report_summary():
    """
    生成报销汇总报告
    """
    import json
    
    # 读取业务招待费
    entertainment_file = "报销助手/业务招待费/记录.json"
    travel_file = "报销助手/差旅费用/记录.json"
    
    entertainment_total = 0
    travel_subsidy = 0
    invoice_collected = 0
    invoice_needed = 0
    
    if os.path.exists(entertainment_file):
        with open(entertainment_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for record in data.get('records', []):
                entertainment_total += record.get('金额', 0)
    
    if os.path.exists(travel_file):
        with open(travel_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            summary = data.get('汇总', {})
            travel_subsidy = summary.get('交通补贴标准', 0)
            invoice_collected = summary.get('已有发票金额', 0)
            invoice_needed = summary.get('还需发票金额', 0)
    
    report = f"""
    ============ 报销汇总 ============
    
    业务招待费: ¥{entertainment_total:.2f}
    交通补贴: ¥{invoice_collected:.2f} / ¥{travel_subsidy:.2f}
    发票差额: ¥{invoice_needed:.2f}
    
    可报销合计: ¥{entertainment_total + invoice_collected:.2f}
    """
    
    return report

if __name__ == "__main__":
    print(generate_report_summary())
