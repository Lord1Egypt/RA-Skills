#!/usr/bin/env python3
"""Regression tests for link-root target preservation, in a throwaway guild.

Run: python3 scripts/test_link_root.py
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ag  # noqa: E402


class LinkRootTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="ag-link-root-")
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.central = self.base / "guild"
        self.guild = self.central / "skills"
        self.root = self.base / "runtime" / "skills"
        self.external = self.base / "runtime" / "external"
        (self.guild / "agent-guild").mkdir(parents=True)
        (self.guild / "agent-guild" / "SKILL.md").write_text(
            "guild skill", encoding="utf-8")
        self.root.mkdir(parents=True)
        self.external.mkdir()
        (self.external / "SKILL.md").write_text(
            "original foreign skill", encoding="utf-8")
        for patcher in (
            mock.patch.object(ag, "CENTRAL", self.central),
            mock.patch.object(ag, "_locate_linkable_root", return_value=self.root),
            mock.patch.object(ag, "audit"),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def link(self, path, target):
        try:
            path.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink support unavailable: {exc}")

    def run_command(self, apply=True):
        output = io.StringIO()
        with redirect_stdout(output):
            code = ag.cmd_link_root(["test"] + (["--apply"] if apply else []))
        return code, output.getvalue()

    def assert_original_target(self, name="foreign"):
        self.assertEqual((self.root / name).resolve(), self.external)
        self.assertEqual((self.root / name / "SKILL.md").read_text(
            encoding="utf-8"), "original foreign skill")

    def test_relative_foreign_link_keeps_target(self):
        self.link(self.root / "foreign", "../external")
        self.assertEqual(self.run_command()[0], 0)
        self.assertEqual(self.root.resolve(), self.guild)
        self.assert_original_target()

    def test_absolute_foreign_link_keeps_target(self):
        self.link(self.root / "foreign", self.external)
        self.assertEqual(self.run_command()[0], 0)
        self.assert_original_target()

    def test_dangling_relative_link_keeps_target(self):
        self.link(self.root / "missing", "../not-installed")
        expected = (self.root / "missing").resolve()
        self.assertEqual(self.run_command()[0], 0)
        self.assertTrue((self.guild / "missing").is_symlink())
        self.assertEqual((self.root / "missing").resolve(), expected)

    def test_dry_run_keeps_relative_link_in_place(self):
        self.link(self.root / "foreign", "../external")
        self.assertEqual(self.run_command(apply=False)[0], 0)
        self.assertFalse(self.root.is_symlink())
        self.assertEqual(os.readlink(self.root / "foreign"), "../external")
        self.assertFalse((self.guild / "foreign").exists())
        self.assert_original_target()

    def test_same_name_different_target_blocks_before_any_changes(self):
        self.link(self.root / "agent-guild", self.guild / "agent-guild")
        self.link(self.root / "foreign", "../external")
        (self.guild / "foreign").mkdir()
        marker = self.guild / "foreign" / "SKILL.md"
        marker.write_text("unrelated guild skill", encoding="utf-8")
        for apply in (False, True):
            with self.subTest(apply=apply):
                code, output = self.run_command(apply=apply)
                self.assertEqual(code, 1)
                self.assertIn("LINK CONFLICT", output)
                self.assertFalse(self.root.is_symlink())
                self.assertTrue((self.root / "agent-guild").is_symlink())
                self.assertEqual(marker.read_text(encoding="utf-8"),
                                 "unrelated guild skill")
                self.assert_original_target()

    def test_same_name_dangling_guild_link_also_blocks(self):
        self.link(self.root / "foreign", "../external")
        self.link(self.guild / "foreign", self.base / "missing")
        self.assertEqual(self.run_command()[0], 1)
        self.assertFalse(self.root.is_symlink())
        self.assert_original_target()
        self.assertEqual(os.readlink(self.guild / "foreign"),
                         str(self.base / "missing"))

    def test_same_name_same_target_is_redundant(self):
        self.link(self.root / "foreign", "../external")
        self.link(self.guild / "foreign", self.external)
        self.assertEqual(self.run_command()[0], 0)
        self.assertEqual(self.root.resolve(), self.guild)
        self.assert_original_target()

    def test_alias_to_differently_named_guild_skill_survives(self):
        self.link(self.root / "alias", self.guild / "agent-guild")
        self.assertEqual(self.run_command()[0], 0)
        self.assertEqual((self.root / "alias").resolve(),
                         self.guild / "agent-guild")
        self.assertEqual((self.root / "alias" / "SKILL.md").read_text(
            encoding="utf-8"), "guild skill")

    def test_unresolvable_loop_is_reported_without_changes(self):
        self.link(self.root / "loop", "loop")
        code, output = self.run_command()
        self.assertEqual(code, 1)
        self.assertIn("LINK CONFLICT", output)
        self.assertFalse(self.root.is_symlink())
        self.assertEqual(os.readlink(self.root / "loop"), "loop")

    def test_failed_replacement_keeps_original_link(self):
        self.link(self.root / "foreign", "../external")
        with mock.patch.object(ag, "make_link", return_value=(False, "denied")):
            self.assertEqual(self.run_command()[0], 1)
        self.assertFalse(self.root.is_symlink())
        self.assertFalse((self.guild / "foreign").is_symlink())
        self.assert_original_target()


if __name__ == "__main__":
    unittest.main()
