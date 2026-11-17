"""Release metadata, package scope and cross-platform static checks."""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import agent_slim  # noqa: E402
import agent_slim_workflow as workflow  # noqa: E402
import build_release  # noqa: E402

TEXT_SUFFIXES = {".md", ".json", ".py", ".sh", ".yaml", ".yml", ".txt", ".toml"}
PRIVATE_MARKERS = ("/" + "Users" + "/", "C:" + "\\" + "Users", "~/" + ".codex")


def manifest():
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def package_files(platform):
    spec = manifest()["release"]["packages"][platform]
    return build_release.collect(spec["include"], spec.get("exclude", []))


class ReleaseMetadataTests(unittest.TestCase):
    def test_versions_match(self):
        data = manifest()
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(front)
        fields = dict(re.findall(r"^([A-Za-z_]+):\s*(.+)$", front.group(1), re.M))
        self.assertEqual(fields.get("name"), "agent-slim")
        self.assertEqual(fields.get("version"), data["version"])
        self.assertEqual(agent_slim.TOOL_VERSION, data["version"])
        self.assertIn("## {} ".format(data["version"]), (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertEqual(data["release"]["version"], data["version"])

    def test_publishable_files_match_github_package(self):
        data = manifest()
        listed_all = set(data["publishableFiles"])
        missing = {rel for rel in listed_all if not (ROOT / rel).is_file()}
        # ClawHub 安装副本由发布器生成，而发布器跳过路径里带点号的隐藏文件；
        # 只允许这类文件缺失，其他缺失仍然是清单与打包不一致。
        self.assertTrue(
            all(any(part.startswith(".") for part in Path(rel).parts) for rel in missing),
            sorted(missing),
        )
        listed = listed_all - missing
        packaged = set(package_files("github"))
        self.assertEqual(listed, packaged)

    def test_packages_exclude_internal_paths(self):
        for platform in ("github", "skillhub", "clawhub"):
            files = package_files(platform)
            self.assertIn("SKILL.md", files)
            self.assertIn("manifest.json", files)
            for rel in files:
                self.assertFalse(rel.startswith(("AGENTS.md", "prompts/", "outputs/", "dist/", "work/")), (platform, rel))
                self.assertNotEqual(rel, "tests/validate_s1.py")

    def test_skillhub_is_lighter_and_has_no_tests(self):
        github = set(package_files("github"))
        skillhub = set(package_files("skillhub"))
        self.assertLess(len(skillhub), len(github))
        self.assertFalse([rel for rel in skillhub if rel.startswith("tests/")])
        self.assertIn("scripts/agent_slim.py", skillhub)
        self.assertIn("scripts/build_release.py", skillhub)
        self.assertIn("scripts/make_icons.py", skillhub)

    def test_skillhub_layout_uses_license_md(self):
        spec = manifest()["release"]["packages"]["skillhub"]
        layout = [arc for _, arc in build_release.apply_renames(
            build_release.collect(spec["include"], spec.get("exclude", [])), spec.get("renames", {}))]
        self.assertIn("LICENSE.md", layout)
        self.assertNotIn("LICENSE", layout)

    def test_no_private_paths_or_secrets_in_package(self):
        for rel in package_files("github"):
            path = ROOT / rel
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in PRIVATE_MARKERS:
                self.assertNotIn(marker, text, "{} contains {}".format(rel, marker))
            self.assertIsNone(re.search(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]{8,}", text), rel)

    def test_scripts_have_extensions(self):
        for path in SCRIPTS.rglob("*"):
            if path.is_file() and path.parent.name != "__pycache__":
                self.assertTrue(path.suffix, "extensionless script: {}".format(path))

    def test_windows_drive_unc_and_traversal_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="agent-slim-win-") as temp:
            home = Path(temp)
            for bad in ("C:/" + "Users" + "/x", "c:\\temp\\x", "//server/share/x", "\\\\server\\share\\x", "../x", "a/../b"):
                with self.assertRaises(workflow.WorkflowError, msg=bad) as caught:
                    workflow.safe_relative_target(home, bad)
                self.assertEqual(caught.exception.code, "SCOPE_VIOLATION")
            self.assertEqual(workflow.safe_relative_target(home, "a\\b"), home.resolve() / "a" / "b")


if __name__ == "__main__":
    unittest.main()
