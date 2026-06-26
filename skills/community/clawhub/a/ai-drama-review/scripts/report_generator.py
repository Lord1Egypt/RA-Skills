"""
合规报告生成器

生成结构化 JSON 报告和可读 Markdown 报告。
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class ComplianceReport:
    """完整合规报告。"""
    report_id: str = ""
    generated_at: str = ""
    input_file: str = ""
    overall_risk_level: str = "low"  # "low"/"medium"/"high"/"critical"
    overall_score: float = 100.0     # 0-100 合规得分（越高越合规）

    copyright_result: Optional[dict] = None
    age_rating_result: Optional[dict] = None
    adaptation_result: Optional[dict] = None

    violation_summary: List[dict] = field(default_factory=list)
    remediation_suggestions: List[str] = field(default_factory=list)


def calculate_overall_risk(copyright_result: dict = None,
                           age_rating_result: dict = None,
                           adaptation_result: dict = None) -> tuple:
    """
    计算总体风险等级和合规得分。

    Returns:
        (risk_level, score)
    """
    risk_scores = []  # 各模块的风险分（越高越危险）

    if copyright_result:
        level = copyright_result.get("risk_level", "low")
        level_map = {"low": 0, "medium": 30, "high": 60, "critical": 90}
        risk_scores.append(level_map.get(level, 0))

    if age_rating_result:
        if not age_rating_result.get("is_compliant", True):
            level = age_rating_result.get("risk_level", "low")
            level_map = {"low": 0, "medium": 30, "high": 60, "critical": 90}
            risk_scores.append(level_map.get(level, 0))
        else:
            risk_scores.append(0)

    if adaptation_result:
        score = adaptation_result.get("deviation_score", 0)
        if score >= 60:
            risk_scores.append(70)
        elif score >= 30:
            risk_scores.append(30)
        else:
            risk_scores.append(0)

    if not risk_scores:
        return "low", 100.0

    max_risk = max(risk_scores)
    avg_risk = sum(risk_scores) / len(risk_scores)

    # 综合风险：最大风险权重 0.7 + 平均风险 0.3
    combined_risk = max_risk * 0.7 + avg_risk * 0.3

    if combined_risk >= 70:
        risk_level = "critical"
    elif combined_risk >= 45:
        risk_level = "high"
    elif combined_risk >= 20:
        risk_level = "medium"
    else:
        risk_level = "low"

    compliance_score = max(0, 100 - combined_risk)
    return risk_level, round(compliance_score, 1)


def _build_violation_summary(copyright_result: dict = None,
                             age_rating_result: dict = None,
                             adaptation_result: dict = None) -> List[dict]:
    """构建违规摘要列表。"""
    violations = []

    if copyright_result and copyright_result.get("suspicious_paragraphs", 0) > 0:
        violations.append({
            "type": "copyright",
            "severity": copyright_result.get("risk_level", "medium"),
            "description": (
                f"发现 {copyright_result['suspicious_paragraphs']} 个疑似侵权段落，"
                f"最高相似度 {copyright_result.get('max_similarity_score', 0):.2f}"
            ),
        })

    if age_rating_result and not age_rating_result.get("is_compliant", True):
        violations.append({
            "type": "age_rating",
            "severity": age_rating_result.get("risk_level", "medium"),
            "description": (
                f"内容建议分级 {age_rating_result.get('suggested_rating', '未知')}，"
                f"超出目标分级 {age_rating_result.get('target_rating', '未知')}，"
                f"共 {age_rating_result.get('total_hits', 0)} 处命中"
            ),
        })

    if adaptation_result and adaptation_result.get("deviation_score", 0) >= 60:
        violations.append({
            "type": "adaptation",
            "severity": "high",
            "description": (
                f"改编偏离度 {adaptation_result['deviation_score']}/100，"
                f"属于{_translate_adaptation_type(adaptation_result.get('adaptation_type', ''))}，"
                f"共 {adaptation_result.get('total_deviations', 0)} 处偏离"
            ),
        })

    return violations


def _translate_adaptation_type(t: str) -> str:
    """翻译改编类型。"""
    types = {
        "faithful": "忠实改编",
        "reasonable": "合理改编",
        "severe_modification": "严重魔改",
    }
    return types.get(t, t)


def _build_remediation(violations: List[dict]) -> List[str]:
    """根据违规摘要生成整改建议。"""
    suggestions = []

    for v in violations:
        if v["type"] == "copyright":
            suggestions.append("对疑似侵权段落进行原创性改写，避免与已有作品高度相似")
            suggestions.append("核实参考来源的版权状态，确认是否需要获取授权")
        elif v["type"] == "age_rating":
            suggestions.append("修改或删除不符合目标年龄分级的内容")
            suggestions.append("对暴力/恐怖/不当场景进行弱化处理")
        elif v["type"] == "adaptation":
            suggestions.append("重新审视对原著核心情节的改动，确保改编的合理性")
            suggestions.append("考虑获取原著权利人的改编授权")

    if not suggestions:
        suggestions.append("当前内容未发现明显违规，建议定期复查")

    return list(dict.fromkeys(suggestions))  # 去重保序


def generate_json_report(report: ComplianceReport) -> str:
    """生成 JSON 格式报告。"""
    data = {
        "report_id": report.report_id,
        "generated_at": report.generated_at,
        "input_file": report.input_file,
        "overall_risk_level": report.overall_risk_level,
        "overall_score": report.overall_score,
        "violation_summary": report.violation_summary,
        "remediation_suggestions": report.remediation_suggestions,
    }
    if report.copyright_result:
        data["copyright_detection"] = report.copyright_result
    if report.age_rating_result:
        data["age_rating_scan"] = report.age_rating_result
    if report.adaptation_result:
        data["adaptation_detection"] = report.adaptation_result

    return json.dumps(data, ensure_ascii=False, indent=2)


def generate_markdown_report(report: ComplianceReport) -> str:
    """生成 Markdown 可读报告。"""
    lines = [
        f"# AI短剧合规审查报告",
        f"",
        f"**报告 ID**: {report.report_id}",
        f"**生成时间**: {report.generated_at}",
        f"**输入文件**: {report.input_file}",
        f"",
        f"## 总体评估",
        f"",
        f"| 项目 | 结果 |",
        f"|------|------|",
        f"| 风险等级 | **{report.overall_risk_level.upper()}** |",
        f"| 合规得分 | {report.overall_score}/100 |",
        f"",
    ]

    if report.violation_summary:
        lines.append("## 违规摘要")
        lines.append("")
        for v in report.violation_summary:
            emoji = {"low": "!", "medium": "!!", "high": "!!!", "critical": "!!!!"}
            lines.append(f"- [{v['severity'].upper()}] **{v['type']}**: {v['description']}")
        lines.append("")

    if report.copyright_result:
        cr = report.copyright_result
        lines.append("## 版权侵权检测")
        lines.append("")
        lines.append(f"- 总段落数: {cr.get('total_paragraphs', 0)}")
        lines.append(f"- 可疑段落: {cr.get('suspicious_paragraphs', 0)}")
        lines.append(f"- 最高相似度: {cr.get('max_similarity_score', 0):.4f}")
        lines.append(f"- 风险等级: {cr.get('risk_level', 'low')}")
        lines.append("")

    if report.age_rating_result:
        ar = report.age_rating_result
        lines.append("## 年龄分级合规")
        lines.append("")
        lines.append(f"- 建议分级: {ar.get('suggested_rating', 'N/A')}")
        lines.append(f"- 目标分级: {ar.get('target_rating', 'N/A')}")
        lines.append(f"- 是否合规: {'是' if ar.get('is_compliant') else '否'}")
        lines.append(f"- 总命中数: {ar.get('total_hits', 0)}")
        lines.append("")

    if report.adaptation_result:
        ad = report.adaptation_result
        lines.append("## 小说改编检测")
        lines.append("")
        lines.append(f"- 偏离度: {ad.get('deviation_score', 0)}/100")
        lines.append(f"- 改编类型: {_translate_adaptation_type(ad.get('adaptation_type', ''))}")
        lines.append(f"- 总偏离数: {ad.get('total_deviations', 0)}")
        lines.append("")

    lines.append("## 整改建议")
    lines.append("")
    for i, suggestion in enumerate(report.remediation_suggestions, 1):
        lines.append(f"{i}. {suggestion}")
    lines.append("")

    lines.append("---")
    lines.append("*本报告由 ai-drama-review 自动生成，仅供参考，不作为法律依据。*")

    return "\n".join(lines)


def generate_violation_annotations(report: ComplianceReport) -> list:
    """生成违规位置标注列表。"""
    annotations = []

    if report.copyright_result:
        for r in report.copyright_result.get("results", []):
            annotations.append({
                "type": "copyright",
                "location": {"paragraph": r.get("source_paragraph_index", 0)},
                "severity": "high" if r.get("combined_score", 0) >= 0.85 else "medium",
                "description": (
                    f"与 {r.get('reference_id', '未知')} 相似度 "
                    f"{r.get('combined_score', 0):.2f}"
                ),
            })

    if report.age_rating_result:
        for hit in report.age_rating_result.get("keyword_hits", []):
            annotations.append({
                "type": "age_rating",
                "location": {
                    "paragraph": hit.get("paragraph_index", 0),
                    "timestamp": hit.get("timestamp"),
                },
                "severity": hit.get("severity", "mild"),
                "description": (
                    f"[{hit.get('category', '')}] "
                    f"关键词 '{hit.get('keyword', '')}'"
                ),
            })

    return annotations


def build_full_report(input_file: str, copyright_result=None,
                      age_rating_result=None,
                      adaptation_result=None) -> ComplianceReport:
    """汇总所有检测结果，构建完整报告。"""
    risk_level, score = calculate_overall_risk(
        copyright_result, age_rating_result, adaptation_result
    )

    violations = _build_violation_summary(
        copyright_result, age_rating_result, adaptation_result
    )
    remediation = _build_remediation(violations)

    report = ComplianceReport(
        report_id=f"DR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        generated_at=datetime.now().isoformat(),
        input_file=input_file,
        overall_risk_level=risk_level,
        overall_score=score,
        copyright_result=copyright_result,
        age_rating_result=age_rating_result,
        adaptation_result=adaptation_result,
        violation_summary=violations,
        remediation_suggestions=remediation,
    )

    return report
