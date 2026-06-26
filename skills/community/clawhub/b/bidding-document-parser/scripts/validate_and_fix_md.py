#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 文档格式检查与自动修复工具
用于检查和修复招标文件解析报告中的常见格式问题
"""

import re
import sys
import os
from collections import Counter


def _is_page_col(header_text):
    """判断某列表头是否为'页码'列"""
    if not header_text:
        return False
    return '页码' in header_text or 'page' in header_text.lower() or '页数' in header_text


def _is_page_value(text):
    """判断某单元格内容是否像页码"""
    if not text:
        return False
    return bool(re.search(r'P\d', text))


def _is_seq_value(text):
    """判断某单元格内容是否像序号"""
    if not text:
        return False
    return bool(re.match(r'^\d+(\.\d+)?$', text.strip())) and len(text.strip()) <= 6


def _align_short_row_fix(cells, header_col_count, header_cells, complete_rows=None):
    """
    智能对齐短行：在缺失的列位置插入空单元格。

    策略优先级：
    1. 页码列对齐：末列是页码列且末单元格像页码 → 页码放末列，中间补空
    2. 参考行+表头语义对齐：
       a) 基于完整行统计哪些列常为空
       b) 叠加表头语义（"备注"等列空列可能性高）
       c) 结合当前行内容模式调整
    3. 兜底：末尾补空
    """
    deficit = header_col_count - len(cells)
    if deficit <= 0:
        return cells[:header_col_count]

    # --- 策略1：页码列对齐 ---
    if len(header_cells) > 0 and _is_page_col(header_cells[-1]) and len(cells) > 0 and _is_page_value(cells[-1]):
        non_page = cells[:-1]
        page_val = cells[-1]
        padding_needed = header_col_count - len(non_page) - 1
        normalized = non_page + [''] * padding_needed + [page_val]
        print(f"    页码前补空修复: 页码放到最后一列，中间补空")
        return normalized

    # --- 策略2：参考行+表头语义对齐 ---
    emptiness = [0.0] * header_col_count

    # 2a: 基于表头语义的先验得分
    for col_idx in range(min(len(header_cells), header_col_count)):
        h = header_cells[col_idx].strip()
        if '备注' in h or '说明' in h or '其他' in h:
            emptiness[col_idx] = 0.7
        elif _is_page_col(h):
            emptiness[col_idx] = 0.02
        elif '序号' in h or '编号' in h:
            emptiness[col_idx] = 0.01
        else:
            emptiness[col_idx] = 0.2

    # 2b: 叠加参考行的实际空列频率
    if complete_rows:
        for col_idx in range(header_col_count):
            empty_count = sum(1 for r in complete_rows if col_idx < len(r) and not r[col_idx].strip())
            freq = empty_count / len(complete_rows)
            emptiness[col_idx] = 0.4 * emptiness[col_idx] + 0.6 * freq

    # 2c: 结合当前行内容模式调整
    for cell in cells:
        cell_text = cell.strip()
        if _is_page_value(cell_text):
            for col_idx in range(min(len(header_cells), header_col_count)):
                if _is_page_col(header_cells[col_idx]):
                    emptiness[col_idx] = 0.0
        elif _is_seq_value(cell_text):
            for col_idx in range(min(len(header_cells), header_col_count)):
                if '序号' in header_cells[col_idx] or '编号' in header_cells[col_idx]:
                    emptiness[col_idx] = 0.0

    # 选择得分最高的 deficit 个位置作为空列插入点
    scored_positions = list(enumerate(emptiness))
    scored_positions.sort(key=lambda x: (-x[1], -x[0]))
    insert_positions = set(idx for idx, score in scored_positions[:deficit])

    # 构建对齐后的行
    result = []
    cell_idx = 0
    for col_idx in range(header_col_count):
        if col_idx in insert_positions:
            result.append('')
        else:
            if cell_idx < len(cells):
                result.append(cells[cell_idx])
                cell_idx += 1
            else:
                result.append('')

    strategy = '参考行+语义' if complete_rows else '表头语义'
    print(f"    智能对齐修复({strategy}策略): 空列插入位置={sorted(insert_positions)}")
    return result


def fix_table_format(table_lines):
    """
    修复表格格式问题
    1. 检查表头和数据行的列数是否一致
    2. 移除多余的空单元格分隔符
    3. 确保每行的列数与表头一致（智能对齐）
    """
    if not table_lines:
        return table_lines
    
    # 过滤空行和分隔线
    content_lines = []
    for line in table_lines:
        line = line.rstrip()
        if not line or re.match(r'^[\|\-\:\s]+$', line):
            continue
        content_lines.append(line)
    
    if not content_lines:
        return table_lines
    
    # 解析每行的列数
    def count_columns(line):
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|'):
            line = line[:-1]
        cells = [c.strip() for c in line.split('|')]
        return len(cells), cells
    
    # 获取表头列数
    header_line = content_lines[0]
    header_col_count, header_cells = count_columns(header_line)
    
    print(f"  表头列数: {header_col_count}")
    print(f"  表头内容: {header_cells}")

    # 预先收集完整行用于参考行分析
    complete_data_rows = []
    for line in content_lines[1:]:
        col_count, cells = count_columns(line)
        if col_count == header_col_count:
            complete_data_rows.append(cells)
    
    # 修复每一行
    fixed_lines = [content_lines[0]]  # 保留原始表头
    
    # 添加分隔线
    separator = '| ' + ' | '.join(['---'] * header_col_count) + ' |'
    fixed_lines.append(separator)
    
    # 修复数据行
    for line in content_lines[1:]:
        col_count, cells = count_columns(line)
        
        if col_count != header_col_count:
            print(f"  发现列数不匹配: 期望 {header_col_count} 列，实际 {col_count} 列")
            print(f"    原始内容: {line}")
            
            if col_count > header_col_count:
                # 列数过多，截断到表头列数
                cells = cells[:header_col_count]
            else:
                # 列数过少：智能对齐
                cells = _align_short_row_fix(cells, header_col_count, header_cells, complete_data_rows)
            
            # 重新构建行
            fixed_line = '| ' + ' | '.join(cells) + ' |'
            print(f"    修复后内容: {fixed_line}")
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    return fixed_lines

def validate_and_fix_markdown(md_file_path, fix=True):
    """
    验证并修复Markdown文件中的格式问题
    
    Args:
        md_file_path: MD文件路径
        fix: 是否自动修复（默认True）
    
    Returns:
        (bool, str): (是否有错误, 错误信息或修复后的内容)
    """
    print(f"\n正在检查文件: {md_file_path}")
    print("=" * 60)
    
    if not os.path.exists(md_file_path):
        return False, f"文件不存在: {md_file_path}"
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    in_table = False
    table_lines = []
    table_count = 0
    errors = []
    
    for i, line in enumerate(lines, 1):
        # 检测表格开始
        if line.strip().startswith('|') and not in_table:
            in_table = True
            table_lines = [line]
            continue
        
        # 在表格中
        if in_table:
            if line.strip().startswith('|'):
                table_lines.append(line)
                continue
            else:
                # 表格结束，处理表格
                table_count += 1
                print(f"\n检查表格 #{table_count} (行 {i-len(table_lines)}-{i-1}):")
                
                if fix:
                    fixed_table = fix_table_format(table_lines)
                    fixed_lines.extend(fixed_table)
                else:
                    fixed_lines.extend(table_lines)
                
                in_table = False
                table_lines = []
        
        # 非表格行，直接添加
        fixed_lines.append(line)
    
    # 处理文件末尾的表格
    if in_table and table_lines:
        table_count += 1
        print(f"\n检查表格 #{table_count} (文件末尾):")
        if fix:
            fixed_table = fix_table_format(table_lines)
            fixed_lines.extend(fixed_table)
        else:
            fixed_lines.extend(table_lines)
    
    print("\n" + "=" * 60)
    print(f"检查完成，共发现 {table_count} 个表格")
    
    if fix:
        # 写回文件
        fixed_content = '\n'.join(fixed_lines)
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"✓ 已自动修复并保存: {md_file_path}")
        return True, "已自动修复"
    else:
        return len(errors) > 0, "\n".join(errors)

def main():
    if len(sys.argv) < 2:
        print("用法: python validate_and_fix_md.py <md文件路径> [--check-only]")
        print("  --check-only: 仅检查，不自动修复")
        sys.exit(1)
    
    md_file = sys.argv[1]
    check_only = '--check-only' in sys.argv
    
    if check_only:
        has_error, msg = validate_and_fix_markdown(md_file, fix=False)
        if has_error:
            print("\n发现以下格式问题:")
            print(msg)
            sys.exit(1)
        else:
            print("\n✓ 未发现格式问题")
    else:
        validate_and_fix_markdown(md_file, fix=True)

if __name__ == '__main__':
    main()
