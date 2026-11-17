#!/usr/bin/env python3
"""自动更新脚本测试 —— parse_version / version_is_newer / 下载 URL / git 保护 / CLI 参数。

运行：python -m pytest tests/test_auto_update.py -v
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import auto_update  # noqa: E402


class TestVersion:
    def test_parse_version(self):
        assert auto_update.parse_version("3.10.0") == (3, 10, 0)
        assert auto_update.parse_version("v2.0.2") == (2, 0, 2)
        assert auto_update.parse_version("2.0.0-rc1") == (2, 0, 0)
        assert auto_update.parse_version("2.0.0+build5") == (2, 0, 0)
        assert auto_update.parse_version("") is None
        assert auto_update.parse_version("abc") is None
        assert auto_update.parse_version("3.10") == (3, 10)

    def test_version_is_newer(self):
        # 源码 3.10.0 必须被判定为比注册表 3.9.1 新（防止更新把本地拉回旧版）
        assert auto_update.version_is_newer("3.10.0", "3.9.1")
        assert not auto_update.version_is_newer("3.9.1", "3.10.0")
        assert not auto_update.version_is_newer("3.10.0", "3.10.0")
        assert auto_update.version_is_newer("v2.0.0", "1.9.9")
        assert auto_update.version_is_newer("2.0.0", "")  # 本地无版本 -> 需更新
        assert not auto_update.version_is_newer("", "1.0.0")
        assert auto_update.version_is_newer("2.0.0-rc1", "1.9.0")


class TestDirectDownloadURL:
    def test_url_template_points_to_official_endpoint(self):
        """下载地址必须指向 skillhub 官方端点，不能用已 404 的 COS 桶地址。"""
        assert "api.skillhub.cn" in auto_update.DIRECT_DOWNLOAD_URL_TEMPLATE
        assert "myqcloud.com" not in auto_update.DIRECT_DOWNLOAD_URL_TEMPLATE
        assert "{slug}" in auto_update.DIRECT_DOWNLOAD_URL_TEMPLATE


class TestGitProtection:
    def test_non_repo_returns_false(self, tmp_path):
        assert auto_update._git_uncommitted(tmp_path) is False

    def test_repo_with_uncommitted_changes_returns_true(self, tmp_path):
        self._init_git(tmp_path)
        (tmp_path / "a.txt").write_text("hi", encoding="utf-8")
        self._git(tmp_path, "add", "a.txt")
        (tmp_path / "a.txt").write_text("changed", encoding="utf-8")  # 未提交
        assert auto_update._git_uncommitted(tmp_path) is True

    def test_clean_repo_returns_false(self, tmp_path):
        self._init_git(tmp_path)
        (tmp_path / "a.txt").write_text("hi", encoding="utf-8")
        self._git(tmp_path, "add", "a.txt")
        self._git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "init")
        assert auto_update._git_uncommitted(tmp_path) is False

    # ---- helpers ----

    def _init_git(self, tmp_path):
        try:
            self._git(tmp_path, "init", "-q")
        except Exception:
            pytest.skip("git 不可用，跳过 git 保护用例")

    def _git(self, tmp_path, *args):
        import subprocess

        subprocess.run(
            ["git", "-C", str(tmp_path), *args],
            check=True,
            capture_output=True,
            timeout=15,
        )


class TestCliInvocation:
    def test_upgrade_call_has_no_force(self, monkeypatch):
        """upgrade 子命令不接受 --force，auto_update 调用时不得携带该参数。"""
        calls = []

        class _R:
            returncode = 0

        def fake_run(cmd, **kw):
            calls.append(cmd)
            return _R()

        monkeypatch.setattr(auto_update.shutil, "which", lambda _name: "/fake/skillhub")
        monkeypatch.setattr(auto_update.subprocess, "run", fake_run)

        ok = auto_update._try_skillhub_cli_upgrade(
            "d-writer", auto_update.SKILL_ROOT, "9.9.9"
        )
        assert ok, "CLI upgrade 路径应成功"
        assert calls, "应调用 skillhub CLI"
        # 第一路径必须是 upgrade 且不带 --force
        assert calls[0][1] == "upgrade"
        assert "--force" not in calls[0]

    def test_install_fallback_still_has_force(self, monkeypatch):
        """install 兜底路径保留 --force（install 子命令支持）。"""
        calls = []

        class _R:
            returncode = 1  # upgrade 失败，触发 install 兜底

        def fake_run(cmd, **kw):
            calls.append(cmd)
            return _R()

        monkeypatch.setattr(auto_update.shutil, "which", lambda _name: "/fake/skillhub")
        monkeypatch.setattr(auto_update.subprocess, "run", fake_run)

        ok = auto_update._try_skillhub_cli_upgrade(
            "d-writer", auto_update.SKILL_ROOT, "9.9.9"
        )
        assert not ok  # upgrade 与 install 都"失败"（returncode 1）
        assert calls and calls[-1][1] == "install"
        assert "--force" in calls[-1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
