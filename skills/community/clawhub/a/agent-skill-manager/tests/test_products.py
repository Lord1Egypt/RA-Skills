"""Tests for agent_skill_manager.products module."""

import pytest
from pathlib import Path
from agent_skill_manager.config.products import (
    PRODUCTS, CENTRAL_DIR,
    get_product_path, get_all_product_dirs, get_product_by_short,
)


class TestProducts:
    def test_products_not_empty(self):
        assert len(PRODUCTS) >= 9

    def test_all_have_required_fields(self):
        required = {"name", "short", "macos_path", "windows_path", "sync_method"}
        for p in PRODUCTS:
            assert required.issubset(p.keys()), f"Missing fields in {p.get('name')}"

    def test_short_names_unique(self):
        shorts = [p["short"] for p in PRODUCTS]
        assert len(shorts) == len(set(shorts)), "Short names must be unique"

    def test_central_dir_is_under_home(self):
        assert str(CENTRAL_DIR).startswith(str(Path.home()))

    def test_get_product_by_short(self):
        p = get_product_by_short("dumate")
        assert p is not None
        assert p["name"].startswith("DuMate")

    def test_get_product_by_short_not_found(self):
        assert get_product_by_short("nonexistent") is None

    def test_get_product_path_returns_path_or_none(self):
        for p in PRODUCTS:
            path = get_product_path(p)
            if p["sync_method"] == "pack":
                assert path is None
            else:
                assert isinstance(path, Path)

    def test_get_all_product_dirs_returns_list(self):
        for p in PRODUCTS:
            dirs = get_all_product_dirs(p)
            assert isinstance(dirs, list)

    def test_minimax_uses_central_dir(self):
        minimax = get_product_by_short("minimax")
        assert minimax["sync_method"] == "native"
        assert get_product_path(minimax) == CENTRAL_DIR

    def test_codebuddy_has_settings_file(self):
        cb = get_product_by_short("codebuddy")
        assert cb is not None
        assert "settings_file" in cb
        assert cb["settings_file"].name == "settings.json"

    def test_comate_path(self):
        comate = get_product_by_short("comate")
        assert comate is not None
        assert comate["sync_method"] == "symlink"
        path = get_product_path(comate)
        assert path is not None
        assert ".comate" in str(path)

    def test_qoder_path(self):
        qoder = get_product_by_short("qoder")
        assert qoder is not None
        assert qoder["sync_method"] == "symlink"
        path = get_product_path(qoder)
        assert path is not None
        assert ".qoderwork" in str(path)

    def test_new_products_count(self):
        """Verify 3 new products were added."""
        shorts = {p["short"] for p in PRODUCTS}
        assert "codebuddy" in shorts
        assert "comate" in shorts
        assert "qoder" in shorts


    def test_qwenwork_path(self):
        qwenwork = get_product_by_short("qwenwork")
        assert qwenwork is not None
        assert qwenwork["sync_method"] == "symlink"
        path = get_product_path(qwenwork)
        assert path is not None
        assert ".qwenworkcn" in str(path)
        assert path.name == "skills"

    def test_doubaowork_path(self):
        dbw = get_product_by_short("doubaowork")
        assert dbw is not None
        assert dbw["sync_method"] == "symlink"
        path = get_product_path(dbw)
        assert path is not None
        assert ".user_skills" in str(path)

    def test_newest_products_count(self):
        """Verify qwenwork + doubaowork were added."""
        shorts = {p["short"] for p in PRODUCTS}
        assert "qwenwork" in shorts
        assert "doubaowork" in shorts
        assert len(PRODUCTS) == 11
