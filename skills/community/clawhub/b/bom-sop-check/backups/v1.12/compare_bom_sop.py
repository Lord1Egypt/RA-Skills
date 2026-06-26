#!/usr/bin/env python3
"""
BOM 与 SOP 校对脚本（v1.9）
- 解析 BOM 和 SOP 文件
- 对比物料差异
- 标注差异单元格（红色/黄色）
- 追加 BOM 数据到新列（BS/BT/BU）
- 新增校对报告工作表
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
    # 解码 HTML 实体
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
    """提取单元格值（支持共享字符串和 inlineStr）
    
    Args:
        cell_content: 单元格内容（<v>...</v> 部分）
        shared_strings: 共享字符串列表
        full_cell: 完整单元格标签（包含 t="s" 属性）
    """
    # 优先检查 inlineStr
    is_match = re.search(r'<is><t[^>]*>([^<]*)</t></is>', cell_content)
    if is_match:
        return decode_html_entities(is_match.group(1))
    
    # 检查共享字符串
    v_match = re.search(r'<v>([^<]*)</v>', cell_content)
    if v_match:
        value = v_match.group(1)
        # 检查 t="s" 属性（可能在 full_cell 或 cell_content 中）
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
    if file_size > 100 * 1024 * 1024:  # 100MB
        return False, f"{file_type}文件过大（超过100MB）"
    
    return True, ""


def parse_bom_file(bom_path: str) -> Dict[str, Dict]:
    """解析 BOM 文件"""
    items = {}
    
    # 解压 xlsx
    extract_dir = f'/tmp/bom_extract_{os.getpid()}'
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    with zipfile.ZipFile(bom_path, 'r') as zf:
        zf.extractall(extract_dir)
    
    # 查找工作表
    worksheets_dir = os.path.join(extract_dir, 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in sorted(os.listdir(worksheets_dir)):
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        raise BOMError("BOM 文件中未找到工作表")
    
    # 解析共享字符串（可能不存在）
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
    
    # 解析工作表
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    # 识别列位置（从第3行数据开始，因为前两行是表头信息）
    # BOM 文件结构：I=物料编码, J=物料名称, K=规格型号, N=用量分子, O=用量分母, P=备注
    
    code_col = 'I'
    name_col = 'J'
    spec_col = 'K'
    qty_num_col = 'N'  # 用量分子
    qty_den_col = 'O'  # 用量分母
    remark_col = 'P'
    
    # 解析数据行
    for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
        row_num = int(row_match.group(1))
        if row_num < 2:  # 跳过表头（第1行）
            continue
        
        row_content = row_match.group(2)
        
        # 提取各列值
        row_data = {}
        for cell_match in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>]*>(.*?)</c>', row_content, re.DOTALL):
            col = cell_match.group(1)
            cell_content = cell_match.group(3)
            full_cell = cell_match.group(0)
            row_data[col] = get_cell_value(cell_content, shared_strings, full_cell)
        
        # 获取物料编码
        code = row_data.get(code_col, '')
        if not code or not MATERIAL_CODE_PATTERN.match(code):
            continue
        
        # 计算数量
        qty_num = row_data.get(qty_num_col, '')
        qty_den = row_data.get(qty_den_col, '')
        try:
            num = float(qty_num) if qty_num else 1
            den = float(qty_den) if qty_den else 1
            qty = num / den if den > 0 else num
            qty = int(qty) if qty == int(qty) else round(qty, 2)
        except:
            qty = qty_num or '1'
        
        # 合并名称和规格
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
    
    # 解压 xlsx
    if os.path.exists(result['extract_dir']):
        shutil.rmtree(result['extract_dir'])
    
    with zipfile.ZipFile(sop_path, 'r') as zf:
        zf.extractall(result['extract_dir'])
    
    # 查找工作表（SOP 通常有多个 sheet，物料信息在第二个）
    worksheets_dir = os.path.join(result['extract_dir'], 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in ['sheet2.xml', 'sheet1.xml']:
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        raise BOMError("SOP 文件中未找到工作表")
    
    # 解析共享字符串
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
    
    # 解析工作表
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    result['sheet_content'] = sheet_content
    
    # 解析物料数据
    for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
        row_num = int(row_match.group(1))
        row_content = row_match.group(2)
        
        # 提取单元格（支持自闭合标签）
        cells = {}
        
        # 匹配有内容的标签：<c ... >... </c>（排除自闭合的情况）
        for cell_match in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>/]*>(.*?)</c>', row_content, re.DOTALL):
            col = cell_match.group(1)
            cell_content = cell_match.group(3)  # 第三个捕获组是内容
            full_cell = cell_match.group(0)  # 完整单元格标签
            cells[col] = get_cell_value(cell_content, shared_strings, full_cell)
        
        # 匹配自闭合标签：<c ... />
        for cell_match in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>]*/>', row_content):
            col = cell_match.group(1)
            if col not in cells:
                cells[col] = ''
        
        # 查找物料编码（在 AQ 列，按用户指定映射）
        code = cells.get('AQ', '')
        if not code or not MATERIAL_CODE_PATTERN.match(code):
            continue
        
        # 提取物料信息（按用户指定映射：AQ=物料编码, AX=名称规格, BI=位号, BO=数量）
        item = {
            'code': code,
            'name_spec': cells.get('AX', ''),  # 名称规格（AX 列）
            'position': cells.get('BI', ''),   # 位号（BI 列）
            'qty': cells.get('BO', ''),        # 数量（BO 列）
            'row': row_num
        }
        
        result['items'][code] = item
        
        # 使用列表存储所有行号（修复同一物料编码出现在多行的问题）
        if code not in result['cells']:
            result['cells'][code] = []
        result['cells'][code].append({
            'row': row_num,
            'code_col': 'AQ',
            'name_col': 'AX',      # 名称规格列
            'position_col': 'BI',  # 位号列
            'qty_col': 'BO',       # 数量列
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
    
    # BOM 独有
    for code in bom_codes - sop_codes:
        result['only_bom'].append(code)
    
    # SOP 独有
    for code in sop_codes - bom_codes:
        result['only_sop'].append(code)
    
    # 对比共有物料
    for code in bom_codes & sop_codes:
        bom_item = bom_items[code]
        sop_item = sop_items[code]
        
        diff_types = []
        diff_details = {}
        
        # 对比名称规格（忽略换行符和分隔符差异）
        bom_name = safe_str(bom_item.get('name_spec', ''), 200)
        sop_name = safe_str(sop_item.get('name_spec', ''), 200)
        if bom_name and sop_name:
            # 规范化比较：统一换行符和分隔符
            bom_name_norm = re.sub(r'[\n\r]+', '|', bom_name)
            sop_name_norm = re.sub(r'[\n\r]+', '|', sop_name)
            # 去除多余空格
            bom_name_norm = re.sub(r'\s+', ' ', bom_name_norm).strip()
            sop_name_norm = re.sub(r'\s+', ' ', sop_name_norm).strip()
            if bom_name_norm != sop_name_norm:
                diff_types.append('名称规格')
                diff_details['名称规格'] = {'bom': bom_name, 'sop': sop_name}
        
        # 对比位号
        bom_pos = safe_str(bom_item.get('remark', ''), 50)
        sop_pos = safe_str(sop_item.get('position', ''), 50)
        if bom_pos and sop_pos:
            # 简化位号比较（去掉空格和逗号差异）
            bom_pos_clean = re.sub(r'[\s,，]+', '', bom_pos)
            sop_pos_clean = re.sub(r'[\s,，]+', '', sop_pos)
            if bom_pos_clean != sop_pos_clean:
                diff_types.append('位号')
                diff_details['位号'] = {'bom': bom_pos, 'sop': sop_pos}
        
        # 对比数量
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
    """生成标注文件（v1.0 简单标注）"""
    if not result['diffs'] and not result['only_sop']:
        return None
    
    name = 'sop_vv6048m'
    if '---' in sop_data.get('name', ''):
        name = sop_data['name'].split('---')[0]
    
    # 读取 SOP 工作表
    worksheets_dir = os.path.join(sop_data['extract_dir'], 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in ['sheet2.xml', 'sheet1.xml']:
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        return None
    
    # 读取工作表内容
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    # 处理样式（添加红色和黄色填充）
    styles_path = os.path.join(sop_data['extract_dir'], 'xl', 'styles.xml')
    if os.path.exists(styles_path):
        with open(styles_path, 'r', encoding='utf-8') as f:
            styles_content = f.read()
    else:
        styles_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"></styleSheet>'
    
    # 添加填充样式和边框样式
    cellxfs_match = re.search(r'<cellXfs count="(\d+)">(.*?)</cellXfs>', styles_content, re.DOTALL)
    fills_count = 2
    red_xf_idx = 0
    yellow_xf_idx = 1
    border_xf_idx = 2  # 带边框样式
    
    if cellxfs_match:
        xfs_count = int(cellxfs_match.group(1))
        xfs_content = cellxfs_match.group(2)
        
        # 添加填充样式
        fills_match = re.search(r'<fills count="(\d+)">(.*?)</fills>', styles_content, re.DOTALL)
        if fills_match:
            fills_count = int(fills_match.group(1))
            fills_content = fills_match.group(2)
            new_fills = fills_content + RED_FILL + YELLOW_FILL
            styles_content = styles_content.replace(
                fills_match.group(0),
                f'<fills count="{fills_count + 2}">{new_fills}</fills>'
            )
        
        # 添加边框样式
        borders_match = re.search(r'<borders count="(\d+)">(.*?)</borders>', styles_content, re.DOTALL)
        borders_count = 1
        if borders_match:
            borders_count = int(borders_match.group(1))
            borders_content = borders_match.group(2)
            # 细边框
            thin_border = '<border><left style="thin"><color indexed="64"/></left><right style="thin"><color indexed="64"/></right><top style="thin"><color indexed="64"/></top><bottom style="thin"><color indexed="64"/></bottom><diagonal/></border>'
            new_borders = borders_content + thin_border
            styles_content = styles_content.replace(
                borders_match.group(0),
                f'<borders count="{borders_count + 1}">{new_borders}</borders>'
            )
        
        # 添加字体样式（加粗）
        fonts_match = re.search(r'<fonts count="(\d+)">(.*?)</fonts>', styles_content, re.DOTALL)
        fonts_count = 1
        if fonts_match:
            fonts_count = int(fonts_match.group(1))
            fonts_content = fonts_match.group(2)
            # 加粗字体
            bold_font = '<font><b/><sz val="11"/><color theme="1"/><name val="等线"/></font>'
            new_fonts = fonts_content + bold_font
            styles_content = styles_content.replace(
                fonts_match.group(0),
                f'<fonts count="{fonts_count + 1}">{new_fonts}</fonts>'
            )
        
        # 添加表头填充样式（浅蓝色背景）
        header_fill = '<fill><patternFill patternType="solid"><fgColor rgb="FFD9E8F7"/><bgColor indexed="64"/></patternFill></fill>'
        new_fills_content = fills_content + RED_FILL + YELLOW_FILL + header_fill
        header_fill_id = fills_count + 2
        
        styles_content = styles_content.replace(
            fills_match.group(0),
            f'<fills count="{fills_count + 3}">{new_fills_content}</fills>'
        )
        
        red_xf_idx = xfs_count
        yellow_xf_idx = xfs_count + 1
        border_xf_idx = xfs_count + 2  # 带边框样式索引
        header_xf_idx = xfs_count + 3  # 表头样式索引
        
        new_xfs_content = xfs_content
        # 红色填充
        new_xfs_content += f'<xf numFmtId="0" fontId="0" fillId="{fills_count}" borderId="0" xfId="0"/>'
        # 黄色填充
        new_xfs_content += f'<xf numFmtId="0" fontId="0" fillId="{fills_count+1}" borderId="0" xfId="0"/>'
        # 边框样式（无填充）
        new_xfs_content += f'<xf numFmtId="0" fontId="0" fillId="0" borderId="{borders_count}" xfId="0"/>'
        # 表头样式（加粗 + 浅蓝背景 + 边框）
        new_xfs_content += f'<xf numFmtId="0" fontId="{fonts_count}" fillId="{header_fill_id}" borderId="{borders_count}" xfId="0"/>'
        
        styles_content = styles_content.replace(
            cellxfs_match.group(0),
            f'<cellXfs count="{xfs_count+4}">{new_xfs_content}</cellXfs>'
        )
    
    with open(styles_path, 'w', encoding='utf-8') as f:
        f.write(styles_content)
    
    # v1.1：标注差异单元格 + 追加 BOM 数据到新列
    
    # 需要更新共享字符串（添加 BOM 数据）
    ss_path = os.path.join(sop_data['extract_dir'], 'xl', 'sharedStrings.xml')
    shared_strings = sop_data.get('shared_strings', [])
    new_strings = []
    
    # 收集所有需要添加的 BOM 数据字符串
    bom_data_to_add = {}  # row -> {name, qty, pos}
    
    # 标注差异单元格（红色）- 遍历所有行，同时收集 BOM 数据
    for diff in result['diffs']:
        code = diff['code']
        if code in sop_data['cells']:
            # 遍历该物料编码的所有行
            for cells_info in sop_data['cells'][code]:
                row = cells_info['row']
                
                # 获取 BOM 数据并记录
                bom_item = bom_items.get(code, {})
                bom_name = safe_str(bom_item.get('name_spec', ''), 100)
                bom_qty = safe_str(bom_item.get('qty', ''), 20)
                bom_pos = safe_str(bom_item.get('remark', ''), 100)
                
                bom_data_to_add[row] = {
                    'name': bom_name,
                    'qty': bom_qty,
                    'pos': bom_pos,
                    'style': red_xf_idx
                }
                
                # 标注差异列
                for diff_type in diff['diff_types']:
                    if diff_type == '名称规格':
                        col = cells_info.get('name_col', 'AX')
                    elif diff_type == '位号':
                        col = cells_info.get('position_col', 'BI')
                    elif diff_type == '数量':
                        col = cells_info.get('qty_col', 'BO')
                    else:
                        continue
                    
                    if col:
                        cell_ref = f"{col}{row}"
                        pattern = rf'(<c r="{cell_ref}"[^>]*?)>'
                        def add_style(m, idx=red_xf_idx):
                            tag = m.group(1)
                            if 's=' in tag:
                                return re.sub(r's="\d+"', f's="{idx}"', tag) + '>'
                            return tag + f' s="{idx}">'
                        sheet_content = re.sub(pattern, add_style, sheet_content)
    
    # 标注仅 SOP 存在的物料（黄色）- 遍历所有行
    for code in result['only_sop']:
        if code in sop_data['cells']:
            # 遍历该物料编码的所有行
            for cells_info in sop_data['cells'][code]:
                row = cells_info['row']
                
                bom_data_to_add[row] = {
                    'name': '',
                    'qty': '',
                    'pos': '',
                    'style': yellow_xf_idx
                }
                
                for col_key in ['name_col', 'position_col', 'qty_col']:
                    col = cells_info.get(col_key)
                    if col:
                        cell_ref = f"{col}{row}"
                        pattern = rf'(<c r="{cell_ref}"[^>]*?)>'
                        def add_style(m, idx=yellow_xf_idx):
                            tag = m.group(1)
                            if 's=' in tag:
                                return re.sub(r's="\d+"', f's="{idx}"', tag) + '>'
                            return tag + f' s="{idx}">'
                        sheet_content = re.sub(pattern, add_style, sheet_content)
    
    # ============ 在 BS 列开始添加 BOM 信息 ============
    # 列结构：BS=BOM名称, BT=BOM数量, BU=BOM位号
    bom_name_col = 'BS'
    bom_qty_col = 'BT'
    bom_pos_col = 'BU'
    
    # 收集所有需要添加的字符串
    all_strings_to_add = []
    
    # 为所有 SOP 物料行添加数据
    all_rows_data = {}  # row -> {code, sop_name, sop_qty, sop_pos, bom_name, bom_qty, bom_pos, has_diff}
    
    # 1. 检测合并单元格模式（在收集数据之前）
    merge_pattern = r'<mergeCell ref="AQ(\d+):AW(\d+)"'
    row_merges = {}  # first_row -> second_row
    for m in re.finditer(merge_pattern, sheet_content):
        start_row = int(m.group(1))
        end_row = int(m.group(2))
        if start_row != end_row:
            row_merges[start_row] = end_row
    
    logger.info(f"检测到 {len(row_merges)} 个合并单元格区域")
    
    # 创建第二行集合（用于跳过）
    second_rows = set(row_merges.values())
    logger.info(f"将跳过 {len(second_rows)} 个第二行")
    
    # 创建差异物料编码集合
    diff_codes = set(d['code'] for d in result['diffs'])
    only_sop_codes = set(result['only_sop'])
    marked_codes = diff_codes | only_sop_codes  # 所有需要标注的物料
    logger.info(f"有标注的物料: {len(marked_codes)} 项")
    
    # 2. 收集有标注物料的数据（只为合并区域的第一行添加）
    all_rows_data = {}  # row -> {code, bom_name, bom_qty, bom_pos, has_diff, is_only_sop}
    
    for code, cells_list in sop_data['cells'].items():
        # 只处理有标注的物料
        if code not in marked_codes:
            continue
        
        for cells_info in cells_list:
            row = cells_info['row']
            
            # 检查是否是合并区域的第二行（跳过）
            if row in second_rows:
                logger.debug(f"跳过合并区域第二行: {row}")
                continue
            
            cells = cells_info.get('cells', {})
            
            # BOM 数据
            bom_item = bom_items.get(code, {})
            bom_name = safe_str(bom_item.get('name_spec', ''), 100)
            bom_qty = safe_str(bom_item.get('qty', ''), 20)
            bom_pos = safe_str(bom_item.get('remark', ''), 100)
            
            # 是否有差异
            has_diff = code in diff_codes
            is_only_sop = code in only_sop_codes
            
            all_rows_data[row] = {
                'code': code,
                'bom_name': bom_name,
                'bom_qty': bom_qty,
                'bom_pos': bom_pos,
                'has_diff': has_diff,
                'is_only_sop': is_only_sop
            }
    
    # 3. 收集所有需要添加的字符串
    for row, data in sorted(all_rows_data.items()):
        for key in ['bom_name', 'bom_qty', 'bom_pos']:
            val = data.get(key, '')
            if val and val not in shared_strings and val not in all_strings_to_add:
                all_strings_to_add.append(val)
    
    # 4. 更新共享字符串
    ss_count = len(shared_strings)
    if all_strings_to_add:
        ss_content_new = '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{}">'.format(ss_count + len(all_strings_to_add))
        for s in shared_strings:
            s_escaped = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            ss_content_new += f'<si><t>{s_escaped}</t></si>'
        for s in all_strings_to_add:
            s_escaped = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            ss_content_new += f'<si><t>{s_escaped}</t></si>'
        ss_content_new += '</sst>'
        
        with open(ss_path, 'w', encoding='utf-8') as f:
            f.write(ss_content_new)
        
        shared_strings = shared_strings + all_strings_to_add
    
    # 4. 获取字符串索引
    def get_str_idx(s):
        if s in shared_strings:
            return shared_strings.index(s)
        return -1
    
    # 5. 添加表头行（在物料编码标题行）
    # 找到物料编码标题行（AQ 列内容为 "物料编码" 的行）
    header_row = None
    for m in re.finditer(r'<c r="AQ(\d+)"[^>]*><v>(\d+)</v></c>', sheet_content):
        row_num = int(m.group(1))
        str_idx = int(m.group(2))
        if str_idx < len(shared_strings) and shared_strings[str_idx] == '物料编码':
            header_row = row_num
            break
    
    if header_row:
        logger.info(f"物料编码标题行: {header_row}")
        
        # 添加表头字符串
        header_texts = ['BOM名称规格', 'BOM数量', 'BOM位号']
        for text in header_texts:
            if text not in shared_strings and text not in all_strings_to_add:
                all_strings_to_add.append(text)
        
        # 重新更新共享字符串
        if all_strings_to_add:
            ss_count = len(shared_strings)
            ss_content_new = '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{}">'.format(ss_count + len(all_strings_to_add))
            for s in shared_strings:
                s_escaped = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                ss_content_new += f'<si><t>{s_escaped}</t></si>'
            for s in all_strings_to_add:
                s_escaped = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                ss_content_new += f'<si><t>{s_escaped}</t></si>'
            ss_content_new += '</sst>'
            
            with open(ss_path, 'w', encoding='utf-8') as f:
                f.write(ss_content_new)
            
            shared_strings = shared_strings + all_strings_to_add
        
        # 在标题行添加表头单元格
        header_cells = ''
        for col, text in [(bom_name_col, 'BOM名称规格'), (bom_qty_col, 'BOM数量'), (bom_pos_col, 'BOM位号')]:
            idx = get_str_idx(text)
            if idx >= 0:
                header_cells += f'<c r="{col}{header_row}" s="{header_xf_idx}" t="s"><v>{idx}</v></c>'
        
        if header_cells:
            row_pattern = rf'(<row r="{header_row}"[^>]*>)(.*?)(</row>)'
            row_match = re.search(row_pattern, sheet_content, re.DOTALL)
            if row_match:
                row_start = row_match.group(1)
                row_content = row_match.group(2)
                row_end = row_match.group(3)
                new_row_content = row_start + row_content + header_cells + row_end
                sheet_content = sheet_content.replace(row_match.group(0), new_row_content)
                logger.info(f"已在行 {header_row} 添加 BOM 表头")
    
    # 6. 为每一行添加 BOM 单元格（支持合并行，带边框）
    new_merge_cells = []  # 新的合并单元格定义
    
    for row, data in sorted(all_rows_data.items()):
        new_cells = ''
        
        # 检查是否是合并区域的第一行
        merge_end_row = row_merges.get(row)
        
        # BS = BOM 名称规格（带边框）
        idx = get_str_idx(data['bom_name'])
        if idx >= 0:
            new_cells += f'<c r="{bom_name_col}{row}" s="{border_xf_idx}" t="s"><v>{idx}</v></c>'
        
        # BT = BOM 数量（带边框）
        idx = get_str_idx(data['bom_qty'])
        if idx >= 0:
            new_cells += f'<c r="{bom_qty_col}{row}" s="{border_xf_idx}" t="s"><v>{idx}</v></c>'
        
        # BU = BOM 位号（带边框）
        idx = get_str_idx(data['bom_pos'])
        if idx >= 0:
            new_cells += f'<c r="{bom_pos_col}{row}" s="{border_xf_idx}" t="s"><v>{idx}</v></c>'
        
        # 如果是合并区域的第一行，添加新的合并单元格定义
        if merge_end_row:
            for col in [bom_name_col, bom_qty_col, bom_pos_col]:
                new_merge_cells.append(f'<mergeCell ref="{col}{row}:{col}{merge_end_row}"/>')
        
        # 在行末添加新单元格
        if new_cells:
            row_pattern = rf'(<row r="{row}"[^>]*>)(.*?)(</row>)'
            row_match = re.search(row_pattern, sheet_content, re.DOTALL)
            if row_match:
                row_start = row_match.group(1)
                row_content = row_match.group(2)
                row_end = row_match.group(3)
                new_row_content = row_start + row_content + new_cells + row_end
                sheet_content = sheet_content.replace(row_match.group(0), new_row_content)
    
    # 6. 添加新的合并单元格定义
    if new_merge_cells:
        # 查找或创建 mergeCells 元素
        merge_cells_match = re.search(r'<mergeCells count="(\d+)">(.*?)</mergeCells>', sheet_content, re.DOTALL)
        if merge_cells_match:
            old_count = int(merge_cells_match.group(1))
            old_content = merge_cells_match.group(2)
            new_content = old_content + ''.join(new_merge_cells)
            new_merge_element = f'<mergeCells count="{old_count + len(new_merge_cells)}">{new_content}</mergeCells>'
            sheet_content = sheet_content.replace(merge_cells_match.group(0), new_merge_element)
            logger.info(f"添加了 {len(new_merge_cells)} 个新合并单元格")
    
    # 8. 更新列宽
    cols_pattern = r'<cols>(.*?)</cols>'
    cols_match = re.search(cols_pattern, sheet_content, re.DOTALL)
    if cols_match:
        cols_content = cols_match.group(1)
        new_cols = ''
        for col_letter in ['BS', 'BT', 'BU']:
            col_num = sum((ord(c) - ord('A') + 1) * (26 ** i) for i, c in enumerate(reversed(col_letter)))
            new_cols += f'<col min="{col_num}" max="{col_num}" width="30" customWidth="1"/>'
        
        new_cols_element = f'<cols>{cols_content}{new_cols}</cols>'
        sheet_content = sheet_content.replace(cols_match.group(0), new_cols_element)
        logger.info("更新了列宽")
    
    # 写回工作表
    with open(sheet_path, 'w', encoding='utf-8') as f:
        f.write(sheet_content)
    
    # ============ v1.9 新增：创建校对报告工作表 ============
    create_report_sheet(result, bom_items, sop_data, border_xf_idx, header_xf_idx)
    
    # 重新打包
    output_path = os.path.join(output_dir, f'{name}.xlsx')
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(sop_data['extract_dir']):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, sop_data['extract_dir'])
                zf.write(file_path, arc_name)
    
    return output_path


def create_report_sheet(result: Dict, bom_items: Dict, sop_data: Dict, border_xf_idx: int, header_xf_idx: int) -> None:
    """创建校对报告工作表（v1.12：分两个表格显示）"""
    extract_dir = sop_data['extract_dir']
    
    # 1. 先读取现有共享字符串数量
    ss_path = os.path.join(extract_dir, 'xl', 'sharedStrings.xml')
    existing_count = 0
    if os.path.exists(ss_path):
        with open(ss_path, 'r', encoding='utf-8') as f:
            ss_content = f.read()
        count_match = re.search(r'count="(\d+)"', ss_content)
        existing_count = int(count_match.group(1)) if count_match else 0
    
    # 2. 创建校对报告工作表 XML
    report_strings = []  # 新增的共享字符串
    
    def add_string(s):
        """添加字符串到共享字符串表，返回索引（含偏移量）"""
        if s in report_strings:
            return existing_count + report_strings.index(s)
        report_strings.append(s)
        return existing_count + len(report_strings) - 1
    
    # 构建工作表数据 - 分两个表格
    rows_xml = ''
    row_num = 1
    
    # ============ 表格1: SOP 独有物料 ============
    title1_idx = add_string('【SOP 独有物料】（SOP中有但BOM中没有）')
    rows_xml += f'<row r="{row_num}"><c r="A{row_num}" t="s"><v>{title1_idx}</v></c></row>'
    row_num += 1
    
    # 表头
    headers = ['物料编码', '物料名称', '名称规格', '数量', '位号']
    header_cells = ''
    for col_idx, header in enumerate(headers):
        col_letter = chr(ord('A') + col_idx)
        str_idx = add_string(header)
        header_cells += f'<c r="{col_letter}{row_num}" s="{header_xf_idx}" t="s"><v>{str_idx}</v></c>'
    rows_xml += f'<row r="{row_num}">{header_cells}</row>'
    row_num += 1
    
    # SOP 独有物料数据
    sop_only_count = 0
    for code in sorted(result['only_sop']):
        item = sop_data['items'].get(code, {})
        code_idx = add_string(code)
        name_idx = add_string('')
        spec_idx = add_string(safe_str(item.get('name_spec', ''), 50))
        qty_idx = add_string(safe_str(item.get('qty', ''), 20))
        pos_idx = add_string(safe_str(item.get('position', ''), 50))
        
        cells = f'<c r="A{row_num}" s="{border_xf_idx}" t="s"><v>{code_idx}</v></c>'
        cells += f'<c r="B{row_num}" s="{border_xf_idx}" t="s"><v>{name_idx}</v></c>'
        cells += f'<c r="C{row_num}" s="{border_xf_idx}" t="s"><v>{spec_idx}</v></c>'
        cells += f'<c r="D{row_num}" s="{border_xf_idx}" t="s"><v>{qty_idx}</v></c>'
        cells += f'<c r="E{row_num}" s="{border_xf_idx}" t="s"><v>{pos_idx}</v></c>'
        rows_xml += f'<row r="{row_num}">{cells}</row>'
        row_num += 1
        sop_only_count += 1
    
    # 空行分隔
    row_num += 1
    
    # ============ 表格2: BOM 独有物料 ============
    title2_idx = add_string('【BOM 独有物料】（BOM中有但SOP中没有）')
    rows_xml += f'<row r="{row_num}"><c r="A{row_num}" t="s"><v>{title2_idx}</v></c></row>'
    row_num += 1
    
    # 表头
    header_cells = ''
    for col_idx, header in enumerate(headers):
        col_letter = chr(ord('A') + col_idx)
        str_idx = add_string(header)
        header_cells += f'<c r="{col_letter}{row_num}" s="{header_xf_idx}" t="s"><v>{str_idx}</v></c>'
    rows_xml += f'<row r="{row_num}">{header_cells}</row>'
    row_num += 1
    
    # BOM 独有物料数据
    bom_only_count = 0
    for code in sorted(result['only_bom']):
        item = bom_items.get(code, {})
        code_idx = add_string(code)
        name_idx = add_string(safe_str(item.get('name', ''), 50))
        spec_idx = add_string(safe_str(item.get('spec', ''), 50))
        qty_idx = add_string(safe_str(item.get('qty', ''), 20))
        pos_idx = add_string(safe_str(item.get('remark', ''), 50))
        
        cells = f'<c r="A{row_num}" s="{border_xf_idx}" t="s"><v>{code_idx}</v></c>'
        cells += f'<c r="B{row_num}" s="{border_xf_idx}" t="s"><v>{name_idx}</v></c>'
        cells += f'<c r="C{row_num}" s="{border_xf_idx}" t="s"><v>{spec_idx}</v></c>'
        cells += f'<c r="D{row_num}" s="{border_xf_idx}" t="s"><v>{qty_idx}</v></c>'
        cells += f'<c r="E{row_num}" s="{border_xf_idx}" t="s"><v>{pos_idx}</v></c>'
        rows_xml += f'<row r="{row_num}">{cells}</row>'
        row_num += 1
        bom_only_count += 1
    
    # 生成工作表 XML
    max_row = row_num - 1
    sheet3_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>
<dimension ref="A1:E{max_row}"/>
<sheetViews><sheetView workbookViewId="0"/></sheetViews>
<sheetFormatPr defaultColWidth="15" defaultRowHeight="15"/>
<cols>
<col min="1" max="1" width="18" customWidth="1"/>
<col min="2" max="2" width="20" customWidth="1"/>
<col min="3" max="3" width="35" customWidth="1"/>
<col min="4" max="4" width="12" customWidth="1"/>
<col min="5" max="5" width="25" customWidth="1"/>
</cols>
<sheetData>{rows_xml}</sheetData>
<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
<pageSetup paperSize="9" orientation="portrait"/>
</worksheet>'''
    
    # 写入工作表文件
    worksheets_dir = os.path.join(extract_dir, 'xl', 'worksheets')
    sheet3_path = os.path.join(worksheets_dir, 'sheet3.xml')
    with open(sheet3_path, 'w', encoding='utf-8') as f:
        f.write(sheet3_content)
    logger.info(f"创建校对报告工作表: SOP独有 {sop_only_count} 项, BOM独有 {bom_only_count} 项")
    
    # 3. 更新共享字符串（追加新字符串）
    if os.path.exists(ss_path):
        # 生成新字符串条目
        new_strings = ''
        for s in report_strings:
            # 转义特殊字符
            s_escaped = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            new_strings += f'<si><t>{s_escaped}</t></si>'
        
        # 更新共享字符串文件
        new_count = existing_count + len(report_strings)
        # 在 </sst> 前插入新字符串
        ss_content = re.sub(r'</sst>', new_strings + '</sst>', ss_content)
        # 更新计数
        ss_content = re.sub(r'count="\d+"', f'count="{new_count}"', ss_content, count=1)
        
        with open(ss_path, 'w', encoding='utf-8') as f:
            f.write(ss_content)
    
    # 4. 更新 workbook.xml（添加新工作表）
    workbook_path = os.path.join(extract_dir, 'xl', 'workbook.xml')
    if os.path.exists(workbook_path):
        with open(workbook_path, 'r', encoding='utf-8') as f:
            workbook_content = f.read()
        
        # 在 <sheets> 中添加新工作表
        # 找到最大的 sheetId
        sheet_id_matches = re.findall(r'sheetId="(\d+)"', workbook_content)
        max_sheet_id = max(int(sid) for sid in sheet_id_matches) if sheet_id_matches else 1
        
        new_sheet = f'<sheet name="校对报告" sheetId="{max_sheet_id + 1}" r:id="rId8"/>'
        workbook_content = re.sub(r'</sheets>', new_sheet + '</sheets>', workbook_content)
        
        with open(workbook_path, 'w', encoding='utf-8') as f:
            f.write(workbook_content)
    
    # 4. 更新 workbook.xml.rels（添加新关系）
    rels_path = os.path.join(extract_dir, 'xl', '_rels', 'workbook.xml.rels')
    if os.path.exists(rels_path):
        with open(rels_path, 'r', encoding='utf-8') as f:
            rels_content = f.read()
        
        # 添加新关系
        new_rel = '<Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>'
        rels_content = re.sub(r'</Relationships>', new_rel + '</Relationships>', rels_content)
        
        with open(rels_path, 'w', encoding='utf-8') as f:
            f.write(rels_content)
    
    # 5. 更新 [Content_Types].xml（注册新工作表）
    content_types_path = os.path.join(extract_dir, '[Content_Types].xml')
    if os.path.exists(content_types_path):
        with open(content_types_path, 'r', encoding='utf-8') as f:
            ct_content = f.read()
        
        # 添加新工作表类型
        new_override = '<Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        ct_content = re.sub(r'</Types>', new_override + '</Types>', ct_content)
        
        with open(content_types_path, 'w', encoding='utf-8') as f:
            f.write(ct_content)
    
    logger.info("校对报告工作表创建完成")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='BOM 与 SOP 校对工具 v1.9')
    parser.add_argument('bom', nargs='?', help='BOM 文件路径')
    parser.add_argument('sop', nargs='?', help='SOP 文件路径')
    parser.add_argument('--mark', '-m', action='store_true', help='生成标注文件')
    parser.add_argument('--output-dir', '-d', default='./output', help='输出目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.bom:
        print("❌ 错误: 请提供文件路径")
        return 1
    
    bom_path = args.bom
    sop_path = args.sop
    
    # 验证文件
    is_valid, error_msg = validate_file(bom_path, 'BOM')
    if not is_valid:
        print(f"❌ 错误: {error_msg}")
        return 1
    
    if not sop_path:
        print("❌ 错误: 请提供 SOP 文件路径")
        return 1
    
    is_valid, error_msg = validate_file(sop_path, 'SOP')
    if not is_valid:
        print(f"❌ 错误: {error_msg}")
        return 1
    
    try:
        # 解析 BOM
        print(f"解析 BOM 文件: {os.path.basename(bom_path)}")
        bom_items = parse_bom_file(bom_path)
        print(f"BOM 共有 {len(bom_items)} 项物料")
        
        # 解析 SOP
        print(f"\n解析 SOP 文件: {os.path.basename(sop_path)}")
        sop_data = parse_sop_file(sop_path)
        sop_data['name'] = os.path.basename(sop_path)
        print(f"SOP 共有 {len(sop_data['items'])} 项物料")
        
        # 对比
        result = compare_bom_sop(bom_items, sop_data['items'])
        
        if result['diffs'] or result['only_bom'] or result['only_sop']:
            print("\n" + "=" * 60)
            print("## ⚠️ 物料差异报告\n")
            print("| 物料编码 | 名称 | 差异类型 | BOM内容 | SOP内容 |")
            print("|----------|------|----------|---------|---------|")
            
            for diff in result['diffs']:
                code = diff['code']
                name = safe_str(diff['name'], 20)
                
                for dt in diff['diff_types']:
                    details = diff['details'].get(dt, {})
                    bom_val = safe_str(details.get('bom', ''), 30)
                    sop_val = safe_str(details.get('sop', ''), 30)
                    print(f"| {code} | {name} | {dt} | {bom_val} | {sop_val} |")
            
            print(f"\n**共 {len(result['diffs'])} 项物料存在差异**")
            print("\n---")
            print(f"**统计**：BOM独有 {len(result['only_bom'])} 项，SOP独有 {len(result['only_sop'])} 项，差异 {len(result['diffs'])} 项")
        else:
            print("\n✅ BOM 与 SOP 完全一致！")
        
        # 生成标注文件
        if args.mark and (result['diffs'] or result['only_sop']):
            print("\n生成标注文件...")
            os.makedirs(args.output_dir, exist_ok=True)
            output_path = generate_marked_file(result, bom_items, sop_data, args.output_dir)
            if output_path:
                print(f"✅ SOP 标注文件: {output_path}")
            else:
                print("❌ 生成标注文件失败")
                return 1
        
        return 0
        
    except BOMError as e:
        print(f"❌ 错误: {e}")
        return 1
    except Exception as e:
        print(f"❌ 异常: {e}")
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
