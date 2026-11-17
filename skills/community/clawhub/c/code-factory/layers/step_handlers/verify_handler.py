"""
Step 4 处理器 —— 自动验证
"""

from pathlib import Path
from typing import Dict, Any, List

from layers.step_handlers.base_handler import BaseStepHandler
from layers.verifier import Verifier, VerificationResult
from middlewares.anti_corruption import AntiCorruptionLayer, ContractViolationError


class VerifyHandler(BaseStepHandler):
    """Step 4: 自动验证处理器"""

    def __init__(
        self,
        target_dir: Path,
        assets: List[str],
        acl: AntiCorruptionLayer,
    ):
        self.target_dir = target_dir
        self.assets = assets
        self.acl = acl
        self.verifier = Verifier()

    def execute(self) -> Dict[str, Any]:
        result: VerificationResult = self.verifier.verify(
            target_dir=self.target_dir,
            assets=self.assets,
        )
        report = result.to_dict()
        validated = self.acl.validate_verification_output(report)
        if not validated.is_valid:
            raise ContractViolationError(
                step="Step4", field="verification",
                expected="valid report", got=str(validated.errors)
            )
        return validated.sanitized_data
