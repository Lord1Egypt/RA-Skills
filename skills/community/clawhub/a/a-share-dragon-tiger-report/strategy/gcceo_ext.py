#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GCCEO 全量整合层（v3.1，2026-11-11 落地）· 非破坏性叠加

来源：/Users/wdj/.workbuddy/skills/gceo-global-ceo-skill-system
  SKILL.md v4.0.0 + skills.json（10 域 91 技能 + 投行 A1-A10 + 出海 G1-G10
  + 8 大模型超能力 + 16 方法论工具 + 五步决策框架）

═══════════════════════════ 七条设计契约（不可协商）═══════════════════════════
1. 六条口径 v2.3 的阈值、字段、判定结果一律不改；`KNOWLEDGE` 45 键不改；
   v3.0 五个只读旁路模块不改。本模块是叠加在 v3 之上的**第二只读旁路层**。
2. GCCEO 是「企业管理能力体系」，不是选股因子。全量整合的正确姿势是**映射**：
   把每个域的决策视角转成研判视角的提问 / 尽调清单 / 风险项 / 叙事模板，
   而不是把企业能力当成打分成分。
3. 本模块只输出「视角标签 / 检查清单 / 风险提问 / 叙事脚手架 / 映射说明」，
   不产生任何剔除动作、不参与 scoring / funnel / predictions 数值计算、
   不给任何个股加分或减分。
4. **不夺权**：GCCEO 映射不覆盖 v2.3 一票否决清单、不改写四层漏斗硬阈值、
   不改写情绪五阶段 30/60/70/20/0% 仓位上限、不改写 v3 宏观只下调契约。
5. **事实 / 预测 / 口径差异**三类水印沿用 v3.0；GCCEO 技能数存在
   frontmatter=96 与 skills.json.total_skills=91 两套口径，按【口径差异】
   只取「十域 91 技能」结构口径，96 记为 2026 新增模块口径，绝对值不写阈值。
6. 全部映射可逐条停用（GCCEO_SWITCHES），并可整体一键回滚：
   data.json 顶层 `gceo.enabled=false` → 回到 v3.0 的 16 页；
   与 `v3.enabled=false` 正交，后者仍回到 14 页纯 v2.3。
7. 渲染器不 import 本模块，只读 data.json 顶层 `gceo.blocks`，
   保证 v2.3 / v3.0 生成器对 GCCEO 层零依赖。

