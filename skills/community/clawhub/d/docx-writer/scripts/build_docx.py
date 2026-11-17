#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx-writer 内容脚本（模板：academic）

用法
----
  1. 复制此文件到工作目录
  2. 改 TEMPLATE_NAME / OUTPUT / FIG_DIR / FN_TEXT_MAP（也可用下面的 CLI 参数覆盖）
  3. 在 build_content() 里用 B/H1/H2/H3/Tc/add_img/add_tbl 写内容
  4. python build_docx.py

CLI（全部可选，缺省即文件内常量，**向后兼容**）
  --template NAME   模板名或 yaml/json 路径（默认 academic）
  --out FILE        输出 docx（默认 输出路径.docx，写当前工作目录）
  --fig-dir DIR     图片基准目录（默认 图片目录）
  --fn-map REF      脚注映射：JSON 文件路径或内联 JSON（默认文件内 FN_TEXT_MAP）

排版全部来自 templates/<TEMPLATE_NAME>.yaml，本文件只负责内容。
要换体例，只需改 TEMPLATE_NAME（academic / push / news / ...），正文代码不用动。
"""
import sys, os, json, argparse

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from docx_engine import Template, Builder

# ═══════════════════ 配置（可被 CLI 覆盖） ═══════════════════
TEMPLATE_NAME = 'academic'          # templates/ 下的模板名（或 yaml 绝对路径）
OUTPUT = r'输出路径.docx'             # 默认写当前工作目录
FIG_DIR = r'图片目录'
FN_TEXT_MAP = {
    'F1': '作者. 标题. 期刊, 年份, 卷(期): 页码.',
}

# 由 _init() 建立；B/H1/... 等薄封装依赖它
_b = None


def _init(template_name=None, fn_map=None):
    global _b
    _b = Builder(Template.load(template_name or TEMPLATE_NAME))
    _b.fn_map.update(fn_map if fn_map is not None else FN_TEXT_MAP)
    return _b


# 模块导入即按默认配置初始化（保持原「import 后 _b/B() 即可用」行为）
_init()


# ═══════════════════ 排版函数（薄封装，勿改） ═══════════════════
def B(t):   return _b.para(t, style='body')        # 正文
def Bs(t):  return _b.para(t, style='abstract')    # 小字正文（摘要）
def H1(t):  return _b.heading(t, style='h1')       # 一级标题
def H2(t):  return _b.heading(t, style='h2')       # 二级标题
def H3(t):  return _b.heading(t, style='h3')       # 三级标题
def Tc(t):  return _b.caption(t)                   # 表题/图题


def add_img(path, cap):
    p = path if os.path.isabs(path) else os.path.join(FIG_DIR, path)
    return _b.image(p, caption=cap)


def add_tbl(h, rows):
    return _b.table(h, rows)


def Fx(latex, cap=None):
    """行间公式（XeLaTeX 真排版 → 紧裁 PNG，居中）。"""
    return _b.formula(latex, caption=cap)


def Lx(text, lx_map, style='body'):
    """含行内公式占位 {X1} 的段落，如 Lx('由 {X1} 可得', {'X1': r'\\alpha_0'})。"""
    return _b.para(text, style=style, lx_map=lx_map)


# ═══════════════════ 正文 ═══════════════════
def build_content():
    # 示例：
    # H1('一、引言')
    # B('这是正文{F1}。')
    # add_img('fig1.png', '图1  示意')
    # add_tbl(['列1', '列2'], [['a', 'b']])
    pass


def _load_fn_map(ref):
    """ref = JSON 文件路径 或 内联 JSON 字符串。"""
    if os.path.exists(ref):
        with open(ref, 'r', encoding='utf-8') as f:
            return json.load(f)
    return json.loads(ref)


def main(argv=None):
    global TEMPLATE_NAME, OUTPUT, FIG_DIR, FN_TEXT_MAP
    ap = argparse.ArgumentParser(
        description='docx-writer 内容脚本（不带参数时行为与原来完全一致）')
    ap.add_argument('--template', default=TEMPLATE_NAME,
                    help='模板名或 yaml/json 路径（默认 %(default)s）')
    ap.add_argument('--out', default=OUTPUT,
                    help='输出 docx 路径（默认 %(default)s，写当前工作目录）')
    ap.add_argument('--fig-dir', default=FIG_DIR,
                    help='图片基准目录（默认 %(default)s）')
    ap.add_argument('--fn-map', default=None,
                    help='脚注映射：JSON 文件路径或内联 JSON（默认文件内 FN_TEXT_MAP）')
    a = ap.parse_args(argv)

    TEMPLATE_NAME, OUTPUT, FIG_DIR = a.template, a.out, a.fig_dir
    if a.fn_map:
        FN_TEXT_MAP = _load_fn_map(a.fn_map)

    _init(TEMPLATE_NAME, FN_TEXT_MAP)
    build_content()
    _b.save(OUTPUT)
    print('Saved: %s' % OUTPUT, file=sys.stderr)


if __name__ == '__main__':
    main()
