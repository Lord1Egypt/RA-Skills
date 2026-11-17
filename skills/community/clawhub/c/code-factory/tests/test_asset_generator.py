"""
资产生成器单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.asset_generator import AssetGenerator
from middlewares.transaction_manager import TransactionManager
from middlewares.side_effect_log import SideEffectTracker


class TestAssetGenerator:
    """AssetGenerator 单元测试"""

    def test_generate_basic_cli(self, tmp_path):
        """基本 CLI 项目生成"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        spec = {
            "description": "A test CLI tool",
            "files": [
                {"path": "src/main.py", "description": "main", "is_entry": True, "is_hard_gate": True},
                {"path": "tests/test_main.py", "description": "test", "is_test": True},
            ],
            "dependencies": [],
            "acceptance_criteria": [],
        }

        assets = gen.generate(
            project_name="test_tool",
            spec=spec,
            tx=tx,
            tracker=tracker,
        )

        # 不 commit，检查 staging 中的文件列表
        assert len(assets) > 0
        assert "src/main.py" in assets
        assert "tests/test_main.py" in assets

    def test_generate_with_dependencies(self, tmp_path):
        """带依赖的项目生成"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        spec = {
            "description": "A test tool with deps",
            "files": [
                {"path": "src/main.py", "description": "main", "is_entry": True, "is_hard_gate": True},
                {"path": "tests/test_main.py", "description": "test", "is_test": True},
            ],
            "dependencies": ["requests>=2.28", "click>=8.0"],
            "acceptance_criteria": [],
        }

        assets = gen.generate(
            project_name="test_tool",
            spec=spec,
            tx=tx,
            tracker=tracker,
        )
        assert "requirements.txt" in assets

    def test_generate_spec_none_raises(self, tmp_path):
        """spec=None 应该抛出明确错误"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        with pytest.raises(ValueError, match="spec=None"):
            gen.generate(
                project_name="test_tool",
                spec=None,
                tx=tx,
                tracker=tracker,
            )

    def test_generate_empty_files_raises(self, tmp_path):
        """空文件列表应该被防腐层拦截（此处测试 AssetGenerator 行为）"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        spec = {
            "description": "A test tool",
            "files": [],
            "dependencies": [],
            "acceptance_criteria": [],
        }

        # 空文件列表不抛异常，只是生成的基础文件（README等）仍会创建
        assets = gen.generate(
            project_name="test_tool",
            spec=spec,
            tx=tx,
            tracker=tracker,
        )
        # 仍然会生成 manifest、README 等基础文件
        assert len(assets) > 0

    def test_generate_main_py_content(self):
        """main.py 模板包含 HARD-GATE 标记"""
        gen = AssetGenerator()
        content = gen._generate_main_py("test_tool", "A test tool")
        assert "HARD-GATE" in content
        assert "def main" in content
        assert "test_tool" in content

    def test_generate_test_py_content(self):
        """test_main.py 模板包含必要的导入"""
        gen = AssetGenerator()
        content = gen._generate_test_py("test_tool")
        assert "import pytest" in content
        assert "from src.main import main" in content
        assert "def test_main_returns_zero" in content

    def test_generate_app_py_for_web(self):
        """Web 应用 app.py 模板"""
        gen = AssetGenerator()
        content = gen._generate_app_py("web_app")
        assert "HARD-GATE" in content
        assert "Flask" in content
        assert "create_app" in content

    def test_generate_api_py_for_service(self):
        """API 服务 api.py 模板"""
        gen = AssetGenerator()
        content = gen._generate_api_py("api_service")
        assert "HARD-GATE" in content
        assert "FastAPI" in content

    def test_generate_unknown_file_type_raises(self):
        """未知文件类型抛出 ValueError"""
        gen = AssetGenerator()
        with pytest.raises(ValueError, match="未知文件类型"):
            gen._generate_file_content("src/unknown.xyz", "test", "desc", [])

    def test_side_effect_tracking(self, tmp_path):
        """验证副作用追踪记录了所有文件创建"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        spec = {
            "description": "A test tool",
            "files": [
                {"path": "src/main.py", "description": "main", "is_entry": True, "is_hard_gate": True},
            ],
            "dependencies": [],
            "acceptance_criteria": [],
        }

        gen.generate(
            project_name="test_tool",
            spec=spec,
            tx=tx,
            tracker=tracker,
        )

        # tracker 应该记录了所有文件创建
        created = tracker.get_created_files()
        assert len(created) > 0
        assert "src/main.py" in created

    def test_transaction_commit(self, tmp_path):
        """事务提交后文件应该存在于磁盘"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        spec = {
            "description": "A test tool",
            "files": [
                {"path": "src/main.py", "description": "main", "is_entry": True, "is_hard_gate": True},
                {"path": "tests/test_main.py", "description": "test", "is_test": True},
            ],
            "dependencies": [],
            "acceptance_criteria": [],
        }

        gen.generate(
            project_name="test_tool",
            spec=spec,
            tx=tx,
            tracker=tracker,
        )
        tx.commit()

        assert (tmp_path / "src" / "main.py").exists()
        assert (tmp_path / "tests" / "test_main.py").exists()

    def test_transaction_rollback(self, tmp_path):
        """事务回滚后文件不应该存在于磁盘"""
        gen = AssetGenerator()
        tx = TransactionManager(tmp_path)
        tracker = SideEffectTracker()

        spec = {
            "description": "A test tool",
            "files": [
                {"path": "src/main.py", "description": "main", "is_entry": True, "is_hard_gate": True},
            ],
            "dependencies": [],
            "acceptance_criteria": [],
        }

        gen.generate(
            project_name="test_tool",
            spec=spec,
            tx=tx,
            tracker=tracker,
        )
        tx.rollback()

        # 回滚后文件不应存在
        assert not (tmp_path / "src" / "main.py").exists()
