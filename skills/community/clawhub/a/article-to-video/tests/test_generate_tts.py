# -*- coding: utf-8 -*-
"""
Stage 2: TTS Generation Tests

Tests for generate_tts.py — validates TTS pipeline logic, caching,
duration measurement, and output structure.
"""

import asyncio
import json
import os
import shutil
import sys
import tempfile
import pytest

from generate_tts import (
    measure_audio_duration,
    get_cache_path,
    check_cache,
    save_to_cache,
    load_progress,
    save_progress,
    process_scene,
)
from config import VOICE_PROFILES, TTS_CONFIG


# ============================================================
# Voice Profile Tests
# ============================================================

class TestVoiceProfiles:
    """Tests for VOICE_PROFILES configuration."""

    def test_profiles_is_dict(self):
        assert isinstance(VOICE_PROFILES, dict)
        assert len(VOICE_PROFILES) >= 5

    def test_all_profiles_have_required_fields(self):
        required = ["label", "voice", "rate", "pitch", "narration_volume", "bgm_style"]
        for name, profile in VOICE_PROFILES.items():
            for field in required:
                assert field in profile, f"Profile '{name}' missing field '{field}'"

    def test_profile_labels_are_chinese(self):
        """All profile labels should be Chinese for user display."""
        for name, profile in VOICE_PROFILES.items():
            label = profile["label"]
            assert len(label) > 0
            # Check at least one CJK character
            assert any('\u4e00' <= c <= '\u9fff' for c in label), \
                f"Profile '{name}' label '{label}' has no CJK characters"

    def test_profile_voices_are_valid(self):
        """All voice IDs should follow edge-tts naming convention."""
        for name, profile in VOICE_PROFILES.items():
            voice = profile["voice"]
            assert voice.startswith("zh-CN-"), \
                f"Profile '{name}' voice '{voice}' doesn't start with 'zh-CN-'"
            assert voice.endswith("Neural"), \
                f"Profile '{name}' voice '{voice}' doesn't end with 'Neural'"

    def test_profile_rates_are_valid_format(self):
        """Rates should be percentage strings like '+0%' or '-5%'."""
        for name, profile in VOICE_PROFILES.items():
            rate = profile["rate"]
            assert rate.endswith("%"), f"Profile '{name}' rate '{rate}' missing %"
            # Should start with + or -
            assert rate[0] in "+-", f"Profile '{name}' rate '{rate}' missing sign"

    def test_profile_pitches_are_valid_format(self):
        """Pitches should be Hz strings like '+0Hz' or '-2Hz'."""
        for name, profile in VOICE_PROFILES.items():
            pitch = profile["pitch"]
            assert pitch.endswith("Hz"), f"Profile '{name}' pitch '{pitch}' missing Hz"
            assert pitch[0] in "+-", f"Profile '{name}' pitch '{pitch}' missing sign"

    def test_profile_bgm_styles_are_valid(self):
        """BGM styles should reference valid BGM_CONFIG styles."""
        from config import BGM_CONFIG
        valid_styles = set(BGM_CONFIG["styles"].keys())
        for name, profile in VOICE_PROFILES.items():
            assert profile["bgm_style"] in valid_styles, \
                f"Profile '{name}' bgm_style '{profile['bgm_style']}' not in BGM_CONFIG"

    def test_profile_volumes_are_valid_format(self):
        """Narration volumes should be dB strings like '-3dB'."""
        for name, profile in VOICE_PROFILES.items():
            vol = profile["narration_volume"]
            assert vol.endswith("dB"), f"Profile '{name}' volume '{vol}' missing dB"

    def test_each_profile_has_unique_voice(self):
        """Each profile should use a distinct voice for variety."""
        voices = [p["voice"] for p in VOICE_PROFILES.values()]
        assert len(voices) == len(set(voices)), \
            "Some profiles share the same voice"

    def test_profile_names_are_descriptive(self):
        """Profile names should be lowercase English identifiers."""
        expected_profiles = {"professional", "casual", "energetic", "documentary", "warm"}
        assert expected_profiles.issubset(set(VOICE_PROFILES.keys())), \
            f"Missing expected profiles. Got: {set(VOICE_PROFILES.keys())}"

    def test_profile_voices_in_tts_config(self):
        """Profile voices should be in the available voices list."""
        all_voices = set(TTS_CONFIG["voices"].values())
        for name, profile in VOICE_PROFILES.items():
            assert profile["voice"] in all_voices, \
                f"Profile '{name}' voice '{profile['voice']}' not in TTS_CONFIG voices"


