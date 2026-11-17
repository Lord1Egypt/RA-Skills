#!/usr/bin/env python3
"""Tests for doctor (ROADMAP T1.10) and schema fingerprinting (T1.2)."""

import contextlib
import io
import json
import os
import plistlib
import sqlite3
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import doctor
import pytest
from test_new_scripts import create_full_test_db

from _common import ExitCode
from _schema import SchemaRegistry, macos_for_model_version


@pytest.fixture
def library(tmp_path) -> Path:
    """A .photoslibrary bundle holding the full fixture, with an originals/ folder."""
    bundle = tmp_path / "Test.photoslibrary"
    (bundle / "database").mkdir(parents=True)
    target = sqlite3.connect(bundle / "database" / "Photos.sqlite")
    create_full_test_db().backup(target)
    # Like a real library (found on macOS 26): a spatial R*Tree the guard must never be asked to open.
    target.execute("CREATE VIRTUAL TABLE Z_RT_Asset_boundedByRect USING rtree(Z_PK, ZMINX, ZMAXX, ZMINY, ZMAXY)")
    target.commit()
    target.close()
    (bundle / "originals" / "A").mkdir(parents=True)
    return bundle


def set_model_version(bundle: Path, version: int) -> None:
    conn = sqlite3.connect(bundle / "database" / "Photos.sqlite")
    conn.execute("CREATE TABLE Z_METADATA (Z_VERSION INTEGER, Z_UUID TEXT, Z_PLIST BLOB)")
    conn.execute("INSERT INTO Z_METADATA VALUES (1, 'x', ?)", (plistlib.dumps({"PLModelVersion": version}),))
    conn.commit()
    conn.close()


