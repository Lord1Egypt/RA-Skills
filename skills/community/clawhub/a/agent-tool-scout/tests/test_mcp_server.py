"""Tests for CLAM MCP Server — tool registration and handler logic."""

import json

from clam.mcp_server import (
    clam_doctor,
    clam_info,
    clam_scan,
)


class TestToolRegistration:
    def test_all_tools_registered(self):
        from clam.mcp_server import mcp
        tools = mcp._tool_manager._tools
        expected = {"clam_scan", "clam_info", "clam_install", "clam_execute", "clam_doctor"}
        assert set(tools.keys()) == expected

    def test_tool_count(self):
        from clam.mcp_server import mcp
        assert len(mcp._tool_manager._tools) == 5


class TestScanTool:
    def test_scan_returns_valid_json(self):
        result = clam_scan()
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_scan_has_music(self):
        result = clam_scan()
        data = json.loads(result)
        ids = {app["app_id"] for app in data}
        assert "music" in ids

    def test_scan_fields(self):
        result = clam_scan()
        data = json.loads(result)
        first = data[0]
        assert "name" in first
        assert "app_id" in first
        assert "commands" in first
        assert "mode" in first
        assert "installed" in first


class TestInfoTool:
    def test_info_music(self):
        result = clam_info("music")
        data = json.loads(result)
        assert data["app_name"] == "Music"
        assert data["app_id"] == "music"
        assert len(data["commands"]) > 0
        assert len(data["properties"]) > 0

    def test_info_has_supported_field(self):
        result = clam_info("music")
        data = json.loads(result)
        for cmd in data["commands"]:
            assert "supported" in cmd

    def test_info_has_nested_groups(self):
        result = clam_info("music")
        data = json.loads(result)
        assert "nested_groups" in data
        group_names = {g["name"] for g in data["nested_groups"]}
        assert "current-track" in group_names

    def test_info_not_found(self):
        result = clam_info("nonexistent_xyz_abc")
        data = json.loads(result)
        assert "error" in data

    def test_info_fuzzy_match(self):
        result = clam_info("chrome")
        data = json.loads(result)
        # Should match google-chrome if installed, or return error
        assert "app_id" in data or "error" in data


class TestDoctorTool:
    def test_doctor_music(self):
        result = clam_doctor("music")
        data = json.loads(result)
        assert data["app_id"] == "music"
        assert data["total"] > 0
        assert data["supported"] + data["unsupported"] == data["total"]

    def test_doctor_not_found(self):
        result = clam_doctor("nonexistent_xyz_abc")
        data = json.loads(result)
        assert "error" in data


class TestExecuteTool:
    def test_execute_not_installed(self):
        from clam.mcp_server import clam_execute
        result = clam_execute("nonexistent_xyz_abc", "play")
        data = json.loads(result)
        assert "error" in data
        assert "未安装" in data["error"]
