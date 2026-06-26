"""Unit tests for survivor-profile memory management."""

from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest


class TestProfileShape:
    def test_empty_profile_first_write(self, memory, isolated_memory_dir: Path):
        profile, created = memory.load_profile()
        assert created is True
        assert profile["schema_version"] == 1
        assert profile["game"] == "Don't Starve"
        assert profile["survivor"]["game_version"] is None
        assert profile["world"]["settings"] == {}
        assert profile["progress"]["bosses_defeated"] == []
        assert profile["characters"] == {}

        memory.save_profile(profile, touch_updated_at=False)
        assert (isolated_memory_dir / "survivor-profile.json").exists()

    def test_normalize_rejects_bad_schema(self, memory):
        with pytest.raises(ValueError, match="Unsupported schema_version"):
            memory.normalize_profile({"schema_version": 99})

    def test_normalize_fills_missing_fields(self, memory):
        profile = memory.normalize_profile({"schema_version": 1, "game": "Don't Starve"})
        assert profile["survivor"]["name"] is None
        assert profile["progress"]["ruins_explored"] is False
        assert profile["preferences"] == []


class TestPatchMerging:
    def test_survivor_world_progress_and_character_patch(self, memory):
        profile = memory.empty_profile()
        updated = memory.apply_patch(
            profile,
            {
                "survivor": {
                    "name": "Moran",
                    "game_version": "DST",
                    "play_style": "survival",
                    "experience": "intermediate",
                },
                "world": {
                    "settings": {"day_length": "long", "caves": True},
                    "season_day": 18,
                    "current_season": "Autumn",
                },
                "progress": {
                    "bosses_defeated": ["Deerclops", "Bee Queen"],
                    "ruins_explored": True,
                    "milestones": ["Built Alchemy Engine"],
                },
                "characters": {
                    "Wendy": {"preferred": True, "notes": ["Comfort pick for hounds."]},
                },
                "preferences": ["base near beefalo"],
            },
        )

        assert updated["survivor"]["game_version"] == "DST"
        assert updated["world"]["settings"]["caves"] is True
        assert updated["world"]["season_day"] == 18
        assert updated["progress"]["bosses_defeated"] == ["Deerclops", "Bee Queen"]
        assert updated["progress"]["ruins_explored"] is True
        assert updated["characters"]["Wendy"]["preferred"] is True
        assert updated["preferences"] == ["base near beefalo"]

    def test_lists_are_deduplicated(self, memory):
        profile = memory.empty_profile()
        first = memory.apply_patch(profile, {"progress": {"bosses_defeated": ["Deerclops", "Deerclops"]}})
        second = memory.apply_patch(first, {"progress": {"bosses_defeated": ["Deerclops", "Bearger"]}})
        assert second["progress"]["bosses_defeated"] == ["Deerclops", "Bearger"]

    def test_boolean_progress_only_upgrades(self, memory):
        profile = memory.apply_patch(memory.empty_profile(), {"progress": {"ruins_explored": True}})
        updated = memory.apply_patch(profile, {"progress": {"ruins_explored": False}})
        assert updated["progress"]["ruins_explored"] is True
        assert any(p["field"] == "progress.ruins_explored" for p in updated["pending_confirmations"])

    def test_text_conflict_goes_to_pending_confirmation(self, memory):
        profile = memory.apply_patch(memory.empty_profile(), {"survivor": {"name": "Moran"}})
        updated = memory.apply_patch(profile, {"survivor": {"name": "Wilson"}})
        assert updated["survivor"]["name"] == "Moran"
        assert updated["pending_confirmations"][0]["field"] == "survivor.name"
        assert updated["pending_confirmations"][0]["incoming"] == "Wilson"

    def test_game_version_is_validated(self, memory):
        with pytest.raises(ValueError, match="game_version"):
            memory.apply_patch(memory.empty_profile(), {"survivor": {"game_version": "ROG"}})

    def test_world_settings_support_bool_number_and_text(self, memory):
        profile = memory.apply_patch(
            memory.empty_profile(),
            {"world": {"settings": {"caves": True, "world_size": "large", "branching": 3}}},
        )
        assert profile["world"]["settings"] == {"caves": True, "world_size": "large", "branching": 3}

    def test_character_preference_can_be_unset_without_pending_confirmation(self, memory):
        profile = memory.apply_patch(memory.empty_profile(), {"characters": {"Wendy": {"preferred": True}}})
        updated = memory.apply_patch(profile, {"characters": {"Wendy": {"preferred": False}}})

        assert updated["characters"]["Wendy"]["preferred"] is False
        assert updated["pending_confirmations"] == []


class TestCommands:
    def test_confirm_applies_pending_value(self, memory):
        profile = memory.apply_patch(memory.empty_profile(), {"survivor": {"name": "Moran"}})
        profile = memory.apply_patch(profile, {"survivor": {"name": "Wilson"}})
        memory.save_profile(profile, touch_updated_at=False)

        rc = memory.command_confirm(SimpleNamespace(field="survivor.name", apply=True))
        assert rc == 0
        loaded, _ = memory.load_profile()
        assert loaded["survivor"]["name"] == "Wilson"
        assert loaded["pending_confirmations"] == []

    def test_dismiss_removes_pending_value(self, memory):
        profile = memory.apply_patch(memory.empty_profile(), {"survivor": {"name": "Moran"}})
        profile = memory.apply_patch(profile, {"survivor": {"name": "Wilson"}})
        memory.save_profile(profile, touch_updated_at=False)

        rc = memory.command_dismiss(SimpleNamespace(field="survivor.name"))
        assert rc == 0
        loaded, _ = memory.load_profile()
        assert loaded["survivor"]["name"] == "Moran"
        assert loaded["pending_confirmations"] == []

    def test_read_initializes_profile(self, memory, isolated_memory_dir: Path):
        rc = memory.command_read(SimpleNamespace())
        assert rc == 0
        assert (isolated_memory_dir / "survivor-profile.json").exists()


class TestPathsAndMigration:
    def test_env_override(self, memory, tmp_path: Path):
        custom_dir = tmp_path / "custom"
        os.environ["DONTSTARVE_MEMORY_DIR"] = str(custom_dir)
        assert memory.memory_dir() == custom_dir.resolve()
        assert memory.profile_path() == custom_dir.resolve() / "survivor-profile.json"

    def test_migration_copies_legacy_profile(self, memory, isolated_memory_dir: Path, tmp_path: Path):
        legacy_root = tmp_path / "legacy"
        legacy_dir = legacy_root / ".dontstarve-memory"
        legacy_dir.mkdir(parents=True)
        legacy_profile = memory.empty_profile()
        legacy_profile["survivor"]["name"] = "Legacy"
        (legacy_dir / "survivor-profile.json").write_text(
            json.dumps(legacy_profile, ensure_ascii=False),
            encoding="utf-8",
        )

        new_path = isolated_memory_dir / "survivor-profile.json"
        with (
            mock.patch.object(memory, "skill_root", return_value=legacy_root),
            mock.patch.dict(os.environ, {"DONTSTARVE_MEMORY_DIR": ""}, clear=False),
            mock.patch.object(memory, "profile_path", return_value=new_path),
        ):
            memory.migrate_legacy_if_needed()

        assert new_path.exists()
        loaded = json.loads(new_path.read_text(encoding="utf-8"))
        assert loaded["survivor"]["name"] == "Legacy"
        assert (legacy_dir / ".migrated").exists()