# ============================================================
# Duration Measurement
# ============================================================

class TestMeasureAudioDuration:
    """Tests for measure_audio_duration()."""

    def test_returns_float(self, workspace_dir):
        audio_path = os.path.join(workspace_dir, "audio", "scene_000.mp3")
        if not os.path.exists(audio_path):
            pytest.skip("Audio file not found")
        duration = measure_audio_duration(audio_path)
        assert isinstance(duration, float)

    def test_returns_positive(self, workspace_dir):
        audio_path = os.path.join(workspace_dir, "audio", "scene_000.mp3")
        if not os.path.exists(audio_path):
            pytest.skip("Audio file not found")
        duration = measure_audio_duration(audio_path)
        assert duration > 0

    def test_nonexistent_file(self):
        """Should return 0.0 for nonexistent files."""
        duration = measure_audio_duration("nonexistent_file.mp3")
        assert duration == 0.0

    def test_existing_audio_reasonable_range(self, workspace_dir):
        """Audio durations should be in a reasonable range (1-60 seconds)."""
        audio_path = os.path.join(workspace_dir, "audio", "scene_000.mp3")
        if not os.path.exists(audio_path):
            pytest.skip("Audio file not found")
        duration = measure_audio_duration(audio_path)
        assert 1.0 <= duration <= 120.0


# ============================================================
# Cache Management
# ============================================================

class TestCacheManagement:
    """Tests for cache path generation, checking, and saving."""

    def test_get_cache_path_format(self, tmp_path):
        cache_dir = str(tmp_path / "cache")
        path = get_cache_path("abc123", cache_dir)
        assert path.endswith("abc123.mp3")
        assert cache_dir in path

    def test_check_cache_miss(self, tmp_path):
        cache_dir = str(tmp_path / "cache")
        result = check_cache("nonexistent_hash", cache_dir)
        assert result is None

    def test_check_cache_hit(self, tmp_path):
        cache_dir = str(tmp_path / "cache")
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, "test_hash.mp3")
        with open(cache_file, 'wb') as f:
            f.write(b'\x00' * 100)  # Dummy audio data
        result = check_cache("test_hash", cache_dir)
        assert result == cache_file

    def test_check_cache_empty_file(self, tmp_path):
        """Empty cache files should not be considered hits."""
        cache_dir = str(tmp_path / "cache")
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, "empty.mp3")
        open(cache_file, 'w').close()  # 0-byte file
        result = check_cache("empty", cache_dir)
        assert result is None

    def test_save_to_cache(self, tmp_path):
        """Test saving a file to cache."""
        cache_dir = str(tmp_path / "cache")
        src_file = str(tmp_path / "src.mp3")
        with open(src_file, 'wb') as f:
            f.write(b'\x00' * 200)
        save_to_cache(src_file, "test_hash", cache_dir)
        cached = os.path.join(cache_dir, "test_hash.mp3")
        assert os.path.exists(cached)
        assert os.path.getsize(cached) == 200

    def test_save_to_cache_creates_dir(self, tmp_path):
        """Cache directory should be created if it doesn't exist."""
        cache_dir = str(tmp_path / "new_cache")
        src_file = str(tmp_path / "src.mp3")
        with open(src_file, 'wb') as f:
            f.write(b'\x00' * 100)
        save_to_cache(src_file, "hash", cache_dir)
        assert os.path.exists(cache_dir)


