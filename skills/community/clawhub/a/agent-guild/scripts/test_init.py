#!/usr/bin/env python3
"""Offline init version-selection regressions; all packages are temporary.

Run: python3 scripts/test_init.py
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


class InitVersionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="ag-init-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        env = patch.dict(os.environ, {
            "AGENT_GUILD_DIR": str(self.root / "guild"),
            "AG_HOST_ID": "test-host",
        })
        env.start()
        self.addCleanup(env.stop)
        spec = importlib.util.spec_from_file_location(
            "ag_init_test", Path(__file__).with_name("ag.py"))
        self.ag = importlib.util.module_from_spec(spec)
        modules = patch.dict(sys.modules, {spec.name: self.ag})
        modules.start()
        self.addCleanup(modules.stop)
        spec.loader.exec_module(self.ag)
        self.source = self.root / "source"
        self.installed = self.ag.CENTRAL / "skills/agent-guild"
        self.ag.__file__ = str(self.source / "scripts/ag.py")

    def package(self, path, skill, proto="3.3", marker="package"):
        path.mkdir(parents=True, exist_ok=True)
        (path / "SKILL.md").write_text(marker, encoding="utf-8")
        (path / "manifest.json").write_text(json.dumps({
            "name": "agent-guild",
            "protocol_version": proto, "skill_version": skill,
        }), encoding="utf-8")
        (path / "references").mkdir(exist_ok=True)
        for doc in self.ag.PROTOCOL_DOCS:
            (path / "references" / doc).write_text(marker + ": " + doc,
                                                   encoding="utf-8")

    def init(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.ag.cmd_init(["test-agent"]), 0)

    def assert_installed(self, skill, proto, marker):
        self.assertEqual(self.ag.current_versions(self.installed), (proto, skill))
        version = self.ag.read_runtime_version()
        self.assertEqual(version["skill_version"], skill)
        self.assertEqual(version["protocol_version"], proto)
        self.assertEqual((self.installed / "SKILL.md").read_text(encoding="utf-8"), marker)

    def test_old_source_keeps_newer_package_anchor_and_docs(self):
        self.package(self.source, "3.10.0", marker="old source")
        self.package(self.installed, "3.11.0", marker="newer installed")
        self.ag.write_runtime_version("3.3", "3.11.0")
        for doc in self.ag.PROTOCOL_DOCS:
            (self.ag.CENTRAL / doc).write_text("existing " + doc, encoding="utf-8")
        self.init()
        self.assert_installed("3.11.0", "3.3", "newer installed")
        for doc in self.ag.PROTOCOL_DOCS:
            self.assertEqual((self.ag.CENTRAL / doc).read_text(encoding="utf-8"),
                             "existing " + doc)

    def test_older_protocol_does_not_trigger_downgrade(self):
        self.package(self.source, "3.10.0", "3.2", "old source")
        self.package(self.installed, "3.11.0", "3.3", "newer installed")
        self.ag.write_runtime_version("3.3", "3.11.0")
        self.init()
        self.assert_installed("3.11.0", "3.3", "newer installed")
        self.assertEqual((self.ag.CENTRAL / "SPEC.md").read_text(encoding="utf-8"),
                         "newer installed: SPEC.md")

    def test_installed_manifest_wins_over_stale_or_missing_anchor(self):
        self.package(self.source, "3.10.0", marker="old source")
        self.package(self.installed, "3.11.0", marker="newer installed")
        self.ag.write_runtime_version("3.3", "3.9.0")
        self.init()
        self.assert_installed("3.11.0", "3.3", "newer installed")
        (self.ag.host_dir() / "VERSION").unlink()
        self.init()
        self.assert_installed("3.11.0", "3.3", "newer installed")

    def test_newer_source_upgrades_package_and_docs_preserving_user_data(self):
        self.package(self.source, "3.11.0", marker="new source")
        self.package(self.installed, "3.10.0", marker="old installed")
        self.ag.write_runtime_version("3.3", "3.10.0")
        profile = self.ag.CENTRAL / "identity/profile.md"
        profile.parent.mkdir()
        profile.write_text("user identity", encoding="utf-8")
        (self.ag.CENTRAL / "SPEC.md").write_text("old spec", encoding="utf-8")
        self.init()
        self.assert_installed("3.11.0", "3.3", "new source")
        self.assertEqual((self.ag.CENTRAL / "SPEC.md").read_text(encoding="utf-8"),
                         "new source: SPEC.md")
        self.assertEqual(profile.read_text(encoding="utf-8"), "user identity")

    def test_missing_package_installs_available_source_despite_stale_anchor(self):
        self.package(self.source, "3.11.0", marker="available source")
        self.ag.write_runtime_version("3.4", "3.12.0")
        self.init()
        self.assert_installed("3.11.0", "3.3", "available source")

    def test_running_updated_central_package_refreshes_old_anchor_and_docs(self):
        self.package(self.installed, "3.11.0", marker="updated central")
        self.ag.__file__ = str(self.installed / "scripts/ag.py")
        self.ag.write_runtime_version("3.3", "3.10.0")
        (self.ag.CENTRAL / "SPEC.md").write_text("old spec", encoding="utf-8")
        self.init()
        self.assert_installed("3.11.0", "3.3", "updated central")
        self.assertEqual((self.ag.CENTRAL / "SPEC.md").read_text(encoding="utf-8"),
                         "updated central: SPEC.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
