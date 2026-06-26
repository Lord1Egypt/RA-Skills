#!/usr/bin/env python3
"""
财务报表分析脚本
功能：读取包含资产负债表、利润表、现金流量表等Sheet的Excel财务报表，
输出专业的财务分析报告（Markdown格式）。

用法：
    python analyze_financial_report.py <excel_file_path> [output_file]

参数：
    excel_file_path  : 财务报表Excel文件路径
    output_file      : 输出Markdown文件路径（可选，默认：financial_analysis_report.md）
"""

import sys
import os
import json
import re
from pathlib import Path

try:
    import pandas as pd
    import openpyxl
except ImportError:
    print("正在安装依赖...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
    import pandas as pd
    import openpyxl


# ─────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────

def fmt_num(v, decimals=2):
    """格式化数字，处理None/NaN"""
    try:
        if v is None or (isinstance(v, float) and (pd.isna(v))):
            return "N/A"
        return f"{float(v):,.{decimals}f}"
    except Exception:
        return str(v)


def pct(v, decimals=2):
    """格式化百分比"""
    try:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return "N/A"
        return f"{float(v) * 100:.{decimals}f}%"
    except Exception:
        return str(v)


def safe_div(a, b):
    """安全除法"""
    try:
        a, b = float(a), float(b)
        if b == 0:
            return None
        return a / b
    except Exception:
        return None


def change_rate(curr, prev):
    """计算增减变动率"""
    try:
        curr, prev = float(curr), float(prev)
        if prev == 0:
            return None
        return (curr - prev) / abs(prev)
    except Exception:
        return None


def find_value(df, keywords, col_index=None):
    """
    在DataFrame中按关键词模糊匹配行，返回指定列的值。
    df: 两列（科目名, 数值）或多列的DataFrame
    keywords: 关键词列表（任意一个匹配即可）
    col_index: 取哪一列（默认取第二列）
    """
    if df is None or df.empty:
        return None
    label_col = df.columns[0]
    for kw in keywords:
        mask = df[label_col].astype(str).str.contains(kw, na=False)
        rows = df[mask]
        if not rows.empty:
            idx = col_index if col_index is not None else 1
            if idx < len(df.columns):
                val = rows.iloc[0, idx]
                try:
                    return float(val)
                except Exception:
                    return None
    return None


# ─────────────────────────────────────────
# 读取Excel
# ─────────────────────────────────────────

SHEET_ALIASES = {
    "balance": ["资产负债表", "Balance Sheet", "balance sheet", "BalanceSheet", "资产负债", "资产"],
    "income":  ["利润表", "损益表", "Income Statement", "income", "P&L", "利润"],
    "cashflow": ["现金流量表", "现金流量", "现流", "Cash Flow", "cashflow", "CashFlow", "现金流"],
}


def load_excel(path: str) -> dict:
    """读取Excel所有Sheet，返回 {sheet_name: DataFrame}"""
    xl = pd.ExcelFile(path, engine="openpyxl")
    sheets = {}
    for name in xl.sheet_names:
        df = xl.parse(name, header=None)
        sheets[name] = df
    return sheets


def detect_sheet(sheets: dict, category: str):
    """根据分类别名，在sheets中找到对应的DataFrame"""
    aliases = SHEET_ALIASES.get(category, [])
    # 优先精确匹配
    for alias in aliases:
        for name, df in sheets.items():
            if alias.lower() in name.lower():
                return name, df
    # 模糊匹配第一列内容
    for name, df in sheets.items():
        first_col = df.iloc[:, 0].astype(str)
        if category == "balance" and first_col.str.contains("资产|负债|权益", na=False).any():
            return name, df
        if category == "income" and first_col.str.contains("营业收入|营收|净利润", na=False).any():
            return name, df
        if category == "cashflow" and first_col.str.contains("经营活动|现金", na=False).any():
            return name, df
    return None, None


def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗原始DataFrame：
    - 找到真正的表头行（包含"项目"/"科目"/"年份"等字样，或数字年份）
    - 删除全空行/列
    - 重置索引
    """
    if raw_df is None or raw_df.empty:
        return pd.DataFrame()

    # 尝试找表头行
    header_row = 0
    for i, row in raw_df.iterrows():
        row_str = " ".join(row.fillna("").astype(str))
        if re.search(r"项目|科目|年份|期末|期初|本期|上期|\d{4}", row_str):
            header_row = i
            break

    df = raw_df.iloc[header_row:].copy()
    df.columns = range(len(df.columns))
    df = df.dropna(how="all").dropna(axis=1, how="all")
    df = df.reset_index(drop=True)
    return df


def extract_periods(df: pd.DataFrame) -> list:
    """从DataFrame第一行提取期间标签"""
    if df.empty:
        return []
    first_row = df.iloc[0]
    periods = []
    for val in first_row:
        s = str(val).strip()
        if s and s not in ("nan", "None", "项目", "科目"):
            # 匹配年份或期间描述
            if re.search(r"\d{4}", s) or re.search(r"期末|期初|本期|上期", s):
                periods.append(s)
    return periods


def to_data_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    将清洗后的DataFrame转为 (科目, 本期, 上期) 格式。
    自动：
    1. 跳过表头/标题行
    2. 识别哪些列是数值列（本期/上期），跳过附注列
    3. 取科目名（第0列）+ 最多2个数值列
    """
    if df.empty:
        return pd.DataFrame()

    # 找到真正的数据起始行
    data_start = 0
    for i in range(len(df)):
        row = df.iloc[i]
        label = str(row.iloc[0]).strip()
        if label in ("nan", "None", "", "项目", "科目", "项          目"):
            continue
        has_num = any(
            str(v).strip() not in ("nan", "None", "NaT", "")
            and re.search(r"^-?\d[\d,\.]*$", str(v).strip())
            for v in row.iloc[1:]
        )
        if has_num:
            data_start = i
            break

    result = df.iloc[data_start:].copy()
    result.columns = range(len(result.columns))
    result = result.dropna(subset=[0])
    result[0] = result[0].astype(str).str.strip()
    result = result[result[0].notna() & (result[0] != "nan") & (result[0] != "") & (result[0] != "NaT")]

    # 识别数值列：找出至少有30%行是数字的列
    num_cols = []
    for col in result.columns[1:]:
        col_vals = result[col].astype(str).str.strip()
        num_count = col_vals.apply(lambda v: bool(re.match(r"^-?\d[\d,\.]*$", str(v))) if str(v) not in ("nan","None","NaT","") else False).sum()
        if num_count >= max(1, len(result) * 0.15):
            num_cols.append(col)

    if len(num_cols) == 0:
        # 退化：直接用第2、3列
        num_cols = list(result.columns[1:3]) if len(result.columns) >= 3 else list(result.columns[1:])

    # 最多取2个数值列（本期、上期）
    use_cols = num_cols[:2]
    out = result[[0] + use_cols].copy()
    out.columns = range(len(out.columns))

    # 数值列转float
    for c in out.columns[1:]:
        out[c] = pd.to_numeric(out[c].astype(str).str.replace(",", "").str.strip(), errors="coerce")

    return out.reset_index(drop=True)


# ─────────────────────────────────────────
# 分析模块
# ─────────────────────────────────────────

def build_change_table(df: pd.DataFrame, title: str) -> str:
    """
    报表项目增减变动表：本期 vs 上期，计算变动金额和变动比例。
    df必须有至少3列：科目名、本期金额、上期金额
    """
    if df.empty or len(df.columns) < 3:
        return f"> **{title}** 数据不足，无法生成增减变动表。\n\n"

    lines = [f"### {title} — 增减变动分析\n"]
    lines.append("| 项目 | 本期 | 上期 | 变动金额 | 变动率 |")
    lines.append("|------|------|------|----------|--------|")

    for _, row in df.iterrows():
        label = str(row.iloc[0]).strip()
        if not label or label in ("nan", "小计", "合计") :
            continue
        try:
            curr = float(row.iloc[1]) if str(row.iloc[1]).strip() not in ("nan","None","") else None
            prev = float(row.iloc[2]) if str(row.iloc[2]).strip() not in ("nan","None","") else None
        except Exception:
            curr, prev = None, None

        if curr is None and prev is None:
            continue

        if curr is not None and prev is not None:
            delta = curr - prev
            rate = change_rate(curr, prev)
            rate_str = pct(rate) if rate is not None else "N/A"
            flag = "🔺" if (delta > 0) else ("🔻" if delta < 0 else "—")
            lines.append(f"| {label} | {fmt_num(curr)} | {fmt_num(prev)} | {flag} {fmt_num(delta)} | {rate_str} |")
        else:
            lines.append(f"| {label} | {fmt_num(curr)} | {fmt_num(prev)} | — | — |")

    lines.append("")
    return "\n".join(lines) + "\n"


def build_structure_table(df: pd.DataFrame, base_keywords: list, title: str, base_label: str = "合计") -> str:
    """
    结构变动表：各项目占基准项目的比例，对比本期与上期。
    """
    if df.empty or len(df.columns) < 3:
        return f"> **{title}** 数据不足，无法生成结构变动表。\n\n"

    # 找基准值（总资产或营业收入）
    base_curr = find_value(df, base_keywords, 1)
    base_prev = find_value(df, base_keywords, 2)

    lines = [f"### {title} — 结构变动分析（基准：{base_label}）\n"]

    if not base_curr or not base_prev:
        lines.append(f"> 未能找到基准项目（{base_label}），无法计算结构比例。\n")
        return "\n".join(lines) + "\n"

    lines.append(f"> 本期{base_label}：**{fmt_num(base_curr)}**　上期{base_label}：**{fmt_num(base_prev)}**\n")
    lines.append(f"| 项目 | 本期金额 | 本期占比 | 上期金额 | 上期占比 | 占比变动 |")
    lines.append(f"|------|----------|----------|----------|----------|----------|")

    for _, row in df.iterrows():
        label = str(row.iloc[0]).strip()
        if not label or label in ("nan",):
            continue
        try:
            curr = float(row.iloc[1]) if str(row.iloc[1]).strip() not in ("nan","None","") else None
            prev = float(row.iloc[2]) if str(row.iloc[2]).strip() not in ("nan","None","") else None
        except Exception:
            curr, prev = None, None

        if curr is None and prev is None:
            continue

        r_curr = safe_div(curr, base_curr)
        r_prev = safe_div(prev, base_prev)

        if r_curr is not None and r_prev is not None:
            r_delta = r_curr - r_prev
            delta_str = f"{r_delta*100:+.2f}pp"
        else:
            delta_str = "N/A"

        lines.append(
            f"| {label} | {fmt_num(curr)} | {pct(r_curr)} | {fmt_num(prev)} | {pct(r_prev)} | {delta_str} |"
        )

    lines.append("")
    return "\n".join(lines) + "\n"


def calculate_ratios(bs_df, inc_df, cf_df) -> dict:
    """
    计算财务指标：盈利能力、偿债能力、营运能力、成长能力
    返回 {指标分类: [(指标名, 本期值, 上期值, 说明)]}
    """

    def g(df, kws, col=1):
        return find_value(df, kws, col)

    # ─── 资产负债表取值 ───
    # 本期
    total_assets_c      = g(bs_df, ["资产合计","总资产","资产总计"])
    current_assets_c    = g(bs_df, ["流动资产合计","流动资产"])
    non_current_c       = g(bs_df, ["非流动资产合计"])
    cash_c              = g(bs_df, ["货币资金"])
    inventory_c         = g(bs_df, ["存货"])
    ar_c                = g(bs_df, ["应收账款"])
    total_liab_c        = g(bs_df, ["负债合计","总负债","负债总计"])
    current_liab_c      = g(bs_df, ["流动负债合计","流动负债"])
    non_current_liab_c  = g(bs_df, ["非流动负债合计"])
    equity_c            = g(bs_df, ["所有者权益合计","股东权益合计","净资产"])
    short_debt_c        = g(bs_df, ["短期借款"])
    long_debt_c         = g(bs_df, ["长期借款"])

    # 上期
    total_assets_p      = g(bs_df, ["资产合计","总资产","资产总计"], 2)
    current_assets_p    = g(bs_df, ["流动资产合计","流动资产"], 2)
    total_liab_p        = g(bs_df, ["负债合计","总负债","负债总计"], 2)
    current_liab_p      = g(bs_df, ["流动负债合计","流动负债"], 2)
    equity_p            = g(bs_df, ["所有者权益合计","股东权益合计","净资产"], 2)
    ar_p                = g(bs_df, ["应收账款"], 2)
    inventory_p         = g(bs_df, ["存货"], 2)

    # ─── 利润表取值 ───
    revenue_c           = g(inc_df, ["营业收入","营业总收入","收入"])
    revenue_p           = g(inc_df, ["营业收入","营业总收入","收入"], 2)
    cogs_c              = g(inc_df, ["营业成本","主营业务成本"])
    net_profit_c        = g(inc_df, ["净利润","归属于母公司所有者的净利润"])
    net_profit_p        = g(inc_df, ["净利润","归属于母公司所有者的净利润"], 2)
    gross_profit_c      = None
    if revenue_c and cogs_c:
        try:
            gross_profit_c = float(revenue_c) - float(cogs_c)
        except Exception:
            pass
    operating_profit_c  = g(inc_df, ["营业利润"])
    operating_profit_p  = g(inc_df, ["营业利润"], 2)
    ebit_c              = operating_profit_c
    interest_c          = g(inc_df, ["财务费用","利息费用"])
    income_tax_c        = g(inc_df, ["所得税费用"])

    # ─── 现金流量表取值 ───
    operating_cf_c      = g(cf_df, ["经营活动产生的现金流量净额","经营活动现金流量净额"])
    operating_cf_p      = g(cf_df, ["经营活动产生的现金流量净额","经营活动现金流量净额"], 2)

    ratios = {}

    # ─── 盈利能力指标 ───
    profitability = []
    # 毛利率
    gp_rate_c = safe_div(gross_profit_c, revenue_c)
    gp_rate_p = None
    if revenue_p:
        cogs_p = g(inc_df, ["营业成本","主营业务成本"], 2)
        if cogs_p:
            try:
                gp_rate_p = safe_div(float(revenue_p) - float(cogs_p), revenue_p)
            except Exception:
                pass
    profitability.append(("毛利率", pct(gp_rate_c), pct(gp_rate_p), "毛利/营业收入，反映产品盈利空间"))

    # 净利率
    npm_c = safe_div(net_profit_c, revenue_c)
    npm_p = safe_div(net_profit_p, revenue_p)
    profitability.append(("净利率", pct(npm_c), pct(npm_p), "净利润/营业收入，综合盈利能力"))

    # ROA
    avg_assets = None
    if total_assets_c and total_assets_p:
        avg_assets = (float(total_assets_c) + float(total_assets_p)) / 2
    roa_c = safe_div(net_profit_c, avg_assets)
    profitability.append(("总资产收益率(ROA)", pct(roa_c), "—", "净利润/平均总资产，资产运用效率"))

    # ROE
    avg_equity = None
    if equity_c and equity_p:
        avg_equity = (float(equity_c) + float(equity_p)) / 2
    roe_c = safe_div(net_profit_c, avg_equity)
    profitability.append(("净资产收益率(ROE)", pct(roe_c), "—", "净利润/平均净资产，股东回报率"))

    # 营业利润率
    op_rate_c = safe_div(operating_profit_c, revenue_c)
    op_rate_p = safe_div(operating_profit_p, revenue_p)
    profitability.append(("营业利润率", pct(op_rate_c), pct(op_rate_p), "营业利润/营业收入"))

    ratios["盈利能力指标"] = profitability

    # ─── 偿债能力指标 ───
    solvency = []
    # 流动比率
    cr_c = safe_div(current_assets_c, current_liab_c)
    cr_p = safe_div(current_assets_p, current_liab_p)
    solvency.append(("流动比率", fmt_num(cr_c), fmt_num(cr_p), "流动资产/流动负债，参考值≥2"))

    # 速动比率
    quick_assets_c = None
    if current_assets_c and inventory_c:
        try:
            quick_assets_c = float(current_assets_c) - float(inventory_c)
        except Exception:
            pass
    qr_c = safe_div(quick_assets_c, current_liab_c)
    quick_assets_p = None
    if current_assets_p and inventory_p:
        try:
            quick_assets_p = float(current_assets_p) - float(inventory_p)
        except Exception:
            pass
    qr_p = safe_div(quick_assets_p, current_liab_p)
    solvency.append(("速动比率", fmt_num(qr_c), fmt_num(qr_p), "(流动资产-存货)/流动负债，参考值≥1"))

    # 资产负债率
    dr_c = safe_div(total_liab_c, total_assets_c)
    dr_p = safe_div(total_liab_p, total_assets_p)
    solvency.append(("资产负债率", pct(dr_c), pct(dr_p), "总负债/总资产，衡量财务风险"))

    # 利息保障倍数
    if ebit_c and interest_c:
        try:
            icr = safe_div(float(ebit_c) + abs(float(interest_c)), abs(float(interest_c)))
            solvency.append(("利息保障倍数", fmt_num(icr), "—", "EBIT/利息费用，参考值≥3"))
        except Exception:
            solvency.append(("利息保障倍数", "N/A", "—", "数据不足"))

    # 产权比率
    er_c = safe_div(total_liab_c, equity_c)
    er_p = safe_div(total_liab_p, equity_p)
    solvency.append(("产权比率", fmt_num(er_c), fmt_num(er_p), "总负债/股东权益"))

    ratios["偿债能力指标"] = solvency

    # ─── 营运能力指标 ───
    operations = []
    # 总资产周转率
    tat_c = safe_div(revenue_c, avg_assets)
    operations.append(("总资产周转率", f"{fmt_num(tat_c)} 次", "—", "营业收入/平均总资产"))

    # 应收账款周转率
    avg_ar = None
    if ar_c and ar_p:
        avg_ar = (float(ar_c) + float(ar_p)) / 2
    art_c = safe_div(revenue_c, avg_ar)
    if art_c:
        art_days = safe_div(365, art_c)
        operations.append(("应收账款周转率", f"{fmt_num(art_c)} 次 ({fmt_num(art_days)}天)", "—", "营业收入/平均应收账款"))
    else:
        operations.append(("应收账款周转率", "N/A", "—", "数据不足"))

    # 存货周转率
    avg_inv = None
    if inventory_c and inventory_p:
        avg_inv = (float(inventory_c) + float(inventory_p)) / 2
    invt_c = safe_div(cogs_c, avg_inv)
    if invt_c:
        invt_days = safe_div(365, invt_c)
        operations.append(("存货周转率", f"{fmt_num(invt_c)} 次 ({fmt_num(invt_days)}天)", "—", "营业成本/平均存货"))
    else:
        operations.append(("存货周转率", "N/A", "—", "数据不足"))

    # 流动资产周转率
    avg_ca = None
    if current_assets_c and current_assets_p:
        avg_ca = (float(current_assets_c) + float(current_assets_p)) / 2
    cat_c = safe_div(revenue_c, avg_ca)
    operations.append(("流动资产周转率", f"{fmt_num(cat_c)} 次", "—", "营业收入/平均流动资产"))

    ratios["营运能力指标"] = operations

    # ─── 成长能力指标 ───
    growth = []
    rev_growth = change_rate(revenue_c, revenue_p)
    np_growth = change_rate(net_profit_c, net_profit_p)
    asset_growth = change_rate(total_assets_c, total_assets_p)
    equity_growth = change_rate(equity_c, equity_p)
    op_cf_growth = change_rate(operating_cf_c, operating_cf_p)
    op_profit_growth = change_rate(operating_profit_c, operating_profit_p)

    growth.append(("营业收入增长率", pct(rev_growth), "—", "本期收入相较上期的增长情况"))
    growth.append(("净利润增长率", pct(np_growth), "—", "盈利规模的扩张速度"))
    growth.append(("总资产增长率", pct(asset_growth), "—", "资产规模扩张速度"))
    growth.append(("净资产增长率", pct(equity_growth), "—", "所有者权益的增长情况"))
    growth.append(("营业利润增长率", pct(op_profit_growth), "—", "核心业务盈利增长"))
    growth.append(("经营现金流增长率", pct(op_cf_growth), "—", "经营活动现金流净额增长"))

    ratios["成长能力指标"] = growth

    return ratios


def build_ratio_section(ratios: dict) -> str:
    """将财务比率字典格式化为Markdown表格"""
    lines = ["## 四、财务比率综合分析\n"]
    for category, items in ratios.items():
        lines.append(f"### {category}\n")
        lines.append("| 指标 | 本期 | 上期/参考 | 说明 |")
        lines.append("|------|------|-----------|------|")
        for name, curr_val, prev_val, note in items:
            lines.append(f"| {name} | {curr_val} | {prev_val} | {note} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def generate_expert_summary(ratios: dict, bs_df, inc_df, cf_df) -> str:
    """
    基于计算结果，生成资深财务专家的综合分析总结与建议。
    （规则模板 + 数值驱动判断）
    """

    def g(d, cat, name):
        items = d.get(cat, [])
        for item in items:
            if item[0] == name:
                try:
                    raw = item[1].replace("%", "").replace("次", "").replace("天", "").strip()
                    if "(" in raw:
                        raw = raw.split("(")[0].strip()
                    return float(raw) if raw not in ("N/A", "—", "") else None
                except Exception:
                    return None
        return None

    gp_rate     = g(ratios, "盈利能力指标", "毛利率")
    npm         = g(ratios, "盈利能力指标", "净利率")
    roe         = g(ratios, "盈利能力指标", "净资产收益率(ROE)")
    roa         = g(ratios, "盈利能力指标", "总资产收益率(ROA)")
    cr          = g(ratios, "偿债能力指标", "流动比率")
    dr          = g(ratios, "偿债能力指标", "资产负债率")
    rev_growth  = g(ratios, "成长能力指标", "营业收入增长率")
    np_growth   = g(ratios, "成长能力指标", "净利润增长率")

    lines = ["## 五、资深财务专家综合分析与建议\n"]
    lines.append("> 以下分析基于报表数据自动提取，建议结合行业背景与管理层说明综合判断。\n")

    # ── 盈利能力评价 ──
    lines.append("### 5.1 盈利能力评价\n")
    if gp_rate is not None:
        if gp_rate > 40:
            lines.append(f"- ✅ **毛利率 {gp_rate:.2f}%** 处于较高水平，产品/服务具备较强的竞争优势与定价能力。")
        elif gp_rate > 20:
            lines.append(f"- ⚠️ **毛利率 {gp_rate:.2f}%** 处于中等水平，盈利空间一般，需关注成本管控与产品结构优化。")
        else:
            lines.append(f"- 🔴 **毛利率 {gp_rate:.2f}%** 偏低，建议深入分析原材料成本、定价策略及产品结构。")
    if npm is not None:
        if npm > 15:
            lines.append(f"- ✅ **净利率 {npm:.2f}%** 较高，说明期间费用管控较好，整体盈利质量优秀。")
        elif npm > 5:
            lines.append(f"- ⚠️ **净利率 {npm:.2f}%** 适中，关注费用率是否有压缩空间。")
        else:
            lines.append(f"- 🔴 **净利率 {npm:.2f}%** 偏低，盈利薄弱，需排查费用结构或收入质量问题。")
    if roe is not None:
        if roe > 15:
            lines.append(f"- ✅ **ROE {roe:.2f}%** 优秀，股东资金得到有效利用，具备较强的价值创造能力。")
        elif roe > 8:
            lines.append(f"- ⚠️ **ROE {roe:.2f}%** 一般，股东回报有待提升，关注资产运营效率与杠杆水平。")
        else:
            lines.append(f"- 🔴 **ROE {roe:.2f}%** 偏低，需关注盈利模式与资产利用效率。")
    lines.append("")

    # ── 偿债能力评价 ──
    lines.append("### 5.2 偿债能力评价\n")
    if cr is not None:
        if cr >= 2:
            lines.append(f"- ✅ **流动比率 {cr:.2f}**，短期偿债能力充足，流动性风险较低。")
        elif cr >= 1:
            lines.append(f"- ⚠️ **流动比率 {cr:.2f}**，短期偿债能力尚可，但应关注流动资产质量（如应收账款可回收性）。")
        else:
            lines.append(f"- 🔴 **流动比率 {cr:.2f}**，低于1，短期偿债压力较大，存在流动性风险，需关注现金流状况。")
    if dr is not None:
        if dr < 40:
            lines.append(f"- ✅ **资产负债率 {dr:.2f}%**，财务结构稳健，债务风险低。")
        elif dr < 65:
            lines.append(f"- ⚠️ **资产负债率 {dr:.2f}%**，负债水平适中，建议关注债务到期结构与偿债安排。")
        else:
            lines.append(f"- 🔴 **资产负债率 {dr:.2f}%**，杠杆率较高，财务风险显著，建议优化负债结构或加快去杠杆。")
    lines.append("")

    # ── 成长能力评价 ──
    lines.append("### 5.3 成长能力评价\n")
    if rev_growth is not None:
        if rev_growth > 20:
            lines.append(f"- ✅ **营业收入增长率 {rev_growth:.2f}%**，高速增长，市场拓展能力强劲。")
        elif rev_growth > 0:
            lines.append(f"- ⚠️ **营业收入增长率 {rev_growth:.2f}%**，稳步增长，但增速有限，需持续开拓市场。")
        else:
            lines.append(f"- 🔴 **营业收入增长率 {rev_growth:.2f}%**，收入下滑，需警惕市场竞争加剧或需求萎缩。")
    if np_growth is not None:
        if np_growth > rev_growth if (rev_growth is not None) else np_growth > 10:
            lines.append(f"- ✅ **净利润增长率 {np_growth:.2f}%** 超过收入增速，规模效应显现，盈利质量提升。")
        elif np_growth > 0:
            lines.append(f"- ⚠️ **净利润增长率 {np_growth:.2f}%**，保持正增长但低于收入增速，成本费用管控需加强。")
        else:
            lines.append(f"- 🔴 **净利润增长率 {np_growth:.2f}%**，利润下滑，需分析原因是收入降低还是成本费用上升。")
    lines.append("")

    # ── 综合建议 ──
    lines.append("### 5.4 综合建议\n")

    risk_flags = []
    strength_flags = []

    if gp_rate is not None and gp_rate < 20:
        risk_flags.append("毛利率偏低，产品竞争力或定价能力有待加强")
    if npm is not None and npm < 5:
        risk_flags.append("净利率偏低，关注费用率控制")
    if cr is not None and cr < 1:
        risk_flags.append("流动比率不足1，短期流动性存在压力")
    if dr is not None and dr > 65:
        risk_flags.append("资产负债率偏高，财务杠杆风险需关注")
    if rev_growth is not None and rev_growth < 0:
        risk_flags.append("营业收入出现负增长，市场竞争力减弱")
    if np_growth is not None and np_growth < 0:
        risk_flags.append("净利润负增长，盈利能力有所弱化")

    if gp_rate is not None and gp_rate > 40:
        strength_flags.append("高毛利率，具备较强产品竞争壁垒")
    if roe is not None and roe > 15:
        strength_flags.append("ROE较高，股东回报能力突出")
    if cr is not None and cr > 2:
        strength_flags.append("流动性充裕，短期财务安全性好")
    if rev_growth is not None and rev_growth > 20:
        strength_flags.append("收入高速增长，成长势头良好")

    if strength_flags:
        lines.append("**核心优势：**\n")
        for s in strength_flags:
            lines.append(f"- ✅ {s}")
        lines.append("")

    if risk_flags:
        lines.append("**风险提示：**\n")
        for r in risk_flags:
            lines.append(f"- ⚠️ {r}")
        lines.append("")

    lines.append("**改进建议：**\n")
    lines.append("1. **盈利提升**：持续优化产品/服务结构，提升附加值，加强成本管控，关注费用率变化趋势。")
    lines.append("2. **偿债安全**：优化债务期限结构，保持充足的备用信用额度，密切监控经营现金流覆盖情况。")
    lines.append("3. **资产效率**：加快应收账款回款与存货周转，提升资产运营效率，避免资金沉淀。")
    lines.append("4. **成长驱动**：聚焦主营业务核心能力，合理规划资本支出，在保持盈利质量的前提下稳步扩张。")
    lines.append("5. **信息质量**：建议结合附注、管理层讨论及行业对标数据，深化分析结论的可靠性。")
    lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────

def merge_balance_sheets(sheets: dict) -> pd.DataFrame:
    """
    当资产负债表被拆分为"资产"和"负债"两个Sheet时，合并为一个完整的DataFrame。
    """
    asset_df = None
    liab_df = None
    for name, df in sheets.items():
        n = name.strip()
        # 负债Sheet：名称含"负债"或第一行含"资产负债表（续）"
        first_cell = str(df.iloc[0, 0]) if not df.empty else ""
        if "负债" in n or "续" in first_cell:
            liab_df = df
        elif "资产" in n:
            asset_df = df

    if asset_df is not None and liab_df is not None:
        combined = pd.concat([asset_df, liab_df], ignore_index=True)
        return combined
    elif asset_df is not None:
        return asset_df
    return None


def analyze(excel_path: str, output_path: str = None):
    if not os.path.exists(excel_path):
        print(f"[ERROR] 文件不存在：{excel_path}")
        sys.exit(1)

    if output_path is None:
        stem = Path(excel_path).stem
        output_path = str(Path(excel_path).parent / f"{stem}_财务分析报告.md")

    print(f"[INFO] 正在读取文件：{excel_path}")
    sheets = load_excel(excel_path)
    print(f"[INFO] 共检测到 {len(sheets)} 个Sheet：{list(sheets.keys())}")

    # ── 判断是否存在"资产"+"负债"分Sheet格式 ──
    sheet_names = list(sheets.keys())
    has_split_bs = any("资产" in n for n in sheet_names) and any("负债" in n for n in sheet_names)

    if has_split_bs:
        print("[INFO] 检测到资产/负债分Sheet格式，自动合并...")
        bs_raw = merge_balance_sheets(sheets)
        bs_name = "资产+负债(合并)"
    else:
        bs_name, bs_raw = detect_sheet(sheets, "balance")

    inc_name, inc_raw = detect_sheet(sheets, "income")
    cf_name, cf_raw = detect_sheet(sheets, "cashflow")

    print(f"[INFO] 资产负债表：{bs_name}")
    print(f"[INFO] 利润表：{inc_name}")
    print(f"[INFO] 现金流量表：{cf_name}")

    bs_df  = to_data_df(clean_df(bs_raw))  if bs_raw  is not None else pd.DataFrame()
    inc_df = to_data_df(clean_df(inc_raw)) if inc_raw is not None else pd.DataFrame()
    cf_df  = to_data_df(clean_df(cf_raw))  if cf_raw  is not None else pd.DataFrame()

    report_lines = []

    # ── 封面 ──
    filename = Path(excel_path).name
    report_lines.append(f"# 财务报表分析报告\n")
    report_lines.append(f"> 文件：`{filename}`  \n> 生成时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")
    report_lines.append("---\n")

    # ── 一、报表项目增减变动 ──
    report_lines.append("## 一、报表项目增减变动分析\n")
    if not bs_df.empty and len(bs_df.columns) >= 3:
        report_lines.append(build_change_table(bs_df, "资产负债表"))
    else:
        report_lines.append("> ⚠️ 资产负债表数据不足\n\n")

    if not inc_df.empty and len(inc_df.columns) >= 3:
        report_lines.append(build_change_table(inc_df, "利润表"))
    else:
        report_lines.append("> ⚠️ 利润表数据不足\n\n")

    if not cf_df.empty and len(cf_df.columns) >= 3:
        report_lines.append(build_change_table(cf_df, "现金流量表"))
    else:
        report_lines.append("> ⚠️ 现金流量表数据不足\n\n")

    # ── 二、资产结构变动 ──
    report_lines.append("## 二、资产项目结构变动分析\n")
    if not bs_df.empty and len(bs_df.columns) >= 3:
        report_lines.append(build_structure_table(
            bs_df,
            base_keywords=["资产合计", "总资产", "资产总计"],
            title="资产负债表",
            base_label="总资产"
        ))
    else:
        report_lines.append("> ⚠️ 资产负债表数据不足\n\n")

    # ── 三、利润表结构变动 ──
    report_lines.append("## 三、利润表项目结构变动分析\n")
    if not inc_df.empty and len(inc_df.columns) >= 3:
        report_lines.append(build_structure_table(
            inc_df,
            base_keywords=["营业收入", "营业总收入", "收入"],
            title="利润表",
            base_label="营业收入"
        ))
    else:
        report_lines.append("> ⚠️ 利润表数据不足\n\n")

    # ── 四、财务比率 ──
    ratios = calculate_ratios(bs_df, inc_df, cf_df)
    report_lines.append(build_ratio_section(ratios))

    # ── 五、专家分析总结 ──
    report_lines.append(generate_expert_summary(ratios, bs_df, inc_df, cf_df))

    # ── 写出报告 ──
    report_text = "\n".join(report_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n[SUCCESS] 分析报告已生成：{output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    excel_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    analyze(excel_file, out_file)
