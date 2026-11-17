"""
预检层单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.preflight import PreflightRunner, PreflightResult


class TestPreflightRunner:
    """Phase 0 环境预检测试"""

    def test_preflight_all_ok(self, tmp_path):
        """正常环境应该通过预检"""
        runner = PreflightRunner()
        result = runner.run(target_dir=tmp_path / "test_project")
        assert result.python_ok
        assert result.dir_writable
        assert result.all_ok

    def test_preflight_python_too_old(self, tmp_path):
        """要求过高 Python 版本时应该失败"""
        runner = PreflightRunner()
        result = runner.run(
            target_dir=tmp_path / "test_project",
            required_python="99.99",
        )
        assert not result.python_ok
        assert not result.all_ok
        assert result.python_issue is not None

    def test_preflight_invalid_python_version(self, tmp_path):
        """无效的 Python 版本格式"""
        runner = PreflightRunner()
        result = runner.run(
            target_dir=tmp_path / "test_project",
            required_python="invalid",
        )
        assert not result.python_ok

    def test_to_dict(self, tmp_path):
        """PreflightResult.to_dict 格式"""
        runner = PreflightRunner()
        result = runner.run(target_dir=tmp_path / "test_project")
        d = result.to_dict()
        assert "all_ok" in d
        assert "python_version" in d
        assert isinstance(d["issues"], list)


class TestPreflightResult:
    """PreflightResult 数据类测试"""

    def test_all_ok_property(self):
        """all_ok 属性应该在所有检查通过时为 True"""
        result = PreflightResult(
            python_ok=True,
            dir_writable=True,
            disk_sufficient=True,
            deps_available=True,
        )
        assert result.all_ok

    def test_all_ok_property_false(self):
        """任一检查失败时 all_ok 应为 False"""
        result = PreflightResult(
            python_ok=False,
            dir_writable=True,
            disk_sufficient=True,
            deps_available=True,
        )
        assert not result.all_ok
