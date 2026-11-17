"""
输出数据契约 —— 最终交付和各步骤的统一输出格式。

统一成功/失败标准，而非"抛异常就是失败"。
"""

from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"        # 前置条件不满足，跳过
    ROLLED_BACK = "rolled_back" # 已回滚
    TIMED_OUT = "timed_out"     # 超时


@dataclass
class StepResult:
    """每个步骤的统一输出契约"""
    step_name: str
    status: StepStatus = StepStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    output_data: Dict = field(default_factory=dict)  # 结构化输出，禁止裸 str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    retry_count: int = 0
    duration_seconds: float = 0.0

    def mark_running(self) -> None:
        self.status = StepStatus.RUNNING
        self.started_at = datetime.now().isoformat()

    def mark_success(self, output: Dict = None) -> None:
        self.status = StepStatus.SUCCESS
        self.completed_at = datetime.now().isoformat()
        if output:
            self.output_data = output

    def mark_failed(self, error: str) -> None:
        self.status = StepStatus.FAILED
        self.completed_at = datetime.now().isoformat()
        self.errors.append(error)

    def mark_skipped(self, reason: str) -> None:
        self.status = StepStatus.SKIPPED
        self.warnings.append(reason)

    def mark_timed_out(self) -> None:
        self.status = StepStatus.TIMED_OUT
        self.completed_at = datetime.now().isoformat()
        self.errors.append("步骤执行超时")

    @property
    def is_terminal(self) -> bool:
        """是否已到达终态"""
        return self.status in (
            StepStatus.SUCCESS,
            StepStatus.FAILED,
            StepStatus.SKIPPED,
            StepStatus.TIMED_OUT,
            StepStatus.ROLLED_BACK,
        )

    @property
    def ok(self) -> bool:
        """是否成功完成"""
        return self.status == StepStatus.SUCCESS


@dataclass
class RetryOutput:
    """Step 5 重试输出的结构化契约"""
    retried: bool
    attempts: int
    success: bool = False
    updated_assets: List[str] = field(default_factory=list)
    updated_verification: Optional[Dict] = None
    failure_pattern: str = ""
    reason: str = ""


@dataclass
class ProjectResult:
    """最终交付的统一输出契约"""

    project_path: str
    project_name: str
    status: StepStatus = StepStatus.PENDING
    steps: List[StepResult] = field(default_factory=list)
    manifest_path: str = ""
    test_results: Dict = field(default_factory=dict)
    generated_files: List[str] = field(default_factory=list)
    failure_learnings: Optional[str] = None
    total_duration_seconds: float = 0.0

    @property
    def all_passed(self) -> bool:
        """所有步骤是否全部成功（至少有一个 SUCCESS 步骤，且无 FAILED）"""
        if not self.steps:
            return False
        has_success = any(s.ok for s in self.steps)
        no_failures = all(
            s.ok or s.status in (StepStatus.SKIPPED, StepStatus.ROLLED_BACK)
            for s in self.steps
        )
        return has_success and no_failures

    @property
    def failed_steps(self) -> List[StepResult]:
        """获取所有失败的步骤"""
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    def to_summary(self) -> str:
        """生成人类可读的摘要"""
        lines = [
            f"项目: {self.project_name}",
            f"路径: {self.project_path}",
            f"状态: {self.status.value}",
            f"耗时: {self.total_duration_seconds:.1f}s",
            "",
            "步骤明细:",
        ]
        for step in self.steps:
            icon = "✅" if step.ok else "❌" if step.status == StepStatus.FAILED else "⏭️"
            lines.append(f"  {icon} {step.step_name}: {step.status.value}"
                         + (f" (重试 {step.retry_count} 次)" if step.retry_count else ""))
            for err in step.errors:
                lines.append(f"      ⚠️ {err}")
        if self.generated_files:
            lines.append(f"\n生成文件 ({len(self.generated_files)}):")
            for f in self.generated_files:
                lines.append(f"  📄 {f}")
        return "\n".join(lines)
