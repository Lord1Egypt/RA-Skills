"""
Step 1 处理器 —— 环境快照
"""

from typing import Dict, Any, List

from layers.step_handlers.base_handler import BaseStepHandler
from middlewares.anti_corruption import AntiCorruptionLayer, ContractViolationError


class SnapshotHandler(BaseStepHandler):
    """Step 1: 环境快照处理器"""

    def __init__(
        self,
        python_version: str,
        dependencies: List[str],
        target_directory: str,
        acl: AntiCorruptionLayer,
    ):
        self.python_version = python_version
        self.dependencies = dependencies
        self.target_directory = target_directory
        self.acl = acl

    def execute(self) -> Dict[str, Any]:
        snapshot = {
            "python_version": self.python_version,
            "installed_packages": self.dependencies,
            "target_directory": self.target_directory,
        }
        validated = self.acl.validate_environment_snapshot(snapshot)
        if not validated.is_valid:
            raise ContractViolationError(
                step="Step1", field="environment_snapshot",
                expected="valid snapshot", got=str(validated.errors)
            )
        return validated.sanitized_data
