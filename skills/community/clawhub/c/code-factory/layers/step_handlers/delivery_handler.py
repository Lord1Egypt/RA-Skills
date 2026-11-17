"""
Step 6 处理器 —— 交付输出
"""

from pathlib import Path
from typing import Dict, Any

from layers.step_handlers.base_handler import BaseStepHandler
from layers.deliverer import Deliverer
from contracts.step_context import StepContext


class DeliveryHandler(BaseStepHandler):
    """Step 6: 交付处理器"""

    def __init__(
        self,
        project_path: Path,
        project_name: str,
        context: StepContext,
    ):
        self.project_path = project_path
        self.project_name = project_name
        self.context = context
        self.deliverer = Deliverer()

    def execute(self) -> Dict[str, Any]:
        return self.deliverer.deliver(
            project_path=self.project_path,
            project_name=self.project_name,
            context=self.context,
        )
