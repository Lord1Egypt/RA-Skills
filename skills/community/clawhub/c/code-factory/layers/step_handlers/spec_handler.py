"""
Step 2 处理器 —— Spec 推导
"""

from typing import Dict, Any, List, Optional

from layers.step_handlers.base_handler import BaseStepHandler
from layers.spec_engine import SpecEngine, SpecResult
from contracts.input_schema import ProjectType, AcceptanceCriterion
from middlewares.anti_corruption import AntiCorruptionLayer, ContractViolationError


class SpecHandler(BaseStepHandler):
    """Step 2: Spec 推导处理器"""

    def __init__(
        self,
        description: str,
        project_type: ProjectType,
        acceptance_criteria: List[AcceptanceCriterion],
        acl: AntiCorruptionLayer,
    ):
        self.description = description
        self.project_type = project_type
        self.acceptance_criteria = acceptance_criteria
        self.acl = acl
        self.engine = SpecEngine()

    def execute(self) -> Dict[str, Any]:
        spec: SpecResult = self.engine.derive(
            description=self.description,
            project_type=self.project_type,
            acceptance_criteria=self.acceptance_criteria,
        )
        spec_dict = spec.to_dict()
        validated = self.acl.validate_spec_output(spec_dict)
        if not validated.is_valid:
            raise ContractViolationError(
                step="Step2", field="spec", expected="valid spec",
                got=str(validated.errors)
            )
        return validated.sanitized_data
