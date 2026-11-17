#!/usr/bin/env python3
"""Smoke test for cookie-manager Skill (keepalive)

自动生成 by generate_smoke_tests.py (BUG-DETECT-014)
验证: SKILL.md存在 + frontmatter正确 + 工作流步骤完整
"""
import re
from pathlib import Path

# 路径: d:\JueJin\skills\cookie-manager\scripts\tests\test_smoke_*.py
# parents[0]=tests/ [1]=scripts/ [2]=cookie-manager/ [3]=skills/ [4]=project_root
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SKILL_PATH = PROJECT_ROOT / "skills" / "cookie-manager" / "SKILL.md"


def test_skill_md_exists():
    """测试SKILL.md文件存在"""
    assert SKILL_PATH.exists(), f"SKILL.md不存在: {SKILL_PATH}"


def test_frontmatter_correct():
    """测试frontmatter格式正确"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")

    # 检查frontmatter存在
    assert content.startswith("---"), "SKILL.md应以---开头"

    # 提取frontmatter
    parts = content.split("---", 2)
    if len(parts) >= 3:
        frontmatter = parts[1]

        # 检查必需字段
        assert "name:" in frontmatter, "frontmatter缺少name字段"
        assert "description:" in frontmatter, "frontmatter缺少description字段"


def test_workflow_complete():
    """测试工作流步骤完整"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")

    # 检查有工作流部分(## 工作流 或 ## Workflow)
    has_workflow = bool(
        re.search(r"^##\s*(工作流|Workflow|工作流程)", content, re.MULTILINE)
    )
    assert has_workflow, "SKILL.md缺少工作流部分"


def test_error_handling():
    """测试异常处理部分"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")

    # 检查有异常处理部分(## 异常处理 或 ## Error Handling)
    has_error = bool(
        re.search(r"^##\s*(异常处理|Error Handling|异常)", content, re.MULTILINE)
    )
    assert has_error, "SKILL.md缺少异常处理部分"


if __name__ == "__main__":
    test_skill_md_exists()
    test_frontmatter_correct()
    test_workflow_complete()
    test_error_handling()
    print("All smoke tests passed for cookie-manager (keepalive)")
