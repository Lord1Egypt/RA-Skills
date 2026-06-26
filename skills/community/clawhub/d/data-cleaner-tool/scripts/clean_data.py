#!/usr/bin/env python3
"""
数据清洗工具 - 智能处理重复、缺失、格式问题
"""

import argparse
import sys
import re
from pathlib import Path
import pandas as pd

def load_data(file_path):
    """加载数据"""
    path = Path(file_path)
    if path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        print(f"错误：不支持的格式 {path.suffix}")
        sys.exit(1)

def save_data(df, file_path):
    """保存数据"""
    path = Path(file_path)
    output = path.parent / f"{path.stem}_cleaned{path.suffix}"
    
    if path.suffix == '.csv':
        df.to_csv(output, index=False)
    else:
        df.to_excel(output, index=False)
    
    return output

def smart_dedup(df, keep='first'):
    """智能去重"""
    original = len(df)
    df = df.drop_duplicates(keep=keep)
    removed = original - len(df)
    return df, removed

def fill_missing(df, strategy='mean'):
    """填充缺失值（只填充确实有缺失的列）"""
    filled_count = 0
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            if df[col].dtype in ['int64', 'float64']:
                if strategy == 'mean':
                    fill_value = df[col].mean()
                elif strategy == 'median':
                    fill_value = df[col].median()
                elif strategy == 'zero':
                    fill_value = 0
                df[col] = df[col].fillna(fill_value)
            else:
                df[col] = df[col].fillna('未知')
            filled_count += missing
    return df, filled_count

def fix_phone(phone):
    """标准化手机号"""
    if pd.isna(phone):
        return phone
    phone = str(phone).strip()
    # 移除非数字字符
    phone = re.sub(r'\D', '', phone)
    # 补全11位手机号
    if len(phone) == 10 and phone.startswith('1'):
        phone = '1' + phone
    return phone

def fix_dates(df):
    """标准化日期格式"""
    date_patterns = [
        (r'(\d{4})/(\d{1,2})/(\d{1,2})', r'\1-\2-\3'),  # 2024/01/01 -> 2024-01-01
        (r'(\d{4})年(\d{1,2})月(\d{1,2})日', r'\1-\2-\3'),  # 2024年1月1日 -> 2024-1-1
        (r'(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{2}):(\d{2})', r'\1-\2-\3'),  # 去除时间
    ]
    fixed = 0
    for col in df.columns:
        if 'date' in col.lower() or '日期' in col or '时间' in col:
            for row_idx, val in enumerate(df[col]):
                if pd.notna(val):
                    original = str(val)
                    for pattern, replacement in date_patterns:
                        new_val = re.sub(pattern, replacement, str(val))
                        if new_val != original:
                            df.at[row_idx, col] = new_val
                            fixed += 1
                            break
    return df, fixed

def fix_phones(df):
    """修复整列手机号"""
    fixed = 0
    for col in df.columns:
        if 'phone' in col.lower() or '手机' in col:
            original = df[col].copy()
            df[col] = df[col].apply(fix_phone)
            fixed += (original != df[col]).sum()
    return df, fixed

def clean_data(input_file, output_format=None, dedup=True, fillna='mean', fix_phone=True, fix_date=True):
    """清洗数据主函数"""
    print(f"📂 加载文件: {input_file}")
    df = load_data(input_file)
    print(f"📊 原始数据: {len(df)}行 x {len(df.columns)}列")
    
    stats = {}
    
    # 去重
    if dedup:
        df, removed = smart_dedup(df)
        stats['去重'] = removed
        print(f"✓ 去重: 移除 {removed} 条重复记录")
    
    # 填充缺失值
    if fillna:
        df, filled = fill_missing(df, fillna)
        stats['填充缺失'] = filled
        print(f"✓ 填充缺失值: {filled} 处")
    
    # 修复手机号
    if fix_phone:
        df, fixed = fix_phones(df)
        if fixed > 0:
            stats['修复手机号'] = fixed
            print(f"✓ 修复手机号: {fixed} 处")
    
    # 修复日期格式
    if fix_date:
        df, fixed = fix_dates(df)
        if fixed > 0:
            stats['修复日期'] = fixed
            print(f"✓ 修复日期格式: {fixed} 处")
    
    # 保存
    output_file = output_format if output_format else input_file
    output_path = save_data(df, output_file)
    print(f"\n✅ 清洗完成!")
    print(f"📁 输出文件: {output_path}")
    print(f"📊 最终数据: {len(df)}行")
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='数据清洗工具')
    parser.add_argument('input', help='输入文件 (CSV/Excel)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--no-dedup', action='store_true', help='禁用去重')
    parser.add_argument('--fillna', choices=['mean', 'median', 'zero', 'none'], 
                        default='mean', help='缺失值填充策略')
    parser.add_argument('--fix-phone', action='store_true', help='修复手机号')
    parser.add_argument('--fix-date', action='store_true', default=True, help='修复日期格式（默认开启）')
    
    args = parser.parse_args()
    
    clean_data(args.input, args.output, not args.no_dedup, args.fillna, args.fix_phone)

if __name__ == '__main__':
    main()
