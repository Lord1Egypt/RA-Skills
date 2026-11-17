"""
StepRegistry 单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.step_registry import (
    STEP_REGISTRY,
    StepDefinition,
    get_step_definition,
    validate_pipeline,
)


class TestStepRegistry:
    """StepRegistry 测试"""

    def test_all_steps_registered(self):
        """7 个步骤全部注册"""
        names = {sd.name for sd in STEP_REGISTRY}
        expected = {"Phase0", "Step1", "Step2", "Step3", "Step4", "Step5", "Step6"}
        assert names == expected

    def test_step_order(self):
        """步骤顺序正确"""
        names = [sd.name for sd in STEP_REGISTRY]
        assert names == ["Phase0", "Step1", "Step2", "Step3", "Step4", "Step5", "Step6"]

    def test_dependency_chain(self):
        """依赖链正确：Phase0→Step1→Step2→Step3→Step4→Step5→Step6"""
        deps = {
            "Phase0": None,
            "Step1": "Phase0",
            "Step2": "Step1",
            "Step3": "Step2",
            "Step4": "Step3",
            "Step5": "Step4",
            "Step6": "Step5",
        }
        for sd in STEP_REGISTRY:
            assert sd.depends_on == deps[sd.name], f"{sd.name} 依赖错误"

    def test_get_step_definition_known(self):
        """已知步骤可查到"""
        sd = get_step_definition("Phase0")
        assert sd is not None
        assert sd.name == "Phase0"

    def test_get_step_definition_unknown(self):
        """未知步骤返回 None"""
        sd = get_step_definition("Step99")
        assert sd is None

    def test_validate_pipeline_no_errors(self):
        """当前管道无错误"""
        errors = validate_pipeline()
        assert errors == []

    def test_commit_fns_exist(self):
        """Phase0-Step5 有 commit_fn，Step6 为 None"""
        for sd in STEP_REGISTRY:
            if sd.name == "Step6":
                assert sd.commit_fn is None, f"{sd.name} 的 commit_fn 应为 None"
            else:
                assert sd.commit_fn is not None, f"{sd.name} 缺少 commit_fn"

    def test_output_types_registered(self):
        """所有步骤都有 output_type"""
        for sd in STEP_REGISTRY:
            assert sd.output_type is not None, f"{sd.name} 缺少 output_type"

    def test_has_side_effects_flag(self):
        """Step3 和 Step5 标记 has_side_effects=True（会产生磁盘副作用）"""
        side_effect_steps = {"Step3", "Step5"}
        for sd in STEP_REGISTRY:
            if sd.name in side_effect_steps:
                assert sd.has_side_effects, f"{sd.name} 应标记 has_side_effects=True"
            else:
                assert not sd.has_side_effects, f"{sd.name} 不应标记 has_side_effects=True"

    def test_step_definition_is_named_tuple(self):
        """StepDefinition 是 NamedTuple"""
        sd = get_step_definition("Phase0")
        assert isinstance(sd, StepDefinition)
        # 可访问字段
        assert hasattr(sd, "name")
        assert hasattr(sd, "depends_on")
        assert hasattr(sd, "commit_fn")
        assert hasattr(sd, "output_type")
        assert hasattr(sd, "has_side_effects")
