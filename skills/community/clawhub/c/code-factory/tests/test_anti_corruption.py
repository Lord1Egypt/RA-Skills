"""
防腐层完整测试 —— 含新增的 Step3 和 Step5 校验器
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from middlewares.anti_corruption import (
    AntiCorruptionLayer,
    ContractViolationError,
    ValidationResult,
)


class TestAntiCorruptionLayer:
    """防腐层完整测试"""

    # ── 已有校验器 ────────────────────────────────

    def test_validate_preflight_output_valid(self):
        """Phase 0 输出校验：有效输入"""
        result = AntiCorruptionLayer.validate_preflight_output({
            "python_ok": True,
            "dir_writable": True,
            "disk_sufficient": True,
            "issues": [],
        })
        assert result.is_valid

    def test_validate_preflight_output_invalid(self):
        """Phase 0 输出校验：缺失字段"""
        result = AntiCorruptionLayer.validate_preflight_output({})
        assert not result.is_valid
        assert len(result.errors) >= 3  # 三个必填 bool 字段

    def test_validate_environment_snapshot_valid(self):
        """Step 1 输出校验：有效输入"""
        result = AntiCorruptionLayer.validate_environment_snapshot({
            "python_version": "3.10",
            "installed_packages": [{"name": "pytest", "version": "7.0"}],
        })
        assert result.is_valid

    def test_validate_spec_output_valid(self):
        """Step 2 输出校验：有效输入"""
        result = AntiCorruptionLayer.validate_spec_output({
            "files": [{"path": "src/main.py", "description": "main"}],
            "dependencies": ["pytest>=7.0"],
            "acceptance_criteria": [{"given": "x", "when": "y", "then": "z"}],
        })
        assert result.is_valid

    def test_validate_spec_output_missing_path(self):
        """Step 2 输出校验：文件缺少 path"""
        result = AntiCorruptionLayer.validate_spec_output({
            "files": [{"description": "no path"}],
            "dependencies": [],
            "acceptance_criteria": [],
        })
        assert not result.is_valid
        assert any("path" in str(e) for e in result.errors)

    def test_validate_verification_output_valid(self):
        """Step 4 输出校验：有效输入"""
        result = AntiCorruptionLayer.validate_verification_output({
            "all_passed": True,
            "test_results": {"passed": True},
            "issues": [],
        })
        assert result.is_valid

    # ── 新增校验器：Step 3 → Step 4 ───────────────

    def test_validate_asset_output_valid(self):
        """Step 3 输出校验：有效输入"""
        result = AntiCorruptionLayer.validate_asset_output({
            "generated_files": ["src/main.py", "tests/test_main.py"],
        })
        assert result.is_valid

    def test_validate_asset_output_missing(self):
        """Step 3 输出校验：缺失字段"""
        result = AntiCorruptionLayer.validate_asset_output({})
        assert not result.is_valid
        assert any("generated_files" in str(e) for e in result.errors)

    def test_validate_asset_output_empty(self):
        """Step 3 输出校验：空列表"""
        result = AntiCorruptionLayer.validate_asset_output({
            "generated_files": [],
        })
        assert not result.is_valid
        assert any("空列表" in str(e) for e in result.errors)

    def test_validate_asset_output_path_traversal(self):
        """Step 3 输出校验：路径穿越检测"""
        result = AntiCorruptionLayer.validate_asset_output({
            "generated_files": ["../etc/passwd"],
        })
        assert not result.is_valid
        assert any(".." in str(e) for e in result.errors)

    def test_validate_asset_output_absolute_path(self):
        """Step 3 输出校验：绝对路径检测"""
        result = AntiCorruptionLayer.validate_asset_output({
            "generated_files": ["/etc/hosts"],
        })
        assert not result.is_valid

    def test_validate_asset_output_wrong_type(self):
        """Step 3 输出校验：类型错误"""
        result = AntiCorruptionLayer.validate_asset_output({
            "generated_files": "not a list",
        })
        assert not result.is_valid

    # ── 新增校验器：Step 5 → Step 6 ───────────────

    def test_validate_retry_output_valid(self):
        """Step 5 输出校验：有效输入"""
        result = AntiCorruptionLayer.validate_retry_output({
            "retried": True,
            "attempts": 2,
            "success": True,
        })
        assert result.is_valid

    def test_validate_retry_output_missing_fields(self):
        """Step 5 输出校验：缺失字段"""
        result = AntiCorruptionLayer.validate_retry_output({})
        assert not result.is_valid
        assert len(result.errors) >= 2  # retried + attempts

    def test_validate_retry_output_wrong_types(self):
        """Step 5 输出校验：类型错误"""
        result = AntiCorruptionLayer.validate_retry_output({
            "retried": "yes",  # 应该是 bool
            "attempts": "three",  # 应该是 int
        })
        assert not result.is_valid
        assert len(result.errors) == 2

    # ── 通用入口 ──────────────────────────────────

    def test_validate_step_transition_all_registered(self):
        """所有步骤转换都有对应的校验器"""
        registered = {"Phase0", "Step1", "Step2", "Step3", "Step4", "Step5"}
        for step in registered:
            # 不应抛出 ValueError
            result = AntiCorruptionLayer.validate_step_transition(step, {"generated_files": ["test.py"]} if step == "Step3" else {"python_ok": True, "dir_writable": True, "disk_sufficient": True, "issues": []} if step == "Phase0" else {"python_version": "3.10", "installed_packages": []} if step == "Step1" else {"files": [{"path": "t.py", "description": "d"}], "dependencies": [], "acceptance_criteria": []} if step == "Step2" else {"all_passed": True, "test_results": {}, "issues": []} if step == "Step4" else {"retried": False, "attempts": 0})
            assert isinstance(result, ValidationResult)

    def test_validate_step_transition_unknown(self):
        """未知步骤名抛出 ValueError"""
        with pytest.raises(ValueError, match="未知步骤"):
            AntiCorruptionLayer.validate_step_transition("Step99", {})
