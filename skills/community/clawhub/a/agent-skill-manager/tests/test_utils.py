"""Tests for agent_skill_manager.utils module."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest
from agent_skill_manager.utils.filesystem import (
    is_symlink_or_junction,
    create_link,
    copy_skill,
    read_skill_metadata,
)


class TestIsSymlinkOrJunction:
    def test_nonexistent_path(self, tmp_path):
        assert not is_symlink_or_junction(tmp_path / "nonexistent")

    def test_regular_directory(self, tmp_path):
        d = tmp_path / "regular"
        d.mkdir()
        assert not is_symlink_or_junction(d)

    def test_regular_file(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("hello")
        assert not is_symlink_or_junction(f)


class TestCreateLink:
    def test_creates_link_to_directory(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "SKILL.md").write_text("content")
        dst = tmp_path / "dst"

        success, method, msg = create_link(src, dst)
        assert success
        assert method in ("symlink", "junction", "copy")
        assert (dst / "SKILL.md").exists()

    def test_replaces_existing(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "SKILL.md").write_text("new")
        dst = tmp_path / "dst"
        dst.mkdir()
        (dst / "old.txt").write_text("old")

        success, method, msg = create_link(src, dst)
        assert success
        assert (dst / "SKILL.md").exists()
        assert not (dst / "old.txt").exists()

    def test_source_not_found(self, tmp_path):
        success, method, msg = create_link(tmp_path / "noexist", tmp_path / "dst")
        assert not success
        assert method == "error"


class TestCopySkill:
    def test_copies_directory(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "SKILL.md").write_text("content")
        (src / "scripts").mkdir()
        (src / "scripts" / "run.py").write_text("# script")

        dst = tmp_path / "dst"
        copy_skill(src, dst)
        assert (dst / "SKILL.md").exists()
        assert (dst / "scripts" / "run.py").exists()

    def test_replaces_existing(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "SKILL.md").write_text("new")
        dst = tmp_path / "dst"
        dst.mkdir()
        (dst / "old.txt").write_text("old")

        copy_skill(src, dst)
        assert (dst / "SKILL.md").exists()
        assert not (dst / "old.txt").exists()


class TestReadSkillMetadata:
    def test_reads_name_and_description(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A test skill\n---\n# Body\n"
        )
        meta = read_skill_metadata(skill_dir)
        assert meta["name"] == "my-skill"
        assert meta["description"] == "A test skill"

    def test_returns_empty_for_no_skill_md(self, tmp_path):
        meta = read_skill_metadata(tmp_path)
        assert meta["name"] == ""
        assert meta["description"] == ""

    def test_handles_multiline_description(self, tmp_path):
        skill_dir = tmp_path / "skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test\ndescription: >\n  Multi-line description here\n---\n"
        )
        meta = read_skill_metadata(skill_dir)
        assert meta["name"] == "test"
