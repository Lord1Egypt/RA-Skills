"""Tests for monorepo workspace_versions merging in lib/dep_parser.py."""

import json
import sys
from pathlib import Path

import pytest

from lib.dep_parser import parse_all, parse_package_json
from lib.schema import DepInfo


class TestWorkspaceVersionsMerge:
    def test_same_package_two_workspaces(self, tmp_path):
        """parse_all() should accumulate workspace_versions instead of last-wins."""
        ws1 = tmp_path / "packages" / "app1"
        ws1.mkdir(parents=True)
        (ws1 / "package.json").write_text(
            json.dumps({"dependencies": {"stripe": "^7.0.0"}}), encoding="utf-8"
        )
        ws2 = tmp_path / "packages" / "app2"
        ws2.mkdir(parents=True)
        (ws2 / "package.json").write_text(
            json.dumps({"dependencies": {"stripe": "^8.0.0"}}), encoding="utf-8"
        )

        files = [str(ws1 / "package.json"), str(ws2 / "package.json")]
        result, errors = parse_all(files)

        assert "stripe" in result
        dep = result["stripe"]
        # workspace_versions should have both paths
        assert len(dep.workspace_versions) == 2
        ws_vers = set(dep.workspace_versions.values())
        assert "7.0.0" in ws_vers or any("7" in v for v in ws_vers)

    def test_single_workspace_no_collision(self, tmp_path):
        """Single workspace: workspace_versions has exactly one entry."""
        ws = tmp_path / "package.json"
        ws.write_text(
            json.dumps({"dependencies": {"chalk": "^5.3.0"}}), encoding="utf-8"
        )
        result, errors = parse_all([str(ws)])
        dep = result.get("chalk")
        assert dep is not None
        assert len(dep.workspace_versions) == 1

    def test_parse_errors_returned(self, tmp_path):
        """parse_all() returns (result, errors); errors includes bad files."""
        bad_file = tmp_path / "package.json"
        bad_file.write_text("{invalid json!!}", encoding="utf-8")
        result, errors = parse_all([str(bad_file)])
        assert len(errors) > 0

    def test_no_error_on_good_file(self, tmp_path):
        good = tmp_path / "package.json"
        good.write_text(json.dumps({"dependencies": {"lodash": "^4.17.21"}}), encoding="utf-8")
        result, errors = parse_all([str(good)])
        assert errors == []
        assert "lodash" in result

    def test_mixed_good_and_bad_files(self, tmp_path):
        good_dir = tmp_path / "app1"
        good_dir.mkdir()
        good = good_dir / "package.json"
        good.write_text(json.dumps({"dependencies": {"axios": "^1.6.0"}}), encoding="utf-8")

        bad_dir = tmp_path / "app2"
        bad_dir.mkdir()
        bad = bad_dir / "package.json"
        bad.write_text("{bad json}", encoding="utf-8")

        result, errors = parse_all([str(good), str(bad)])
        assert "axios" in result
        assert len(errors) == 1

    def test_workspace_versions_key_is_file_path(self, tmp_path):
        """workspace_versions keys should be absolute file paths."""
        ws = tmp_path / "package.json"
        ws.write_text(json.dumps({"dependencies": {"stripe": "7.0.0"}}), encoding="utf-8")
        result, _ = parse_all([str(ws)])
        dep = result["stripe"]
        assert str(ws) in dep.workspace_versions

    def test_three_workspaces_same_package(self, tmp_path):
        versions = ["1.0.0", "2.0.0", "3.0.0"]
        files = []
        for i, ver in enumerate(versions):
            ws = tmp_path / f"app{i}" / "package.json"
            ws.parent.mkdir()
            ws.write_text(json.dumps({"dependencies": {"mylib": ver}}), encoding="utf-8")
            files.append(str(ws))
        result, errors = parse_all(files)
        dep = result["mylib"]
        assert len(dep.workspace_versions) == 3
        stored_versions = set(dep.workspace_versions.values())
        assert stored_versions == {"1.0.0", "2.0.0", "3.0.0"}
