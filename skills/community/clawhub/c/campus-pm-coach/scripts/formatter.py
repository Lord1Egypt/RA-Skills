#!/usr/bin/env python3
"""
输出格式化模块：生成 Markdown 评分报告 / 模拟面试题报告 / JSON 结果。
"""

import json
import os


def _level(score: float) -> str:
    if score >= 85:
        return "优秀"
    if score >= 70:
        return "良好"
    if score >= 55:
        return "及格"
    if score >= 40:
        return "待改进"
    return "不合格"


def format_evaluation_report(evaluation: dict, jd_text: str) -> str:
    """生成能力1的 Markdown 评分报告。"""
    lines = []
    total = evaluation.get("total_score", 0)
    lines.append("# 简历 × JD 多维评价报告")
    lines.append("")
    lines.append(f"**综合评分：{total} / 100** 　**等级：{_level(total)}**")
    lines.append("")
    if evaluation.get("verdict"):
        lines.append(f"> {evaluation['verdict']}")
        lines.append("")

    # 分数概览表
    lines.append("## 一、各维度评分概览")
    lines.append("")
    lines.append("| 维度 | 权重 | 得分 | 评语 |")
    lines.append("| --- | --- | --- | --- |")
    for d in evaluation.get("dimension_scores", []):
        lines.append(
            f"| {d['name']} | {d['weight']}% | {d['score']} | {d.get('comment', '').replace('|', '/')} |"
        )
    lines.append("")

    # JD 关键要求拆解
    jd = evaluation.get("jd_analysis") or {}
    lines.append("## 二、JD 关键要求拆解")
    lines.append("")
    if jd.get("summary"):
        lines.append(f"**JD 核心诉求**：{jd['summary']}")
        lines.append("")
    if jd.get("must_have_skills"):
        lines.append(f"- **必备技能**：{', '.join(jd['must_have_skills'])}")
    if jd.get("plus_skills"):
        lines.append(f"- **加分技能**：{', '.join(jd['plus_skills'])}")
    if jd.get("key_responsibilities"):
        lines.append("- **关键职责**：")
        for r in jd["key_responsibilities"]:
            lines.append(f"  - {r}")
    lines.append("")

    # 逐维度详细评价与建议
    lines.append("## 三、逐维度评价与优化建议")
    lines.append("")
    for i, d in enumerate(evaluation.get("dimension_scores", []), 1):
        lines.append(f"### {i}. {d['name']}（{d['score']} / 100，权重 {d['weight']}%）")
        lines.append("")
        if d.get("comment"):
            lines.append(f"**评语**：{d['comment']}")
            lines.append("")
        suggestions = d.get("suggestions") or []
        if suggestions:
            lines.append("**优化建议**：")
            for s in suggestions:
                lines.append(f"- {s}")
            lines.append("")

    # 评分依据（规则可追溯）
    rule_trace = evaluation.get("rule_trace") or {}
    if rule_trace:
        lines.append("## 四、评分依据（规则可追溯）")
        lines.append("")
        lines.append("> 本技能不依赖大模型，所有得分均由本地规则引擎计算，以下为每条规则的命中证据。")
        lines.append("")
        for d in evaluation.get("dimension_scores", []):
            traces = rule_trace.get(d["id"], [])
            if not traces:
                continue
            lines.append(f"### {d['name']}（{d['score']} 分）")
            lines.append("")
            for t in traces:
                lines.append(f"- **{t.get('label', t.get('type', ''))}**（{t['score']} 分）：{t['evidence'][0] if t.get('evidence') else ''}")
            lines.append("")

    # 亮点与差距
    lines.append("## 五、亮点与核心差距")
    lines.append("")
    lines.append("### 候选人亮点")
    for h in evaluation.get("highlights", []):
        lines.append(f"- {h}")
    lines.append("")
    lines.append("### 与 JD 的核心差距")
    for g in evaluation.get("gaps", []):
        lines.append(f"- {g}")
    lines.append("")

    lines.append("## 附：目标 JD 原文")
    lines.append("")
    lines.append("```")
    lines.append(jd_text.strip())
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def format_interview_report(questions_md: str) -> str:
    """生成能力2的模拟面试报告（含头部说明）。"""
    header = [
        "# 模拟面试问题集",
        "",
        "> 基于优化后简历与目标 JD 生成。建议按顺序自测，每题先用 30 秒组织思路再回答，回答后用录音复盘。",
        "",
    ]
    return "\n".join(header) + questions_md.strip() + "\n"


def save_report(text: str, output_dir: str, filename: str) -> str:
    """将 Markdown 报告写入文件，返回完整路径。"""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def save_json(data: dict, output_dir: str, filename: str) -> str:
    """将结果 dict 写入 JSON 文件，返回完整路径。"""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ---------------------------------------------------------------------------
# 首轮诊断（一体化三部分输出）
# ---------------------------------------------------------------------------

def _match_level(total: float) -> str:
    """匹配度等级（由综合评分推导）。"""
    if total >= 80:
        return "高匹配"
    if total >= 65:
        return "中高匹配"
    if total >= 50:
        return "中匹配"
    if total >= 35:
        return "中低匹配"
    return "低匹配"


def extract_questions(questions_md: str, top_n: int = 8) -> list:
    """从模拟面试题 Markdown 中提取「问题」行（用于诊断报告第②部分）。"""
    questions = []
    for line in questions_md.splitlines():
        if "**问题**" in line:
            q = line.split("**问题**", 1)[-1].strip(" ：:：")
            if q:
                questions.append(q)
        if len(questions) >= top_n:
            break
    return questions


