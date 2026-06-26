#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portrait - 综合财务数据可视化工具

包含图表（每行两图，3行布局）：
1. 按账龄披露的应收账款期末账面余额
2. 境内外毛利率对比
3. 营业收入与营业成本堆积柱状图
4. 财务费用（利息收支）分组柱状图
5. 管理费用分类（前5项）堆积柱状图
6. 销售费用分类（前5项）堆积柱状图

用法示例：
    python Portrait.py 688002 --save
    python Portrait.py --all
"""

import os
import sys
import re
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ==================== 配色规范（参考 图表格式及配色规范指引202406.xlsx）====================
COLORS_BAR = [
    '#3B65AE',  # 1 深蓝  RGB(59,101,174)
    '#D1DDF1',  # 2 浅蓝  RGB(209,221,241)
    '#0B318F',  # 3 更深蓝 RGB(11,49,143)
    '#6E87B8',  # 4 中蓝  RGB(110,135,184)
    '#D0CECE',  # 5 浅灰  RGB(208,206,206)
    '#A7BCE4',  # 6 中浅蓝 RGB(167,188,228)
    '#4472C4',  # 7 中蓝  RGB(68,114,196)
    '#BFBFBF',  # 8 灰色  RGB(191,191,191)
]
COLORS_LINE = [
    '#0B318F',  # 1
    '#A7BCE4',  # 2
    '#BA9866',  # 3 金色 RGB(186,152,102)
    '#D0CECE',  # 4
    '#3B65AE',  # 5
    '#BFBFBF',  # 6
]
COLOR_AXIS = '#D9D9D9'       # 坐标轴 RGB(217,217,217)
COLOR_TEXT = '#3E3A39'       # 文字 RGB(62,58,57)

import matplotlib
from matplotlib import font_manager

# ==================== 字体加载 ====================
# 优先 skill assets/fonts/ 目录，其次系统路径
_script_dir = Path(__file__).parent
_local_font_dir = _script_dir.parent / "assets" / "fonts"

font_files = []
if _local_font_dir.exists():
    font_files += [
        str(_local_font_dir / "NotoSansCJK-Regular.ttc"),
        str(_local_font_dir / "NotoSansCJK-Bold.ttc"),
        str(_local_font_dir / "NotoSerifCJK-Regular.ttc"),
    ]
font_files += [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
]

for font_file in font_files:
    try:
        if Path(font_file).exists():
            font_manager.fontManager.addfont(font_file)
    except Exception:
        pass

# 预定义字体属性对象（供局部 text 使用）
_font_candidates = []
if _local_font_dir.exists():
    _font_candidates += [
        str(_local_font_dir / "NotoSansCJK-Regular.ttc"),
        str(_local_font_dir / "NotoSansCJK-Bold.ttc"),
    ]
_font_candidates += [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
]

font_sans = None
font_sans_bold = None
for fp in _font_candidates:
    if Path(fp).exists():
        if font_sans is None and 'Regular' in fp:
            font_sans = font_manager.FontProperties(fname=fp)
        if font_sans_bold is None and 'Bold' in fp:
            font_sans_bold = font_manager.FontProperties(fname=fp)
    if font_sans and font_sans_bold:
        break

# ==================== Matplotlib 全局设置 ====================
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Noto Sans CJK TC', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False
rcParams['axes.edgecolor'] = COLOR_AXIS
rcParams['axes.linewidth'] = 0.75
rcParams['xtick.color'] = COLOR_TEXT
rcParams['ytick.color'] = COLOR_TEXT
rcParams['axes.labelcolor'] = COLOR_TEXT
rcParams['text.color'] = COLOR_TEXT
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

# ==================== 数据解析工具函数 ====================
def parse_money(value) -> Optional[float]:
    """将金额字符串转为浮点数，处理 None/NaN/逗号/空字符串等情况"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        s = value.strip()
        if s in ('', 'None', 'none', '—', '-', 'nan', 'NaN'):
            return None
        s = s.replace(',', '').replace(' ', '')
        try:
            return float(s)
        except ValueError:
            return None
    return None


