#!/usr/bin/env python3
"""Smoke test for biometric-confirm Skill

验证: SKILL.md存在 + frontmatter正确 + 工作流步骤完整 + 异常处理
"""
import re
from pathlib import Path

# Walk up to find project root (contains skills/ directory)
_file_path = Path(__file__).resolve()
PROJECT_ROOT = _file_path
while PROJECT_ROOT != PROJECT_ROOT.parent:
    if (PROJECT_ROOT / "skills").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
SKILL_PATH = PROJECT_ROOT / "skills" / "biometric-confirm" / "SKILL.md"


def test_skill_md_exists():
    """测试SKILL.md文件存在"""
    assert SKILL_PATH.exists(), f"SKILL.md不存在: {SKILL_PATH}"


def test_frontmatter_correct():
    """测试frontmatter格式正确"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")

    assert content.startswith("---"), "SKILL.md应以---开头"

    parts = content.split("---", 2)
    if len(parts) >= 3:
        frontmatter = parts[1]

        assert "name:" in frontmatter, "frontmatter缺少name字段"
        assert "description:" in frontmatter, "frontmatter缺少description字段"


def test_workflow_complete():
    """测试工作流步骤完整"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")

    has_workflow = bool(
        re.search(r"^##\s*([一二三四五六七八九十\d]+[、.]\s*)?(工作流|Workflow|工作流程)", content, re.MULTILINE)
    )
    assert has_workflow, "SKILL.md缺少工作流部分"


def test_error_handling():
    """测试异常处理部分"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")

    has_error = bool(
        re.search(r"^##\s*([一二三四五六七八九十\d]+[、.]\s*)?(异常处理|Error Handling|异常)", content, re.MULTILINE)
    )
    assert has_error, "SKILL.md缺少异常处理部分"


def test_description_has_trigger():
    """测试description包含触发关键词"""
    if not SKILL_PATH.exists():
        import pytest
        pytest.skip("SKILL.md不存在")

    content = SKILL_PATH.read_text(encoding="utf-8", errors="ignore")
    parts = content.split("---", 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        assert "触发" in frontmatter or "trigger" in frontmatter.lower(), \
            "description应包含触发关键词"


if __name__ == "__main__":
    test_skill_md_exists()
    test_frontmatter_correct()
    test_workflow_complete()
    test_error_handling()
    test_description_has_trigger()
    print("All smoke tests passed for biometric-confirm")
