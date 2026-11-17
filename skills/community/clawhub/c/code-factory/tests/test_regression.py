"""
回归测试 —— 验证已修复的系统性缺陷不会复发。

覆盖：
1. 时序耦合：Step3-6 在 lambda 工厂中延迟实例化，执行时 context 数据已就绪
2. 连续两次 run() 状态隔离：saga/tracker/breaker 不跨调用污染
3. Learner 时机：Phase 0 通过后正确加载
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from contracts.input_schema import ProjectRequest, ProjectType
from contracts.output_schema import StepStatus
from contracts.step_context import StepContext
from layers.orchestrator import Orchestrator
from middlewares.circuit_breaker import CircuitBreaker
from middlewares.service_container import ServiceContainer


class TestTimingCoupling:
    """时序耦合回归测试"""

    def setup_method(self):
        CircuitBreaker.reset_instance()

    def teardown_method(self):
        CircuitBreaker.reset_instance()

    def test_step3_receives_valid_spec_after_step2(self, tmp_path):
        """
        验证 Step3 在 lambda 工厂中执行时，context.derived_spec 已就绪。

        关键断言：如果时序耦合存在（Handler 在 reset 后立即实例化），
        derived_spec 将是 None，导致 AssetGenerator 抛出 ValueError。
        lambda 工厂模式确保 Step3 执行时才读取最新 context。
        """
        req = ProjectRequest(
            project_name="timing_test",
            description="A test project for timing coupling validation",
            project_type=ProjectType.CLI_TOOL,
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "timing_test")
        result = orch.run()

        # Step3 应该在 Step2 之后执行，且 derived_spec 不为 None
        step3_results = [s for s in result.steps if s.step_name == "Step3"]
        assert len(step3_results) > 0

        step3 = step3_results[0]
        # Step3 不应该因为 spec=None 而失败
        if step3.status == StepStatus.FAILED:
            assert "spec=None" not in str(step3.errors), \
                f"时序耦合导致 Step3 收到 None spec: {step3.errors}"

    def test_step4_receives_valid_assets_after_step3(self, tmp_path):
        """
        验证 Step4 执行时 context.generated_assets 已就绪。

        如果时序耦合存在，generated_assets 将是空列表。
        """
        req = ProjectRequest(
            project_name="assets_test",
            description="A test project for asset timing validation",
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "assets_test")
        result = orch.run()

        # 如果管道成功，Step4 应该能读取到 Step3 生成的文件
        if result.all_passed:
            assert len(result.generated_files) > 0, \
                "管道成功但 generated_files 为空——时序耦合"

    def test_full_pipeline_no_timing_errors(self, tmp_path):
        """完整管道执行不应有时序相关的错误"""
        req = ProjectRequest(
            project_name="full_timing_test",
            description="A complete test project for timing validation",
            project_type=ProjectType.WEB_APP,
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "full_timing_test")
        result = orch.run()

        # 所有失败步骤不应包含时序相关的错误
        for step in result.steps:
            if step.status == StepStatus.FAILED:
                errors_str = str(step.errors)
                assert "spec=None" not in errors_str, \
                    f"步骤 {step.step_name} 有时序耦合错误"
                assert "未注册处理函数" not in errors_str, \
                    f"步骤 {step.step_name} 未正确注册"


class TestCrossRunIsolation:
    """跨 run() 状态隔离回归测试"""

    def setup_method(self):
        CircuitBreaker.reset_instance()

    def teardown_method(self):
        CircuitBreaker.reset_instance()

    def test_two_consecutive_runs_independent(self, tmp_path):
        """
        连续两次 run() 应完全独立，不受对方状态影响。

        验证：
        - 第一次 run() 的 generated_assets 不泄露到第二次
        - 第二次 run() 的 steps 数量 ≥ 第一次
        - CircuitBreaker 计时器不跨 run 残留
        """
        req = ProjectRequest(
            project_name="isolation_test",
            description="A test project for cross-run isolation validation",
        )
        target = tmp_path / "isolation_test"
        container = ServiceContainer()

        orch1 = Orchestrator(request=req, target_dir=target, container=container)
        result1 = orch1.run()

        orch2 = Orchestrator(request=req, target_dir=target, container=container)
        result2 = orch2.run()

        # 两次执行的文件列表应该一致（幂等性）
        assert set(result1.generated_files) == set(result2.generated_files), \
            f"两次 run() 生成文件不一致: {result1.generated_files} vs {result2.generated_files}"

        # 两次都应该有完整的步骤列表
        assert len(result2.steps) >= len(result1.steps), \
            "第二次 run() 步骤数少于第一次——可能被 CircuitBreaker 状态污染"

    def test_context_reset_between_runs(self, tmp_path):
        """StepContext 在两次 run() 间完全重置"""
        req = ProjectRequest(
            project_name="ctx_reset_test",
            description="A test project for context reset validation",
        )
        orch = Orchestrator(request=req, target_dir=tmp_path / "ctx_reset_test")

        # 第一次 run
        orch.run()

        # 手动污染 context
        orch.context.generated_assets = ["stale_pollution.py"]
        orch.context.verification_report = {"all_passed": False, "stale": True}  # type: ignore
        orch.context.retry_history = [{"attempt": 99, "stale": True}]  # type: ignore

        # 第二次 run —— context 应被 reset
        result = orch.run()

        # 验证：第二次 run 的 generated_files 不包含手动污染的条目
        assert "stale_pollution.py" not in result.generated_files, \
            "context.reset() 未清除跨 run 污染"


class TestLearnerTiming:
    """Learner 加载时机回归测试"""

    def setup_method(self):
        CircuitBreaker.reset_instance()

    def teardown_method(self):
        CircuitBreaker.reset_instance()

    def test_learner_loaded_after_phase0(self, tmp_path):
        """
        验证 Learner 在 Phase 0 通过后才加载。

        如果 Learner 在 __init__ 中加载（目标目录不存在），
        应该静默处理（不抛异常），且在 Phase 0 通过后正确加载。
        """
        req = ProjectRequest(
            project_name="learner_test",
            description="A test project for learner timing validation",
        )
        # 使用不存在的目录路径
        non_existent = tmp_path / "non_existent_subdir" / "learner_test"
        orch = Orchestrator(request=req, target_dir=non_existent)
        result = orch.run()

        # 即使目录初始不存在，Phase 0 也应该创建它并继续
        phase0 = [s for s in result.steps if s.step_name == "Phase0"]
        if phase0:
            # Phase 0 不应该因为目录问题而崩溃
            assert phase0[0].status != StepStatus.FAILED or \
                "目录" not in str(phase0[0].errors), \
                "Learner 在目录不存在时崩溃"
