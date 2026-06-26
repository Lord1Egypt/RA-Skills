"""
Models for Code Quality Guardian
数据模型
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


class Severity(Enum):
    """问题严重程度"""
    CRITICAL = 5  # 严重（安全漏洞）
    HIGH = 4      # 高
    MEDIUM = 3    # 中
    LOW = 2       # 低
    INFO = 1      # 信息/建议


class Category(Enum):
    """问题类别"""
    STYLE = "style"              # 代码风格
    COMPLEXITY = "complexity"    # 复杂度
    SECURITY = "security"        # 安全
    MAINTAINABILITY = "maintainability"  # 可维护性
    PERFORMANCE = "performance"  # 性能
    ERROR = "error"              # 错误


@dataclass
class Issue:
    """代码问题"""
    tool: str                           # 检测工具
    severity: Severity                  # 严重程度
    category: Category                  # 类别
    message: str                        # 描述信息
    file: str                           # 文件路径
    line: int = 0                       # 行号
    column: int = 0                     # 列号
    code: str = ""                      # 问题代码
    suggestion: str = ""                # 修复建议
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "tool": self.tool,
            "severity": self.severity.name,
            "category": self.category.value,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "code": self.code,
            "suggestion": self.suggestion,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Issue":
        """从字典创建"""
        return cls(
            tool=data["tool"],
            severity=Severity[data.get("severity", "INFO")],
            category=Category(data.get("category", "style")),
            message=data["message"],
            file=data["file"],
            line=data.get("line", 0),
            column=data.get("column", 0),
            code=data.get("code", ""),
            suggestion=data.get("suggestion", ""),
        )


@dataclass 
class FileMetrics:
    """文件指标"""
    path: str
    lines_of_code: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    complexity: float = 0.0
    maintainability_index: float = 0.0


@dataclass
class AnalysisResult:
    """分析结果"""
    files_analyzed: int = 0
    lines_of_code: int = 0
    total_issues: int = 0
    issues_by_severity: Dict[Severity, int] = field(default_factory=dict)
    issues_by_category: Dict[Category, int] = field(default_factory=dict)
    complexity_score: float = 0.0
    maintainability_rank: str = ""
    security_score: float = 100.0
    issues: List[Issue] = field(default_factory=list)
    file_metrics: List[FileMetrics] = field(default_factory=list)
    thresholds: Dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0
    
    def __post_init__(self):
        """初始化后的处理"""
        if not self.issues_by_severity:
            self.issues_by_severity = {s: 0 for s in Severity}
        if not self.issues_by_category:
            self.issues_by_category = {c: 0 for c in Category}
    
    @property
    def quality_score(self) -> float:
        """计算质量分数 (0-10)"""
        if self.total_issues == 0:
            return 10.0
        
        # 根据严重程度和问题数量计算分数
        weights = {
            Severity.CRITICAL: 10,
            Severity.HIGH: 5,
            Severity.MEDIUM: 2,
            Severity.LOW: 0.5,
            Severity.INFO: 0.1,
        }
        
        penalty = sum(
            self.issues_by_severity.get(s, 0) * w 
            for s, w in weights.items()
        )
        
        # 基于代码行数标准化
        if self.lines_of_code > 0:
            penalty = penalty / (self.lines_of_code / 100)
        
        score = max(0, 10 - penalty)
        return round(score, 1)
    
    @property
    def quality_rank(self) -> str:
        """获取质量等级"""
        score = self.quality_score
        if score >= 9:
            return "A+"
        elif score >= 8:
            return "A"
        elif score >= 7:
            return "B"
        elif score >= 6:
            return "C"
        elif score >= 5:
            return "D"
        else:
            return "F"
    
    @property
    def quality_gate_passed(self) -> bool:
        """检查是否通过质量门禁"""
        min_score = self.thresholds.get("min_quality_score", 0)
        if self.quality_score < min_score:
            return False
        
        max_complexity = self.thresholds.get("max_complexity", float("inf"))
        if self.complexity_score > max_complexity:
            return False
        
        fail_on = self.thresholds.get("fail_on", "high")
        fail_severity = Severity[fail_on.upper()] if fail_on != "never" else None
        
        if fail_severity:
            for severity, count in self.issues_by_severity.items():
                if severity.value >= fail_severity.value and count > 0:
                    return False
        
        return True
    
    @property
    def has_failures(self) -> bool:
        """是否有失败"""
        return not self.quality_gate_passed
    
    @property
    def failure_reason(self) -> str:
        """获取失败原因"""
        if self.quality_gate_passed:
            return ""
        
        reasons = []
        
        min_score = self.thresholds.get("min_quality_score", 0)
        if self.quality_score < min_score:
            reasons.append(f"质量分数 {self.quality_score} 低于阈值 {min_score}")
        
        max_complexity = self.thresholds.get("max_complexity", float("inf"))
        if self.complexity_score > max_complexity:
            reasons.append(f"复杂度 {self.complexity_score} 超过阈值 {max_complexity}")
        
        fail_on = self.thresholds.get("fail_on", "high")
        if fail_on != "never":
            fail_severity = Severity[fail_on.upper()]
            for severity, count in self.issues_by_severity.items():
                if severity.value >= fail_severity.value and count > 0:
                    reasons.append(f"发现 {count} 个 {severity.name} 级别问题")
        
        return "; ".join(reasons)
    
    @property
    def critical_issues(self) -> List[Issue]:
        """获取严重问题"""
        return [i for i in self.issues if i.severity == Severity.CRITICAL]
    
    @property
    def security_issues(self) -> List[Issue]:
        """获取安全问题"""
        return [i for i in self.issues if i.category == Category.SECURITY]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "meta": {
                "version": "1.0.0",
                "duration_ms": self.duration_ms,
            },
            "summary": {
                "files_analyzed": self.files_analyzed,
                "lines_of_code": self.lines_of_code,
                "total_issues": self.total_issues,
            },
            "issues": {
                "by_severity": {s.name: c for s, c in self.issues_by_severity.items()},
                "by_category": {c.value: n for c, n in self.issues_by_category.items()},
                "details": [i.to_dict() for i in self.issues],
            },
            "metrics": {
                "complexity": self.complexity_score,
                "maintainability": self.maintainability_rank,
                "security_score": self.security_score,
                "quality_score": self.quality_score,
                "quality_rank": self.quality_rank,
            },
            "quality_gate": {
                "status": "PASSED" if self.quality_gate_passed else "FAILED",
                "threshold": self.thresholds.get("min_quality_score", 0),
                "actual": self.quality_score,
            },
        }
