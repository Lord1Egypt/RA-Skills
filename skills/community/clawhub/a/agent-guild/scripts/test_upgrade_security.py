#!/usr/bin/env python3
"""release 完整性、受限解包与安全交换回归；不联网、不使用真实 HOME。"""
import hashlib
import importlib.util
import io
import json
import os
import stat
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
VERSION = "4.0.0"
API = "https://api.github.com/repos/dqsjqian/agent-guild/releases/tags/v4.0.0"
URL = "https://github.com/dqsjqian/agent-guild/releases/download/v4.0.0/agent-guild-v4.0.0.zip"
NAME = "agent-guild-v4.0.0.zip"


class UpgradeSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ag-upgrade-security-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.central = self.base / "guild"
        self.environment = patch.dict(os.environ, HOME=str(self.base), USERPROFILE=str(self.base),
                                      AGENT_GUILD_DIR=str(self.central), AG_HOST_ID="test-host")
        self.environment.start()
        self.addCleanup(self.environment.stop)
        spec = importlib.util.spec_from_file_location("ag_upgrade_security_test", ROOT / "scripts/ag.py")
        self.ag = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.ag)
        self.files = {
            "agent-guild/SKILL.md": "release skill\n",
            "agent-guild/manifest.json": json.dumps({"name": "agent-guild", "skill_version": VERSION,
                                                     "protocol_version": "4.0"}),
        }
        # 当前完整包的模块清单（新版四模块）；解包校验只强制 payload 自身
        # 声明/静态 import 的模块，多出的文件不构成失败。
        for module in ("ag.py", "ag_tasks.py", "ag_history.py", "ag_retention.py"):
            self.files["agent-guild/scripts/" + module] = "# release module\n"
        for name in self.ag.PROTOCOL_DOCS:
            self.files["agent-guild/references/" + name] = "release protocol\n"
        self.data = self.make_zip()
        self.metadata = {"tag_name": "v4.0.0", "draft": False, "prerelease": False,
                         "assets": [{"name": NAME, "browser_download_url": URL,
                                     "size": len(self.data), "state": "uploaded",
                                     "digest": "sha256:" + hashlib.sha256(self.data).hexdigest()}]}
        self.requests = []

    def make_zip(self, extras=(), compression=zipfile.ZIP_STORED):
        stream = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(stream, "w", compression=compression) as package:
                for name, body in self.files.items():
                    package.writestr(name, body)
                for name, body in extras:
                    package.writestr(name, body)
        return stream.getvalue()

    def response(self, url, limit, timeout=120):
        self.requests.append(url)
        if url == API:
            return json.dumps(self.metadata).encode()
        if url == URL:
            return self.data
        if url == URL + ".sha256" and hasattr(self, "sidecar"):
            return self.sidecar
        self.fail("非预期网络请求: " + url)

    def download(self):
        with patch.object(self.ag, "_release_bytes", side_effect=self.response):
            return self.ag._download_and_apply(VERSION)

    def sidecar_fallback(self, content=None):
        self.metadata["assets"][0].pop("digest", None)
        self.sidecar = content or (hashlib.sha256(self.data).hexdigest() + "  " + NAME + "\n").encode()
        self.metadata["assets"].append({"name": NAME + ".sha256", "size": len(self.sidecar),
                                       "state": "uploaded", "browser_download_url": URL + ".sha256"})

    def seed_old(self):
        old = self.central / "skills/agent-guild"
        old.mkdir(parents=True)
        (old / "manifest.json").write_text(json.dumps({"name": "agent-guild", "skill_version": "3.9.9",
                                                       "protocol_version": "3.9"}), encoding="utf-8")
        (old / "SKILL.md").write_text("old protocol", encoding="utf-8")
        (self.central / "ONBOARDING.md").write_text("old onboarding", encoding="utf-8")
        (self.central / "identity").mkdir()
        (self.central / "identity/profile.md").write_text("private user data", encoding="utf-8")
        return old

    def assert_unchanged(self, old):
        self.assertEqual((old / "SKILL.md").read_text(), "old protocol")
        self.assertEqual((self.central / "ONBOARDING.md").read_text(), "old onboarding")
        self.assertEqual((self.central / "identity/profile.md").read_text(), "private user data")

    def test_valid_digest_installs_preserving_user_data_and_one_code_backup(self):
        old = self.seed_old()
        ok, message = self.download()
        self.assertTrue(ok, message)
        self.assertIn("SHA-256 verified", message)
        self.assertEqual(self.requests, [API, URL])
        self.assertEqual((old / "SKILL.md").read_text(), "release skill\n")
        self.assertEqual((self.central / "identity/profile.md").read_text(), "private user data")
        backup = old.with_name(".agent-guild.previous-code")
        self.assertEqual((backup / "package/SKILL.md").read_text(), "old protocol")
        self.assertTrue(self.download()[0])
        self.assertEqual((backup / "package/SKILL.md").read_text(), "release skill\n")
        self.assertEqual(len(list(self.central.rglob("*.previous-code"))), 1)
        self.assertEqual(list(self.central.rglob(".ag-release-stage-*")), [])
        anchor = self.central / "hosts/test-host/VERSION"
        self.assertIn("skill_version=4.0.0", anchor.read_text())

    def test_valid_sidecar_fallback_is_bound_to_same_release(self):
        self.sidecar_fallback()
        ok, message = self.download()
        self.assertTrue(ok, message)
        self.assertEqual(self.requests, [API, URL + ".sha256", URL])

    def test_missing_digest_and_sidecar_fails_closed(self):
        self.metadata["assets"][0].pop("digest")
        self.assertFalse(self.download()[0])
        self.assertEqual(self.requests, [API])
        self.assertFalse(self.central.exists())

    def test_malformed_digest_never_falls_back(self):
        for value in ("sha256:abc", "sha512:" + "a" * 64, 123):
            with self.subTest(value=value):
                self.metadata["assets"][0]["digest"] = value
                self.assertFalse(self.download()[0])
        self.assertNotIn(URL, self.requests)

    def test_wrong_hash_and_size_preserve_working_install(self):
        old = self.seed_old()
        self.metadata["assets"][0]["digest"] = "sha256:" + "0" * 64
        self.assertFalse(self.download()[0])
        self.assert_unchanged(old)
        self.metadata["assets"][0]["digest"] = "sha256:" + hashlib.sha256(self.data).hexdigest()
        self.metadata["assets"][0]["size"] += 1
        self.assertFalse(self.download()[0])
        self.assert_unchanged(old)

    def test_asset_tag_url_state_size_and_duplicates_are_rejected(self):
        mutations = [
            lambda m: m.update(tag_name="v9.9.9"),
            lambda m: m.update(draft=True),
            lambda m: m.update(prerelease=True),
            lambda m: m["assets"][0].update(browser_download_url=URL.replace("v4.0.0", "v9.9.9")),
            lambda m: m["assets"][0].update(browser_download_url=URL.replace("https:", "http:")),
            lambda m: m["assets"][0].update(state="new"),
            lambda m: m["assets"][0].update(size=65 * 1024 * 1024),
            lambda m: m["assets"].append(dict(m["assets"][0])),
        ]
        original = json.loads(json.dumps(self.metadata))
        for mutate in mutations:
            self.metadata = json.loads(json.dumps(original))
            mutate(self.metadata)
            self.assertFalse(self.download()[0])
        self.assertNotIn(URL, self.requests)

    def test_sidecar_wrong_filename_path_multiple_lines_or_hash_rejected(self):
        digest = hashlib.sha256(self.data).hexdigest()
        invalid = [f"{digest}  other.zip\n", f"{digest}  ../{NAME}\n",
                   f"{digest}  {NAME}\n{digest}  {NAME}\n", f"abc  {NAME}\n", digest]
        for body in invalid:
            with self.subTest(body=body):
                self.metadata["assets"] = self.metadata["assets"][:1]
                self.sidecar_fallback(body.encode())
                self.assertFalse(self.download()[0])
        self.assertNotIn(URL, self.requests)

    def test_sidecar_digest_mismatch_rejected(self):
        self.sidecar_fallback()
        self.metadata["assets"][1]["digest"] = "sha256:" + "0" * 64
        self.assertFalse(self.download()[0])
        self.assertNotIn(URL, self.requests)

    def test_version_injection_rejected_before_network(self):
        with patch.object(self.ag, "_release_bytes") as network:
            for version in ("../4.0.0", "4.0.0?x", "4.0.0/asset", "v4.0.0", "main", "4.0.0\n"):
                self.assertFalse(self.ag._download_and_apply(version)[0])
        network.assert_not_called()

    def test_zip_path_traversal_absolute_alias_collisions_and_devices_rejected(self):
        cases = [
            [("../outside", "bad")], [("/absolute", "bad")], [("C:/evil", "bad")],
            [("agent-guild/../outside", "bad")], [("agent-guild//bad", "bad")],
            [("agent-guild/bad//", "")], [("agent-guild/./bad", "bad")],
            [("agent-guild/scripts\\evil.py", "bad")], [("agent-guild/CON.txt", "bad")],
            [("agent-guild/trailing.", "bad")], [("agent-guild/file:stream", "bad")],
            [("agent-guild/SKILL.md", "duplicate")], [("agent-guild/skill.md", "collision")],
            [("agent-guild/SCRIPTS/bad.py", "collision")],
            [("agent-guild/a", "file"), ("agent-guild/a/b", "child")],
            [("agent-guild/é", "one"), ("agent-guild/e\u0301", "two")],
            [("agent-guild/a/b/c", "deep")],
        ]
        for index, extras in enumerate(cases):
            with self.subTest(extras=extras):
                stage = self.base / str(index)
                stage.mkdir()
                with self.assertRaises(ValueError):
                    self.ag._extract_verified_release(self.make_zip(extras), stage, VERSION)
                self.assertEqual(list(stage.iterdir()), [])
        self.assertFalse((self.base / "outside").exists())

    def test_null_byte_in_raw_zip_filename_rejected(self):
        data = self.make_zip([("agent-guild/aXb", "null")])
        data = data.replace(b"agent-guild/aXb", b"agent-guild/a\x00b")
        with self.assertRaises(ValueError):
            self.ag._extract_verified_release(data, self.base, VERSION)

    def test_symlink_and_special_entries_rejected(self):
        for mode in (stat.S_IFLNK, stat.S_IFIFO, stat.S_IFSOCK):
            info = zipfile.ZipInfo("agent-guild/link")
            info.create_system = 3
            info.external_attr = (mode | 0o777) << 16
            with self.assertRaises(ValueError):
                self.ag._extract_verified_release(self.make_zip([(info, "../../outside")]), self.base, VERSION)

    def test_zip_size_entry_count_and_ratio_bounds(self):
        with patch.object(self.ag, "_UPGRADE_MAX_BYTES", 32):
            with self.assertRaises(ValueError):
                self.ag._extract_verified_release(self.data, self.base, VERSION)
        with patch.object(self.ag, "_UPGRADE_MAX_ENTRIES", 2):
            with self.assertRaises(ValueError):
                self.ag._extract_verified_release(self.data, self.base, VERSION)
        bomb = self.make_zip([("agent-guild/bomb.txt", "0" * 1024 * 1024)], zipfile.ZIP_DEFLATED)
        with self.assertRaises(ValueError):
            self.ag._extract_verified_release(bomb, self.base, VERSION)

    def test_manifest_version_and_required_modules_rejected(self):
        # manifest 版本与 release tag 不匹配必须被拒。
        stage = self.base / "manifest"
        stage.mkdir()
        self.files["agent-guild/manifest.json"] = json.dumps(
            {"name": "agent-guild", "skill_version": "9.9.9", "protocol_version": "4.0"})
        with self.assertRaises(ValueError):
            self.ag._extract_verified_release(self.make_zip(), stage, VERSION)
        # 缺 CLI 本体 ag.py（无条件必需）必须被拒。
        stage = self.base / "cli"
        stage.mkdir()
        self.files.pop("agent-guild/scripts/ag.py")
        with self.assertRaises(ValueError):
            self.ag._extract_verified_release(self.make_zip(), stage, VERSION)

    def test_legacy_three_module_release_installs(self):
        # 真实 v4.0.0 布局：manifest.scripts 只声明 cli（package.sh 未打包），
        # 三模块 ag.py/ag_tasks.py/ag_history.py，ag_history 不 import ag_retention。
        # 完整旧包必须成功安装；package.sh 声明为 shell 不属于运行模块。
        old = self.seed_old()
        self.files = {
            "agent-guild/SKILL.md": "legacy release skill\n",
            "agent-guild/manifest.json": json.dumps({
                "name": "agent-guild", "skill_version": VERSION, "protocol_version": "4.0",
                "scripts": {"cli": "scripts/ag.py", "package": "scripts/package.sh"}}),
            "agent-guild/scripts/ag.py": "import ag_history\nimport ag_tasks\n",
            "agent-guild/scripts/ag_tasks.py": "import ag_history\n",
            "agent-guild/scripts/ag_history.py": "import os\n",
        }
        for name in self.ag.PROTOCOL_DOCS:
            self.files["agent-guild/references/" + name] = "legacy protocol\n"
        self.data = self.make_zip()
        self.metadata = {"tag_name": "v4.0.0", "draft": False, "prerelease": False,
                         "assets": [{"name": NAME, "browser_download_url": URL,
                                     "size": len(self.data), "state": "uploaded",
                                     "digest": "sha256:" + hashlib.sha256(self.data).hexdigest()}]}
        ok, message = self.download()
        self.assertTrue(ok, message)
        self.assertEqual((old / "SKILL.md").read_text(), "legacy release skill\n")
        self.assertFalse((old / "scripts/ag_retention.py").exists())
        self.assertEqual(self.requests, [API, URL])

    def test_release_missing_self_required_modules_rejected(self):
        # 缺"自身必需"模块才失败：manifest 声明的 .py 缺失，或 ag.py /
        # ag_history.py 静态 import 的兄弟模块缺失。
        base = {
            "agent-guild/SKILL.md": "release skill\n",
            "agent-guild/scripts/ag.py": "import ag_history\n",
            "agent-guild/scripts/ag_history.py": "import ag_retention\n",
        }
        for name in self.ag.PROTOCOL_DOCS:
            base["agent-guild/references/" + name] = "release protocol\n"
        cases = {
            "declared-script-missing": {
                "agent-guild/manifest.json": json.dumps({
                    "name": "agent-guild", "skill_version": VERSION, "protocol_version": "4.0",
                    "scripts": {"retention": "scripts/ag_retention.py"}}),
                "agent-guild/scripts/ag_history.py": "import os\n",
            },
            "ag.py-import-missing": {
                "agent-guild/manifest.json": json.dumps({"name": "agent-guild", "skill_version": VERSION,
                                                         "protocol_version": "4.0"}),
            },
            "ag_history-import-missing": {
                "agent-guild/manifest.json": json.dumps({"name": "agent-guild", "skill_version": VERSION,
                                                         "protocol_version": "4.0"}),
                "agent-guild/scripts/ag.py": "import ag_history\nimport ag_tasks\n",
            },
        }
        for label, overrides in cases.items():
            with self.subTest(case=label):
                stage = self.base / label
                stage.mkdir()
                files = dict(base)
                files.update(overrides)
                self.files = files
                with self.assertRaises(ValueError):
                    self.ag._extract_verified_release(self.make_zip(), stage, VERSION)
                self.assertEqual(list(stage.iterdir()), [])

    def test_swap_failure_restores_old_code_without_touching_user_data(self):
        old = self.seed_old()
        original = self.ag.os.replace
        triggered = []

        def fail_new_package(src, dst):
            if Path(dst) == old and ".ag-release-stage-" in str(src) and not triggered:
                triggered.append(True)
                raise OSError("simulated rename failure")
            return original(src, dst)

        with patch.object(self.ag.os, "replace", side_effect=fail_new_package):
            ok, message = self.download()
        self.assertFalse(ok)
        self.assertIn("simulated rename failure", message)
        self.assert_unchanged(old)
        self.assertEqual(list(self.central.rglob(".ag-release-stage-*")), [])

    def test_downgrade_is_rejected_inside_install_lock(self):
        old = self.seed_old()
        (old / "manifest.json").write_text(json.dumps({"name": "agent-guild", "skill_version": "9.0.0",
                                                       "protocol_version": "9.0"}), encoding="utf-8")
        self.assertFalse(self.download()[0])
        self.assert_unchanged(old)
        self.assertFalse(old.with_name(".agent-guild.previous-code").exists())

    def test_interrupted_backup_does_not_allow_downgrade(self):
        old = self.seed_old()
        (old / "manifest.json").write_text(json.dumps({"name": "agent-guild", "skill_version": "9.0.0",
                                                       "protocol_version": "9.0"}), encoding="utf-8")
        backup = old.with_name(".agent-guild.previous-code")
        backup.mkdir()
        (backup / "OWNER").write_text("Agent Guild protocol code backup v1\n", encoding="utf-8")
        old.rename(backup / "package")
        self.assertFalse(self.download()[0])
        self.assert_unchanged(old)

    def test_doc_write_failure_restores_code_and_previous_docs(self):
        old = self.seed_old()
        original = self.ag._atomic_write_text

        def fail_second_document(path, text):
            if path.name == "CONVENTIONS.md":
                raise OSError("simulated doc failure")
            return original(path, text)

        with patch.object(self.ag, "_atomic_write_text", side_effect=fail_second_document):
            self.assertFalse(self.download()[0])
        self.assert_unchanged(old)

    def test_unknown_backup_is_never_deleted(self):
        old = self.seed_old()
        backup = old.with_name(".agent-guild.previous-code")
        backup.mkdir()
        payload = backup / "private.txt"
        payload.write_text("must preserve", encoding="utf-8")
        self.assertFalse(self.download()[0])
        self.assertEqual(payload.read_text(), "must preserve")
        self.assert_unchanged(old)

    def test_interrupted_swap_recovers_managed_backup(self):
        old = self.seed_old()
        backup = old.with_name(".agent-guild.previous-code")
        backup.mkdir()
        (backup / "OWNER").write_text("Agent Guild protocol code backup v1\n", encoding="utf-8")
        old.rename(backup / "package")
        self.assertTrue(self.download()[0])
        self.assertEqual((old / "SKILL.md").read_text(), "release skill\n")
        self.assertEqual((backup / "package/SKILL.md").read_text(), "old protocol")

    def test_symlink_code_or_document_target_is_rejected(self):
        for name in ("skills", "ONBOARDING.md"):
            with self.subTest(name=name):
                self.central.mkdir(exist_ok=True)
                target = self.base / ("outside-" + name.replace(".", "-"))
                if name == "skills":
                    target.mkdir()
                else:
                    target.write_text("outside", encoding="utf-8")
                link = self.central / name
                link.symlink_to(target, target_is_directory=target.is_dir())
                self.assertFalse(self.download()[0])
                if target.is_file():
                    self.assertEqual(target.read_text(), "outside")
                else:
                    self.assertEqual(list(target.iterdir()), [])
                link.unlink()

    def test_https_origin_and_redirects_are_validated_before_download(self):
        for url in ("http://github.com/test", "https://evil.invalid/test",
                    "file:///etc/passwd", "https://user:pass@github.com/test"):
            with self.assertRaises(ValueError):
                self.ag._release_bytes(url, 100)

        def opener(handler):
            handler = handler()
            with self.assertRaises(ValueError):
                handler.redirect_request(None, None, 302, "redirect", {}, "http://github.com/test")
            with self.assertRaises(ValueError):
                handler.redirect_request(None, None, 302, "redirect", {}, "https://evil.invalid/test")
            raise OSError("network intentionally disabled")

        with patch.object(self.ag.urllib.request, "build_opener", side_effect=opener):
            with self.assertRaises(OSError):
                self.ag._release_bytes(API, 100)

    def test_http_download_is_size_bounded(self):
        class Response(io.BytesIO):
            def geturl(self):
                return API

        class Opener:
            def open(self, request, timeout):
                return Response(b"x" * 33)

        with patch.object(self.ag.urllib.request, "build_opener", return_value=Opener()):
            with self.assertRaises(ValueError):
                self.ag._release_bytes(API, 32)


if __name__ == "__main__":
    unittest.main()
