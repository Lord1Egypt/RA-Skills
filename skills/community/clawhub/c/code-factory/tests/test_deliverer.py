"""
交付器单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.deliverer import Deliverer
from contracts.input_schema import ProjectRequest
from contracts.step_context import StepContext


class TestDeliverer:
    """Deliverer 交付器测试"""

    def test_deliver_basic(self, tmp_path):
        """基本交付输出"""
        req = ProjectRequest(
            project_name="test_project",
            description="A test project for delivery validation",
        )
        ctx = StepContext(request=req)

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )

        assert "project_path" in result
        assert "readme_preview" in result
        assert "manifest_summary" in result
        assert "manifest_json_summary" in result
        assert "test_summary" in result
        assert str(tmp_path.absolute()) in result["project_path"]

    def test_deliver_with_verification_report(self, tmp_path):
        """有验证报告时的交付"""
        req = ProjectRequest(
            project_name="test_project",
            description="A test project for delivery with verification",
        )
        ctx = StepContext(request=req)
        ctx.verification_report = {
            "all_passed": True,
            "issues": [],
        }

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "全部通过" in result["test_summary"]

    def test_deliver_with_failed_verification(self, tmp_path):
        """验证失败时的交付"""
        req = ProjectRequest(
            project_name="test_project",
            description="A test project for delivery with failed verification",
        )
        ctx = StepContext(request=req)
        ctx.verification_report = {
            "all_passed": False,
            "issues": ["循环引用: a.py ↔ b.py"],
        }

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "存在失败" in result["test_summary"]
        assert "循环引用" in result["test_summary"]

    def test_deliver_no_verification(self, tmp_path):
        """未执行验证时的交付"""
        req = ProjectRequest(
            project_name="test_project",
            description="A test project for delivery without verification",
        )
        ctx = StepContext(request=req)

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "未执行验证" in result["test_summary"]

    def test_readme_preview_missing(self, tmp_path):
        """README 不存在时的预览"""
        req = ProjectRequest(
            project_name="test_project",
            description="A test project for readme preview testing",
        )
        ctx = StepContext(request=req)

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "未找到" in result["readme_preview"]

    def test_readme_preview_truncated(self, tmp_path):
        """README 内容超过 500 字符时截断"""
        docs = tmp_path / "docs"
        docs.mkdir(parents=True)
        long_content = "# Title\n\n" + "Lorem ipsum dolor sit amet. " * 100
        (docs / "README.md").write_text(long_content, encoding="utf-8")

        req = ProjectRequest(
            project_name="test_project",
            description="A test project for truncated readme preview",
        )
        ctx = StepContext(request=req)

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "截断" in result["readme_preview"]
        assert len(result["readme_preview"]) <= 510  # 500 + 截断标记

    def test_manifest_summary(self, tmp_path):
        """ASSET_MANIFEST.md 摘要"""
        manifest_content = """# 资源地图

## 资源清单

| 文件 | 用途 | 生成方式 |
|------|------|---------|
| `src/main.py` | 主程序 | auto_generated |
| `tests/test_main.py` | 测试 | auto_generated |
"""
        (tmp_path / "ASSET_MANIFEST.md").write_text(manifest_content, encoding="utf-8")

        req = ProjectRequest(
            project_name="test_project",
            description="A test project for manifest summary testing",
        )
        ctx = StepContext(request=req)

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "src/main.py" in result["manifest_summary"]

    def test_manifest_json_summary(self, tmp_path):
        """manifest.json 摘要"""
        import json
        manifest_data = {
            "project_name": "test_project",
            "generated_at": "2026-01-01T00:00:00",
            "assets": [
                {"path": "src/main.py", "purpose": "main"},
                {"path": "tests/test_main.py", "purpose": "test"},
            ],
        }
        (tmp_path / "manifest.json").write_text(
            json.dumps(manifest_data, ensure_ascii=False), encoding="utf-8"
        )

        req = ProjectRequest(
            project_name="test_project",
            description="A test project for JSON manifest summary testing",
        )
        ctx = StepContext(request=req)

        deliverer = Deliverer()
        result = deliverer.deliver(
            project_path=tmp_path,
            project_name="test_project",
            context=ctx,
        )
        assert "test_project" in result["manifest_json_summary"]
