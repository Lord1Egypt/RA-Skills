#!/usr/bin/env python3
"""
Frozen Benchmark Interface

不可变的基准测试集，用于评估 Skill 的标准能力。
一旦创建，测试用例和评分标准即冻结，确保评估的一致性和可比性。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Union
import hashlib
import json


class MetricType(Enum):
    """评估指标类型"""
    ACCURACY = "accuracy"           # 准确性
    RELIABILITY = "reliability"     # 可靠性
    EFFICIENCY = "efficiency"       # 效率 (时间)
    COST = "cost"                   # 成本 (token)
    COVERAGE = "coverage"           # 覆盖率
    SECURITY = "security"           # 安全性
    SAFETY = "safety"               # 安全性 (AI 安全)


@dataclass(frozen=True)
class ScoringCriteria:
    """
    评分标准 (不可变)

    Attributes:
        metric: 评估指标类型
        weight: 权重 (0.0 - 1.0)
        threshold: 及格阈值
        target: 目标值
        scoring_function: 评分函数标识符
    """
    metric: MetricType
    weight: float = 1.0
    threshold: float = 0.6
    target: float = 0.9
    scoring_function: str = "linear"  # linear, step, exponential

    def __post_init__(self):
        assert 0.0 <= self.weight <= 1.0, "Weight must be in [0, 1]"
        assert 0.0 <= self.threshold <= 1.0, "Threshold must be in [0, 1]"


@dataclass(frozen=True)
class BenchmarkCase:
    """
    单个基准测试用例 (不可变)

    Attributes:
        id: 唯一标识符
        name: 测试名称
        input_data: 输入数据 (可以是任意可序列化类型)
        expected_output: 期望输出 (用于验证)
        category: 测试类别
        difficulty: 难度等级 1-5
        tags: 标签列表
        created_at: 创建时间戳
        checksum: 数据完整性校验
    """
    id: str
    name: str
    input_data: Any
    expected_output: Any
    category: str = "general"
    difficulty: int = 3
    tags: tuple = field(default_factory=tuple)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    checksum: str = field(default="")

    def __post_init__(self):
        # 计算校验和以确保数据完整性
        if not self.checksum:
            object.__setattr__(
                self,
                'checksum',
                self._compute_checksum()
            )

    def _compute_checksum(self) -> str:
        """计算数据校验和"""
        data = json.dumps({
            "id": self.id,
            "input": self.input_data,
            "expected": self.expected_output,
            "category": self.category,
        }, sort_keys=True, default=str)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def verify_integrity(self) -> bool:
        """验证数据完整性"""
        return self.checksum == self._compute_checksum()


@dataclass(frozen=True)
class BenchmarkResult:
    """
    基准测试结果 (不可变)

    Attributes:
        case_id: 测试用例 ID
        passed: 是否通过
        score: 得分 (0.0 - 1.0)
        actual_output: 实际输出
        execution_time_ms: 执行时间 (毫秒)
        token_usage: Token 使用量
        error_message: 错误信息 (如果有)
        metadata: 额外元数据
    """
    case_id: str
    passed: bool
    score: float = 0.0
    actual_output: Any = None
    execution_time_ms: float = 0.0
    token_usage: int = 0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        assert 0.0 <= self.score <= 1.0, "Score must be in [0, 1]"


@dataclass(frozen=True)
class BenchmarkSuite:
    """
    基准测试套件 (不可变)

    Attributes:
        id: 套件唯一标识符
        name: 套件名称
        version: 版本号 (语义化版本)
        description: 描述
        cases: 测试用例列表
        criteria: 评分标准列表
        frozen_at: 冻结时间戳
        signature: 数字签名/校验和
    """
    id: str
    name: str
    version: str
    description: str
    cases: tuple = field(default_factory=tuple)
    criteria: tuple = field(default_factory=tuple)
    frozen_at: str = field(default_factory=lambda: datetime.now().isoformat())
    signature: str = ""

    def __post_init__(self):
        if not self.signature:
            object.__setattr__(self, 'signature', self._compute_signature())

    def _compute_signature(self) -> str:
        """计算套件签名"""
        data = {
            "id": self.id,
            "version": self.version,
            "cases": [(c.id, c.checksum) for c in self.cases],
            "criteria": [(c.metric.value, c.weight) for c in self.criteria],
            "frozen_at": self.frozen_at,
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def verify(self) -> bool:
        """验证套件完整性"""
        # 验证套件签名
        if self.signature != self._compute_signature():
            return False
        # 验证所有用例完整性
        return all(case.verify_integrity() for case in self.cases)

    def get_case(self, case_id: str) -> Optional[BenchmarkCase]:
        """根据 ID 获取测试用例"""
        for case in self.cases:
            if case.id == case_id:
                return case
        return None

    def get_cases_by_category(self, category: str) -> List[BenchmarkCase]:
        """根据类别获取测试用例"""
        return [c for c in self.cases if c.category == category]

    def get_cases_by_difficulty(self, min_diff: int, max_diff: int) -> List[BenchmarkCase]:
        """根据难度范围获取测试用例"""
        return [c for c in self.cases if min_diff <= c.difficulty <= max_diff]


class Evaluator(Protocol):
    """
    Skill 评估器协议

    实现此协议的类可以用于执行基准测试。
    """

    def evaluate(self, case: BenchmarkCase) -> BenchmarkResult:
        """
        执行单个测试用例评估

        Args:
            case: 基准测试用例

        Returns:
            评估结果
        """
        ...

    def get_capabilities(self) -> Dict[str, Any]:
        """返回评估器能力描述"""
        ...


class FrozenBenchmark:
    """
    冻结基准测试执行器

    确保评估的一致性和可重复性。所有测试用例在执行前
    都会验证完整性，任何篡改都会被检测到。
    """

    def __init__(self, suite: BenchmarkSuite):
        """
        初始化冻结基准测试

        Args:
            suite: 基准测试套件

        Raises:
            ValueError: 如果套件验证失败
        """
        if not suite.verify():
            raise ValueError("Benchmark suite integrity check failed - may have been tampered with")
        self._suite = suite
        self._results: List[BenchmarkResult] = []

    @property
    def suite(self) -> BenchmarkSuite:
        """获取测试套件 (只读)"""
        return self._suite

    def run(self, evaluator: Evaluator, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        运行完整基准测试

        Args:
            evaluator: Skill 评估器
            progress_callback: 进度回调函数 (case_index, total_cases, result)

        Returns:
            完整评估报告
        """
        self._results = []
        total_cases = len(self._suite.cases)

        for idx, case in enumerate(self._suite.cases):
            result = evaluator.evaluate(case)
            self._results.append(result)

            if progress_callback:
                progress_callback(idx + 1, total_cases, result)

        return self._generate_report()

    def _generate_report(self) -> Dict[str, Any]:
        """生成评估报告"""
        if not self._results:
            return {"error": "No results available"}

        # 计算各项指标
        total_cases = len(self._results)
        passed_cases = sum(1 for r in self._results if r.passed)
        avg_score = sum(r.score for r in self._results) / total_cases
        avg_time = sum(r.execution_time_ms for r in self._results) / total_cases
        total_tokens = sum(r.token_usage for r in self._results)

        # 按类别统计
        category_stats: Dict[str, Dict] = {}
        for case in self._suite.cases:
            cat = case.category
            if cat not in category_stats:
                category_stats[cat] = {"total": 0, "passed": 0, "total_score": 0.0}

        for case, result in zip(self._suite.cases, self._results):
            cat = case.category
            category_stats[cat]["total"] += 1
            if result.passed:
                category_stats[cat]["passed"] += 1
            category_stats[cat]["total_score"] += result.score

        for cat, stats in category_stats.items():
            stats["pass_rate"] = stats["passed"] / stats["total"] if stats["total"] > 0 else 0
            stats["avg_score"] = stats["total_score"] / stats["total"] if stats["total"] > 0 else 0

        # 计算加权总分
        weighted_score = 0.0
        total_weight = 0.0
        for criteria in self._suite.criteria:
            if criteria.metric == MetricType.ACCURACY:
                weighted_score += avg_score * criteria.weight
                total_weight += criteria.weight

        return {
            "suite_id": self._suite.id,
            "suite_version": self._suite.version,
            "suite_signature": self._suite.signature[:16] + "...",
            "summary": {
                "total_cases": total_cases,
                "passed_cases": passed_cases,
                "pass_rate": passed_cases / total_cases,
                "avg_score": round(avg_score, 4),
                "weighted_score": round(weighted_score / total_weight if total_weight > 0 else avg_score, 4),
                "avg_execution_time_ms": round(avg_time, 2),
                "total_token_usage": total_tokens,
            },
            "by_category": category_stats,
            "results": [
                {
                    "case_id": r.case_id,
                    "passed": r.passed,
                    "score": r.score,
                    "time_ms": r.execution_time_ms,
                    "tokens": r.token_usage,
                    "error": r.error_message,
                }
                for r in self._results
            ],
            "verified": True,
        }

    def export_results(self, path: Union[str, Path]) -> Path:
        """导出结果到文件"""
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        report = self._generate_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        return output_path


