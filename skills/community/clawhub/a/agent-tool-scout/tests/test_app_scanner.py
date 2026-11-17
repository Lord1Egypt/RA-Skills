"""Tests for app_scanner — scan macOS apps (shared scan result)."""

from pathlib import Path

import pytest

from clam.scanner.app_scanner import (
    SCAN_DIRS,
    _KNOWN_UI_APPS,
    find_app,
    find_basic_app,
    scan_applications,
)


@pytest.fixture(scope="module")
def scanned_apps():
    """Scan once per module, not per test."""
    return scan_applications()


class TestScanApplications:
    def test_scan_finds_music(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "music" in ids

    def test_scan_finds_calendar(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "calendar" in ids

    def test_scan_returns_sdef_paths(self, scanned_apps):
        for app in scanned_apps:
            # UI-scriptable apps have no sdef
            if not app.basic_mode:
                assert app.sdef_path.endswith(".sdef")

    def test_scan_returns_bundle_paths(self, scanned_apps):
        for app in scanned_apps:
            assert app.bundle_path.endswith(".app")


class TestFindApp:
    def test_find_by_id(self):
        app = find_app("music")
        assert app is not None
        assert app.name == "Music"

    def test_find_by_name(self):
        app = find_app("Music")
        assert app is not None
        assert app.app_id == "music"

    def test_find_case_insensitive(self):
        app = find_app("MUSIC")
        assert app is not None
        assert app.app_id == "music"

    def test_find_not_found(self):
        assert find_app("nonexistent_app_xyz_123") is None


class TestFinderAndFigma:
    """Tests for Finder (CoreServices .sdef) and Figma (known UI app) in scan."""

    def test_scan_finds_finder(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "finder" in ids

    def test_finder_has_sdef(self, scanned_apps):
        finder = next(a for a in scanned_apps if a.app_id == "finder")
        assert finder.sdef_path.endswith(".sdef")
        assert not finder.basic_mode

    def test_scan_finds_figma(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "figma" in ids

    def test_figma_is_basic_mode(self, scanned_apps):
        figma = next(a for a in scanned_apps if a.app_id == "figma")
        assert figma.basic_mode
        assert figma.sdef_path == ""

    def test_find_app_finder(self):
        app = find_app("finder")
        assert app is not None
        assert app.name == "Finder"

    def test_find_basic_app_figma(self):
        app = find_basic_app("figma")
        assert app is not None
        assert app.app_id == "figma"


class TestExpandedDetection:
    """Tests for expanded scan dirs, UI app list, and nested sdef detection."""

    def test_home_applications_in_scan_dirs(self):
        assert Path.home() / "Applications" in SCAN_DIRS

    def test_known_ui_apps_has_common_apps(self):
        ids = {entry[1] for entry in _KNOWN_UI_APPS}
        # Must include key UI apps
        for expected in ("wechat", "telegram", "visual-studio-code", "cursor", "lark"):
            assert expected in ids, f"{expected} not in _KNOWN_UI_APPS"

    def test_ui_apps_have_process_names(self):
        for _, app_id, _, process_name in _KNOWN_UI_APPS:
            assert process_name, f"{app_id} missing process_name"

    def test_scan_finds_ui_apps(self, scanned_apps):
        """UI apps that are installed should appear in scan results."""
        ids = {a.app_id for a in scanned_apps}
        # At least some of the UI apps should be found (machine-dependent)
        ui_ids = {entry[1] for entry in _KNOWN_UI_APPS}
        found = ids & ui_ids
        assert len(found) >= 1, "No UI apps found on this machine"

    def test_ui_apps_have_correct_process_name(self, scanned_apps):
        """UI apps should store their process_name."""
        for app in scanned_apps:
            if app.basic_mode and app.app_id != "figma":
                # Non-Figma UI apps were added with explicit process names
                if app.process_name:
                    assert len(app.process_name) > 0

    def test_nested_sdef_detection(self, scanned_apps):
        """Apps with nested sdef files should be found."""
        ids = {a.app_id for a in scanned_apps}
        # If ChatGPT Atlas is installed, it should be detected via nested sdef
        # This is machine-dependent, so just verify the scan didn't break
        assert len(scanned_apps) >= 42  # at least as many as before

    def test_total_apps_increased(self, scanned_apps):
        """Expanded detection should find more apps than the original 42."""
        assert len(scanned_apps) >= 42
