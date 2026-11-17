# -*- coding: utf-8 -*-
"""
Stage 3: Slide Generation Tests

Tests for create_slides.py — validates theme resolution,
slide rendering, image output, and manifest structure.
"""

import json
import os
import sys
import pytest
from PIL import Image

from create_slides import (
    get_theme,
    resolve_style,
    render_template_slide,
    render_title_slide,
    run_slide_pipeline,
    generate_ai_manifest,
)
from config import SLIDE_CONFIG, VIDEO_CONFIG, CONTENT_TYPE_STYLES


# ============================================================
# Theme Resolution
# ============================================================

# ============================================================
# Visual Style Resolution
# ============================================================

class TestResolveStyle:
    """Tests for resolve_style() — content type to visual style mapping."""

    def test_returns_dict(self):
        result = resolve_style("default")
        assert isinstance(result, dict)

    def test_has_required_fields(self):
        result = resolve_style("default")
        for field in ["theme", "theme_name", "font_title", "font_body",
                       "ken_burns_speed", "content_type"]:
            assert field in result, f"Missing field: {field}"

    def test_default_content_type(self):
        result = resolve_style("default")
        assert result["content_type"] == "default"
        assert result["ken_burns_speed"] == "normal"

    def test_finance_style(self):
        result = resolve_style("finance")
        assert result["theme_name"] == "ocean"
        assert result["ken_burns_speed"] == "slow"

    def test_technology_style(self):
        result = resolve_style("technology")
        assert result["theme_name"] == "dark"
        assert result["ken_burns_speed"] == "fast"

    def test_business_style(self):
        result = resolve_style("business")
        assert result["theme_name"] == "default"
        assert result["ken_burns_speed"] == "normal"

    def test_education_style(self):
        result = resolve_style("education")
        assert result["theme_name"] == "warm"
        assert result["ken_burns_speed"] == "normal"

    def test_news_style(self):
        result = resolve_style("news")
        assert result["theme_name"] == "light"
        assert result["ken_burns_speed"] == "fast"

    def test_science_style(self):
        result = resolve_style("science")
        assert result["theme_name"] == "ocean"
        assert result["ken_burns_speed"] == "slow"

    def test_lifestyle_style(self):
        result = resolve_style("lifestyle")
        assert result["theme_name"] == "warm"
        assert result["ken_burns_speed"] == "normal"

    def test_unknown_type_falls_back(self):
        """Unknown content type should fall back to 'default' style."""
        result = resolve_style("nonexistent_type")
        assert result["content_type"] == "nonexistent_type"
        # Should use default style settings
        assert result["ken_burns_speed"] == "normal"

    def test_user_theme_override(self):
        """User theme override should take precedence over content type theme."""
        result = resolve_style("finance", user_theme="dark")
        assert result["theme_name"] == "dark"
        # But ken_burns_speed should still come from content type
        assert result["ken_burns_speed"] == "slow"

    def test_theme_override_colors_applied(self):
        """Content type theme_override colors should be applied to theme dict."""
        result = resolve_style("finance")
        theme = result["theme"]
        # finance has accent_secondary in override
        assert "accent_secondary" in theme
        assert theme["accent_secondary"] == "#f59e0b"

    def test_default_has_no_override(self):
        """Default content type should have no theme override."""
        result = resolve_style("default")
        # Theme should be the base default theme
        base_theme = get_theme("default")
        assert result["theme"]["bg"] == base_theme["bg"]
        assert result["theme"]["accent"] == base_theme["accent"]

    def test_all_content_types_resolvable(self):
        """All content types in CONTENT_TYPE_STYLES should resolve without error."""
        for content_type in CONTENT_TYPE_STYLES:
            result = resolve_style(content_type)
            assert isinstance(result, dict)
            assert "theme" in result
            assert "ken_burns_speed" in result

    def test_font_title_differs_by_type(self):
        """Different content types should have different font configurations."""
        finance = resolve_style("finance")
        tech = resolve_style("technology")
        assert finance["font_title"] != tech["font_title"]


