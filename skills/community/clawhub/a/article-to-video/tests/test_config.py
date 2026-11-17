# -*- coding: utf-8 -*-
"""
Configuration Validation Tests

Tests for config.py — validates the structure, consistency, and completeness
of all Phase 1 configuration sections: content types, voice profiles,
visual styles, BGM config, and Ken Burns speed map.
"""

import sys
import os
import pytest

# conftest.py already adds SCRIPTS_DIR to sys.path
from config import (
    TTS_CONFIG,
    VOICE_PROFILES,
    VIDEO_CONFIG,
    EFFECTS_CONFIG,
    BGM_CONFIG,
    SLIDE_CONFIG,
    CONTENT_TYPE_KEYWORDS,
    CONTENT_TYPE_STYLES,
    KEN_BURNS_SPEED_MAP,
    PARSE_CONFIG,
    PATHS_CONFIG,
    CACHE_CONFIG,
    CONCURRENCY_CONFIG,
    AI_IMAGE_CONFIG,
)


# ============================================================
# Content Type Keywords Configuration
# ============================================================

class TestContentTypeKeywords:
    """Tests for CONTENT_TYPE_KEYWORDS configuration."""

    def test_is_dict(self):
        assert isinstance(CONTENT_TYPE_KEYWORDS, dict)
        assert len(CONTENT_TYPE_KEYWORDS) >= 7

    def test_all_values_are_lists(self):
        for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
            assert isinstance(keywords, list), \
                f"Content type '{content_type}' keywords is not a list"
            assert len(keywords) > 0, \
                f"Content type '{content_type}' has no keywords"

    def test_has_expected_types(self):
        expected = {"finance", "business", "technology", "science",
                    "education", "news", "lifestyle"}
        assert expected.issubset(set(CONTENT_TYPE_KEYWORDS.keys())), \
            f"Missing expected content types. Got: {set(CONTENT_TYPE_KEYWORDS.keys())}"

    def test_keywords_are_strings(self):
        for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
            for kw in keywords:
                assert isinstance(kw, str), \
                    f"Keyword '{kw}' in '{content_type}' is not a string"
                assert len(kw) > 0, \
                    f"Empty keyword in '{content_type}'"

    def test_has_both_chinese_and_english(self):
        """Each content type should have both Chinese and English keywords."""
        for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
            has_chinese = any(any('\u4e00' <= c <= '\u9fff' for c in kw) for kw in keywords)
            has_english = any(kw.isascii() and kw.isalpha() for kw in keywords)
            assert has_chinese, f"Content type '{content_type}' has no Chinese keywords"
            assert has_english, f"Content type '{content_type}' has no English keywords"

    def test_no_duplicate_keywords_within_type(self):
        """No duplicate keywords within the same content type."""
        for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
            lower_keywords = [kw.lower() for kw in keywords]
            assert len(lower_keywords) == len(set(lower_keywords)), \
                f"Duplicate keywords in '{content_type}': {lower_keywords}"


# ============================================================
# Content Type Styles Configuration
# ============================================================

class TestContentTypeStyles:
    """Tests for CONTENT_TYPE_STYLES configuration."""

    def test_is_dict(self):
        assert isinstance(CONTENT_TYPE_STYLES, dict)
        assert len(CONTENT_TYPE_STYLES) >= 8  # 7 types + default

    def test_has_default_style(self):
        assert "default" in CONTENT_TYPE_STYLES

    def test_all_styles_have_required_fields(self):
        required = ["label", "theme", "font_title", "font_body",
                    "ken_burns_speed", "transition", "transition_duration",
                    "subtitle_position"]
        for content_type, style in CONTENT_TYPE_STYLES.items():
            for field in required:
                assert field in style, \
                    f"Content type '{content_type}' missing field '{field}'"

    def test_all_ken_burns_speeds_are_valid(self):
        valid_speeds = set(KEN_BURNS_SPEED_MAP.keys())
        for content_type, style in CONTENT_TYPE_STYLES.items():
            assert style["ken_burns_speed"] in valid_speeds, \
                f"Content type '{content_type}' has invalid ken_burns_speed: '{style['ken_burns_speed']}'"

    def test_all_themes_are_valid(self):
        valid_themes = set(SLIDE_CONFIG["themes"].keys())
        for content_type, style in CONTENT_TYPE_STYLES.items():
            assert style["theme"] in valid_themes, \
                f"Content type '{content_type}' has invalid theme: '{style['theme']}'"

    def test_all_transitions_are_valid(self):
        valid_transitions = {"fade", "dissolve", "slideleft", "slideright",
                            "wipeup", "wipedown", "circleopen", "none"}
        for content_type, style in CONTENT_TYPE_STYLES.items():
            assert style["transition"] in valid_transitions, \
                f"Content type '{content_type}' has invalid transition: '{style['transition']}'"

    def test_transition_duration_is_positive(self):
        for content_type, style in CONTENT_TYPE_STYLES.items():
            assert style["transition_duration"] > 0, \
                f"Content type '{content_type}' has non-positive transition_duration"

    def test_subtitle_position_is_valid(self):
        valid_positions = {"bottom", "center", "top"}
        for content_type, style in CONTENT_TYPE_STYLES.items():
            assert style["subtitle_position"] in valid_positions, \
                f"Content type '{content_type}' has invalid subtitle_position"

    def test_theme_override_colors_are_hex(self):
        """theme_override colors should be valid hex color strings."""
        for content_type, style in CONTENT_TYPE_STYLES.items():
            override = style.get("theme_override")
            if override:
                for key in ("bg", "accent", "text", "accent_secondary"):
                    if key in override:
                        color = override[key]
                        assert color.startswith("#"), \
                            f"'{content_type}' override '{key}' is not a hex color: {color}"
                        assert len(color) == 7, \
                            f"'{content_type}' override '{key}' has wrong length: {color}"

    def test_styles_match_keywords_types(self):
        """All content types in KEYWORDS should have corresponding STYLES."""
        for content_type in CONTENT_TYPE_KEYWORDS:
            assert content_type in CONTENT_TYPE_STYLES, \
                f"Content type '{content_type}' has keywords but no style"

    def test_labels_are_chinese(self):
        for content_type, style in CONTENT_TYPE_STYLES.items():
            label = style["label"]
            assert any('\u4e00' <= c <= '\u9fff' for c in label), \
                f"Content type '{content_type}' label '{label}' has no CJK characters"


