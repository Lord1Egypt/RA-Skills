"""
契约测试 —— 验证输入/输出 Schema 的正确性。

测试目标：
1. 无效输入被正确拒绝
2. 边界值正确处理
3. Schema 变更向后兼容
"""

import pytest
import sys
from pathlib import Path

# 确保项目根目录在 sys.path 中
sys.path.insert(0, str(Path(__file__).parent.parent))

from contracts.input_schema import ProjectRequest, ProjectType, AcceptanceCriterion
from contracts.output_schema import StepResult, StepStatus, ProjectResult
from contracts.step_context import StepContext


class TestInputSchema:
    """输入契约测试"""

    def test_valid_project_request(self):
        """有效输入应该通过校验"""
        req = ProjectRequest(
            project_name="my_tool",
            description="A simple CLI tool for file management",
            project_type=ProjectType.CLI_TOOL,
        )
        assert req.project_name == "my_tool"

    def test_empty_project_name_raises(self):
        """空项目名应该抛出异常"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="",
                description="A simple CLI tool for file management",
            )

    def test_reserved_name_raises(self):
        """保留字项目名应该抛出异常"""
        for name in ("test", "tmp", "temp"):
            with pytest.raises(ValueError):
                ProjectRequest(
                    project_name=name,
                    description="A simple CLI tool for file management",
                )

    def test_short_description_raises(self):
        """过短的描述应该抛出异常"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="my_tool",
                description="short",  # < 10 chars
            )

    def test_invalid_python_version_raises(self):
        """无效的 Python 版本格式应该抛出异常"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="my_tool",
                description="A simple CLI tool for file management",
                target_python_version="3",  # 缺少 minor
            )

    def test_name_with_special_chars_raises(self):
        """含特殊字符的项目名应该抛出异常"""
        with pytest.raises(ValueError):
            ProjectRequest(
                project_name="my-tool!",  # - and ! are invalid
                description="A simple CLI tool for file management",
            )

    def test_acceptance_criterion_validation(self):
        """验收标准应该校验字段长度"""
        with pytest.raises(ValueError):
            AcceptanceCriterion(given="", when="test", then="test")

        with pytest.raises(ValueError):
            AcceptanceCriterion(given="test", when="ab", then="test")  # < 5 chars

        with pytest.raises(ValueError):
            AcceptanceCriterion(given="test", when="test", then="test", priority=5)

    def test_from_dict(self):
        """from_dict 应该正确处理字典输入"""
        req = ProjectRequest.from_dict({
            "project_name": "my_tool",
            "description": "A simple CLI tool for file management",
            "project_type": "cli_tool",
        })
        assert req.project_name == "my_tool"
        assert req.project_type == ProjectType.CLI_TOOL


class TestOutputSchema:
    """输出契约测试"""

    def test_step_result_lifecycle(self):
        """StepResult 状态转换测试"""
        sr = StepResult(step_name="Phase0")
        assert sr.status == StepStatus.PENDING
        assert not sr.is_terminal

        sr.mark_running()
        assert sr.status == StepStatus.RUNNING
        assert sr.started_at is not None

        sr.mark_success({"all_ok": True})
        assert sr.status == StepStatus.SUCCESS
        assert sr.ok
        assert sr.is_terminal

    def test_step_result_failure(self):
        """StepResult 失败状态测试"""
        sr = StepResult(step_name="Step3")
        sr.mark_running()
        sr.mark_failed("磁盘空间不足")
        assert sr.status == StepStatus.FAILED
        assert not sr.ok
        assert "磁盘空间不足" in sr.errors[0]

    def test_project_result_all_passed(self):
        """ProjectResult 全部通过检测"""
        result = ProjectResult(
            project_path="/tmp/test",
            project_name="test",
            steps=[
                StepResult(step_name="Phase0", status=StepStatus.SUCCESS),
                StepResult(step_name="Step1", status=StepStatus.SUCCESS),
            ],
        )
        assert result.all_passed

    def test_project_result_with_failure(self):
        """ProjectResult 存在失败步骤检测"""
        result = ProjectResult(
            project_path="/tmp/test",
            project_name="test",
            steps=[
                StepResult(step_name="Phase0", status=StepStatus.SUCCESS),
                StepResult(step_name="Step1", status=StepStatus.FAILED),
            ],
        )
        assert not result.all_passed
        assert len(result.failed_steps) == 1

    def test_to_summary(self):
        """摘要生成测试"""
        result = ProjectResult(
            project_path="/tmp/test",
            project_name="test_project",
            steps=[
                StepResult(step_name="Phase0", status=StepStatus.SUCCESS),
            ],
            generated_files=["src/main.py", "tests/test_main.py"],
        )
        summary = result.to_summary()
        assert "test_project" in summary
        assert "src/main.py" in summary


class TestStepContext:
    """步骤上下文测试"""

    def test_context_initialization(self):
        """StepContext 初始化测试"""
        req = ProjectRequest(
            project_name="context_test",
            description="A test project for validation",
        )
        ctx = StepContext(request=req)
        assert ctx.current_step == "phase0"
        assert ctx.generated_assets == []
        assert ctx.retry_history == []

    def test_context_snapshot_update(self):
        """环境快照更新测试"""
        req = ProjectRequest(
            project_name="snapshot_test",
            description="A test project for validation",
        )
        ctx = StepContext(request=req)
        ctx.update_snapshot({"python_version": "3.10", "packages": []})
        assert ctx.environment_snapshot is not None
        assert ctx.current_step == "step1"

    def test_context_spec_update(self):
        """Spec 更新测试"""
        req = ProjectRequest(
            project_name="spec_test",
            description="A test project for validation",
        )
        ctx = StepContext(request=req)
        ctx.update_spec({"files": [], "dependencies": []})
        assert ctx.derived_spec is not None
        assert ctx.current_step == "step2"

    def test_retry_history(self):
        """重试历史记录测试"""
        req = ProjectRequest(
            project_name="retry_test",
            description="A test project for validation",
        )
        ctx = StepContext(request=req)
        ctx.add_retry_record(1, "测试失败", "直接修复")
        ctx.add_retry_record(2, "仍失败", "缩小范围")
        assert len(ctx.retry_history) == 2
        assert ctx.retry_history[0]["attempt"] == 1
        assert ctx.retry_history[0]["strategy"] == "直接修复"
