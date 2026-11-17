"""Tests for clam CLI commands — 使用 CliRunner。"""

import json

import pytest
from click.testing import CliRunner

from clam.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestScan:
    def test_scan_json_returns_valid_json(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_scan_json_has_expected_fields(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        data = json.loads(result.output)
        first = data[0]
        assert "name" in first
        assert "app_id" in first
        assert "commands" in first
        assert "properties" in first
        assert "installed" in first

    def test_scan_json_music_present(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        data = json.loads(result.output)
        ids = {app["app_id"] for app in data}
        assert "music" in ids

    def test_scan_human_mode(self, runner):
        result = runner.invoke(cli, ["scan"])
        assert result.exit_code == 0
        assert "扫描完成" in result.output

    def test_scan_json_finder_present(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        data = json.loads(result.output)
        ids = {app["app_id"] for app in data}
        assert "finder" in ids

    def test_scan_json_figma_present(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        data = json.loads(result.output)
        ids = {app["app_id"] for app in data}
        assert "figma" in ids

    def test_scan_json_finder_has_commands(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        data = json.loads(result.output)
        finder = next(app for app in data if app["app_id"] == "finder")
        assert finder["commands"] > 0
        assert finder["mode"] == "full"

    def test_scan_json_figma_is_ui_mode(self, runner):
        result = runner.invoke(cli, ["--json", "scan"])
        data = json.loads(result.output)
        figma = next(app for app in data if app["app_id"] == "figma")
        assert figma["mode"] == "ui"


class TestInfo:
    def test_info_json(self, runner):
        result = runner.invoke(cli, ["--json", "info", "music"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["app_name"] == "Music"
        assert "commands" in data
        assert "properties" in data
        assert len(data["commands"]) > 0
        assert len(data["properties"]) > 0

    def test_info_json_has_entry_point(self, runner):
        result = runner.invoke(cli, ["--json", "info", "music"])
        data = json.loads(result.output)
        assert data["entry_point"] == "clam-music"

    def test_info_json_has_nested_groups(self, runner):
        result = runner.invoke(cli, ["--json", "info", "music"])
        data = json.loads(result.output)
        assert "nested_groups" in data
        group_names = {g["name"] for g in data["nested_groups"]}
        assert "current-track" in group_names
        # Check compound command
        track_group = next(g for g in data["nested_groups"] if g["name"] == "current-track")
        assert track_group["compound_command"] == "get-current-track"
        # Check individual properties
        prop_names = {p["name"] for p in track_group["properties"]}
        assert "name" in prop_names
        assert "artist" in prop_names

    def test_info_not_found(self, runner):
        result = runner.invoke(cli, ["info", "nonexistent_xyz"])
        assert result.exit_code != 0

    def test_info_human_mode(self, runner):
        result = runner.invoke(cli, ["info", "music"])
        assert result.exit_code == 0
        assert "Music" in result.output


class TestDoctor:
    def test_doctor_json_music(self, runner):
        result = runner.invoke(cli, ["--json", "doctor", "music"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["app_id"] == "music"
        assert data["total"] > 0
        assert data["supported"] + data["unsupported"] == data["total"]
        assert isinstance(data["commands"], list)

    def test_doctor_json_has_supported_field(self, runner):
        result = runner.invoke(cli, ["--json", "doctor", "music"])
        data = json.loads(result.output)
        for cmd in data["commands"]:
            assert "supported" in cmd
            assert "name" in cmd
            assert isinstance(cmd["supported"], bool)

    def test_doctor_human_mode(self, runner):
        result = runner.invoke(cli, ["doctor", "music"])
        assert result.exit_code == 0
        assert "可靠性检查" in result.output

    def test_doctor_not_found(self, runner):
        result = runner.invoke(cli, ["doctor", "nonexistent_xyz"])
        assert result.exit_code != 0

    def test_info_json_has_supported_field(self, runner):
        """clam info --json should include supported field per command."""
        result = runner.invoke(cli, ["--json", "info", "music"])
        data = json.loads(result.output)
        for cmd in data["commands"]:
            assert "supported" in cmd


class TestList:
    def test_list_empty(self, runner):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0

    def test_list_json_empty(self, runner):
        result = runner.invoke(cli, ["--json", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
