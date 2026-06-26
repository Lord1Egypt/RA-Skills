#!/usr/bin/env python3
"""
External Regression Hook - P2 Engineering Enhancement

外部回归测试结果接入接口，允许将外部回归测试结果并入最终评分/报告。

设计目标:
1. 适配层设计：支持多种外部回归结果格式 (JSON/CSV/JUnit XML)
2. 结果归一化：将不同格式的结果统一为标准评分格式
3. 可插拔：支持自定义适配器
4. 可追溯：保留原始结果引用和元数据

使用场景:
- CI/CD pipeline 回归测试结果导入
- 历史基准测试结果对比
- 第三方评估工具结果整合
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Union
import json
import csv
import xml.etree.ElementTree as ET


class RegressionSourceType(Enum):
    """外部回归结果来源类型"""
    CI_PIPELINE = "ci_pipeline"       # CI/CD pipeline (GitHub Actions, Jenkins, etc.)
    HISTORICAL = "historical"         # 历史基准测试
    THIRD_PARTY = "third_party"       # 第三方评估工具 (Promptfoo, LangSmith, etc.)
    CUSTOM = "custom"                 # 自定义格式


class RegressionStatus(Enum):
    """回归测试状态"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass(frozen=True)
class RegressionTestResult:
    """
    单个回归测试结果 (不可变)

    Attributes:
        test_id: 测试 ID
        test_name: 测试名称
        status: 测试状态
        score: 得分 (0.0 - 1.0)
        duration_ms: 执行时间 (毫秒)
        error_message: 错误消息 (如果有)
        metadata: 附加元数据
        timestamp: 时间戳
    """
    test_id: str
    test_name: str
    status: RegressionStatus
    score: float = 1.0
    duration_ms: float = 0.0
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        assert 0.0 <= self.score <= 1.0, "Score must be in [0, 1]"


@dataclass
class RegressionSuiteResult:
    """
    回归测试套件总结果

    Attributes:
        suite_id: 套件 ID
        suite_name: 套件名称
        source_type: 来源类型
        total_tests: 总测试数
        passed: 通过数
        failed: 失败数
        skipped: 跳过数
        error: 错误数
        overall_score: 总体得分
        results: 单个测试结果列表
        metadata: 套件元数据
        generated_at: 生成时间
    """
    suite_id: str
    suite_name: str
    source_type: RegressionSourceType
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    error: int = 0
    overall_score: float = 0.0
    results: List[RegressionTestResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_result(self, result: RegressionTestResult) -> None:
        """添加测试结果并更新统计"""
        self.results.append(result)
        self.total_tests += 1

        if result.status == RegressionStatus.PASSED:
            self.passed += 1
        elif result.status == RegressionStatus.FAILED:
            self.failed += 1
        elif result.status == RegressionStatus.SKIPPED:
            self.skipped += 1
        elif result.status == RegressionStatus.ERROR:
            self.error += 1

        # 重新计算总体得分
        if self.results:
            self.overall_score = sum(r.score for r in self.results) / len(self.results)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "suite_id": self.suite_id,
            "suite_name": self.suite_name,
            "source_type": self.source_type.value,
            "summary": {
                "total": self.total_tests,
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "error": self.error,
                "overall_score": round(self.overall_score, 4),
            },
            "results": [
                {
                    "test_id": r.test_id,
                    "test_name": r.test_name,
                    "status": r.status.value,
                    "score": r.score,
                    "duration_ms": r.duration_ms,
                    "error_message": r.error_message,
                }
                for r in self.results
            ],
            "metadata": self.metadata,
            "generated_at": self.generated_at,
        }


class RegressionAdapter(Protocol):
    """
    回归结果适配器协议

    实现此协议的类可以将特定格式的外部结果转换为标准格式。
    """

    def parse(self, source: Union[str, Path, Dict]) -> RegressionSuiteResult:
        """
        解析外部回归结果

        Args:
            source: 结果来源 (文件路径或原始数据)

        Returns:
            标准化的回归套件结果
        """
        ...

    def get_source_type(self) -> RegressionSourceType:
        """返回适配器支持的来源类型"""
        ...


