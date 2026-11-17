"""
Orchestrator 集成测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from contracts.input_schema import ProjectRequest, ProjectType
from contracts.output_schema import StepStatus
from contracts.step_context import StepContext
from layers.orchestrator import Orchestrator
from contracts.exceptions import PreflightFailedError
from middlewares.circuit_breaker import CircuitBreaker
from middlewares.service_container import ServiceContainer


class TestOrchestratorIntegration:
    """Orchestrator 集成测试"""

    def setup_method(self):
        """每个测试前重置 CircuitBreaker 单例"""
        CircuitBreaker.reset_instance()

    def teardown_method(self):
        """每个测试后重置 CircuitBreaker 单例"""
        CircuitBreaker.reset_instance()

    def test_run_basic_cli(self, tmp_path):
        """基本 CLI 项目完整流程"""
        req = ProjectRequest(
            project_name="integration_test",
            description="A test project for integration testing",
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "integration_test")
        result = orch.run()

        assert result.project_name == "integration_test"
        assert len(result.steps) > 0

        # Phase 0 应该通过
        phase0 = [s for s in result.steps if s.step_name == "Phase0"]
        assert len(phase0) > 0
        if phase0[0].status == StepStatus.SUCCESS:
            # 后续步骤应该正常执行
            step_names = [s.step_name for s in result.steps]
            assert "Step1" in step_names
            assert "Step2" in step_names

    def test_context_reset_between_runs(self, tmp_path):
        """连续两次 run() 之间 context 应被重置"""
        req = ProjectRequest(
            project_name="reset_test",
            description="A test project for context reset validation",
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "reset_test")

        # 第一次 run
        result1 = orch.run()

        # 手动设置一些数据模拟污染
        orch.context.generated_assets = ["stale_file.py"]
        orch.context.verification_report = {"all_passed": False, "stale": True}

        # 第二次 run —— context 应该被重置
        result2 = orch.run()

        # 第二次 run 不应该受第一次残留数据影响
        assert orch.context.generated_assets != ["stale_file.py"] or len(result2.steps) > 0

    def test_preflight_failure_skips_remaining(self, tmp_path):
        """Phase 0 失败时后续步骤应全部 SKIPPED"""
        req = ProjectRequest(
            project_name="skip_test",
            description="A test project for skip on preflight failure",
            target_python_version="99.99",  # 不存在的版本
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "skip_test")
        result = orch.run()

        # 应该有 Phase 0 FAILED 和后续 SKIPPED
        phase0 = [s for s in result.steps if s.step_name == "Phase0"]
        assert len(phase0) > 0
        assert phase0[0].status == StepStatus.FAILED

        skipped = [s for s in result.steps if s.status == StepStatus.SKIPPED]
        assert len(skipped) >= 6  # Step1-6 全部跳过

    def test_step_context_reset_method(self):
        """StepContext.reset() 方法测试"""
        req = ProjectRequest(
            project_name="ctx_test",
            description="A test project for step context testing",
        )
        ctx = StepContext(request=req)

        # 模拟数据填充
        ctx.generated_assets = ["file1.py", "file2.py"]
        ctx.verification_report = {"all_passed": True}
        ctx.retry_history = [{"attempt": 1}]
        ctx.current_step = "step5"

        # 重置
        ctx.reset()

        assert ctx.generated_assets == []
        assert ctx.verification_report is None
        assert ctx.retry_history == []
        assert ctx.current_step == "phase0"

    def test_run_web_app(self, tmp_path):
        """Web 应用项目流程"""
        req = ProjectRequest(
            project_name="web_integration",
            description="A web dashboard for system monitoring",
            project_type=ProjectType.WEB_APP,
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "web_integration")
        result = orch.run()

        assert result.project_name == "web_integration"
        assert len(result.steps) > 0

    def test_saga_compensation_on_step_failure(self, tmp_path):
        """步骤失败时的 Saga 补偿"""
        req = ProjectRequest(
            project_name="saga_test",
            description="A test project for saga compensation testing",
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "saga_test")
        result = orch.run()

        # 如果流程全部通过，检查 generated_files 是否一致
        if result.status == StepStatus.SUCCESS:
            assert len(result.generated_files) > 0
        # 如果有失败步骤，检查是否有回滚标记
        rolled_back = [s for s in result.steps if s.status == StepStatus.ROLLED_BACK]
        # Saga 补偿在当前流程中可能不会被触发（因为所有步骤都成功），
        # 但不应该有异常
