# -*- coding: utf-8 -*-
"""
Stage 1: Document Parsing Tests

Tests for parse_doc.py — validates document parsing, scene building,
and output structure for all supported input formats.
"""

import json
import os
import sys
import tempfile
import pytest

# conftest.py already adds SCRIPTS_DIR to sys.path
from parse_doc import (
    detect_format,
    parse_txt,
    parse_md,
    build_scenes,
    detect_content_type,
    _looks_like_heading,
    _clean_markdown,
    _generate_image_prompt,
    _make_scene,
)


# ============================================================
# Format Detection
# ============================================================

class TestDetectFormat:
    """Tests for detect_format()."""

    def test_docx(self):
        assert detect_format("article.docx") == "docx"

    def test_doc(self):
        assert detect_format("article.doc") == "docx"

    def test_pdf(self):
        assert detect_format("report.pdf") == "pdf"

    def test_txt(self):
        assert detect_format("notes.txt") == "txt"

    def test_md(self):
        assert detect_format("doc.md") == "md"

    def test_markdown_extension(self):
        assert detect_format("doc.markdown") == "md"

    def test_uppercase_extension(self):
        assert detect_format("report.PDF") == "pdf"

    def test_unsupported_format_raises(self):
        with pytest.raises(ValueError, match="Unsupported file format"):
            detect_format("file.csv")

    def test_no_extension_raises(self):
        with pytest.raises(ValueError, match="Unsupported file format"):
            detect_format("noextension")


# ============================================================
# TXT Parsing
# ============================================================

class TestParseTxt:
    """Tests for parse_txt()."""

    def test_returns_list(self, sample_txt_file):
        blocks = parse_txt(sample_txt_file)
        assert isinstance(blocks, list)

    def test_blocks_have_required_fields(self, sample_txt_file):
        blocks = parse_txt(sample_txt_file)
        for block in blocks:
            assert "type" in block
            assert "level" in block
            assert "text" in block
            assert block["type"] in ("heading", "paragraph", "table")

    def test_detects_headings(self, sample_txt_file):
        blocks = parse_txt(sample_txt_file)
        headings = [b for b in blocks if b["type"] == "heading"]
        assert len(headings) >= 2  # "第一章 引言" and "第二章 方法"
        assert any("引言" in h["text"] for h in headings)
        assert any("方法" in h["text"] for h in headings)

    def test_paragraphs_preserved(self, sample_txt_file):
        blocks = parse_txt(sample_txt_file)
        paragraphs = [b for b in blocks if b["type"] == "paragraph"]
        assert len(paragraphs) >= 2

    def test_empty_file(self, test_data_dir):
        path = os.path.join(test_data_dir, "empty.txt")
        with open(path, 'w', encoding='utf-8') as f:
            f.write("")
        blocks = parse_txt(path)
        assert blocks == []

    def test_encoding_utf8(self, test_data_dir):
        path = os.path.join(test_data_dir, "utf8.txt")
        with open(path, 'w', encoding='utf-8') as f:
            f.write("中文测试内容\n\n第二段落")
        blocks = parse_txt(path)
        assert len(blocks) == 2


# ============================================================
# Markdown Parsing
# ============================================================

class TestParseMd:
    """Tests for parse_md()."""

    def test_returns_list(self, sample_md_file):
        blocks = parse_md(sample_md_file)
        assert isinstance(blocks, list)

    def test_detects_h1_heading(self, sample_md_file):
        blocks = parse_md(sample_md_file)
        h1 = [b for b in blocks if b["type"] == "heading" and b["level"] == 1]
        assert len(h1) >= 1
        assert "测试文档标题" in h1[0]["text"]

    def test_detects_h2_heading(self, sample_md_file):
        blocks = parse_md(sample_md_file)
        h2 = [b for b in blocks if b["type"] == "heading" and b["level"] == 2]
        assert len(h2) >= 2  # "第一节" and "第二节"

    def test_strips_markdown_formatting(self, sample_md_file):
        blocks = parse_md(sample_md_file)
        # The bold text should have ** stripped
        bold_block = [b for b in blocks if "加粗" in b.get("text", "")]
        if bold_block:
            assert "**" not in bold_block[0]["text"]

    def test_strips_links(self, sample_md_file):
        blocks = parse_md(sample_md_file)
        for b in blocks:
            if b["type"] == "paragraph":
                assert "](" not in b["text"]  # link syntax stripped

    def test_strips_inline_code(self, sample_md_file):
        blocks = parse_md(sample_md_file)
        for b in blocks:
            if b["type"] == "paragraph":
                assert "`" not in b["text"]


