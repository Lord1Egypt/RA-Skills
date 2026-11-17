#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""金融理论大师 —— 数据集模式定义（单一来源）。

所有数据集的字段名与枚举取值都在本文件定义一次，其余脚本一律 `import schema`
引用，不再各自重抄。改动枚举只改这里一处。

改枚举的流程（替代旧版「同时改两个文件」的约定）：
    1. 改本文件的 ENUM_* 常量
    2. 改 gen_data.py 里对应的 RECORDS 数据
    3. 运行 python scripts/gen_data.py 重新生成
    4. 运行 python scripts/validate_data.py 确认通过
    5. 更新 data/README.md 的枚举清单，保持文档与代码一致

为什么单独一个模块：字段名和枚举原本在 gen_data.py、validate_data.py、
theory_lookup.py 三处各写一遍（共 24 处重复声明）。任何一次只改其中一处，
校验器与生成器就会对不上——这正是 data/README.md 第九节特意警告过的坑。
收敛到单一来源后，这个坑从「靠纪律避免」变成「结构上不可能发生」。
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REF_DIR = ROOT / "references"

PATH_THEORY = DATA_DIR / "theory_index.csv"
PATH_TIMELINE = DATA_DIR / "financial_history_timeline.csv"
PATH_POLICY = DATA_DIR / "policy_toolkit.csv"
PATH_CASES = DATA_DIR / "investor_cases.csv"

# ---------------------------------------------------------------------------
# 枚举取值
# ---------------------------------------------------------------------------

# theory_index.csv
ENUM_MODULE = ["资产定价", "投资组合", "有效市场", "行为金融", "公司金融", "货币宏观", "风险管理"]
ENUM_STRENGTH = ["框架级", "极强", "强", "中", "低"]
ENUM_STATUS = ["稳健", "有争议", "已削弱"]

# financial_history_timeline.csv
ENUM_STAGE = ["起源", "古典与中世纪", "商业革命", "金融革命", "金本位与央行时代", "美元本位与全球化"]
ENUM_HCATEGORY = ["货币", "信用与银行", "市场与机构", "危机", "监管与制度", "国际体系", "技术与工具"]

# policy_toolkit.csv
ENUM_MARKET_STAGE = ["通用", "牛市", "熊市", "震荡市", "危机行情"]
ENUM_POLICY_LEVEL = ["货币政策", "财政政策", "微观与市场政策"]

# investor_cases.csv —— 案例不适用「通用」，只用四类真实行情
ENUM_CASE_STAGE = ["牛市", "熊市", "震荡市", "危机行情"]

# investor_cases.csv 的 pattern 取值，必须与 references/14 的七种模式一致
ENUM_PATTERN = [
    "政策不可持续模式",
    "资产负债表错配模式",
    "融资结构模式",
    "极端估值模式",
    "央行承诺模式",
    "制度变革模式",
    "催化剂与时点模式",
]

# ---------------------------------------------------------------------------
# 字段列表（顺序即 CSV 列顺序，不可随意调整）
# ---------------------------------------------------------------------------

FIELDS_THEORY = [
    "theory_id", "name_cn", "abbrev", "proposer", "year", "module",
    "core_claim", "core_assumption", "applicable_scene", "main_limitation",
    "hypothesis_strength", "evidence_status", "evidence_note",
    "complementary", "conflicting", "key_reference",
]

# 允许为空的字段（其余为必填）
OPTIONAL_THEORY = {"evidence_note"}

FIELDS_TIMELINE = [
    "sort_key", "year", "event", "stage", "category",
    "region", "significance", "related_theory",
]

FIELDS_POLICY = [
    "tool_id", "market_stage", "level", "tool_name",
    "target", "mechanism", "lag", "constraint", "case_example",
]

FIELDS_CASES = [
    "case_id", "period", "region", "market_stage", "policy_env",
    "signal", "reasoning", "decision", "outcome", "pattern", "survivorship",
]

# 各数据集的唯一标识字段，校验器据此查重与报错定位
ID_FIELD = {
    PATH_THEORY: "theory_id",
    PATH_TIMELINE: "year",
    PATH_POLICY: "tool_id",
    PATH_CASES: "case_id",
}

# 校验时字段名 → 允许枚举的映射（值为 None 表示该字段不做枚举校验）
FIELD_ENUM = {
    "module": ENUM_MODULE,
    "hypothesis_strength": ENUM_STRENGTH,
    "evidence_status": ENUM_STATUS,
    "stage": ENUM_STAGE,
    "category": ENUM_HCATEGORY,
    "market_stage": ENUM_MARKET_STAGE,
    "level": ENUM_POLICY_LEVEL,
}

# ---------------------------------------------------------------------------
# 取值语义
# ---------------------------------------------------------------------------

# 显式的「不适用 / 无」标记。这是有意义的值，不算缺失。
NOT_APPLICABLE = frozenset({"—", "-"})

# 知识正文文件清单。新增模块时在此追加。
EXPECTED_REFS = [
    "01-资产定价理论.md",
    "02-投资组合理论.md",
    "03-有效市场假说与市场异象.md",
    "04-行为金融学.md",
    "05-公司金融.md",
    "06-货币与宏观金融.md",
    "07-风险管理.md",
    "08-理论对比矩阵.md",
    "09-理论谱系与思想史.md",
    "10-世界金融史（上）起源到金本位.md",
    "11-世界金融史（下）布雷顿森林到数字金融.md",
    "12-金融史脉络对照与索引.md",
    "13-行情类型与政策工具箱.md",
    "14-投资案例与判断逻辑.md",
    "15-非西方金融史与政策实践.md",
]

# 理论索引的关键词检索字段，按相关性排序（越靠前权重越高）
SEARCH_FIELDS = [
    "name_cn",
    "abbrev",
    "core_claim",
    "main_limitation",
    "applicable_scene",
    "core_assumption",
    "proposer",
    "complementary",
    "conflicting",
    "key_reference",
    "evidence_note",
]

# 查询工具简要表的列（控制在 6 列以内，便于阅读）
BRIEF_COLS = ["theory_id", "name_cn", "year", "module", "hypothesis_strength", "evidence_status"]

# 查询工具详细视图的字段顺序与中文标签
DETAIL_LABELS = [
    ("theory_id", "标识"),
    ("name_cn", "中文名称"),
    ("abbrev", "英文缩写"),
    ("proposer", "提出者"),
    ("year", "年份"),
    ("module", "所属板块"),
    ("core_claim", "核心命题"),
    ("core_assumption", "核心假设"),
    ("applicable_scene", "适用场景"),
    ("main_limitation", "主要局限"),
    ("hypothesis_strength", "假设强度"),
    ("evidence_status", "实证地位"),
    ("evidence_note", "补充说明"),
    ("complementary", "互补理论"),
    ("conflicting", "冲突理论"),
    ("key_reference", "关键文献"),
]
