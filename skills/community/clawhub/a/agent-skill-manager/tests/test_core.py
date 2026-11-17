"""Tests for agent_skill_manager.core module."""

import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from agent_skill_manager.services.sync import (
    list_skills,
    get_status,
    sync_skill,
    pack_skill,
    _update_workbuddy_settings,
)


class TestListSkills:
    def test_empty_when_no_central_dir(self, tmp_path):
        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path / "nonexistent"):
            assert list_skills() == []

    def test_lists_skill_dirs(self, tmp_path):
        skill1 = tmp_path / "skill1"
        skill1.mkdir()
        (skill1 / "SKILL.md").write_text("---\nname: skill1\n---\n")

        skill2 = tmp_path / "skill2"
        skill2.mkdir()
        (skill2 / "SKILL.md").write_text("---\nname: skill2\n---\n")

        not_skill = tmp_path / "not-skill"
        not_skill.mkdir()

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            skills = list_skills()
            assert len(skills) == 2
            assert skill1 in skills
            assert skill2 in skills

    def test_sorted_results(self, tmp_path):
        for name in ["zebra", "alpha", "mango"]:
            d = tmp_path / name
            d.mkdir()
            (d / "SKILL.md").write_text("---\nname: %s\n---\n" % name)

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            skills = list_skills()
            names = [s.name for s in skills]
            assert names == sorted(names)


class TestGetStatus:
    def test_returns_results_for_all_products(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            results = get_status("my-skill")
            assert len(results) > 0
            shorts = {r["product_short"] for r in results}
            assert "dumate" in shorts
            assert "minimax" in shorts

    def test_empty_for_nonexistent_skill(self, tmp_path):
        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            assert get_status("nonexistent") == []


class TestPackSkill:
    def test_creates_zip(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n# Body")
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "run.py").write_text("# script")

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            result = pack_skill("my-skill", verbose=False)
            assert result is not None
            assert result.suffix == ".zip"
            assert result.exists()

    def test_returns_none_for_missing_skill(self, tmp_path):
        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            assert pack_skill("nonexistent", verbose=False) is None

    def test_returns_none_without_skill_md(self, tmp_path):
        d = tmp_path / "no-md"
        d.mkdir()

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            assert pack_skill("no-md", verbose=False) is None


class TestWorkBuddySettings:
    def test_creates_settings_file(self, tmp_path):
        settings_path = tmp_path / "settings.json"
        _update_workbuddy_settings(settings_path, "my-skill", verbose=False)
        assert settings_path.exists()
        data = json.loads(settings_path.read_text())
        assert data["skills"]["my-skill"] is True

    def test_updates_existing_settings(self, tmp_path):
        settings_path = tmp_path / "settings.json"
        settings_path.write_text(json.dumps({"skills": {"existing": True}}))
        _update_workbuddy_settings(settings_path, "new-skill", verbose=False)
        data = json.loads(settings_path.read_text())
        assert data["skills"]["existing"] is True
        assert data["skills"]["new-skill"] is True


class TestExtraDirsSync:
    """2026-08-14: extra_dirs (e.g. AutoClaw's ~/.openclaw-autoclaw/skills/) must be synced too."""

    def test_sync_creates_links_in_extra_dirs(self, tmp_path):
        """sync_skill should create junction/symlink in each declared extra dir."""
        from unittest.mock import patch, MagicMock
        from agent_skill_manager.services import sync as core

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        extra_dir = tmp_path / "extra-skills"
        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "primary",
            "windows_path": tmp_path / "primary",
            "sync_method": "symlink",
            "extra_dirs_macos": [extra_dir],
            "extra_dirs_windows": [extra_dir],
        }

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path", return_value=tmp_path / "primary"):
            results = core.sync_skill("my-skill", verbose=False)

        assert "my-skill" in results
        assert (extra_dir / "my-skill").exists() or (extra_dir / "my-skill").is_symlink()

    def test_get_status_reports_ok_when_extra_dir_has_link(self, tmp_path):
        """get_status should report ok if the skill exists only in an extra dir."""
        from unittest.mock import patch
        from agent_skill_manager.services import sync as core

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        extra_dir = tmp_path / "extra-skills"
        extra_dir.mkdir()
        # Simulate a pre-existing junction/copy in the extra dir
        (extra_dir / "my-skill").mkdir()

        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "primary",
            "windows_path": tmp_path / "primary",
            "sync_method": "symlink",
            "extra_dirs_macos": [extra_dir],
            "extra_dirs_windows": [extra_dir],
        }

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path", return_value=tmp_path / "primary"):
            results = core.get_status("my-skill")

        assert len(results) == 1
        assert results[0]["status"] == "ok"