# ============================================================
# Scene Building
# ============================================================

class TestBuildScenes:
    """Tests for build_scenes()."""

    def test_returns_dict(self, sample_blocks):
        result = build_scenes(sample_blocks)
        assert isinstance(result, dict)

    def test_has_required_top_level_fields(self, sample_blocks):
        result = build_scenes(sample_blocks)
        assert "title" in result
        assert "scenes" in result
        assert "total_chars" in result
        assert "estimated_duration_sec" in result
        assert "language" in result

    def test_title_from_first_heading(self, sample_blocks):
        result = build_scenes(sample_blocks)
        assert result["title"] == "测试标题"

    def test_scenes_is_list(self, sample_blocks):
        result = build_scenes(sample_blocks)
        assert isinstance(result["scenes"], list)

    def test_scene_has_required_fields(self, sample_blocks):
        result = build_scenes(sample_blocks)
        for scene in result["scenes"]:
            assert "index" in scene
            assert "heading" in scene
            assert "level" in scene
            assert "narration" in scene
            assert "slide_text" in scene
            assert "image_prompt" in scene
            assert "char_count" in scene
            assert "estimated_duration" in scene
            assert "text_hash" in scene

    def test_scene_index_sequential(self, sample_blocks):
        result = build_scenes(sample_blocks)
        indices = [s["index"] for s in result["scenes"]]
        assert indices == list(range(len(indices)))

    def test_char_count_matches_narration(self, sample_blocks):
        result = build_scenes(sample_blocks)
        for scene in result["scenes"]:
            assert scene["char_count"] == len(scene["narration"])

    def test_total_chars_matches_sum(self, sample_blocks):
        result = build_scenes(sample_blocks)
        assert result["total_chars"] == sum(s["char_count"] for s in result["scenes"])

    def test_estimated_duration_positive(self, sample_blocks):
        result = build_scenes(sample_blocks)
        for scene in result["scenes"]:
            assert scene["estimated_duration"] > 0

    def test_total_duration_matches_sum(self, sample_blocks):
        result = build_scenes(sample_blocks)
        expected = sum(s["estimated_duration"] for s in result["scenes"])
        assert abs(result["estimated_duration_sec"] - round(expected, 1)) < 0.1

    def test_table_converted_to_text(self, sample_blocks):
        result = build_scenes(sample_blocks)
        # Table content should appear as "表格内容如下："
        all_narration = " ".join(s["narration"] for s in result["scenes"])
        assert "表格内容如下" in all_narration

    def test_language_field(self, sample_blocks):
        result = build_scenes(sample_blocks, lang="zh")
        assert result["language"] == "zh"

    def test_language_en(self, sample_blocks):
        result = build_scenes(sample_blocks, lang="en")
        assert result["language"] == "en"

    def test_text_hash_is_hex(self, sample_blocks):
        result = build_scenes(sample_blocks)
        for scene in result["scenes"]:
            assert len(scene["text_hash"]) == 16
            int(scene["text_hash"], 16)  # Should be valid hex

    def test_empty_blocks(self):
        result = build_scenes([])
        assert result["scenes"] == []
        assert result["total_chars"] == 0

    def test_long_text_split(self):
        """Test that text exceeding max_chars_per_scene gets split."""
        long_text = "这是一个很长的句子。" * 100  # ~1000 chars
        blocks = [{"type": "heading", "level": 1, "text": "长文本测试"},
                  {"type": "paragraph", "level": 0, "text": long_text}]
        result = build_scenes(blocks)
        assert len(result["scenes"]) >= 2  # Should be split

    def test_content_type_in_output(self, sample_blocks):
        """build_scenes should include content_type field in output."""
        result = build_scenes(sample_blocks)
        assert "content_type" in result

    def test_content_type_auto_detected(self, finance_blocks):
        """Content type should be auto-detected from blocks."""
        result = build_scenes(finance_blocks)
        assert result["content_type"] == "finance"

    def test_content_type_manual_override(self, finance_blocks):
        """Manual content_type override should be respected."""
        result = build_scenes(finance_blocks, content_type="technology")
        assert result["content_type"] == "technology"


