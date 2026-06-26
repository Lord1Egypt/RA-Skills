import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "skill_updater.py"
SPEC = importlib.util.spec_from_file_location("skill_updater", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def git(args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True)


def git_output(args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


class GitSourceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tempdir.name)
        self.remote = self.root / "remote.git"
        self.seed = self.root / "seed"
        self.skill = self.root / "workspace" / ".agents" / "skills" / "demo-skill"
        self.skill.parent.mkdir(parents=True)

        git(["init", "--bare", str(self.remote)], cwd=self.root)
        git(["clone", str(self.remote), str(self.seed)], cwd=self.root)
        git(["config", "user.name", "Test User"], cwd=self.seed)
        git(["config", "user.email", "test@example.com"], cwd=self.seed)
        (self.seed / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
        git(["add", "SKILL.md"], cwd=self.seed)
        git(["commit", "-m", "init"], cwd=self.seed)
        git(["push", "-u", "origin", "main"], cwd=self.seed)
        git(["clone", str(self.remote), str(self.skill)], cwd=self.root)

    def tearDown(self):
        self.tempdir.cleanup()

    def make_remote_commit(self, message="update"):
        (self.seed / "SKILL.md").write_text(f"# {message}\n", encoding="utf-8")
        git(["add", "SKILL.md"], cwd=self.seed)
        git(["commit", "-m", message], cwd=self.seed)
        git(["push"], cwd=self.seed)

    def test_git_skill_reports_update_available(self):
        self.make_remote_commit("branch-update")

        report = MODULE.inspect_git_skill(self.skill)

        self.assertEqual(report.status, "update-available")
        self.assertEqual(report.source_type, "git")
        self.assertEqual(report.skill_name, "demo-skill")
        self.assertGreater(report.meta["behind_count"], 0)

    def test_git_skill_update_fast_forwards(self):
        self.make_remote_commit("branch-update")

        report = MODULE.update_git_skill(self.skill)

        self.assertEqual(report.status, "updated")
        self.assertEqual(
            git_output(["rev-parse", "HEAD"], cwd=self.skill),
            git_output(["rev-parse", "origin/main"], cwd=self.skill),
        )

    def test_git_skill_skips_dirty_repo(self):
        self.make_remote_commit("dirty-update")
        (self.skill / "local.txt").write_text("dirty\n", encoding="utf-8")

        report = MODULE.update_git_skill(self.skill)

        self.assertEqual(report.status, "dirty")

    def test_git_skill_uses_tag_strategy(self):
        git(["tag", "v1.0.0"], cwd=self.seed)
        git(["push", "origin", "v1.0.0"], cwd=self.seed)
        self.make_remote_commit("release-update")
        git(["tag", "v1.1.0"], cwd=self.seed)
        git(["push", "origin", "v1.1.0"], cwd=self.seed)
        git(["fetch", "--tags", "origin"], cwd=self.skill)
        git(["checkout", "v1.0.0"], cwd=self.skill)

        report = MODULE.inspect_git_skill(self.skill)

        self.assertEqual(report.status, "update-available")
        self.assertEqual(report.current_ref_or_hash, "v1.0.0")
        self.assertEqual(report.latest_ref_or_hash, "v1.1.0")

    def test_git_skill_reports_ahead(self):
        (self.skill / "LOCAL.md").write_text("local\n", encoding="utf-8")
        git(["add", "LOCAL.md"], cwd=self.skill)
        git(["config", "user.name", "Local User"], cwd=self.skill)
        git(["config", "user.email", "local@example.com"], cwd=self.skill)
        git(["commit", "-m", "local"], cwd=self.skill)

        report = MODULE.inspect_git_skill(self.skill)

        self.assertEqual(report.status, "ahead")

    def test_git_skill_reports_diverged(self):
        self.make_remote_commit("remote")
        (self.skill / "LOCAL.md").write_text("local\n", encoding="utf-8")
        git(["add", "LOCAL.md"], cwd=self.skill)
        git(["config", "user.name", "Local User"], cwd=self.skill)
        git(["config", "user.email", "local@example.com"], cwd=self.skill)
        git(["commit", "-m", "local"], cwd=self.skill)

        report = MODULE.inspect_git_skill(self.skill)

        self.assertEqual(report.status, "diverged")

    def test_git_skill_without_origin_is_unsupported(self):
        git(["remote", "remove", "origin"], cwd=self.skill)

        report = MODULE.inspect_git_skill(self.skill)

        self.assertEqual(report.status, "unsupported")


class LockfileSourceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tempdir.name)
        self.source_repo = self.root / "impeccable"
        self.provider_root = self.root / ".agents"
        self.skills_root = self.provider_root / "skills"
        self.skills_root.mkdir(parents=True)

        git(["init", "-b", "main", str(self.source_repo)], cwd=self.root)
        git(["config", "user.name", "Test User"], cwd=self.source_repo)
        git(["config", "user.email", "test@example.com"], cwd=self.source_repo)

        self.remote_skill_dir = self.source_repo / ".agents" / "skills" / "adapt"
        self.remote_skill_dir.mkdir(parents=True)
        (self.remote_skill_dir / "SKILL.md").write_text("# Adapt v1\n", encoding="utf-8")
        git(["add", ".agents/skills/adapt/SKILL.md"], cwd=self.source_repo)
        git(["commit", "-m", "init"], cwd=self.source_repo)

        self.local_skill_dir = self.skills_root / "adapt"
        self.local_skill_dir.mkdir(parents=True)
        (self.local_skill_dir / "SKILL.md").write_text("# Adapt v1\n", encoding="utf-8")

        self.lock_path = self.provider_root / ".skill-lock.json"
        self.write_lock()

    def tearDown(self):
        self.tempdir.cleanup()

    def write_lock(self):
        tree_hash = git_output(["rev-parse", "HEAD:.agents/skills/adapt"], cwd=self.source_repo)
        payload = {
            "version": 3,
            "skills": {
                "adapt": {
                    "source": "pbakaus/impeccable",
                    "sourceType": "github",
                    "sourceUrl": str(self.source_repo),
                    "skillPath": ".agents/skills/adapt/SKILL.md",
                    "skillFolderHash": tree_hash,
                    "installedAt": "2026-03-28T00:00:00Z",
                    "updatedAt": "2026-03-28T00:00:00Z",
                }
            },
        }
        self.lock_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def make_remote_update(self):
        (self.remote_skill_dir / "SKILL.md").write_text("# Adapt v2\n", encoding="utf-8")
        git(["add", ".agents/skills/adapt/SKILL.md"], cwd=self.source_repo)
        git(["commit", "-m", "update"], cwd=self.source_repo)

    def test_lockfile_source_reports_up_to_date(self):
        reports = MODULE.inspect_lockfile_provider(self.provider_root)

        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].status, "up-to-date")
        self.assertEqual(reports[0].source_type, "lockfile")

    def test_lockfile_source_reports_update_available(self):
        self.make_remote_update()

        reports = MODULE.inspect_lockfile_provider(self.provider_root)

        self.assertEqual(reports[0].status, "update-available")

    def test_lockfile_source_skips_modified_local_skill(self):
        self.make_remote_update()
        (self.local_skill_dir / "SKILL.md").write_text("# local edit\n", encoding="utf-8")

        reports = MODULE.inspect_lockfile_provider(self.provider_root)

        self.assertEqual(reports[0].status, "modified-locally")

    def test_lockfile_source_updates_skill_and_lockfile(self):
        self.make_remote_update()

        reports = MODULE.update_lockfile_provider(self.provider_root)

        self.assertEqual(reports[0].status, "updated")
        self.assertEqual((self.local_skill_dir / "SKILL.md").read_text(encoding="utf-8"), "# Adapt v2\n")
        lock = json.loads(self.lock_path.read_text(encoding="utf-8"))
        self.assertEqual(
            lock["skills"]["adapt"]["skillFolderHash"],
            git_output(["rev-parse", "HEAD:.agents/skills/adapt"], cwd=self.source_repo),
        )
        backup_path = pathlib.Path(reports[0].message.split("备份位于 ", 1)[1].rstrip("。"))
        self.assertTrue(backup_path.exists())

    def test_lockfile_source_reports_missing_source(self):
        shutil_target = self.source_repo / ".agents" / "skills" / "adapt"
        for file_path in sorted(shutil_target.rglob("*"), reverse=True):
            if file_path.is_file():
                file_path.unlink()
        shutil_target.rmdir()
        git(["add", "-A"], cwd=self.source_repo)
        git(["commit", "-m", "remove adapt"], cwd=self.source_repo)

        reports = MODULE.inspect_lockfile_provider(self.provider_root)

        self.assertEqual(reports[0].status, "missing-source")

    def test_lockfile_source_reports_lock_invalid(self):
        lock = json.loads(self.lock_path.read_text(encoding="utf-8"))
        del lock["skills"]["adapt"]["sourceUrl"]
        self.lock_path.write_text(json.dumps(lock, indent=2), encoding="utf-8")

        reports = MODULE.inspect_lockfile_provider(self.provider_root)

        self.assertEqual(reports[0].status, "lock-invalid")

    def test_lockfile_source_reports_missing_local_skill(self):
        shutil_target = self.local_skill_dir
        for file_path in sorted(shutil_target.rglob("*"), reverse=True):
            if file_path.is_file():
                file_path.unlink()
        shutil_target.rmdir()

        reports = MODULE.inspect_lockfile_provider(self.provider_root)

        self.assertEqual(reports[0].status, "missing-local-skill")


