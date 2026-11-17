#!/usr/bin/env python3
"""
多维评价与评分引擎（规则驱动，零大模型依赖）。

- JD 关键要求拆解：从 JD 提取技能关键词、职责点、行业方向
- 逐维度评分：按用户提供的评价维度（含标准与规则）逐条计算 0-100 分
- 总分 = 维度加权平均；每条得分均可追溯（规则 + 命中证据）
"""

import re

from rule_engine import run_rule, strip_meta_text

# 产品经理常用技能/工具词库（用于 JD 技能关键词提取）
PM_SKILL_LEXICON = [
    "需求分析", "用户调研", "用户访谈", "竞品分析", "PRD", "需求文档", "原型", "Axure", "Figma",
    "墨刀", "SQL", "Excel", "Python", "数据分析", "数据看板", "埋点", "A/B测试", "AB测试",
    "用户增长", "留存", "转化率", "漏斗", "用户画像", "项目管理", "敏捷", "Scrum", "跨部门协作",
    "沟通", "文档", "流程图", "XMind", "思维导图", "MVP", "roadmap", "Roadmap", "OCR",
    "机器学习", "AI", "大模型", "LLM", "AIGC", "ChatGPT", "prompt", "提示词", "智能体", "Agent",
    "RAG", "Copilot", "算法", "推荐系统", "策略", "内容运营", "用户运营", "活动运营", "增长黑客",
    "商业化", "广告", "会员", "支付", "供应链", "直播", "短视频", "电商", "社交", "游戏",
]

# 行业/产品方向词库（用于 JD 行业提示提取）
INDUSTRY_LEXICON = [
    "AI", "人工智能", "电商", "游戏", "金融", "社交", "内容", "工具", "教育", "医疗", "汽车",
    "零售", "物流", "出海", "本地生活", "短视频", "直播", "SaaS", "云计算", "安全", "社交电商",
]

# JD 职责动词（用于职责点提取）
JD_ACTION_VERBS = [
    "负责", "参与", "跟进", "推动", "主导", "输出", "制定", "梳理", "对接", "协调",
    "搭建", "设计", "优化", "分析", "挖掘", "规划", "监控", "评估", "执行", "维护",
]

STOPWORDS = {"的", "了", "和", "与", "及", "等", "相关", "工作", "以及", "进行", "对", "为", "在", "从", "并", "或", "中"}


def _score_level(score: float) -> str:
    if score >= 85:
        return "优秀"
    if score >= 70:
        return "良好"
    if score >= 55:
        return "及格"
    if score >= 40:
        return "待改进"
    return "不合格"


def analyze_jd(jd_text: str) -> dict:
    """JD 关键要求拆解（本地规则）。"""
    jd = jd_text or ""

    # 1. 技能关键词：词库命中 + "熟悉/掌握/熟练/了解"后置词
    skill_keywords = []
    for kw in PM_SKILL_LEXICON:
        if kw in jd:
            skill_keywords.append(kw)
    for m in re.finditer(r"(熟悉|掌握|熟练|了解|具备|要求)[\s:：、]*([\u4e00-\u9fa5A-Za-z0-9+/]{2,12})", jd):
        w = m.group(2)
        if w not in skill_keywords and not any(c.isdigit() for c in w):
            skill_keywords.append(w)
    # 去重保序
    seen = set()
    skill_keywords = [w for w in skill_keywords if not (w in seen or seen.add(w))][:20]

    # 2. 职责点：含职责动词的行 → 提取关键词
    responsibilities = []
    seen_r = set()
    for line in jd.splitlines():
        line = line.strip()
        if not line or len(line) > 60:
            continue
        if any(v in line for v in JD_ACTION_VERBS):
            # 取每行中可能的关键短语（去掉常见标点）
            clean = re.sub(r"[，。；、：:（）()\d.,，\-—\s]+", " ", line)
            words = [w.strip() for w in clean.split(" ") if 2 <= len(w.strip()) <= 12]
            for w in words:
                if w in STOPWORDS or w in JD_ACTION_VERBS:
                    continue
                if any(v in w for v in JD_ACTION_VERBS):
                    continue
                if w not in seen_r:
                    seen_r.add(w)
                    responsibilities.append({"origin": line[:50], "keyword": w})
            if len(responsibilities) >= 15:
                break

    # 3. 行业/产品方向提示
    industry_hints = []
    for kw in INDUSTRY_LEXICON:
        if kw in jd:
            industry_hints.append(kw)

    return {
        "skill_keywords": skill_keywords[:15],
        "responsibilities": responsibilities[:12],
        "industry_hints": industry_hints,
        "summary": _jd_summary(jd, industry_hints),
    }


def _jd_summary(jd: str, industry_hints: list) -> str:
    """JD 核心诉求一句话概括（规则）。"""
    parts = []
    if industry_hints:
        parts.append(f"{'、'.join(industry_hints[:3])} 方向")
    if "产品经理" in jd or "PM" in jd:
        parts.append("产品经理岗位")
    elif "产品" in jd:
        parts.append("产品相关岗位")
    if "实习" in jd:
        parts.append("实习机会")
    elif "校招" in jd or "应届" in jd:
        parts.append("校招")
    if "熟悉" in jd or "掌握" in jd or "要求" in jd:
        parts.append("对候选人有明确技能要求")
    return "目标岗位为" + ("，".join(parts) if parts else "产品经理类岗位")