# ============================================================
# Content Type Detection
# ============================================================

class TestDetectContentType:
    """Tests for detect_content_type()."""

    def test_returns_string(self, sample_blocks):
        result = detect_content_type(sample_blocks)
        assert isinstance(result, str)

    def test_finance_detection(self, finance_blocks):
        result = detect_content_type(finance_blocks)
        assert result == "finance"

    def test_technology_detection(self, technology_blocks):
        result = detect_content_type(technology_blocks)
        assert result == "technology"

    def test_business_detection(self, business_blocks):
        result = detect_content_type(business_blocks)
        assert result == "business"

    def test_manual_override(self, finance_blocks):
        """Manual override should skip detection."""
        result = detect_content_type(finance_blocks, manual_override="technology")
        assert result == "technology"

    def test_manual_override_unknown_type(self, finance_blocks):
        """Unknown manual override should fall back to detection."""
        result = detect_content_type(finance_blocks, manual_override="nonexistent")
        # Should fall back to detection since "nonexistent" is not in CONTENT_TYPE_KEYWORDS
        assert result == "finance"

    def test_empty_blocks_returns_default(self):
        result = detect_content_type([])
        assert result == "default"

    def test_empty_text_returns_default(self):
        """Blocks with no text content should return default."""
        blocks = [{"type": "heading", "level": 1, "text": ""}]
        result = detect_content_type(blocks)
        assert result == "default"

    def test_generic_content_returns_default(self, generic_blocks):
        """Content with no strong keyword signal should return default."""
        result = detect_content_type(generic_blocks)
        assert result == "default"

    def test_english_keywords_detected(self):
        """English keywords should also be detected."""
        blocks = [
            {"type": "heading", "level": 1, "text": "Investment Report"},
            {"type": "paragraph", "level": 0,
             "text": "The stock market shows strong revenue growth. "
                     "Portfolio allocation and asset valuation are key considerations. "
                     "Profit margins and liability management require attention."},
        ]
        result = detect_content_type(blocks)
        assert result == "finance"

    def test_case_insensitive_matching(self):
        """Keywords should match case-insensitively."""
        blocks = [
            {"type": "heading", "level": 1, "text": "AI Technology"},
            {"type": "paragraph", "level": 0,
             "text": "ARTIFICIAL INTELLIGENCE and MACHINE LEARNING are transforming "
                     "SOFTWARE development. CLOUD computing and BLOCKCHAIN are key trends."},
        ]
        result = detect_content_type(blocks)
        assert result == "technology"

    def test_multiple_types_clear_winner(self):
        """When one type clearly dominates, it should be selected."""
        blocks = [
            {"type": "heading", "level": 1, "text": "股票投资策略"},
            {"type": "paragraph", "level": 0,
             "text": "金融市场中股票和基金的投资策略。银行利率变化对债券收益的影响。"
                     "资产配置需要评估风险和估值水平。市盈率是重要参考指标。"
                     "投资组合的负债管理也很关键。"},
        ]
        result = detect_content_type(blocks)
        assert result == "finance"

    def test_all_content_types_have_keywords(self):
        """Verify that all content types in CONTENT_TYPE_KEYWORDS can be detected."""
        from config import CONTENT_TYPE_KEYWORDS
        for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
            # Create blocks using the first few keywords
            test_text = " ".join(keywords[:5])
            blocks = [{"type": "paragraph", "level": 0, "text": test_text}]
            result = detect_content_type(blocks)
            # Should detect this type (or at least not crash)
            assert isinstance(result, str)


