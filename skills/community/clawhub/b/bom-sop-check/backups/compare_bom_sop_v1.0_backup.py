#!/usr/bin/env python3
"""
BOM 与 SOP 校对脚本（v1.0）
- 解析 BOM 和 SOP 文件
- 对比物料差异
- 标注差异单元格（红色/黄色）
"""

import sys
import os
import zipfile
import xml.etree.ElementTree as ET
import re
import shutil
import logging
import traceback
from typing import Dict, List, Optional, Tuple, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NS = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

# 填充颜色
RED_FILL = '<fill><patternFill patternType="solid"><fgColor rgb="FFFF0000"/></patternFill></fill>'
YELLOW_FILL = '<fill><patternFill patternType="solid"><fgColor rgb="FFFFFF00"/></patternFill></fill>'

# 常量
MAX_STRING_LENGTH = 500
MAX_ROWS = 10000
MATERIAL_CODE_PATTERN = re.compile(r'^\d{5}-\d{3}-\d{3}$')


def decode_html_entities(s: str) -> str:
    """解码 HTML 实体（如 &#25955; -> 散）"""
    if not s:
        return s
    import html
    s = html.unescape(s)
    return s


class BOMError(Exception):
    """BOM校对相关错误"""
    pass


def safe_str(s: Any, max_len: int = 100) -> str:
    """安全转换为字符串"""
    if s is None:
        return ''
    s = str(s).strip()
    if len(s) > max_len:
        s = s[:max_len] + '...'
    return s


def get_cell_value(cell_content: str, shared_strings: List[str], full_cell: str = '') -> str:
    """提取单元格值（支持共享字符串和 inlineStr）"""
    # 优先检查 inlineStr
    is_match = re.search(r'<is><t[^>]*>([^<]*)</t></is>', cell_content)
    if is_match:
        return decode_html_entities(is_match.group(1))
    
    # 检查共享字符串
    v_match = re.search(r'<v>([^<]*)</v>', cell_content)
    if v_match:
        value = v_match.group(1)
        is_shared = 't="s"' in cell_content or 't="s"' in full_cell
        if is_shared:
            try:
                idx = int(value)
                if 0 <= idx < len(shared_strings):
                    return decode_html_entities(shared_strings[idx])
            except:
                pass
        return decode_html_entities(value)
    
    return ''


def validate_file(file_path: str, file_type: str) -> Tuple[bool, str]:
    """验证文件"""
    if not os.path.exists(file_path):
        return False, f"{file_type}文件不存在"
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.xlsx', '.xls']:
        return False, f"{file_type}文件格式不支持，仅支持 .xlsx 格式"
    
    file_size = os.path.getsize(file_path)
    if file_size > 100 * 1024 * 1024:
        return False, f"{file_type}文件过大（超过100MB）"
    
    return True, ""


def parse_bom_file(bom_path: str) -> Dict[str, Dict]:
    """解析 BOM 文件"""
    items = {}
    
    extract_dir = f'/tmp/bom_extract_{os.getpid()}'
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    with zipfile.ZipFile(bom_path, 'r') as zf:
        zf.extractall(extract_dir)
    
    worksheets_dir = os.path.join(extract_dir, 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in sorted(os.listdir(worksheets_dir)):
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        raise BOMError("BOM 文件中未找到工作表")
    
    ss_path = os.path.join(extract_dir, 'xl', 'sharedStrings.xml')
    shared_strings = []
    if os.path.exists(ss_path):
        with open(ss_path, 'r', encoding='utf-8') as f:
            ss_content = f.read()
        try:
            ss_root = ET.fromstring(ss_content)
            for si in ss_root.findall('main:si', NS):
                text_parts = []
                for t in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                    if t.text:
                        text_parts.append(t.text)
                shared_strings.append(''.join(text_parts))
        except:
            pass
    
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    code_col = 'I'
    name_col = 'J'
    spec_col = 'K'
    qty_num_col = 'N'
    qty_den_col = 'O'
    remark_col = 'P'
    
    for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
        row_num = int(row_match.group(1))
        if row_num < 2:
            continue
        
        row_content = row_match.group(2)
        row_data = {}
        for cell_match in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>]*>(.*?)</c>', row_content, re.DOTALL):
            col = cell_match.group(1)
            cell_content = cell_match.group(3)
            full_cell = cell_match.group(0)
            row_data[col] = get_cell_value(cell_content, shared_strings, full_cell)
        
        code = row_data.get(code_col, '')
        if not code or not MATERIAL_CODE_PATTERN.match(code):
            continue
        
        qty_num = row_data.get(qty_num_col, '')
        qty_den = row_data.get(qty_den_col, '')
        try:
            num = float(qty_num) if qty_num else 1
            den = float(qty_den) if qty_den else 1
            qty = num / den if den > 0 else num
            qty = int(qty) if qty == int(qty) else round(qty, 2)
        except:
            qty = qty_num or '1'
        
        name = row_data.get(name_col, '')
        spec = row_data.get(spec_col, '')
        name_spec = f"{name}|{spec}" if name and spec else (name or spec)
        
        items[code] = {
            'code': code,
            'name': name,
            'spec': spec,
            'name_spec': name_spec,
            'qty': str(qty),
            'remark': row_data.get(remark_col, ''),
            'row': row_num
        }
    
    return items


