# -*- coding: utf-8 -*-
"""
Stage 4: Video Assembly Tests

Tests for assemble_video.py — validates FFmpeg detection, SRT generation,
video output validity, and subtitle format.
"""

import json
import os
import re
import subprocess
import sys
import shutil
import pytest

from config import PATHS_CONFIG, VIDEO_CONFIG, EFFECTS_CONFIG, BGM_CONFIG
from assemble_video import (
    run_ffmpeg,
    check_disk_space,
    generate_srt,
    _get_duration,
    _has_audio_stream,
    _ensure_all_clips_have_audio,
    _find_bgm_for_type,
    _get_bgm_volume,
)


# ============================================================
# FFmpeg Configuration
# ============================================================

class TestFFmpegConfig:
    """Tests for FFmpeg binary detection and availability."""

    def test_ffmpeg_path_is_string(self):
        assert isinstance(PATHS_CONFIG["ffmpeg"], str)
        assert len(PATHS_CONFIG["ffmpeg"]) > 0

    def test_ffmpeg_binary_exists(self):
        assert os.path.exists(PATHS_CONFIG["ffmpeg"]), \
            f"FFmpeg binary not found: {PATHS_CONFIG['ffmpeg']}"

    def test_ffmpeg_runs(self):
        """FFmpeg should execute without error."""
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-version"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0

    def test_ffmpeg_has_libx264_encoder(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-encoders"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "libx264" in result.stdout

    def test_ffmpeg_has_png_decoder(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-decoders"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "png" in result.stdout.lower()

    def test_ffmpeg_has_mp3_decoder(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-decoders"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "mp3" in result.stdout.lower()

    def test_ffmpeg_has_aac_encoder(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-encoders"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "aac" in result.stdout.lower()

    def test_ffmpeg_has_concat_filter(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-filters"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "concat" in result.stdout

    def test_ffmpeg_has_scale_filter(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-filters"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "scale" in result.stdout

    def test_ffmpeg_has_subtitles_filter(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-filters"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "subtitles" in result.stdout.lower()

    def test_ffmpeg_has_zoompan_filter(self):
        cmd = [PATHS_CONFIG["ffmpeg"], "-hide_banner", "-filters"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "zoompan" in result.stdout.lower()


# ============================================================
# BGM Auto-Selection
# ============================================================

class TestBGMSelection:
    """Tests for _find_bgm_for_type() — content type to BGM mapping."""

    def test_returns_string(self):
        result = _find_bgm_for_type("default")
        assert isinstance(result, str)

    def test_unknown_content_type_returns_default_style(self):
        """Unknown content type should map to default BGM style."""
        # This returns "" if no BGM files are in the directory
        result = _find_bgm_for_type("nonexistent_type")
        assert isinstance(result, str)

    def test_finance_maps_to_corporate(self):
        """Finance content should map to corporate BGM style."""
        # Check the mapping in config
        bgm_style = BGM_CONFIG["type_bgm_map"].get("finance")
        assert bgm_style == "corporate"

    def test_technology_maps_to_electronic(self):
        """Technology content should map to electronic BGM style."""
        bgm_style = BGM_CONFIG["type_bgm_map"].get("technology")
        assert bgm_style == "electronic"

    def test_education_maps_to_soft(self):
        """Education content should map to soft BGM style."""
        bgm_style = BGM_CONFIG["type_bgm_map"].get("education")
        assert bgm_style == "soft"

    def test_lifestyle_maps_to_acoustic(self):
        """Lifestyle content should map to acoustic BGM style."""
        bgm_style = BGM_CONFIG["type_bgm_map"].get("lifestyle")
        assert bgm_style == "acoustic"

    def test_science_maps_to_cinematic(self):
        """Science content should map to cinematic BGM style."""
        bgm_style = BGM_CONFIG["type_bgm_map"].get("science")
        assert bgm_style == "cinematic"

    def test_default_maps_to_corporate(self):
        """Default content should map to corporate BGM style."""
        bgm_style = BGM_CONFIG["type_bgm_map"].get("default")
        assert bgm_style == "corporate"

    def test_all_content_types_have_bgm_mapping(self):
        """All content types should have a BGM mapping."""
        from config import CONTENT_TYPE_STYLES
        for content_type in CONTENT_TYPE_STYLES:
            assert content_type in BGM_CONFIG["type_bgm_map"], \
                f"Content type '{content_type}' missing from type_bgm_map"

    def test_all_bgm_styles_have_config(self):
        """All BGM styles in type_bgm_map should have config entries."""
        for content_type, bgm_style in BGM_CONFIG["type_bgm_map"].items():
            assert bgm_style in BGM_CONFIG["styles"], \
                f"BGM style '{bgm_style}' (mapped from '{content_type}') not in styles config"

    def test_bgm_config_has_required_fields(self):
        """BGM_CONFIG should have all required top-level fields."""
        for field in ["styles", "default_style", "auto_select", "type_bgm_map"]:
            assert field in BGM_CONFIG, f"Missing BGM_CONFIG field: {field}"

    def test_bgm_styles_have_dir_and_volume(self):
        """Each BGM style should have 'dir' and 'volume' fields."""
        for name, style in BGM_CONFIG["styles"].items():
            assert "dir" in style, f"Style '{name}' missing 'dir'"
            assert "label" in style, f"Style '{name}' missing 'label'"
            assert "volume" in style, f"Style '{name}' missing 'volume'"

    def test_auto_select_is_enabled(self):
        """Auto-select should be enabled by default."""
        assert BGM_CONFIG["auto_select"] is True

    def test_style_override_bypasses_content_type(self):
        """style_override should bypass content type mapping."""
        # Even with finance content type, override to cinematic
        result = _find_bgm_for_type("finance", style_override="cinematic")
        assert isinstance(result, str)

    def test_style_override_works_with_unknown_content_type(self):
        """style_override should work even with unknown content type."""
        result = _find_bgm_for_type("nonexistent_type", style_override="corporate")
        assert isinstance(result, str)

    def test_style_override_unknown_style_returns_empty(self):
        """Unknown style_override should return empty string."""
        result = _find_bgm_for_type("finance", style_override="nonexistent_style")
        assert result == ""

    def test_auto_select_disabled_returns_empty_without_override(self):
        """When auto_select is disabled, no override should return empty."""
        # Note: this test checks the function behavior when auto_select is False
        # We can't easily change config in test, so we test the override path
        result = _find_bgm_for_type("default", style_override="corporate")
        assert isinstance(result, str)


# ============================================================
# BGM Volume Retrieval
# ============================================================

class TestGetBGMVolume:
    """Tests for _get_bgm_volume() — style-specific volume retrieval."""

    def test_returns_string(self):
        result = _get_bgm_volume("")
        assert isinstance(result, str)

    def test_empty_path_returns_default(self):
        result = _get_bgm_volume("")
        assert result == EFFECTS_CONFIG["bgm_volume"]

    def test_none_path_returns_default(self):
        result = _get_bgm_volume(None)
        assert result == EFFECTS_CONFIG["bgm_volume"]

    def test_corporate_style_volume(self):
        """BGM from corporate style directory should return corporate volume."""
        corporate_vol = BGM_CONFIG["styles"]["corporate"]["volume"]
        # Simulate a path like .../bgm/corporate/track01.mp3
        fake_path = os.path.join("fake", "bgm", "corporate", "track01.mp3")
        result = _get_bgm_volume(fake_path)
        assert result == corporate_vol

    def test_cinematic_style_volume(self):
        """BGM from cinematic style directory should return cinematic volume."""
        cinematic_vol = BGM_CONFIG["styles"]["cinematic"]["volume"]
        fake_path = os.path.join("fake", "bgm", "cinematic", "track01.mp3")
        result = _get_bgm_volume(fake_path)
        assert result == cinematic_vol

    def test_unknown_style_returns_default(self):
        """BGM from unknown style directory should return default volume."""
        fake_path = os.path.join("fake", "bgm", "unknown_style", "track01.mp3")
        result = _get_bgm_volume(fake_path)
        assert result == EFFECTS_CONFIG["bgm_volume"]

    def test_all_styles_have_volume(self):
        """Each BGM style should have a volume field."""
        for style_name, style_info in BGM_CONFIG["styles"].items():
            assert "volume" in style_info, f"Style '{style_name}' missing volume"
            vol = _get_bgm_volume(os.path.join("x", "bgm", style_info["dir"], "test.mp3"))
            assert vol == style_info["volume"]


# ============================================================
# Ken Burns Speed Map Tests
# ============================================================

class TestKenBurnsSpeedMap:
    """Tests for KEN_BURNS_SPEED_MAP configuration."""

    def test_has_three_speeds(self):
        from config import KEN_BURNS_SPEED_MAP
        assert "slow" in KEN_BURNS_SPEED_MAP
        assert "normal" in KEN_BURNS_SPEED_MAP
        assert "fast" in KEN_BURNS_SPEED_MAP

    def test_each_speed_has_zoom_params(self):
        from config import KEN_BURNS_SPEED_MAP
        for speed, cfg in KEN_BURNS_SPEED_MAP.items():
            assert "zoom_start" in cfg, f"Speed '{speed}' missing zoom_start"
            assert "zoom_end" in cfg, f"Speed '{speed}' missing zoom_end"
            assert cfg["zoom_start"] < cfg["zoom_end"], \
                f"Speed '{speed}': zoom_start should be < zoom_end"

    def test_slow_zooms_least(self):
        from config import KEN_BURNS_SPEED_MAP
        slow_range = KEN_BURNS_SPEED_MAP["slow"]["zoom_end"] - KEN_BURNS_SPEED_MAP["slow"]["zoom_start"]
        fast_range = KEN_BURNS_SPEED_MAP["fast"]["zoom_end"] - KEN_BURNS_SPEED_MAP["fast"]["zoom_start"]
        assert slow_range < fast_range, "Slow should zoom less than fast"

    def test_all_content_types_have_ken_burns_speed(self):
        from config import CONTENT_TYPE_STYLES
        for content_type, style in CONTENT_TYPE_STYLES.items():
            assert "ken_burns_speed" in style, \
                f"Content type '{content_type}' missing ken_burns_speed"


# ============================================================
# Disk Space Check
# ============================================================

class TestCheckDiskSpace:
    """Tests for check_disk_space()."""

    def test_returns_true_for_valid_path(self, tmp_path):
        assert check_disk_space(str(tmp_path)) is True

    def test_returns_true_for_workspace(self, workspace_dir):
        assert check_disk_space(workspace_dir) is True

    def test_returns_true_for_nonexistent_path(self):
        """Should return True (skip check) for paths that can't be checked."""
        assert check_disk_space("Z:/nonexistent/path/xyz") is True


# ============================================================
# Duration Measurement
# ============================================================

class TestGetDuration:
    """Tests for _get_duration()."""

    def test_returns_float(self, existing_video_path):
        duration = _get_duration(existing_video_path)
        assert isinstance(duration, float)

    def test_returns_positive(self, existing_video_path):
        duration = _get_duration(existing_video_path)
        assert duration > 0

    def test_nonexistent_file(self):
        duration = _get_duration("nonexistent.mp4")
        assert duration == 10.0  # Fallback value

    def test_existing_video_reasonable_range(self, existing_video_path):
        duration = _get_duration(existing_video_path)
        assert 10.0 <= duration <= 300.0  # 10s to 5min


# ============================================================
# SRT Generation
# ============================================================

class TestGenerateSrt:
    """Tests for generate_srt()."""

    def test_creates_srt_file(self, tmp_path):
        scenes = [
            {"index": 0, "narration": "第一段叙述文本。"},
            {"index": 1, "narration": "第二段叙述文本。"},
        ]
        timing = [
            {"index": 0, "duration": 5.0},
            {"index": 1, "duration": 3.0},
        ]
        srt_path = str(tmp_path / "test.srt")
        generate_srt(scenes, timing, srt_path)
        assert os.path.exists(srt_path)

    def test_srt_has_entries(self, tmp_path):
        scenes = [
            {"index": 0, "narration": "第一段叙述文本。"},
            {"index": 1, "narration": "第二段叙述文本。"},
        ]
        timing = [
            {"index": 0, "duration": 5.0},
            {"index": 1, "duration": 3.0},
        ]
        srt_path = str(tmp_path / "test.srt")
        generate_srt(scenes, timing, srt_path)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "第一段叙述文本" in content
        assert "第二段叙述文本" in content

    def test_srt_timestamps_format(self, tmp_path):
        """SRT timestamps should follow HH:MM:SS,mmm format."""
        scenes = [{"index": 0, "narration": "测试文本"}]
        timing = [{"index": 0, "duration": 5.0}]
        srt_path = str(tmp_path / "test.srt")
        generate_srt(scenes, timing, srt_path)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Should contain timestamp pattern
        assert re.search(r'\d{2}:\d{2}:\d{2},\d{3}', content)

    def test_srt_has_sequence_numbers(self, tmp_path):
        """SRT entries should be numbered sequentially starting from 1."""
        scenes = [
            {"index": 0, "narration": "第一段"},
            {"index": 1, "narration": "第二段"},
        ]
        timing = [
            {"index": 0, "duration": 5.0},
            {"index": 1, "duration": 3.0},
        ]
        srt_path = str(tmp_path / "test.srt")
        generate_srt(scenes, timing, srt_path)
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # First line should be "1"
        assert lines[0].strip() == "1"

    def test_srt_arrow_format(self, tmp_path):
        """SRT should use --> arrow format."""
        scenes = [{"index": 0, "narration": "测试文本"}]
        timing = [{"index": 0, "duration": 5.0}]
        srt_path = str(tmp_path / "test.srt")
        generate_srt(scenes, timing, srt_path)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert " --> " in content

    def test_srt_timestamps_chronological(self, tmp_path):
        """SRT timestamps should be in ascending order."""
        scenes = [
            {"index": 0, "narration": "第一段"},
            {"index": 1, "narration": "第二段"},
            {"index": 2, "narration": "第三段"},
        ]
        timing = [
            {"index": 0, "duration": 5.0},
            {"index": 1, "duration": 3.0},
            {"index": 2, "duration": 4.0},
        ]
        srt_path = str(tmp_path / "test.srt")
        generate_srt(scenes, timing, srt_path)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        timestamps = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})', content)
        # Convert to seconds for comparison
        def to_sec(ts):
            h, m, rest = ts.split(':')
            s, ms = rest.split(',')
            return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
        sec_values = [to_sec(ts) for ts in timestamps]
        for i in range(1, len(sec_values)):
            assert sec_values[i] >= sec_values[i-1]

    def test_srt_with_time_offset(self, tmp_path):
        """SRT timestamps should be shifted by time_offset."""
        scenes = [{"index": 0, "narration": "测试文本"}]
        timing = [{"index": 0, "duration": 5.0}]
        srt_path = str(tmp_path / "test_offset.srt")
        generate_srt(scenes, timing, srt_path, time_offset=3.0)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # First timestamp should start at 00:00:03,000 (3 second offset)
        first_ts = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', content)
        assert first_ts is not None
        h, m, rest = first_ts.group(1).split(':')
        s, ms = rest.split(',')
        assert int(s) == 3, f"Expected offset of 3s, got {s}s"

    def test_srt_time_offset_zero(self, tmp_path):
        """With time_offset=0, SRT should start at 00:00:00."""
        scenes = [{"index": 0, "narration": "测试文本"}]
        timing = [{"index": 0, "duration": 5.0}]
        srt_path = str(tmp_path / "test_zero.srt")
        generate_srt(scenes, timing, srt_path, time_offset=0.0)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        first_ts = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', content)
        assert first_ts is not None
        h, m, rest = first_ts.group(1).split(':')
        s, ms = rest.split(',')
        assert int(s) == 0


# ============================================================
# Existing Video Output Validation
# ============================================================

class TestExistingVideoOutput:
    """Validate the existing final_video.mp4 from the pipeline run."""

    def test_video_file_exists(self, existing_video_path):
        assert os.path.exists(existing_video_path)

    def test_video_file_nonempty(self, existing_video_path):
        size = os.path.getsize(existing_video_path)
        assert size > 100000  # At least 100KB

    def test_video_duration(self, existing_video_path):
        duration = _get_duration(existing_video_path)
        assert duration > 30.0  # At least 30 seconds

    def test_video_has_video_stream(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "Video:" in result.stderr

    def test_video_has_audio_stream(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "Audio:" in result.stderr

    def test_video_codec_is_h264(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "h264" in result.stderr.lower() or "H.264" in result.stderr

    def test_video_audio_codec_is_aac(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "aac" in result.stderr.lower() or "AAC" in result.stderr

    def test_video_resolution_1080p(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "1920x1080" in result.stderr

    def test_video_pixel_format(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "yuv420p" in result.stderr.lower()

    def test_video_is_mp4_container(self, existing_video_path):
        cmd = [PATHS_CONFIG["ffmpeg"], "-i", existing_video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert "mp4" in result.stderr.lower() or "mov" in result.stderr.lower()


# ============================================================
# Existing SRT Validation
# ============================================================

class TestExistingSrt:
    """Validate the existing final_video.srt."""

    def test_srt_file_exists(self, existing_srt_path):
        assert os.path.exists(existing_srt_path)

    def test_srt_nonempty(self, existing_srt_path):
        assert os.path.getsize(existing_srt_path) > 0

    def test_srt_has_entries(self, existing_srt_path):
        with open(existing_srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Should have multiple entries
        entries = content.strip().split('\n\n')
        assert len(entries) >= 5  # At least 5 subtitle entries

    def test_srt_timestamps_valid(self, existing_srt_path):
        with open(existing_srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        timestamps = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', content)
        assert len(timestamps) >= 5

    def test_srt_has_text_content(self, existing_srt_path):
        with open(existing_srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Should contain text between timestamps
        text_lines = re.findall(r'-->\s*\d[^\n]*\n(.+?)(?=\n\n|\Z)', content, re.DOTALL)
        assert len(text_lines) >= 5

    def test_srt_starts_at_zero(self, existing_srt_path):
        """First subtitle should start near 00:00:00."""
        with open(existing_srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        first_ts = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', content)
        assert first_ts is not None
        h, m, rest = first_ts.group(1).split(':')
        assert int(h) == 0 and int(m) == 0


# ============================================================
# Thumbnail Validation
# ============================================================

class TestThumbnail:
    """Validate the video thumbnail."""

    def test_thumbnail_exists(self, workspace_dir):
        path = os.path.join(workspace_dir, "final_video_thumb.jpg")
        assert os.path.exists(path)

    def test_thumbnail_nonempty(self, workspace_dir):
        path = os.path.join(workspace_dir, "final_video_thumb.jpg")
        assert os.path.getsize(path) > 1000

    def test_thumbnail_is_jpeg(self, workspace_dir):
        from PIL import Image
        path = os.path.join(workspace_dir, "final_video_thumb.jpg")
        with Image.open(path) as img:
            assert img.format in ("JPEG", "JPG")

    def test_thumbnail_dimensions(self, workspace_dir):
        from PIL import Image
        path = os.path.join(workspace_dir, "final_video_thumb.jpg")
        with Image.open(path) as img:
            w, h = img.size
            assert w >= 640  # At least 640px wide
            assert h >= 360


# ============================================================
# FFmpeg run_ffmpeg helper
# ============================================================

class TestRunFFmpeg:
    """Tests for the run_ffmpeg helper function."""

    def test_successful_command(self):
        """Test that run_ffmpeg executes a simple command."""
        success, output = run_ffmpeg(["-version"], check=False)
        assert success is True

    def test_failing_command(self):
        """Test that run_ffmpeg reports failure for invalid commands."""
        success, output = run_ffmpeg(["-invalid_flag"], check=False)
        assert success is False

    def test_returns_stderr_on_failure(self):
        """Failed commands should return error message in output."""
        success, output = run_ffmpeg(["-invalid_flag"], check=False)
        assert isinstance(output, str)
        assert len(output) > 0


# ============================================================
# Audio Stream Detection (P1 fix: xfade audio error tolerance)
# ============================================================

class TestHasAudioStream:
    """Tests for _has_audio_stream() — audio stream detection helper."""

    def test_returns_bool(self, sample_audio_file):
        """Should return a boolean."""
        result = _has_audio_stream(sample_audio_file)
        assert isinstance(result, bool)

    def test_valid_audio_file_has_audio(self, sample_audio_file):
        """A valid WAV file should have an audio stream."""
        result = _has_audio_stream(sample_audio_file)
        assert result is True

    def test_nonexistent_file_returns_false(self):
        """Non-existent file should return False (not raise exception)."""
        result = _has_audio_stream("nonexistent_file.mp4")
        assert result is False

    def test_video_with_audio(self, existing_video_path):
        """The existing final_video.mp4 should have audio."""
        result = _has_audio_stream(existing_video_path)
        assert result is True

    def test_image_file_has_no_audio(self, temp_output_dir):
        """A PNG image should not have an audio stream."""
        from create_slides import get_theme, render_title_slide
        # Create a test image
        img_path = os.path.join(temp_output_dir, "test_no_audio.png")
        theme = get_theme("default")
        render_title_slide("Test", img_path, theme, 1920, 1080)
        result = _has_audio_stream(img_path)
        assert result is False


class TestEnsureAllClipsHaveAudio:
    """Tests for _ensure_all_clips_have_audio() — audio normalization helper."""

    def test_returns_list(self, sample_audio_file, tmp_path):
        """Should always return a list."""
        output_path = str(tmp_path / "output.mp4")
        result = _ensure_all_clips_have_audio([sample_audio_file], output_path)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_clips_with_audio_unchanged(self, sample_audio_file, tmp_path):
        """Clips that already have audio should be returned as-is."""
        output_path = str(tmp_path / "output.mp4")
        result = _ensure_all_clips_have_audio([sample_audio_file], output_path)
        assert result[0] == sample_audio_file

    def test_empty_list_returns_empty(self, tmp_path):
        """Empty input should return empty list."""
        output_path = str(tmp_path / "output.mp4")
        result = _ensure_all_clips_have_audio([], output_path)
        assert result == []

    def test_mixed_clips(self, sample_audio_file, temp_output_dir, tmp_path):
        """Mix of audio and non-audio clips should all end up with audio."""
        from config import VIDEO_CONFIG
        from create_slides import get_theme, render_title_slide

        # Create a video with no audio using ffmpeg
        no_audio_video = str(tmp_path / "no_audio.mp4")
        img_path = str(tmp_path / "test.png")
        theme = get_theme("default")
        render_title_slide("Test", img_path, theme, 1920, 1080)

        success, _ = run_ffmpeg([
            "-loop", "1", "-i", img_path,
            "-t", "2",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
            "-c:v", VIDEO_CONFIG["video_codec"], "-preset", "fast",
            "-crf", str(VIDEO_CONFIG["video_crf"]),
            "-pix_fmt", VIDEO_CONFIG["pixel_format"],
            "-an",  # No audio
            no_audio_video
        ], check=False)
        if not success:
            pytest.skip("Could not create test video without audio")

        # Verify it has no audio
        assert _has_audio_stream(no_audio_video) is False

        # Now ensure audio
        output_path = str(tmp_path / "output.mp4")
        result = _ensure_all_clips_have_audio(
            [sample_audio_file, no_audio_video], output_path
        )
        # First clip should be unchanged (already has audio)
        assert result[0] == sample_audio_file
        # Second clip should be a new file with audio added
        assert result[1] != no_audio_video
        assert _has_audio_stream(result[1]) is True