class TestInstallSync:
    """install_skill with sync=True auto-syncs to products."""

    def test_install_local_with_sync(self, tmp_path):
        """install --sync from local path should install + sync."""
        from unittest.mock import patch, MagicMock
        from agent_skill_manager.services import sync as core

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "primary",
            "windows_path": tmp_path / "primary",
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path / "central"), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path",
                   return_value=tmp_path / "primary"):
            ok = core.install_skill(str(skill_dir), sync=True, verbose=False)
            assert ok is True

        # Central repo should have the skill
        assert (tmp_path / "central" / "my-skill" / "SKILL.md").exists()

    def test_install_url_returns_name(self, tmp_path):
        """_install_from_url returns skill name on success."""
        from unittest.mock import patch, MagicMock
        from agent_skill_manager.services import sync as core

        # tmp is the clone root; code appends sub_path "my-skill"
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path / "central"), \
             patch("subprocess.run", return_value=MagicMock(returncode=0)), \
             patch("tempfile.TemporaryDirectory") as mock_tmp, \
             patch("shutil.copytree") as mock_copy:

            mock_tmp.return_value.__enter__.return_value = str(tmp_path)

            name, ok = core._install_from_url(
                "https://github.com/user/repo/tree/main/my-skill", verbose=False
            )
            assert name == "my-skill"
            assert ok is True

    def test_install_blob_url(self, tmp_path):
        """_install_from_url handles /blob/ URLs (strips SKILL.md)."""
        from unittest.mock import patch, MagicMock
        from agent_skill_manager.services import sync as core

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path / "central"), \
             patch("subprocess.run", return_value=MagicMock(returncode=0)), \
             patch("tempfile.TemporaryDirectory") as mock_tmp, \
             patch("shutil.copytree") as mock_copy:

            mock_tmp.return_value.__enter__.return_value = str(tmp_path)

            name, ok = core._install_from_url(
                "https://github.com/user/repo/blob/main/my-skill/SKILL.md",
                verbose=False
            )
            assert name == "my-skill"
            assert ok is True

    def test_install_repo_root_url(self, tmp_path):
        """_install_from_url handles repo root URL (no /tree/ or /blob/)."""
        from unittest.mock import patch, MagicMock
        from agent_skill_manager.services import sync as core

        # repo root: sub_path="", so src = tmp (clone root) itself
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        (repo_root / "SKILL.md").write_text("---\nname: agent-skill-manager\n---\n")

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path / "central"), \
             patch("subprocess.run", return_value=MagicMock(returncode=0)), \
             patch("tempfile.TemporaryDirectory") as mock_tmp, \
             patch("shutil.copytree") as mock_copy:

            mock_tmp.return_value.__enter__.return_value = str(repo_root)

            name, ok = core._install_from_url(
                "https://github.com/yxdwind/agent-skill-manager",
                verbose=False
            )
            assert name == "agent-skill-manager"
            assert ok is True

    def test_install_rejects_non_github_url(self, tmp_path):
        """_install_from_url rejects non-GitHub URLs."""
        from unittest.mock import patch
        from agent_skill_manager.services import sync as core

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path / "central"):
            name, ok = core._install_from_url("https://gitlab.com/user/repo", verbose=False)
            assert name is None
            assert ok is False