class JSONRegressionAdapter:
    """
    JSON 格式回归结果适配器

    支持标准 JSON 格式的回归测试结果。
    期望格式:
    {
        "suite_id": "regression-001",
        "suite_name": "Daily Regression",
        "tests": [
            {
                "test_id": "test-001",
                "test_name": "Test Feature A",
                "status": "passed",
                "score": 1.0,
                "duration_ms": 123.45,
                "metadata": {}
            }
        ]
    }
    """

    def __init__(self, suite_id: str = "json-import", suite_name: str = "JSON Import"):
        self.suite_id = suite_id
        self.suite_name = suite_name

    def get_source_type(self) -> RegressionSourceType:
        return RegressionSourceType.CUSTOM

    def parse(self, source: Union[str, Path, Dict]) -> RegressionSuiteResult:
        """解析 JSON 格式结果"""
        if isinstance(source, (str, Path)):
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = source

        result = RegressionSuiteResult(
            suite_id=data.get("suite_id", self.suite_id),
            suite_name=data.get("suite_name", self.suite_name),
            source_type=RegressionSourceType.CUSTOM,
            metadata=data.get("metadata", {}),
        )

        for test_data in data.get("tests", []):
            status_str = test_data.get("status", "passed").lower()
            try:
                status = RegressionStatus(status_str)
            except ValueError:
                status = RegressionStatus.ERROR

            test_result = RegressionTestResult(
                test_id=test_data.get("test_id", "unknown"),
                test_name=test_data.get("test_name", "Unknown Test"),
                status=status,
                score=float(test_data.get("score", 1.0 if status == RegressionStatus.PASSED else 0.0)),
                duration_ms=float(test_data.get("duration_ms", 0.0)),
                error_message=test_data.get("error_message", ""),
                metadata=test_data.get("metadata", {}),
            )
            result.add_result(test_result)

        return result


class JUnitXMLRegressionAdapter:
    """
    JUnit XML 格式回归结果适配器

    支持标准 JUnit XML 格式的测试结果 (GitHub Actions, Jenkins, etc.)。
    """

    def __init__(self, suite_name: str = "JUnit Import"):
        self.suite_name = suite_name

    def get_source_type(self) -> RegressionSourceType:
        return RegressionSourceType.CI_PIPELINE

    def parse(self, source: Union[str, Path]) -> RegressionSuiteResult:
        """解析 JUnit XML 格式结果"""
        if isinstance(source, str):
            source = Path(source)

        tree = ET.parse(source)
        root = tree.getroot()

        # 处理 testsuites 或 testsuite 根元素
        if root.tag == "testsuites":
            suites = root.findall("testsuite")
        elif root.tag == "testsuite":
            suites = [root]
        else:
            suites = []

        result = RegressionSuiteResult(
            suite_id=f"junit-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            suite_name=self.suite_name,
            source_type=RegressionSourceType.CI_PIPELINE,
        )

        test_id_counter = 0
        for suite in suites:
            suite_name = suite.get("name", "Unknown Suite")

            for testcase in suite.findall("testcase"):
                test_id_counter += 1
                test_name = testcase.get("name", f"Test-{test_id_counter}")
                classname = testcase.get("classname", "")
                duration = float(testcase.get("time", 0.0)) * 1000  # 转换为毫秒

                # 检查是否有失败或错误
                failure = testcase.find("failure")
                error = testcase.find("error")
                skipped = testcase.find("skipped")

                if failure is not None:
                    status = RegressionStatus.FAILED
                    error_message = failure.get("message", "")
                    score = 0.0
                elif error is not None:
                    status = RegressionStatus.ERROR
                    error_message = error.get("message", "")
                    score = 0.0
                elif skipped is not None:
                    status = RegressionStatus.SKIPPED
                    error_message = ""
                    score = 0.0
                else:
                    status = RegressionStatus.PASSED
                    error_message = ""
                    score = 1.0

                test_result = RegressionTestResult(
                    test_id=f"{classname}.{test_name}" if classname else test_name,
                    test_name=test_name,
                    status=status,
                    score=score,
                    duration_ms=duration,
                    error_message=error_message,
                    metadata={
                        "classname": classname,
                        "suite": suite_name,
                    },
                )
                result.add_result(test_result)

        return result