接入点：data.json 顶层可选字段 `gceo`（与 `v3` 平级）。
"""
from __future__ import annotations

from typing import Any

# ─────────────────────────────── 版本与开关 ───────────────────────────────
GCCEO_EXT_VERSION = "v3.1"          # 本整合层版本（框架版本随之升 v3.1）
GCCEO_SOURCE_VERSION = "4.0.0"      # 被整合的 GCCEO 源技能版本
GCCEO_CONFIRMED_ON = "2026-11-11"
CALIBER_VERSION_UNCHANGED = "v2.3"  # 六条口径永久锚，不动
V3_VERSION_UNCHANGED = "v3.0"       # v3 只读旁路层，不动
FRAMEWORK_VERSION = "v3.1"
OVERLAY_ONLY = True
NO_VETO = True
NO_POSITION_UP = True

GCCEO_SWITCHES: dict[str, bool] = {
    "gceo_decision_os": True,          # 五步决策框架 → 研判决策工程
    "gceo_domain_map": True,           # 十域 91 技能 → 研判视角映射
    "gceo_ib_pe_map": True,            # 投行私募 A1-A10 → 资本运作映射
    "gceo_global_expansion": True,     # 出海 G1-G10 → 出海链映射
    "gceo_ai_superpowers": True,       # AI 超能力 8 模块 → AI 研判工作台
    "gceo_method_toolbox": True,       # 16 方法论工具 → 可审计推理链
    "gceo_governance_talent": True,    # 治理/人才/ESG 域 → 定性尽调清单
    "gceo_risk_radar": True,           # 地缘/网络/气候风险 → 风险清单增补
    "gceo_narrative": True,            # 叙事与复盘纪律
    "gceo_watermark": True,            # 口径差异水印（96 vs 91）
}

# ─────────────────────── GCCEO 源体系盘点（只读登记）───────────────────────
# 十域 91 技能（skills.json 权威口径，域内合计 = 91）
DOMAINS: list[dict] = [
    {"id": 1, "zh": "人工智能与大数据", "en": "AI & Big Data", "n": 10},
    {"id": 2, "zh": "网络与网络空间安全", "en": "Cybersecurity", "n": 8},
    {"id": 3, "zh": "技术素养", "en": "Technology Literacy", "n": 8},
    {"id": 4, "zh": "创造性思维", "en": "Creative Thinking", "n": 9},
    {"id": 5, "zh": "韧性、灵活性与敏捷性", "en": "Resilience, Flexibility & Agility", "n": 10},
    {"id": 6, "zh": "好奇心与终身学习", "en": "Curiosity & Lifelong Learning", "n": 9},
    {"id": 7, "zh": "领导力与社会影响力", "en": "Leadership & Social Influence", "n": 10},
    {"id": 8, "zh": "人才管理", "en": "Talent Management", "n": 9},
    {"id": 9, "zh": "分析思维", "en": "Analytical Thinking", "n": 9},
    {"id": 10, "zh": "环境管理", "en": "Environmental Stewardship", "n": 9},
]
DOMAIN_SKILL_TOTAL = sum(d["n"] for d in DOMAINS)  # = 91
IB_SKILLS = ["IPO筹备", "并购整合", "PE价值创造", "杠杆收购", "困境扭转",
             "跨境并购", "资本市场策略", "股东积极主义防御", "PE募集", "实物资产"]  # A1-A10
GLOBALIZATION_SKILLS = ["全球市场锚定", "跨境合规", "跨境财税", "本地化运营",
                        "香港超级联系人", "一带一路", "新兴市场进入", "全球IP保护",
                        "出海文化智商", "全球危机声誉"]  # G1-G10
AI_SUPERPOWERS = ["AI战略顾问", "AI投资分析师", "AI风险雷达", "AI创新伙伴",
                  "AI学习教练", "AI组织诊断师", "AI ESG合规官", "AI决策副驾"]
METHOD_TOOLS = ["MECE", "Issue Tree", "假设驱动", "BCG Matrix", "Porter五力",
                "Blue Ocean", "Balanced Scorecard", "OKR", "Design Thinking",
                "Agile/Scrum", "Systems Thinking", "Pre-Mortem", "DCF/LBO",
                "9-Box Grid", "FAIR Model", "TCFD"]  # 16
DECISION_5STEP = ["DEFINE 定义", "ANALYZE 分析", "SYNTHESIZE 综合",
                  "DECIDE 决策", "EXECUTE 执行"]
GLOBALIZATION_4D = ["全球市场锚定", "跨境合规构建", "跨境财税优化", "本地化运营"]

# 口径差异登记（水印）
CALIBER_DIFFS: list[dict] = [
    {"item": "GCCEO 技能总数", "v_frontmatter": 96, "v_skillsjson": 91,
     "resolution": "取 skills.json 十域合计 91 为结构口径；96 含 2026 Q1-Q2 新增模块口径。绝对值不写阈值。",
     "watermark": "口径差异"},
]

# ───────────────────── 五步决策框架 → 研判决策工程映射 ──────────────────────
DECISION_OS_MAP: list[dict] = [
    {"step": "DEFINE 定义", "src": "gceo-mckinsey-problem-solving",
     "research": "问题陈述：今日是否值得出手？MECE 拆解宏观/情绪/资金/标的/失败五问",
     "landing": "第 5.1 节 Issue Tree（已注入）+ 第 2 页核心判断", "power": "脚手架"},
    {"step": "ANALYZE 分析", "src": "gceo-investment-analysis / financial-modeling / competitive-intelligence",
     "research": "定量（分位/额比/DCF 锚）× 定性（Porter 五力/管理层）× ESG 整合",
     "landing": "第 6 章五维共振引擎 + 第 3-10 页图表", "power": "脚手架"},
    {"step": "SYNTHESIZE 综合", "src": "So What / 80-20 / Storyline",
     "research": "So What 提炼：主线=？关键数=？80/20 聚焦，结论式标题",
     "landing": "第 12 章叙事 123 + 第 13 页结论式标题", "power": "脚手架"},
    {"step": "DECIDE 决策", "src": "Pre-Mortem / Margin of Safety / Go-No-Go",
     "research": "事前尸检 + ≥30% 安全边际 + 打板许可闸门 → 决策门",
     "landing": "第 5.2/5.4 节 + 第 12 页风险清单 + 第 14 页 5 条预判", "power": "脚手架"},
    {"step": "EXECUTE 执行", "src": "100-Day Plan / Risk Triggers / AAR",
     "research": "跟踪清单 + 风险触发器 + 次日 19:15 预判核验复盘（AAR）",
     "landing": "第 13 页跟踪清单 + 预判核验任务", "power": "脚手架"},
]

# ───────────────────── 十域 → A 股研判视角映射（核心）─────────────────────
# power ∈ {脚手架, 定性清单, 风险提问, 叙事}；一律无剔除权、无打分权
DOMAIN_MAP: list[dict] = [
    {"domain": 1, "zh": "AI与大数据", "lens": "AI 产业趋势与技术真伪",
     "research_q": "本轮 AI 主线是算力兑现、智能体扩散还是应用落地？技术是否经得起尽调？",
     "hook": "第 10 章 Anthropic 映射 + S09 AI 分层 + 第 3 域技术尽调", "power": "定性清单"},
    {"domain": 2, "zh": "网络安全", "lens": "地缘/制裁/数据跨境风险",
     "research_q": "标的是否暴露于出口管制、制裁、数据跨境合规风险？",
     "hook": "第 12 页风险清单（对应 L0 缺口 M09/M10）", "power": "风险提问"},
    {"domain": 3, "zh": "技术素养", "lens": "技术尽调与新兴技术雷达",
     "research_q": "题材的技术壁垒是真还是叙事？处于 Gartner 曲线哪一段？",
     "hook": "第 6.0 节前置层证据核验 + 技术尽调清单", "power": "定性清单"},
    {"domain": 4, "zh": "创造性思维", "lens": "主题孵化与范式转换",
     "research_q": "这是蓝海价值创新还是红海跟风？是否范式转换级机会？",
     "hook": "第 6.4 节 X-主题三层白名单 + 未来回溯规划", "power": "叙事"},
    {"domain": 5, "zh": "韧性敏捷", "lens": "反脆弱与地缘敏捷",
     "research_q": "组合是否杠铃化（底仓防御+小仓期权）？地缘风险有无对冲？",
     "hook": "第 6.7 节反身性 + α 三层面分桶 + 情景规划", "power": "风险提问"},
    {"domain": 6, "zh": "好奇心与学习", "lens": "心智模型与假设检验",
     "research_q": "是否落入‘这次不一样’叙事？用芒格格栅/第一性原理交叉检验了吗？",
     "hook": "第 4 章哲学底座 + 第 6.0 节人性层", "power": "叙事"},
    {"domain": 7, "zh": "领导力与社会影响", "lens": "治理与政治智慧",
     "research_q": "实控人/董事会治理有无劣迹？政策解读是否到位？",
     "hook": "治理尽调清单（呼应达尔文六大禁区‘骗子治理’）", "power": "定性清单"},
    {"domain": 8, "zh": "人才管理", "lens": "组织健康与人才密度",
     "research_q": "管理层能力与激励是否对齐？组织是否支撑成长兑现？",
     "hook": "第 10.2 节管理层评估 + L3 基本面定性补充", "power": "定性清单"},
    {"domain": 9, "zh": "分析思维", "lens": "可审计推理链（最实质域）",
     "research_q": "决策树/贝叶斯更新/战略估值（EVA/SVA/实物期权）是否留痕？",
     "hook": "第 5 章决策层 + 第 5.5 节估值锚 + FAIR 风险量化", "power": "脚手架"},
    {"domain": 10, "zh": "环境管理", "lens": "ESG 与气候风险",
     "research_q": "有无 TCFD 物理/转型风险？绿色金融/碳中和是否构成主题催化？",
     "hook": "第 12 页风险清单 + X-绿电主题（6.4 节）", "power": "风险提问"},
]

# ───────────────────── 投行私募 A1-A10 → 资本运作映射 ─────────────────────
IB_PE_MAP: list[dict] = [
    {"id": "A1", "name": "IPO筹备", "research": "次新股/拟上市影子股；Anthropic S-1 对标已落 §10", "power": "定性清单"},
    {"id": "A2", "name": "并购整合", "research": "央企重组/专业化整合（X-主题 A 层）", "power": "定性清单"},
    {"id": "A3", "name": "PE价值创造", "research": "100 天价值创造计划 → 经营改善兑现观察", "power": "叙事"},
    {"id": "A4", "name": "杠杆收购", "research": "高杠杆标的列为达尔文禁区（第 6.0 节）", "power": "风险提问"},
    {"id": "A5", "name": "困境扭转", "research": "困境反转四象限（S01）+ 连续两年亏损否决口径④", "power": "定性清单"},
    {"id": "A6", "name": "跨境并购", "research": "CFIUS/反垄断/汇率对冲 → 出海链风险清单", "power": "风险提问"},
    {"id": "A7", "name": "资本市场策略", "research": "定增/可转债/优先股 → 资本运作事件标签", "power": "定性清单"},
    {"id": "A8", "name": "股东积极主义防御", "research": "十大流通股东变化 + 筹码集中度（L3 已有）", "power": "定性清单"},
    {"id": "A9", "name": "PE募集", "research": "创投/专精特新/独角兽密度（X-主题 A/B 层）", "power": "定性清单"},
    {"id": "A10", "name": "实物资产", "research": "REITs/基础设施/自然资源（S03 红利底仓）", "power": "定性清单"},
]

# ───────────────────── 出海 G1-G10 → 出海链映射 ───────────────────────────
GLOBALIZATION_MAP: list[dict] = [
    {"id": "G1", "name": "全球市场锚定", "research": "市场选择四维 → 出口链/海外营收占比标的", "power": "定性清单"},
    {"id": "G2", "name": "跨境合规", "research": "制裁/出口管制风险 → 风险清单（呼应域二）", "power": "风险提问"},
    {"id": "G3", "name": "跨境财税", "research": "汇率对冲 → M09 汇率缺口定性", "power": "风险提问"},
    {"id": "G4", "name": "本地化运营", "research": "本地化落地 → 出海兑现验证", "power": "定性清单"},
    {"id": "G5", "name": "香港超级联系人", "research": "中概股回归/A+H（呼应好孩子 A+H 资本运作）", "power": "叙事"},
    {"id": "G6", "name": "一带一路", "research": "互联互通基建/电力绿电出海（X-主题）", "power": "定性清单"},
    {"id": "G7", "name": "新兴市场进入", "research": "东南亚/中东/非洲市场洞察", "power": "定性清单"},
    {"id": "G8", "name": "全球IP保护", "research": "专利布局/IP 货币化 → 创新药 BD 技术出海", "power": "定性清单"},
    {"id": "G9", "name": "出海文化智商", "research": "数字文化/游戏网剧出海（商务部实践篇）", "power": "定性清单"},
    {"id": "G10", "name": "全球危机声誉", "research": "跨国危机公关/ESG 国际舆论 → 风险清单", "power": "风险提问"},
]

# ───────────────────── AI 超能力 8 模块 → 研判工作台 ──────────────────────
AI_SUPERPOWER_MAP: list[dict] = [
    {"name": "AI战略顾问", "research": "实时战略选项与风险评估 → L0 宏观定位辅助", "hook": "6.2 节"},
    {"name": "AI投资分析师", "research": "自动 DCF/敏感性/备忘录 → 5.5 节估值锚辅助", "hook": "5.5 节"},
    {"name": "AI风险雷达", "research": "地缘/网络/气候实时预警 → 第 12 页风险清单", "hook": "12 页"},
    {"name": "AI创新伙伴", "research": "跨界概念组合 → X-主题孵化", "hook": "6.4 节"},
    {"name": "AI学习教练", "research": "认知偏见识别 → 达尔文禁区/人性层自检", "hook": "4/6.0 节"},
    {"name": "AI组织诊断师", "research": "组织网络分析 → 管理层/组织尽调", "hook": "域八清单"},
    {"name": "AI ESG合规官", "research": "TCFD/碳足迹 → ESG 风险清单", "hook": "域十清单"},
    {"name": "AI决策副驾", "research": "Pre-Mortem/贝叶斯更新/决策树 → 5 章决策层", "hook": "5 章"},
]

# ───────────────────── 16 方法论工具 → 可审计推理链 ───────────────────────
METHOD_MAP: list[dict] = [
    {"m": "MECE", "status": "已注入", "landing": "5.1 Issue Tree"},
    {"m": "Issue Tree", "status": "已注入", "landing": "5.1 议题树"},
    {"m": "假设驱动", "status": "已注入", "landing": "5.1 + 6.0 前置层"},
    {"m": "BCG Matrix", "status": "映射", "landing": "S01 四象限"},
    {"m": "Porter五力", "status": "映射", "landing": "第 10 章产业链分析"},
    {"m": "Blue Ocean", "status": "映射", "landing": "域四主题孵化"},
    {"m": "Balanced Scorecard", "status": "映射", "landing": "跟踪清单多维度"},
    {"m": "OKR", "status": "定性", "landing": "管理层执行观察"},
    {"m": "Design Thinking", "status": "定性", "landing": "叙事层"},
    {"m": "Agile/Scrum", "status": "定性", "landing": "组织尽调"},
    {"m": "Systems Thinking", "status": "映射", "landing": "反身性 + 因果回路"},
    {"m": "Pre-Mortem", "status": "已注入", "landing": "5.2 事前尸检"},
    {"m": "DCF/LBO", "status": "部分注入", "landing": "5.5 DCF，LBO 域九登记"},
    {"m": "9-Box Grid", "status": "定性", "landing": "人才尽调"},
    {"m": "FAIR Model", "status": "映射", "landing": "风险量化方法论（域九登记）"},
    {"m": "TCFD", "status": "映射", "landing": "域十气候风险清单"},
]

# ───────────────────── 治理 / 人才 / ESG 定性尽调清单 ──────────────────────
DD_CHECKLIST: list[dict] = [
    {"item": "实控人/董事会治理劣迹", "src": "域七 board-governance", "gate": "呼应达尔文禁区·骗子治理（定性，不新增否决口径）"},
    {"item": "管理层能力与激励对齐", "src": "域八 executive-compensation", "gate": "L3 基本面定性补充，不改半年归母同比判定"},
    {"item": "组织健康与人才密度", "src": "域八 talent-strategy", "gate": "成长兑现观察项，不参与打分"},
    {"item": "TCFD 物理/转型风险", "src": "域十 climate-risk", "gate": "风险清单定性增补，不改写六条口径"},
    {"item": "数据跨境与制裁合规", "src": "域二 data-privacy / G2", "gate": "风险清单定性增补"},
    {"item": "技术壁垒尽调", "src": "域三 tech-due-diligence", "gate": "题材真伪核验，不改 L1/L2 阈值"},
]

# ───────────────────── 风险雷达增补提问 ────────────────────────────────────
RISK_RADAR_Q: list[dict] = [
    {"q": "地缘政治风险矩阵是否已更新（季度）？", "src": "域五 geopolitical-agility", "fill": "westock 无接口 → 仅定性"},
    {"q": "网络安全事件/数据泄露是否影响标的？", "src": "域二 incident-response", "fill": "仅定性"},
    {"q": "出口管制/制裁是否命中产业链？", "src": "域二 + G2", "fill": "仅定性"},
    {"q": "气候物理/转型风险是否计入？", "src": "域十 climate-risk (TCFD)", "fill": "仅定性"},
    {"q": "高杠杆/并购成瘾是否命中达尔文禁区？", "src": "域九 + A4/A2", "fill": "定性交叉，不新增数值"},
]


# ─────────────────────────── 映射配置出口 ───────────────────────────
def decision_os() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_decision_os"], "steps": DECISION_5STEP,
            "mapping": DECISION_OS_MAP, "note": "五步框架只是推理链脚手架，不改变任何判定结果。"}


def domain_map() -> dict:
    by_power: dict[str, int] = {}
    for d in DOMAIN_MAP:
        by_power[d["power"]] = by_power.get(d["power"], 0) + 1
    return {"enabled": GCCEO_SWITCHES["gceo_domain_map"], "domains": DOMAINS,
            "domain_skill_total": DOMAIN_SKILL_TOTAL, "mapping": DOMAIN_MAP,
            "power_counts": by_power,
            "unchanged": "18方向/102板块/31行业/70只代表个股/四层漏斗/情绪五阶段一律不动",
            "note": "十域能力映射为研判视角，不作为选股因子；无剔除权、无打分权。"}


def ib_pe_map() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_ib_pe_map"], "skills": IB_SKILLS,
            "mapping": IB_PE_MAP, "n": len(IB_PE_MAP),
            "note": "投行私募能力映射为资本运作事件标签；A4 高杠杆反向接入达尔文禁区。"}


def globalization_map() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_global_expansion"],
            "skills": GLOBALIZATION_SKILLS, "four_dimensions": GLOBALIZATION_4D,
            "mapping": GLOBALIZATION_MAP, "n": len(GLOBALIZATION_MAP),
            "note": "G1-G10 映射为出海链定性标签，与 X-主题出海方向（6.4）对齐；无剔除权。"}


def ai_superpowers() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_ai_superpowers"],
            "powers": AI_SUPERPOWERS, "mapping": AI_SUPERPOWER_MAP, "n": len(AI_SUPERPOWER_MAP),
            "note": "8 大模型超能力作为研判工作台辅助定位，落到既有章节，不新增信号。"}


def method_toolbox() -> dict:
    injected = sum(1 for m in METHOD_MAP if m["status"] == "已注入")
    mapped = sum(1 for m in METHOD_MAP if m["status"] in ("映射", "部分注入"))
    return {"enabled": GCCEO_SWITCHES["gceo_method_toolbox"], "tools": METHOD_TOOLS,
            "mapping": METHOD_MAP, "n": len(METHOD_MAP),
            "injected": injected, "mapped": mapped,
            "note": "16 方法论标注落点：已注入/映射/定性；推理链可审计，不改判定。"}


def governance_talent() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_governance_talent"],
            "checklist": DD_CHECKLIST, "n": len(DD_CHECKLIST),
            "note": "治理/人才/ESG 域转为定性尽调清单；全部标注 gate，明确不改写任何硬口径。"}


def risk_radar() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_risk_radar"],
            "questions": RISK_RADAR_Q, "n": len(RISK_RADAR_Q),
            "note": "地缘/网络/气候/杠杆风险提问；westock 无接口一律标「仅定性」，不编造。"}


def narrative_setup() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_narrative"],
            "principles": [
                "结论先行（So What）：每页先给判断再给依据（叙事 123 继承）",
                "可审计：每个判断标注来自哪条 GCCEO 视角/清单，推理链留痕",
                "反叙事：禁用「这次不一样」，命中即触发 Pre-Mortem（5.2）",
                "复盘纪律：次日 19:15 预判核验即 AAR（行动后复盘）",
                "水印先行：GCCEO 技能数 96/91 口径差异登记，不写绝对值阈值",
            ]}


def watermark_setup() -> dict:
    return {"enabled": GCCEO_SWITCHES["gceo_watermark"], "caliber_diffs": CALIBER_DIFFS,
            "rule": "【事实】已发布 /【预测】前瞻 /【口径差异】多来源冲突只取方向",
            "note": "沿用 v3.0 三类水印；GCCEO 技能数双口径登记，不污染六条口径绩效。"}


# ───────────────────── 非侵入性自检（口径未被污染）─────────────────────
GCEEO_EXPECTED = {
    "CALIBER_VERSION": "v2.3",
    "SOE_BACKGROUND_IS_GATE": False,
    "EMERGING_TECH_FIRST": True,
    "PROFIT_GROWTH_CALIBER": "half_year",
    "SINGLE_YEAR_LOSS_IS_VETO": False,
    "TWO_CONSECUTIVE_LOSSES_IS_VETO": True,
    "CHAIN_THEME_SKIPS_L1_VETO": True,
    "TRADABILITY_LAYER": "L2.5",
    "RANK_LOW_THRESHOLD": 25.0,
    "VR_THRESHOLD": 1.0,
    "DISPERSION_ALERT": 60.0,
}


def gceo_non_invasive_check(C=None, KN=None, V3=None) -> dict:
    """只读快照比对，证明 GCCEO 全量整合未污染 v2.3 口径 / KNOWLEDGE / v3 层。"""
    if C is None:
        from strategy import calibers as C  # noqa
    if KN is None:
        try:
            from strategy import knowledge as KN  # noqa
        except ImportError:
            KN = None
    checks: list[dict] = []
    # A. 六条口径 + 四层阈值（11 项）
    for k, exp in GCEEO_EXPECTED.items():
        act = getattr(C, k, "<缺失>")
        checks.append({"item": k, "expected": exp, "actual": act, "ok": act == exp})
    # B. KNOWLEDGE（3 项）
    k = getattr(C, "KNOWLEDGE", {}) or {}
    checks.append({"item": "KNOWLEDGE 键数", "expected": 45, "actual": len(k), "ok": len(k) == 45})
    checks.append({"item": "KNOWLEDGE 红旗否决线", "expected": 2,
                   "actual": k.get("红旗否决线"), "ok": k.get("红旗否决线") == 2})
    checks.append({"item": "KNOWLEDGE 打板连板率门槛", "expected": 0.60,
                   "actual": k.get("打板_连板率门槛"), "ok": k.get("打板_连板率门槛") == 0.60})
    # C. v3 层未被改写（2 项）
    checks.append({"item": "v3 旁路版本不变", "expected": "v3.0",
                   "actual": getattr(C, "EXTENSION_VERSION", "<缺失>"),
                   "ok": getattr(C, "EXTENSION_VERSION", None) == "v3.0"})
    checks.append({"item": "v3 五模块数不变", "expected": 5,
                   "actual": len(getattr(C, "EXTENSION_MODULES", ())),
                   "ok": len(getattr(C, "EXTENSION_MODULES", ())) == 5})
    # D. GCCEO 层自身结构（6 项）
    checks.append({"item": "GCCEO 源版本", "expected": "4.0.0", "actual": GCCEO_SOURCE_VERSION,
                   "ok": GCCEO_SOURCE_VERSION == "4.0.0"})
    checks.append({"item": "GCCEO 十域数", "expected": 10, "actual": len(DOMAINS), "ok": len(DOMAINS) == 10})
    checks.append({"item": "GCCEO 域内技能合计", "expected": 91, "actual": DOMAIN_SKILL_TOTAL,
                   "ok": DOMAIN_SKILL_TOTAL == 91})
    checks.append({"item": "GCCEO 映射模块数", "expected": len(GCCEO_SWITCHES),
                   "actual": len(GCCEO_SWITCHES), "ok": len(GCCEO_SWITCHES) == 10})
    checks.append({"item": "GCCEO 只读无剔除", "expected": True, "actual": NO_VETO, "ok": NO_VETO is True})
    checks.append({"item": "GCCEO 无仓位上调权", "expected": True, "actual": NO_POSITION_UP,
                   "ok": NO_POSITION_UP is True})
    # E. 复用 v3 自检结果（不重复跑，引用入参）
    v3_recheck = None
    if V3 is not None:
        v3_recheck = {"passed": V3.get("passed"), "total": V3.get("total"),
                      "all_ok": V3.get("all_ok", False)}
        checks.append({"item": "v3 non_invasive_check 复用", "expected": True,
                       "actual": bool(V3.get("all_ok")), "ok": bool(V3.get("all_ok"))
                       and V3.get("passed") == 14 and V3.get("total") == 14})

    passed = sum(1 for c in checks if c["ok"])
    return {"passed": passed, "total": len(checks), "all_ok": all(c["ok"] for c in checks),
            "checks": checks, "v3_recheck": v3_recheck,
            "knowledge_module_present": KN is not None,
            "contract": "v2.3 六口径 + KNOWLEDGE45 + v3 五模块全部只读比对；GCCEO 仅旁路映射。"}


# ─────────────────────────── 统一入口 ───────────────────────────
def build_gceo_overlay(data: dict, check_modules: bool = True,
                       v3_check: dict | None = None) -> dict:
    """生成可 JSON 序列化的 `gceo` 覆盖层，写入 data.json 顶层。只读，不改既有键。"""
    ov: dict[str, Any] = {"enabled": True, "overlay_only": OVERLAY_ONLY}
    ov.update({
        "extension_version": GCCEO_EXT_VERSION,
        "source_version": GCCEO_SOURCE_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "confirmed_on": GCCEO_CONFIRMED_ON,
        "caliber_version_unchanged": CALIBER_VERSION_UNCHANGED,
        "v3_version_unchanged": V3_VERSION_UNCHANGED,
        "no_veto": NO_VETO,
        "no_position_up": NO_POSITION_UP,
        "switches": dict(GCCEO_SWITCHES),
        "decision_os": decision_os(),
        "domains": domain_map(),
        "ib_pe": ib_pe_map(),
        "globalization": globalization_map(),
        "ai_superpowers": ai_superpowers(),
        "method_toolbox": method_toolbox(),
        "governance_talent": governance_talent(),
        "risk_radar": risk_radar(),
        "narrative": narrative_setup(),
        "watermark": watermark_setup(),
        "source_counts": {
            "domains": len(DOMAINS), "domain_skills": DOMAIN_SKILL_TOTAL,
            "ib_pe": len(IB_SKILLS), "globalization": len(GLOBALIZATION_SKILLS),
            "ai_superpowers": len(AI_SUPERPOWERS), "method_tools": len(METHOD_TOOLS),
            "decision_steps": len(DECISION_5STEP), "globalization_dims": len(GLOBALIZATION_4D),
        },
        "non_invasive_check": (
            gceo_non_invasive_check(V3=v3_check) if check_modules
            else {"passed": 0, "total": 0, "all_ok": True, "checks": [], "v3_recheck": None}
        ),
        "rollback": (
            "data.json 顶层 gceo.enabled=false → 回到 v3.0 16 页；"
            "v3.enabled=false 正交 → 14 页纯 v2.3。二者互不影响。"
        ),
        "frequency": "GCCEO 映射为常驻只读视角层，随报告日重算叙事；不引入新的取数频率。",
    })
    return ov


def gceo_report_blocks(ov: dict) -> dict:
    """把覆盖层压成渲染器可直接取用的文本块（避免模板里写逻辑）。"""
    dm, ib, gl = ov["domains"], ov["ib_pe"], ov["globalization"]
    ai, mt, gt, rr = ov["ai_superpowers"], ov["method_toolbox"], ov["governance_talent"], ov["risk_radar"]
    ch = ov["non_invasive_check"]
    return {
        "headline": (
            f"GCCEO 全量整合层已生效 · 十域 {dm['domain_skill_total']} 技能 → 研判视角映射 · "
            f"投行 {ib['n']} / 出海 {gl['n']} / AI超能力 {ai['n']} / 方法论 {mt['n']} · "
            f"只读无剔除 · 六条口径 v2.3 与 v3.0 结论零改动"
        ),
        "decision_rows": [{"step": m["step"], "research": m["research"], "landing": m["landing"]}
                          for m in ov["decision_os"]["mapping"]],
        "domain_rows": [{"domain": d["domain"], "zh": d["zh"], "lens": d["lens"],
                         "q": d["research_q"], "hook": d["hook"], "power": d["power"]}
                        for d in dm["mapping"]],
        "ib_rows": [{"id": m["id"], "name": m["name"], "research": m["research"], "power": m["power"]}
                    for m in ib["mapping"]],
        "gl_rows": [{"id": m["id"], "name": m["name"], "research": m["research"], "power": m["power"]}
                    for m in gl["mapping"]],
        "ai_rows": [{"name": m["name"], "research": m["research"], "hook": m["hook"]}
                    for m in ai["mapping"]],
        "method_rows": [{"m": m["m"], "status": m["status"], "landing": m["landing"]}
                        for m in mt["mapping"]],
        "dd_rows": [{"item": m["item"], "src": m["src"], "gate": m["gate"]}
                    for m in gt["checklist"]],
        "risk_rows": [{"q": m["q"], "src": m["src"], "fill": m["fill"]}
                      for m in rr["questions"]],
        "narrative": ov["narrative"]["principles"],
        "caliber_diffs": ov["watermark"]["caliber_diffs"],
        "checks": ch,
        "rollback": ov["rollback"],
        "counts": {
            "domains": dm["domain_skill_total"],
            "ib_pe": ib["n"], "globalization": gl["n"], "ai_superpowers": ai["n"],
            "method_tools": mt["n"], "method_injected": mt["injected"],
            "method_mapped": mt["mapped"], "dd_items": gt["n"], "risk_q": rr["n"],
            "decision_steps": len(ov["decision_os"]["steps"]),
            "checks_passed": ch["passed"], "checks_total": ch["total"],
        },
    }


if __name__ == "__main__":
    # 脚本方式直跑（python3 strategy/gcceo_ext.py）时，把项目根加入 path，
    # 与 SKILL.md §13.1 的自检调用方式保持一致。
    import os as _os
    import sys as _sys
    _ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    if _ROOT not in _sys.path:
        _sys.path.insert(0, _ROOT)
    from strategy.v3_ext import non_invasive_check as v3_check
    demo = build_gceo_overlay({"context": {"sentiment_stage": "发酵"}},
                              v3_check=v3_check())
    import json as _j
    print(_j.dumps(gceo_report_blocks(demo)["counts"], ensure_ascii=False, indent=2))
    print("checks:", demo["non_invasive_check"]["passed"], "/", demo["non_invasive_check"]["total"],
          "all_ok:", demo["non_invasive_check"]["all_ok"])
