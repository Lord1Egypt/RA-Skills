"""
Step 5 处理器 —— 智能重试
"""

import dataclasses
from pathlib import Path
from typing import Dict, Any

from layers.step_handlers.base_handler import BaseStepHandler
from layers.retry_controller import RetryController
from layers.verifier import Verifier
from layers.asset_generator import AssetGenerator
from contracts.step_context import StepContext
from contracts.output_schema import RetryOutput
from middlewares.side_effect_log import SideEffectTracker
from middlewares.pipeline_guard import PipelineGuard


class RetryHandler(BaseStepHandler):
    """Step 5: 智能重试处理器"""

    def __init__(
        self,
        context: StepContext,
        verifier: Verifier,
        asset_generator: AssetGenerator,
        target_dir: Path,
        tracker: SideEffectTracker,
        guard: PipelineGuard,
    ):
        self.context = context
        self.verifier = verifier
        self.asset_generator = asset_generator
        self.target_dir = target_dir
        self.tracker = tracker
        self.guard = guard
        self.controller = RetryController(max_retries=3)

    def execute(self) -> Dict[str, Any]:
        if not self.context.verification_report:
            return dataclasses.asdict(RetryOutput(
                retried=False, attempts=0, success=False,
                reason="无需重试（无验证报告）",
            ))

        report = self.context.verification_report
        if report.get("all_passed", False):
            return dataclasses.asdict(RetryOutput(
                retried=False, attempts=0, success=True,
                reason="验证已通过，无需重试",
            ))

        retry_result: RetryOutput = self.controller.retry(
            context=self.context,
            verifier=self.verifier,
            asset_generator=self.asset_generator,
            target_dir=self.target_dir,
            tracker=self.tracker,
            guard=self.guard,
        )
        return dataclasses.asdict(retry_result)
