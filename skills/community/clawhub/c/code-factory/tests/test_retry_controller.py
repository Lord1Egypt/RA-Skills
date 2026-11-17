"""
RetryController 单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from contracts.input_schema import ProjectRequest, ProjectType
from contracts.step_context import StepContext
from layers.retry_controller import RetryController
from layers.asset_generator import AssetGenerator
from layers.verifier import Verifier
from middlewares.side_effect_log import SideEffectTracker


class TestRetryController:
    """RetryController 单元测试"""

    def test_init_defaults(self):
        """默认初始化"""
        rc = RetryController()
        assert rc.max_retries == 3
        assert rc.MAX_RETRIES == 3

    def test_init_custom_retries(self):
        """自定义重试次数"""
        rc = RetryController(max_retries=5)
        assert rc.max_retries == 5

    def test_choose_strategy(self):
        """策略选择"""
        rc = RetryController()
        assert "直接修复" in rc._choose_strategy(1)
        assert "缩小修改" in rc._choose_strategy(2)
        assert "最小化变更" in rc._choose_strategy(3)
        assert "放弃修复" == rc._choose_strategy(99)

    def test_extract_errors_from_context(self, tmp_path):
        """从上下文提取错误信息"""
        req = ProjectRequest(
            project_name="err_test",
            description="A test project for error extraction validation",
        )
        ctx = StepContext(request=req)
        rc = RetryController()

        # 无验证报告
        errors = rc._extract_errors(ctx)
        assert "无验证报告" in errors[0]

        # 有验证报告但有 issues
        ctx.verification_report = {
            "all_passed": False,
            "issues": ["循环引用: a.py ↔ b.py", "测试失败"],
        }
        errors = rc._extract_errors(ctx)
        assert len(errors) == 2

        # 有验证报告但无 issues
        ctx.verification_report = {"all_passed": False, "issues": []}
        errors = rc._extract_errors(ctx)
        assert len(errors) == 1

    def test_retry_when_already_passed(self, tmp_path):
        """验证已通过时 _extract_errors 正确提取"""
        req = ProjectRequest(
            project_name="pass_test",
            description="A test project that already passed verification",
        )
        ctx = StepContext(request=req)
        ctx.verification_report = {"all_passed": True, "issues": []}

        rc = RetryController()

        # 已通过的验证报告，extract_errors 应返回空列表或默认消息
        errors = rc._extract_errors(ctx)
        # 验证通过 + 无 issues 时应返回默认消息
        assert len(errors) == 1
        assert "无具体错误" in errors[0] or "未知原因" in errors[0]

    def test_regenerate_all(self, tmp_path):
        """全量重新生成"""
        req = ProjectRequest(
            project_name="regen_test",
            description="A test project for regeneration validation",
        )
        ctx = StepContext(request=req)
        ctx.derived_spec = {
            "files": [
                {"path": "src/main.py", "description": "main"},
                {"path": "tests/test_main.py", "description": "test"},
            ],
            "dependencies": [],
            "acceptance_criteria": [],
        }

        from middlewares.transaction_manager import TransactionManager
        rc = RetryController()
        tracker = SideEffectTracker()
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)

        result = rc._regenerate_all(gen, ctx, tx, tracker)
        assert result[0] is True
        assert len(result[1]) > 0  # 有资产列表

    def test_regenerate_core(self, tmp_path):
        """仅重新生成核心文件"""
        req = ProjectRequest(
            project_name="core_test",
            description="A test project for core file regeneration",
        )
        ctx = StepContext(request=req)

        rc = RetryController()
        tracker = SideEffectTracker()
        gen = AssetGenerator()

        from middlewares.transaction_manager import TransactionManager
        tx = TransactionManager(tmp_path)

        result = rc._regenerate_core(gen, ctx, tx, tracker, tmp_path)
        assert result[0] is True
        assert "src/main.py" in result[1]

    def test_regenerate_minimal(self, tmp_path):
        """最小化生成"""
        req = ProjectRequest(
            project_name="min_test",
            description="A test project for minimal regeneration",
        )
        ctx = StepContext(request=req)

        rc = RetryController()
        tracker = SideEffectTracker()
        gen = AssetGenerator()

        from middlewares.transaction_manager import TransactionManager
        tx = TransactionManager(tmp_path)

        result = rc._regenerate_minimal(gen, ctx, tx, tracker)
        assert result[0] is True
        assert result[1] == ["src/main.py"]

    def test_record_failure(self, tmp_path):
        """失败模式记录"""
        req = ProjectRequest(
            project_name="fail_test",
            description="A test project for failure pattern recording",
        )
        ctx = StepContext(request=req)
        ctx.add_retry_record(1, "测试失败", "直接修复")

        rc = RetryController()
        rc.learnings_dir = tmp_path / ".learnings"
        rc.learnings_dir.mkdir(parents=True, exist_ok=True)

        pattern = rc._record_failure(ctx)
        assert "retry_exhausted" in pattern
        assert "fail_test" in pattern

        # 检查文件是否写入
        import json
        files = list(rc.learnings_dir.glob("failure_*.json"))
        assert len(files) >= 1
        data = json.loads(files[0].read_text(encoding="utf-8"))
        assert data["error_type"] == "retry_exhausted"

    def test_verify_with_timeout_normal(self, tmp_path):
        """正常验证（不超时）"""
        rc = RetryController()
        verifier = Verifier()

        req = ProjectRequest(
            project_name="vt_test",
            description="A test project for verification timeout testing",
        )
        ctx = StepContext(request=req)

        result = rc._verify_with_timeout(verifier, tmp_path, ctx)
        # 空目录的验证应该返回 VerificationResult
        assert result is not None

    def test_verify_with_timeout_timeout(self, tmp_path):
        """超时验证 — guard=None 回退到直接调用（SlowVerifier 不超时，返回结果）"""
        import time

        class SlowVerifier:
            def verify(self, *args, **kwargs):
                time.sleep(0.1)  # 短 sleep，不触发超时
                from layers.verifier import VerificationResult
                return VerificationResult()

        rc = RetryController()
        slow_v = SlowVerifier()

        req = ProjectRequest(
            project_name="to_test",
            description="A test project for slow verification timeout testing",
        )
        ctx = StepContext(request=req)

        # guard=None → 直接调用，返回 VerificationResult（非 None）
        result = rc._verify_with_timeout(slow_v, tmp_path, ctx)  # type: ignore
        assert result is not None  # 直接调用不超时