def _dimension_comment(dim: dict, score: float, rule_results: list) -> str:
    """按分数段生成维度评语（模板化 + 引用证据）。"""
    std = dim.get("standard", "")
    if score >= 85:
        base = f"表现出色（{score} 分）。{std}"
    elif score >= 70:
        base = f"整体达标（{score} 分）。{std}"
    elif score >= 55:
        base = f"有基础但仍有提升空间（{score} 分）。{std}"
    elif score >= 40:
        base = f"明显不足（{score} 分）。{std}"
    else:
        base = f"严重欠缺（{score} 分）。{std}"
    return base


def _dimension_suggestions(dim: dict, score: float, rule_results: list) -> list:
    """按规则证据生成具体可执行的优化建议（模板化）。"""
    suggestions = []
    lowest = min(rule_results, key=lambda r: r.score)
    if score < 70:
        suggestions.append(
            f"本维度得分 {score} 分，重点改进：“{lowest.detail}”。"
        )
    # 规则级建议
    for r in rule_results:
        if r.score >= 85:
            continue
        ev = r.evidence[0] if r.evidence else ""
        suggestions.append(f"[{r.detail}] 当前：{ev}")
    if score < 55 and lowest.score < 40:
        suggestions.append("建议优先补齐该维度基础项，再考虑亮点包装。")
    return suggestions[:4]


def evaluate_resume(
    resume_text: str,
    structured: dict,
    jd_text: str,
    dimensions: list,
) -> dict:
    """按用户提供的维度配置对简历进行多维评分。

    评分前会剥离优化稿/报告中的元信息（摘要、诊断、头部声明、量化标注等），
    仅对简历正文计算规则得分，避免"优化后反而低分"的误判。

    返回 dict：
      total_score / computed_score / verdict
      dimension_scores: [{id, name, weight, score, comment, suggestions, evidence}]
      jd_analysis / highlights / gaps / rule_trace
    """
    # 评分以剥离元信息后的简历正文为准（结构化解析仍基于原始文本）
    clean_text = strip_meta_text(resume_text)
    ctx = {
        "resume_text": clean_text,
        "structured": structured,
        "jd_text": jd_text,
        "jd_analysis": analyze_jd(jd_text),
    }
    jd = ctx["jd_analysis"]

    dimension_scores = []
    rule_trace = {}
    for dim in dimensions:
        rules = dim.get("rules") or []
        results = [run_rule(r, ctx) for r in rules]
        rule_trace[dim["id"]] = [
            {
                "label": rule.get("label", rule.get("type", "")),
                "type": rule.get("type", ""),
                "score": r.score,
                "evidence": r.evidence,
            }
            for r, rule in zip(results, rules)
        ]
        total_w = sum(r.weight for r in results) or 1.0
        dim_score = round(sum(r.score * r.weight for r in results) / total_w, 1)
        dimension_scores.append({
            "id": dim.get("id", ""),
            "name": dim.get("name", ""),
            "weight": dim.get("weight", 0),
            "standard": dim.get("standard", ""),
            "score": dim_score,
            "comment": _dimension_comment(dim, dim_score, results),
            "suggestions": _dimension_suggestions(dim, dim_score, results),
            "evidence": [r.evidence for r in results],
        })

    total_w = sum(d.get("weight", 0) for d in dimension_scores) or 100.0
    computed = round(sum(d["score"] * d["weight"] for d in dimension_scores) / total_w, 1)
    total_score = computed

    highlights, gaps = _highlights_gaps(clean_text, dimension_scores, jd)

    verdict = (
        f"综合评分 {total_score}/100（{_score_level(total_score)}）。"
        + _verdict_tail(total_score, gaps)
    )

    return {
        "total_score": total_score,
        "computed_score": computed,
        "verdict": verdict,
        "dimension_scores": dimension_scores,
        "jd_analysis": jd,
        "highlights": highlights,
        "gaps": gaps,
        "rule_trace": rule_trace,
    }


def _verdict_tail(score: float, gaps: list) -> str:
    if score >= 70:
        return "简历已具备较好竞争力，按报告建议微调后即可投递。"
    if score >= 55:
        return "简历存在明显短板，建议针对差距逐项优化后再投递。"
    return "简历当前竞争力不足，建议先补齐结构、突出量化成果，再针对岗位定制。"


def _highlights_gaps(resume_text: str, dimension_scores: list, jd: dict) -> tuple:
    """亮点与差距（规则化）。"""
    highlights = []
    gaps = []

    strong = [d for d in dimension_scores if d["score"] >= 75]
    weak = sorted([d for d in dimension_scores if d["score"] < 60], key=lambda d: d["score"])

    if strong:
        highlights.append(f"优势维度：{', '.join(d['name'] for d in strong)}")
    if re.search(r"[\d.]+%", resume_text):
        highlights.append("含百分比量化成果，数据意识较好")
    if re.search(r"(主导|负责|搭建|从0到1)", resume_text):
        highlights.append("经历描述使用强动词，体现个人贡献")
    if not highlights:
        highlights.append("未检测到明显亮点，建议从量化成果与产品流程完整性入手提升")

    if weak:
        for d in weak[:3]:
            gaps.append(f"{d['name']}（{d['score']} 分）：{d['suggestions'][0] if d['suggestions'] else '需改进'}")
    jd_skills = jd.get("skill_keywords") or []
    if jd_skills:
        miss = [s for s in jd_skills if s not in resume_text][:4]
        if miss:
            gaps.append(f"JD 要求但简历未体现的技能/关键词：{', '.join(miss)}")
    if not gaps:
        gaps.append("无明显硬伤，可结合 JD 做最后一轮针对性微调")

    return highlights[:3], gaps[:4]
