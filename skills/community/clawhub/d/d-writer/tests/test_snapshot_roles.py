#!/usr/bin/env python3
"""快照/回滚对角色卡 glob 展开的测试。

运行：python -m pytest tests/test_snapshot_roles.py -v
"""

import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import _contract
from snapshot_book import create_snapshot
from rollback_book import plan_rollback


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


class TestResolveSnapshotFiles:
    def test_non_glob_pass_through(self, tmp_path):
        """非通配 pattern（current_state.md 等）原样返回。"""
        paths = _contract.resolve_snapshot_files(str(tmp_path))
        assert "story/current_state.md" in paths

    def test_glob_expands_to_existing_role_files(self, tmp_path):
        """story/roles/** 应展开为实际存在的角色文件，且不包含不存在的路径。"""
        book = tmp_path
        role = book / "story" / "roles" / "major" / "陆恒.md"
        role.parent.mkdir(parents=True, exist_ok=True)
        role.write_text("# 陆恒\n", encoding="utf-8")
        paths = _contract.resolve_snapshot_files(str(book))
        assert "story/roles/major/陆恒.md" in paths
        # 不存在的角色文件不应出现
        assert "story/roles/major/不存在.md" not in paths

    def test_glob_dedup_keeps_order(self, tmp_path):
        """重复 pattern 去重，输出稳定排序。"""
        book = tmp_path
        for name in ["甲.md", "乙.md"]:
            f = book / "story" / "roles" / "minor" / name
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("# x\n", encoding="utf-8")
        paths = _contract.resolve_snapshot_files(str(book))
        minor = [p for p in paths if p.startswith("story/roles/minor/")]
        assert minor == sorted(minor)
        assert len(minor) == len(set(minor))


class TestSnapshotIncludesRoles:
    def test_snapshot_copies_role_files(self, tmp_path):
        """create_snapshot 应把角色卡文件纳入快照目录。"""
        shutil.copytree(os.path.join(FIXTURES_DIR, "standard-book"), str(tmp_path),
                        dirs_exist_ok=True)
        result = create_snapshot(str(tmp_path), chapter=1, dry_run=False, force=True)
        assert result["ok"]
        snap_dir = tmp_path / "story" / "snapshots" / "0001"
        assert (snap_dir / "story" / "roles" / "major" / "陆恒.md").is_file()
        assert "story/roles/major/陆恒.md" in result["included_files"]


class TestRollbackManifestHasRoles:
    def test_rollback_plan_lists_role_files(self, tmp_path):
        """manifest.includedFiles 含角色卡，回滚计划应列出。"""
        shutil.copytree(os.path.join(FIXTURES_DIR, "standard-book"), str(tmp_path),
                        dirs_exist_ok=True)
        create_snapshot(str(tmp_path), chapter=1, dry_run=False, force=True)
        plan = plan_rollback(str(tmp_path), chapter=1)
        assert plan["ok"]
        assert any(p.startswith("story/roles/") for p in plan["restore_files"])