class TestGetTheme:
    """Tests for get_theme()."""

    def test_returns_dict(self):
        theme = get_theme("default")
        assert isinstance(theme, dict)

    def test_default_theme_has_required_fields(self):
        theme = get_theme("default")
        assert "bg" in theme
        assert "accent" in theme
        assert "text" in theme

    def test_all_configured_themes_valid(self):
        for name in SLIDE_CONFIG["themes"]:
            theme = get_theme(name)
            assert "bg" in theme
            assert "accent" in theme
            assert "text" in theme

    def test_unknown_theme_falls_back(self):
        theme = get_theme("nonexistent_theme")
        default = get_theme(SLIDE_CONFIG["default_theme"])
        assert theme == default

    def test_dark_theme(self):
        theme = get_theme("dark")
        assert theme["bg"] == "#0f0f0f"

    def test_light_theme(self):
        theme = get_theme("light")
        assert theme["bg"] == "#f8f9fa"

    def test_warm_theme(self):
        theme = get_theme("warm")
        assert theme["bg"] == "#2d1810"

    def test_ocean_theme(self):
        theme = get_theme("ocean")
        assert theme["bg"] == "#0c1e3a"


# ============================================================
# Template Slide Rendering
# ============================================================

class TestRenderTemplateSlide:
    """Tests for render_template_slide()."""

    def test_creates_png_file(self, sample_scene, temp_output_dir):
        theme = get_theme("default")
        width, height = 1920, 1080
        output = os.path.join(temp_output_dir, "test_scene.png")
        result = render_template_slide(sample_scene, output, theme, width, height)
        assert os.path.exists(output)

    def test_returns_output_path(self, sample_scene, temp_output_dir):
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "test_scene.png")
        result = render_template_slide(sample_scene, output, theme, 1920, 1080)
        assert result == output

    def test_correct_dimensions(self, sample_scene, temp_output_dir):
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "test_scene.png")
        render_template_slide(sample_scene, output, theme, 1920, 1080)
        with Image.open(output) as img:
            assert img.size == (1920, 1080)

    def test_custom_dimensions(self, sample_scene, temp_output_dir):
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "test_scene_720.png")
        render_template_slide(sample_scene, output, theme, 1280, 720)
        with Image.open(output) as img:
            assert img.size == (1280, 720)

    def test_png_format(self, sample_scene, temp_output_dir):
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "test_format.png")
        render_template_slide(sample_scene, output, theme, 1920, 1080)
        with Image.open(output) as img:
            assert img.format == "PNG"

    def test_different_themes(self, sample_scene, temp_output_dir):
        """Test rendering with different themes doesn't crash."""
        for theme_name in SLIDE_CONFIG["themes"]:
            theme = get_theme(theme_name)
            output = os.path.join(temp_output_dir, f"test_{theme_name}.png")
            render_template_slide(sample_scene, output, theme, 1920, 1080)
            assert os.path.exists(output)

    def test_vertical_resolution(self, sample_scene, temp_output_dir):
        """Test TikTok-style vertical resolution."""
        theme = get_theme("dark")
        output = os.path.join(temp_output_dir, "test_vertical.png")
        render_template_slide(sample_scene, output, theme, 1080, 1920)
        with Image.open(output) as img:
            assert img.size == (1080, 1920)


