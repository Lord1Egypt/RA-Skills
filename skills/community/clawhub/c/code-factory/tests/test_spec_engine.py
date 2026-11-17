"""
Spec 引擎单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.spec_engine import SpecEngine, SpecResult, FileSpec
from contracts.input_schema import ProjectType, AcceptanceCriterion


class TestSpecEngine:
    """Spec 推导引擎测试"""

    def test_derive_basic_cli(self):
        """基本的 CLI 工具 Spec 推导"""
        engine = SpecEngine()
        result = engine.derive(
            description="A file backup tool",
            project_type=ProjectType.CLI_TOOL,
        )
        assert len(result.files) >= 9  # 标准 9 文件结构
        assert isinstance(result.to_dict()["files"], list)

    def test_derive_web_app_adds_extra_files(self):
        """Web 应用应该包含额外的 app.py"""
        engine = SpecEngine()
        result = engine.derive(
            description="A web dashboard",
            project_type=ProjectType.WEB_APP,
        )
        paths = [f.path for f in result.files]
        assert "src/app.py" in paths
        assert "flask>=3.0" in result.dependencies

    def test_derive_api_service(self):
        """API 服务推导"""
        engine = SpecEngine()
        result = engine.derive(
            description="A REST API service",
            project_type=ProjectType.API_SERVICE,
        )
        paths = [f.path for f in result.files]
        assert "src/api.py" in paths
        assert any("fastapi" in d for d in result.dependencies)
        assert any("uvicorn" in d for d in result.dependencies)

    def test_derive_with_acceptance_criteria(self):
        """带验收标准的推导"""
        engine = SpecEngine()
        result = engine.derive(
            description="A file backup tool",
            acceptance_criteria=[
                AcceptanceCriterion(
                    given="a file exists",
                    when="backup is triggered",
                    then="file is copied to backup dir",
                    priority=1,
                )
            ],
        )
        assert len(result.acceptance_criteria) == 1
        assert result.acceptance_criteria[0]["priority"] == 1

    def test_file_spec_has_entry_point(self):
        """至少有一个文件标记为入口点"""
        engine = SpecEngine()
        result = engine.derive(description="A test tool")
        entry_files = [f for f in result.files if f.is_entry]
        assert len(entry_files) >= 1
        assert entry_files[0].path == "src/main.py"

    def test_file_spec_has_hard_gate(self):
        """入口文件应该标记为 HARD-GATE"""
        engine = SpecEngine()
        result = engine.derive(description="A test tool")
        entry = [f for f in result.files if f.is_entry][0]
        assert entry.is_hard_gate