def parse_percent(value) -> Optional[float]:
    """将百分比字符串或数值转为小数，如 '85.32%' -> 0.8532, 29.28 -> 0.2928"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        v = float(value)
        # 如果数值明显大于1，假设是百分比数值（如29.28表示29.28%）
        if v > 1:
            return v / 100
        return v
    if isinstance(value, str):
        s = value.strip().replace('%', '').replace(' ', '')
        try:
            return float(s) / 100
        except ValueError:
            return None
    return None


# ==================== 股票索引类 ====================
@dataclass
class StockIndex:
    dirname: str
    code: str
    name: str
    dir_path: Path
    aging_file: Optional[Path] = None
    revenue_cost_file: Optional[Path] = None       # 营业收入和营业成本情况（主营业务，用于图1/图3）
    revenue_cost_detail_file: Optional[Path] = None # 营业收入、营业成本的分解信息（境内外，用于图2）
    finance_expense_file: Optional[Path] = None
    management_expense_file: Optional[Path] = None
    sales_expense_file: Optional[Path] = None
    rd_expense_file: Optional[Path] = None         # 研发费用（图8）
    impairment_file: Optional[Path] = None         # 资产减值损失（图3）
    non_operating_income_file: Optional[Path] = None  # 营业外收入（图4）
    inventory_file: Optional[Path] = None          # 存货分类（图10）
    employee_compensation_file: Optional[Path] = None # 应付职工薪酬列示（图11）
    fixed_asset_file: Optional[Path] = None        # 固定资产情况（图12）
    ip_file: Optional[Path] = None                 # 知识产权列表（图13）
    rnd_project_file: Optional[Path] = None        # 在研项目情况（图14）
    top5_customer_file: Optional[Path] = None      # 公司前五名客户（图15）
    top5_supplier_file: Optional[Path] = None      # 公司前五名供应商（图16）


class DataIndex:
    """全量数据索引，一次性扫描，后续快速查找"""
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.stocks: List[StockIndex] = []
        self._code_map: Dict[str, StockIndex] = {}
        self._name_map: Dict[str, StockIndex] = {}
        self._build_index()

    def _build_index(self):
        if not self.output_dir.exists():
            return
        for entry in self.output_dir.iterdir():
            if not entry.is_dir() or entry.name.startswith('.'):
                continue
            parts = entry.name.split('_', 1)
            if len(parts) != 2:
                continue
            code, name = parts
            stock = StockIndex(
                dirname=entry.name,
                code=code,
                name=name,
                dir_path=entry
            )
            # 查找按账龄披露文件（兼容 output 和 output2 的命名方式）
            aging_base = entry / "01_资产负债表附注" / "01_流动资产"
            if aging_base.exists():
                for f in aging_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "按账龄披露" in f.name or "应收账款" in f.name:
                            stock.aging_file = f
                            break
            # 查找收入成本文件：
            #   - "营业收入和营业成本情况" 用于图3（主营业务收入/成本）
            #   - "营业收入、营业成本的分解信息" 用于图2（境内外毛利率）
            revenue_base = entry / "02_利润表附注" / "01_收入成本"
            if revenue_base.exists():
                for f in revenue_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "营业收入和营业成本情况" in f.name:
                            stock.revenue_cost_file = f
                        elif "营业收入、营业成本的分解信息" in f.name:
                            stock.revenue_cost_detail_file = f
            # 查找期间费用文件
            expense_base = entry / "02_利润表附注" / "02_期间费用"
            if expense_base.exists():
                for f in expense_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "财务费用" in f.name:
                            stock.finance_expense_file = f
                        elif "管理费用" in f.name:
                            stock.management_expense_file = f
                        elif "销售费用" in f.name:
                            stock.sales_expense_file = f
                        elif "研发费用" in f.name:
                            stock.rd_expense_file = f
            # 查找其他损益文件
            other_profit_base = entry / "02_利润表附注" / "03_其他损益"
            if other_profit_base.exists():
                for f in other_profit_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "资产减值损失" in f.name:
                            stock.impairment_file = f
            # 查找营业外收支文件
            non_operating_base = entry / "02_利润表附注" / "04_营业外收支"
            if non_operating_base.exists():
                for f in non_operating_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "营业外收入" in f.name:
                            stock.non_operating_income_file = f
            # 查找存货分类文件
            inventory_base = entry / "01_资产负债表附注" / "01_流动资产"
            if inventory_base.exists():
                for f in inventory_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "存货分类" in f.name:
                            stock.inventory_file = f
            # 查找应付职工薪酬列示文件
            liability_base = entry / "01_资产负债表附注" / "03_流动负债"
            if liability_base.exists():
                for f in liability_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "应付职工薪酬列示" in f.name:
                            stock.employee_compensation_file = f
            # 查找固定资产情况文件
            non_current_asset_base = entry / "01_资产负债表附注" / "02_非流动资产"
            if non_current_asset_base.exists():
                for f in non_current_asset_base.iterdir():
                    if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                        if "固定资产情况" in f.name:
                            stock.fixed_asset_file = f
            # 查找管理层讨论与分析文件
            management_base = entry / "11_管理层讨论与分析"
            if management_base.exists():
                core_competence_base = management_base / "03_核心竞争力"
                if core_competence_base.exists():
                    for f in core_competence_base.iterdir():
                        if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                            if "知识产权列表" in f.name:
                                stock.ip_file = f
                            elif "在研项目情况" in f.name:
                                stock.rnd_project_file = f
                business_base = management_base / "05_主要经营情况"
                if business_base.exists():
                    for f in business_base.iterdir():
                        if f.is_file() and f.suffix in ('.xlsx', '.xls'):
                            if "公司前五名客户" in f.name:
                                stock.top5_customer_file = f
                            elif "公司前五名供应商" in f.name:
                                stock.top5_supplier_file = f
            self.stocks.append(stock)
            self._code_map[code] = stock
            self._name_map[name] = stock

    def search(self, query: str) -> Optional[StockIndex]:
        """根据代码或名称查找，支持精确匹配和模糊匹配"""
        query = query.strip()
        if not query:
            return None
        if query in self._code_map:
            return self._code_map[query]
        if query in self._name_map:
            return self._name_map[query]
        matches = []
        for s in self.stocks:
            if s.code.startswith(query) or query in s.name:
                matches.append(s)
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"找到多个匹配结果，请输入更精确的名称或代码：")
            for m in matches:
                print(f"  - {m.code} {m.name}")
            return None
        return None

    def list_all(self) -> List[StockIndex]:
        return self.stocks


# ==================== 数据加载：按账龄披露 ====================
def normalize_age_label(label) -> Optional[str]:
    """规范化账龄标签"""
    if pd.isna(label):
        return None
    label = str(label).strip()
    if label.startswith(('其中：', '减：', '加：', '202', '20')):
        return None
    non_age_keywords = ('借款', '往来款', '押金', '保证金', '备用金', '拆借', '代垫', '坏账准备',
                        '第一阶段', '第二阶段', '第三阶段', '转入', '转出')
    if any(kw in label for kw in non_age_keywords):
        return None
    if re.match(r'^(1年以内|6个月以内|6個月以內)', label):
        return '1年以内'
    if '小计' in label or label == '合计':
        return None
    if label in ('其他',):
        return None
    for pattern, std in [
        (r'^1至2年', '1至2年'),
        (r'^2至3年', '2至3年'),
        (r'^3年以上', '3年以上'),
        (r'^3至4年', '3至4年'),
        (r'^4至5年', '4至5年'),
        (r'^5年以上', '5年以上'),
    ]:
        if re.match(pattern, label):
            return std
    return label


def load_aging_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """
    读取按账龄披露 Excel，返回 DataFrame
    行索引：账龄类别；列：各年份；值：期末账面余额（元）
    """
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    all_sheets = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=0)
        except Exception:
            continue
        age_col = None
        val_col = None
        for c in df.columns:
            col_str = str(c)
            if '账龄' in col_str:
                age_col = c
            if '期末账面余额' in col_str:
                val_col = c
        if age_col is None or val_col is None:
            continue
        records = []
        for _, row in df.iterrows():
            label = normalize_age_label(row.get(age_col))
            if label is None:
                continue
            val = parse_money(row.get(val_col))
            if val is None:
                continue
            records.append({'账龄': label, '期末账面余额': val})
        if records:
            all_sheets[year] = records

    if not all_sheets:
        return None

    merged = {}
    for year, records in all_sheets.items():
        seen = {}
        for r in records:
            label = r['账龄']
            val = r['期末账面余额']
            if label not in seen:
                seen[label] = val
            elif val > seen[label]:
                seen[label] = val
        for label, val in seen.items():
            merged.setdefault(label, {})[year] = val

    result_df = pd.DataFrame.from_dict(merged, orient='index')
    if result_df.empty:
        return None
    result_df = result_df[sorted(result_df.columns)]
    result_df.index.name = '账龄'
    return result_df


# ==================== 数据加载：境内外毛利率 ====================
def load_region_gross_margin(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """
    读取营业收入、营业成本的分解信息，提取境内外毛利率。
    兼容 output / output2 两种数据结构：
      - 标准格式：列0=项目，列1=收入，列2=成本
      - output2 格式：列0=合同分类，列1~N 成对出现（收入, 成本），
        可能有多个分类（主营业务/其他业务/合计等），优先取"合计"列对，
        否则取第一个非空的有效列对。
    返回 DataFrame：行=['境内毛利率','境外毛利率']，列=各年份，值=毛利率（小数）
    """
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None

    domestic_labels = {'境内', '国内', '境内销售'}
    foreign_labels = {'境外', '国外', '境外销售'}

    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue

        # 1) 定位“按经营地区分类”标题行
        region_header_idx = None
        for i, row in df.iterrows():
            cell0 = str(row[0]) if pd.notna(row[0]) else ''
            if ('经营地' in cell0 and ('分类' in cell0 or '区' in cell0)) or '境内外' in cell0:
                region_header_idx = i
                break
        if region_header_idx is None:
            continue

        def _label_match(label: str, targets: set) -> bool:
            """模糊匹配标签，如 '其中:境内' -> '境内'"""
            pure = label.strip().lstrip('其中:').lstrip('其中：').strip()
            return pure in targets

        def _extract_rev_cost(row) -> tuple:
            """
            从一行中提取 (revenue, cost)。
            策略：遍历所有可能的（奇数列收入, 偶数列成本）对，
            收集 revenue>0 且 cost>=0 的有效对，取 revenue 最大的一对。
            在数据结构正常时，"合计"列对的 revenue 通常最大，因此会被自然选中；
            若出现数据错位导致"合计"列数值异常偏小，也能自动回退到正确列对。
            """
            candidates = []
            for rev_col in range(1, len(row), 2):  # 1, 3, 5, ...
                cost_col = rev_col + 1
                if cost_col >= len(row):
                    continue
                rev = parse_money(row[rev_col])
                cost = parse_money(row[cost_col])
                if rev is not None and rev > 0 and cost is not None and cost >= 0:
                    candidates.append((rev, cost))

            if candidates:
                return max(candidates, key=lambda x: x[0])
            return None, None

        domestic_revenue = None
        domestic_cost = None
        foreign_revenue = None
        foreign_cost = None

        for i in range(region_header_idx + 1, min(region_header_idx + 15, len(df))):
            row = df.iloc[i]
            label = str(row[0]).strip() if pd.notna(row[0]) else ''
            if not label:
                continue
            # 遇到新的分类标题（如"按商品转让的时间分类"）则停止
            if label.startswith(('按', '合')) and '经营地区' not in label and '境内外' not in label:
                break

            rev, cost = _extract_rev_cost(row)
            if rev is None:
                continue

            if _label_match(label, domestic_labels):
                domestic_revenue = rev
                domestic_cost = cost
            elif _label_match(label, foreign_labels):
                foreign_revenue = rev
                foreign_cost = cost

        dm = None
        fm = None
        if domestic_revenue is not None and domestic_revenue > 0 and domestic_cost is not None:
            dm = (domestic_revenue - domestic_cost) / domestic_revenue
        if foreign_revenue is not None and foreign_revenue > 0 and foreign_cost is not None:
            fm = (foreign_revenue - foreign_cost) / foreign_revenue

        if dm is not None or fm is not None:
            years_data[year] = {'境内毛利率': dm, '境外毛利率': fm}

    if not years_data:
        return None

    df = pd.DataFrame.from_dict(years_data, orient='index').T
    df = df[sorted(df.columns)]
    df.index.name = '类别'
    return df


# ==================== 数据加载：营业收入与营业成本 ====================
def load_revenue_cost_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """
    读取 "营业收入和营业成本情况" 文件，提取主营业务收入/成本。
    文件结构（每个 sheet 含两年数据）：
      Row 0: ['项目', '本期发生额_收入', '本期发生额_成本', '上期发生额_收入', '上期发生额_成本']
      Row 1: ['主营业务', 本期收入, 本期成本, 上期收入, 上期成本]
      Row 2: ['其他业务', ...]
      Row 3: ['合计', ...]
    本期 = sheet 年份，上期 = sheet 年份 - 1。
    优先使用本期数据；若某年份已存在，跳过上期重复数据。
    返回 DataFrame：行=['营业收入','营业成本']，列=年份，值=元
    """
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None

    years_data = {}

    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        sheet_year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue

        if len(df) == 0 or len(df.columns) < 3:
            continue

        # 定位列索引
        header_vals = [str(v) if pd.notna(v) else '' for v in df.iloc[0]]
        current_rev_col = None
        current_cost_col = None
        prev_rev_col = None
        prev_cost_col = None
        for idx, hv in enumerate(header_vals):
            if '本期' in hv and '收入' in hv:
                current_rev_col = idx
            elif '本期' in hv and '成本' in hv:
                current_cost_col = idx
            elif '上期' in hv and '收入' in hv:
                prev_rev_col = idx
            elif '上期' in hv and '成本' in hv:
                prev_cost_col = idx

        # 如果没找到标准表头，尝试固定列（兼容无表头的情况）
        if current_rev_col is None:
            current_rev_col = 1
        if current_cost_col is None:
            current_cost_col = 2
        if prev_rev_col is None:
            prev_rev_col = 3 if len(df.columns) > 3 else None
        if prev_cost_col is None:
            prev_cost_col = 4 if len(df.columns) > 4 else None

        # 读取主营业务行（仅本期发生额）
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if '主营' in label:
                rev = parse_money(df.iloc[i, current_rev_col])
                cst = parse_money(df.iloc[i, current_cost_col])
                if rev is not None and cst is not None and rev > 0:
                    years_data[sheet_year] = {'营业收入': rev, '营业成本': cst}
                break

    if not years_data:
        return None

    df = pd.DataFrame.from_dict(years_data, orient='index').T
    df = df[sorted(df.columns)]
    df.index.name = '类别'
    return df


# ==================== 数据加载：财务费用（利息收支） ====================
def load_finance_expense_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None

    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue

        interest_expense = None
        interest_income = None

        first_cell = str(df.iloc[0, 0]) if pd.notna(df.iloc[0, 0]) else ''
        if '项目_' in first_cell or ('本期发生额' in first_cell and '项目' in first_cell):
            for i in range(len(df)):
                cell0 = str(df.iloc[i, 0]) if pd.notna(df.iloc[i, 0]) else ''
                if '项目_' in cell0:
                    label = cell0.split('项目_', 1)[1].strip()
                else:
                    label = cell0.strip()
                val = parse_money(df.iloc[i, 1])
                if val is None:
                    continue
                if ('利息支出' in label or '利息费用' in label) and '租赁负债' not in label:
                    interest_expense = abs(val)
                elif '利息收入' in label and '租赁负债' not in label:
                    interest_income = abs(val)
        else:
            for i in range(1, len(df)):
                label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
                if not label:
                    continue
                if label == '合计':
                    break
                val = parse_money(df.iloc[i, 1])
                if val is None:
                    continue
                if ('利息支出' in label or '利息费用' in label) and '租赁负债' not in label:
                    interest_expense = abs(val)
                elif '利息收入' in label and '租赁负债' not in label:
                    interest_income = abs(val)

        if interest_expense is not None or interest_income is not None:
            years_data[year] = {
                '利息支出': interest_expense if interest_expense is not None else 0,
                '利息收入': interest_income if interest_income is not None else 0,
            }

    if not years_data:
        return None

    df = pd.DataFrame.from_dict(years_data, orient='index').T
    df = df[sorted(df.columns)]
    df.index.name = '类别'
    return df


# ==================== 项目名称归一化 ====================
def normalize_expense_label(label: str) -> str:
    """将费用项目名称归一化，统一不同年份的类似表述"""
    label = label.strip()
    if re.search(r'股份支付|股权激励', label):
        return '股份支付'
    if re.search(r'折旧.*摊销|摊销.*折旧|使用权资产折旧|固定资产折旧|无形资产摊销|低值易耗品摊销|折旧费', label):
        return '折旧及摊销'
    if re.search(r'房租|物业|租赁|租金', label):
        return '房租物业费'
    if re.search(r'人工|职工|人员|员工|薪酬|工资', label):
        return '人工成本'
    if re.search(r'市场|推广|广告|宣传|营销|展览|参展', label):
        return '市场推广费'
    if re.search(r'维修|保修|售后|质保|产品质量保证|预计产品质量保证|客户端维护|修理费', label):
        return '维修及售后费'
    if re.search(r'差旅|交通', label):
        return '差旅交通费'
    if re.search(r'业务招待|招待费', label):
        return '业务招待费'
    if re.search(r'咨询|中介', label):
        return '咨询及中介费'
    if re.search(r'销售服务', label):
        return '销售服务费'
    if re.search(r'办公|会务|会议', label):
        return '办公会务费'
    if re.search(r'机物料|物料消耗|低值易耗品|原材料|耗用的原材料', label):
        return '物料消耗'
    if re.search(r'水电|燃料动力', label):
        return '水电费'
    if re.search(r'技术服务', label):
        return '技术服务费'
    if re.search(r'外部服务|外采服务', label):
        return '外部服务费'
    if re.search(r'仓储|物流|运输', label):
        return '物流仓储费'
    if re.search(r'邮电|通讯', label):
        return '邮电通讯费'
    if re.search(r'软件|IT', label):
        return '软件及IT费'
    if re.search(r'车辆', label):
        return '车辆费'
    if re.search(r'保险', label):
        return '保险费'
    if re.search(r'专利', label):
        return '专利费'
    if re.search(r'招聘', label):
        return '招聘费'
    if re.search(r'样品', label):
        return '样品费'
    if re.search(r'装修', label):
        return '装修费'
    if re.search(r'诉讼', label):
        return '诉讼费'
    if re.search(r'佣金', label):
        return '佣金'
    if re.search(r'安全生产', label):
        return '安全生产费'
    if re.search(r'残保金|残疾人就业保障金', label):
        return '残保金'
    if re.search(r'顾问', label):
        return '顾问费'
    if re.search(r'投标|招标', label):
        return '招投标费'
    if re.search(r'特许权使用', label):
        return '特许权使用费'
    if re.search(r'劳保', label):
        return '劳保费'
    if re.search(r'厂务杂费', label):
        return '厂务杂费'
    if re.search(r'存货报废', label):
        return '存货报废'
    if re.search(r'税金|税费', label):
        return '税金'
    if re.search(r'服务费', label):
        return '服务费'
    return label


# ==================== 数据加载：费用分类（前5项） ====================
def load_expense_top5_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None

    all_years_data = {}
    item_totals = {}

    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue

        year_data = {}
        header_detected = False

        for i in range(len(df)):
            cell0 = str(df.iloc[i, 0]) if pd.notna(df.iloc[i, 0]) else ''
            if not cell0 or cell0.strip() == '':
                continue
            if '项目' in cell0:
                header_detected = True
                continue
            if not header_detected:
                continue

            label = cell0.strip()
            if label == '合计':
                break
            if label in ('其他',):
                continue

            val = parse_money(df.iloc[i, 1])
            if val is not None and val != 0:
                norm_label = normalize_expense_label(label)
                year_data[norm_label] = year_data.get(norm_label, 0) + val
                item_totals[norm_label] = item_totals.get(norm_label, 0) + val

        if year_data:
            all_years_data[year] = year_data

    if not all_years_data or not item_totals:
        return None

    top5_items = sorted(item_totals.keys(), key=lambda x: item_totals[x], reverse=True)[:5]

    result = {}
    for year, data in all_years_data.items():
        result[year] = {item: data.get(item, 0) for item in top5_items}

    df = pd.DataFrame.from_dict(result, orient='index').T
    df = df[sorted(df.columns)]
    df.index.name = '项目'
    return df


# ==================== 新增数据加载函数 ====================
def load_revenue_gross_margin_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """基于营业收入和营业成本计算主营毛利率，同时保留收入/成本金额（单位：元）"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        sheet_year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        if len(df) == 0 or len(df.columns) < 3:
            continue
        header_vals = [str(v) if pd.notna(v) else '' for v in df.iloc[0]]
        rev_col = None
        cost_col = None
        for idx, hv in enumerate(header_vals):
            if '本期' in hv and '收入' in hv:
                rev_col = idx
            elif '本期' in hv and '成本' in hv:
                cost_col = idx
        if rev_col is None:
            rev_col = 1
        if cost_col is None:
            cost_col = 2
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if '主营' in label:
                rev = parse_money(df.iloc[i, rev_col])
                cst = parse_money(df.iloc[i, cost_col])
                if rev is not None and cst is not None and rev > 0:
                    years_data[sheet_year] = {
                        '营业收入': rev,
                        '营业成本': cst,
                        '主营毛利率': (rev - cst) / rev,
                    }
                break
    if not years_data:
        return None
    df = pd.DataFrame.from_dict(years_data, orient='index').T
    df = df[sorted(df.columns)]
    return df


