#!/usr/bin/env python3
"""
Integration tests for the multi-platform project scanner.

Tests:
  - Android scanning via the unified ScanReport schema
  - Platform auto-detection
  - CLI compatibility (scan_project still works with positional path)
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))


# ── Fixtures ──

@pytest.fixture
def mock_android_project(tmp_path):
    """Create a minimal Android project structure for testing."""
    root = tmp_path / "MockAndroid"
    root.mkdir()

    # settings.gradle.kts
    (root / "settings.gradle.kts").write_text(
        'include(":app")\n'
        'include(":core:common")\n'
        'include(":feature:home")\n',
        encoding="utf-8",
    )

    # === app module ===
    app = root / "app"
    app_res = app / "src" / "main" / "res" / "values"
    app_res.mkdir(parents=True)

    (app / "build.gradle.kts").write_text(
        'plugins { id("com.android.application") }\n'
        "dependencies {\n"
        '    implementation(project(":core:common"))\n'
        '    implementation(project(":feature:home"))\n'
        '    implementation("com.google.android.material:material:1.11.0")\n'
        "}\n",
        encoding="utf-8",
    )

    (app_res / "colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <color name="primary">#FF6200EE</color>\n'
        '    <color name="primary_dark">#FF3700B3</color>\n'
        '    <color name="accent">#FF03DAC5</color>\n'
        '    <color name="text_primary">#FF0F0F0F</color>\n'
        '    <color name="text_secondary">#FF666666</color>\n'
        '    <color name="bg_white">#FFFFFFFF</color>\n'
        "</resources>\n",
        encoding="utf-8",
    )

    (app_res / "strings.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <string name="app_name">DotFortune</string>\n'
        '    <string name="notification_settings">Notification Settings</string>\n'
        '    <string name="cancel">Cancel</string>\n'
        '    <string name="confirm">Confirm</string>\n'
        "</resources>\n",
        encoding="utf-8",
    )

    (app_res / "dimens.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <dimen name="margin_normal">16dp</dimen>\n'
        '    <dimen name="text_size_title">18sp</dimen>\n'
        "</resources>\n",
        encoding="utf-8",
    )

    # Drawable
    drawable_dir = app / "src" / "main" / "res" / "drawable"
    drawable_dir.mkdir(parents=True)
    (drawable_dir / "bg_card.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<shape xmlns:android="http://schemas.android.com/apk/res/android"\n'
        '    android:shape="rectangle">\n'
        '    <solid android:color="#FFFFFFFF" />\n'
        '    <corners android:radius="12dp" />\n'
        '    <stroke android:width="1dp" android:color="#FFE0E0E0" />\n'
        "</shape>\n",
        encoding="utf-8",
    )

    # Custom Views
    kt_dir = app / "src" / "main" / "java" / "com" / "dotfortune" / "widget"
    kt_dir.mkdir(parents=True)
    (kt_dir / "CompactSwitchCompat.kt").write_text(
        "package com.dotfortune.widget\n\n"
        "class CompactSwitchCompat(context: Context) : SwitchCompat(context) {\n"
        "}\n",
        encoding="utf-8",
    )
    (kt_dir / "RoundImageView.kt").write_text(
        "package com.dotfortune.widget\n\n"
        "class RoundImageView(context: Context) : ImageView(context) {\n"
        "}\n",
        encoding="utf-8",
    )

    # === core:common module (dependency) ===
    core = root / "core" / "common"
    core_res = core / "src" / "main" / "res" / "values"
    core_res.mkdir(parents=True)
    (core / "build.gradle.kts").write_text(
        'plugins { id("com.android.library") }\n', encoding="utf-8"
    )
    (core_res / "colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        '    <color name="core_divider">#FFE0E0E0</color>\n'
        '    <color name="core_background">#FFF5F5F5</color>\n'
        "</resources>\n",
        encoding="utf-8",
    )

    # === feature:home module (dependency, empty — no src/main) ===
    home = root / "feature" / "home"
    home.mkdir(parents=True)
    (home / "build.gradle.kts").write_text(
        'plugins { id("com.android.library") }\n', encoding="utf-8"
    )

    return root


# ── Helper to extract totals from new schema ──

def _count(report, field):
    """Sum len(module[field]) across all modules."""
    return sum(len(m.get(field, [])) for m in report.get("modules", []))


def _all_items(report, field):
    """Flatten module[field] across all modules."""
    items = []
    for m in report.get("modules", []):
        items.extend(m.get(field, []))
    return items


# ── Tests ──

class TestAndroidScan:
    """Test Android project scanning via the unified schema."""

    def test_scan_report_schema(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        # Top-level schema fields
        assert report["platform"] == "android"
        assert "modules" in report
        assert "indices" in report
        assert "errors" in report
        assert "metadata" in report

    def test_modules_discovered(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        # app + core:common = 2 scannable modules
        mod_names = [m["name"] for m in report["modules"]]
        assert len(mod_names) == 2
        assert ":app" in mod_names
        assert ":core:common" in mod_names

        # feature:home skipped (no src/main)
        meta = report["metadata"]
        assert meta["modules_scanned"] == 2
        assert meta["modules_skipped"] == 1

    def test_colors(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        total_colors = _count(report, "colors")
        assert total_colors == 8  # 6 app + 2 core

    def test_strings(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        total_strings = _count(report, "strings")
        assert total_strings == 4

    def test_dimens(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        total_dimens = _count(report, "dimens")
        assert total_dimens == 2

    def test_images_drawables(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        # bg_card.xml drawable should appear as an image entry
        all_images = _all_items(report, "images")
        image_names = {i["name"] for i in all_images}
        assert "bg_card" in image_names

    def test_custom_views(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        all_views = _all_items(report, "custom_views")
        view_names = {v["name"] for v in all_views}
        assert "CompactSwitchCompat" in view_names
        assert "RoundImageView" in view_names

    def test_color_index(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        ci = report["indices"]["colors"]
        assert ci.get("#FF6200EE") == "@color/primary"
        assert ci.get("#FF0F0F0F") == "@color/text_primary"

    def test_string_index(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        si = report["indices"]["strings"]
        assert si.get("Cancel") == "@string/cancel"
        assert si.get("DotFortune") == "@string/app_name"

    def test_json_serializable(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        json_str = json.dumps(report, indent=2, ensure_ascii=False, default=str)
        parsed = json.loads(json_str)
        assert parsed["platform"] == "android"
        assert len(parsed["modules"]) == 2

    def test_text_report(self, mock_android_project):
        from project_scan import scan_project, format_text_report
        report = scan_project(str(mock_android_project))

        text = format_text_report(report)
        assert "Platform: android" in text
        assert "Colors:" in text
        assert "Custom Views" in text


class TestPlatformDetection:
    """Test auto-detection and --platform override."""

    def test_android_auto_detected(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))
        assert report["platform"] == "android"

    def test_force_platform(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project), platform="android")
        assert report["platform"] == "android"

    def test_unknown_platform(self, tmp_path):
        from project_scan import scan_project
        # Empty directory — no platform detected
        report = scan_project(str(tmp_path))
        assert "unknown" in report["platform"] or len(report["errors"]) > 0

    def test_invalid_platform_name(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project), platform="nonexistent")
        assert len(report["errors"]) > 0
        assert "nonexistent" in report["errors"][0]


class TestScanReportBase:
    """Test the base ScanReport dataclass."""

    def test_to_dict(self):
        from scanners.base import ScanReport, ModuleReport, ColorEntry
        report = ScanReport(
            platform="test",
            project_root="/tmp/test",
            modules=[
                ModuleReport(
                    name="mod1",
                    path="/tmp/test/mod1",
                    colors=[ColorEntry(name="red", value="#FF0000")],
                )
            ],
        )
        d = report.to_dict()
        assert d["platform"] == "test"
        assert len(d["modules"]) == 1
        assert d["modules"][0]["colors"][0]["name"] == "red"

    def test_finalize_metadata(self):
        from scanners.base import ScanReport
        report = ScanReport(platform="test", project_root="/tmp")
        report.finalize_metadata(modules_skipped=3)
        assert report.metadata["scanner_version"] == "2.0.0"
        assert report.metadata["modules_skipped"] == 3
        assert "scan_time" in report.metadata


class TestAndroidDetector:
    """Test AndroidDetector specifically."""

    def test_detects_gradle_kts(self, tmp_path):
        from scanners.android_scanner import AndroidDetector
        (tmp_path / "settings.gradle.kts").write_text('include(":app")')
        assert AndroidDetector().detect(tmp_path) is True

    def test_detects_gradle_groovy(self, tmp_path):
        from scanners.android_scanner import AndroidDetector
        (tmp_path / "settings.gradle").write_text("include ':app'")
        assert AndroidDetector().detect(tmp_path) is True

    def test_no_gradle(self, tmp_path):
        from scanners.android_scanner import AndroidDetector
        assert AndroidDetector().detect(tmp_path) is False


class TestDependencyVisibility:
    """Test that only visible (dependency-reachable) resources appear in indices."""

    def test_visible_colors(self, mock_android_project):
        from project_scan import scan_project
        report = scan_project(str(mock_android_project))

        ci = report["indices"]["colors"]
        # core:common colors should be visible to :app via implementation dep
        assert "#FFE0E0E0" in ci  # core_divider
        assert "#FFF5F5F5" in ci  # core_background


# ── Legacy compat: keep the old main() runnable ──

def main():
    """Run as standalone script (backward compat)."""
    tmp = Path(tempfile.mkdtemp(prefix="mock_android_"))
    print(f"Mock project: {tmp}")

    try:
        # Reuse fixture logic inline
        from test_project_scan import mock_android_project
        # Can't call fixture directly; just import and run scan_project
        from project_scan import scan_project, format_text_report

        # Create mock project manually
        root = tmp
        _create_mock_inline(root)

        report = scan_project(str(root))
        print(format_text_report(report))
        print()
        print(f"Modules: {len(report['modules'])}")
        print(f"Platform: {report['platform']}")
        print("---")
        print("OK (use `pytest tests/ -v` for full validation)")

    finally:
        shutil.rmtree(tmp)


def _create_mock_inline(root):
    """Inline mock creation for standalone script mode."""
    (root / "settings.gradle.kts").write_text(
        'include(":app")\ninclude(":core:common")\ninclude(":feature:home")\n'
    )
    app_res = root / "app" / "src" / "main" / "res" / "values"
    app_res.mkdir(parents=True)
    (root / "app" / "build.gradle.kts").write_text(
        'plugins { id("com.android.application") }\n'
        'dependencies {\n'
        '    implementation(project(":core:common"))\n'
        '}\n'
    )
    (app_res / "colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <color name="primary">#FF6200EE</color>\n</resources>\n'
    )
    (app_res / "strings.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <string name="app_name">Test</string>\n</resources>\n'
    )
    core_res = root / "core" / "common" / "src" / "main" / "res" / "values"
    core_res.mkdir(parents=True)
    (root / "core" / "common" / "build.gradle.kts").write_text(
        'plugins { id("com.android.library") }\n'
    )
    (core_res / "colors.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <color name="core_bg">#FFF5F5F5</color>\n</resources>\n'
    )
    (root / "feature" / "home").mkdir(parents=True)
    (root / "feature" / "home" / "build.gradle.kts").write_text(
        'plugins { id("com.android.library") }\n'
    )


if __name__ == "__main__":
    main()
