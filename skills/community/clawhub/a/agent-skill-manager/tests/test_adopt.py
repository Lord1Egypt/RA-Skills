"""Tests for adopt_from_platform."""

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from agent_skill_manager.services.sync import adopt_from_platform


class TestAdoptFromPlatform:
    def test_unknown_platform(self, tmp_path):
        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            result = adopt_from_platform("nope", verbose=False)
            assert result["adopted"] == []

    def test_native_platform_skipped(self, tmp_path):
        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", tmp_path):
            result = adopt_from_platform("minimax", verbose=False)
            assert result["adopted"] == []

    def test_adopt_single_skill(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "platform-skills",
            "windows_path": tmp_path / "platform-skills",
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }
        platform_dir = tmp_path / "platform-skills"
        platform_dir.mkdir()
        shutil.copytree(skill_dir, platform_dir / "my-skill")

        central = tmp_path / "central"
        central.mkdir()

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", central), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path",
                   return_value=platform_dir), \
             patch("agent_skill_manager.services.sync._is_junction",
                   return_value=False):
            result = adopt_from_platform("testprod", "my-skill", verbose=False)

        assert len(result["adopted"]) == 1
        assert result["adopted"][0][1] is True
        assert (central / "my-skill" / "SKILL.md").exists()

    def test_skill_not_found(self, tmp_path):
        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "platform-skills",
            "windows_path": tmp_path / "platform-skills",
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }
        platform_dir = tmp_path / "platform-skills"
        platform_dir.mkdir()

        central = tmp_path / "central"
        central.mkdir()

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", central), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path",
                   return_value=platform_dir):
            result = adopt_from_platform("testprod", "nonexistent", verbose=False)

        assert result["adopted"] == []

    def test_skip_already_in_central(self, tmp_path):
        """Same name in central but different source -> conflict, no overwrite."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "platform-skills",
            "windows_path": tmp_path / "platform-skills",
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }
        platform_dir = tmp_path / "platform-skills"
        platform_dir.mkdir()
        shutil.copytree(skill_dir, platform_dir / "my-skill")

        central = tmp_path / "central"
        central.mkdir()
        shutil.copytree(skill_dir, central / "my-skill")
        # Make central version slightly different so it is a "different source"
        (central / "my-skill" / "SKILL.md").write_text(
            "---\nname: my-skill\n---\n# central version"
        )

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", central), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path",
                   return_value=platform_dir), \
             patch("agent_skill_manager.services.sync._is_junction",
                   return_value=False):
            result = adopt_from_platform("testprod", "my-skill", verbose=False)

        assert len(result["adopted"]) == 1
        assert result["adopted"][0][1] is False
        assert result["adopted"][0][2] == "conflict"
        # Central version must NOT have been overwritten
        content = (central / "my-skill" / "SKILL.md").read_text()
        assert "# central version" in content

    def test_same_source_is_already_present(self, tmp_path):
        """Junction-style same source in central -> already-present."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        product = {
            "name": "TestProduct",
            "short": "testprod",
            "macos_path": tmp_path / "platform-skills",
            "windows_path": tmp_path / "platform-skills",
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }
        platform_dir = tmp_path / "platform-skills"
        platform_dir.mkdir()
        shutil.copytree(skill_dir, platform_dir / "my-skill")

        central = tmp_path / "central"
        central.mkdir()
        shutil.copytree(skill_dir, central / "my-skill")
        # Simulate junction: source dir IS the central dir (resolve to same)
        shutil.rmtree(platform_dir / "my-skill")
        # make platform dir entry point back at central (hardlink-free copy)
        shutil.copytree(central / "my-skill", platform_dir / "my-skill")
        # Trick resolve: patch Path.resolve to return central path (both dirs)
        def _fake_resolve(self, strict=False):
            if "my-skill" in str(self):
                return central / "my-skill"
            return self

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", central), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product]), \
             patch("agent_skill_manager.services.sync.get_product_path",
                   return_value=platform_dir), \
             patch("agent_skill_manager.services.sync._is_junction",
                   return_value=False), \
             patch("pathlib.Path.resolve", _fake_resolve):
            result = adopt_from_platform("testprod", "my-skill", verbose=False)

        assert len(result["adopted"]) == 1
        assert result["adopted"][0][2] == "already-present"

    def test_excludes_source_platform_from_sync(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

        primary = tmp_path / "primary"
        primary.mkdir()

        product_a = {
            "name": "ProductA",
            "short": "product-a",
            "macos_path": primary,
            "windows_path": primary,
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }
        product_b = {
            "name": "ProductB",
            "short": "product-b",
            "macos_path": primary,
            "windows_path": primary,
            "sync_method": "symlink",
            "extra_dirs_macos": [],
            "extra_dirs_windows": [],
        }

        # The platform skill dir IS the product path (get_product_path -> primary)
        shutil.copytree(skill_dir, primary / "my-skill")

        central = tmp_path / "central"
        central.mkdir()

        with patch("agent_skill_manager.services.sync.CENTRAL_DIR", central), \
             patch("agent_skill_manager.services.sync.PRODUCTS", [product_a, product_b]), \
             patch("agent_skill_manager.services.sync.get_product_path",
                   return_value=primary), \
             patch("agent_skill_manager.services.sync._is_junction",
                   return_value=False):
            result = adopt_from_platform("product-a", "my-skill", verbose=False)

        assert len(result["adopted"]) == 1
        synced = result.get("synced", {})
        assert "my-skill" in synced