def build_judgement(evaluation: dict) -> list:
    """综合判断（第③部分）：由评分与差距分析规则化推导，零大模型。"""
    total = evaluation.get("total_score", 0)
    lines = [f"**匹配度结论**：{_match_level(total)}（综合评分 {total} 分，等级 {_level(total)}）", ""]

    highlights = evaluation.get("highlights") or []
    if highlights:
        lines.append("**核心竞争力**：")
        for h in highlights[:3]:
            lines.append(f"- {h}")
        lines.append("")

    gaps = evaluation.get("gaps") or []
    if gaps:
        lines.append("**关键风险点**：")
        for g in gaps[:4]:
            lines.append(f"- {g}")
        lines.append("")

    must_fix = []
    for d in evaluation.get("dimension_scores", []):
        if d["score"] < 60:
            s = d.get("suggestions") or []
            tip = s[0] if s else "待提升"
            must_fix.append(f"{d['name']}（{d['score']} 分）：{tip}")
    if must_fix:
        lines.append("**投递前必改项**：")
        for m in must_fix:
            lines.append(f"- {m}")
        lines.append("")

    if total >= 75:
        advice = "建议投递：整体与 JD 匹配度较高，补齐短板后竞争力更强。"
    elif total >= 60:
        advice = "建议优化后投递：整体达标但存在明显短板，优先完成上方「投递前必改项」。"
    else:
        advice = "暂不建议投递：与 JD 核心要求差距较大，建议先补齐硬性差距再投递。"
    lines.append(f"**投递建议**：{advice}")
    return lines


def _render_score_section(evaluation: dict, detailed: bool = True) -> list:
    """渲染第①部分：评分总览表 + 细项原因（逐条规则证据）。"""
    lines = []
    lines.append("| 维度 | 权重 | 得分 | 评语 |")
    lines.append("| --- | --- | --- | --- |")
    for d in evaluation.get("dimension_scores", []):
        lines.append(
            f"| {d['name']} | {d['weight']}% | {d['score']} | {d.get('comment', '').replace('|', '/')} |"
        )
    lines.append("")
    if not detailed:
        return lines
    rule_trace = evaluation.get("rule_trace") or {}
    if rule_trace:
        lines.append("**细项原因（逐条规则证据，可追溯）**")
        lines.append("")
        for d in evaluation.get("dimension_scores", []):
            traces = rule_trace.get(d["id"], [])
            if not traces:
                continue
            lines.append(f"- **{d['name']}（{d['score']} 分）**")
            for t in traces:
                ev = t.get("evidence") or [""]
                lines.append(f"  - {t.get('label', t.get('type', ''))}（{t['score']} 分）：{ev[0]}")
        lines.append("")
    return lines


def format_quick_report(evaluation: dict, jd_text: str, questions_md: str) -> str:
    """首轮诊断报告（一体化三部分：①评分+细项原因 ②可能问到的问题 ③综合判断）。"""
    total = evaluation.get("total_score", 0)
    lines = ["# 简历 × JD 首轮诊断报告", ""]
    lines.append(
        f"**综合评分：{total} / 100**　**等级：{_level(total)}**　**匹配度：{_match_level(total)}**"
    )
    lines.append("")
    lines.append(
        "> 本报告为首轮沟通一体化诊断，共 3 部分：① 简历评分与细项原因描述 ② 可能问到的问题 ③ 综合判断。"
        "全部得分由本地规则引擎计算，零大模型依赖、可追溯。"
    )
    lines.append("")

    lines.append("## 一、简历评分与细项原因描述")
    lines.append("")
    lines.extend(_render_score_section(evaluation, detailed=True))

    lines.append("## 二、可能问到的问题（按 JD 匹配度与简历短板排序）")
    lines.append("")
    qs = extract_questions(questions_md, 8)
    if qs:
        for i, q in enumerate(qs, 1):
            lines.append(f"{i}. {q}")
    else:
        lines.append("（暂无生成结果，可运行 --stage all 获取完整题库）")
    lines.append("")

    lines.append("## 三、综合判断")
    lines.append("")
    lines.extend(build_judgement(evaluation))
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("> 完整逐条评分依据见 `01_评分报告.md`；完整模拟面试题库见 `04_模拟面试题.md`（`--stage all` 生成）。")
    lines.append("")
    return "\n".join(lines)


def append_diagnosis_section(optimized_resume: str, evaluation: dict, questions_md: str) -> str:
    """在优化后简历文档末尾追加三部分（每轮优化简历后输出结构恒含三部分）。"""
    lines = [optimized_resume.rstrip(), "", "---", "", "## 本轮优化后的三部分诊断", ""]

    lines.append("### ① 简历评分与细项原因描述")
    lines.append("")
    lines.extend(_render_score_section(evaluation, detailed=True))

    lines.append("### ② 可能问到的问题（Top 5）")
    lines.append("")
    qs = extract_questions(questions_md, 5)
    if qs:
        for i, q in enumerate(qs, 1):
            lines.append(f"{i}. {q}")
    else:
        lines.append("（暂无，可运行 --stage all 生成完整题库）")
    lines.append("")

    lines.append("### ③ 综合判断")
    lines.append("")
    lines.extend(build_judgement(evaluation))
    lines.append("")
    return "\n".join(lines)
