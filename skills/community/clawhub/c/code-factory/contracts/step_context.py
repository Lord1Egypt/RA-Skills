"""
步骤上下文（StepContext）—— 步骤间传递的结构化状态对象。

这是防腐层的唯一数据载体，所有步骤间传递必须经过此对象。
杜绝"自然语言猜测"式数据传递。

v2.3 增强：
- 增加 update_preflight() 写入 Phase0 真实预检结果
- get_step_output("Phase0") 改为读取真实数据（非硬编码假数据）
- 数据流单通道：所有写入由 Orchestrator._commit_step_output() 统一调用

v3.0 增强：
- 字段类型标注从 Optional[Dict] 升级为具体的 TypedDict 类型
- 编译期和 IDE 可检查步骤间数据传递的类型安全性
"""

import copy
import threading
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from contracts.input_schema import ProjectRequest
from contracts.step_outputs import (
    PreflightOutput,
    EnvironmentSnapshotOutput,
    SpecOutput,
    VerificationOutput,
)


@dataclass
class StepContext:
    """步骤间传递的全局状态对象（线程安全）"""

    request: ProjectRequest

    # Phase 0 输出：预检结果
    preflight_result: Optional[PreflightOutput] = None

    # Step 1 输出：环境快照
    environment_snapshot: Optional[EnvironmentSnapshotOutput] = None

    # Step 2 输出：推导出的 Spec
    derived_spec: Optional[SpecOutput] = None

    # Step 3 输出：已生成的资产文件列表
    generated_assets: List[str] = field(default_factory=list)

    # Step 4 输出：验证报告
    verification_report: Optional[VerificationOutput] = None

    # Step 5 记录：重试历史
    retry_history: List[Dict] = field(default_factory=list)

    # 状态追踪
    current_step: str = "phase0"
    global_timeout_seconds: int = 600

    # 副作用追踪引用（用于回滚）
    staged_files: List[str] = field(default_factory=list)

    # ── 线程安全 ──────────────────────────────────

    _lock: threading.RLock = field(default_factory=threading.RLock, repr=False)

    # ── 状态更新（加锁） ──────────────────────────

    def update_preflight(self, data: PreflightOutput) -> None:
        """更新 Phase 0 预检结果"""
        with self._lock:
            self.preflight_result = {
                "python_ok": data.get("python_ok", False),
                "dir_writable": data.get("dir_writable", False),
                "disk_sufficient": data.get("disk_sufficient", False),
                "deps_available": data.get("deps_available", True),
                "issues": list(data.get("issues", [])),
            }
            self.current_step = "phase0"

    def update_snapshot(self, snapshot: EnvironmentSnapshotOutput) -> None:
        """更新环境快照（Step 1 输出）"""
        with self._lock:
            self.environment_snapshot = copy.deepcopy(snapshot)
            self.current_step = "step1"

    def update_spec(self, spec: SpecOutput) -> None:
        """更新 Spec 推导结果（Step 2 输出）"""
        with self._lock:
            self.derived_spec = copy.deepcopy(spec)
            self.current_step = "step2"

    def update_assets(self, assets: List[str]) -> None:
        """更新生成的资产列表（Step 3 输出）"""
        with self._lock:
            self.generated_assets = list(assets)
            self.current_step = "step3"

    def update_verification(self, report: VerificationOutput) -> None:
        """更新验证报告（Step 4 输出）"""
        with self._lock:
            self.verification_report = copy.deepcopy(report)
            self.current_step = "step4"

    def add_retry_record(self, attempt: int, error: str, strategy: str) -> None:
        """记录一次重试（Step 5）"""
        from datetime import datetime
        with self._lock:
            self.retry_history.append({
                "attempt": attempt,
                "error": error,
                "strategy": strategy,
                "timestamp": datetime.now().isoformat(),
            })
            self.current_step = "step5"

    # ── 安全读取 ──────────────────────────────────

    def get_step_output(self, step_name: str) -> Dict[str, object]:
        """
        获取指定步骤的输出，用于防腐层校验。

        Phase0 现在读取真实预检结果，不再使用硬编码假数据。
        """
        with self._lock:
            mapping: Dict[str, Dict[str, object]] = {
                "Phase0": self.preflight_result or {
                    "python_ok": False,
                    "dir_writable": False,
                    "disk_sufficient": False,
                    "deps_available": True,
                    "issues": ["Phase 0 尚未执行或预检结果未写入"],
                },
                "Step1": self.environment_snapshot or {},
                "Step2": self.derived_spec or {},
                "Step3": {"generated_files": list(self.generated_assets)},
                "Step4": self.verification_report or {},
                "Step5": {
                    "retried": bool(self.retry_history),
                    "attempts": len(self.retry_history),
                    "success": (
                        self.verification_report is not None
                        and self.verification_report.get("all_passed", False)
                    ),
                },
            }
            return mapping.get(step_name, {})

    def snapshot(self) -> Dict[str, object]:
        """返回当前状态的深拷贝快照（不可变）。"""
        with self._lock:
            return {
                "current_step": self.current_step,
                "preflight_result": copy.deepcopy(self.preflight_result),
                "environment_snapshot": copy.deepcopy(self.environment_snapshot),
                "derived_spec": copy.deepcopy(self.derived_spec),
                "generated_assets": list(self.generated_assets),
                "verification_report": copy.deepcopy(self.verification_report),
                "retry_history": copy.deepcopy(self.retry_history),
                "staged_files": list(self.staged_files),
            }

    def reset(self) -> None:
        """
        重置所有步骤数据，每次 run() 调用前执行。

        防止连续 run() 调用间数据污染：
        - 上一次的 generated_assets 不会泄露到本次
        - 上一次的 verification_report 不会误导本次的 retry 判断
        - 上一次的 retry_history 不会累积
        """
        with self._lock:
            self.preflight_result = None
            self.environment_snapshot = None
            self.derived_spec = None
            self.generated_assets = []
            self.verification_report = None
            self.retry_history = []
            self.staged_files = []
            self.current_step = "phase0"
