"""Tests for lib/ignores.py — .depradar-ignore system."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

from lib.ignores import is_ignored, load_ignores, _parse_ignore_file


class TestIsIgnored:
    def test_exact_match(self):
        ignores = {"chalk@5.3.0"}
        assert is_ignored("chalk", "5.3.0", ignores)

    def test_exact_match_case_insensitive(self):
        ignores = {"chalk@5.3.0"}
        assert is_ignored("Chalk", "5.3.0", ignores)

    def test_major_wildcard(self):
        ignores = {"chalk@5"}
        assert is_ignored("chalk", "5.3.0", ignores)
        assert is_ignored("chalk", "5.0.0", ignores)
        assert not is_ignored("chalk", "4.3.0", ignores)

    def test_package_wildcard(self):
        ignores = {"chalk"}
        assert is_ignored("chalk", "5.3.0", ignores)
        assert is_ignored("chalk", "4.1.2", ignores)
        assert is_ignored("chalk", "99.0.0", ignores)

    def test_no_match(self):
        ignores = {"stripe@8"}
        assert not is_ignored("chalk", "5.3.0", ignores)

    def test_empty_ignores(self):
        assert not is_ignored("chalk", "5.3.0", set())

    def test_different_major_not_ignored(self):
        ignores = {"chalk@5"}
        assert not is_ignored("chalk", "6.0.0", ignores)

    def test_exact_beats_wildcard(self):
        ignores = {"chalk@5", "chalk@5.3.0"}
        assert is_ignored("chalk", "5.3.0", ignores)

    def test_package_with_at_scope(self):
        ignores = {"@company/mylib@2"}
        assert is_ignored("@company/mylib", "2.1.0", ignores)
        assert not is_ignored("@company/mylib", "3.0.0", ignores)

    def test_dotenv_pattern(self):
        ignores = {"dotenv@17"}
        assert is_ignored("dotenv", "17.0.1", ignores)
        assert is_ignored("dotenv", "17.5.0", ignores)
        assert not is_ignored("dotenv", "16.0.0", ignores)


class TestParseIgnoreFile:
    def test_basic_entries(self, tmp_path):
        ignore_file = tmp_path / ".depradar-ignore"
        ignore_file.write_text("chalk@5\ndotenv@17\nstripe\n", encoding="utf-8")
        ignores: set = set()
        _parse_ignore_file(ignore_file, ignores)
        assert "chalk@5" in ignores
        assert "dotenv@17" in ignores
        assert "stripe" in ignores

    def test_strips_comments(self, tmp_path):
        ignore_file = tmp_path / ".depradar-ignore"
        ignore_file.write_text(
            "chalk@5  # ESM-only, evaluated 2026-03-27\n"
            "# This is a full-line comment\n"
            "stripe  # all versions\n",
            encoding="utf-8",
        )
        ignores: set = set()
        _parse_ignore_file(ignore_file, ignores)
        assert "chalk@5" in ignores
        assert "stripe" in ignores
        assert len(ignores) == 2

    def test_strips_v_prefix_in_version(self, tmp_path):
        ignore_file = tmp_path / ".depradar-ignore"
        ignore_file.write_text("chalk@v5.3.0\n", encoding="utf-8")
        ignores: set = set()
        _parse_ignore_file(ignore_file, ignores)
        assert "chalk@5.3.0" in ignores

    def test_empty_lines_ignored(self, tmp_path):
        ignore_file = tmp_path / ".depradar-ignore"
        ignore_file.write_text("\n\n  \nchalk@5\n\n", encoding="utf-8")
        ignores: set = set()
        _parse_ignore_file(ignore_file, ignores)
        assert len(ignores) == 1

    def test_missing_file_no_error(self, tmp_path):
        ignores: set = set()
        _parse_ignore_file(tmp_path / "nonexistent.ignore", ignores)
        assert len(ignores) == 0


class TestLoadIgnores:
    def test_loads_project_file(self, tmp_path):
        ignore_file = tmp_path / ".depradar-ignore"
        ignore_file.write_text("chalk@5\n", encoding="utf-8")
        ignores = load_ignores(str(tmp_path))
        assert "chalk@5" in ignores

    def test_no_ignore_file_returns_empty(self, tmp_path):
        ignores = load_ignores(str(tmp_path))
        assert len(ignores) == 0

    def test_merges_both_files(self, tmp_path, monkeypatch):
        project_file = tmp_path / ".depradar-ignore"
        project_file.write_text("chalk@5\n", encoding="utf-8")

        global_dir = tmp_path / "global"
        global_dir.mkdir()
        global_file = global_dir / "ignore"
        global_file.write_text("stripe@8\n", encoding="utf-8")

        # Monkey-patch the global path
        import lib.ignores as ignores_mod
        orig = ignores_mod._GLOBAL_IGNORE_FILE
        monkeypatch.setattr(ignores_mod, "_GLOBAL_IGNORE_FILE", global_file)
        try:
            ignores = load_ignores(str(tmp_path))
            assert "chalk@5" in ignores
            assert "stripe@8" in ignores
        finally:
            monkeypatch.setattr(ignores_mod, "_GLOBAL_IGNORE_FILE", orig)