def load_impairment_top3_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """资产减值损失前三项本期发生额"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    all_years_data = {}
    all_items = set()
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        year_data = {}
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if not label or '合计' in label:
                continue
            val = parse_money(df.iloc[i, 1])
            if val is not None and val != 0:
                # 简写过长的标签
                short_label = label[:8] + '...' if len(label) > 10 else label
                year_data[short_label] = abs(val)
                all_items.add(short_label)
        if year_data:
            all_years_data[year] = year_data
    if not all_years_data or not all_items:
        return None
    result = {}
    for year, data in all_years_data.items():
        result[year] = {item: data.get(item, 0) for item in all_items}
    df = pd.DataFrame.from_dict(result, orient='index').T.fillna(0)
    df = df[sorted(df.columns)]
    df.index.name = '项目'
    return df


def load_non_operating_income_top3_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """营业外收入前三项本期发生额"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    all_years_data = {}
    all_items = set()
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        year_data = {}
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if not label or '合计' in label or label.startswith('其中：') or label.startswith('非流动资产'):
                continue
            val = parse_money(df.iloc[i, 1])
            if val is not None and val > 0:
                short_label = label[:8] + '...' if len(label) > 10 else label
                year_data[short_label] = val
                all_items.add(short_label)
        if year_data:
            all_years_data[year] = year_data
    if not all_years_data or not all_items:
        return None
    result = {}
    for year, data in all_years_data.items():
        result[year] = {item: data.get(item, 0) for item in all_items}
    df = pd.DataFrame.from_dict(result, orient='index').T.fillna(0)
    df = df[sorted(df.columns)]
    df.index.name = '项目'
    return df


def load_inventory_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """存货分类期末账面余额"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    all_categories = set()
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=0)
        except Exception:
            continue
        # 找到"期末余额_账面余额"列
        val_col = None
        for c in df.columns:
            col_str = str(c)
            if '期末余额' in col_str and '账面余额' in col_str:
                val_col = c
                break
        if val_col is None:
            continue
        year_data = {}
        for _, row in df.iterrows():
            label = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
            if not label or '合计' in label:
                continue
            val = parse_money(row.get(val_col))
            if val is not None and val > 0:
                short_label = label[:6] + '...' if len(label) > 8 else label
                year_data[short_label] = val
                all_categories.add(short_label)
        if year_data:
            years_data[year] = year_data
    if not years_data:
        return None
    result = {}
    for year, data in years_data.items():
        result[year] = {cat: data.get(cat, 0) for cat in sorted(all_categories)}
    df = pd.DataFrame.from_dict(result, orient='index').T
    df = df[sorted(df.columns)]
    df.index.name = '存货类别'
    return df


def load_employee_compensation_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """本期辞退福利 / 应付职工薪酬合计"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        severance = None
        total = None
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if '辞退福利' in label:
                severance = parse_money(df.iloc[i, 2])
            elif label == '合计':
                total = parse_money(df.iloc[i, 2])
        if total is not None and total > 0:
            ratio = (severance / total * 100) if severance is not None else 0
            years_data[year] = ratio
    if not years_data:
        return None
    df = pd.DataFrame({'辞退福利占比': list(years_data.values())}, index=list(years_data.keys())).T
    df = df[sorted(df.columns)]
    return df


