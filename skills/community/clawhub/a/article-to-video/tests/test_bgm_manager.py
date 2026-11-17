# -*- coding: utf-8 -*-
"""
BGM Manager Tests

Tests for bgm_manager.py — validates BGM library management operations:
upload, list, remove, validate, and info.
"""

import json
import os
import shutil
import sys
import pytest

# conftest.py already adds SCRIPTS_DIR to sys.path
from bgm_manager import (
    validate_audio_file,
    get_bgm_base_dir,
    get_style_dir,
    list_bgm_files,
    upload_bgm_file,
    remove_bgm_file,
    get_bgm_info,
)
from config import BGM_CONFIG, PATHS_CONFIG


# ============================================================
# BGM Directory Resolution
# ============================================================

class TestBGMDirectory:
    """Tests for BGM directory path resolution."""

    def test_get_bgm_base_dir_returns_string(self):
        result = get_bgm_base_dir()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_bgm_base_dir_contains_bgm(self):
        result = get_bgm_base_dir()
        assert "bgm" in result

    def test_get_style_dir_valid_style(self):
        result = get_style_dir("corporate")
        assert isinstance(result, str)
        assert "corporate" in result

    def test_get_style_dir_unknown_style_returns_empty(self):
        result = get_style_dir("nonexistent_style")
        assert result == ""

    def test_get_style_dir_all_configured_styles(self):
        for style_name in BGM_CONFIG["styles"]:
            result = get_style_dir(style_name)
            assert len(result) > 0
            assert BGM_CONFIG["styles"][style_name]["dir"] in result


# ============================================================
# Audio File Validation
# ============================================================

class TestValidateAudioFile:
    """Tests for validate_audio_file()."""

    def test_nonexistent_file(self):
        is_valid, msg = validate_audio_file("nonexistent_file.mp3")
        assert is_valid is False
        assert "not found" in msg.lower()

    def test_unsupported_extension(self, tmp_path):
        fake_file = tmp_path / "test.txt"
        fake_file.write_text("not audio")
        is_valid, msg = validate_audio_file(str(fake_file))
        assert is_valid is False
        assert "unsupported" in msg.lower()

    def test_file_too_small(self, tmp_path):
        tiny_file = tmp_path / "tiny.mp3"
        tiny_file.write_bytes(b"\x00" * 100)  # 100 bytes, below 10KB threshold
        is_valid, msg = validate_audio_file(str(tiny_file))
        assert is_valid is False
        assert "small" in msg.lower()

    def test_valid_audio_file_passes(self, sample_audio_file):
        """A real audio file should pass validation."""
        is_valid, msg = validate_audio_file(sample_audio_file)
        assert is_valid is True, f"Validation failed: {msg}"

    def test_validation_message_contains_info(self, sample_audio_file):
        """Validation success message should contain useful info."""
        is_valid, msg = validate_audio_file(sample_audio_file)
        assert is_valid is True
        # Message should contain some info about the file
        assert len(msg) > 0

    def test_validation_handles_nonexistent_gracefully(self):
        """Non-existent file should not raise exception."""
        is_valid, msg = validate_audio_file("does_not_exist.mp3")
        assert is_valid is False
        assert "not found" in msg.lower()


# ============================================================
# BGM File Listing
# ============================================================

class TestListBGMFiles:
    """Tests for list_bgm_files()."""

    def test_returns_dict(self):
        result = list_bgm_files()
        assert isinstance(result, dict)

    def test_all_styles_present(self):
        result = list_bgm_files()
        for style_name in BGM_CONFIG["styles"]:
            assert style_name in result

    def test_filtered_by_style(self):
        result = list_bgm_files("corporate")
        assert "corporate" in result
        assert len(result) == 1

    def test_unknown_style_returns_empty(self):
        result = list_bgm_files("nonexistent_style")
        assert result == {}

    def test_each_style_has_required_fields(self):
        result = list_bgm_files()
        for style_name, info in result.items():
            assert "label" in info
            assert "dir" in info
            assert "volume" in info
            assert "files" in info
            assert "count" in info
            assert isinstance(info["files"], list)
            assert isinstance(info["count"], int)

    def test_file_info_has_required_fields(self):
        result = list_bgm_files()
        for style_name, info in result.items():
            for f in info["files"]:
                assert "filename" in f
                assert "path" in f
                assert "size_kb" in f


# ============================================================
# BGM Info
# ============================================================

