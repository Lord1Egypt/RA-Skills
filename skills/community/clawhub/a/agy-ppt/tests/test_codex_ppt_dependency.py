#!/usr/bin/env python3
"""Deterministic tests for the codex-ppt external dependency resolver.

agy-ppt is a standalone repository. ``skills/codex-ppt/`` is not vendored, not
a Git submodule, and not copied into this repository, the Global AGY Skill
install location, or any presentation workspace. Anything that needs the
upstream skill implementation at runtime resolves it through
``scripts/codex_ppt_dependency.py`` -- the single dependency-resolver
authority -- which caches a shallow clone in an OS application-cache
location, external to all three of those locations.

None of these tests use the real GitHub network. Every "upstream" is a
temporary local Git repository created by this test module; the real
``UPSTREAM_URL`` constant is never dereferenced here.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import codex_ppt_dependency as dep  # noqa: E402


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(  # noqa: S603 - fixed "git" executable, test-only local repo
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
    )


def make_local_upstream(root: Path, *, branch: str = "main") -> Path:
    """A tiny local Git repository standing in for the real upstream."""
    repo = root / "fake_upstream"
    repo.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q", "-b", branch, "."], cwd=repo)
    _git(["config", "user.email", "test@example.invalid"], cwd=repo)
    _git(["config", "user.name", "Test"], cwd=repo)
    skill_dir = repo / dep.UPSTREAM_SKILL_SUBDIR
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: codex-ppt\ndescription: fake upstream for tests\n---\n# Fake\n",
        encoding="utf-8",
    )
    (repo / "README.md").write_text("fake upstream\n", encoding="utf-8")
    _git(["add", "-A"], cwd=repo)
    _git(["commit", "-q", "-m", "initial"], cwd=repo)
    return repo


def commit_new_change(repo: Path, marker: str) -> str:
    (repo / dep.UPSTREAM_SKILL_SUBDIR / "CHANGE.md").write_text(marker, encoding="utf-8")
    _git(["add", "-A"], cwd=repo)
    _git(["commit", "-q", "-m", f"change: {marker}"], cwd=repo)
    result = _git(["rev-parse", "HEAD"], cwd=repo)
    return result.stdout.strip()


def head_commit(repo: Path) -> str:
    return _git(["rev-parse", "HEAD"], cwd=repo).stdout.strip()


class DependencyResolverTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.upstream = make_local_upstream(self.root)
        self.cache_root = self.root / "cache"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def resolve(self, **kwargs):
        kwargs.setdefault("upstream_url", str(self.upstream))
        kwargs.setdefault("cache_root", self.cache_root)
        return dep.resolve_codex_ppt_dependency(**kwargs)


# -- Test 1: cache missing, fake/local upstream available ---------------------
class Test1FirstResolutionFetchesOutsideRepo(DependencyResolverTestCase):
    def test_dependency_fetched_and_resolved_outside_repo(self):
        self.assertFalse(self.cache_root.exists())
        resolved = self.resolve()

        self.assertEqual(resolved.source, "cache_updated")
        self.assertTrue(resolved.skill_root.is_dir())
        self.assertTrue((resolved.skill_root / "SKILL.md").is_file())
        self.assertIsNotNone(resolved.metadata)
        self.assertEqual(resolved.metadata.resolved_commit, head_commit(self.upstream))

        repo_root = Path(__file__).resolve().parents[3]
        global_skill_root = Path.home() / ".gemini" / "config" / "skills" / "agy-ppt"
        self.assertNotIn(str(repo_root), str(resolved.root.resolve()))
        self.assertNotIn(str(global_skill_root), str(resolved.root.resolve()))


# -- Test 2: cache current -> no unnecessary destructive update ---------------
class Test2CacheCurrentNoUnnecessaryUpdate(DependencyResolverTestCase):
    def test_second_resolution_reuses_cache_without_recloning(self):
        first = self.resolve()
        marker_file = first.skill_root / "SKILL.md"
        original_mtime = marker_file.stat().st_mtime

        second = self.resolve()

        self.assertEqual(second.source, "cache_hit")
        self.assertEqual(second.metadata.resolved_commit, first.metadata.resolved_commit)
        # The checkout was not touched: file identity/mtime is unchanged.
        self.assertEqual(marker_file.stat().st_mtime, original_mtime)


# -- Test 3: upstream newer -> cache updates, resolved commit changes ---------
class Test3UpstreamNewerUpdatesCache(DependencyResolverTestCase):
    def test_upstream_change_triggers_cache_update(self):
        first = self.resolve()
        first_commit = first.metadata.resolved_commit

        new_commit = commit_new_change(self.upstream, "hello from upstream update")
        self.assertNotEqual(new_commit, first_commit)

        second = self.resolve()

        self.assertEqual(second.source, "cache_updated")
        self.assertEqual(second.metadata.resolved_commit, new_commit)
        self.assertTrue((second.skill_root / "CHANGE.md").is_file())


# -- Test 4: upstream unavailable + cache exists -> cached dependency reused --
class Test4OfflineWithCacheReusesCache(DependencyResolverTestCase):
    def test_offline_with_existing_cache_warns_and_reuses(self):
        first = self.resolve()
        cached_commit = first.metadata.resolved_commit

        with mock.patch.object(dep, "remote_head_commit", return_value=None):
            resolved = self.resolve()

        self.assertEqual(resolved.source, "cache_stale_offline")
        self.assertEqual(resolved.metadata.resolved_commit, cached_commit)
        self.assertTrue(resolved.warnings)
        self.assertIn(cached_commit, resolved.warnings[0])
        self.assertIn("Unable to check/fetch latest upstream revision", resolved.warnings[0])
        # Must never call itself an API fallback.
        for warning in resolved.warnings:
            self.assertNotIn("API fallback", warning)


# -- Test 5: upstream unavailable + no cache -> deterministic error ----------
class Test5OfflineWithoutCacheRaisesDeterministicError(DependencyResolverTestCase):
    def test_offline_without_cache_raises_dependency_unavailable(self):
        self.assertFalse(self.cache_root.exists())
        with mock.patch.object(dep, "remote_head_commit", return_value=None):
            with self.assertRaises(dep.CodexPptDependencyError) as ctx:
                self.resolve()
        self.assertEqual(ctx.exception.error_code, dep.ERROR_DEPENDENCY_UNAVAILABLE)
        # This must never be spelled/handled as an image-generation failure.
        self.assertNotIn("IMAGE_GENERATION_FAILED", str(ctx.exception))
        self.assertNotEqual(ctx.exception.error_code, "IMAGE_GENERATION_FAILED")


# -- Test 6/7: dependency path never enters engineering repo or Global Skill --
class Test6And7DependencyPathNeverEntersOwnedLocations(DependencyResolverTestCase):
    def test_dependency_path_does_not_enter_engineering_repo(self):
        resolved = self.resolve()
        repo_root = Path(__file__).resolve().parents[3]
        self.assertNotIn(str(repo_root), str(resolved.root.resolve()))
        self.assertNotIn(str(repo_root), str(resolved.skill_root.resolve()))

    def test_dependency_path_does_not_enter_global_agy_skill(self):
        resolved = self.resolve()
        for candidate in (
            Path.home() / ".gemini" / "config" / "skills" / "agy-ppt",
            Path.home() / ".agents" / "skills" / "agy-ppt",
        ):
            self.assertNotIn(str(candidate), str(resolved.root.resolve()))

    def test_default_cache_root_is_never_inside_a_repo_relative_path(self):
        cache = dep.default_cache_root()
        self.assertTrue(cache.is_absolute())
        self.assertNotIn("skills", cache.parts)


# -- Test 8: dependency resolver never uses an API-key fallback --------------
class Test8NoApiKeyFallback(DependencyResolverTestCase):
    def test_resolution_does_not_read_api_key_env_vars(self):
        blocked_vars = (
            "OPENAI_API_KEY",
            "CODEX_API_KEY",
            "KIRO_API_KEY",
            "GEMINI_API_KEY",
        )
        # Make sure they are set to sentinel values that would be an obvious
        # failure if this module ever read or forwarded them.
        with mock.patch.dict(
            "os.environ", {name: "sentinel-should-not-be-read" for name in blocked_vars}
        ):
            resolved = self.resolve()
        self.assertTrue((resolved.skill_root / "SKILL.md").is_file())

    def test_module_never_reads_api_key_env_vars_at_runtime(self):
        # The module documents, in prose, which env vars it deliberately does
        # NOT read (see the module docstring) -- that mention is intentional.
        # What must never exist is an *executable* os.environ/os.getenv access
        # to any of these names.
        import ast

        source = Path(dep.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        blocked = {"OPENAI_API_KEY", "CODEX_API_KEY", "KIRO_API_KEY", "GEMINI_API_KEY"}
        offending: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                is_environ_get = (
                    isinstance(func, ast.Attribute)
                    and func.attr in ("get", "getenv")
                )
                is_getenv = isinstance(func, ast.Name) and func.id == "getenv"
                if not (is_environ_get or is_getenv):
                    continue
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and arg.value in blocked:
                        offending.append(str(arg.value))
            if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant):
                if node.slice.value in blocked:
                    offending.append(str(node.slice.value))

        self.assertEqual(offending, [])

    def test_git_ls_remote_uses_no_auth_header(self):
        # A plain "git ls-remote <url> <ref>" call, nothing else.
        with mock.patch.object(dep, "_run_git") as fake_run:
            fake_run.return_value = subprocess.CompletedProcess(
                args=[], returncode=0, stdout=f"{head_commit(self.upstream)}\trefs/heads/main\n", stderr=""
            )
            dep.remote_head_commit(str(self.upstream), "main")
            called_args = fake_run.call_args[0][0]
        self.assertEqual(called_args[0], "ls-remote")
        joined = " ".join(called_args)
        self.assertNotIn("Authorization", joined)
        self.assertNotIn("Bearer", joined)


# -- Test 9: explicit development override ------------------------------------
class Test9LocalOverrideUsesProvidedPathWithoutCopying(DependencyResolverTestCase):
    def test_override_pointing_at_full_checkout_is_used_directly(self):
        resolved = self.resolve(local_override=str(self.upstream))
        self.assertEqual(resolved.source, "local_override")
        self.assertEqual(resolved.skill_root, self.upstream / dep.UPSTREAM_SKILL_SUBDIR)
        # No copy was made: the cache directory was never created.
        self.assertFalse(self.cache_root.exists())

    def test_override_pointing_directly_at_skill_dir_is_used_directly(self):
        skill_dir = self.upstream / dep.UPSTREAM_SKILL_SUBDIR
        resolved = self.resolve(local_override=str(skill_dir))
        self.assertEqual(resolved.source, "local_override")
        self.assertEqual(resolved.skill_root, skill_dir)
        self.assertFalse(self.cache_root.exists())

    def test_override_via_environment_variable(self):
        with mock.patch.dict("os.environ", {dep.LOCAL_OVERRIDE_ENV_VAR: str(self.upstream)}):
            resolved = dep.resolve_codex_ppt_dependency(cache_root=self.cache_root)
        self.assertEqual(resolved.source, "local_override")
        self.assertFalse(self.cache_root.exists())

    def test_invalid_override_path_raises_clear_error(self):
        with self.assertRaises(dep.CodexPptDependencyError) as ctx:
            self.resolve(local_override="/definitely/does/not/exist/anywhere")
        self.assertEqual(ctx.exception.error_code, dep.ERROR_INVALID_OVERRIDE)


# -- Additional hardening: atomic update / metadata hygiene -------------------
class AtomicUpdateAndMetadataHygieneTests(DependencyResolverTestCase):
    def test_failed_update_does_not_destroy_a_working_cache(self):
        first = self.resolve()
        good_commit = first.metadata.resolved_commit

        commit_new_change(self.upstream, "this update will be interrupted")

        with mock.patch.object(
            dep, "_validate_checkout", side_effect=dep.CodexPptDependencyError("boom", "CODEX_PPT_DEPENDENCY_CORRUPT")
        ):
            with self.assertRaises(dep.CodexPptDependencyError):
                self.resolve()

        # The previously-good cache must still be intact and usable.
        with mock.patch.object(dep, "remote_head_commit", return_value=good_commit):
            recovered = self.resolve()
        self.assertEqual(recovered.source, "cache_hit")
        self.assertEqual(recovered.metadata.resolved_commit, good_commit)
        self.assertTrue((recovered.skill_root / "SKILL.md").is_file())

    def test_metadata_file_lives_beside_cache_not_inside_git_checkout(self):
        resolved = self.resolve()
        metadata_path = self.cache_root / dep.METADATA_FILENAME
        self.assertTrue(metadata_path.is_file())
        self.assertFalse((resolved.root / dep.METADATA_FILENAME).exists())

    def test_metadata_contains_only_the_minimal_fields(self):
        self.resolve()
        payload = json.loads((self.cache_root / dep.METADATA_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(
            set(payload.keys()), {"upstream_url", "upstream_branch", "resolved_commit", "resolved_at"}
        )
        for forbidden in ("token", "credential", "cookie", "password", "secret", "auth"):
            for key in payload:
                self.assertNotIn(forbidden, key.lower())

    def test_upstream_url_constant_is_the_trusted_https_github_url(self):
        self.assertEqual(dep.UPSTREAM_URL, "https://github.com/ningzimu/codex-ppt-skill.git")

    def test_default_branch_is_main_not_a_hardcoded_tag(self):
        self.assertEqual(dep.UPSTREAM_DEFAULT_BRANCH, "main")


if __name__ == "__main__":
    unittest.main()