def parse_sop_file(sop_path: str) -> Dict:
    """解析 SOP 文件"""
    result = {
        'items': {},
        'cells': {},
        'extract_dir': f'/tmp/sop_extract_{os.getpid()}'
    }
    
    if os.path.exists(result['extract_dir']):
        shutil.rmtree(result['extract_dir'])
    
    with zipfile.ZipFile(sop_path, 'r') as zf:
        zf.extractall(result['extract_dir'])
    
    worksheets_dir = os.path.join(result['extract_dir'], 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in ['sheet2.xml', 'sheet1.xml']:
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        raise BOMError("SOP 文件中未找到工作表")
    
    ss_path = os.path.join(result['extract_dir'], 'xl', 'sharedStrings.xml')
    shared_strings = []
    if os.path.exists(ss_path):
        with open(ss_path, 'r', encoding='utf-8') as f:
            ss_content = f.read()
        try:
            ss_root = ET.fromstring(ss_content)
            for si in ss_root.findall('main:si', NS):
                text_parts = []
                for t in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                    if t.text:
                        text_parts.append(t.text)
                shared_strings.append(''.join(text_parts))
        except:
            pass
    
    result['shared_strings'] = shared_strings
    
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    result['sheet_content'] = sheet_content
    
    for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
        row_num = int(row_match.group(1))
        row_content = row_match.group(2)
        
        cells = {}
        for cell_match in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>/]*>(.*?)</c>', row_content, re.DOTALL):
            col = cell_match.group(1)
            cell_content = cell_match.group(3)
            full_cell = cell_match.group(0)
            cells[col] = get_cell_value(cell_content, shared_strings, full_cell)
        
        for cell_match in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>]*/>', row_content):
            col = cell_match.group(1)
            if col not in cells:
                cells[col] = ''
        
        code = cells.get('AQ', '')
        if not code or not MATERIAL_CODE_PATTERN.match(code):
            continue
        
        item = {
            'code': code,
            'name_spec': cells.get('AX', ''),
            'position': cells.get('BI', ''),
            'qty': cells.get('BO', ''),
            'row': row_num
        }
        
        result['items'][code] = item
        
        if code not in result['cells']:
            result['cells'][code] = []
        result['cells'][code].append({
            'row': row_num,
            'code_col': 'AQ',
            'name_col': 'AX',
            'position_col': 'BI',
            'qty_col': 'BO',
            'cells': cells
        })
    
    return result


