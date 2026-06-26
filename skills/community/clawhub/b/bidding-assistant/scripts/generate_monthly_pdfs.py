#!/usr/bin/env python3
"""生成当月月报PDF"""

import os
import sys
from datetime import datetime

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_generator import PDFGenerator

# 设置正确的数据库路径（与采集器一致）
db_path = os.path.expanduser('~/.openclaw/workspace/skills/bidding-assistant/招投标数据/history.db')
output_dir = os.path.expanduser('~/.openclaw/workspace/skills/bidding-assistant/招投标数据/daily')

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 获取当前年月
now = datetime.now()
year = now.year
month = now.month

print("="*60)
print(f"招投标月报PDF生成 - {year}年{month:02d}月")
print("="*60)
print(f"\n数据库路径: {db_path}")
print(f"数据库存在: {os.path.exists(db_path)}")
print(f"输出目录: {output_dir}")

# 初始化PDF生成器
generator = PDFGenerator(db_path=db_path)
generator.output_dir = output_dir

# 生成当月月报
print("\n" + "="*60)
print(f"正在生成 {year}年{month:02d}月 月报...")
print("="*60)
pdf = generator.generate_monthly_report(year, month)
if pdf:
    print(f"[OK] 月报生成成功: {pdf}")
    print(f"文件大小: {os.path.getsize(pdf) / 1024:.1f} KB")
else:
    print("[ERROR] 月报生成失败")

print("\n" + "="*60)
print("完成!")
print("="*60)