def load_fixed_asset_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """固定资产减值准备 / 账面原值"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        original_cost = None
        impairment = None
        current_section = None  # one of: original / depreciation / impairment / book_value
        for i in range(len(df)):
            cell0 = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            normalized_cell0 = re.sub(r'[\s_：:]+', '', cell0)

            # 先按当前章节抓取“期末余额”，避免“2.期末余额_四、账面价值”这类同格拼接被漏读
            if '期末余额' in normalized_cell0:
                last_col = len(df.columns) - 1
                value = parse_money(df.iloc[i, last_col])
                if value is not None:
                    if current_section == 'original' and original_cost is None:
                        original_cost = value
                    elif current_section == 'impairment' and impairment is None:
                        impairment = value

                    if original_cost is not None and impairment is not None:
                        break

            if '一、账面原值' in normalized_cell0:
                current_section = 'original'
                continue
            if '二、累计折旧' in normalized_cell0:
                current_section = 'depreciation'
                continue
            if '三、减值准备' in normalized_cell0:
                current_section = 'impairment'
                continue
            if '四、账面价值' in normalized_cell0:
                current_section = 'book_value'
                # 进入下一节后，若减值值已取到即可提前结束
                if impairment is not None:
                    break
                continue
        if original_cost is not None and original_cost > 0:
            ratio = (impairment / original_cost * 100) if impairment is not None else 0
            years_data[year] = ratio
    if not years_data:
        return None
    df = pd.DataFrame({'减值准备占比': list(years_data.values())}, index=list(years_data.keys())).T
    df = df[sorted(df.columns)]
    return df


def load_ip_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """发明专利/合计（累计获得数）"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        invention = None
        total = None
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if label == '发明专利':
                invention = parse_money(df.iloc[i, 4])
            elif label == '合计':
                total = parse_money(df.iloc[i, 4])
        if invention is not None and total is not None and total > 0:
            years_data[year] = {'发明专利': invention, '合计': total}
    if not years_data:
        return None
    df = pd.DataFrame.from_dict(years_data, orient='index').T
    df = df[sorted(df.columns)]
    return df


def load_rnd_projects_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """在研项目数量及投资金额（本期投入金额合计）"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        count = max(0, len(df) - 1)
        total_investment = 0
        for i in range(1, len(df)):
            val = parse_money(df.iloc[i, 3])
            if val is not None:
                total_investment += val
        years_data[year] = {'项目数量': count, '投资金额': total_investment}
    if not years_data:
        return None
    df = pd.DataFrame.from_dict(years_data, orient='index').T
    df = df[sorted(df.columns)]
    return df


def load_customer_concentration_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """客户集中度（前五大客户销售占比）"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        ratio = None
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if label == '合计':
                ratio = parse_percent(df.iloc[i, 3])
                if ratio is None:
                    ratio = parse_money(df.iloc[i, 3])
                    if ratio is not None and ratio > 1:
                        ratio = ratio / 100
                break
        if ratio is not None:
            # ratio 此时是分数形式（如 0.1591 = 15.91%）
            # 如果结果异常大（>1），说明原始数据被错误放大，尝试修正
            if ratio > 1:
                money_val = parse_money(df.iloc[i, 3])
                if money_val is not None:
                    if money_val > 10000:
                        ratio = money_val / 10000 / 100
                    elif money_val > 100:
                        ratio = money_val / 100 / 100
            years_data[year] = ratio * 100  # 转为百分比数值（如 15.91）供图表显示
    if not years_data:
        return None
    df = pd.DataFrame({'客户集中度': list(years_data.values())}, index=list(years_data.keys())).T
    df = df[sorted(df.columns)]
    return df


def load_supplier_concentration_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """供应商集中度（前五大供应商采购占比）"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    years_data = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        ratio = None
        for i in range(1, len(df)):
            label = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ''
            if label == '合计':
                ratio = parse_percent(df.iloc[i, 3])
                if ratio is None:
                    ratio = parse_money(df.iloc[i, 3])
                    if ratio is not None and ratio > 1:
                        ratio = ratio / 100
                break
        if ratio is not None:
            # ratio 此时是分数形式（如 0.1591 = 15.91%）
            # 如果结果异常大（>1），说明原始数据被错误放大，尝试修正
            if ratio > 1:
                money_val = parse_money(df.iloc[i, 3])
                if money_val is not None:
                    if money_val > 10000:
                        ratio = money_val / 10000 / 100
                    elif money_val > 100:
                        ratio = money_val / 100 / 100
            years_data[year] = ratio * 100  # 转为百分比数值（如 15.91）供图表显示
    if not years_data:
        return None
    df = pd.DataFrame({'供应商集中度': list(years_data.values())}, index=list(years_data.keys())).T
    df = df[sorted(df.columns)]
    return df


# ==================== LLM 语义分析数据加载 ====================

def load_llm_competitiveness_summary(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """读取 LLM 核心竞争力分析，返回最新年份的精简摘要"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None

    # 只取最新年份
    target_year = None
    for sheet_name in xl.sheet_names:
        if '核心竞争力' not in sheet_name:
            continue
        year_match = re.search(r'(\d{4})', sheet_name)
        if year_match:
            y = int(year_match.group(1))
            if target_year is None or y > target_year:
                target_year = y

    if target_year is None:
        return None

    rows = []
    for sheet_name in xl.sheet_names:
        if '核心竞争力' not in sheet_name:
            continue
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match or int(year_match.group(1)) != target_year:
            continue
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name)
        except Exception:
            continue
        for _, row in df.iterrows():
            dim = str(row.get('竞争维度', '')).strip()
            adv = str(row.get('核心优势', '')).strip()
            if not dim:
                continue
            adv_short = adv[:55] + '...' if len(adv) > 55 else adv
            rows.append({'年份': str(target_year), '竞争维度': dim, '核心优势': adv_short})
    if not rows:
        return None
    return pd.DataFrame(rows)


