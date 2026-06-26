#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TextAnalysis9.py
================

基于 annual_report_extractor 最新提取逻辑的多进程年报 PDF 提取工具。
保留 TextAnalysis9 的多进程输出架构（filelock + 按公司分组目录），
提取逻辑完全复用 annual_report_extractor 的模块化代码。

用法:
    python TextAnalysis9.py input/ output2/
    python TextAnalysis9.py input/ output2/ --workers 4
"""

import argparse
import logging
import os
import re
import sys
import time
import traceback
import unicodedata
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import pandas as pd
import pdfplumber
from filelock import FileLock

logger = logging.getLogger(__name__)

# =============================================================================
# 配置数据 (原 config/items.py)
# =============================================================================

FINANCIAL_ITEMS: Dict[str, dict] = {
    # ---- 资产负债表：流动资产 ----
    "货币资金": {
        "titles": ["货币资金"],
        "next_titles": [
            "交易性金融资产", "衍生金融资产",
            "以公允价值计量且其变动计入当期损益的金融资产",
        ],
        "category": "01_资产负债表附注/01_流动资产",
    },
    "交易性金融资产": {
        "titles": ["交易性金融资产"],
        "next_titles": ["衍生金融资产", "应收票据", "应收票据及应收账款", "应收账款"],
        "category": "01_资产负债表附注/01_流动资产",
    },
    "应收票据": {
        "titles": ["应收票据"],
        "next_titles": ["应收账款", "应收款项融资", "预付款项"],
        "category": "01_资产负债表附注/01_流动资产",
    },
    "应收账款": {
        "titles": ["应收账款"],
        "next_titles": ["应收款项融资", "预付款项", "其他应收款", "应收账款融资"],
        "category": "01_资产负债表附注/01_流动资产",
        "header_keywords": ["账龄"],
        "first_table_only": True,
        "allow_multipage": True,
        "max_pages": 10,
    },
    "存货分类": {
        "titles": ["存货分类"],
        "next_titles": [
            "合同资产", "持有待售资产",
            "一年内到期的非流动资产", "其他流动资产",
            "存货跌价准备",
        ],
        "category": "01_资产负债表附注/01_流动资产",
        "header_keywords": ["期末余额", "期初余额", "账面余额", "账面价值"],
    },
    # ---- 资产负债表：非流动资产 ----
    "固定资产情况": {
        "titles": ["固定资产情况"],
        "next_titles": [
            "在建工程", "生产性生物资产", "油气资产",
            "使用权资产", "无形资产",
            "暂时闲置的固定资产",
        ],
        "category": "01_资产负债表附注/02_非流动资产",
        "header_keywords": ["房屋及建筑物", "机器设备", "账面原值", "期末余额"],
    },
    "在建工程": {
        "titles": ["在建工程"],
        "next_titles": [
            "工程物资", "生产性生物资产", "油气资产",
            "使用权资产", "无形资产", "开发支出",
            "商誉", "长期待摊费用", "递延所得税资产",
        ],
        "category": "01_资产负债表附注/02_非流动资产",
        "header_keywords": ["期末余额", "期初余额", "在建工程"],
    },
    "商誉": {
        "titles": ["商誉账面原值", "商誉的账面原值"],
        "next_titles": [
            "商誉减值", "商誉减值准备", "商誉的减值准备",
            "长期待摊费用", "递延所得税资产", "递延所得税负债",
        ],
        "category": "01_资产负债表附注/02_非流动资产",
        "header_keywords": ["期初余额", "期末余额", "被投资"],
    },
    # ---- 资产负债表：流动负债 ----
    "短期借款分类": {
        "titles": ["短期借款"],
        "next_titles": [
            "交易性金融负债", "衍生金融负债",
            "应付票据", "应付账款",
        ],
        "category": "01_资产负债表附注/03_流动负债",
    },
    "应付职工薪酬列示": {
        "titles": ["应付职工薪酬"],
        "next_titles": [
            "应交税费", "其他应付款", "持有待售负债",
            "一年内到期的非流动负债",
        ],
        "category": "01_资产负债表附注/03_流动负债",
    },
    "短期薪酬列示": {
        "titles": ["短期薪酬列示"],
        "next_titles": ["设定提存计划", "辞退福利", "应交税费", "其他应付款", "离职后福利"],
        "category": "01_资产负债表附注/03_流动负债",
        "require_prefix": False,
        "header_keywords": ["期初余额", "本期增加", "本期减少", "期末余额"],
    },
    "其他流动负债": {
        "titles": ["其他流动负债"],
        "next_titles": ["长期借款", "应付债券", "租赁负债", "长期应付款"],
        "category": "01_资产负债表附注/03_流动负债",
    },
    # ---- 资产负债表：非流动负债 ----
    "长期借款分类": {
        "titles": ["长期借款"],
        "next_titles": [
            "应付债券", "租赁负债", "长期应付款", "长期应付职工薪酬",
        ],
        "category": "01_资产负债表附注/04_非流动负债",
    },
    # ---- 利润表：收入成本 ----
    "营业收入和营业成本情况": {
        "titles": [
            "营业收入和营业成本情况",
            "营业收入和营业成本",
            "营业收入",
        ],
        "next_titles": [
            "营业收入、营业成本的分解信息",
            "营业收入营业成本的分解信息",
            "税金及附加", "销售费用", "管理费用",
        ],
        "category": "02_利润表附注/01_收入成本",
        "header_keywords": ["项目", "本期发生额", "上期发生额"],
    },
    "营业收入、营业成本的分解信息": {
        "titles": [
            "营业收入、营业成本的分解信息",
            "营业收入营业成本的分解信息",
            "营业收入和营业成本的分解信息",
        ],
        "next_titles": ["税金及附加", "销售费用", "管理费用", "履约义务的说明"],
        "category": "02_利润表附注/01_收入成本",
        "header_keywords": ["合同分类", "类别", "收入", "成本"],
    },
    "销售费用": {
        "titles": ["销售费用"],
        "next_titles": ["管理费用", "研发费用", "财务费用"],
        "category": "02_利润表附注/02_期间费用",
    },
    "管理费用": {
        "titles": ["管理费用"],
        "next_titles": ["研发费用", "财务费用", "其他收益"],
        "category": "02_利润表附注/02_期间费用",
    },
    "研发费用": {
        "titles": ["研发费用"],
        "next_titles": ["财务费用", "其他收益", "投资收益"],
        "category": "02_利润表附注/02_期间费用",
    },
    "财务费用": {
        "titles": ["财务费用"],
        "next_titles": ["其他收益", "投资收益", "公允价值变动收益"],
        "category": "02_利润表附注/02_期间费用",
    },
    "其他收益": {
        "titles": ["其他收益"],
        "next_titles": [
            "投资收益", "公允价值变动收益", "信用减值损失", "资产减值损失",
        ],
        "category": "02_利润表附注/03_其他损益",
    },
    "投资收益": {
        "titles": ["投资收益"],
        "next_titles": [
            "公允价值变动收益", "信用减值损失", "资产减值损失",
            "资产处置收益", "营业外收入",
        ],
        "category": "02_利润表附注/03_其他损益",
    },
    "公允价值变动收益": {
        "titles": ["公允价值变动收益"],
        "next_titles": ["信用减值损失", "资产减值损失", "资产处置收益", "营业外收入"],
        "category": "02_利润表附注/03_其他损益",
    },
    "信用减值损失": {
        "titles": ["信用减值损失"],
        "next_titles": ["资产减值损失", "资产处置收益", "营业外收入"],
        "category": "02_利润表附注/03_其他损益",
    },
    "资产处置收益": {
        "titles": ["资产处置收益"],
        "next_titles": ["营业外收入", "营业外支出", "所得税费用"],
        "category": "02_利润表附注/03_其他损益",
    },
    "资产减值损失": {
        "titles": ["资产减值损失"],
        "next_titles": ["信用减值损失", "资产处置收益", "营业外收入"],
        "category": "02_利润表附注/03_其他损益",
    },
    "营业外收入": {
        "titles": ["营业外收入"],
        "next_titles": ["营业外支出", "所得税费用"],
        "category": "02_利润表附注/04_营业外收支",
    },
    "营业外支出": {
        "titles": ["营业外支出"],
        "next_titles": ["所得税费用", "其他综合收益", "现金流量表补充资料"],
        "category": "02_利润表附注/04_营业外收支",
    },
    # ---- 现金流量表 ----
    "收到的其他与经营活动有关的现金": {
        "titles": ["收到的其他与经营活动有关的现金"],
        "next_titles": ["支付的其他与经营活动有关的现金"],
        "category": "03_现金流量表注释/01_经营活动",
        "parent": "与经营活动有关的现金",
        "require_prefix": False,
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "支付的其他与经营活动有关的现金": {
        "titles": ["支付的其他与经营活动有关的现金"],
        "next_titles": [
            "收到的其他与投资活动有关的现金",
            "收到的重要的投资活动有关的现金",
        ],
        "category": "03_现金流量表注释/01_经营活动",
        "parent": "与经营活动有关的现金",
        "require_prefix": False,
        "exclude_suffix": "说明",
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "收到的重要的投资活动有关的现金": {
        "titles": ["收到的重要的投资活动有关的现金"],
        "next_titles": [
            "支付的重要的投资活动有关的现金",
            "支付的其他与投资活动有关的现金",
        ],
        "category": "03_现金流量表注释/02_投资活动",
        "parent": "与投资活动有关的现金",
        "require_prefix": False,
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "支付的重要的投资活动有关的现金": {
        "titles": ["支付的重要的投资活动有关的现金"],
        "next_titles": [
            "收到的其他与投资活动有关的现金",
            "收到的其他与筹资活动有关的现金",
        ],
        "category": "03_现金流量表注释/02_投资活动",
        "parent": "与投资活动有关的现金",
        "require_prefix": False,
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "收到的其他与投资活动有关的现金": {
        "titles": ["收到的其他与投资活动有关的现金"],
        "next_titles": ["支付的其他与投资活动有关的现金"],
        "category": "03_现金流量表注释/02_投资活动",
        "parent": "与投资活动有关的现金",
        "require_prefix": False,
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "支付的其他与投资活动有关的现金": {
        "titles": ["支付的其他与投资活动有关的现金"],
        "next_titles": ["收到的其他与筹资活动有关的现金"],
        "category": "03_现金流量表注释/02_投资活动",
        "parent": "与投资活动有关的现金",
        "require_prefix": False,
        "exclude_suffix": "说明",
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "收到的其他与筹资活动有关的现金": {
        "titles": ["收到的其他与筹资活动有关的现金"],
        "next_titles": ["支付的其他与筹资活动有关的现金"],
        "category": "03_现金流量表注释/03_筹资活动",
        "parent": "与筹资活动有关的现金",
        "require_prefix": False,
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "支付的其他与筹资活动有关的现金": {
        "titles": ["支付的其他与筹资活动有关的现金"],
        "next_titles": ["现金和现金等价物的构成"],
        "category": "03_现金流量表注释/03_筹资活动",
        "parent": "与筹资活动有关的现金",
        "require_prefix": False,
        "exclude_suffix": "说明",
        "header_keywords": ["项目", "金额", "本期", "上期"],
    },
    "现金和现金等价物的构成": {
        "titles": ["现金和现金等价物的构成"],
        "next_titles": [],
        "next_pattern": r"\d{1,3}\s*[、.．]\s*(?:政府补助|所有者权益|股东权益|其他重要事项|现金及现金等价物净变动|所有权或使用权受到限制)",
        "category": "03_现金流量表注释/04_现金构成",
        "require_prefix": False,
        "header_keywords": ["项目", "期末", "期初"],
        "allow_multipage": True,
        "max_pages": 3,
        "first_table_only": True,
    },
}

MANAGEMENT_DISCUSSION_ITEMS: Dict[str, dict] = {
    # ---- 表格类 ----
    "公司前五名客户": {
        "titles": ["公司前五名客户", "公司前5名客户"],
        "next_titles": ["公司前五名供应商", "公司前5名供应商"],
        "category": "11_管理层讨论与分析/05_主要经营情况",
        "extract_type": "table",
        "require_prefix": False,
        "allow_multipage": True,
        "max_pages": 3,
        "header_keywords": ["客户名称", "销售额"],
    },
    "公司前五名供应商": {
        "titles": ["公司前五名供应商", "公司前5名供应商"],
        "next_titles": [],
        "next_pattern": r"^\s*(?:3|三)\s*[、.．]\s*费用|^\s*(?:四|4)\s*[、.．]",
        "category": "11_管理层讨论与分析/05_主要经营情况",
        "extract_type": "table",
        "require_prefix": False,
        "allow_multipage": True,
        "max_pages": 3,
        "header_keywords": ["供应商名称", "采购额"],
    },
    "核心技术及其先进性": {
        "titles": ["核心技术及其先进性"],
        "next_titles": [],
        "next_pattern": r"(?:\d{1,2}|[一二三四五六七八九十]{1,4})\s*[、.]",
        "category": "11_管理层讨论与分析/03_核心竞争力",
        "extract_type": "table",
        "require_prefix": False,
        "allow_multipage": True,
        "header_keywords": ["技术", "先进性", "核心"],
    },
    "在研项目情况": {
        "titles": ["在研项目情况"],
        "next_titles": [],
        "next_pattern": r"^\s*(?:\d{1,2}|[一二三四五六七八九十]{1,4})\s*[、.．]\s*(?:研发人员|知识产权|专利|员工|核心技术|已获得|报告期内获得|研发投入|研究开发)",
        "category": "11_管理层讨论与分析/03_核心竞争力",
        "extract_type": "table",
        "require_prefix": False,
        "allow_multipage": True,
        "header_keywords": ["序号", "项目名称", "预计总投资", "进展", "技术水平"],
    },
    "知识产权列表": {
        "titles": ["报告期内获得的知识产权列表", "知识产权列表"],
        "next_titles": [],
        "next_pattern": r"(?:\d{1,2}|[一二三四五六七八九十]{1,4})\s*[、.]",
        "category": "11_管理层讨论与分析/03_核心竞争力",
        "extract_type": "table",
        "require_prefix": False,
        "allow_multipage": False,
        "header_keywords": ["申请数", "获得数", "专利", "商标"],
    },
    # ---- 文本类 ----
    "经营情况讨论与分析": {
        "titles": ["经营情况讨论与分析", "经营情况的讨论与分析"],
        "next_titles": [],
        "next_pattern": r"(?:三|3)\s*[、.]",
        "category": "11_管理层讨论与分析/02_经营情况",
        "extract_type": "text",
        "require_prefix": True,
    },
    "新技术新产业发展趋势": {
        "titles": [
            "报告期内新技术、新产业、新业态、新模式的发展情况和未来发展趋势",
            "新技术新产业发展趋势",
        ],
        "next_titles": [],
        "next_pattern": r"(?:三|3|四|4)\s*[、.]",
        "category": "11_管理层讨论与分析/01_业务与行业",
        "extract_type": "text",
        "require_prefix": False,
    },
    "核心竞争力分析": {
        "titles": ["核心竞争力分析"],
        "next_titles": [],
        "next_pattern": r"[（(]\s*二\s*[)）]",
        "category": "11_管理层讨论与分析/03_核心竞争力",
        "extract_type": "text",
        "require_prefix": False,
    },
    "风险因素": {
        "titles": ["风险因素"],
        "next_titles": [],
        "next_pattern": r"(?:五|5)\s*[、.]",
        "category": "11_管理层讨论与分析/04_风险因素",
        "extract_type": "text",
        "require_prefix": True,
    },
}


# =============================================================================
# 文本规范化 (原 core/normalizer.py)
# =============================================================================

_ZERO_WIDTH_RE = re.compile(
    r"[ \u2000-\u200f\u2028-\u202e\u2060-\u206f\u3000\ufeff]"
)
_WS_RE = re.compile(r"\s+")


def normalize(text) -> str:
    """
    1. None/非 str 视为空
    2. Unicode NFKC（全角数字/字母/标点 → 半角）
    3. 去零宽/不可见字符（NBSP、ZWSP、BOM 等）
    4. 多空白合并为单个空格
    5. 两端 strip
    """
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = _ZERO_WIDTH_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text)
    return text.strip()


def clean_cell(cell) -> str:
    """清洗表格单元格：去换行/NBSP/前后空白，合并内部连续空白。不做 NFKC，保留原始数值格式。"""
    if cell is None:
        return ""
    s = str(cell).replace("\n", " ").replace("\r", " ").replace("\xa0", " ")
    s = _WS_RE.sub(" ", s)
    return s.strip()


# =============================================================================
# 单位识别与数值换算 (原 core/unit_converter.py)
# =============================================================================

_UNIT_RE = re.compile(r"(?:单位|币种|金额单位)\s*[：:]\s*([^\s\d,，]+)")
_DATE_RE = re.compile(r"\d{4}[-./]\d{1,2}[-./]\d{1,2}")
_YEAR_RE = re.compile(r"^(?:19|20)\d{2}$")


def parse_unit_multiplier(text: str) -> float:
    """从文本中抽取单位倍数。找不到返回 1.0。支持：亿、千万、百万、十万、万、千。"""
    if not text:
        return 1.0
    clean = text.replace(" ", "")
    for bracket in ("（", "）", "(", ")"):
        clean = clean.replace(bracket, "")
    m = _UNIT_RE.search(clean)
    if not m:
        return 1.0
    unit_str = m.group(1)
    if "亿" in unit_str:
        return 1e8
    if "千万" in unit_str:
        return 1e7
    if "百万" in unit_str:
        return 1e6
    if "十万" in unit_str:
        return 1e5
    if "万" in unit_str:
        return 1e4
    if "千" in unit_str:
        return 1e3
    return 1.0


def find_unit_positions(page) -> List[Tuple[float, float]]:
    """返回页面上所有单位标注的 [(y_top, multiplier), ...]，按 y 升序。"""
    found: List[Tuple[float, float]] = []
    try:
        matches = page.search(
            r"(?:单位|币种|金额单位)[：:]\s*[^\s\d,，]+",
            regex=True,
        )
    except Exception:
        return []
    for m in matches or []:
        text = m.get("text", "")
        mult = parse_unit_multiplier(text)
        if mult is not None:
            found.append((float(m.get("top", 0.0)), mult))
    found.sort(key=lambda x: x[0])
    return found


def get_table_multiplier(
    table_y_top: float,
    page_units: List[Tuple[float, float]],
    global_multiplier: float,
) -> float:
    """
    表格与单位关联：
      1. 取 table_y_top 上方最近单位
      2. 无上方单位时取下方第一个（Bug 5 修复）
      3. 仍无则回退 global_multiplier
    """
    above = [u for u in page_units if u[0] <= table_y_top]
    if above:
        return above[-1][1]
    below = [u for u in page_units if u[0] > table_y_top]
    if below:
        return below[0][1]
    return global_multiplier


def convert_cell(val, multiplier: float):
    """单元格数值换算。豁免：百分比/日期/年份/小整数/非数字。"""
    if multiplier == 1.0 or val is None:
        return val
    val_str = str(val).strip()
    if not val_str:
        return val
    # 百分比
    if "%" in val_str:
        return val
    # 日期
    if _DATE_RE.search(val_str):
        return val
    # 纯数字：负号 + 小数 + 千分位
    cleaned = val_str.replace(",", "")
    # 年份（4 位整数，19xx/20xx）
    if _YEAR_RE.match(cleaned):
        return val
    try:
        f = float(cleaned)
    except ValueError:
        return val
    if abs(f) < 50 and f == int(f):
        return val
    new_val = f * multiplier
    return f"{new_val:.2f}"


# =============================================================================
# 标题定位 (原 core/title_locator.py)
# =============================================================================

# 仅汉字数字，不含普通汉字词
_CN_NUM = r"[一二三四五六七八九十百千万零]"

_NUM_PREFIX = (
    r"(?:"
    r"\d{1,3}\s*[、.．]"                                # 65、 32.
    rf"|{_CN_NUM}{{1,6}}\s*[、.．]"                     # 一、 二十一、 六十六、
    rf"|[（(]\s*{_CN_NUM}{{1,6}}\s*[)）]\s*[、.．]?"    # （一） (二十一) (十六).
    rf"|[（(]\s*\d{{1,3}}\s*[)）]\s*[、.．]?"           # (1) （32） (1).
    r")"
)


def build_title_re(
    titles: Sequence[str],
    *,
    require_prefix: bool = True,
    exclude_suffix: Optional[str] = None,
) -> "re.Pattern":
    """
    构建标题匹配正则（不使用 ^/$ 锚定，兼容同行附带其他文字）。

    require_prefix=True 要求编号前缀，用于财报附注大标题，避免正文误匹配。
    exclude_suffix 用于排除特定后缀（如"说明"），避免 "XXX说明" 被误认作 XXX。
    """
    parts: List[str] = []
    for t in titles:
        escaped = re.escape(t)
        if exclude_suffix:
            escaped += rf"(?!{re.escape(exclude_suffix)})"
        parts.append(escaped)
    alts = "|".join(parts)
    if require_prefix:
        return re.compile(rf"{_NUM_PREFIX}\s*(?:{alts})")
    return re.compile(rf"(?:{_NUM_PREFIX}\s*)?(?:{alts})")


def build_boundary_re(
    next_titles: Sequence[str],
    next_pattern: Optional[str] = None,
) -> Optional["re.Pattern"]:
    """下一节边界正则。next_titles 为空时回退到 next_pattern；都无则返回 None。"""
    if next_titles:
        alts = "|".join(re.escape(t) for t in next_titles)
        return re.compile(rf"{_NUM_PREFIX}\s*(?:{alts})")
    if next_pattern:
        return re.compile(next_pattern)
    return None


def find_title_y(
    page, title_text: str, line_idx: Optional[int] = None
) -> Optional[float]:
    """
    三级策略获取 y 坐标：
      1) 词级（extract_words + 行聚合）
      2) 字符级（page.chars，y-band 聚合）
      3) 行号比例估算（line_idx / n_lines * page.height）
    任一级成功即返回，全部失败返回 None（但调用方需用三级兜底保证不 None）。

    line_idx 指示标题命中所在的文本行号，用于筛除同页中更早出现的同名短语
    （如数据行 "1年内到期的长期借款"），避免 y 被拉到错误的上方位置。
    """
    search_clean = title_text.replace(" ", "")

    expected_y: Optional[float] = None
    y_tol: Optional[float] = None
    if line_idx is not None:
        try:
            text = page.extract_text(x_tolerance=1, y_tolerance=1) or ""
            n_lines = max(len(text.split("\n")), 1)
            expected_y = (line_idx / n_lines) * float(page.height)
            y_tol = float(page.height) * 0.20
        except Exception:
            expected_y = None

    def _y_ok(y: float) -> bool:
        if expected_y is None or y_tol is None:
            return True
        return abs(y - expected_y) <= y_tol

    try:
        words = page.extract_words(x_tolerance=5, y_tolerance=3)
        if words:
            for w in words:
                if search_clean in w["text"].replace(" ", "") and _y_ok(w["top"]):
                    return w["top"]
            lines_by_y: Dict[int, list] = defaultdict(list)
            for w in words:
                lines_by_y[round(w["top"] / 4) * 4].append(w)
            for yk in sorted(lines_by_y):
                row_top = lines_by_y[yk][0]["top"]
                if not _y_ok(row_top):
                    continue
                row_text = "".join(
                    w["text"] for w in sorted(lines_by_y[yk], key=lambda w: w["x0"])
                )
                if search_clean in row_text.replace(" ", ""):
                    return row_top
            # 兜底：若 expected_y 约束下找不到，放宽约束回退到原逻辑
            if expected_y is not None:
                for w in words:
                    if search_clean in w["text"].replace(" ", ""):
                        return w["top"]
                for yk in sorted(lines_by_y):
                    row_text = "".join(
                        w["text"] for w in sorted(lines_by_y[yk], key=lambda w: w["x0"])
                    )
                    if search_clean in row_text.replace(" ", ""):
                        return lines_by_y[yk][0]["top"]
    except Exception:
        pass

    try:
        chars = page.chars
        if chars:
            bands: Dict[int, list] = defaultdict(list)
            for c in chars:
                bands[round(c["top"] / 3) * 3].append(c)
            for yk in sorted(bands):
                band_top = bands[yk][0]["top"]
                if not _y_ok(band_top):
                    continue
                band_text = "".join(
                    c["text"] for c in sorted(bands[yk], key=lambda c: c["x0"])
                )
                if search_clean in band_text:
                    return band_top
            if expected_y is not None:
                for yk in sorted(bands):
                    band_text = "".join(
                        c["text"] for c in sorted(bands[yk], key=lambda c: c["x0"])
                    )
                    if search_clean in band_text:
                        return bands[yk][0]["top"]
    except Exception:
        pass

    if expected_y is not None:
        return expected_y

    return None


def should_replace_hit(prev: dict, new_page: int, new_applicability: str) -> bool:
    """
    同名项目重复命中时判定是否替换。

    规则：仅在"旧命中适用性未知、新命中适用性明确"时替换。
    这能把第一次命中在政策章节（未标 √/□）的情形升级到正式表格章节；
    同时避免把后续纯文本引用（页数相差很大）误当作正文而覆盖真正的首次命中。
    """
    prev_app = prev.get("applicability", "未知")
    if prev_app == "未知" and new_applicability != "未知":
        return True
    return False


# =============================================================================
# 文本提取 (原 core/text_extractor.py)
# =============================================================================


def extract_text_under_title(
    pdf,
    pos: dict,
    boundary_re,
    page_texts: Dict[int, List[str]],
    max_pages: int = 30,
    min_line_len: int = 5,
) -> List[str]:
    """
    从 pos["page"] 的 pos["line"] 起向后收集正文行，直到 boundary_re 命中。

    注意：
    - 起始页的 pos["line"] 本身是标题行，不收集；标题之后各行进入收集阶段；
    - 起始页、标题之后行出现的边界也应触发停止（一般正文至少几行）；
    - 跨页时，新页一开始就允许触发边界。
    """
    start_page = pos["page"]
    start_line = pos["line"]
    end_page = min(start_page + max_pages, len(pdf.pages))

    collected: List[str] = []
    found = False
    stop = False

    for pg in range(start_page, end_page):
        if stop:
            break
        lines = page_texts.get(pg, [])
        for li, raw in enumerate(lines):
            if pg == start_page and li < start_line:
                continue
            if pg == start_page and li == start_line:
                found = True
                continue
            if not found:
                # 不可能走到（start_line 严格之前已 continue），防御
                continue
            clean = normalize(raw)
            if boundary_re is not None:
                stripped = clean.lstrip()
                # 仅将"行首命中 + 行长较短"视作小节边界，避免
                # "23.15%" / "19,183.07" 等数字片段误命中 (?:三|3)\s*[、.].
                if stripped and len(stripped) < 60 and boundary_re.match(stripped):
                    stop = True
                    break
            if clean and len(clean) >= min_line_len:
                collected.append(clean)

    return collected


def find_section_start(
    pdf,
    keyword: str,
    max_page: int = 250,
    extract_text_fn=None,
) -> int:
    """
    定位章节首页（排除目录/摘要中的引用）。

    修复 Bug 3：
    - 要求命中行长度 < 40；
    - 排除含"请参见/详见/请查阅/如需了解"等引用词的行；
    - 若全部都被排除则退而求其次，返回首次包含 keyword 的页。
    """
    exclude = re.compile(r"请参见|详见|请查阅|如需了解")
    extract = extract_text_fn or (
        lambda page: page.extract_text(x_tolerance=1, y_tolerance=3) or ""
    )

    fallback: Optional[int] = None
    n = min(max_page, len(pdf.pages))
    for i in range(n):
        page = pdf.pages[i]
        text = extract(page) or ""
        if keyword not in text:
            continue
        for line in text.split("\n"):
            stripped = line.strip()
            if keyword in stripped and len(stripped) < 40 and not exclude.search(stripped):
                return i
        if fallback is None:
            fallback = i
    return fallback if fallback is not None else 0


# =============================================================================
# 表格提取 (原 core/table_extractor.py)
# =============================================================================

TABLE_STRATEGIES: List[dict] = [
    {"vertical_strategy": "lines", "horizontal_strategy": "lines", "snap_tolerance": 3},
    {"vertical_strategy": "lines", "horizontal_strategy": "lines", "snap_tolerance": 7},
    {"vertical_strategy": "text", "horizontal_strategy": "text", "snap_tolerance": 5},
]


def extract_tables_with_fallback(page) -> List[dict]:
    """按策略顺序尝试，返回第一个非空结果；每个元素 {page, y_top, y_bottom, data}。"""
    for strategy in TABLE_STRATEGIES:
        try:
            tobjs = page.find_tables(table_settings=strategy)
        except Exception:
            continue
        out = []
        for t in tobjs or []:
            try:
                data = t.extract()
            except Exception:
                data = None
            if not data:
                continue
            out.append(
                {
                    "page": page.page_number - 1,
                    "y_top": t.bbox[1],
                    "y_bottom": t.bbox[3],
                    "data": data,
                }
            )
        if out:
            return out
    return []


_FILL_BY_KEYWORDS = [
    (("申请数", "获得数"), "专利类型"),
    (("账面", "跌价"), "项目"),
    (("企业合并", "形成"), "被投资单位或事项"),
    (("营业", "收入", "成本"), "合同分类"),
]


def _pick_fill(header_str: str) -> str:
    for keywords, fill in _FILL_BY_KEYWORDS:
        if any(kw in header_str for kw in keywords):
            return fill
    return "项目"


def compress_multilevel_header(table_data):
    """双层表头合并：
      触发条件：第1行含 营业/收入/成本/申请数/获得数/账面/跌价。
      合并方式：top_val 跨列继承，形如 "大类_小类"。
      若数据列数超过表头有效列，按关键词补首列。
    """
    if not table_data or len(table_data) < 2:
        return table_data

    def _flat(v) -> str:
        if v is None:
            return ""
        # 合并单元格内换行：pdfplumber 会把 '企业合\n并形成\n的' 这类保留回行
        return "".join(str(v).split()).strip()

    row0 = [_flat(x) for x in table_data[0]]
    row1 = [_flat(x) for x in table_data[1]]

    trigger = (
        any("营业" in x for x in row1)
        or any("收入" in x for x in row1)
        or any("成本" in x for x in row1)
        or (any("申请数" in x for x in row1) and any("获得数" in x for x in row1))
        or any("账面" in x for x in row1)
        or any("跌价" in x for x in row1)
        or any("企业合并" in x for x in row1)
    )
    if not trigger:
        return table_data

    new_header: List[str] = []
    last_top = ""
    width = max(len(row0), len(row1))
    for k in range(width):
        top = row0[k] if k < len(row0) else ""
        btm = row1[k] if k < len(row1) else ""
        if top == "" and last_top and btm:
            top = last_top
        elif top:
            last_top = top
        if top and btm:
            new_header.append(f"{top}_{btm}")
        elif top:
            new_header.append(top)
        elif btm:
            new_header.append(btm)
        else:
            new_header.append("")

    if len(table_data) > 2:
        max_data_cols = max(
            (
                len([x for x in r if x is not None and str(x).strip()])
                for r in table_data[2:8]
            ),
            default=0,
        )
        actual = [h for h in new_header if h]
        if max_data_cols > len(actual):
            diff = max_data_cols - len(actual)
            fill = _pick_fill("".join(actual))
            new_header = [fill] * diff + actual
        else:
            new_header = actual

    return [new_header] + table_data[2:]


def collect_tables_multipage(
    pdf,
    proj_page: int,
    proj_y: float,
    boundary_re,
    header_keywords: Sequence[str],
    page_texts: Dict[int, List[str]],
    max_pages: int = 30,
    extract_fn: Optional[Callable] = None,
) -> List[dict]:
    """
    从 (proj_page, proj_y) 起向后逐页收集表格。
    使用显式 stop_flag；遇边界先停在当前页之前，避免同页多科目过早中断。

    extract_fn(page) -> List[dict] 注入用于测试；默认 extract_tables_with_fallback。
    """
    if extract_fn is None:
        extract_fn = extract_tables_with_fallback

    result: List[dict] = []
    end = min(proj_page + max_pages, len(pdf.pages))

    for pg in range(proj_page, end):
        page = pdf.pages[pg]

        # 检查边界：仅在"非起始页"时做
        # 匹配必须在行首（lstrip 后位置 0），避免 "V1.0" / "225,375.23" / "CIPS2.0"
        # 等数字内容误判为下一节编号前缀。同时限制行长 < 60 排除表格宽行。
        boundary_y: Optional[float] = None
        if pg > proj_page and boundary_re is not None:
            lines = page_texts.get(pg, [])
            n_lines = max(len(lines), 1)
            for li, raw in enumerate(lines):
                ln = raw.strip()
                if not ln or len(ln) > 60:
                    continue
                if boundary_re.match(ln):
                    boundary_y = (li / n_lines) * float(page.height)
                    break

        tables = extract_fn(page)
        for t in tables:
            if pg == proj_page and t["y_top"] <= proj_y:
                continue
            if boundary_y is not None and t["y_top"] >= boundary_y:
                continue
            if header_keywords and not result:
                hdr = str(t["data"][0]) if t["data"] else ""
                if not any(kw in hdr for kw in header_keywords):
                    continue
            result.append(t)

        if boundary_y is not None:
            break

    return result


def keep_first_logical_table(tables: List[dict]) -> List[dict]:
    """For first_table_only: keep first table + cross-page continuations.

    A continuation is a table on a strictly-later page with the same column count
    whose first row contains numeric data (i.e., not a new header row).
    Stops at the first table that breaks the rule (typically a new sub-table).
    """
    if not tables:
        return tables
    base = tables[0]
    base_data = base.get("data") or []
    if not base_data:
        return [base]
    base_cols = len(base_data[0])
    base_page = base["page"]

    kept = [base]
    last_page = base_page
    for t in tables[1:]:
        if t["page"] <= last_page:
            break
        d = t.get("data") or []
        if not d or len(d[0]) != base_cols:
            break
        first_row = d[0]
        has_num = False
        for c in first_row[1:]:
            s = str(c or "").strip()
            if any(ch.isdigit() for ch in s):
                has_num = True
                break
        if not has_num:
            break
        kept.append(t)
        last_page = t["page"]
    return kept


def collect_tables_singlepage(
    all_tables: List[dict],
    proj_page: int,
    proj_y: float,
    next_page: Optional[int],
    next_y_same_page: Optional[float],
    header_keywords: Sequence[str],
) -> List[dict]:
    """单页模式：只收集 proj_page 页内 y_top 在 (proj_y, next_y_same_page) 区间的表格。

    若同页无表，fallback 到下一页（前提：下一个科目在更后的页）。
    """
    selected: List[dict] = []
    for t in all_tables:
        if t["page"] != proj_page:
            continue
        if t["y_top"] <= proj_y:
            continue
        if next_y_same_page is not None and t["y_top"] >= next_y_same_page:
            continue
        if header_keywords:
            hdr = str(t["data"][0]) if t["data"] else ""
            if not any(kw in hdr for kw in header_keywords):
                continue
        selected.append(t)

    if not selected:
        fallback = proj_page + 1
        if next_page is None or fallback <= next_page:
            for t in all_tables:
                if t["page"] != fallback:
                    continue
                if header_keywords:
                    hdr = str(t["data"][0]) if t["data"] else ""
                    if not any(kw in hdr for kw in header_keywords):
                        continue
                selected.append(t)

    return selected


_REPEAT_HDR_TOKENS = {
    "项目", "本期发生额", "上期发生额", "期末余额", "期初余额",
    "申请数", "获得数", "客户名称", "供应商名称", "序号",
}


def _is_header_continuation(first_row: List[str]) -> bool:
    """判断跨页表第二页首行是否为上页表头的延续（而非数据行）。

    特征：全部非空 cell 均为 ≤2 字符的短字符串，且不含数字/任何 _REPEAT_HDR_TOKENS。
    典型场景：三层 header 的最后一行（如"备"）被切到次页。
    """
    non_empty = [c for c in first_row if c and str(c).strip()]
    if not non_empty:
        return False
    if any(c in _REPEAT_HDR_TOKENS for c in non_empty):
        return False
    for c in non_empty:
        s = str(c).strip()
        if len(s) > 2:
            return False
        if any(ch.isdigit() for ch in s):
            return False
    return True


def merge_tables(tables: List[dict]):
    """将多张 proj_tables 拼成 (header, rows)。首张表抽表头；后续重复表头则跳过。"""
    header: Optional[List[str]] = None
    all_rows: List[list] = []
    for ti, info in enumerate(tables):
        data = info["data"]
        if not data:
            continue
        data = compress_multilevel_header(data)
        if ti == 0:
            header = [clean_cell(c) for c in data[0]]
            rows = data[1:] if len(data) > 1 else []
        else:
            first_row = [clean_cell(c) for c in data[0]]
            if header and _is_header_continuation(first_row):
                # 把延续片段拼回上页 header 对应列
                for k, c in enumerate(first_row):
                    if c and k < len(header):
                        header[k] = (header[k] or "") + c
                rows = data[1:] if len(data) > 1 else []
            else:
                is_repeat = any(h in first_row for h in _REPEAT_HDR_TOKENS)
                rows = data[1:] if is_repeat and len(data) > 1 else data
        for row in rows:
            rd = [clean_cell(c) for c in row]
            if header:
                while len(rd) < len(header):
                    rd.append("")
                rd = rd[: len(header)]
            all_rows.append(rd)
    return header, all_rows


# =============================================================================
# Excel / txt 写入 (原 output/writer.py)
# =============================================================================


def _sanitize_sheet(name: str) -> str:
    cleaned = re.sub(r"[\[\]:*?/\\]", "_", str(name or "").strip())
    return cleaned[:31].strip() or "Sheet1"


def write_df_sheet(df: pd.DataFrame, path: str, sheet_name: str, *, header: bool = True):
    """追加/替换一个 sheet。目标文件若不存在则创建。"""
    sheet = _sanitize_sheet(sheet_name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    mode = "a" if os.path.exists(path) else "w"
    kw: dict = dict(engine="openpyxl", mode=mode)
    if mode == "a":
        kw["if_sheet_exists"] = "replace"
    with pd.ExcelWriter(path, **kw) as w:
        df.to_excel(w, sheet_name=sheet, index=False, header=header)


def write_text(path: str, text: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text or "")


# =============================================================================
# 单 PDF 处理主流程 (原 pipeline/single_pdf.py)
# =============================================================================

_RE_CHECK = r"[√✓☑✔]"
_RE_NOT_APPLICABLE = re.compile(rf"□\s*适用\s*{_RE_CHECK}\s*不适用")
_RE_APPLICABLE = re.compile(rf"{_RE_CHECK}\s*适用\s*□\s*不适用")


def _truncate_at_first_total(df: pd.DataFrame) -> pd.DataFrame:
    """遇到首个"合计"行时截断（保留该行）。避免串到下一科目。

    扫描每一行所有单元格，若 strip 去空格后等于 "合计" 即视为命中。
    找不到则原样返回。
    """
    for i in range(len(df)):
        for val in df.iloc[i].tolist():
            s = str(val).strip().replace(" ", "").replace("　", "")
            if s == "合计":
                return df.iloc[: i + 1].reset_index(drop=True)
    return df


def _clean_index_column(df: pd.DataFrame) -> pd.DataFrame:
    """清理 DataFrame 第一列（项目/类别列）中的空格，并合并重复行。

    对第一列进行以下处理：
    1. 去除所有空格（包括中英文空格）
    2. 去除首尾空白
    3. 如果清理后出现重复行，数值列求和合并
    
    注意：此函数用于处理 PDF 表格提取时同一项目在不同年份
    出现不同空格模式的问题（如"原材 料"和"原材料"）。
    """
    if df.empty or len(df.columns) == 0:
        return df
    
    df = df.copy()
    first_col = df.columns[0]
    
    # 保存原始值用于调试
    orig_values = df[first_col].astype(str).tolist()
    
    # 清理第一列：去除所有空格（中英文空格全部去掉）
    df[first_col] = df[first_col].astype(str).str.replace(r'\s+', '', regex=True).str.strip()
    
    # 识别可合并的行（非空、非"合计"、不以"其中"开头）
    def _is_mergeable(val):
        try:
            s = str(val).strip()
            return bool(s and s != '合计' and not s.startswith('其中'))
        except Exception:
            return False
    
    # 获取可合并行的索引（显式转换为布尔 Series 避免 pandas 误解析）
    mask = df[first_col].map(_is_mergeable).fillna(False).astype(bool)
    mergeable_idx = df[mask].index.tolist()
    
    if len(mergeable_idx) <= 1:
        return df
    
    # 检查可合并行中是否有重复
    mergeable_values = df.loc[mergeable_idx, first_col].tolist()
    seen = set()
    has_dup = False
    for v in mergeable_values:
        if v in seen:
            has_dup = True
            break
        seen.add(v)
    
    if not has_dup:
        return df
    
    # 有重复，需要合并
    mergeable = df.loc[mergeable_idx].copy()
    non_mergeable_idx = [i for i in df.index if i not in mergeable_idx]
    non_mergeable = df.loc[non_mergeable_idx].copy() if non_mergeable_idx else pd.DataFrame(columns=df.columns)
    
    # 对可合并行按第一列分组，数值列求和
    # 判断数值列（不依赖 numpy，使用 pandas 内置方法）
    numeric_cols = []
    for col in mergeable.columns:
        if col == first_col:
            continue
        if pd.api.types.is_numeric_dtype(mergeable[col]):
            numeric_cols.append(col)
    
    agg_dict = {first_col: 'first'}
    for col in numeric_cols:
        agg_dict[col] = 'sum'
    # 非数值列取 first
    for col in mergeable.columns:
        if col not in agg_dict:
            agg_dict[col] = 'first'
    
    merged = mergeable.groupby(first_col, as_index=False).agg(agg_dict)
    
    # 重新组合：合并后的行 + 不可合并行
    result = pd.concat([merged, non_mergeable], ignore_index=True)
    
    # 保持"合计"行在最后
    total_mask = result[first_col] == '合计'
    if total_mask.any():
        non_total = result[~total_mask].copy()
        total_rows = result[total_mask].copy()
        result = pd.concat([non_total, total_rows], ignore_index=True)
    
    return result


def _check_applicability(lines: List[str], start: int, end: int) -> str:
    for i in range(start, min(len(lines), end)):
        ln = normalize(lines[i])
        if _RE_NOT_APPLICABLE.search(ln):
            return "不适用"
        if _RE_APPLICABLE.search(ln):
            return "适用"
    return "未知"


def build_report_context(pdf_path: str) -> Tuple[str, str, str]:
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    parts = stem.split("_")
    return (
        parts[0] if parts else "unknown",
        parts[1] if len(parts) > 1 else "unknown",
        "_".join(parts[2:]) if len(parts) > 2 else stem,
    )


def _safe_name(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", name)[:30]


# ---------------------------------------------------------------------------
# 两阶段扫描
# ---------------------------------------------------------------------------


def _scan_all(
    pdf, items_config: Dict[str, dict], start_page: int
) -> Tuple[Dict[str, dict], List[dict], Dict[int, List[str]], Dict[int, List[Tuple[float, float]]]]:
    """Phase 1：收集标题位置、所有表格、页面文本、页面单位标注。"""
    compiled = {
        name: build_title_re(
            cfg["titles"],
            require_prefix=cfg.get("require_prefix", True),
            exclude_suffix=cfg.get("exclude_suffix"),
        )
        for name, cfg in items_config.items()
    }

    title_positions: Dict[str, dict] = {}
    all_tables: List[dict] = []
    page_texts: Dict[int, List[str]] = {}
    page_units: Dict[int, List[Tuple[float, float]]] = {}

    for page_num in range(start_page, len(pdf.pages)):
        page = pdf.pages[page_num]
        raw_text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
        lines = raw_text.split("\n")
        page_texts[page_num] = lines
        page_units[page_num] = find_unit_positions(page)

        for name, title_re in compiled.items():
            cfg = items_config[name]
            for i, line in enumerate(lines):
                clean = normalize(line)
                if not title_re.search(clean):
                    continue
                # Bug 6: require_prefix=False 的科目额外过滤
                if not cfg.get("require_prefix", True):
                    if len(clean) >= 40 or any(p in clean for p in "。；"):
                        continue
                y = find_title_y(page, cfg["titles"][0], line_idx=i)
                applicability = _check_applicability(lines, i, i + 8)
                new_info = {
                    "page": page_num,
                    "line": i,
                    "y": y,
                    "applicability": applicability,
                }
                if name in title_positions:
                    if should_replace_hit(title_positions[name], page_num, applicability):
                        logger.info(
                            "更新 %s: 第%d页→第%d页 (适用性=%s)",
                            name, title_positions[name]["page"] + 1,
                            page_num + 1, applicability,
                        )
                        title_positions[name] = new_info
                else:
                    title_positions[name] = new_info
                    logger.info(
                        "找到 %s: 第%d页 (适用性=%s)", name, page_num + 1, applicability
                    )
                break

        # 所有表格
        for t in extract_tables_with_fallback(page):
            all_tables.append(t)

    return title_positions, all_tables, page_texts, page_units


# ---------------------------------------------------------------------------
# 按类型提取
# ---------------------------------------------------------------------------


def _collect_tables_with_upper_bound(
    all_tables: List[dict],
    *,
    proj_page: int,
    proj_y: float,
    upper_page: int,
    upper_y_same_page: Optional[float],
    upper_page_min_y: Optional[float],
    header_keywords: List[str],
) -> List[dict]:
    """
    区间式收集：表格必须满足
      - page ∈ [proj_page, upper_page]
      - 同 proj_page：y_top > proj_y 且 y_top < upper_y_same_page（若有）
      - 同 upper_page（≠ proj_page）：y_top < upper_page_min_y（若有）
    header_keywords 非空时，首张表必须含关键词。
    """
    selected: List[dict] = []
    for t in all_tables:
        pg = t["page"]
        if pg < proj_page or pg > upper_page:
            continue
        y = t["y_top"]
        if pg == proj_page:
            if y <= proj_y:
                continue
            if upper_y_same_page is not None and y >= upper_y_same_page:
                continue
        if pg == upper_page and pg != proj_page:
            if upper_page_min_y is not None and y >= upper_page_min_y:
                continue
        if header_keywords and not selected:
            # 多层表头：合并前 3 行参与匹配
            data = t.get("data") or []
            hdr = "|".join(str(row) for row in data[:3])
            if not any(kw in hdr for kw in header_keywords):
                continue
        selected.append(t)

    return selected


def _extract_tables_for_item(
    pdf,
    name: str,
    cfg: dict,
    pos: dict,
    sorted_titles: List,
    idx: int,
    all_tables: List[dict],
    page_texts: Dict[int, List[str]],
    page_units: Dict[int, List[Tuple[float, float]]],
) -> dict:
    proj_page = pos["page"]
    proj_line = pos["line"]
    allow_multipage = cfg.get("allow_multipage", False)
    header_keywords = cfg.get("header_keywords", [])
    boundary_re = build_boundary_re(cfg.get("next_titles", []), cfg.get("next_pattern"))

    # y 回退（Level 3：行号比例）
    proj_y = pos["y"]
    if proj_y is None:
        page = pdf.pages[proj_page]
        n_lines = max(len(page_texts.get(proj_page, [])), 1)
        proj_y = (proj_line / n_lines) * float(page.height)

    # Bug 4：基于全体 sorted_titles 重新计算本科目的区间上界
    # - upper_y_same_page: 同页内 y > proj_y 的最小 y
    # - upper_page:        最早的、在更后页上的其它科目所在页
    # - upper_y_cross_page: upper_page 上其它科目的最小 y（限制该页可收集范围）
    same_page_ys: List[float] = []
    later_pages: List[int] = []
    for nm, p in sorted_titles:
        if nm == name:
            continue
        py = p.get("y")
        if p["page"] == proj_page and py is not None and py > proj_y:
            same_page_ys.append(py)
        elif p["page"] > proj_page:
            later_pages.append(p["page"])
    upper_y_same_page = min(same_page_ys) if same_page_ys else None
    # 保守策略：若同页后续有科目，只扫本页；若无同页后续，取最早的后续科目所在页；
    # 若全文无后续科目（target 过滤极端情况），仅扫本页，避免一路收到页末。
    if upper_y_same_page is not None:
        upper_page = proj_page
    elif later_pages:
        upper_page = min(later_pages)
    else:
        upper_page = proj_page

    # 确定 upper_page 上的最小 y（进入该页后的 y 上界）
    upper_page_min_y: Optional[float] = None
    if upper_page > proj_page:
        same_up = [
            p.get("y") for nm, p in sorted_titles
            if nm != name and p["page"] == upper_page and p.get("y") is not None
        ]
        if same_up:
            upper_page_min_y = min(same_up)

    if allow_multipage:
        proj_tables = collect_tables_multipage(
            pdf, proj_page, proj_y, boundary_re, header_keywords, page_texts,
            max_pages=cfg.get("max_pages", 30),
        )
    else:
        proj_tables = _collect_tables_with_upper_bound(
            all_tables,
            proj_page=proj_page,
            proj_y=proj_y,
            upper_page=upper_page,
            upper_y_same_page=upper_y_same_page,
            upper_page_min_y=upper_page_min_y,
            header_keywords=header_keywords,
        )

    if cfg.get("first_table_only") and proj_tables:
        proj_tables = keep_first_logical_table(proj_tables)

    if not proj_tables:
        return {
            "name": name,
            "status": "无表格",
            "category": cfg["category"],
            "parent": cfg.get("parent"),
        }

    # 应用单位换算（每张表独立判定）
    global_mult = 1.0
    for t in proj_tables:
        units = page_units.get(t["page"], [])
        mult = get_table_multiplier(t["y_top"], units, global_mult)
        t["multiplier"] = mult
        global_mult = mult

    header, all_rows = merge_tables(proj_tables)
    if not all_rows:
        return {
            "name": name,
            "status": "空表格",
            "category": cfg["category"],
            "parent": cfg.get("parent"),
        }

    # 按表为单位换算数值（按行所属的原始表）
    converted_rows: List[list] = []
    row_cursor = 0
    for ti, t_info in enumerate(proj_tables):
        data = t_info["data"]
        mult = t_info.get("multiplier", 1.0)
        rows_this = (
            len(data) - 1 if ti == 0 and data else max(len(data) - 1, 0)
        )
        if ti > 0:
            first_row = [clean_cell(c) for c in data[0]]
            is_repeat = any(
                h in first_row
                for h in ("项目", "本期发生额", "上期发生额", "期末余额", "期初余额")
            )
            rows_this = len(data) - 1 if is_repeat else len(data)
        end = row_cursor + rows_this
        segment = all_rows[row_cursor:end]
        for row in segment:
            if mult != 1.0:
                row = [convert_cell(c, mult) if i > 0 else c for i, c in enumerate(row)]
            converted_rows.append(row)
        row_cursor = end
    if row_cursor < len(all_rows):
        converted_rows.extend(all_rows[row_cursor:])

    df = pd.DataFrame(converted_rows, columns=header)
    df = _truncate_at_first_total(df)
    df = _clean_index_column(df)
    return {
        "name": name,
        "parent": cfg.get("parent"),
        "status": "成功",
        "category": cfg["category"],
        "rows": len(df),
        "tables": len(proj_tables),
        "data": df,
    }


def _extract_text_for_item(
    pdf, name: str, cfg: dict, pos: dict, page_texts: Dict[int, List[str]]
) -> dict:
    boundary = build_boundary_re(cfg.get("next_titles", []), cfg.get("next_pattern"))
    collected = extract_text_under_title(pdf, pos, boundary, page_texts)
    if collected:
        return {
            "name": name,
            "status": "成功",
            "category": cfg["category"],
            "parent": cfg.get("parent"),
            "extract_type": "text",
            "lines": len(collected),
            "text": "\n".join(collected),
        }
    return {
        "name": name,
        "status": "无内容",
        "category": cfg["category"],
        "parent": cfg.get("parent"),
        "extract_type": "text",
    }


# ---------------------------------------------------------------------------
# 统一提取入口
# ---------------------------------------------------------------------------


def extract_all_items(
    pdf, items_config: Dict[str, dict], start_page: int
) -> List[dict]:
    title_positions, all_tables, page_texts, page_units = _scan_all(
        pdf, items_config, start_page
    )

    sorted_titles = sorted(
        title_positions.items(),
        key=lambda x: (x[1]["page"], x[1]["y"] if x[1]["y"] is not None else 0),
    )

    results: List[dict] = []
    for idx, (name, pos) in enumerate(sorted_titles):
        cfg = items_config[name]
        extract_type = cfg.get("extract_type", "table")

        if pos["applicability"] == "不适用":
            results.append({
                "name": name,
                "status": "不适用",
                "category": cfg["category"],
                "parent": cfg.get("parent"),
                "extract_type": extract_type,
            })
            continue

        if extract_type == "text":
            results.append(_extract_text_for_item(pdf, name, cfg, pos, page_texts))
            continue

        results.append(
            _extract_tables_for_item(
                pdf, name, cfg, pos, sorted_titles, idx, all_tables, page_texts, page_units
            )
        )

    for name in items_config:
        if name not in title_positions:
            cfg = items_config[name]
            results.append({
                "name": name,
                "status": "未匹配",
                "category": cfg["category"],
                "parent": cfg.get("parent"),
                "extract_type": cfg.get("extract_type", "table"),
            })

    return results


# ---------------------------------------------------------------------------
# 单 PDF 处理
# ---------------------------------------------------------------------------


def process_pdf(
    pdf_path: str,
    output_dir: str,
    *,
    target_items: Optional[List[str]] = None,
    text_sections: Optional[List[str]] = None,
) -> List[dict]:
    """
    处理单个 PDF 文件。

    target_items: 仅提取指定的财务科目名（None 表全部）
    text_sections: 仅提取指定的管理层讨论科目名（None 表全部）
    """
    company_code, company_name, report_label = build_report_context(pdf_path)

    logger.info("=" * 60)
    logger.info("处理: %s %s", company_code, company_name)
    logger.info("=" * 60)

    # 新输出布局：以 {代码}_{公司名} 作为顶层公司文件夹
    company_root = os.path.join(output_dir, f"{company_code}_{company_name}")
    os.makedirs(company_root, exist_ok=True)
    all_results: List[dict] = []

    with pdfplumber.open(pdf_path) as pdf:
        # ===== 财务报表附注 =====
        fin_cfg = FINANCIAL_ITEMS
        if target_items is not None:
            fin_cfg = {k: v for k, v in fin_cfg.items() if k in target_items}
        if fin_cfg:
            start_page = find_section_start(pdf, "财务报表项目注释")
            if start_page == 0:
                start_page = find_section_start(pdf, "合并财务报表项目注释")
            logger.info("财务报表项目注释起始页: 第 %d 页", start_page + 1)
            all_results.extend(extract_all_items(pdf, fin_cfg, start_page))

        # ===== 管理层讨论与分析 =====
        md_cfg = MANAGEMENT_DISCUSSION_ITEMS
        if text_sections is not None:
            md_cfg = {k: v for k, v in md_cfg.items() if k in text_sections}
        if md_cfg:
            md_start = find_section_start(pdf, "管理层讨论与分析", max_page=60)
            logger.info("管理层讨论与分析起始页: 第 %d 页", md_start + 1)
            all_results.extend(extract_all_items(pdf, md_cfg, md_start))

        # ===== 写文件 =====
        for r in all_results:
            if r.get("status") != "成功":
                continue
            cat_dir = os.path.join(company_root, r["category"])
            os.makedirs(cat_dir, exist_ok=True)
            safe = _safe_name(r["name"])
            if r.get("extract_type") == "text":
                filename = f"{safe}_{company_name}_{report_label}.txt"
                filepath = os.path.join(cat_dir, filename)
                write_text(filepath, r.get("text", ""))
                r["file"] = filepath
            elif "data" in r:
                # 按 batch 模式：写 Temp.xlsx；batch 结尾会合并
                # 文件名包含年份标识，避免不同年份 PDF 覆盖同名文件
                filename = f"{safe}_{company_name}_{report_label}_Temp.xlsx"
                filepath = os.path.join(cat_dir, filename)
                write_df_sheet(r["data"], filepath, _sanitize_sheet(report_label))
                r["file"] = filepath

        # ===== 汇总表 =====
        summary = [
            {
                "项目名称": r["name"],
                "父项目": r.get("parent", ""),
                "类别": r.get("category", ""),
                "状态": r["status"],
                "提取类型": r.get("extract_type", "table"),
                "行数": r.get("rows", r.get("lines", 0)),
                "表格数": r.get("tables", 0),
                "输出文件": r.get("file", ""),
            }
            for r in all_results
        ]
        summary_path = os.path.join(company_root, f"_汇总表_{company_name}.xlsx")
        write_df_sheet(
            pd.DataFrame(summary), summary_path, _sanitize_sheet(report_label)
        )

    return all_results


# =============================================================================
# 批量辅助函数 (原 pipeline/batch.py 中抽取)
# =============================================================================


def _collect_pdfs(input_dir: str) -> List[str]:
    out = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                out.append(os.path.join(root, f))
    return sorted(out)


def merge_by_company(output_dir: str, selected_items: Optional[List[str]] = None):
    """合并 *_Temp.xlsx 为多 Sheet 的单一 xlsx（按 公司名/科目 分组），然后删除 Temp。

    新文件名格式: {item}_{company}_{report_label}_Temp.xlsx
    同一 (item, company) 的所有 Temp 文件被合并为一个最终 xlsx，
    包含所有年份的 sheet。
    """
    # 匹配 item_company_report_Temp.xlsx（report_label 含年报等字样）
    temp_re = re.compile(r"^(?P<item>.+?)_(?P<company>.+?)_(?P<report>.+?)_Temp\.xlsx$")

    # 收集所有 Temp 文件并按 (item, company) 分组
    grouped: Dict[Tuple[str, str, str], List[str]] = {}
    for root, _, files in os.walk(output_dir):
        for f in files:
            if not f.endswith("_Temp.xlsx"):
                continue
            m = temp_re.match(f)
            if not m:
                continue
            item = m.group("item")
            company = m.group("company")
            report = m.group("report")
            if selected_items is not None and item not in selected_items:
                continue
            key = (root, item, company)
            temp_path = os.path.join(root, f)
            grouped.setdefault(key, []).append(temp_path)

    # 逐组合并
    for (root, item, company), temp_paths in grouped.items():
        final_path = os.path.join(root, f"{item}_{company}.xlsx")

        # 读取所有 Temp 文件的所有 sheet
        all_sheets: Dict[str, pd.DataFrame] = {}
        for temp_path in temp_paths:
            try:
                sheets = pd.read_excel(temp_path, sheet_name=None)
            except Exception as e:
                logger.warning("读取 %s 失败: %s", temp_path, e)
                continue
            for sheet, df in sheets.items():
                sheet = str(sheet)[:31]
                if sheet in all_sheets:
                    # 同名 sheet（理论上不应出现，因不同年份 sheet 名不同）
                    logger.warning("Sheet %s 重复，保留后读入的版本", sheet)
                all_sheets[sheet] = df

        if not all_sheets:
            continue

        # 写入最终文件（覆盖模式，确保所有 sheet 完整）
        try:
            with pd.ExcelWriter(final_path, engine="openpyxl", mode="w") as w:
                for sheet, df in all_sheets.items():
                    df.to_excel(w, sheet_name=sheet[:31], index=False)
        except Exception as e:
            logger.warning("写入 %s 失败: %s", final_path, e)
            continue

        # 删除所有 Temp 文件
        for temp_path in temp_paths:
            try:
                os.remove(temp_path)
            except OSError:
                pass


# =============================================================================
# TextAnalysis9 多进程主控
# =============================================================================

BATCH_SIZE = 500


# ---------------------------------------------------------------------------
# 多进程安全写入（monkey-patch）
# ---------------------------------------------------------------------------

_orig_write_df_sheet = write_df_sheet


def _write_df_sheet_locked(df, path, sheet_name, *, header=True):
    """带 filelock 的 write_df_sheet，防止多进程并发写入同一文件冲突。"""
    lock_path = path + ".lock"
    lock = FileLock(lock_path, timeout=60)
    try:
        with lock:
            _orig_write_df_sheet(df, path, sheet_name, header=header)
    finally:
        try:
            if os.path.exists(lock_path):
                os.remove(lock_path)
        except OSError:
            pass


def _patch_writer():
    """在子进程中打补丁，确保多进程并发写入安全。"""
    global write_df_sheet
    write_df_sheet = _write_df_sheet_locked


def _process_one(args):
    pdf_path, output_dir, target_items, text_sections = args
    # 在子进程中打补丁，确保多进程并发写入安全
    _patch_writer()
    try:
        process_pdf(
            pdf_path,
            output_dir,
            target_items=target_items,
            text_sections=text_sections,
        )
        return (pdf_path, None)
    except Exception as e:
        err = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
        return (pdf_path, err)


# ---------------------------------------------------------------------------
# 批量运行
# ---------------------------------------------------------------------------


def run(
    input_dir: str,
    output_dir: str,
    *,
    max_workers: Optional[int] = None,
    target_items: Optional[List[str]] = None,
    text_sections: Optional[List[str]] = None,
) -> Dict[str, str]:
    """批量处理。返回失败映射 {pdf_path: error_msg}。"""
    os.makedirs(output_dir, exist_ok=True)
    pdfs = _collect_pdfs(input_dir)
    if not pdfs:
        logger.warning("未找到 PDF 文件")
        return {}

    if max_workers is None:
        import multiprocessing

        max_workers = max(1, min(multiprocessing.cpu_count() - 1, 4))

    failed: Dict[str, str] = {}
    t0 = time.time()

    for bi in range(0, len(pdfs), BATCH_SIZE):
        batch = pdfs[bi : bi + BATCH_SIZE]
        logger.info("批次 %d: %d 个文件", bi // BATCH_SIZE + 1, len(batch))

        with ProcessPoolExecutor(
            max_workers=max_workers,
            max_tasks_per_child=1,  # 每个 worker 处理 1 个任务后退出，防止内存泄漏导致 OOM
        ) as pool:
            futures = {
                pool.submit(_process_one, (p, output_dir, target_items, text_sections)): p
                for p in batch
            }
            for fut in as_completed(futures):
                path = futures[fut]
                try:
                    _, err = fut.result()
                except Exception as e:
                    err = f"{type(e).__name__}: {e}"
                if err:
                    failed[path] = err
                    logger.warning("失败: %s -> %s", path, err)
                else:
                    logger.info("完成: %s", path)

    # 跨期合并：将 *_Temp.xlsx 合并为按科目分组的多 Sheet xlsx
    merge_by_company(output_dir, target_items)

    logger.info(
        "批量完成 %d/%d，用时 %.1fs",
        len(pdfs) - len(failed),
        len(pdfs),
        time.time() - t0,
    )
    return failed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_list(val):
    if val is None:
        return None
    return [x.strip() for x in val.split(",") if x.strip()]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="TextAnalysis9 - 基于 annual_report_extractor 的多进程年报提取"
    )
    parser.add_argument("input", help="PDF 文件或目录")
    parser.add_argument(
        "output", nargs="?", default="output2", help="输出目录（默认 output2）"
    )
    parser.add_argument(
        "--workers", type=int, default=None, help="并行进程数（默认 CPU-1，上限4）"
    )
    parser.add_argument("--items", type=str, help="仅提取指定科目，逗号分隔")
    parser.add_argument("--text-sections", type=str, help="仅提取指定文本章节，逗号分隔")
    args = parser.parse_args(argv)

    items = _parse_list(args.items)
    texts = _parse_list(args.text_sections)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    failed = run(
        args.input,
        args.output,
        max_workers=args.workers,
        target_items=items,
        text_sections=texts,
    )
    if failed:
        print(f"\n失败 {len(failed)} 个文件:")
        for p, e in failed.items():
            print(f"  {os.path.basename(p)}: {e[:200]}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
