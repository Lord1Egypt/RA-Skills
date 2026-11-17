#!/usr/bin/env python3
"""Tests for analyze_requirements.py"""

import json
import sys
import os
import tempfile

# Add scripts dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from analyze_requirements import analyze_text, analyze_docx, match_scene, extract_scoring_items


# ---------------------------------------------------------------------------
# Sample inputs for testing
# ---------------------------------------------------------------------------

SAMPLE_SAFETY_SERVICE_TEXT = """
QG2025年年度安全服务项目 招标文件 技术需求

一、项目概述
本项目为QG集团2025年度安全服务采购，服务内容包括：
1. 渗透测试服务：每季度对核心业务系统进行渗透测试
2. 重保服务：重大活动期间提供7×24小时现场保障
3. 应急响应服务：安全事件发生后2小时内到达现场处置
4. 安全运营服务：提供日常安全监控和日志分析

二、评分标准
| 评分项 | 分值 |
|--------|------|
| 项目理解 | 5分 |
| 需求分析 | 10分 |
| 服务方案 | 25分 |
| 实施计划 | 10分 |
| 服务承诺 | 5分 |
"""

SAMPLE_PRODUCT_TEXT = """
XX银行数据安全建设项目 技术规格书

一、建设内容
本项目需采购以下安全产品：
1. 数据分类分级系统 1套
2. 数据脱敏系统 1套
3. DLP数据防泄漏系统 1套
4. 数据库审计系统 1套

二、评分标准
| 评分项 | 分值 |
|--------|------|
| 总体设计方案 | 15分 |
| 技术方案 | 25分 |
| 实施方案 | 10分 |
| 培训方案 | 5分 |
| 售后服务 | 5分 |
"""

SAMPLE_DBJ_TEXT = """
XX医院等保测评项目

一、项目内容
对医院信息系统开展等级保护三级测评工作，包括：
1. 定级备案
2. 差距评估
3. 整改建议
4. 测评报告

二、评分标准
| 评分项 | 分值 |
|--------|------|
| 项目理解 | 5分 |
| 需求分析 | 10分 |
| 整改方案 | 20分 |
| 实施计划 | 10分 |
"""


# ---------------------------------------------------------------------------
# Test: extract_scoring_items
# ---------------------------------------------------------------------------

def test_extract_scoring_items():
    items = extract_scoring_items(SAMPLE_SAFETY_SERVICE_TEXT)
    assert len(items) >= 3, f"Expected at least 3 scoring items, got {len(items)}"
    names = [item['name'] for item in items]
    assert '服务方案' in names, f"Expected '服务方案' in scoring items, got {names}"


def test_extract_scoring_items_product():
    items = extract_scoring_items(SAMPLE_PRODUCT_TEXT)
    assert len(items) >= 3
    names = [item['name'] for item in items]
    assert '总体设计方案' in names or '技术方案' in names


# ---------------------------------------------------------------------------
# Test: match_scene
# ---------------------------------------------------------------------------

def test_match_scene_safety_service():
    result = match_scene(SAMPLE_SAFETY_SERVICE_TEXT)
    assert result is not None, "match_scene returned None"
    assert result['scene'] == '安全服务类', f"Expected 安全服务类, got {result['scene']}"
    assert result['score'] >= 2, f"Expected score >= 2, got {result['score']}"


def test_match_scene_product():
    result = match_scene(SAMPLE_PRODUCT_TEXT)
    assert result is not None
    assert result['scene'] == '产品交付类', f"Expected 产品交付类, got {result['scene']}"


def test_match_scene_dengbao():
    result = match_scene(SAMPLE_DBJ_TEXT)
    assert result is not None
    assert result['scene'] == '等保测评类', f"Expected 等保测评类, got {result['scene']}"


def test_match_scene_fallback():
    """Text with no clear keywords should fallback to default scene."""
    result = match_scene("这是一个普通的信息化项目，需要做一些常规工作")
    assert result is not None
    # Should fall back to default (综合类) or have low score
    assert result['scene'] == '综合类' or result['score'] < 2


# ---------------------------------------------------------------------------
# Test: analyze_text
# ---------------------------------------------------------------------------

def test_analyze_text_full():
    result = analyze_text(SAMPLE_SAFETY_SERVICE_TEXT)
    assert isinstance(result, dict)
    assert 'project_type' in result
    assert 'project_name' in result
    assert 'scoring_items' in result
    assert 'tech_domains' in result
    assert 'key_requirements' in result
    assert isinstance(result['scoring_items'], list)


def test_analyze_text_empty():
    result = analyze_text("")
    assert isinstance(result, dict)
    assert 'project_type' in result
    assert result['scoring_items'] == []


# ---------------------------------------------------------------------------
# Test: analyze_docx
# ---------------------------------------------------------------------------

def test_analyze_docx_from_path():
    """Create a simple .docx and test analysis."""
    try:
        from docx import Document
    except ImportError:
        print("SKIP: python-docx not installed")
        return

    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
        doc = Document()
        doc.add_paragraph(SAMPLE_SAFETY_SERVICE_TEXT)
        doc.save(f.name)
        tmp_path = f.name

    try:
        result = analyze_docx(tmp_path)
        assert isinstance(result, dict)
        assert 'project_type' in result
        assert 'tech_domains' in result
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Test: JSON output format
# ---------------------------------------------------------------------------

def test_output_format():
    result = analyze_text(SAMPLE_SAFETY_SERVICE_TEXT)
    # Verify required top-level keys
    required_keys = ['project_type', 'project_name', 'scoring_items', 'tech_domains', 'key_requirements']
    for key in required_keys:
        assert key in result, f"Missing key: {key}"

    # Verify scoring_items structure
    for item in result['scoring_items']:
        assert 'name' in item, f"Scoring item missing 'name': {item}"
        assert 'max_score' in item, f"Scoring item missing 'max_score': {item}"


if __name__ == '__main__':
    import pytest
    sys.exit(pytest.main([__file__, '-v']))