def load_llm_business_summary(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """读取 LLM 经营情况分析，返回最新年份的业务板块摘要"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None

    # 只取最新年份
    target_year = None
    for sheet_name in xl.sheet_names:
        if '经营情况' not in sheet_name:
            continue
        year_match = re.search(r'(\d{4})', sheet_name)
        if year_match:
            y = int(year_match.group(1))
            if target_year is None or y > target_year:
                target_year = y

    if target_year is None:
        return None

    rows = []
    for sheet_name in xl.sheet_names:
        if '经营情况' not in sheet_name:
            continue
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match or int(year_match.group(1)) != target_year:
            continue
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name)
        except Exception:
            continue
        for _, row in df.iterrows():
            biz = str(row.get('业务板块', '')).strip()
            goal = str(row.get('战略目标', '')).strip()
            if not biz or biz in ['研发', '销售', '市场营销', '生产', '财务']:
                continue
            goal_short = goal[:45] + '...' if len(goal) > 45 else goal
            rows.append({'年份': str(target_year), '业务板块': biz, '战略目标': goal_short})
    if not rows:
        return None
    return pd.DataFrame(rows)


def plot_portrait_trend_header(portrait_summary_items: list, stock_name: str, stock_code: str):
    """
    绘制 Portrait 财务趋势分析头部图
    5 个维度卡片式横向排列 - 优化版
    """
    import textwrap
    
    if not portrait_summary_items:
        return Image.new('RGB', (1, 1), 'white')

    # 配色：5 个维度各一种颜色
    dim_colors = {
        '营收与盈利': '#1565C0',
        '费用结构': '#6A1B9A',
        '资产质量': '#C62828',
        '研发创新': '#2E7D32',
        '供应链风险': '#E65100',
    }
    dim_bg_colors = {
        '营收与盈利': '#E3F2FD',
        '费用结构': '#F3E5F5',
        '资产质量': '#FFEBEE',
        '研发创新': '#E8F5E9',
        '供应链风险': '#FFF3E0',
    }

    # 增加画布高度，避免重叠
    fig_height = 5.2
    fig, ax = plt.subplots(figsize=(14, fig_height))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, fig_height)
    ax.axis('off')

    # 标题区域（顶部，不占卡片空间）
    title_kwargs = {'fontproperties': font_sans} if font_sans else {}
    ax.text(7, fig_height - 0.3, f'{stock_code} {stock_name}',
            ha='center', va='top', fontsize=20, fontweight='bold',
            color='#1A1A1A', **title_kwargs)
    ax.text(7, fig_height - 0.75, '三年财务趋势摘要 · LLM智能分析',
            ha='center', va='top', fontsize=12, fontweight='normal',
            color='#666666', **title_kwargs)

    # 卡片区域（标题下方）
    n_items = len(portrait_summary_items)
    card_width = 13.2 / n_items
    gap = 0.15
    card_height = 3.6
    y_start = 0.25  # 卡片起始位置

    for i, item in enumerate(portrait_summary_items):
        dim = item.get('维度', '')
        trend = item.get('三年趋势', '')
        change = item.get('关键变化', '')
        risk = item.get('风险提示', '')
        conclusion = item.get('结论', '')

        color = dim_colors.get(dim, '#555555')
        bg_color = dim_bg_colors.get(dim, '#F5F5F5')

        x0 = 0.4 + i * (card_width + gap)
        y0 = y_start
        cw = card_width - gap
        ch = card_height

        # 卡片背景（圆角效果）
        rect = plt.Rectangle((x0, y0), cw, ch, facecolor=bg_color,
                              edgecolor=color, linewidth=2.5, 
                              joinstyle='round', zorder=1)
        ax.add_patch(rect)

        # 顶部色条
        bar_height = 0.45
        bar = plt.Rectangle((x0, y0 + ch - bar_height), cw, bar_height, 
                            facecolor=color, zorder=2)
        ax.add_patch(bar)

        # 维度名称（白色，在色条上）
        ax.text(x0 + cw / 2, y0 + ch - bar_height/2, dim, 
                ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', 
                **title_kwargs)

        # 内容区域起始位置
        content_y = y0 + ch - bar_height - 0.25
        line_height = 0.38
        
        # 三年趋势（彩色标签）
        trend_color = '#2E7D32' if '增长' in trend or '升' in trend else '#C62828' if '降' in trend else '#555555'
        ax.text(x0 + 0.12, content_y, f'趋势: {trend}', 
                ha='left', va='top',
                fontsize=9, color=trend_color, fontweight='bold', 
                **title_kwargs)
        
        # 关键变化（自动换行）
        content_y -= line_height
        max_chars = int(cw * 8)  # 根据卡片宽度计算最大字符数
        change_text = change[:80] + '...' if len(change) > 80 else change
        wrapped_lines = textwrap.wrap(change_text, width=max_chars//2)
        n_lines = min(len(wrapped_lines), 2)  # 实际显示行数
        for j, line in enumerate(wrapped_lines[:2]):  # 最多显示2行
            ax.text(x0 + 0.12, content_y - j*0.32, line, 
                    ha='left', va='top',
                    fontsize=8, color='#333333', 
                    **title_kwargs)
        content_y -= (n_lines - 1) * 0.32 + 0.45  # 更新 content_y，为下一项留出空间
        
        # 风险提示（如果有）
        if risk and risk != '无':
            risk_text = f'风险: {risk[:30]}' if len(risk) > 30 else f'风险: {risk}'
            ax.text(x0 + 0.12, content_y, risk_text, 
                    ha='left', va='top',
                    fontsize=8, color='#D32F2F', 
                    **title_kwargs)
            content_y -= 0.5  # 更新 content_y
        
        # 结论（底部，加粗，带背景）
        concl_text = conclusion[:35] + '...' if len(conclusion) > 35 else conclusion
        ax.text(x0 + cw / 2, y0 + 0.35, concl_text, 
                ha='center', va='center',
                fontsize=9, color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor=color, linewidth=1.5, alpha=0.9),
                **title_kwargs)

    plt.tight_layout(pad=0.3)

    tmp = f'/tmp/portrait_header_{stock_code}.png'
    fig.savefig(tmp, dpi=300, bbox_inches='tight',
                facecolor='#FAFAFA', edgecolor='none')
    plt.close(fig)

    return Image.open(tmp)


def plot_llm_summary_figure(comp_df: pd.DataFrame, biz_df: pd.DataFrame,
                            stock_name: str, stock_code: str) -> 'PIL.Image.Image':
    """生成 LLM 语义分析摘要图，双栏文本布局，返回 PIL Image"""
    n_biz = len(biz_df) if biz_df is not None else 0
    n_comp = len(comp_df) if comp_df is not None else 0
    max_items = max(n_biz, n_comp)
    # 每行约 0.55 英寸，标题占 1.2 英寸
    height = max(5, max_items * 0.55 + 1.7)

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, height))

    fig.patch.set_facecolor('#FAFAFA')
    ax_left.set_facecolor('#F0F7FF')
    ax_right.set_facecolor('#F0FFF4')

    for ax in [ax_left, ax_right]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    fig.suptitle(f'{stock_code} {stock_name}  |  LLM 语义分析摘要',
                 fontsize=20, fontweight='bold', color='#1565C0', y=0.98)

    # ---- 左栏：经营战略 ----
    ax_left.text(0.5, 0.96, '经营战略',
                 transform=ax_left.transAxes,
                 fontsize=16, fontweight='bold', ha='center', va='top',
                 color='white',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#1565C0',
                          edgecolor='#0D47A1', linewidth=2))

    y = 0.88
    step = 0.13

    if biz_df is not None and not biz_df.empty:
        for _, row in biz_df.iterrows():
            biz = row['业务板块']
            goal = row['战略目标'][:80] + ('…' if len(row['战略目标']) > 80 else '')
            ax_left.text(0.06, y, f'● {biz}',
                        transform=ax_left.transAxes,
                        fontsize=13, fontweight='bold', va='top', color='#0D47A1')
            ax_left.text(0.10, y - 0.035, goal,
                        transform=ax_left.transAxes,
                        fontsize=11, va='top', color='#333333',
                        linespacing=1.4)
            y -= step
    else:
        ax_left.text(0.5, 0.5, '暂无经营战略数据', transform=ax_left.transAxes,
                     fontsize=12, ha='center', va='center', color='#999999')

    # ---- 右栏：科研成果与核心优势 ----
    ax_right.text(0.5, 0.96, '科研成果与核心优势',
                  transform=ax_right.transAxes,
                  fontsize=16, fontweight='bold', ha='center', va='top',
                  color='white',
                  bbox=dict(boxstyle='round,pad=0.35', facecolor='#2E7D32',
                           edgecolor='#1B5E20', linewidth=2))

    y = 0.88
    if comp_df is not None and not comp_df.empty:
        for _, row in comp_df.iterrows():
            dim = row['竞争维度']
            adv = row['核心优势'][:100] + ('…' if len(row['核心优势']) > 100 else '')
            ax_right.text(0.06, y, f'● {dim}',
                         transform=ax_right.transAxes,
                         fontsize=13, fontweight='bold', va='top', color='#1B5E20')
            ax_right.text(0.10, y - 0.035, adv,
                         transform=ax_right.transAxes,
                         fontsize=11, va='top', color='#333333',
                         linespacing=1.4)
            y -= step
    else:
        ax_right.text(0.5, 0.5, '暂无核心竞争力数据', transform=ax_right.transAxes,
                      fontsize=12, ha='center', va='center', color='#999999')

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.94])
    fig.savefig('/tmp/_llm_tmp.png', dpi=300, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    from PIL import Image
    return Image.open('/tmp/_llm_tmp.png')


def normalize_rd_expense_label(label: str) -> str:
    """研发费用项目归一化"""
    label = label.strip()
    if re.search(r'股份支付', label):
        return '股份支付'
    if re.search(r'折旧.*摊销|摊销.*折旧|使用权资产折旧|固定资产折旧|无形资产摊销|低值易耗品摊销|折旧费', label):
        return '折旧及摊销'
    if re.search(r'人工|职工|人员|员工|薪酬|工资', label):
        return '人工成本'
    if re.search(r'机物料|物料消耗|低值易耗品|原材料', label):
        return '物料消耗'
    if re.search(r'差旅|交通', label):
        return '差旅费'
    if re.search(r'咨询|中介', label):
        return '咨询费'
    if re.search(r'技术服务', label):
        return '技术服务费'
    if re.search(r'测试|化验|加工', label):
        return '测试化验加工费'
    if re.search(r'房租|物业|租赁|租金', label):
        return '房租物业费'
    if re.search(r'燃料|动力|水电', label):
        return '燃料动力费'
    if re.search(r'办公|会务|会议', label):
        return '办公费'
    if re.search(r'软件|IT', label):
        return '软件及IT费'
    return label


def load_rd_expense_top5_data(xlsx_path: Path) -> Optional[pd.DataFrame]:
    """研发费用前5项"""
    if not xlsx_path or not xlsx_path.exists():
        return None
    try:
        xl = pd.ExcelFile(xlsx_path)
    except Exception:
        return None
    all_years_data = {}
    item_totals = {}
    for sheet_name in xl.sheet_names:
        year_match = re.search(r'(\d{4})', sheet_name)
        if not year_match:
            continue
        year = int(year_match.group(1))
        try:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        except Exception:
            continue
        year_data = {}
        first_cell = str(df.iloc[0, 0]) if pd.notna(df.iloc[0, 0]) else ''
        malformed = '项目_' in first_cell
        for i in range(len(df)):
            cell0 = str(df.iloc[i, 0]) if pd.notna(df.iloc[i, 0]) else ''
            if malformed and '项目_' in cell0:
                label = cell0.split('项目_', 1)[1].strip()
                val = parse_money(df.iloc[i, 1])
            elif malformed:
                label = cell0.strip()
                val = parse_money(df.iloc[i, 1])
            else:
                if i == 0 or '项目' in cell0:
                    continue
                label = cell0.strip()
                val = parse_money(df.iloc[i, 1])
            if not label or label in ('合计', '其他'):
                continue
            if val is not None and val != 0:
                norm_label = normalize_rd_expense_label(label)
                year_data[norm_label] = year_data.get(norm_label, 0) + val
                item_totals[norm_label] = item_totals.get(norm_label, 0) + val
        if year_data:
            all_years_data[year] = year_data
    if not all_years_data or not item_totals:
        return None
    top5_items = sorted(item_totals.keys(), key=lambda x: item_totals[x], reverse=True)[:5]
    result = {}
    for year, data in all_years_data.items():
        result[year] = {item: data.get(item, 0) for item in top5_items}
    df = pd.DataFrame.from_dict(result, orient='index').T
    df = df[sorted(df.columns)]
    df.index.name = '项目'
    return df


# ==================== 绘图函数 ====================
def setup_chart_style(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLOR_AXIS)
    ax.spines['bottom'].set_color(COLOR_AXIS)
    ax.spines['left'].set_linewidth(0.75)
    ax.spines['bottom'].set_linewidth(0.75)
    ax.tick_params(axis='both', which='both', length=0)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=COLOR_AXIS)


def plot_aging_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """按账龄披露的应收账款期末账面余额"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无账龄披露数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n按账龄披露的应收账款期末账面余额', fontsize=14, fontweight="bold")
        ax.axis('off')
        return

    df_plot = df / 1e8
    years = df_plot.columns.tolist()
    x = np.arange(len(df_plot.index))
    width = 0.8 / len(years) if years else 0.4

    for i, year in enumerate(years):
        offset = width * (i - (len(years) - 1) / 2)
        color = COLORS_BAR[i % len(COLORS_BAR)]
        bars = ax.bar(
            x + offset,
            df_plot[year].fillna(0),
            width,
            label=f'{year}年',
            color=color,
            edgecolor='white',
            linewidth=0.5
        )
        for bar, val in zip(bars, df_plot[year]):
            if pd.notna(val) and val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f'{val:.2f}',
                    ha='center', va='bottom', fontsize=6, color=COLOR_TEXT
                )

    ax.set_xticks(x)
    ax.set_xticklabels(df_plot.index, rotation=30, ha='right', fontsize=8)
    ax.set_ylabel('期末账面余额（亿元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n按账龄披露的应收账款期末账面余额', fontsize=14, fontweight="bold", pad=20)
    ax.legend(
        title='年份', title_fontsize=7, fontsize=7,
        loc='upper center', bbox_to_anchor=(0.5, 1.06),
        ncol=min(len(years), 4), frameon=False
    )
    setup_chart_style(ax)