def run(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with (
        patch.object(sys, "argv", ["doctor", *argv]),
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(io.StringIO()),
    ):
        code = doctor.main()
    return code, out.getvalue()


def report_for(*argv: str) -> tuple[int, dict]:
    code, out = run(*argv, "--format", "json")
    report = json.loads(out)
    report["by_name"] = {c["name"]: c for c in report["checks"]}
    return code, report


class TestChecks:
    def test_healthy_library(self, library):
        code, report = report_for("--library", str(library))
        assert code == ExitCode.OK
        assert report["ok"]
        checks = report["by_name"]
        assert [checks[n]["status"] for n in ("python", "library", "read_access", "library_size")] == ["ok"] * 4
        assert checks["schema"]["status"] == "warn"  # unknown, but diagnosed: not a "not authorized" failure
        assert checks["automation"]["status"] == "skip"
        assert report["library"]["assets"] > 0
        assert report["degraded"] == []

    def test_missing_library(self, tmp_path):
        code, report = report_for("--db-path", str(tmp_path / "missing.sqlite"))
        assert code == ExitCode.DB_NOT_FOUND
        assert report["by_name"]["library"]["status"] == "fail"
        assert "--library" in report["by_name"]["library"]["fix"]
        assert report["by_name"]["schema"]["status"] == "skip"

    @pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permissions")
    def test_unreadable_database(self, library):
        db = library / "database" / "Photos.sqlite"
        db.chmod(0)
        try:
            code, report = report_for("--library", str(library))
        finally:
            db.chmod(0o600)
        assert code == ExitCode.PERMISSION_DENIED
        assert "Full Disk Access" in report["by_name"]["read_access"]["fix"]

    def test_features_reports_each_script_contract(self, library):
        _, report = report_for("--library", str(library))
        degraded = {(d["command"], d["section"]) for d in report["features"]["degraded_sections"]}
        # The shared fixture has no face-quality or iCloud columns.
        assert ("face_quality", "faces") in degraded
        assert ("icloud_status", "icloud") in degraded
        assert report["by_name"]["features"]["status"] == "warn"

    def test_unavailable_command_is_a_warning_not_a_failure(self, library):
        conn = sqlite3.connect(library / "database" / "Photos.sqlite")
        conn.execute("ALTER TABLE ZGENERICALBUM DROP COLUMN ZTITLE")
        conn.commit()
        conn.close()
        code, report = report_for("--library", str(library))
        assert code == ExitCode.OK
        assert {"command": "album_auditor", "missing": ["ZGENERICALBUM.ZTITLE"]} in report["features"][
            "unavailable_commands"
        ]

    def test_human_output_shows_fixes(self, tmp_path):
        code, out = run("--db-path", str(tmp_path / "missing.sqlite"))
        assert code == ExitCode.DB_NOT_FOUND
        assert "❌ library" in out
        assert "→ Pass the library explicitly" in out


class TestSchemaIdentification:
    def test_fingerprint_depends_on_schema_not_data(self):
        a, b = create_full_test_db(), create_full_test_db()
        b.execute("DELETE FROM ZASSET")
        assert SchemaRegistry(a).fingerprint() == SchemaRegistry(b).fingerprint()
        b.execute("ALTER TABLE ZASSET ADD COLUMN ZNEWCOLUMN INTEGER")
        assert SchemaRegistry(a).fingerprint() != SchemaRegistry(b).fingerprint()

    @pytest.mark.parametrize(
        ("version", "macos"),
        [
            (16210, "macOS 13 Ventura"),
            (17120, "macOS 14 Sonoma"),
            (18000, "macOS 15 Sequoia"),
            (19607, "macOS 26 Tahoe"),  # observed on a real macOS 26.7.2 library
            (99999, None),
        ],
    )
    def test_model_version_ranges(self, version, macos):
        assert macos_for_model_version(version) == macos

    def test_recognized_version_with_new_fingerprint_warns_with_contribution_steps(self, library):
        set_model_version(library, 18123)
        _, report = report_for("--library", str(library))
        assert report["schema"]["model_version"] == 18123
        assert report["schema"]["macos"] == "macOS 15 Sequoia"
        schema_check = report["by_name"]["schema"]
        assert schema_check["status"] == "warn"
        assert "--schema-dump" in schema_check["fix"]

    def test_old_model_version_is_flagged(self, library):
        set_model_version(library, 15500)
        _, report = report_for("--library", str(library))
        assert "older than the tested range" in report["by_name"]["schema"]["detail"]

    def test_unknown_schema_warns_never_crashes(self, library):
        _, report = report_for("--library", str(library))
        assert report["schema"]["model_version"] is None
        assert report["by_name"]["schema"]["status"] == "warn"
        assert "Unrecognized schema" in report["by_name"]["schema"]["detail"]

    def test_known_fingerprint(self, library, tmp_path, monkeypatch):
        fingerprint = SchemaRegistry(sqlite3.connect(library / "database" / "Photos.sqlite")).fingerprint()
        known = tmp_path / "fingerprints.json"
        known.write_text(json.dumps({"fingerprints": {fingerprint: {"macos": "macOS 26 Tahoe"}}}))
        monkeypatch.setattr(doctor, "FINGERPRINTS_PATH", known)
        _, report = report_for("--library", str(library))
        assert report["schema"]["known_fingerprint"]
        assert report["by_name"]["schema"] == {
            "name": "schema",
            "status": "ok",
            "detail": "macOS 26 Tahoe schema (known fingerprint)",
            "fix": None,
        }

    def test_shipped_fingerprints_file_is_valid(self):
        data = json.loads(doctor.FINGERPRINTS_PATH.read_text(encoding="utf-8"))
        assert data["fingerprints"], "at least one verified fingerprint ships"
        for fingerprint, entry in data["fingerprints"].items():
            assert len(fingerprint) == 64 and int(fingerprint, 16) >= 0
            assert entry["macos"].startswith("macOS ")
            # The recorded model version must agree with the range table.
            assert macos_for_model_version(entry["model_version"]) == entry["macos"]


class TestSchemaDump:
    def test_dump_contains_definitions_and_no_rows(self, library):
        code, out = run("--library", str(library), "--schema-dump")
        assert code == ExitCode.OK
        assert "CREATE TABLE ZASSET" in out
        assert "-- fingerprint: " in out
        assert "INSERT" not in out.upper()
        # Fixture rows (filenames, people) must never appear.
        assert "IMG_" not in out and "Alice" not in out

    def test_dump_of_missing_library(self, tmp_path):
        code, _ = run("--db-path", str(tmp_path / "missing.sqlite"), "--schema-dump")
        assert code == ExitCode.DB_NOT_FOUND


class TestOptimizeStorage:
    def test_originals_present(self, library):
        _, report = report_for("--library", str(library))
        assets = report["library"]["assets"]
        for i in range(assets):
            (library / "originals" / "A" / f"{i}.heic").write_bytes(b"x")
        _, report = report_for("--library", str(library))
        assert report["by_name"]["optimize_storage"]["status"] == "ok"

    def test_most_originals_missing(self, library):
        (library / "originals" / "A" / "only.heic").write_bytes(b"x")
        _, report = report_for("--library", str(library))
        check = report["by_name"]["optimize_storage"]
        assert check["status"] == "warn"
        assert "Download Originals" in check["fix"]

    def test_bare_database_cannot_tell(self, tmp_path):
        db = tmp_path / "Photos.sqlite"
        target = sqlite3.connect(db)
        create_full_test_db().backup(target)
        target.close()
        _, report = report_for("--db-path", str(db))
        assert report["by_name"]["optimize_storage"]["status"] == "skip"


class TestAutomation:
    @pytest.mark.parametrize(
        ("returncode", "stderr", "status"),
        [(0, "", "ok"), (1, "execution error: Not authorized to send Apple events to Photos. (-1743)", "fail")],
    )
    def test_check(self, library, returncode, stderr, status):
        with patch("doctor.subprocess.run", return_value=MagicMock(returncode=returncode, stdout="", stderr=stderr)):
            code, report = report_for("--library", str(library), "--check-automation")
        assert report["by_name"]["automation"]["status"] == status
        assert code == (ExitCode.OK if status == "ok" else ExitCode.ERROR)
        if status == "fail":
            assert "Automation" in report["by_name"]["automation"]["fix"]

    def test_not_run_unless_asked(self, library):
        with patch("doctor.subprocess.run") as osascript:
            report_for("--library", str(library))
        osascript.assert_not_called()


class TestReportShape:
    """JSON consumers rely on a fixed check list; checks that couldn't run are "skip", never absent."""

    def test_healthy(self, library):
        _, report = report_for("--library", str(library))
        assert [c["name"] for c in report["checks"]] == list(doctor.CHECK_NAMES)

    def test_missing_library(self, tmp_path):
        _, report = report_for("--db-path", str(tmp_path / "missing.sqlite"))
        assert [c["name"] for c in report["checks"]] == list(doctor.CHECK_NAMES)
        assert report["by_name"]["read_access"]["status"] == "skip"
        assert report["by_name"]["optimize_storage"]["status"] == "skip"

    @pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permissions")
    def test_unreadable(self, library):
        db = library / "database" / "Photos.sqlite"
        db.chmod(0)
        try:
            _, report = report_for("--library", str(library))
        finally:
            db.chmod(0o600)
        assert [c["name"] for c in report["checks"]] == list(doctor.CHECK_NAMES)
        assert report["by_name"]["optimize_storage"]["status"] == "skip"


def test_old_python_gets_the_fix_not_a_traceback():
    """Stock macOS python3 is 3.9: the project modules can't even import there, so _bootstrap must catch it."""
    scripts = Path(doctor.__file__).parent
    code = f"import sys; sys.version_info = (3, 9, 25, 'final', 0); sys.path.insert(0, {str(scripts)!r}); import _bootstrap"
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
    assert result.returncode == 1
    assert "Python 3.9 is too old" in result.stderr
    assert "brew install python" in result.stderr
    assert "Traceback" not in result.stderr


def test_doctor_imports_bootstrap_before_any_project_module():
    source = Path(doctor.__file__).read_text(encoding="utf-8")
    project_imports = [line for line in source.splitlines() if line.startswith(("import _", "from _"))]
    assert project_imports[0] == "import _bootstrap"


def test_a_database_error_fails_one_check_not_the_report(library):
    """A denial or query error in one check must not take down the whole diagnosis."""
    with patch("doctor.library_stats", side_effect=sqlite3.OperationalError("not authorized")):
        code, report = report_for("--library", str(library))
    size = report["by_name"]["library_size"]
    assert size["status"] == "fail"
    assert "not authorized" in size["detail"]
    assert "--verbose" in size["fix"]
    assert report["by_name"]["schema"]["status"] != "fail"
    assert [c["name"] for c in report["checks"]] == list(doctor.CHECK_NAMES)
    assert code == ExitCode.ERROR
