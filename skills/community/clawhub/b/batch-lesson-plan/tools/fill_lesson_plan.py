# -*- coding: utf-8 -*-
"""
通用教案填充工具（自适配任意 docx 模板）

用法:
    # 分析模板结构（输出 JSON 到 stdout）
    python fill_lesson_plan.py --analyze <模板.docx> [> structure.json]

    # 填充（自动分析传入的模板）
    python fill_lesson_plan.py <内容JSON> <输出.docx> [模板.docx]

    # 填充（用预先生成的结构描述，跳过模板分析）
    python fill_lesson_plan.py <内容JSON> <输出.docx> --structure <structure.json>

    # 不传任何模板时，使用内置默认结构（15 行标准中专教案）

内容 JSON 结构:
{
  "fields": {
    "teacher": "...", "course": "...", "textbook": "...",
    "class": "...", "content": "...", "hours": "2课时"
  },
  "cells": {
    "4,2": ["段落1", "段落2"],   // (row, col) -> 多段内容
    "5,2": [...],
    ...
  }
}

技术要点：必须用 zipfile + lxml 直改 document.xml，禁用 python-docx（会破坏 vMerge）。
"""
import json
import os
import sys
import zipfile
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XMLSPACE = '{http://www.w3.org/XML/1998/namespace}space'

# ===== 内置默认结构（不传任何模板时使用） =====
DEFAULT_TEMPLATE = (
    os.environ.get('LESSON_TEMPLATE')
    or os.path.join(
        os.path.expanduser('~'), '.workbuddy', 'skills', 'zhongshan-lesson-plan',
        'templates', '中专教案模板.docx')
)

DEFAULT_STRUCTURE = {
    "row_count": 15,
    "rows": [
        {"cells": 4, "vMerges": [None, None, None, None]},
        {"cells": 2, "vMerges": [None, None]},
        {"cells": 2, "vMerges": [None, None]},
        {"cells": 4, "vMerges": [None, None, None, None]},
        {"cells": 3, "vMerges": ["restart", None, None]},
        {"cells": 3, "vMerges": ["continue", None, None]},
        {"cells": 3, "vMerges": ["continue", None, None]},
        {"cells": 2, "vMerges": [None, None]},
        {"cells": 2, "vMerges": [None, None]},
        {"cells": 2, "vMerges": [None, None]},
        {"cells": 1, "vMerges": [None]},
        {"cells": 3, "vMerges": [None, None, None]},
        {"cells": 3, "vMerges": [None, None, None]},
        {"cells": 4, "vMerges": [None, None, None, None]},
        {"cells": 2, "vMerges": [None, None]},
    ],
}

FONT = '宋体'
SZ = '21'  # 10.5pt


# ============================================================
#  模板分析
# ============================================================
def analyze_template(template_path):
    """读 docx 模板，提取表格结构。

    返回 dict：
      {
        "row_count": int,
        "rows": [
          {"cells": int, "vMerges": [None|"restart"|"continue", ...]},
          ...
        ]
      }
    """
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f'模板不存在: {template_path}')
    with zipfile.ZipFile(template_path, 'r') as z:
        root = etree.fromstring(z.read('word/document.xml'))
    tbl = root.find(W + 'body').find(W + 'tbl')
    if tbl is None:
        raise ValueError(f'模板中没有表格: {template_path}')
    rows = tbl.findall(W + 'tr')
    structure = {'row_count': len(rows), 'rows': []}
    for row in rows:
        cells = row.findall(W + 'tc')
        v_merges = []
        for c in cells:
            tcpr = c.find(W + 'tcPr')
            vm = tcpr.find(W + 'vMerge') if tcpr is not None else None
            if vm is None:
                v_merges.append(None)
            else:
                val = vm.get(W + 'val') or 'continue'
                v_merges.append(val)
        structure['rows'].append({'cells': len(cells), 'vMerges': v_merges})
    return structure


def validate_structure(docx_path, structure):
    """校验生成的 docx 是否符合模板结构。返回 (ok: bool, msg: str)。"""
    with zipfile.ZipFile(docx_path, 'r') as z:
        root = etree.fromstring(z.read('word/document.xml'))
    rows = root.findall('.//' + W + 'tr')
    if len(rows) != structure['row_count']:
        return False, f'行数不符: 期望 {structure["row_count"]}, 实际 {len(rows)}'
    for ri, exp in enumerate(structure['rows']):
        cells = rows[ri].findall(W + 'tc')
        if len(cells) != exp['cells']:
            return False, f'R{ri} 列数不符: 期望 {exp["cells"]}, 实际 {len(cells)}'
        for ci, vm in enumerate(exp['vMerges']):
            tcpr = cells[ci].find(W + 'tcPr')
            actual = tcpr.find(W + 'vMerge') if tcpr is not None else None
            if vm == 'restart':
                if actual is None or actual.get(W + 'val') != 'restart':
                    return False, f'R{ri}C{ci} vMerge=restart 缺失'
            elif vm == 'continue':
                if actual is None or actual.get(W + 'val') not in (None, 'continue'):
                    return False, f'R{ri}C{ci} vMerge=continue 缺失'
    return True, '结构完整'


