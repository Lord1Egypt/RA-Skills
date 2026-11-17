"""
Phase 0 处理器 —— 环境预检
"""

from pathlib import Path
from typing import Dict, Any, Optional, List

from layers.step_handlers.base_handler import BaseStepHandler
from layers.preflight import PreflightRunner, PreflightResult
from contracts.exceptions import PreflightFailedError


class PreflightHandler(BaseStepHandler):
    """Phase 0: 环境预检处理器"""

    def __init__(
        self,
        target_dir: Path,
        required_python: str,
        required_deps: List[str],
    ):
        self.target_dir = target_dir
        self.required_python = required_python
        self.required_deps = required_deps
        self.runner = PreflightRunner()

    def execute(self) -> Dict[str, Any]:
        preflight_result = self.runner.run(
            target_dir=self.target_dir,
            required_python=self.required_python,
            required_deps=self.required_deps,
        )
        if not preflight_result.all_ok:
            issues = [i for i in [
                preflight_result.python_issue,
                preflight_result.dir_issue,
                preflight_result.disk_issue,
                preflight_result.deps_issue,
            ] if i]
            raise PreflightFailedError("; ".join(issues))
        return {"preflight": preflight_result.to_dict()}