# ============================================================
# Cross-Configuration Consistency
# ============================================================

class TestConfigConsistency:
    """Tests for consistency across configuration sections."""

    def test_voice_profile_bgm_styles_exist_in_bgm_config(self):
        """All voice profile bgm_style values should exist in BGM_CONFIG styles."""
        bgm_styles = set(BGM_CONFIG["styles"].keys())
        for profile_name, profile in VOICE_PROFILES.items():
            assert profile["bgm_style"] in bgm_styles, \
                f"Voice profile '{profile_name}' bgm_style '{profile['bgm_style']}' not in BGM_CONFIG"

    def test_content_type_bgm_map_covers_all_types(self):
        """type_bgm_map should cover all content types plus 'default'."""
        for content_type in CONTENT_TYPE_STYLES:
            assert content_type in BGM_CONFIG["type_bgm_map"], \
                f"Content type '{content_type}' missing from BGM type_bgm_map"

    def test_bgm_style_dirs_are_unique(self):
        """Each BGM style should have a unique directory."""
        dirs = [s["dir"] for s in BGM_CONFIG["styles"].values()]
        assert len(dirs) == len(set(dirs)), "Duplicate BGM directories"

    def test_ken_burns_speed_values_match_content_styles(self):
        """All ken_burns_speed values in CONTENT_TYPE_STYLES should exist in KEN_BURNS_SPEED_MAP."""
        for content_type, style in CONTENT_TYPE_STYLES.items():
            speed = style["ken_burns_speed"]
            assert speed in KEN_BURNS_SPEED_MAP, \
                f"Content type '{content_type}' uses unknown Ken Burns speed: '{speed}'"

    def test_voice_profile_voices_match_tts_config(self):
        """All voice profile voices should be in TTS_CONFIG available voices."""
        all_voices = set(TTS_CONFIG["voices"].values())
        for name, profile in VOICE_PROFILES.items():
            assert profile["voice"] in all_voices, \
                f"Voice profile '{name}' voice '{profile['voice']}' not in TTS_CONFIG"

    def test_default_bgm_style_exists(self):
        """BGM_CONFIG default_style should exist in styles."""
        assert BGM_CONFIG["default_style"] in BGM_CONFIG["styles"], \
            f"Default BGM style '{BGM_CONFIG['default_style']}' not in styles"

    def test_ffmpeg_path_is_configured(self):
        """FFmpeg path should be configured and point to a real binary."""
        assert PATHS_CONFIG["ffmpeg"] != "ffmpeg" or os.path.exists("ffmpeg"), \
            "FFmpeg path is not properly configured"
        # If using imageio-ffmpeg, path should exist
        if PATHS_CONFIG["ffmpeg"] != "ffmpeg":
            assert os.path.exists(PATHS_CONFIG["ffmpeg"]), \
                f"FFmpeg binary not found at: {PATHS_CONFIG['ffmpeg']}"

    def test_paths_config_has_skill_root(self):
        """PATHS_CONFIG should have skill_root field."""
        assert "skill_root" in PATHS_CONFIG
        assert os.path.isdir(PATHS_CONFIG["skill_root"]), \
            f"skill_root is not a valid directory: {PATHS_CONFIG['skill_root']}"

    def test_paths_are_dynamic(self):
        """temp_dir and assets_dir should be under skill_root, not hardcoded."""
        skill_root = PATHS_CONFIG["skill_root"]
        assert PATHS_CONFIG["temp_dir"].startswith(skill_root) or \
               os.path.normpath(PATHS_CONFIG["temp_dir"]).startswith(os.path.normpath(skill_root)), \
            f"temp_dir '{PATHS_CONFIG['temp_dir']}' is not under skill_root '{skill_root}'"
        assert PATHS_CONFIG["assets_dir"].startswith(skill_root) or \
               os.path.normpath(PATHS_CONFIG["assets_dir"]).startswith(os.path.normpath(skill_root)), \
            f"assets_dir '{PATHS_CONFIG['assets_dir']}' is not under skill_root '{skill_root}'"

    def test_cache_dir_is_dynamic(self):
        """cache_dir should be under skill_root."""
        skill_root = PATHS_CONFIG["skill_root"]
        cache_dir = CACHE_CONFIG["cache_dir"]
        assert os.path.normpath(cache_dir).startswith(os.path.normpath(skill_root)), \
            f"cache_dir '{cache_dir}' is not under skill_root '{skill_root}'"

    def test_assets_dir_exists(self):
        """assets_dir should point to an existing directory."""
        assert os.path.isdir(PATHS_CONFIG["assets_dir"]), \
            f"assets_dir does not exist: {PATHS_CONFIG['assets_dir']}"

    def test_temp_dir_path_valid(self):
        """temp_dir path should be valid (parent exists)."""
        parent = os.path.dirname(PATHS_CONFIG["temp_dir"])
        assert os.path.isdir(parent), \
            f"temp_dir parent does not exist: {parent}"

    def test_ai_image_config_type_map_matches_content_types(self):
        """AI_IMAGE_CONFIG type_style_map should match CONTENT_TYPE_STYLES keys."""
        content_type_keys = set(CONTENT_TYPE_STYLES.keys())
        ai_style_keys = set(AI_IMAGE_CONFIG["type_style_map"].keys())
        assert content_type_keys == ai_style_keys or content_type_keys.issubset(ai_style_keys), \
            f"Mismatch: CONTENT_TYPE_STYLES has {content_type_keys - ai_style_keys} not in AI_IMAGE_CONFIG"