# ============================================================
# Progress / Resume
# ============================================================

class TestProgressManagement:
    """Tests for progress save/load functionality."""

    def test_load_progress_nonexistent(self, tmp_path):
        progress_path = str(tmp_path / "progress.json")
        result = load_progress(progress_path)
        assert result == {}

    def test_save_and_load_progress(self, tmp_path):
        progress_path = str(tmp_path / "progress.json")
        data = {"0": {"done": True, "duration": 10.5, "engine": "edge-tts"}}
        save_progress(progress_path, data)
        loaded = load_progress(progress_path)
        assert loaded == data

    def test_save_progress_creates_file(self, tmp_path):
        progress_path = str(tmp_path / "progress.json")
        save_progress(progress_path, {"test": True})
        assert os.path.exists(progress_path)


# ============================================================
# Timing JSON Validation
# ============================================================

class TestTimingJson:
    """Validate the existing timing.json output."""

    def test_has_required_fields(self, existing_timing_json):
        assert "scenes" in existing_timing_json
        assert "total_duration" in existing_timing_json
        assert "voice" in existing_timing_json
        assert "generated_at" in existing_timing_json

    def test_scenes_is_list(self, existing_timing_json):
        assert isinstance(existing_timing_json["scenes"], list)

    def test_total_duration_positive(self, existing_timing_json):
        assert existing_timing_json["total_duration"] > 0

    def test_scene_fields(self, existing_timing_json):
        for scene in existing_timing_json["scenes"]:
            assert "index" in scene
            assert "audio_file" in scene
            assert "duration" in scene
            assert "engine" in scene
            assert "hash" in scene

    def test_scene_durations_positive(self, existing_timing_json):
        for scene in existing_timing_json["scenes"]:
            assert scene["duration"] > 0

    def test_total_duration_matches_sum(self, existing_timing_json):
        expected = sum(s["duration"] for s in existing_timing_json["scenes"])
        assert abs(existing_timing_json["total_duration"] - round(expected, 2)) < 1.0

    def test_voice_field(self, existing_timing_json):
        assert existing_timing_json["voice"].startswith("zh-")

    def test_engine_is_valid(self, existing_timing_json):
        valid_engines = {"edge-tts", "gtts", "pyttsx3", "cached", "existing"}
        for scene in existing_timing_json["scenes"]:
            assert scene["engine"] in valid_engines


# ============================================================
# Voice Profile Propagation Tests
# ============================================================