def compare_bom_sop(bom_items: Dict, sop_items: Dict) -> Dict:
    """对比 BOM 和 SOP"""
    result = {
        'diffs': [],
        'only_bom': [],
        'only_sop': [],
        'matches': []
    }
    
    bom_codes = set(bom_items.keys())
    sop_codes = set(sop_items.keys())
    
    for code in bom_codes - sop_codes:
        result['only_bom'].append(code)
    
    for code in sop_codes - bom_codes:
        result['only_sop'].append(code)
    
    for code in bom_codes & sop_codes:
        bom_item = bom_items[code]
        sop_item = sop_items[code]
        
        diff_types = []
        diff_details = {}
        
        bom_name = safe_str(bom_item.get('name_spec', ''), 200)
        sop_name = safe_str(sop_item.get('name_spec', ''), 200)
        if bom_name and sop_name:
            bom_name_norm = re.sub(r'[\n\r]+', '|', bom_name)
            sop_name_norm = re.sub(r'[\n\r]+', '|', sop_name)
            bom_name_norm = re.sub(r'\s+', ' ', bom_name_norm).strip()
            sop_name_norm = re.sub(r'\s+', ' ', sop_name_norm).strip()
            if bom_name_norm != sop_name_norm:
                diff_types.append('名称规格')
                diff_details['名称规格'] = {'bom': bom_name, 'sop': sop_name}
        
        bom_pos = safe_str(bom_item.get('remark', ''), 50)
        sop_pos = safe_str(sop_item.get('position', ''), 50)
        if bom_pos and sop_pos:
            bom_pos_clean = re.sub(r'[\s,，]+', '', bom_pos)
            sop_pos_clean = re.sub(r'[\s,，]+', '', sop_pos)
            if bom_pos_clean != sop_pos_clean:
                diff_types.append('位号')
                diff_details['位号'] = {'bom': bom_pos, 'sop': sop_pos}
        
        bom_qty = safe_str(bom_item.get('qty', ''))
        sop_qty = safe_str(sop_item.get('qty', ''))
        if bom_qty and sop_qty:
            try:
                bom_qty_val = float(bom_qty)
                sop_qty_val = float(sop_qty)
                if abs(bom_qty_val - sop_qty_val) > 0.001:
                    diff_types.append('数量')
                    diff_details['数量'] = {'bom': bom_qty, 'sop': sop_qty}
            except:
                if bom_qty != sop_qty:
                    diff_types.append('数量')
                    diff_details['数量'] = {'bom': bom_qty, 'sop': sop_qty}
        
        if diff_types:
            result['diffs'].append({
                'code': code,
                'name': bom_item.get('name', sop_item.get('name_spec', '')),
                'diff_types': diff_types,
                'details': diff_details
            })
        else:
            result['matches'].append(code)
    
    return result