# ============================================================
# BGM Directory Structure
# ============================================================

class TestBGMDirectoryStructure:
    """Tests for BGM directory structure existence."""

    def test_bgm_base_dir_exists(self):
        """assets/bgm directory should exist."""
        bgm_base = os.path.join(PATHS_CONFIG["assets_dir"], "bgm")
        assert os.path.exists(bgm_base), f"BGM base directory not found: {bgm_base}"

    def test_all_style_dirs_exist(self):
        """Each BGM style directory should exist (may be empty)."""
        bgm_base = os.path.join(PATHS_CONFIG["assets_dir"], "bgm")
        for style_name, style_info in BGM_CONFIG["styles"].items():
            style_dir = os.path.join(bgm_base, style_info["dir"])
            assert os.path.exists(style_dir), \
                f"BGM style directory not found: {style_dir}"

    def test_bgm_readme_exists(self):
        """BGM README should exist with instructions."""
        readme = os.path.join(PATHS_CONFIG["assets_dir"], "bgm", "README.txt")
        assert os.path.exists(readme), "BGM README.txt not found"


# ============================================================
# AI Image Configuration
# ============================================================

class TestAIImageConfig:
    """Tests for AI_IMAGE_CONFIG configuration."""

    def test_is_dict(self):
        assert isinstance(AI_IMAGE_CONFIG, dict)

    def test_has_required_fields(self):
        for field in ["image_size", "default_style", "no_text", "type_style_map"]:
            assert field in AI_IMAGE_CONFIG, f"Missing AI_IMAGE_CONFIG field: {field}"

    def test_type_style_map_covers_all_content_types(self):
        """type_style_map should have entries for all content types."""
        from config import CONTENT_TYPE_STYLES
        for content_type in CONTENT_TYPE_STYLES:
            assert content_type in AI_IMAGE_CONFIG["type_style_map"], \
                f"Content type '{content_type}' missing from AI_IMAGE_CONFIG type_style_map"

    def test_has_default_style(self):
        assert "default" in AI_IMAGE_CONFIG["type_style_map"]

    def test_each_style_has_required_fields(self):
        for content_type, style in AI_IMAGE_CONFIG["type_style_map"].items():
            assert "artistic_style" in style, f"'{content_type}' missing artistic_style"
            assert "color_mood" in style, f"'{content_type}' missing color_mood"
            assert "composition" in style, f"'{content_type}' missing composition"

    def test_no_text_is_boolean(self):
        assert isinstance(AI_IMAGE_CONFIG["no_text"], bool)

    def test_image_size_is_valid_preset(self):
        valid_sizes = {"square", "portrait_4_3", "portrait_16_9",
                       "landscape_4_3", "landscape_16_9"}
        assert AI_IMAGE_CONFIG["image_size"] in valid_sizes or "x" in AI_IMAGE_CONFIG["image_size"]

    def test_style_descriptions_are_strings(self):
        for content_type, style in AI_IMAGE_CONFIG["type_style_map"].items():
            assert isinstance(style["artistic_style"], str)
            assert isinstance(style["color_mood"], str)
            assert isinstance(style["composition"], str)
            assert len(style["artistic_style"]) > 0
            assert len(style["color_mood"]) > 0
            assert len(style["composition"]) > 0
