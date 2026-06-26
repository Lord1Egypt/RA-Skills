"""
报告生成器 - 生成结构化的评估报告
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class ReportGenerator:
    """评估报告生成器"""

    def __init__(self, template_dir: Optional[str] = None):
        self.template_dir = Path(template_dir) if template_dir else None

    def generate_audit_report(
        self,
        audit_result,
        candidate_info: Optional[Dict] = None,
        candidate_id: str = "",
    ) -> str:
        """生成简历审计报告（模式A）"""
        logger.info("生成简历审计报告...")

        lines = []
        lines.append("# AI人才简历审计报告\n")
        lines.append("## 基本信息")
        lines.append(f"- 评估时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"- 候选人编号: {candidate_id or candidate_info.get('candidate_id', 'N/A')}")
        lines.append(f"- 审计模式: 仅简历审计\n")

        # 审计结果
        lines.append("---\n")
        lines.append("## 一、简历漏洞穿透审计\n")

        # 按类别分组
        issues_by_category = {}
        for issue in audit_result.issues:
            cat = issue.category
            if cat not in issues_by_category:
                issues_by_category[cat] = []
            issues_by_category[cat].append(issue)

        for idx, (category, issues) in enumerate(issues_by_category.items(), 1):
            lines.append(f"### 1.{idx} {category}")
            for issue in issues:
                icon = "🔴" if issue.risk_level.value == "高嫌疑" else "🟡" if issue.risk_level.value == "中嫌疑" else "🟢"
                lines.append(f"- {icon} **{issue.risk_level.value}**: {issue.description}")
                lines.append(f"  - 证据: {issue.evidence}")
                if issue.suggested_question:
                    lines.append(f"  - 建议追问: {issue.suggested_question}")
            lines.append("")

        # 综合结论
        lines.append("---\n")
        lines.append("## 二、综合审计结论\n")
        lines.append("| 指标 | 结果 |")
        lines.append("|------|------|")
        for category, issues in issues_by_category.items():
            high_count = sum(1 for i in issues if i.risk_level.value == "高嫌疑")
            med_count = sum(1 for i in issues if i.risk_level.value == "中嫌疑")
            status = "🔴 有问题" if high_count > 0 else "🟡 需关注" if med_count > 0 else "🟢 正常"
            lines.append(f"| {category} | {status} |")

        lines.append(f"| **综合结论** | **{audit_result.overall_conclusion.value}** |")
        lines.append(f"| 审计可信度 | {audit_result.confidence_score:.0%} |\n")

        # 测谎面试题
        lines.append("---\n")
        lines.append("## 三、定制化测谎面试题\n")
        for idx, q in enumerate(audit_result.lie_detection_questions, 1):
            lines.append(f"### 追问{idx}（{q.question_type}）")
            lines.append(f"> {q.content}\n")

        return '\n'.join(lines)

    def generate_full_report(
        self,
        evaluation_result,
        audit_result,
        cross_verification=None,
        candidate_info: Optional[Dict] = None,
        candidate_id: str = "",
        source_files: Optional[List[str]] = None,
    ) -> str:
        """生成完整定级报告（模式B）"""
        logger.info("生成完整定级报告...")

        lines = []
        lines.append("# AI人才完整定级报告\n")
        lines.append("## 基本信息")
        lines.append(f"- 候选人ID: {candidate_id}")
        lines.append(f"- 评估时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if source_files:
            lines.append(f"- 数据来源: {', '.join(source_files)}")
        lines.append(f"- 评估模式: 完整定级\n")

        # ===== 简历审计摘要 =====
        lines.append("---\n")
        lines.append("## 一、简历审计结果\n")

        high_issues = [i for i in audit_result.issues if i.risk_level.value == "高嫌疑"]
        med_issues = [i for i in audit_result.issues if i.risk_level.value == "中嫌疑"]

        lines.append(f"- 审计结论: **{audit_result.overall_conclusion.value}**")
        lines.append(f"- 高嫌疑指标: {len(high_issues)} 项")
        lines.append(f"- 中嫌疑指标: {len(med_issues)} 项\n")

        if high_issues:
            lines.append("### 关键疑点")
            for issue in high_issues:
                lines.append(f"- 🔴 [{issue.category}] {issue.description}")
            lines.append("")

        # ===== 面试交叉验证 =====
        if cross_verification:
            lines.append("---\n")
            lines.append("## 二、面试交叉验证\n")
            lines.append("### 疑点处理统计\n")
            lines.append(f"| 状态 | 数量 |")
            lines.append(f"|------|------|")
            lines.append(f"| 已覆盖 | {cross_verification.covered} |")
            lines.append(f"| 已确认（存疑） | {cross_verification.confirmed} |")
            lines.append(f"| 已排除 | {cross_verification.excluded} |")
            lines.append(f"| 待验证 | {cross_verification.pending} |")
            lines.append(f"| 未覆盖 | {cross_verification.not_covered} |\n")

            if cross_verification.not_covered > 0:
                lines.append("### ⚠️ 未覆盖疑点")
                for item in cross_verification.items:
                    if item.status.value == "未覆盖":
                        lines.append(f"- {item.audit_issue[:80]}...")
                lines.append("")

        # ===== 六维度评估 =====
        lines.append("---\n")
        lines.append("## 三、六维度评估\n")
        lines.append("| 维度 | 得分 | 认知层级 | 评估依据 |")
        lines.append("|------|------|---------|---------|")

        for score in evaluation_result.dimension_scores:
            lines.append(
                f"| {score.dimension} | {score.score:.0f}/4 | {score.cognitive_level} | {score.evidence[:60]} |"
            )
        lines.append(f"\n**能力平均分**: {evaluation_result.weighted_result.average_score}\n")

        # ===== 加权计算 =====
        wr = evaluation_result.weighted_result
        lines.append("---\n")
        lines.append("## 四、加权计算\n")
        lines.append("| 因子 | 等级 | 系数/调整 | 说明 |")
        lines.append("|------|------|----------|------|")
        lines.append(f"| 环境复杂度 | {wr.env_complexity} | ×{wr.env_coefficient} | - |")
        lines.append(f"| 个人杠杆率 | {wr.leverage_level} | ×{wr.leverage_coefficient} | - |")
        lines.append(f"| 成长速度 | {wr.growth_level} | {wr.growth_adjustment:+.1f} | - |\n")

        lines.append("```")
        lines.append(
            f"({wr.average_score} × {wr.env_coefficient} × {wr.leverage_coefficient})"
            f" + ({wr.growth_adjustment:+.1f}) = {wr.weighted_score}"
        )
        lines.append(f"加权后得分: {wr.weighted_score} × 4 = {wr.final_score}")
        lines.append("```\n")

        # ===== 定级结果 =====
        lines.append("---\n")
        lines.append("## 五、定级结果\n")
        grade = evaluation_result.final_grade

        lines.append("| 项目 | 内容 |")
        lines.append("|------|------|")
        lines.append(f"| **最终级别** | **L{grade.level}** |")
        lines.append(f"| 级别名称 | {grade.level_name} |")
        lines.append(f"| P序列参考 | {grade.p_level} |")
        lines.append(f"| 级别定义 | {grade.definition} |\n")

        if grade.notes:
            lines.append("### 特殊标注")
            for note in grade.notes:
                lines.append(f"- {note}")
            lines.append("")

        if grade.is_downgraded:
            lines.append("> ⚠️ 降级说明：原始评估达L4，但因硬性门槛不满足而降级\n")

        # ===== v3.2 评分一致性检验 =====
        final_score = wr.final_score
        dim_scores = [s.score for s in evaluation_result.dimension_scores]
        max_dim = max(dim_scores)
        min_dim = min(dim_scores)
        dim_gap = max_dim - min_dim

        if final_score >= 13 or final_score <= 7:
            lines.append("### 🔍 评分一致性检验（v3.2）\n")
            lines.append(f"> 综合得分 {final_score} 属于极端区间（≥13 或 ≤7），触发一致性检验：")
            if final_score >= 13:
                lines.append(f"- 高分置信度: 请确认所有高维度均有充分证据支撑，非凭感觉打分")
            else:
                lines.append(f"- 低分说明: 请确认低分维度是否因信息不足，如有请标注'待补充'")
            lines.append(f"- 最高维度: {max_dim}/4，最低维度: {min_dim}/4")
            lines.append("")

        if dim_gap >= 2:
            lines.append("### ⚠️ 非均衡型标注\n")
            max_idx = dim_scores.index(max_dim)
            min_idx = dim_scores.index(min_dim)
            max_name = evaluation_result.dimension_scores[max_idx].dimension
            min_name = evaluation_result.dimension_scores[min_idx].dimension
            lines.append(f"- 最高维度: {max_name} ({max_dim}/4)")
            lines.append(f"- 最低维度: {min_name} ({min_dim}/4)")
            lines.append(f"- 分差: {dim_gap} ≥ 2，需标注: {'潜力型' if max_dim >= 3 else '短板型'}")
            lines.append("")

        # ===== 风险提示 =====
        lines.append("---\n")
        lines.append("## 六、风险提示\n")
        if evaluation_result.risk_items:
            for risk in evaluation_result.risk_items:
                lines.append(f"- ⚠️ {risk}")
        else:
            lines.append("- 未发现显著风险项")
        lines.append("")

        # ===== 数据质量 =====
        dq = evaluation_result.data_quality
        lines.append("---\n")
        lines.append("## 七、数据质量评估\n")
        lines.append("| 维度 | 评分(1-5) |")
        lines.append("|------|----------|")
        lines.append(f"| 简历完整度 | {dq.get('resume_completeness', 3)} |")
        lines.append(f"| 面试记录质量 | {dq.get('interview_quality', 3)} |")
        lines.append(f"| 评估可信度 | {dq.get('confidence', 3)} |")

        return '\n'.join(lines)

    def generate_json(self, evaluation_result, audit_result, candidate_id: str = "") -> str:
        """生成JSON格式报告"""
        report = {
            'candidate_id': candidate_id,
            'timestamp': datetime.now().isoformat(),
            'audit': {
                'conclusion': audit_result.overall_conclusion.value,
                'confidence': audit_result.confidence_score,
                'high_suspicion_count': audit_result.high_suspicion_count,
                'medium_suspicion_count': audit_result.medium_suspicion_count,
            },
            'evaluation': {
                'dimensions': [
                    {
                        'name': s.dimension,
                        'score': s.score,
                        'cognitive_level': s.cognitive_level,
                    }
                    for s in evaluation_result.dimension_scores
                ],
                'weighted': {
                    'average_score': evaluation_result.weighted_result.average_score,
                    'env_complexity': evaluation_result.weighted_result.env_complexity,
                    'env_coefficient': evaluation_result.weighted_result.env_coefficient,
                    'leverage_level': evaluation_result.weighted_result.leverage_level,
                    'leverage_coefficient': evaluation_result.weighted_result.leverage_coefficient,
                    'growth_level': evaluation_result.weighted_result.growth_level,
                    'growth_adjustment': evaluation_result.weighted_result.growth_adjustment,
                    'final_score': evaluation_result.weighted_result.final_score,
                },
                'grade': {
                    'level': evaluation_result.final_grade.level,
                    'name': evaluation_result.final_grade.level_name,
                    'p_level': evaluation_result.final_grade.p_level,
                    'definition': evaluation_result.final_grade.definition,
                },
            },
            'risks': evaluation_result.risk_items,
            'data_quality': evaluation_result.data_quality,
        }
        return json.dumps(report, ensure_ascii=False, indent=2)

    def save_report(self, report: str, output_path: str, format: str = 'md'):
        """保存报告到文件"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"报告已保存: {output_path}")