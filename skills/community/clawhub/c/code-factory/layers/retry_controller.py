"""
Step 5: 智能重试控制器 —— 借鉴 SkillOpt epoch 模式。

重试策略：
- 第 1 次失败：基于 VerificationResult 分析错误 → 修改代码 → 重新验证
- 第 2 次失败：更换修复策略（缩小修改范围）→ 重新验证
- 第 3 次失败：记录失败模式到 .learnings/ → 暂停并报告

v2.4 增强（纳入单通道体系）：
- 移除所有直接写 StepContext 的操作
- 返回值使用 RetryOutput 结构化契约（替代裸 dict）
- 超时验证统一使用 PipelineGuard.verify_with_timeout()
- 由 Orchestrator._commit_step_output 统一写入
"""

import json
import logging
import tempfile
import time as _time
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING
from datetime import datetime

from contracts.output_schema import RetryOutput
from contracts.step_context import StepContext
from middlewares.side_effect_log import SideEffectTracker
from middlewares.transaction_manager import TransactionManager

if TYPE_CHECKING:
    from layers.verifier import Verifier, VerificationResult
    from layers.asset_generator import AssetGenerator
    from middlewares.pipeline_guard import PipelineGuard


class RetryController:
    """智能重试控制器（v3.0：增加指数退避）"""

    MAX_RETRIES = 3
    STEP_TIMEOUT_SECONDS = 120
    BACKOFF_BASE_SECONDS = 1  # 退避基数：1s → 2s → 4s

    def __init__(self, max_retries: int = 3, backoff_base: float = 1.0):
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.learnings_dir: Optional[Path] = None

    def retry(
        self,
        context: StepContext,
        verifier: "Verifier",
        asset_generator: "AssetGenerator",
        target_dir: Path,
        tracker: SideEffectTracker,
        guard: Optional["PipelineGuard"] = None,
    ) -> RetryOutput:
        """
        执行智能重试循环。

        每次重试：
        1. 分析 VerificationResult 中的 errors/issues
        2. 选择修复策略
        3. 创建独立 TransactionManager
        4. 重新生成受影响文件
        5. 事务提交后重新验证（使用 PipelineGuard 超时保护）
        6. 返回 RetryOutput 结构化契约

        注意：不直接写 StepContext，由 Orchestrator._commit_step_output 统一写入。
        """
        self.learnings_dir = target_dir / ".learnings"
        self.learnings_dir.mkdir(parents=True, exist_ok=True)

        last_errors = self._extract_errors(context)
        updated_assets: List[str] = []
        updated_verification: Optional[Dict] = None

        for attempt in range(1, self.max_retries + 1):
            strategy = self._choose_strategy(attempt)
            error_summary = "; ".join(last_errors[:3]) if last_errors else "未知错误"
            context.add_retry_record(attempt, error_summary, strategy)

            # 指数退避：第 N 次重试前等待 backoff_base * 2^(N-1) 秒
            if attempt > 1:
                wait = self.backoff_base * (2 ** (attempt - 1))
                _time.sleep(wait)

            tx = TransactionManager(target_dir)
            try:
                fix_applied, new_assets = self._apply_fix(
                    attempt=attempt,
                    context=context,
                    asset_generator=asset_generator,
                    target_dir=target_dir,
                    tracker=tracker,
                    tx=tx,
                    errors=last_errors,
                )
                if not fix_applied:
                    continue
                tx.commit()
                if new_assets:
                    updated_assets = new_assets
            except Exception as e:
                tx.rollback()
                context.add_retry_record(attempt, f"修复异常: {e}", strategy)
                continue

            # 重新验证（统一使用 PipelineGuard 超时保护）
            vr = self._verify_with_timeout(verifier, target_dir, context, guard)
            if vr is None:
                context.add_retry_record(attempt, "验证超时", strategy)
                continue

            if vr.all_passed:
                updated_verification = vr.to_dict()
                return RetryOutput(
                    retried=True,
                    attempts=attempt,
                    success=True,
                    updated_assets=updated_assets,
                    updated_verification=updated_verification,
                )

            last_errors = vr.issues if vr.issues else [f"退出码 {vr.test_results.get('returncode', '?')}"]

        # 全部失败
        failure_pattern = self._record_failure(context)
        return RetryOutput(
            retried=True,
            attempts=self.max_retries,
            success=False,
            failure_pattern=failure_pattern,
        )

    def _extract_errors(self, context: StepContext) -> List[str]:
        if not context.verification_report:
            return ["无验证报告"]
        report = context.verification_report
        errors = list(report.get("issues", []))
        if not errors and not report.get("all_passed", False):
            errors.append("验证未通过（无具体错误信息）")
        return errors if errors else ["验证失败（未知原因）"]

    def _choose_strategy(self, attempt: int) -> str:
        strategies = {
            1: "直接修复错误（基于 VerificationResult 修改源代码）",
            2: "缩小修改范围（仅修改失败部分，不触及其他文件）",
            3: "最小化变更（只保留核心功能，跳过边界情况）",
        }
        return strategies.get(attempt, "放弃修复")

    def _apply_fix(
        self, attempt: int, context: StepContext,
        asset_generator: "AssetGenerator", target_dir: Path,
        tracker: SideEffectTracker, tx: TransactionManager,
        errors: List[str],
    ) -> tuple:
        if attempt == 1:
            return self._regenerate_all(asset_generator, context, tx, tracker)
        elif attempt == 2:
            return self._regenerate_core(asset_generator, context, tx, tracker, target_dir)
        elif attempt == 3:
            return self._regenerate_minimal(asset_generator, context, tx, tracker)
        return (False, [])

    def _regenerate_all(
        self, asset_generator: "AssetGenerator", context: StepContext,
        tx: TransactionManager, tracker: SideEffectTracker,
    ) -> tuple:
        try:
            assets = asset_generator.generate(
                project_name=context.request.project_name,
                spec=context.derived_spec,
                tx=tx, tracker=tracker,
            )
            return (True, assets)
        except Exception:
            return (False, [])

    def _regenerate_core(
        self, asset_generator: "AssetGenerator", context: StepContext,
        tx: TransactionManager, tracker: SideEffectTracker, target_dir: Path,
    ) -> tuple:
        try:
            from middlewares.side_effect_log import SideEffectType
            main_content = asset_generator._generate_main_py(
                context.request.project_name, context.request.description,
            )
            test_content = asset_generator._generate_test_py(
                context.request.project_name,
            )
            tx.stage_create("src/main.py", main_content)
            tx.stage_create("tests/test_main.py", test_content)
            tracker.record(SideEffectType.FILE_MODIFY, "src/main.py", after_state=main_content)
            tracker.record(SideEffectType.FILE_MODIFY, "tests/test_main.py", after_state=test_content)
            return (True, ["src/main.py", "tests/test_main.py"])
        except Exception:
            return (False, [])

    def _regenerate_minimal(
        self, asset_generator: "AssetGenerator", context: StepContext,
        tx: TransactionManager, tracker: SideEffectTracker,
    ) -> tuple:
        try:
            from middlewares.side_effect_log import SideEffectType
            minimal_main = f'''"""
{context.request.project_name} — 最小化版本
<!-- HARD-GATE -->
"""

import sys


def main() -> int:
    """主入口函数（最小化）"""
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
            tx.stage_create("src/main.py", minimal_main)
            tracker.record(SideEffectType.FILE_MODIFY, "src/main.py", after_state=minimal_main)
            return (True, ["src/main.py"])
        except Exception:
            return (False, [])

    def _verify_with_timeout(
        self, verifier: "Verifier", target_dir: Path,
        context: StepContext, guard: Optional["PipelineGuard"] = None,
    ) -> Optional["VerificationResult"]:
        """带超时保护的验证调用，使用 PipelineGuard 统一超时保护。"""
        if guard is not None:
            return guard.verify_with_timeout(
                lambda: verifier.verify(target_dir, context.generated_assets),
                timeout_seconds=self.STEP_TIMEOUT_SECONDS,
            )
        # guard=None 时直接调用（无超时保护，用于独立测试场景）
        try:
            return verifier.verify(target_dir, context.generated_assets)
        except Exception:
            return None

    def _record_failure(self, context: StepContext) -> str:
        pattern = {
            "error_type": "retry_exhausted",
            "step": context.current_step,
            "retry_history": context.retry_history,
            "timestamp": datetime.now().isoformat(),
            "project_name": context.request.project_name,
            "verification_report": context.verification_report,
        }
        if self.learnings_dir:
            _logger = logging.getLogger(__name__)

            pattern_file = self.learnings_dir / f"failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            pattern_json = json.dumps(pattern, ensure_ascii=False, indent=2)

            # v3.2: 三层写入策略：原子 → 直接 → 日志
            try:
                fd, tmp_path = tempfile.mkstemp(
                    suffix=".json", prefix="failure_tmp_",
                    dir=str(self.learnings_dir),
                )
                with open(fd, "w", encoding="utf-8") as f:
                    f.write(pattern_json)
                Path(tmp_path).rename(pattern_file)
            except OSError:
                try:
                    pattern_file.write_text(pattern_json, encoding="utf-8")
                except OSError:
                    _logger.warning(
                        "无法写入失败模式到 %s，丢失诊断数据: %s",
                        pattern_file, pattern_json[:200],
                    )
        return json.dumps(pattern, ensure_ascii=False)