# 预定义的标准基准测试套件

STANDARD_BENCHMARK_SUITE = BenchmarkSuite(
    id="skill-eval-standard-v1",
    name="Skill Evaluator Standard Benchmark",
    version="1.0.0",
    description="Standard benchmark suite for evaluating skill capabilities",
    cases=tuple([
        BenchmarkCase(
            id="basic-functionality-001",
            name="Basic Functionality Test",
            input_data={"task": "simple_addition", "a": 2, "b": 3},
            expected_output={"result": 5},
            category="functionality",
            difficulty=1,
            tags=("math", "basic"),
        ),
        BenchmarkCase(
            id="error-handling-001",
            name="Error Handling Test",
            input_data={"task": "divide", "a": 10, "b": 0},
            expected_output={"error": "division_by_zero"},
            category="reliability",
            difficulty=2,
            tags=("error", "edge-case"),
        ),
        BenchmarkCase(
            id="performance-001",
            name="Performance Test",
            input_data={"task": "sort", "data": list(range(1000, 0, -1))},
            expected_output={"sorted": True},
            category="efficiency",
            difficulty=3,
            tags=("performance", "sorting"),
        ),
    ]),
    criteria=tuple([
        ScoringCriteria(MetricType.ACCURACY, weight=0.4, threshold=0.8, target=0.95),
        ScoringCriteria(MetricType.RELIABILITY, weight=0.3, threshold=0.7, target=0.9),
        ScoringCriteria(MetricType.EFFICIENCY, weight=0.2, threshold=0.6, target=0.85),
        ScoringCriteria(MetricType.COST, weight=0.1, threshold=0.5, target=0.8),
    ]),
)