def plot_margin_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """境内外毛利率对比"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无境内外毛利率数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n境内外毛利率对比', fontsize=14, fontweight="bold")
        ax.axis('off')
        return

    years = df.columns.tolist()
    categories = df.index.tolist()
    x = np.arange(len(years))
    width = 0.35

    colors = [COLORS_BAR[0], COLORS_LINE[2]]

    for i, cat in enumerate(categories):
        vals = df.loc[cat].values
        vals_display = [v * 100 if pd.notna(v) else 0 for v in vals]
        bars = ax.bar(
            x + (i - (len(categories) - 1) / 2) * width,
            vals_display,
            width,
            label=cat,
            color=colors[i % len(colors)],
            edgecolor='white',
            linewidth=0.5
        )
        for bar, val in zip(bars, vals):
            if pd.notna(val):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f'{val*100:.1f}%',
                    ha='center', va='bottom', fontsize=7, color=COLOR_TEXT
                )

    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('毛利率', fontsize=9)
    ax.set_ylim(0, min(100, ax.get_ylim()[1] * 1.15))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))
    ax.set_title(f'{stock_code} {stock_name}\n境内外毛利率对比', fontsize=14, fontweight="bold", pad=20)
    ax.legend(
        title='', fontsize=8,
        loc='upper center', bbox_to_anchor=(0.5, 1.06),
        ncol=len(categories), frameon=False
    )
    setup_chart_style(ax)


def plot_revenue_cost_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """营业收入与营业成本正负堆积柱状图
    营业收入在0轴上方（正值），营业成本在0轴下方（负值），
    0轴用深红色粗线标识为'重叠处'
    """
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n营业收入与营业成本', fontsize=14, fontweight="bold")
        ax.axis('off')
        return

    years = df.columns.tolist()
    revenue = df.loc['营业收入'].values
    cost = df.loc['营业成本'].values

    revenue_yi = revenue / 1e8
    cost_yi = cost / 1e8

    x = np.arange(len(years))
    width = 0.5

    # 营业成本：负值（0轴下方）
    ax.bar(
        x, -cost_yi, width,
        label='营业成本',
        color=COLORS_BAR[1],
        edgecolor='white',
        linewidth=0.5
    )
    # 营业收入：正值（0轴上方）
    ax.bar(
        x, revenue_yi, width,
        label='营业收入',
        color=COLORS_BAR[0],
        edgecolor='white',
        linewidth=0.5
    )

    # 0轴重叠处：深红色粗线
    ax.axhline(0, color='#920000', linewidth=2.5, zorder=5)

    for i, (rev, cst) in enumerate(zip(revenue_yi, cost_yi)):
        # 营业收入标注（正半轴顶部）
        ax.text(
            x[i], rev,
            f'{rev:.2f}',
            ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold'
        )
        # 营业成本标注（负半轴底部，显示为正数）
        ax.text(
            x[i], -cst,
            f'{cst:.2f}',
            ha='center', va='top', fontsize=8, color=COLOR_TEXT, fontweight='bold'
        )
        # 毛利标注（放在正半轴内部偏下位置）
        gross = rev - cst
        ax.text(
            x[i], rev * 0.15,
            f'毛利 {gross:.2f}',
            ha='center', va='center', fontsize=7, color='white', fontweight='bold'
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('金额（亿元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n营业收入与营业成本', fontsize=14, fontweight="bold", pad=20)
    ax.legend(
        title='', fontsize=8,
        loc='upper center', bbox_to_anchor=(0.5, 1.06),
        ncol=2, frameon=False
    )
    setup_chart_style(ax)
    ymax = max(ax.get_ylim()[1], max(revenue_yi) * 1.15)
    ymin = min(ax.get_ylim()[0], -max(cost_yi) * 1.15)
    ax.set_ylim(ymin, ymax)


def plot_finance_expense_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """财务费用（利息收支）分组柱状图
    利息支出为正值（向上），利息收入为负值（向下），直观显示净财务费用
    """
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n财务费用（利息收支）', fontsize=14, fontweight="bold")
        ax.axis('off')
        return

    years = df.columns.tolist()
    expense = df.loc['利息支出'].values
    income = df.loc['利息收入'].values

    # 利息收入始终显示为负值（向下）
    expense_wan = expense / 1e4
    income_wan = -np.abs(income) / 1e4

    x = np.arange(len(years))
    width = 0.35

    bars_exp = ax.bar(
        x - width / 2, expense_wan, width,
        label='利息支出',
        color=COLORS_BAR[0],
        edgecolor='white',
        linewidth=0.5
    )
    bars_inc = ax.bar(
        x + width / 2, income_wan, width,
        label='利息收入',
        color=COLORS_BAR[1],
        edgecolor='white',
        linewidth=0.5
    )

    # 0轴标识线
    ax.axhline(0, color='#920000', linewidth=1.5, zorder=5)

    for bar, val in zip(bars_exp, expense_wan):
        if val != 0:
            ax.text(bar.get_x() + bar.get_width() / 2, val, f'{val:.0f}',
                    ha='center', va='bottom', fontsize=7, color=COLOR_TEXT)
    for bar, val in zip(bars_inc, income_wan):
        if val != 0:
            ax.text(bar.get_x() + bar.get_width() / 2, val, f'{abs(val):.0f}',
                    ha='center', va='top', fontsize=7, color=COLOR_TEXT)

    # 标注净利息费用（放在利息支出柱体内部偏下，仅在支出不为0时显示）
    for i in range(len(years)):
        net = expense_wan[i] + income_wan[i]
        if expense_wan[i] != 0:
            ax.text(
                x[i] - width / 2, expense_wan[i] * 0.15,
                f'净额 {net:.0f}',
                ha='center', va='center', fontsize=7, color='white', fontweight='bold'
            )

    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('金额（万元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n财务费用（利息收支）', fontsize=14, fontweight="bold", pad=20)
    ax.legend(
        title='', fontsize=8,
        loc='upper center', bbox_to_anchor=(0.5, 1.06),
        ncol=2, frameon=False
    )
    setup_chart_style(ax)
    ymax = max(ax.get_ylim()[1], max(expense_wan) * 1.15) if len(expense_wan) > 0 else ax.get_ylim()[1]
    ymin = min(ax.get_ylim()[0], min(income_wan) * 1.15) if len(income_wan) > 0 else ax.get_ylim()[0]
    ax.set_ylim(ymin, ymax)


def plot_expense_stacked_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str, title: str):
    """费用分类堆积柱状图（前5项）"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n{title}', fontsize=14, fontweight="bold")
        ax.axis('off')
        return

    years = df.columns.tolist()
    items = df.index.tolist()

    x = np.arange(len(years))
    width = 0.5

    bottom = np.zeros(len(years))
    colors = [COLORS_BAR[i % len(COLORS_BAR)] for i in range(len(items))]

    for idx, item in enumerate(items):
        vals = df.loc[item].values / 1e4
        ax.bar(
            x, vals, width,
            bottom=bottom,
            label=item,
            color=colors[idx],
            edgecolor='white',
            linewidth=0.5
        )
        bottom += vals

    for i, total in enumerate(bottom):
        ax.text(
            x[i], total,
            f'{total:.0f}',
            ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold'
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('金额（万元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n{title}（前5项）', fontsize=14, fontweight="bold", pad=20)
    ax.legend(
        title='', fontsize=7,
        loc='upper center', bbox_to_anchor=(0.5, 1.06),
        ncol=min(len(items), 3), frameon=False
    )
    setup_chart_style(ax)
    ymax = ax.get_ylim()[1]
    ax.set_ylim(0, ymax * 1.1)


# ==================== 新增绘图函数 ====================
def plot_revenue_gross_margin_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """主营毛利率柱状图"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n主营毛利率', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    x = np.arange(len(years))

    # 兼容旧格式（仅毛利率）
    if '营业收入' not in df.index or '营业成本' not in df.index:
        vals = df.loc['主营毛利率'].values * 100
        bars = ax.bar(x, vals, 0.5, color=COLORS_BAR[0], edgecolor='white', linewidth=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{val:.1f}%',
                    ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
        ax.set_ylabel('毛利率', fontsize=9)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))
        setup_chart_style(ax)
        ax.set_ylim(0, max(vals) * 1.2 if len(vals) > 0 else 1)
        ax.set_title(f'{stock_code} {stock_name}\n主营毛利率', fontsize=14, fontweight="bold", pad=20)
        return

    # 新格式：堆积柱状图（成本+毛利）+ 毛利率折线（双Y轴）
    revenue = df.loc['营业收入'].values / 1e8
    cost = df.loc['营业成本'].values / 1e8
    margin = df.loc['主营毛利率'].values * 100
    profit = revenue - cost

    ax2 = ax.twinx()
    ax2.spines['top'].set_visible(False)

    # 堆积柱状图：成本（浅蓝）+ 毛利（深蓝）
    ax.bar(x, cost, 0.5, label='营业成本', color=COLORS_BAR[1],
           edgecolor='white', linewidth=0.5)
    bars_profit = ax.bar(x, profit, 0.5, bottom=cost, label='毛利', color=COLORS_BAR[0],
                         edgecolor='white', linewidth=0.5)

    # 柱顶标注总收入（亿元）
    for i, (bar, total) in enumerate(zip(bars_profit, revenue)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + cost[i],
                f'{total:.1f}', ha='center', va='bottom', fontsize=7,
                color=COLOR_TEXT, fontweight='bold')

    # 右轴折线：毛利率
    ax2.plot(x, margin, color=COLORS_LINE[2], marker='o', linewidth=2, label='毛利率', zorder=5)
    for i, val in enumerate(margin):
        ax2.text(x[i], val, f'{val:.1f}%', ha='center', va='bottom', fontsize=7,
                 color=COLOR_TEXT, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('金额（亿元）', fontsize=9)
    ax2.set_ylabel('毛利率', fontsize=9)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

    # 合并图例
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc='upper center',
              bbox_to_anchor=(0.5, 1.10), ncol=3, frameon=False)

    ax.set_title(f'{stock_code} {stock_name}\n主营毛利率', fontsize=14, fontweight="bold", pad=20)
    setup_chart_style(ax)
    ax.set_ylim(0, max(revenue) * 1.25 if len(revenue) > 0 else 1)
    ax2.set_ylim(0, max(margin) * 1.25 if len(margin) > 0 else 1)


def plot_margin_line_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """境内外毛利率折线图"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无境内外毛利率数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n境内外毛利率对比', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    categories = df.index.tolist()
    colors = [COLORS_BAR[0], COLORS_LINE[2]]
    for i, cat in enumerate(categories):
        vals = pd.to_numeric(df.loc[cat], errors='coerce').values * 100
        ax.plot(years, vals, marker='o', color=colors[i % len(colors)], linewidth=2, label=cat)
        for j, val in enumerate(vals):
            if pd.notna(val):
                ax.text(years[j], val, f'{val:.1f}%', ha='center', va='bottom', fontsize=7, color=COLOR_TEXT)
    ax.set_xticks(years)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('毛利率', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n境内外毛利率对比', fontsize=14, fontweight="bold", pad=20)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))
    ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=len(categories), frameon=False)
    setup_chart_style(ax)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.15)


