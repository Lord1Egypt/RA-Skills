#!/usr/bin/env python3
"""
Human Review Receipt - P2 Engineering Enhancement

人工抽检/审查结果接入接口，产出 machine-readable receipt/decision artifact。

设计目标:
1. 最小化 UI 依赖：不要求完整 UI，但可以接受人工输入
2. Machine-readable：产出结构化 JSON receipt，可被程序处理
3. 可追溯：保留审查者、时间、决策依据等元数据
4. 可合并：支持多个人工审查结果合并到最终判定

使用场景:
- 关键 Skill 发布前的人工抽检
- 自动化评估边界案例的人工复核
- 争议性评估结果的人工仲裁
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json
import hashlib


class ReviewDecision(Enum):
    """人工审查决策类型"""
    APPROVED = "approved"           # 批准通过
    REJECTED = "rejected"           # 拒绝
    NEEDS_REVISION = "needs_revision"  # 需要修改
    ESCALATED = "escalated"         # 升级处理
    DEFERRED = "deferred"           # 暂缓决定


class ReviewSeverity(Enum):
    """问题严重程度"""
    CRITICAL = "critical"   # 严重：必须修复
    MAJOR = "major"         # 主要：应该修复
    MINOR = "minor"         # 次要：可以修复
    COSMETIC = "cosmetic"   # 外观：可选修复


@dataclass(frozen=True)
class ReviewFinding:
    """
    审查发现的问题/发现 (不可变)

    Attributes:
        id: 发现 ID
        category: 问题类别
        severity: 严重程度
        title: 问题标题
        description: 详细描述
        evidence: 证据/示例
        recommendation: 改进建议
        location: 问题位置 (文件/行号等)
    """
    id: str
    category: str
    severity: ReviewSeverity
    title: str
    description: str
    evidence: str = ""
    recommendation: str = ""
    location: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "location": self.location,
        }


@dataclass
class HumanReviewReceipt:
    """
    人工审查回执 (machine-readable decision artifact)

    Attributes:
        receipt_id: 回执 ID (唯一标识)
        skill_name: 被审查的 Skill 名称
        skill_version: Skill 版本
        reviewer_id: 审查者 ID
        reviewer_name: 审查者姓名
        decision: 审查决策
        confidence: 置信度 (0.0 - 1.0)
        findings: 发现的问题列表
        comments: 审查意见
        automated_score_reference: 引用的自动化评分
        manual_override: 是否人工覆盖了自动化结果
        final_score: 最终评分 (可能经过人工调整)
        requires_followup: 是否需要后续跟进
        followup_deadline: 跟进截止时间
        metadata: 附加元数据
        created_at: 创建时间
        signature: 数字签名 (用于验证完整性)
    """
    receipt_id: str
    skill_name: str
    skill_version: str
    reviewer_id: str
    reviewer_name: str
    decision: ReviewDecision
    confidence: float = 0.8
    findings: List[ReviewFinding] = field(default_factory=list)
    comments: str = ""
    automated_score_reference: Optional[Dict[str, Any]] = None
    manual_override: bool = False
    final_score: Optional[float] = None
    requires_followup: bool = False
    followup_deadline: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    signature: str = ""

    def __post_init__(self):
        assert 0.0 <= self.confidence <= 1.0, "Confidence must be in [0, 1]"
        if self.final_score is not None:
            assert 0.0 <= self.final_score <= 1.0, "Final score must be in [0, 1]"
        # Don't auto-compute signature in __post_init__ for frozen dataclass
        # Signature will be computed when save() is called or explicitly requested

    def _compute_signature(self) -> str:
        """计算回执的数字签名 (用于验证完整性)"""
        content = json.dumps({
            "receipt_id": self.receipt_id,
            "skill_name": self.skill_name,
            "skill_version": self.skill_version,
            "reviewer_id": self.reviewer_id,
            "decision": self.decision.value,
            "final_score": self.final_score,
            "created_at": self.created_at,
            "findings_count": len(self.findings),
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def verify_signature(self) -> bool:
        """验证签名是否有效"""
        return self.signature == self._compute_signature()

    def add_finding(self, finding: ReviewFinding) -> None:
        """添加审查发现的问题"""
        self.findings.append(finding)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "receipt_id": self.receipt_id,
            "skill_name": self.skill_name,
            "skill_version": self.skill_version,
            "reviewer": {
                "id": self.reviewer_id,
                "name": self.reviewer_name,
            },
            "decision": {
                "type": self.decision.value,
                "confidence": self.confidence,
                "manual_override": self.manual_override,
            },
            "findings": [f.to_dict() for f in self.findings],
            "comments": self.comments,
            "automated_score_reference": self.automated_score_reference,
            "final_score": self.final_score,
            "followup": {
                "required": self.requires_followup,
                "deadline": self.followup_deadline,
            },
            "metadata": self.metadata,
            "created_at": self.created_at,
            "signature": self.signature,
            "signature_valid": self.verify_signature(),
        }

    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: Union[str, Path]) -> str:
        """
        保存回执到文件

        Args:
            path: 输出文件路径

        Returns:
            保存的文件路径
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Compute signature before saving
        object.__setattr__(self, 'signature', self._compute_signature())

        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())

        return str(path)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "HumanReviewReceipt":
        """
        从文件加载回执

        Args:
            path: 文件路径

        Returns:
            加载的回执实例
        """
        path = Path(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 重建枚举类型
        decision = ReviewDecision(data["decision"]["type"])
        findings = [
            ReviewFinding(
                id=f["id"],
                category=f["category"],
                severity=ReviewSeverity(f["severity"]),
                title=f["title"],
                description=f["description"],
                evidence=f.get("evidence", ""),
                recommendation=f.get("recommendation", ""),
                location=f.get("location", ""),
            )
            for f in data.get("findings", [])
        ]

        return cls(
            receipt_id=data["receipt_id"],
            skill_name=data["skill_name"],
            skill_version=data["skill_version"],
            reviewer_id=data["reviewer"]["id"],
            reviewer_name=data["reviewer"]["name"],
            decision=decision,
            confidence=data["decision"]["confidence"],
            findings=findings,
            comments=data.get("comments", ""),
            automated_score_reference=data.get("automated_score_reference"),
            manual_override=data["decision"]["manual_override"],
            final_score=data.get("final_score"),
            requires_followup=data["followup"]["required"],
            followup_deadline=data["followup"]["deadline"],
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", ""),
            signature=data.get("signature", ""),
        )


class HumanReviewManager:
    """
    人工审查管理器

    管理多个人工审查回执，支持合并和汇总。

    使用示例:
        manager = HumanReviewManager()
        
        # 创建审查回执
        receipt = manager.create_receipt(
            skill_name="my-skill",
            skill_version="1.0.0",
            reviewer_id="reviewer-001",
            reviewer_name="张三",
            decision=ReviewDecision.APPROVED,
        )
        
        # 添加发现的问题
        receipt.add_finding(ReviewFinding(
            id="finding-001",
            category="performance",
            severity=ReviewSeverity.MINOR,
            title="响应时间略高",
            description="在某些边界情况下响应时间超过 1 秒",
        ))
        
        # 保存回执
        receipt.save("reviews/my-skill-review-001.json")
        
        # 加载已有回执
        manager.load_receipt("reviews/my-skill-review-001.json")
        
        # 获取汇总
        summary = manager.get_summary()
    """

    def __init__(self):
        self._receipts: Dict[str, HumanReviewReceipt] = {}

    def create_receipt(
        self,
        skill_name: str,
        skill_version: str,
        reviewer_id: str,
        reviewer_name: str,
        decision: ReviewDecision,
        confidence: float = 0.8,
        comments: str = "",
        automated_score_reference: Optional[Dict[str, Any]] = None,
        manual_override: bool = False,
        final_score: Optional[float] = None,
        requires_followup: bool = False,
        followup_deadline: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> HumanReviewReceipt:
        """
        创建新的审查回执

        Args:
            skill_name: Skill 名称
            skill_version: Skill 版本
            reviewer_id: 审查者 ID
            reviewer_name: 审查者姓名
            decision: 审查决策
            confidence: 置信度
            comments: 审查意见
            automated_score_reference: 引用的自动化评分
            manual_override: 是否人工覆盖
            final_score: 最终评分
            requires_followup: 是否需要跟进
            followup_deadline: 跟进截止时间
            metadata: 附加元数据

        Returns:
            创建的审查回执
        """
        receipt_id = f"review-{skill_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        receipt = HumanReviewReceipt(
            receipt_id=receipt_id,
            skill_name=skill_name,
            skill_version=skill_version,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            decision=decision,
            confidence=confidence,
            comments=comments,
            automated_score_reference=automated_score_reference,
            manual_override=manual_override,
            final_score=final_score,
            requires_followup=requires_followup,
            followup_deadline=followup_deadline,
            metadata=metadata or {},
        )

        self._receipts[receipt_id] = receipt
        return receipt

    def add_receipt(self, receipt: HumanReviewReceipt) -> None:
        """添加已有的审查回执"""
        self._receipts[receipt.receipt_id] = receipt

    def load_receipt(self, path: Union[str, Path]) -> HumanReviewReceipt:
        """
        从文件加载审查回执

        Args:
            path: 文件路径

        Returns:
            加载的审查回执
        """
        receipt = HumanReviewReceipt.load(path)
        self._receipts[receipt.receipt_id] = receipt
        return receipt

    def get_receipt(self, receipt_id: str) -> Optional[HumanReviewReceipt]:
        """获取指定的审查回执"""
        return self._receipts.get(receipt_id)

    def get_all_receipts(self) -> List[HumanReviewReceipt]:
        """获取所有审查回执"""
        return list(self._receipts.values())

    def get_summary(self) -> Dict[str, Any]:
        """获取所有审查回执的汇总统计"""
        if not self._receipts:
            return {
                "total_reviews": 0,
                "by_decision": {},
                "avg_confidence": 0.0,
                "total_findings": 0,
                "by_severity": {},
            }

        receipts = list(self._receipts.values())
        by_decision = {}
        by_severity = {}
        total_findings = 0

        for receipt in receipts:
            # 统计决策
            decision_key = receipt.decision.value
            by_decision[decision_key] = by_decision.get(decision_key, 0) + 1

            # 统计问题
            total_findings += len(receipt.findings)
            for finding in receipt.findings:
                severity_key = finding.severity.value
                by_severity[severity_key] = by_severity.get(severity_key, 0) + 1

        avg_confidence = sum(r.confidence for r in receipts) / len(receipts)

        return {
            "total_reviews": len(receipts),
            "by_decision": by_decision,
            "avg_confidence": round(avg_confidence, 4),
            "total_findings": total_findings,
            "by_severity": by_severity,
            "manual_overrides": sum(1 for r in receipts if r.manual_override),
        }

    def merge_scores(
        self,
        base_score: float,
        review_weight: float = 0.3,
        use_final_scores: bool = True,
    ) -> float:
        """
        将人工审查结果合并到基础评分中

        Args:
            base_score: 基础评分 (来自自动化评估)
            review_weight: 人工审查权重 (0.0 - 1.0)
            use_final_scores: 是否使用人工指定的 final_score

        Returns:
            合并后的最终评分
        """
        if not self._receipts:
            return base_score

        if use_final_scores:
            # 使用人工指定的 final_score
            final_scores = []
            for r in self._receipts.values():
                if hasattr(r, 'final_score') and r.final_score is not None:
                    final_scores.append(r.final_score)
                elif isinstance(r, dict) and r.get('final_score') is not None:
                    final_scores.append(r['final_score'])
            
            if final_scores:
                review_score = sum(final_scores) / len(final_scores)
            else:
                # 如果没有 final_score，根据决策转换
                review_score = self._decision_to_score()
        else:
            review_score = self._decision_to_score()

        return base_score * (1 - review_weight) + review_score * review_weight

    def _decision_to_score(self) -> float:
        """将审查决策转换为分数"""
        if not self._receipts:
            return 0.0

        decision_scores = {
            ReviewDecision.APPROVED: 1.0,
            ReviewDecision.REJECTED: 0.0,
            ReviewDecision.NEEDS_REVISION: 0.5,
            ReviewDecision.ESCALATED: 0.3,
            ReviewDecision.DEFERRED: 0.5,
        }

        total = 0.0
        for receipt_id, receipt in self._receipts.items():
            # Handle both HumanReviewReceipt objects and dict representations
            if hasattr(receipt, 'decision'):
                # It's a HumanReviewReceipt object
                decision_value = receipt.decision
                confidence = receipt.confidence
            elif isinstance(receipt, dict):
                # It's a dict representation
                decision_value = receipt.get('decision', ReviewDecision.APPROVED)
                confidence = receipt.get('confidence', 0.8)
            else:
                continue
            
            if isinstance(decision_value, str):
                decision_value = ReviewDecision(decision_value)
            
            base_score = decision_scores.get(decision_value, 0.5)
            # 考虑置信度
            total += base_score * confidence

        return total / len(self._receipts)

    def export_report(self, output_path: Union[str, Path], format: str = "json") -> str:
        """
        导出审查报告

        Args:
            output_path: 输出文件路径
            format: 输出格式 ("json" 或 "markdown")

        Returns:
            输出文件路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            data = {
                "summary": self.get_summary(),
                "receipts": [r.to_dict() for r in self._receipts.values()],
                "generated_at": datetime.now().isoformat(),
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        elif format == "markdown":
            md_content = self._generate_markdown_report()
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
        else:
            raise ValueError(f"Unknown format: {format}")

        return str(output_path)

    def _generate_markdown_report(self) -> str:
        """生成 Markdown 格式报告"""
        summary = self.get_summary()

        lines = [
            "# Human Review Report",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- **Total Reviews**: {summary['total_reviews']}",
            f"- **Average Confidence**: {summary['avg_confidence']:.2%}",
            f"- **Total Findings**: {summary['total_findings']}",
            f"- **Manual Overrides**: {summary['manual_overrides']}",
            "",
            "### Decisions",
            "",
        ]

        for decision, count in summary["by_decision"].items():
            lines.append(f"- {decision}: {count}")

        lines.extend([
            "",
            "### Findings by Severity",
            "",
        ])

        for severity, count in summary["by_severity"].items():
            lines.append(f"- {severity}: {count}")

        lines.extend([
            "",
            "## Individual Reviews",
            "",
        ])

        for receipt in self._receipts.values():
            lines.extend([
                f"### {receipt.receipt_id}",
                "",
                f"- **Skill**: {receipt.skill_name} v{receipt.skill_version}",
                f"- **Reviewer**: {receipt.reviewer_name} ({receipt.reviewer_id})",
                f"- **Decision**: {receipt.decision.value} (confidence: {receipt.confidence:.2%})",
                f"- **Final Score**: {receipt.final_score if receipt.final_score else 'N/A'}",
                f"- **Manual Override**: {receipt.manual_override}",
                "",
            ])

            if receipt.findings:
                lines.append("**Findings**:")
                lines.append("")
                for finding in receipt.findings:
                    lines.extend([
                        f"- **[{finding.severity.value.upper()}]** {finding.title}",
                        f"  - {finding.description}",
                        f"  - Recommendation: {finding.recommendation}",
                    ])
                lines.append("")

            if receipt.comments:
                lines.extend([
                    "**Comments**:",
                    "",
                    f"> {receipt.comments}",
                    "",
                ])

        return "\n".join(lines)


# 辅助函数

def create_review_finding(
    category: str,
    severity: ReviewSeverity,
    title: str,
    description: str,
    evidence: str = "",
    recommendation: str = "",
    location: str = "",
) -> ReviewFinding:
    """
    创建审查发现的辅助函数

    Args:
        category: 问题类别
        severity: 严重程度
        title: 问题标题
        description: 详细描述
        evidence: 证据/示例
        recommendation: 改进建议
        location: 问题位置

    Returns:
        审查发现
    """
    finding_id = f"finding-{category}-{datetime.now().strftime('%H%M%S')}"

    return ReviewFinding(
        id=finding_id,
        category=category,
        severity=severity,
        title=title,
        description=description,
        evidence=evidence,
        recommendation=recommendation,
        location=location,
    )
