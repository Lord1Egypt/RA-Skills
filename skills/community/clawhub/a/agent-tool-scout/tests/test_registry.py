"""Tests for registry — CRUD 操作，使用 tmp_path 隔离。"""

import json

import pytest

from clam.registry import registry


@pytest.fixture(autouse=True)
def tmp_registry(tmp_path, monkeypatch):
    """将注册表重定向到临时目录。"""
    monkeypatch.setattr(registry, "REGISTRY_DIR", tmp_path)
    monkeypatch.setattr(registry, "REGISTRY_FILE", tmp_path / "registry.json")


class TestRegistry:
    def test_load_empty(self):
        data = registry.load()
        assert data == {"version": 1, "wrappers": {}}

    def test_register_and_get(self):
        registry.register(
            app_id="music",
            app_name="Music",
            sdef_path="/path/to/sdef",
            wrapper_dir="/path/to/wrapper",
            command_count=11,
            property_count=24,
        )
        info = registry.get("music")
        assert info is not None
        assert info["app_name"] == "Music"
        assert info["entry_point"] == "clam-music"
        assert info["command_count"] == 11

    def test_unregister(self):
        registry.register(
            app_id="music",
            app_name="Music",
            sdef_path="/p",
            wrapper_dir="/w",
            command_count=1,
            property_count=1,
        )
        assert registry.unregister("music") is True
        assert registry.get("music") is None

    def test_unregister_nonexistent(self):
        assert registry.unregister("nonexistent") is False

    def test_list_all(self):
        registry.register("a", "App A", "/a", "/wa", 1, 1)
        registry.register("b", "App B", "/b", "/wb", 2, 2)
        all_wrappers = registry.list_all()
        assert len(all_wrappers) == 2
        assert "a" in all_wrappers
        assert "b" in all_wrappers

    def test_persistence(self, tmp_path):
        """注册表数据在 load/save 周期中持久化。"""
        registry.register("x", "App X", "/x", "/wx", 5, 10)
        # 直接读文件验证
        data = json.loads((tmp_path / "registry.json").read_text())
        assert "x" in data["wrappers"]
        assert data["wrappers"]["x"]["command_count"] == 5

    def test_register_overwrites(self):
        """重复注册同一 app_id 应覆盖。"""
        registry.register("music", "Music", "/p1", "/w1", 5, 10)
        registry.register("music", "Music", "/p2", "/w2", 8, 15)
        info = registry.get("music")
        assert info["sdef_path"] == "/p2"
        assert info["command_count"] == 8