def plot_impairment_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """资产减值损失前三项"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n资产减值损失前三项', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    x = np.arange(len(years))
    width = 0.22
    rank_labels = ['Top1', 'Top2', 'Top3']
    rank_values = {idx: [] for idx in range(3)}
    top_items_by_year = []

    for year in years:
        s = pd.to_numeric(df[year], errors='coerce').fillna(0)
        top3 = s[s > 0].sort_values(ascending=False).head(3)
        top_items_by_year.append(top3.index.tolist())
        values = top3.values.tolist()
        while len(values) < 3:
            values.append(0)
        for idx in range(3):
            rank_values[idx].append(values[idx] / 1e4)

    for idx in range(3):
        offset = width * (idx - 1)
        bars = ax.bar(
            x + offset,
            rank_values[idx],
            width,
            label=rank_labels[idx],
            color=COLORS_BAR[idx % len(COLORS_BAR)],
            edgecolor='white',
            linewidth=0.5,
        )
        for bar, val in zip(bars, rank_values[idx]):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f'{val:.0f}',
                    ha='center',
                    va='bottom',
                    fontsize=6,
                    color=COLOR_TEXT,
                )

    xticklabels = []
    for year, items in zip(years, top_items_by_year):
        padded = items + ['无'] * (3 - len(items))
        xticklabels.append(
            f'{year}年\n1.{padded[0]}\n2.{padded[1]}\n3.{padded[2]}'
        )

    ax.set_xticks(x)
    ax.set_xticklabels(xticklabels, fontsize=8)
    ax.set_ylabel('金额（万元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n资产减值损失前三项', fontsize=14, fontweight="bold", pad=20)
    ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=3, frameon=False)
    setup_chart_style(ax)


def plot_non_operating_income_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """营业外收入前三项"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n营业外收入前三项', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    x = np.arange(len(years))
    width = 0.22
    rank_labels = ['Top1', 'Top2', 'Top3']
    rank_values = {idx: [] for idx in range(3)}
    top_items_by_year = []

    for year in years:
        s = pd.to_numeric(df[year], errors='coerce').fillna(0)
        top3 = s[s > 0].sort_values(ascending=False).head(3)
        top_items_by_year.append(top3.index.tolist())
        values = top3.values.tolist()
        while len(values) < 3:
            values.append(0)
        for idx in range(3):
            rank_values[idx].append(values[idx] / 1e4)

    for idx in range(3):
        offset = width * (idx - 1)
        bars = ax.bar(
            x + offset,
            rank_values[idx],
            width,
            label=rank_labels[idx],
            color=COLORS_BAR[idx % len(COLORS_BAR)],
            edgecolor='white',
            linewidth=0.5,
        )
        for bar, val in zip(bars, rank_values[idx]):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f'{val:.0f}',
                    ha='center',
                    va='bottom',
                    fontsize=6,
                    color=COLOR_TEXT,
                )

    xticklabels = []
    for year, items in zip(years, top_items_by_year):
        padded = items + ['无'] * (3 - len(items))
        xticklabels.append(
            f'{year}年\n1.{padded[0]}\n2.{padded[1]}\n3.{padded[2]}'
        )

    ax.set_xticks(x)
    ax.set_xticklabels(xticklabels, fontsize=8)
    ax.set_ylabel('金额（万元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n营业外收入前三项', fontsize=14, fontweight="bold", pad=20)
    ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=3, frameon=False)
    setup_chart_style(ax)


def plot_inventory_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """存货分类堆积柱状图"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n存货分类', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    items = df.index.tolist()
    x = np.arange(len(years))
    width = 0.5
    bottom = np.zeros(len(years))
    colors = [COLORS_BAR[i % len(COLORS_BAR)] for i in range(len(items))]
    for idx, item in enumerate(items):
        vals = df.loc[item].values / 1e8
        ax.bar(x, vals, width, bottom=bottom, label=item, color=colors[idx], edgecolor='white', linewidth=0.5)
        bottom += vals
    for i, total in enumerate(bottom):
        ax.text(x[i], total, f'{total:.2f}', ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('金额（亿元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n存货分类', fontsize=14, fontweight="bold", pad=20)
    ax.legend(fontsize=6, loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=min(len(items), 4), frameon=False)
    setup_chart_style(ax)
    ymax = ax.get_ylim()[1]
    ax.set_ylim(0, ymax * 1.1)


def plot_employee_comp_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """辞退福利占比"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n辞退福利占比', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    vals = df.loc['辞退福利占比'].values
    x = np.arange(len(years))
    bars = ax.bar(x, vals, 0.5, color=COLORS_BAR[0], edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{val:.2f}%',
                ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('占比（%）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n辞退福利/应付职工薪酬合计', fontsize=14, fontweight="bold", pad=20)
    setup_chart_style(ax)
    ax.set_ylim(0, max(vals) * 1.2 if len(vals) > 0 else 1)


def plot_fixed_asset_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """固定资产减值准备占比"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n固定资产减值准备占比', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    vals = df.loc['减值准备占比'].values
    if len(vals) == 0 or np.all(np.isclose(vals, 0)):
        ax.text(0.5, 0.5, '无固定资产减值准备/账面原值', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n固定资产减值准备/账面原值', fontsize=14, fontweight="bold", pad=20)
        ax.axis('off')
        return
    x = np.arange(len(years))
    bars = ax.bar(x, vals, 0.5, color=COLORS_BAR[0], edgecolor='white', linewidth=0.5)

    def fmt_pct(v: float) -> str:
        if abs(v) >= 0.01:
            return f'{v:.2f}%'
        if abs(v) >= 0.0001:
            return f'{v:.4f}%'
        return f'{v:.6f}%'

    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), fmt_pct(val),
                ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('占比（%）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n固定资产减值准备/账面原值', fontsize=14, fontweight="bold", pad=20)
    setup_chart_style(ax)
    ymax = max(vals) if len(vals) > 0 else 0
    ax.set_ylim(0, ymax * 1.2 if ymax > 0 else 1)


def plot_ip_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """发明专利/合计"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n发明专利/合计', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    categories = df.index.tolist()
    x = np.arange(len(years))
    width = 0.35
    colors = [COLORS_BAR[0], COLORS_BAR[1]]
    for i, cat in enumerate(categories):
        vals = df.loc[cat].values
        bars = ax.bar(x + (i - (len(categories) - 1) / 2) * width, vals, width,
                      label=cat, color=colors[i % len(colors)], edgecolor='white', linewidth=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(val)}',
                    ha='center', va='bottom', fontsize=7, color=COLOR_TEXT)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('数量（个）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n发明专利/合计（累计获得数）', fontsize=14, fontweight="bold", pad=20)
    ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=len(categories), frameon=False)
    setup_chart_style(ax)