class TestGetBGMInfo:
    """Tests for get_bgm_info()."""

    def test_returns_dict(self):
        result = get_bgm_info()
        assert isinstance(result, dict)

    def test_has_required_fields(self):
        result = get_bgm_info()
        for field in ["base_dir", "auto_select", "default_style",
                       "total_files", "styles", "type_bgm_map"]:
            assert field in result, f"Missing field: {field}"

    def test_base_dir_is_string(self):
        result = get_bgm_info()
        assert isinstance(result["base_dir"], str)

    def test_auto_select_matches_config(self):
        result = get_bgm_info()
        assert result["auto_select"] == BGM_CONFIG["auto_select"]

    def test_default_style_matches_config(self):
        result = get_bgm_info()
        assert result["default_style"] == BGM_CONFIG["default_style"]

    def test_total_files_is_int(self):
        result = get_bgm_info()
        assert isinstance(result["total_files"], int)
        assert result["total_files"] >= 0

    def test_styles_has_all_configured(self):
        result = get_bgm_info()
        for style_name in BGM_CONFIG["styles"]:
            assert style_name in result["styles"]

    def test_type_bgm_map_has_all_types(self):
        result = get_bgm_info()
        for content_type in BGM_CONFIG["type_bgm_map"]:
            assert content_type in result["type_bgm_map"]

    def test_type_bgm_map_has_style_info(self):
        result = get_bgm_info()
        for content_type, m in result["type_bgm_map"].items():
            assert "bgm_style" in m
            assert "style_label" in m


# ============================================================
# Upload and Remove (with temp files)
# ============================================================

class TestUploadRemove:
    """Tests for upload_bgm_file() and remove_bgm_file() with temp files."""

    def test_upload_unknown_style_fails(self, tmp_path):
        fake_audio = tmp_path / "test.mp3"
        fake_audio.write_bytes(b"\x00" * 20000)  # > 10KB
        success, msg = upload_bgm_file(str(fake_audio), "nonexistent_style")
        assert success is False
        assert "unknown" in msg.lower()

    def test_upload_validates_file(self, tmp_path):
        """Upload should validate the audio file before copying."""
        invalid_file = tmp_path / "invalid.txt"
        invalid_file.write_text("not audio")
        success, msg = upload_bgm_file(str(invalid_file), "corporate")
        assert success is False

    def test_remove_unknown_style_fails(self):
        success, msg = remove_bgm_file("nonexistent_style", "test.mp3")
        assert success is False

    def test_remove_nonexistent_file_fails(self):
        success, msg = remove_bgm_file("corporate", "nonexistent_file.mp3")
        assert success is False

    def test_remove_non_audio_file_refused(self, tmp_path):
        """remove_bgm_file should refuse to delete non-audio files."""
        # Create a non-audio file in the style directory
        style_dir = get_style_dir("corporate")
        os.makedirs(style_dir, exist_ok=True)
        txt_file = os.path.join(style_dir, "readme.txt")
        with open(txt_file, 'w') as f:
            f.write("test")
        success, msg = remove_bgm_file("corporate", "readme.txt")
        assert success is False
        assert "non-audio" in msg.lower() or "refusing" in msg.lower()
        # Clean up
        os.remove(txt_file)

    def test_upload_with_force_overwrites(self, sample_audio_file):
        """upload_bgm_file with force=True should overwrite existing file."""
        # First upload (copy real audio to corporate style dir)
        success1, msg1 = upload_bgm_file(sample_audio_file, "corporate",
                                         rename="test_force.mp3")
        assert success1 is True, f"First upload failed: {msg1}"
        # Second upload without force should fail (file already exists)
        success2, msg2 = upload_bgm_file(sample_audio_file, "corporate",
                                         rename="test_force.mp3")
        assert success2 is False
        assert "already exists" in msg2.lower()
        # Third upload with force should succeed
        success3, msg3 = upload_bgm_file(sample_audio_file, "corporate",
                                         rename="test_force.mp3", force=True)
        assert success3 is True, f"Force upload failed: {msg3}"
        # Clean up
        remove_bgm_file("corporate", "test_force.mp3")

    def test_upload_with_force_param_default_false(self, sample_audio_file):
        """upload_bgm_file force parameter should default to False."""
        # Upload first time (should succeed)
        success1, _ = upload_bgm_file(sample_audio_file, "corporate",
                                      rename="test_default_force.mp3")
        assert success1 is True
        # Upload second time without force (should fail — file already exists)
        success2, msg2 = upload_bgm_file(sample_audio_file, "corporate",
                                         rename="test_default_force.mp3")
        assert success2 is False
        assert "already exists" in msg2.lower()
        # Clean up
        remove_bgm_file("corporate", "test_default_force.mp3")


# ============================================================
# BGM Configuration Consistency
# ============================================================

class TestBGMConfigConsistency:
    """Cross-tests between bgm_manager and BGM_CONFIG."""

    def test_all_styles_in_config_have_dirs(self):
        for style_name, info in BGM_CONFIG["styles"].items():
            assert "dir" in info
            assert len(info["dir"]) > 0

    def test_all_styles_in_config_have_volumes(self):
        for style_name, info in BGM_CONFIG["styles"].items():
            assert "volume" in info
            assert "dB" in info["volume"]

    def test_all_type_bgm_map_values_exist_in_styles(self):
        for content_type, bgm_style in BGM_CONFIG["type_bgm_map"].items():
            assert bgm_style in BGM_CONFIG["styles"], \
                f"Content type '{content_type}' maps to unknown BGM style '{bgm_style}'"

    def test_style_dirs_are_unique(self):
        dirs = [s["dir"] for s in BGM_CONFIG["styles"].values()]
        assert len(dirs) == len(set(dirs)), "Duplicate BGM style directories"