class TestRenderTitleSlide:
    """Tests for render_title_slide()."""

    def test_creates_png_file(self, temp_output_dir):
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "title.png")
        render_title_slide("测试标题", output, theme, 1920, 1080, subtitle="副标题")
        assert os.path.exists(output)

    def test_correct_dimensions(self, temp_output_dir):
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "title.png")
        render_title_slide("标题", output, theme, 1920, 1080)
        with Image.open(output) as img:
            assert img.size == (1920, 1080)

    def test_with_subtitle(self, temp_output_dir):
        theme = get_theme("dark")
        output = os.path.join(temp_output_dir, "title_sub.png")
        render_title_slide("标题", output, theme, 1920, 1080, subtitle="3.5 min video")
        assert os.path.getsize(output) > 0

    def test_without_subtitle(self, temp_output_dir):
        theme = get_theme("dark")
        output = os.path.join(temp_output_dir, "title_nosub.png")
        render_title_slide("标题", output, theme, 1920, 1080)
        assert os.path.getsize(output) > 0

    def test_long_title(self, temp_output_dir):
        """Test that very long titles don't crash."""
        theme = get_theme("default")
        output = os.path.join(temp_output_dir, "title_long.png")
        long_title = "这是一个非常非常非常非常长的标题文本" * 5
        render_title_slide(long_title, output, theme, 1920, 1080)
        assert os.path.exists(output)


# ============================================================
# AI Image Manifest Generation
# ============================================================