class CSVRegressionAdapter:
    """
    CSV 格式回归结果适配器

    支持 CSV 格式的测试结果。
    期望列：test_id, test_name, status, score, duration_ms, error_message
    """

    def __init__(self, suite_name: str = "CSV Import"):
        self.suite_name = suite_name

    def get_source_type(self) -> RegressionSourceType:
        return RegressionSourceType.HISTORICAL

    def parse(self, source: Union[str, Path]) -> RegressionSuiteResult:
        """解析 CSV 格式结果"""
        if isinstance(source, str):
            source = Path(source)

        result = RegressionSuiteResult(
            suite_id=f"csv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            suite_name=self.suite_name,
            source_type=RegressionSourceType.HISTORICAL,
        )

        with open(source, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                status_str = row.get("status", "passed").lower()
                try:
                    status = RegressionStatus(status_str)
                except ValueError:
                    status = RegressionStatus.ERROR

                test_result = RegressionTestResult(
                    test_id=row.get("test_id", "unknown"),
                    test_name=row.get("test_name", "Unknown Test"),
                    status=status,
                    score=float(row.get("score", 1.0 if status == RegressionStatus.PASSED else 0.0)),
                    duration_ms=float(row.get("duration_ms", 0.0)),
                    error_message=row.get("error_message", ""),
                )
                result.add_result(test_result)

        return result


class ExternalRegressionHook:
    """
    外部回归结果接入钩子

    统一管理外部回归结果的导入、归一化和整合。

    使用示例:
        hook = ExternalRegressionHook()
        
        # 导入 JSON 格式结果
        hook.load_from_file("results.json", adapter_type="json")
        
        # 导入 JUnit XML 结果
        hook.load_from_file("junit-results.xml", adapter_type="junit")
        
        # 获取整合后的评分
        score = hook.get_normalized_score()
        
        # 获取详细结果
        all_results = hook.get_all_results()
    """

    def __init__(self):
        self._adapters: Dict[RegressionSourceType, RegressionAdapter] = {
            RegressionSourceType.CUSTOM: JSONRegressionAdapter(),
            RegressionSourceType.CI_PIPELINE: JUnitXMLRegressionAdapter(),
            RegressionSourceType.HISTORICAL: CSVRegressionAdapter(),
        }
        self._results: List[RegressionSuiteResult] = []
        self._custom_adapters: Dict[str, RegressionAdapter] = {}

    def register_adapter(
        self,
        name: str,
        adapter: RegressionAdapter,
        source_type: RegressionSourceType = RegressionSourceType.CUSTOM,
    ) -> None:
        """
        注册自定义适配器

        Args:
            name: 适配器名称
            adapter: 适配器实例
            source_type: 来源类型
        """
        self._custom_adapters[name] = adapter
        self._adapters[source_type] = adapter

    def load_from_file(
        self,
        path: Union[str, Path],
        adapter_type: str = "json",
        suite_id: Optional[str] = None,
        suite_name: Optional[str] = None,
    ) -> RegressionSuiteResult:
        """
        从文件加载回归结果

        Args:
            path: 文件路径
            adapter_type: 适配器类型 ("json", "junit", "csv")
            suite_id: 可选的套件 ID (覆盖默认值)
            suite_name: 可选的套件名称 (覆盖默认值)

        Returns:
            解析后的回归套件结果
        """
        path = Path(path)

        if adapter_type == "json":
            adapter = JSONRegressionAdapter(
                suite_id=suite_id or "json-import",
                suite_name=suite_name or "JSON Import",
            )
        elif adapter_type == "junit":
            adapter = JUnitXMLRegressionAdapter(
                suite_name=suite_name or "JUnit Import",
            )
        elif adapter_type == "csv":
            adapter = CSVRegressionAdapter(
                suite_name=suite_name or "CSV Import",
            )
        elif adapter_type in self._custom_adapters:
            adapter = self._custom_adapters[adapter_type]
        else:
            raise ValueError(f"Unknown adapter type: {adapter_type}")

        result = adapter.parse(path)
        self._results.append(result)
        return result

    def load_from_dict(
        self,
        data: Dict[str, Any],
        suite_id: str = "dict-import",
        suite_name: str = "Dict Import",
    ) -> RegressionSuiteResult:
        """
        从字典加载回归结果

        Args:
            data: 结果数据
            suite_id: 套件 ID
            suite_name: 套件名称

        Returns:
            解析后的回归套件结果
        """
        adapter = JSONRegressionAdapter(suite_id=suite_id, suite_name=suite_name)
        result = adapter.parse(data)
        self._results.append(result)
        return result

    def add_result(self, result: RegressionSuiteResult) -> None:
        """直接添加回归套件结果"""
        self._results.append(result)

    def get_all_results(self) -> List[RegressionSuiteResult]:
        """获取所有加载的回归结果"""
        return self._results.copy()

    def get_normalized_score(self, weighting: Optional[Dict[str, float]] = None) -> float:
        """
        获取归一化后的总体评分

        Args:
            weighting: 可选的权重配置 (按 suite_id 或 source_type)

        Returns:
            归一化后的总体评分 (0.0 - 1.0)
        """
        if not self._results:
            return 0.0

        if weighting:
            # 加权平均
            total_weight = 0.0
            weighted_score = 0.0

            for result in self._results:
                weight = weighting.get(result.suite_id) or weighting.get(result.source_type.value, 1.0)
                weighted_score += result.overall_score * weight
                total_weight += weight

            return weighted_score / total_weight if total_weight > 0 else 0.0
        else:
            # 简单平均
            return sum(r.overall_score for r in self._results) / len(self._results)

    def get_summary(self) -> Dict[str, Any]:
        """获取所有回归结果的汇总统计"""
        if not self._results:
            return {
                "total_suites": 0,
                "total_tests": 0,
                "overall_score": 0.0,
            }

        total_tests = sum(r.total_tests for r in self._results)
        total_passed = sum(r.passed for r in self._results)
        total_failed = sum(r.failed for r in self._results)

        return {
            "total_suites": len(self._results),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": sum(r.skipped for r in self._results),
            "total_errors": sum(r.error for r in self._results),
            "overall_score": round(self.get_normalized_score(), 4),
            "by_source_type": {
                st.value: sum(r.overall_score for r in self._results if r.source_type == st)
                for st in RegressionSourceType
            },
        }

    def merge_into_score(
        self,
        base_score: float,
        regression_weight: float = 0.2,
    ) -> float:
        """
        将回归结果合并到基础评分中

        Args:
            base_score: 基础评分 (来自 benchmark/hidden tests)
            regression_weight: 回归结果权重 (0.0 - 1.0)

        Returns:
            合并后的最终评分
        """
        if not self._results:
            return base_score

        regression_score = self.get_normalized_score()
        return base_score * (1 - regression_weight) + regression_score * regression_weight

    def export_report(self, output_path: Union[str, Path], format: str = "json") -> str:
        """
        导出回归结果报告

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
                "suites": [r.to_dict() for r in self._results],
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
            "# External Regression Results Report",
            "",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- **Total Suites**: {summary['total_suites']}",
            f"- **Total Tests**: {summary['total_tests']}",
            f"- **Passed**: {summary['total_passed']}",
            f"- **Failed**: {summary['total_failed']}",
            f"- **Overall Score**: {summary['overall_score']:.4f}",
            "",
            "## Results by Suite",
            "",
        ]

        for result in self._results:
            lines.extend([
                f"### {result.suite_name}",
                "",
                f"- **Source Type**: {result.source_type.value}",
                f"- **Tests**: {result.total_tests} ({result.passed} passed, {result.failed} failed)",
                f"- **Score**: {result.overall_score:.4f}",
                "",
            ])

        return "\n".join(lines)


# 辅助函数

def create_regression_result(
    test_id: str,
    test_name: str,
    passed: bool,
    score: float = None,
    duration_ms: float = 0.0,
    error_message: str = "",
) -> RegressionTestResult:
    """
    创建回归测试结果的辅助函数

    Args:
        test_id: 测试 ID
        test_name: 测试名称
        passed: 是否通过
        score: 得分 (可选，默认 passed=1.0, failed=0.0)
        duration_ms: 执行时间
        error_message: 错误消息

    Returns:
        回归测试结果
    """
    if score is None:
        score = 1.0 if passed else 0.0

    status = RegressionStatus.PASSED if passed else RegressionStatus.FAILED

    return RegressionTestResult(
        test_id=test_id,
        test_name=test_name,
        status=status,
        score=score,
        duration_ms=duration_ms,
        error_message=error_message,
    )
