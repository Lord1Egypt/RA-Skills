"""
端到端集成测试 —— 验证完整编排流程
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from contracts.input_schema import ProjectRequest, ProjectType
from layers.orchestrator import Orchestrator


class TestIntegration:
    """端到端集成测试"""

    def test_full_pipeline_basic(self, tmp_path):
        """基础完整流程测试"""
        req = ProjectRequest(
            project_name="integration_test",
            description="A simple integration test project for validation",
            project_type=ProjectType.CLI_TOOL,
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "integration_test")
        result = orch.run()

        # 验证基本输出
        assert result.project_name == "integration_test"
        assert len(result.steps) > 0

        # Phase 0 应该成功（当前 Python 版本应满足 3.10）
        phase0 = [s for s in result.steps if s.step_name == "Phase0"]
        if phase0:
            assert phase0[0].ok or phase0[0].status.value in ("skipped",)

    def test_pipeline_with_invalid_project_name(self, tmp_path):
        """无效项目名的处理"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="",  # 空名称
                description="A simple integration test project for validation",
            )

    def test_orchestrator_steps_order(self, tmp_path):
        """验证步骤执行顺序"""
        req = ProjectRequest(
            project_name="order_test",
            description="A simple project to test step execution order",
            project_type=ProjectType.CLI_TOOL,
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "order_test")
        result = orch.run()

        step_names = [s.step_name for s in result.steps]
        expected_order = ["Phase0", "Step1", "Step2", "Step3", "Step4", "Step5", "Step6"]
        # 验证出现的步骤顺序正确（可能有些被跳过）
        filtered = [s for s in expected_order if s in step_names]
        assert filtered == step_names

    def test_pipeline_generates_files(self, tmp_path):
        """验证文件生成"""
        req = ProjectRequest(
            project_name="file_gen_test",
            description="A simple project to test file generation during pipeline",
            project_type=ProjectType.CLI_TOOL,
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "file_gen_test")
        result = orch.run()

        # 检查是否有文件生成
        if result.all_passed:
            assert len(result.generated_files) > 0
            # 关键文件应该存在
            expected_files = ["src/main.py", "requirements.txt", "docs/README.md"]
            for ef in expected_files:
                assert (tmp_path / "file_gen_test" / ef).exists(), f"{ef} 不存在"

    def test_pipeline_idempotency(self, tmp_path):
        """验证同一输入执行两次结果一致（幂等性）"""
        req = ProjectRequest(
            project_name="idempotent_test",
            description="A simple project to verify idempotent execution",
            project_type=ProjectType.CLI_TOOL,
        )
        target = tmp_path / "idempotent_test"

        orch1 = Orchestrator(request=req, target_dir=target)
        result1 = orch1.run()

        orch2 = Orchestrator(request=req, target_dir=target)
        result2 = orch2.run()

        # 两次执行的文件列表应该一致
        assert set(result1.generated_files) == set(result2.generated_files)

    def test_dangerous_characters_rejected(self):
        """危险字符应该被拒绝"""
        with pytest.raises(ValueError, match="危险字符"):
            ProjectRequest(
                project_name="bad_project",
                description="A test; rm -rf / -- dangerous injection attempt here",
            )