class TestGenerateAIManifest:
    """Tests for generate_ai_manifest() — AI image request manifest."""

    def test_creates_manifest_file(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "technology", 1920, 1080
        )
        assert os.path.exists(manifest_path)

    def test_manifest_is_valid_json(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "default", 1920, 1080
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        assert isinstance(manifest, dict)

    def test_manifest_has_required_fields(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "default", 1920, 1080
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        assert "mode" in manifest
        assert "content_type" in manifest
        assert "image_size" in manifest
        assert "resolution" in manifest
        assert "total_requests" in manifest
        assert "requests" in manifest
        assert "instructions" in manifest

    def test_manifest_requests_match_scene_count(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "default", 1920, 1080
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        assert manifest["total_requests"] == len(scenes_data["scenes"])
        assert len(manifest["requests"]) == len(scenes_data["scenes"])

    def test_each_request_has_prompt_and_output_path(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "technology", 1920, 1080
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        for req in manifest["requests"]:
            assert "prompt" in req
            assert "output_path" in req
            assert "image_size" in req
            assert "scene_index" in req
            assert len(req["prompt"]) > 0

    def test_manifest_content_type_matches(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "finance", 1920, 1080
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        assert manifest["content_type"] == "finance"

    def test_manifest_resolution_matches(self, sample_scenes_json, temp_output_dir):
        import json
        with open(sample_scenes_json, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)
        manifest_path = generate_ai_manifest(
            scenes_data["scenes"], temp_output_dir, "default", 1080, 1920
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        assert manifest["resolution"] == "1080x1920"


# ============================================================
# Slide Pipeline
# ============================================================

class TestRunSlidePipeline:
    """Tests for the full slide pipeline."""

    def test_generates_images(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        files = os.listdir(temp_output_dir)
        png_files = [f for f in files if f.endswith(".png")]
        assert len(png_files) >= 3  # 1 title + 2 scenes

    def test_generates_manifest(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        manifest_path = os.path.join(temp_output_dir, "manifest.json")
        assert os.path.exists(manifest_path)
        assert isinstance(manifest, dict)

    def test_manifest_has_required_fields(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="dark",
            platform="youtube"
        )
        assert "title_slide" in manifest
        assert "scenes" in manifest
        assert "theme" in manifest
        assert "resolution" in manifest
        assert "platform" in manifest
        assert "content_type" in manifest
        assert "ken_burns_speed" in manifest

    def test_manifest_scene_count(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        assert len(manifest["scenes"]) == 2  # sample_scenes_json has 2 scenes

    def test_title_slide_exists(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        assert os.path.exists(manifest["title_slide"])

    def test_scene_images_exist(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        for scene in manifest["scenes"]:
            assert os.path.exists(scene["image"])

    def test_image_dimensions_match_platform(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="tiktok"
        )
        expected_w, expected_h = 1080, 1920
        for scene in manifest["scenes"]:
            with Image.open(scene["image"]) as img:
                assert img.size == (expected_w, expected_h)

    def test_manifest_theme_matches(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="ocean",
            platform="youtube"
        )
        assert manifest["theme"] == "ocean"

    def test_manifest_resolution_matches(self, sample_scenes_json, temp_output_dir):
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        assert manifest["resolution"] == "1920x1080"

    def test_manifest_content_type_matches_input(self, sample_scenes_json_with_content_type, temp_output_dir):
        """Manifest content_type should match scenes.json content_type."""
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json_with_content_type,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        assert manifest["content_type"] == "technology"

    def test_manifest_ken_burns_speed_for_technology(self, sample_scenes_json_with_content_type, temp_output_dir):
        """Technology content type should produce fast Ken Burns speed in manifest."""
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json_with_content_type,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        assert manifest["ken_burns_speed"] == "fast"

    def test_ai_mode_generates_manifest(self, sample_scenes_json, temp_output_dir):
        """AI mode should generate ai_image_requests.json manifest."""
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="ai",
            theme_name="default",
            platform="youtube"
        )
        ai_manifest_path = os.path.join(temp_output_dir, "ai_image_requests.json")
        assert os.path.exists(ai_manifest_path)

    def test_ai_mode_manifest_has_requests(self, sample_scenes_json, temp_output_dir):
        """AI mode manifest should contain image generation requests."""
        import json
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="ai",
            theme_name="default",
            platform="youtube"
        )
        ai_manifest_path = os.path.join(temp_output_dir, "ai_image_requests.json")
        with open(ai_manifest_path, 'r', encoding='utf-8') as f:
            ai_manifest = json.load(f)
        assert ai_manifest["total_requests"] > 0
        assert len(ai_manifest["requests"]) > 0

    def test_ai_mode_generates_fallback_slides(self, sample_scenes_json, temp_output_dir):
        """AI mode should generate template slides as fallback."""
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="ai",
            theme_name="default",
            platform="youtube"
        )
        # Fallback slides should exist
        for scene in manifest["scenes"]:
            assert os.path.exists(scene["image"])

    def test_manifest_has_mode_field(self, sample_scenes_json, temp_output_dir):
        """Manifest should include mode field."""
        manifest = run_slide_pipeline(
            scenes_path=sample_scenes_json,
            output_dir=temp_output_dir,
            mode="template",
            theme_name="default",
            platform="youtube"
        )
        assert manifest["mode"] == "template"


# ============================================================
# Existing Output Validation
# ============================================================

class TestExistingSlides:
    """Validate existing slide images from the pipeline run."""

    def test_slide_files_exist(self, workspace_dir, existing_manifest_json):
        slides_dir = os.path.join(workspace_dir, "slides")
        assert os.path.exists(os.path.join(slides_dir, "title.png"))
        for scene in existing_manifest_json["scenes"]:
            filename = os.path.basename(scene["image"])
            path = os.path.join(slides_dir, filename)
            assert os.path.exists(path)

    def test_slide_images_are_png(self, workspace_dir, existing_manifest_json):
        slides_dir = os.path.join(workspace_dir, "slides")
        title_path = os.path.join(slides_dir, "title.png")
        with Image.open(title_path) as img:
            assert img.format == "PNG"

    def test_slide_dimensions(self, workspace_dir, existing_manifest_json):
        slides_dir = os.path.join(workspace_dir, "slides")
        title_path = os.path.join(slides_dir, "title.png")
        with Image.open(title_path) as img:
            assert img.size == (1920, 1080)

    def test_slide_files_nonempty(self, workspace_dir, existing_manifest_json):
        slides_dir = os.path.join(workspace_dir, "slides")
        title_path = os.path.join(slides_dir, "title.png")
        assert os.path.getsize(title_path) > 5000  # At least 5KB

    def test_manifest_structure(self, existing_manifest_json):
        assert "title_slide" in existing_manifest_json
        assert "scenes" in existing_manifest_json
        assert "theme" in existing_manifest_json
        assert "resolution" in existing_manifest_json
        assert "platform" in existing_manifest_json

    def test_manifest_resolution_value(self, existing_manifest_json):
        assert "x" in existing_manifest_json["resolution"]
        w, h = existing_manifest_json["resolution"].split("x")
        assert int(w) > 0
        assert int(h) > 0
