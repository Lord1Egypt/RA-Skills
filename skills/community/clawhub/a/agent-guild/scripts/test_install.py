#!/usr/bin/env python3
"""安装器离线回归：临时 HOME，只有 HTTPS 下载被测试夹具替代。"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")


@unittest.skipUnless(shutil.which("bash"), "需要 bash 测试 shell 安装器")
class ShellInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ag-install-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.central = self.home / ".agent-guild"
        self.repo = self.base / "repo"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".DS_Store"))
        self.mock = self.base / "mock"
        self.mock.mkdir()
        self.version = json.loads((self.repo / "manifest.json").read_text())["skill_version"]
        self.tag = "v" + self.version
        (self.mock / "sitecustomize.py").write_text('''
import io
import os
import urllib.request
from pathlib import Path

TAG = os.environ["MOCK_RELEASE_TAG"]

class Response(io.BytesIO):
    def __init__(self, content, url):
        super().__init__(content)
        self.url = url
    def geturl(self):
        return self.url

class Opener:
    def open(self, request, timeout=None):
        url = request.full_url
        if url == "https://api.github.com/repos/dqsjqian/agent-guild/releases/tags/" + TAG:
            name = "release.json"
        elif url == "https://github.com/dqsjqian/agent-guild/releases/download/" + TAG + "/agent-guild-" + TAG + ".zip":
            name = "agent-guild-" + TAG + ".zip"
        elif url == "https://github.com/dqsjqian/agent-guild/releases/download/" + TAG + "/agent-guild-" + TAG + ".zip.sha256":
            name = "agent-guild-" + TAG + ".zip.sha256"
        else:
            raise OSError("unexpected URL: " + url)
        if name == os.environ.get("MOCK_DOWNLOAD_FAIL"):
            raise OSError("simulated transfer failure")
        return Response((Path(os.environ["MOCK_RELEASE"]) / name).read_bytes(), url)

urllib.request.build_opener = lambda *args, **kwargs: Opener()
''', encoding="utf-8")
        self.env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home),
                        AGENT_GUILD_DIR=str(self.central), AGENT_GUILD_PYTHON=sys.executable,
                        AGENT_GUILD_VERSION=self.version, AG_HOST_ID="install-test",
                        PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(self.mock),
                        MOCK_RELEASE=str(self.mock), MOCK_RELEASE_TAG=self.tag)
        self.build_release()

    def build_release(self):
        archive = self.mock / ("agent-guild-" + self.tag + ".zip")
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
            for name in ("SKILL.md", "manifest.json", "README.md", "README_EN.md"):
                package.write(self.repo / name, "agent-guild/" + name)
            for folder in ("scripts", "references"):
                for path in sorted((self.repo / folder).iterdir()):
                    if path.is_file() and not path.name.endswith((".pyc", ".pyo")):
                        package.write(path, "agent-guild/" + folder + "/" + path.name)
        data = archive.read_bytes()
        (self.mock / (archive.name + ".sha256")).write_text(
            hashlib.sha256(data).hexdigest() + "  " + archive.name + "\n", encoding="utf-8")
        asset = {"name": archive.name, "size": len(data), "state": "uploaded",
                 "browser_download_url": "https://github.com/dqsjqian/agent-guild/releases/download/"
                                         + self.tag + "/" + archive.name,
                 "digest": "sha256:" + hashlib.sha256(data).hexdigest()}
        (self.mock / "release.json").write_text(json.dumps({
            "tag_name": self.tag, "draft": False, "prerelease": False, "assets": [asset]}),
            encoding="utf-8")

    def install(self, fail=None):
        env = dict(self.env)
        if fail:
            env["MOCK_DOWNLOAD_FAIL"] = fail
        return subprocess.run(["bash", str(self.repo / "scripts/install.sh")],
                              env=env, capture_output=True, text=True)

    def assertInstalled(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Read ~/.agent-guild/ONBOARDING.md", result.stdout)
        self.assertTrue((self.central / "ONBOARDING.md").is_file())
        package = self.central / "skills/agent-guild"
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        for reference in set(re.findall(r"references/[\w.-]+\.md", skill)):
            self.assertTrue((package / reference).is_file(), reference)
        for module in ("ag.py", "ag_tasks.py", "ag_history.py", "ag_retention.py"):
            self.assertTrue((package / "scripts" / module).is_file(), module)
        self.assertTrue((self.central / "handoff/active").is_dir())
        self.assertTrue((self.central / "messages/inbox").is_dir())
        self.assertFalse((self.central / "handoff/shared-state/current-focus.md").exists())
        for name in ("README.md", "README_EN.md", "references/dsh.md"):
            document = package / name
            for link in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if "://" in link:
                    continue
                target = link.split("#", 1)[0]
                if target:
                    self.assertTrue((document.parent / target).is_file(), f"{name}: {link}")
        registry = (self.central / "registry.json").read_text(encoding="utf-8")
        self.assertIsInstance(json.loads(registry)["agents"], dict)

    def test_fresh_install_contains_runtime_and_referenced_docs(self):
        self.assertInstalled(self.install())

    def test_reinstall_refreshes_protocol_and_preserves_user_files(self):
        self.assertInstalled(self.install())
        profile = self.central / "identity/profile.md"
        registry = self.central / "registry.json"
        profile.write_text("my profile\n", encoding="utf-8")
        registry.write_text('{"agents":{"my-agent":{}}}\n', encoding="utf-8")
        source = self.repo / "references/ONBOARDING.md"
        source.write_text("new protocol instructions\n", encoding="utf-8")
        self.build_release()
        self.assertInstalled(self.install())
        self.assertEqual(profile.read_text(encoding="utf-8"), "my profile\n")
        self.assertEqual(registry.read_text(encoding="utf-8"), '{"agents":{"my-agent":{}}}\n')
        self.assertEqual((self.central / "ONBOARDING.md").read_text(encoding="utf-8"),
                         source.read_text(encoding="utf-8"))
        backup = self.central / "skills/.agent-guild.previous-code/package"
        self.assertTrue((backup / "SKILL.md").is_file())
        self.assertInstalled(self.install())
        self.assertEqual(len(list(self.central.rglob("*.previous-code"))), 1)

    def test_failed_download_reports_failure_without_success_message(self):
        result = self.install(fail="agent-guild-" + self.tag + ".zip")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("simulated transfer failure", result.stderr)
        self.assertNotIn("Read ~/.agent-guild/ONBOARDING.md", result.stdout)
        self.assertFalse(self.central.exists())

    def test_interrupted_reinstall_preserves_previous_file(self):
        self.assertInstalled(self.install())
        onboarding = self.central / "ONBOARDING.md"
        previous = onboarding.read_bytes()
        result = self.install(fail="agent-guild-" + self.tag + ".zip")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(onboarding.read_bytes(), previous)
        self.assertEqual(list(self.central.rglob(".ag-release-stage-*")), [])

    def test_hash_mismatch_blocks_install(self):
        archive = self.mock / ("agent-guild-" + self.tag + ".zip")
        archive.write_bytes(archive.read_bytes() + b"tampered")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Read ~/.agent-guild/ONBOARDING.md", result.stdout)
        self.assertFalse(self.central.exists())

    def test_missing_local_reviewed_cli_fails_without_download(self):
        (self.repo / "scripts/ag.py").rename(self.repo / "scripts/ag-reviewed.py")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ag.py", result.stderr)
        self.assertFalse(self.central.exists())


@unittest.skipUnless(POWERSHELL, "本机没有 PowerShell；未实测 Windows")
class PowerShellInstallerTests(ShellInstallerTests):
    def install(self, fail=None):
        env = dict(self.env)
        if fail:
            env["MOCK_DOWNLOAD_FAIL"] = fail
        return subprocess.run([POWERSHELL, "-NoProfile", "-NonInteractive",
                               "-File", str(self.repo / "scripts/install.ps1")], env=env,
                              capture_output=True, text=True)


class InstallerContractTests(unittest.TestCase):
    def test_both_wrappers_use_same_local_python_verifier(self):
        for name in ("install.sh", "install.ps1"):
            body = (ROOT / "scripts" / name).read_text(encoding="utf-8-sig")
            self.assertIn("ag._install_release(sys.argv[2])", body)
            self.assertIn("AGENT_GUILD_PYTHON", body)
            self.assertIn("AGENT_GUILD_VERSION", body)
            self.assertNotIn("raw.githubusercontent.com", body)
            self.assertNotRegex(body, r"\|\s*(?:bash|iex)\b")
        windows = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8-sig")
        self.assertIn("& $Python -c $Code $PSScriptRoot $Version", windows)
        self.assertIn("if ($LASTEXITCODE -ne 0)", windows)
        code = re.search(r'^\$Code = "([^\n]+)"$', windows, re.M).group(1)
        self.assertNotIn('"', code)
        compile(code, "powershell-installer-code", "exec")
        self.assertNotIn("-ExecutionPolicy Bypass", windows)


if __name__ == "__main__":
    unittest.main()