def plot_rnd_projects_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """在研项目数量及投资金额"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n在研项目数量及投资金额', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    project_counts = df.loc['项目数量'].values
    investments = df.loc['投资金额'].values / 1e8
    x = np.arange(len(years))
    width = 0.35
    ax2 = ax.twinx()
    ax2.spines['top'].set_visible(False)
    bars = ax.bar(x - width / 2, project_counts, width, label='项目数量', color=COLORS_BAR[0],
                  edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, project_counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(val)}',
                ha='center', va='bottom', fontsize=8, color=COLOR_TEXT)
    line = ax2.plot(x + width / 2, investments, color=COLORS_LINE[2], marker='o', linewidth=2, label='投资金额')
    for j, val in enumerate(investments):
        ax2.text(x[j] + width / 2, val, f'{val:.2f}', ha='center', va='bottom', fontsize=7, color=COLOR_TEXT)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('项目数量', fontsize=9)
    ax2.set_ylabel('投资金额（亿元）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n在研项目数量及投资金额', fontsize=14, fontweight="bold", pad=20)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc='upper center',
              bbox_to_anchor=(0.5, 1.08), ncol=2, frameon=False)
    setup_chart_style(ax)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.2)
    ax2.set_ylim(0, ax2.get_ylim()[1] * 1.2)


def plot_customer_concentration_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """客户集中度"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n客户集中度', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    vals = df.loc['客户集中度'].values
    x = np.arange(len(years))
    bars = ax.bar(x, vals, 0.5, color=COLORS_BAR[0], edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{val:.1f}%',
                ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('占比（%）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n客户集中度（前五大）', fontsize=14, fontweight="bold", pad=20)
    setup_chart_style(ax)
    ax.set_ylim(0, max(vals) * 1.2 if len(vals) > 0 else 1)


def plot_supplier_concentration_chart(ax, df: pd.DataFrame, stock_name: str, stock_code: str):
    """供应商集中度"""
    if df is None or df.empty:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{stock_code} {stock_name}\n供应商集中度', fontsize=14, fontweight="bold")
        ax.axis('off')
        return
    years = df.columns.tolist()
    vals = df.loc['供应商集中度'].values
    x = np.arange(len(years))
    bars = ax.bar(x, vals, 0.5, color=COLORS_BAR[0], edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{val:.1f}%',
                ha='center', va='bottom', fontsize=8, color=COLOR_TEXT, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{y}年' for y in years], fontsize=9)
    ax.set_ylabel('占比（%）', fontsize=9)
    ax.set_title(f'{stock_code} {stock_name}\n供应商集中度（前五大）', fontsize=14, fontweight="bold", pad=20)
    setup_chart_style(ax)
    ax.set_ylim(0, max(vals) * 1.2 if len(vals) > 0 else 1)


# ==================== 综合绘图 ====================
def plot_all_charts(stock: StockIndex, save_path: Optional[Path] = None):
    """绘制 4×4 综合图表"""
    gross_margin_df = load_revenue_gross_margin_data(stock.revenue_cost_file)
    margin_line_df = load_region_gross_margin(stock.revenue_cost_detail_file)
    impairment_df = load_impairment_top3_data(stock.impairment_file)
    non_op_income_df = load_non_operating_income_top3_data(stock.non_operating_income_file)
    finance_df = load_finance_expense_data(stock.finance_expense_file)
    mgmt_df = load_expense_top5_data(stock.management_expense_file)
    sales_df = load_expense_top5_data(stock.sales_expense_file)
    rd_df = load_rd_expense_top5_data(stock.rd_expense_file)
    aging_df = load_aging_data(stock.aging_file)
    inventory_df = load_inventory_data(stock.inventory_file)
    emp_comp_df = load_employee_compensation_data(stock.employee_compensation_file)
    fixed_asset_df = load_fixed_asset_data(stock.fixed_asset_file)
    ip_df = load_ip_data(stock.ip_file)
    rnd_project_df = load_rnd_projects_data(stock.rnd_project_file)
    customer_df = load_customer_concentration_data(stock.top5_customer_file)
    supplier_df = load_supplier_concentration_data(stock.top5_supplier_file)

    fig, axes = plt.subplots(8, 2, figsize=(14, 40))
    fig.suptitle(f'{stock.code} {stock.name}  ┊  财务状况深度分析', fontsize=24, fontweight='bold', y=0.99)

    plot_revenue_gross_margin_chart(axes[0, 0], gross_margin_df, stock.name, stock.code)
    plot_margin_line_chart(axes[0, 1], margin_line_df, stock.name, stock.code)
    plot_impairment_chart(axes[1, 0], impairment_df, stock.name, stock.code)
    plot_non_operating_income_chart(axes[1, 1], non_op_income_df, stock.name, stock.code)

    plot_finance_expense_chart(axes[2, 0], finance_df, stock.name, stock.code)
    plot_expense_stacked_chart(axes[2, 1], mgmt_df, stock.name, stock.code, "管理费用")
    plot_expense_stacked_chart(axes[3, 0], sales_df, stock.name, stock.code, "销售费用")
    plot_expense_stacked_chart(axes[3, 1], rd_df, stock.name, stock.code, "研发费用")

    plot_aging_chart(axes[4, 0], aging_df, stock.name, stock.code)
    plot_inventory_chart(axes[4, 1], inventory_df, stock.name, stock.code)
    plot_employee_comp_chart(axes[5, 0], emp_comp_df, stock.name, stock.code)
    plot_fixed_asset_chart(axes[5, 1], fixed_asset_df, stock.name, stock.code)

    plot_ip_chart(axes[6, 0], ip_df, stock.name, stock.code)
    plot_rnd_projects_chart(axes[6, 1], rnd_project_df, stock.name, stock.code)
    plot_customer_concentration_chart(axes[7, 0], customer_df, stock.name, stock.code)
    plot_supplier_concentration_chart(axes[7, 1], supplier_df, stock.name, stock.code)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # 生成 LLM 语义分析摘要并拼接
    if save_path:
        # 先保存 Portrait 到临时文件
        portrait_tmp = '/tmp/_portrait_tmp.png'
        fig.savefig(portrait_tmp, dpi=300, bbox_inches='tight')
        plt.close(fig)

        # --- 加载 Portrait 数据并生成趋势分析头部 ---
        header_img = None
        portrait_json = stock.dir_path.parent / "portrait_data" / f"{stock.code}_{stock.name}_portrait_data.json"
        if portrait_json.exists():
            try:
                with open(portrait_json, 'r', encoding='utf-8') as f:
                    portrait_data = json.load(f)
                # 调用 LLM 生成 5 维度总结
                sys.path.insert(0, str(Path(__file__).parent))
                from LLM2Excel3 import LLMCombinedAnalyzer
                # 自动选择 LLM provider
                if os.environ.get('DEEPSEEK_API_KEY'):
                    provider = 'deepseek'
                    model = 'deepseek-chat'
                elif os.environ.get('KIMI_API_KEY'):
                    provider = 'moonshot'
                    model = 'kimi-k2p5'
                else:
                    provider = 'ollama'
                    model = 'gemma3:1b'
                analyzer = LLMCombinedAnalyzer(model=model, provider=provider)
                portrait_summary = analyzer.analyze_portrait_data(portrait_data, stock.code, stock.name)
                if portrait_summary:
                    header_img = plot_portrait_trend_header(portrait_summary, stock.name, stock.code)
                    print(f"  📊 Portrait 趋势头部已生成 ({len(portrait_summary)} 维度)")
            except Exception as e:
                print(f"  ⚠️ Portrait 趋势头部生成失败: {e}")

        llm_file = stock.dir_path / f'{stock.code}_{stock.name}_LLM分析结果.xlsx'
        comp_df = load_llm_competitiveness_summary(llm_file)
        biz_df = load_llm_business_summary(llm_file)

        # 收集所有图层
        layers = []
        if header_img:
            layers.append(header_img)
        layers.append(Image.open(portrait_tmp))
        if comp_df is not None or biz_df is not None:
            llm_img = plot_llm_summary_figure(comp_df, biz_df, stock.name, stock.code)
            if llm_img and llm_img.size != (1, 1):
                layers.append(llm_img)

        # 三层垂直拼接
        if len(layers) > 1:
            w = max(img.width for img in layers)
            h = sum(img.height for img in layers)
            combined = Image.new('RGB', (w, h), 'white')
            y = 0
            for img in layers:
                combined.paste(img, (0, y))
                y += img.height
            combined.save(save_path, dpi=(300, 300))
            print(f"图表已保存至：{save_path}（含趋势头部 + {len(layers)-1} 层）")
        else:
            layers[0].save(save_path, dpi=(300, 300))
            print(f"图表已保存至：{save_path}")

        # 同时保存结构化数据（懒加载避免循环导入）
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from portrait_data_export import save_portrait_data
            save_portrait_data(stock, stock.dir_path.parent)
        except ImportError:
            pass  # 可选模块，不存在时跳过
    else:
        plt.show()
        plt.close(fig)


# ==================== 交互主程序 ====================
def main(output_dir: Path):
    index = DataIndex(output_dir)
    stocks = index.list_all()
    if not stocks:
        print(f"未在 {output_dir} 目录中找到股票数据")
        return

    print("=" * 60)
    print("Portrait - 综合财务数据可视化工具")
    print("=" * 60)
    print(f"\n已发现 {len(stocks)} 只股票的数据，示例：")
    for s in stocks[:5]:
        flags = []
        if s.aging_file:
            flags.append('账龄')
        if s.revenue_cost_file or s.revenue_cost_detail_file:
            flags.append('收入成本')
        if s.finance_expense_file:
            flags.append('财务费用')
        if s.management_expense_file:
            flags.append('管理费用')
        if s.sales_expense_file:
            flags.append('销售费用')
        print(f"  {s.code}  {s.name}  ({', '.join(flags) if flags else '无'})")
    if len(stocks) > 5:
        print(f"  ... 等共 {len(stocks)} 只")

    while True:
        print("\n" + "-" * 60)
        query = input("请输入股票代码或股票名称（输入 q 退出）：").strip()
        if query.lower() in ('q', 'quit', 'exit'):
            print("已退出")
            break

        stock = index.search(query)
        if stock is None:
            print("未找到匹配的股票，请检查后重新输入")
            continue

        print(f"\n已选中：{stock.code} {stock.name}")

        save_input = input("是否保存图表？（y/n，默认 y）：").strip().lower()
        if save_input in ('', 'y', 'yes'):
            portraits_dir = output_dir.parent / "portraits"
            portraits_dir.mkdir(exist_ok=True)
            save_path = portraits_dir / f"Portrait_{stock.code}_{stock.name}.png"
            plot_all_charts(stock, save_path=save_path)
        else:
            plot_all_charts(stock)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Portrait - 综合财务数据可视化')
    parser.add_argument('query', nargs='?', help='股票代码或股票名称（可选，不提供则进入交互模式）')
    parser.add_argument('--save', '-s', action='store_true', help='直接保存图表，不弹窗显示')
    parser.add_argument('--all', '-a', action='store_true', help='批量生成所有股票的图表')
    parser.add_argument('--output-dir', '-o', type=str, default='output2', help='数据目录（默认 output2）')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    index = DataIndex(output_dir)
    stocks = index.list_all()
    if not stocks:
        print(f"未在 {output_dir} 目录中找到股票数据")
        sys.exit(1)

    if args.all:
        print(f"开始批量生成 {len(stocks)} 只股票的图表...")
        success_count = 0
        portraits_dir = output_dir.parent / "portraits"
        portraits_dir.mkdir(exist_ok=True)
        for stock in stocks:
            save_path = portraits_dir / f"Portrait_{stock.code}_{stock.name}.png"
            plot_all_charts(stock, save_path=save_path)
            success_count += 1
        print(f"\n批量生成完成，共 {success_count} 只")
        sys.exit(0)

    if args.query:
        stock = index.search(args.query)
        if stock is None:
            print(f"未找到匹配的股票：{args.query}")
            sys.exit(1)

        print(f"已选中：{stock.code} {stock.name}")

        if args.save:
            portraits_dir = output_dir.parent / "portraits"
            portraits_dir.mkdir(exist_ok=True)
            save_path = portraits_dir / f"Portrait_{stock.code}_{stock.name}.png"
            plot_all_charts(stock, save_path=save_path)
        else:
            plot_all_charts(stock)
    else:
        main(output_dir)