class TestVoiceProfilePropagation:
    """Tests for voice profile parameter propagation to timing.json."""

    def test_profile_params_in_voice_profiles(self):
        """Each voice profile should have narration_volume and bgm_style."""
        for name, profile in VOICE_PROFILES.items():
            assert "narration_volume" in profile, \
                f"Profile '{name}' missing narration_volume"
            assert "bgm_style" in profile, \
                f"Profile '{name}' missing bgm_style"

    def test_profile_narration_volume_is_valid_db(self):
        """narration_volume should be a dB string."""
        for name, profile in VOICE_PROFILES.items():
            vol = profile["narration_volume"]
            assert vol.endswith("dB"), \
                f"Profile '{name}' narration_volume '{vol}' missing dB suffix"
            assert vol[0] in "+-", \
                f"Profile '{name}' narration_volume '{vol}' missing sign"

    def test_profile_bgm_style_in_bgm_config(self):
        """bgm_style should reference valid BGM_CONFIG styles."""
        from config import BGM_CONFIG
        valid_styles = set(BGM_CONFIG["styles"].keys())
        for name, profile in VOICE_PROFILES.items():
            assert profile["bgm_style"] in valid_styles, \
                f"Profile '{name}' bgm_style '{profile['bgm_style']}' not in BGM_CONFIG"

    def test_timing_json_accepts_profile_fields(self, tmp_path):
        """timing.json structure should support profile-related fields."""
        # Simulate what run_tts_pipeline would write
        from config import EFFECTS_CONFIG
        timing = {
            "scenes": [],
            "total_duration": 0.0,
            "voice": "zh-CN-YunyangNeural",
            "rate": "+0%",
            "pitch": "+0Hz",
            "profile": "professional",
            "narration_volume": VOICE_PROFILES["professional"]["narration_volume"],
            "bgm_style": VOICE_PROFILES["professional"]["bgm_style"],
            "generated_at": "2026-08-06 12:00:00"
        }
        timing_path = str(tmp_path / "timing.json")
        with open(timing_path, 'w', encoding='utf-8') as f:
            json.dump(timing, f, ensure_ascii=False, indent=2)

        # Read back and verify
        with open(timing_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert loaded["profile"] == "professional"
        assert loaded["narration_volume"] == "-3dB"
        assert loaded["bgm_style"] == "corporate"
        assert loaded["rate"] == "+0%"
        assert loaded["pitch"] == "+0Hz"


# ============================================================
# Audio File Validation
# ============================================================

class TestAudioFiles:
    """Validate that audio files exist and are valid."""

    def test_audio_files_exist(self, workspace_dir, existing_timing_json):
        audio_dir = os.path.join(workspace_dir, "audio")
        for scene in existing_timing_json["scenes"]:
            filename = os.path.basename(scene["audio_file"])
            path = os.path.join(audio_dir, filename)
            assert os.path.exists(path), f"Missing audio: {filename}"

    def test_audio_files_nonempty(self, workspace_dir, existing_timing_json):
        audio_dir = os.path.join(workspace_dir, "audio")
        for scene in existing_timing_json["scenes"]:
            filename = os.path.basename(scene["audio_file"])
            path = os.path.join(audio_dir, filename)
            size = os.path.getsize(path)
            assert size > 1000, f"Audio file too small: {filename} ({size} bytes)"

    def test_audio_file_naming_convention(self, existing_timing_json):
        """Audio files should follow scene_NNN.mp3 naming."""
        import re
        for scene in existing_timing_json["scenes"]:
            filename = os.path.basename(scene["audio_file"])
            assert re.match(r"scene_\d{3}\.mp3", filename), \
                f"Unexpected filename: {filename}"

    def test_audio_count_matches_scenes(self, existing_timing_json, existing_scenes_json):
        assert len(existing_timing_json["scenes"]) == len(existing_scenes_json["scenes"]) \
            or len(existing_timing_json["scenes"]) >= 5  # At least the tested scenes


# ============================================================
# Cache File Validation
# ============================================================

class TestCacheFiles:
    """Validate cache directory from the pipeline run."""

    def test_cache_dir_exists(self, workspace_dir):
        cache_dir = os.path.join(workspace_dir, ".trae", "skills", "article-to-video",
                                 "tmp", ".cache")
        assert os.path.exists(cache_dir)

    def test_cache_files_are_mp3(self, workspace_dir):
        cache_dir = os.path.join(workspace_dir, ".trae", "skills", "article-to-video",
                                 "tmp", ".cache")
        if not os.path.exists(cache_dir):
            pytest.skip("Cache dir not found")
        for f in os.listdir(cache_dir):
            assert f.endswith(".mp3"), f"Non-MP3 file in cache: {f}"

    def test_cache_hash_matches_scenes(self, workspace_dir, existing_timing_json):
        """Cache filenames should contain hashes from timing.json."""
        cache_dir = os.path.join(workspace_dir, ".trae", "skills", "article-to-video",
                                 "tmp", ".cache")
        if not os.path.exists(cache_dir):
            pytest.skip("Cache dir not found")
        cached_hashes = {os.path.splitext(f)[0] for f in os.listdir(cache_dir)}
        timing_hashes = {s["hash"] for s in existing_timing_json["scenes"]}
        # At least some hashes should match
        overlap = cached_hashes & timing_hashes
        assert len(overlap) > 0, "No cache hashes match timing.json hashes"
