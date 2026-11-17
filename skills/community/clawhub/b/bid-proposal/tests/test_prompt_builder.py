#!/usr/bin/env python3
"""Tests for prompt_builder.py"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from prompt_builder import (
    build_chapter_prompt,
    build_all_prompts,
    load_chapter_template,
    find_material_references
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_ANALYSIS = {
    "project_type": "安全服务类",
    "project_name": "QG2025年年度安全服务项目",
    "scoring_items": [
        {"name": "项目理解", "max_score": 5},
        {"name": "需求分析", "max_score": 10},
        {"name": "服务方案", "max_score": 25},
        {"name": "实施计划", "max_score": 10},
        {"name": "服务承诺", "max_score": 5}
    ],
    "tech_domains": ["安全服务", "安全运营"],
    "key_requirements": ["渗透测试", "重保", "应急响应", "安全运营", "MSS"],
    "special_notes": ""
}

SAMPLE_CHAPTER = {
    "id": "service_solution",
    "name": "服务方案",
    "prompt_guide": "详细阐述每项服务的内容、方法、工具、流程和交付物。"
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_build_chapter_prompt_basic():
    """Build a prompt for a single chapter with basic analysis."""
    prompt = build_chapter_prompt(SAMPLE_CHAPTER, SAMPLE_ANALYSIS)
    assert isinstance(prompt, str)
    assert len(prompt) > 50, "Prompt too short"
    # Should contain chapter name
    assert '服务方案' in prompt
    # Should contain project context
    assert 'QG2025' in prompt
    # Should contain scoring reference
    assert '25分' in prompt or '服务方案' in prompt
    # Should have structure hints
    assert any(marker in prompt for marker in ['写作要求', '生成', '编写', '内容', '#'])


def test_build_chapter_prompt_with_material():
    """Build a prompt with material library references."""
    # Create temporary material directory
    with tempfile.TemporaryDirectory() as tmpdir:
        material_file = os.path.join(tmpdir, '服务方案范例.md')
        with open(material_file, 'w', encoding='utf-8') as f:
            f.write("# 服务方案范例\n\n这是某项目服务方案的范例内容。")

        prompt = build_chapter_prompt(SAMPLE_CHAPTER, SAMPLE_ANALYSIS, material_lib_dir=tmpdir)
        assert isinstance(prompt, str)
        # Should contain material reference hint
        # (exact content depends on implementation, but should be longer due to material)
        assert len(prompt) > 100


def test_build_chapter_prompt_empty_analysis():
    """Build a prompt with minimal analysis data."""
    minimal = {
        "project_type": "综合类",
        "project_name": "测试项目",
        "scoring_items": [],
        "tech_domains": [],
        "key_requirements": [],
        "special_notes": ""
    }
    prompt = build_chapter_prompt(SAMPLE_CHAPTER, minimal)
    assert isinstance(prompt, str)
    assert len(prompt) > 30
    assert '测试项目' in prompt


def test_build_all_prompts():
    """Build prompts for all chapters in a chapter config."""
    chapters = [
        {"id": "background", "name": "项目背景与目标", "prompt_guide": "阐述项目背景"},
        {"id": "requirement", "name": "需求分析", "prompt_guide": "分析需求"},
        {"id": "service_solution", "name": "服务方案", "prompt_guide": "详细服务方案"},
    ]
    results = build_all_prompts(chapters, SAMPLE_ANALYSIS)
    assert len(results) == 3
    for ch_id, prompt in results.items():
        assert isinstance(prompt, str)
        assert len(prompt) > 30, f"Prompt for {ch_id} too short"


def test_find_material_references():
    """Find material library references for a chapter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a material file
        examples_dir = os.path.join(tmpdir, 'chapter-examples')
        os.makedirs(examples_dir)
        with open(os.path.join(examples_dir, '服务方案范例.md'), 'w') as f:
            f.write("# 范例\n\n这是服务方案的参考内容。")

        refs = find_material_references('服务方案', tmpdir)
        assert isinstance(refs, list)
        assert len(refs) >= 1, f"Should find at least 1 reference, got {len(refs)}"


def test_find_material_references_empty():
    """Find material references in non-existent directory."""
    refs = find_material_references('服务方案', '/nonexistent/path')
    assert isinstance(refs, list)
    assert len(refs) == 0, "Should get empty list for non-existent dir"


def test_prompt_includes_scoring_context():
    """Prompt should reference scoring items when available."""
    analysis_with_scoring = dict(SAMPLE_ANALYSIS)
    analysis_with_scoring['scoring_items'] = [
        {"name": "服务方案", "max_score": 25, "requirements": ["服务内容完整性", "技术专业性"]}
    ]
    prompt = build_chapter_prompt(SAMPLE_CHAPTER, analysis_with_scoring)
    assert '25' in prompt or '评分' in prompt
    assert '服务方案' in prompt


def test_prompt_structure():
    """Verify prompt has a usable structure."""
    prompt = build_chapter_prompt(SAMPLE_CHAPTER, SAMPLE_ANALYSIS)
    # Should not be empty
    assert prompt.strip()
    # Should have at least a title indicator
    lines = prompt.strip().split('\n')
    assert len(lines) >= 3, f"Prompt should have multiple lines, got {len(lines)}"


if __name__ == '__main__':
    import pytest
    sys.exit(pytest.main([__file__, '-v']))
