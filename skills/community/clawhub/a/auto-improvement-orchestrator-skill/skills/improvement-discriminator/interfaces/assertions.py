#!/usr/bin/env python3
"""
Assertion System - 最小断言系统

P1 实现：引入 structured checks 思路，让评估输出更像 assertion-driven，
而不是纯自然语言打分。

核心设计:
- 断言类型：contains, equals, regex, json_schema, latency, cost
- 断言结果：pass/fail + 详细错误信息
- 可组合：支持多个断言组合成一个测试用例
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
import re
import time


class AssertionType(Enum):
    """断言类型"""
    CONTAINS = "contains"           # 包含某字符串/关键词
    EQUALS = "equals"               # 完全相等
    REGEX = "regex"                 # 正则匹配
    JSON_SCHEMA = "json_schema"     # JSON Schema 验证
    LATENCY = "latency"             # 延迟检查
    COST = "cost"                   # 成本检查
    THRESHOLD = "threshold"         # 阈值检查 (通用)
    CUSTOM = "custom"               # 自定义断言函数


@dataclass(frozen=True)
class Assertion:
    """
    单个断言定义 (不可变)

    Attributes:
        type: 断言类型
        value: 期望值/阈值
        description: 断言描述 (可选)
        weight: 权重 (0.0 - 1.0)，默认 1.0
        required: 是否必须通过，默认 True
    """
    type: AssertionType
    value: Any
    description: str = ""
    weight: float = 1.0
    required: bool = True

    def __post_init__(self):
        assert 0.0 <= self.weight <= 1.0, "Weight must be in [0, 1]"


@dataclass
class AssertionResult:
    """
    断言执行结果

    Attributes:
        passed: 是否通过
        assertion: 原始断言定义
        actual_value: 实际值
        expected_value: 期望值
        message: 详细消息/错误信息
        execution_time_ms: 执行时间
    """
    passed: bool
    assertion: Assertion
    actual_value: Any = None
    expected_value: Any = None
    message: str = ""
    execution_time_ms: float = 0.0

    def __str__(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} [{self.assertion.type.value}] {self.assertion.description or self.assertion.type.value}: {self.message}"


class AssertionExecutor:
    """
    断言执行器

    执行各种类型的断言检查。
    """

    def __init__(self, timeout_ms: float = 5000):
        """
        初始化执行器

        Args:
            timeout_ms: 单个断言超时时间 (毫秒)
        """
        self.timeout_ms = timeout_ms

    def execute(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """
        执行单个断言

        Args:
            assertion: 断言定义
            actual_output: 实际输出

        Returns:
            断言结果
        """
        start_time = time.time()

        try:
            if assertion.type == AssertionType.CONTAINS:
                return self._check_contains(assertion, actual_output)
            elif assertion.type == AssertionType.EQUALS:
                return self._check_equals(assertion, actual_output)
            elif assertion.type == AssertionType.REGEX:
                return self._check_regex(assertion, actual_output)
            elif assertion.type == AssertionType.LATENCY:
                return self._check_latency(assertion, actual_output)
            elif assertion.type == AssertionType.COST:
                return self._check_cost(assertion, actual_output)
            elif assertion.type == AssertionType.THRESHOLD:
                return self._check_threshold(assertion, actual_output)
            elif assertion.type == AssertionType.CUSTOM:
                return self._check_custom(assertion, actual_output)
            else:
                return AssertionResult(
                    passed=False,
                    assertion=assertion,
                    message=f"Unknown assertion type: {assertion.type}",
                )
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return AssertionResult(
                passed=False,
                assertion=assertion,
                message=f"Assertion error: {str(e)}",
                execution_time_ms=execution_time,
            )

    def _check_contains(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """检查是否包含某字符串/关键词"""
        start_time = time.time()
        expected = assertion.value

        # 处理实际输出
        if isinstance(actual_output, dict):
            actual_str = str(actual_output.get("output", str(actual_output)))
        elif isinstance(actual_output, list):
            actual_str = " ".join(str(item) for item in actual_output)
        else:
            actual_str = str(actual_output)

        # 支持单个字符串或列表
        if isinstance(expected, str):
            passed = expected.lower() in actual_str.lower()
            expected_value = expected
            message = f"Expected to contain '{expected}'" if not passed else f"Found '{expected}'"
        elif isinstance(expected, list):
            passed = all(item.lower() in actual_str.lower() for item in expected)
            expected_value = expected
            message = f"Expected to contain all of {expected}" if not passed else f"Found all keywords"
        else:
            passed = False
            expected_value = expected
            message = f"Invalid expected value type: {type(expected)}"

        execution_time = (time.time() - start_time) * 1000
        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=actual_str[:200],  # 截断避免过长
            expected_value=expected_value,
            message=message,
            execution_time_ms=execution_time,
        )

    def _check_equals(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """检查是否完全相等"""
        start_time = time.time()
        expected = assertion.value

        # 处理字典输出
        if isinstance(actual_output, dict) and isinstance(expected, dict):
            passed = actual_output == expected
            message = "Values match" if passed else f"Expected {expected}, got {actual_output}"
        else:
            passed = str(actual_output) == str(expected)
            message = "Values match" if passed else f"Expected '{expected}', got '{actual_output}'"

        execution_time = (time.time() - start_time) * 1000
        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=actual_output,
            expected_value=expected,
            message=message,
            execution_time_ms=execution_time,
        )

    def _check_regex(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """正则匹配"""
        start_time = time.time()
        pattern = assertion.value

        actual_str = str(actual_output)

        try:
            compiled = re.compile(pattern, re.IGNORECASE)
            passed = bool(compiled.search(actual_str))
            message = f"Matched pattern '{pattern}'" if passed else f"Pattern '{pattern}' not found"
        except re.error as e:
            passed = False
            message = f"Invalid regex pattern: {e}"

        execution_time = (time.time() - start_time) * 1000
        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=actual_str[:200],
            expected_value=pattern,
            message=message,
            execution_time_ms=execution_time,
        )

    def _check_latency(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """
        延迟检查

        注意：这个断言需要实际输出包含执行时间信息，
        或者由外部传入执行时间。
        """
        # 这个断言需要特殊处理，因为实际输出本身不包含延迟信息
        # 通常由外部框架在执行后传入
        execution_time = actual_output if isinstance(actual_output, (int, float)) else 0

        threshold_ms = assertion.value
        passed = execution_time <= threshold_ms
        message = f"Latency {execution_time:.0f}ms <= {threshold_ms}ms" if passed else f"Latency {execution_time:.0f}ms > {threshold_ms}ms"

        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=execution_time,
            expected_value=threshold_ms,
            message=message,
            execution_time_ms=0,
        )

    def _check_cost(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """
        成本检查

        类似 latency，需要外部传入成本信息。
        """
        cost = actual_output if isinstance(actual_output, (int, float)) else 0
        threshold = assertion.value
        passed = cost <= threshold
        message = f"Cost ${cost:.4f} <= ${threshold:.4f}" if passed else f"Cost ${cost:.4f} > ${threshold:.4f}"

        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=cost,
            expected_value=threshold,
            message=message,
            execution_time_ms=0,
        )

    def _check_threshold(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """
        通用阈值检查

        用于数值比较：actual >= threshold 或 actual <= threshold
        """
        threshold = assertion.value
        actual = float(actual_output) if not isinstance(actual_output, (int, float)) else actual_output

        # 支持 >= 或 <= 检查
        if isinstance(threshold, dict):
            min_val = threshold.get("min")
            max_val = threshold.get("max")
            if min_val is not None and max_val is not None:
                passed = min_val <= actual <= max_val
                message = f"{actual} in [{min_val}, {max_val}]" if passed else f"{actual} not in [{min_val}, {max_val}]"
            elif min_val is not None:
                passed = actual >= min_val
                message = f"{actual} >= {min_val}" if passed else f"{actual} < {min_val}"
            elif max_val is not None:
                passed = actual <= max_val
                message = f"{actual} <= {max_val}" if passed else f"{actual} > {max_val}"
            else:
                passed = False
                message = "Invalid threshold format"
        else:
            # 默认 >= 检查
            passed = actual >= threshold
            message = f"{actual} >= {threshold}" if passed else f"{actual} < {threshold}"

        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=actual,
            expected_value=threshold,
            message=message,
            execution_time_ms=0,
        )

    def _check_custom(self, assertion: Assertion, actual_output: Any) -> AssertionResult:
        """
        自定义断言函数

        assertion.value 应该是一个 Callable[[Any], bool] 或返回 (bool, str) 的函数
        """
        start_time = time.time()
        func = assertion.value

        if not callable(func):
            return AssertionResult(
                passed=False,
                assertion=assertion,
                message="Custom assertion value must be callable",
            )

        try:
            result = func(actual_output)
            if isinstance(result, tuple):
                passed, message = result
            else:
                passed = bool(result)
                message = "Custom assertion passed" if passed else "Custom assertion failed"
        except Exception as e:
            passed = False
            message = f"Custom assertion error: {str(e)}"

        execution_time = (time.time() - start_time) * 1000
        return AssertionResult(
            passed=passed,
            assertion=assertion,
            actual_value=actual_output,
            message=message,
            execution_time_ms=execution_time,
        )


@dataclass
class AssertionCheck:
    """
    断言检查集合

    将多个断言组合成一个检查单元。

    Attributes:
        name: 检查名称
        assertions: 断言列表
        description: 检查描述
    """
    name: str
    assertions: List[Assertion]
    description: str = ""


@dataclass
class CheckResult:
    """
    检查结果

    Attributes:
        check: 原始检查定义
        results: 各个断言的结果
        passed: 是否整体通过
        score: 得分 (0.0 - 1.0)
        message: 汇总消息
    """
    check: AssertionCheck
    results: List[AssertionResult]
    passed: bool
    score: float = 0.0
    message: str = ""

    @classmethod
    def from_results(cls, check: AssertionCheck, results: List[AssertionResult]) -> "CheckResult":
        """从断言结果创建检查结果"""
        # 计算加权得分
        total_weight = sum(a.weight for a in check.assertions)
        weighted_score = sum(
            r.passed * r.assertion.weight
            for r in results
        ) / total_weight if total_weight > 0 else 0.0

        # 检查是否有 required 断言失败
        required_failed = any(
            not r.passed and r.assertion.required
            for r in results
        )

        passed = weighted_score >= 0.8 and not required_failed

        # 生成汇总消息
        passed_count = sum(1 for r in results if r.passed)
        total_count = len(results)
        message = f"{passed_count}/{total_count} assertions passed"

        return cls(
            check=check,
            results=results,
            passed=passed,
            score=round(weighted_score, 4),
            message=message,
        )


class AssertionRunner:
    """
    断言运行器

    执行完整的断言检查流程。
    """

    def __init__(self, executor: Optional[AssertionExecutor] = None):
        """
        初始化运行器

        Args:
            executor: 断言执行器，使用默认如果未提供
        """
        self.executor = executor or AssertionExecutor()

    def run(self, check: AssertionCheck, actual_output: Any) -> CheckResult:
        """
        运行断言检查

        Args:
            check: 断言检查定义
            actual_output: 实际输出

        Returns:
            检查结果
        """
        results = []
        for assertion in check.assertions:
            result = self.executor.execute(assertion, actual_output)
            results.append(result)

        return CheckResult.from_results(check, results)

    def run_batch(
        self,
        checks: List[AssertionCheck],
        actual_output: Any,
    ) -> List[CheckResult]:
        """
        批量运行多个检查

        Args:
            checks: 检查列表
            actual_output: 实际输出

        Returns:
            检查结果列表
        """
        return [self.run(check, actual_output) for check in checks]


# 便捷函数

def create_assertion(
    type: str,  # 使用 type 作为参数名，方便调用
    value: Any,
    description: str = "",
    weight: float = 1.0,
    required: bool = True,
) -> Assertion:
    """
    创建断言的便捷函数

    Args:
        type: 断言类型字符串 (contains/equals/regex/latency/cost/threshold/custom)
        value: 期望值
        description: 描述
        weight: 权重
        required: 是否必须

    Returns:
        断言对象
    """
    type_map = {
        "contains": AssertionType.CONTAINS,
        "equals": AssertionType.EQUALS,
        "regex": AssertionType.REGEX,
        "latency": AssertionType.LATENCY,
        "cost": AssertionType.COST,
        "threshold": AssertionType.THRESHOLD,
        "custom": AssertionType.CUSTOM,
    }

    assertion_type = type_map.get(type.lower())
    if not assertion_type:
        raise ValueError(f"Unknown assertion type: {type}")

    return Assertion(
        type=assertion_type,
        value=value,
        description=description,
        weight=weight,
        required=required,
    )


def create_check(
    name: str,
    assertions: List[Dict],
    description: str = "",
) -> AssertionCheck:
    """
    创建断言检查的便捷函数

    Args:
        name: 检查名称
        assertions: 断言定义列表 (字典格式)
        description: 描述

    Returns:
        断言检查对象
    """
    assertion_objects = [
        create_assertion(**a) for a in assertions
    ]
    return AssertionCheck(
        name=name,
        assertions=assertion_objects,
        description=description,
    )


def run_demo():
    """运行演示"""
    print("=" * 60)
    print("Assertion System Demo")
    print("=" * 60)

    # 创建检查
    check = create_check(
        name="Basic Functionality Check",
        assertions=[
            {"type": "contains", "value": "success", "description": "Contains 'success'", "weight": 0.5},
            {"type": "contains", "value": "completed", "description": "Contains 'completed'", "weight": 0.3},
            {"type": "threshold", "value": 0.8, "description": "Score >= 0.8", "weight": 0.2},
        ],
        description="Basic functionality assertions",
    )

    # 运行检查
    runner = AssertionRunner()
    actual_output = {"output": "Operation success - completed", "score": 0.85}

    result = runner.run(check, actual_output)

    print(f"\nCheck: {result.check.name}")
    print(f"Passed: {result.passed}")
    print(f"Score: {result.score:.2%}")
    print(f"Message: {result.message}")
    print("\nDetailed Results:")
    for r in result.results:
        print(f"  {r}")

    return result


if __name__ == "__main__":
    run_demo()
