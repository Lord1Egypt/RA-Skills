"""
管道守护者（PipelineGuard）—— 统一包装所有步骤执行。

职责：
1. 从 Orchestrator 提取 _execute_step，提供统一的执行保护
2. 确保重试循环内部调用也经过保护（熔断 + 超时 + 异常捕获）
3. 步骤间强制防腐层校验

用法：
    guard = PipelineGuard(breaker, acl)
    result = guard.execute("Step4", lambda: verifier.verify(...), from_step="Step3")
"""

import time
from typing import Callable, Any, Dict, Optional

from middlewares.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    GlobalTimeoutError,
)
from middlewares.anti_corruption import (
    AntiCorruptionLayer,
    ContractViolationError,
    ValidationResult,
)
from contracts.output_schema import StepResult, StepStatus


class PipelineGuard:
    """
    管道守护者 —— 统一执行保护。

    三重保护：
    1. 熔断状态检查（CircuitBreaker）
    2. 全局/步骤超时控制
    3. 异常捕获与结构化错误报告
    """

    def __init__(
        self,
        breaker: CircuitBreaker,
        acl: Optional[AntiCorruptionLayer] = None,
    ):
        self.breaker = breaker
        self.acl = acl or AntiCorruptionLayer()

    def execute_step(
        self,
        step_name: str,
        step_fn: Callable[[], Any],
    ) -> StepResult:
        """
        执行单个步骤，带完整保护。

        Args:
            step_name: 步骤名称（如 "Step3"）
            step_fn: 步骤执行函数

        Returns:
            StepResult 包含执行状态、输出、错误信息
        """
        step_result = StepResult(step_name=step_name)
        step_result.mark_running()
        step_start = time.monotonic()

        try:
            output = self.breaker.execute_protected(step_fn)
            step_result.mark_success(output if isinstance(output, dict) else {})
        except CircuitBreakerOpenError:
            step_result.mark_failed("熔断器已打开，拒绝执行")
        except GlobalTimeoutError:
            step_result.mark_timed_out()
        except ContractViolationError as e:
            step_result.mark_failed(f"契约违规: {e}")
            self.breaker.record_failure()
        except Exception as e:
            step_result.mark_failed(f"{type(e).__name__}: {e}")
            self.breaker.record_failure()

        step_result.duration_seconds = time.monotonic() - step_start

        if step_result.ok:
            self.breaker.record_success()

        return step_result

    def execute_with_validation(
        self,
        step_name: str,
        step_fn: Callable[[], Any],
        from_step: str,
        raw_data: Dict[str, Any],
    ) -> StepResult:
        """
        执行步骤 + 输入/输出防腐层双重校验。

        1. 先校验上一步的输出（raw_data）作为当前步骤的输入
        2. 执行当前步骤
        3. 校验当前步骤的输出是否符合契约
           - 失败时标记 step_result 为 FAILED（而非仅 warning）

        Args:
            step_name: 当前步骤名称
            step_fn: 当前步骤执行函数
            from_step: 上一步骤名称（用于选择输入校验器）
            raw_data: 上一步骤的原始输出（允许空字典，由校验器决定是否合法）

        Returns:
            StepResult
        """
        # 1. 校验输入（不再短路空字典——让校验器自行判断）
        if from_step:
            validated: ValidationResult = self.acl.validate_step_transition(
                from_step, raw_data
            )
            if not validated.is_valid:
                error_msgs = [str(e) for e in validated.errors]
                sr = StepResult(step_name=step_name)
                sr.mark_failed(
                    f"防腐层输入校验失败 [{from_step}→{step_name}]: {'; '.join(error_msgs)}"
                )
                return sr

        # 2. 执行步骤
        step_result = self.execute_step(step_name, step_fn)

        # 3. 校验输出（失败时标记 FAILED，不再只是 warning）
        if step_result.ok and step_result.output_data:
            try:
                output_validated: ValidationResult = self.acl.validate_step_transition(
                    step_name, step_result.output_data
                )
                if not output_validated.is_valid:
                    error_msgs = [str(e) for e in output_validated.errors]
                    # 输出校验失败 → 标记为 FAILED
                    step_result.status = StepStatus.FAILED
                    step_result.errors.append(
                        f"防腐层输出校验失败 [{step_name}]: {'; '.join(error_msgs)}"
                    )
            except ValueError:
                # 某些步骤没有对应的输出校验器，忽略
                pass

        return step_result

    def verify_with_timeout(
        self,
        verify_fn: Callable[[], Any],
        timeout_seconds: Optional[int] = None,
    ) -> Optional[Any]:
        """
        带超时保护的验证调用（保留供外部使用）。

        RetryController 有自带的 _verify_with_timeout，
        此方法保留作为 PipelineGuard 的公开 API。
        """
        try:
            return self.breaker.execute_with_timeout(
                verify_fn,
                timeout_seconds=timeout_seconds,
                on_timeout=None,
            )
        except Exception:
            return None