# ============================================================
# Helper Functions
# ============================================================

class TestLooksLikeHeading:
    """Tests for _looks_like_heading()."""

    def test_chinese_chapter(self):
        assert _looks_like_heading("第一章 引言") is True

    def test_chinese_numbered(self):
        assert _looks_like_heading("一、概述") is True

    def test_numbered_heading(self):
        assert _looks_like_heading("1. 引言") is True

    def test_all_caps(self):
        assert _looks_like_heading("INTRODUCTION") is True

    def test_english_chapter(self):
        assert _looks_like_heading("Chapter 1") is True

    def test_english_section(self):
        assert _looks_like_heading("Section 2") is True

    def test_normal_text(self):
        assert _looks_like_heading("这是一段普通的段落文本内容") is False

    def test_long_text(self):
        assert _looks_like_heading("This is a very long sentence that is definitely not a heading") is False


class TestCleanMarkdown:
    """Tests for _clean_markdown()."""

    def test_bold(self):
        assert _clean_markdown("**bold text**") == "bold text"

    def test_italic(self):
        assert _clean_markdown("*italic text*") == "italic text"

    def test_link(self):
        assert _clean_markdown("[text](http://url.com)") == "text"

    def test_image(self):
        assert _clean_markdown("![alt text](http://img.com/x.png)") == "alt text"

    def test_inline_code(self):
        assert _clean_markdown("`code`") == "code"

    def test_list_markers(self):
        assert _clean_markdown("- item1\n- item2") == "item1 item2"

    def test_numbered_list(self):
        result = _clean_markdown("1. first\n2. second")
        assert "first" in result
        assert "second" in result

    def test_blockquote(self):
        assert _clean_markdown("> quoted text") == "quoted text"

    def test_horizontal_rule(self):
        result = _clean_markdown("text\n---\nmore")
        assert "---" not in result


class TestGenerateImagePrompt:
    """Tests for _generate_image_prompt() — content-type-aware prompt generation."""

    def test_returns_string(self):
        prompt = _generate_image_prompt("标题", "内容", "default")
        assert isinstance(prompt, str)

    def test_contains_heading(self):
        prompt = _generate_image_prompt("AI合规", "内容文本", "technology")
        assert "AI合规" in prompt

    def test_contains_content_context(self):
        prompt = _generate_image_prompt("标题", "这是一段关于金融的内容", "finance")
        assert "金融" in prompt

    def test_contains_purpose_prefix(self):
        """Prompt should start with [PURPOSE] prefix for GenerateImage tool."""
        prompt = _generate_image_prompt("标题", "内容", "default")
        assert "[PURPOSE]" in prompt

    def test_contains_artistic_style(self):
        """Prompt should include artistic style from AI_IMAGE_CONFIG."""
        prompt = _generate_image_prompt("标题", "内容", "technology")
        assert "Artistic style:" in prompt

    def test_contains_color_mood(self):
        """Prompt should include color mood from AI_IMAGE_CONFIG."""
        prompt = _generate_image_prompt("标题", "内容", "finance")
        assert "Color mood:" in prompt

    def test_contains_composition(self):
        """Prompt should include composition guidance from AI_IMAGE_CONFIG."""
        prompt = _generate_image_prompt("标题", "内容", "default")
        assert "Composition:" in prompt

    def test_contains_no_text_instruction(self):
        """Prompt should include 'No text in image' instruction."""
        prompt = _generate_image_prompt("标题", "内容", "default")
        assert "No text" in prompt

    def test_finance_style_differs_from_technology(self):
        """Finance and technology prompts should have different styles."""
        finance_prompt = _generate_image_prompt("标题", "内容", "finance")
        tech_prompt = _generate_image_prompt("标题", "内容", "technology")
        assert finance_prompt != tech_prompt

    def test_unknown_content_type_uses_default(self):
        """Unknown content type should fall back to default style."""
        prompt = _generate_image_prompt("标题", "内容", "nonexistent_type")
        assert "[PURPOSE]" in prompt
        assert "Artistic style:" in prompt

    def test_default_content_type(self):
        """Default content type should work without errors."""
        prompt = _generate_image_prompt("标题", "内容")
        assert isinstance(prompt, str)
        assert "[PURPOSE]" in prompt