def generate_marked_file(result: Dict, bom_items: Dict, sop_data: Dict, output_dir: str) -> Optional[str]:
    """生成标注文件（v1.0 简单标注 - 仅标注差异，不追加 BOM 数据）"""
    if not result['diffs'] and not result['only_sop']:
        return None
    
    name = 'sop_vv6048m'
    if '---' in sop_data.get('name', ''):
        name = sop_data['name'].split('---')[0]
    
    worksheets_dir = os.path.join(sop_data['extract_dir'], 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in ['sheet2.xml', 'sheet1.xml']:
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        return None
    
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    styles_path = os.path.join(sop_data['extract_dir'], 'xl', 'styles.xml')
    if os.path.exists(styles_path):
        with open(styles_path, 'r', encoding='utf-8') as f:
            styles_content = f.read()
    else:
        styles_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"></styleSheet>'
    
    cellxfs_match = re.search(r'<cellXfs count="(\d+)">(.*?)</cellXfs>', styles_content, re.DOTALL)
    fills_count = 2
    red_xf_idx = 0
    yellow_xf_idx = 1
    
    if cellxfs_match:
        xfs_count = int(cellxfs_match.group(1))
        xfs_content = cellxfs_match.group(2)
        
        fills_match = re.search(r'<fills count="(\d+)">(.*?)</fills>', styles_content, re.DOTALL)
        if fills_match:
            fills_count = int(fills_match.group(1))
            fills_content = fills_match.group(2)
            new_fills = fills_content + RED_FILL + YELLOW_FILL
            styles_content = styles_content.replace(
                fills_match.group(0),
                f'<fills count="{fills_count + 2}">{new_fills}</fills>'
            )
        
        red_xf_idx = xfs_count
        yellow_xf_idx = xfs_count + 1
        
        new_xfs_content = xfs_content
        new_xfs_content += f'<xf numFmtId="0" fontId="0" fillId="{fills_count}" borderId="0" xfId="0"/>'
        new_xfs_content += f'<xf numFmtId="0" fontId="0" fillId="{fills_count+1}" borderId="0" xfId="0"/>'
        
        styles_content = styles_content.replace(
            cellxfs_match.group(0),
            f'<cellXfs count="{xfs_count+2}">{new_xfs_content}</cellXfs>'
        )
    
    with open(styles_path, 'w', encoding='utf-8') as f:
        f.write(styles_content)
    
    # 标注差异单元格
    diff_codes = set(d['code'] for d in result['diffs'])
    only_sop_codes = set(result['only_sop'])
    
    for code, cell_list in sop_data['cells'].items():
        for cell_info in cell_list:
            row = cell_info['row']
            
            if code in diff_codes:
                style_idx = red_xf_idx
            elif code in only_sop_codes:
                style_idx = yellow_xf_idx
            else:
                continue
            
            for col in [cell_info['name_col'], cell_info['position_col'], cell_info['qty_col']]:
                pattern = rf'<c r="{col}{row}"([^>]*)>(.*?)</c>'
                match = re.search(pattern, sheet_content, re.DOTALL)
                if match:
                    original_attrs = match.group(1)
                    cell_content = match.group(2)
                    
                    if 's="' in original_attrs:
                        new_attrs = re.sub(r's="\d+"', f's="{style_idx}"', original_attrs)
                    else:
                        new_attrs = f'{original_attrs} s="{style_idx}"'
                    
                    new_cell = f'<c r="{col}{row}"{new_attrs}>{cell_content}</c>'
                    sheet_content = sheet_content.replace(match.group(0), new_cell)
    
    with open(sheet_path, 'w', encoding='utf-8') as f:
        f.write(sheet_content)
    
    output_path = os.path.join(output_dir, f'{name}.xlsx')
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(sop_data['extract_dir']):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, sop_data['extract_dir'])
                zf.write(file_path, arc_name)
    
    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='BOM 与 SOP 校对工具 v1.0')
    parser.add_argument('bom', nargs='?', help='BOM 文件路径')
    parser.add_argument('sop', nargs='?', help='SOP 文件路径')
    parser.add_argument('--mark', '-m', action='store_true', help='生成标注文件')
    parser.add_argument('--output-dir', '-d', default='.', help='输出目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.bom or not args.sop:
        print("用法: python compare_bom_sop.py <bom_file> <sop_file> [--mark] [--output-dir DIR]")
        sys.exit(1)
    
    valid, msg = validate_file(args.bom, 'BOM')
    if not valid:
        print(f"错误: {msg}")
        sys.exit(1)
    
    valid, msg = validate_file(args.sop, 'SOP')
    if not valid:
        print(f"错误: {msg}")
        sys.exit(1)
    
    print(f"解析 BOM 文件: {os.path.basename(args.bom)}")
    bom_items = parse_bom_file(args.bom)
    print(f"BOM 共有 {len(bom_items)} 项物料")
    
    print(f"\n解析 SOP 文件: {os.path.basename(args.sop)}")
    sop_data = parse_sop_file(args.sop)
    print(f"SOP 共有 {len(sop_data['items'])} 项物料")
    
    result = compare_bom_sop(bom_items, sop_data['items'])
    
    if result['diffs'] or result['only_bom'] or result['only_sop']:
        print("\n" + "=" * 60)
        print("## ⚠️ 物料差异报告\n")
        print("| 物料编码 | 名称 | 差异类型 | BOM内容 | SOP内容 |")
        print("|----------|------|----------|---------|---------|")
        
        for diff in result['diffs']:
            for dtype in diff['diff_types']:
                detail = diff['details'].get(dtype, {})
                bom_val = safe_str(detail.get('bom', ''), 50)
                sop_val = safe_str(detail.get('sop', ''), 50)
                print(f"| {diff['code']} | {safe_str(diff['name'], 20)} | {dtype} | {bom_val} | {sop_val} |")
        
        print(f"\n**共 {len(result['diffs'])} 项物料存在差异**")
        print("\n---")
        print(f"**统计**：BOM独有 {len(result['only_bom'])} 项，SOP独有 {len(result['only_sop'])} 项，差异 {len(result['diffs'])} 项")
    else:
        print("\n✅ BOM 与 SOP 完全一致！")
    
    if args.mark:
        print("\n生成标注文件...")
        output_path = generate_marked_file(result, bom_items, sop_data, args.output_dir)
        if output_path:
            print(f"✅ SOP 标注文件: {output_path}")
        else:
            print("⚠️ 无需标注（无差异）")


if __name__ == '__main__':
    main()