class ScanTests(unittest.TestCase):
    def test_default_provider_roots_include_project_and_home(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            workspace = root / "workspace"
            home = root / "home"
            (workspace / ".claude" / "skills").mkdir(parents=True)
            (home / ".agents" / "skills").mkdir(parents=True)
            (home / ".openclaw" / "skills").mkdir(parents=True)
            (home / ".openclaw" / "workspace" / "skills").mkdir(parents=True)

            roots = MODULE.default_provider_roots(workspace_root=workspace, home_root=home)

            self.assertIn((workspace / ".claude").resolve(), roots)
            self.assertIn((home / ".agents").resolve(), roots)
            self.assertIn((home / ".openclaw").resolve(), roots)
            self.assertIn((home / ".openclaw" / "workspace").resolve(), roots)
            self.assertEqual(len(roots), len(set(roots)))

    def test_infer_provider_root_handles_openclaw_workspace(self):
        skill_path = pathlib.Path("/tmp/demo/.openclaw/workspace/skills/demo-skill/SKILL.md")

        provider_root = MODULE.infer_provider_root(skill_path)

        self.assertEqual(provider_root, pathlib.Path("/tmp/demo/.openclaw/workspace"))

    def test_collect_reports_honors_source_filter(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source_repo = root / "source"
            provider = root / ".agents"
            local_skill = provider / "skills" / "adapt"
            local_skill.mkdir(parents=True)
            git(["init", "-b", "main", str(source_repo)], cwd=root)
            git(["config", "user.name", "Test User"], cwd=source_repo)
            git(["config", "user.email", "test@example.com"], cwd=source_repo)
            remote_skill = source_repo / ".agents" / "skills" / "adapt"
            remote_skill.mkdir(parents=True)
            (remote_skill / "SKILL.md").write_text("# Adapt\n", encoding="utf-8")
            git(["add", ".agents/skills/adapt/SKILL.md"], cwd=source_repo)
            git(["commit", "-m", "init"], cwd=source_repo)
            (local_skill / "SKILL.md").write_text("# Adapt\n", encoding="utf-8")
            tree_hash = git_output(["rev-parse", "HEAD:.agents/skills/adapt"], cwd=source_repo)
            lock = {
                "version": 3,
                "skills": {
                    "adapt": {
                        "source": "pbakaus/impeccable",
                        "sourceType": "github",
                        "sourceUrl": str(source_repo),
                        "skillPath": ".agents/skills/adapt/SKILL.md",
                        "skillFolderHash": tree_hash,
                        "installedAt": "2026-03-28T00:00:00Z",
                        "updatedAt": "2026-03-28T00:00:00Z",
                    }
                },
            }
            (provider / ".skill-lock.json").write_text(json.dumps(lock, indent=2), encoding="utf-8")
            with tempfile.TemporaryDirectory() as cache:
                reports = MODULE.collect_reports("check", [provider], source_filters=["pbakaus/impeccable"], cache_root=pathlib.Path(cache))
            self.assertEqual(len(reports), 1)
            self.assertEqual(reports[0].skill_name, "adapt")


if __name__ == "__main__":
    unittest.main()