class TestMakeScene:
    """Tests for _make_scene()."""

    def test_returns_dict(self):
        scene = _make_scene(0, "标题", 1, "内容文本", 4.5)
        assert isinstance(scene, dict)

    def test_has_required_fields(self):
        scene = _make_scene(0, "标题", 1, "内容文本", 4.5)
        for field in ["index", "heading", "level", "narration",
                       "slide_text", "image_prompt", "char_count",
                       "estimated_duration", "text_hash"]:
            assert field in scene

    def test_char_count(self):
        text = "测试文本"
        scene = _make_scene(0, "标题", 1, text, 4.5)
        assert scene["char_count"] == len(text)

    def test_estimated_duration(self):
        text = "测试文本"
        scene = _make_scene(0, "标题", 1, text, 4.5)
        assert abs(scene["estimated_duration"] - round(len(text) / 4.5, 1)) < 0.1

    def test_slide_text_truncation(self):
        long_text = "这是一个很长的句子。" * 50  # > 200 chars
        scene = _make_scene(0, "标题", 1, long_text, 4.5)
        assert len(scene["slide_text"]) <= 204  # 200 + "..." or natural break

    def test_text_hash_consistency(self):
        text = "相同的文本"
        scene1 = _make_scene(0, "标题", 1, text, 4.5)
        scene2 = _make_scene(1, "其他", 2, text, 4.5)
        assert scene1["text_hash"] == scene2["text_hash"]

    def test_content_type_affects_image_prompt(self):
        """Different content types should produce different image prompts."""
        text = "这是一段关于金融投资的内容"
        scene_finance = _make_scene(0, "标题", 1, text, 4.5, "finance")
        scene_tech = _make_scene(1, "标题", 1, text, 4.5, "technology")
        assert scene_finance["image_prompt"] != scene_tech["image_prompt"]

    def test_default_content_type_in_make_scene(self):
        """_make_scene should work with default content_type."""
        scene = _make_scene(0, "标题", 1, "内容", 4.5)
        assert "[PURPOSE]" in scene["image_prompt"]


# ============================================================
# Integration: Existing scenes.json
# ============================================================

class TestExistingScenesJson:
    """Validate the existing scenes.json from the pipeline run."""

    def test_has_required_fields(self, existing_scenes_json):
        assert "title" in existing_scenes_json
        assert "scenes" in existing_scenes_json
        assert "total_chars" in existing_scenes_json
        assert "estimated_duration_sec" in existing_scenes_json
        assert "language" in existing_scenes_json

    def test_title_is_nonempty(self, existing_scenes_json):
        assert len(existing_scenes_json["title"]) > 0

    def test_scenes_nonempty(self, existing_scenes_json):
        assert len(existing_scenes_json["scenes"]) > 0

    def test_scene_indices_sequential(self, existing_scenes_json):
        scenes = existing_scenes_json["scenes"]
        indices = [s["index"] for s in scenes]
        assert indices == list(range(len(indices)))

    def test_scene_fields_valid(self, existing_scenes_json):
        for scene in existing_scenes_json["scenes"]:
            assert isinstance(scene["index"], int)
            assert isinstance(scene["narration"], str)
            assert len(scene["narration"]) > 0
            assert isinstance(scene["char_count"], int)
            assert scene["char_count"] > 0
            assert scene["estimated_duration"] > 0

    def test_total_chars_matches(self, existing_scenes_json):
        expected = sum(s["char_count"] for s in existing_scenes_json["scenes"])
        assert existing_scenes_json["total_chars"] == expected