# ============================================================
#  内容填充
# ============================================================
def make_paragraph(text, alignment='left'):
    p = etree.Element(W + 'p')
    pPr = etree.SubElement(p, W + 'pPr')
    jc = etree.SubElement(pPr, W + 'jc')
    jc.set(W + 'val', alignment)
    sp = etree.SubElement(pPr, W + 'spacing')
    sp.set(W + 'before', '20')
    sp.set(W + 'after', '20')
    sp.set(W + 'line', '320')
    sp.set(W + 'lineRule', 'auto')
    r = etree.SubElement(p, W + 'r')
    rPr = etree.SubElement(r, W + 'rPr')
    rf = etree.SubElement(rPr, W + 'rFonts')
    rf.set(W + 'ascii', FONT)
    rf.set(W + 'hAnsi', FONT)
    rf.set(W + 'eastAsia', FONT)
    sz = etree.SubElement(rPr, W + 'sz')
    sz.set(W + 'val', SZ)
    szCs = etree.SubElement(rPr, W + 'szCs')
    szCs.set(W + 'val', SZ)
    t = etree.SubElement(r, W + 't')
    t.text = text
    t.set(XMLSPACE, 'preserve')
    return p


def fill_cell(cell, content):
    for p in cell.findall(W + 'p'):
        cell.remove(p)
    lines = [content] if isinstance(content, str) else content
    for line in lines:
        if str(line).strip():
            cell.append(make_paragraph(str(line)))


def build_cells(spec):
    """fields + cells -> {(row, col): content}"""
    f = spec.get('fields', {})
    cmap = {
        (0, 1): f.get('teacher', ''),
        (0, 3): f.get('course', ''),
        (1, 1): f.get('textbook', ''),
        (2, 1): f.get('class', ''),
        (3, 1): f.get('content', ''),
        (3, 3): f.get('hours', ''),
    }
    for key, val in spec.get('cells', {}).items():
        r, c = (int(x) for x in key.split(','))
        cmap[(r, c)] = val
    return cmap


def fill_docx(src, out_path, spec):
    """把内容 JSON 写入源模板，输出新 docx。返回填充后的 docx 路径。"""
    cmap = build_cells(spec)
    with zipfile.ZipFile(src, 'r') as z:
        root = etree.fromstring(z.read('word/document.xml'))
    tbl = root.find(W + 'body').find(W + 'tbl')
    rows = tbl.findall(W + 'tr')

    n = 0
    for (ri, ci), content in cmap.items():
        cells = rows[ri].findall(W + 'tc')
        if ci >= len(cells):
            print(f'WARN: JSON 中 ({ri},{ci}) 超出该行单元格数 {len(cells)}，跳过', file=sys.stderr)
            continue
        fill_cell(cells[ci], content)
        n += 1

    new_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    if os.path.exists(out_path):
        os.remove(out_path)
    with zipfile.ZipFile(src, 'r') as zin, zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, new_xml)
            else:
                zout.writestr(item, zin.read(item.filename))
    return n


# ============================================================
#  命令行入口
# ============================================================
def usage_and_exit():
    print(__doc__)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args:
        usage_and_exit()

    # --analyze <模板>
    if args[0] == '--analyze':
        if len(args) < 2:
            print('用法: python fill_lesson_plan.py --analyze <模板.docx>', file=sys.stderr)
            sys.exit(1)
        try:
            structure = analyze_template(args[1])
        except (FileNotFoundError, ValueError) as e:
            print(f'ERROR: {e}', file=sys.stderr)
            sys.exit(1)
        print(json.dumps(structure, ensure_ascii=False, indent=1))
        sys.exit(0)

    # --structure <structure.json> [可选]
    pre_structure = None
    if '--structure' in args:
        i = args.index('--structure')
        if i + 1 >= len(args):
            print('ERROR: --structure 后面必须跟 JSON 路径', file=sys.stderr)
            sys.exit(1)
        with open(args[i + 1], encoding='utf-8') as fh:
            pre_structure = json.load(fh)
        del args[i:i + 2]

    if len(args) < 2:
        usage_and_exit()

    spec_path, out_path = args[0], args[1]
    src = args[2] if len(args) > 2 else None

    with open(spec_path, encoding='utf-8') as fh:
        spec = json.load(fh)

    # 决定模板 + 结构
    if src is not None and os.path.isfile(src):
        # 用户传了模板文件 → 用它 + 自动分析结构
        structure = pre_structure or analyze_template(src)
    elif pre_structure is not None:
        # 用户没传模板，但提供了预生成结构 → 用内置默认空白模板不可用，需要 src
        print('ERROR: 提供了 --structure 但未指定模板文件，无法生成 docx', file=sys.stderr)
        sys.exit(1)
    else:
        # 用户没传模板 → 用内置默认（前提是默认模板存在）
        src = DEFAULT_TEMPLATE
        if not os.path.isfile(src):
            print(f'ERROR: 未传模板，且默认模板不可用 ({src}).\n'
                  f'       请用第 3 个命令行参数传入模板路径，或设置 LESSON_TEMPLATE。',
                  file=sys.stderr)
            sys.exit(1)
        structure = DEFAULT_STRUCTURE

    # 填充
    n = fill_docx(src, out_path, spec)

    # 校验
    ok, msg = validate_structure(out_path, structure)
    rows_info = json.dumps([r['cells'] for r in structure['rows']])
    print(f'filled={n} rows={structure["row_count"]} cells_spec={rows_info}')
    print(f'validate: {msg}')
    print('OUTPUT:', out_path)
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()