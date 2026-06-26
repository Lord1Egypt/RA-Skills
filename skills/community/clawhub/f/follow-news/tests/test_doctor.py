#!/usr/bin/env python3
"""Tests for the project-level preflight doctor command."""

import subprocess
import sys
import unittest
import importlib.util
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

spec = importlib.util.spec_from_file_location("doctor_module", SCRIPTS_DIR / "doctor.py")
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)
sys.modules.setdefault("doctor_module", doctor)


def _ok_cp(args):
    if args and args[:2] == ["--version"]:
        return _build_cp(args, stdout="opencli 1.8.0")
    if args and args[:1] == ["version"]:
        return _build_cp(args, stdout="opencli version 1.8.0")
    if args and args[:1] == ["-v"]:
        return _build_cp(args, stdout="1.8.0")
    if args and args[:1] == ["-V"]:
        return _build_cp(args, stdout="opencli 1.8.0")
    return subprocess.CompletedProcess(args=args, returncode=0, stdout='{"commands":[{"site":"twitter","name":"tweets"}]}', stderr="")


def _build_cp(args, returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(args=args, returncode=returncode, stdout=stdout, stderr=stderr)


class TestDoctorSuccess(unittest.TestCase):
    def setUp(self):
        self._opencli_bin_patch = patch(
            "doctor_module._fetch_twitter.resolve_opencli_bin",
            return_value="/bin/opencli",
        )
        self._opencli_bin_patch.start()
        self.addCleanup(self._opencli_bin_patch.stop)

    def _make_opencli_success(self):
        def _opencli(args, timeout):
            if args and args[:2] == ["--version"]:
                return _build_cp(args, stdout="opencli 1.8.0")
            if args and args[:1] == ["version"]:
                return _build_cp(args, stdout="opencli version 1.8.0")
            if args and args[:1] == ["-v"]:
                return _build_cp(args, stdout="1.8.0")
            if args and args[:1] == ["-V"]:
                return _build_cp(args, stdout="opencli 1.8.0")
            if args[:3] == ["list", "-f", "json"]:
                return _ok_cp(args)
            if args[:3] == ["browser", "tab", "list"]:
                return _build_cp(args, stdout="[]")
            if args == ["doctor"]:
                return _build_cp(args, stdout="ok")
            return _build_cp(args)

        return _opencli

    def test_doctor_report_ok(self):
        with patch("doctor_module._run_opencli_command", side_effect=self._make_opencli_success()), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="t1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "ok", "total": 3}):
            report = doctor.run_doctor()

        self.assertEqual(report["status"], "ok")
        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli"]["status"], "ok")
        self.assertEqual(checks["opencli_browser_bridge"]["status"], "ok")
        self.assertEqual(checks["opencli_x_login"]["status"], "ok")
        self.assertEqual(checks["web_brave"]["status"], "ok")
        self.assertEqual(checks["web_tavily"]["status"], "ok")

    def test_opencli_version_too_old_is_warning(self):
        def _opencli(args, timeout):
            if args and args[:2] == ["--version"]:
                return _build_cp(args, stdout="opencli 0.0.1")
            if args and args[:1] == ["version"]:
                return _build_cp(args, stdout="opencli version 0.0.1")
            if args and args[:1] == ["-v"]:
                return _build_cp(args, stdout="0.0.1")
            if args and args[:1] == ["-V"]:
                return _build_cp(args, stdout="opencli 0.0.1")
            return _ok_cp(args)

        with patch("doctor_module._run_opencli_command", side_effect=_opencli), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="k1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "ok", "total": 1}):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli"]["status"], "warning")
        self.assertEqual(checks["opencli"]["code"], "opencli_version_too_old")


    def test_opencli_version_not_parseable_is_warning(self):
        def _opencli(args, timeout):
            if args and args[:2] == ["--version"]:
                return _build_cp(args, stdout="opencli dev")
            if args and args[:1] == ["version"]:
                return _build_cp(args, stdout="dev")
            if args and args[:1] == ["-v"]:
                return _build_cp(args, stdout="dev")
            if args and args[:1] == ["-V"]:
                return _build_cp(args, stdout="dev")
            return _ok_cp(args)

        with patch("doctor_module._run_opencli_command", side_effect=_opencli), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="k1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "ok", "total": 1}):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli"]["status"], "warning")
        self.assertEqual(checks["opencli"]["code"], "opencli_version_unknown")

    def test_opencli_version_with_two_part_number_is_accepted(self):
        def _opencli(args, timeout):
            if args and args[:2] == ["--version"]:
                return _build_cp(args, stdout="opencli 1.8")
            if args and args[:1] == ["version"]:
                return _build_cp(args, stdout="opencli version 1.8")
            if args and args[:1] == ["-v"]:
                return _build_cp(args, stdout="1.8")
            if args and args[:1] == ["-V"]:
                return _build_cp(args, stdout="opencli 1.8")
            return _ok_cp(args)

        with patch("doctor_module._run_opencli_command", side_effect=_opencli), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="k1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "ok", "total": 1}):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli"]["status"], "ok")

class TestDoctorFailureModes(unittest.TestCase):
    def setUp(self):
        self._opencli_bin_patch = patch(
            "doctor_module._fetch_twitter.resolve_opencli_bin",
            return_value="/bin/opencli",
        )
        self._opencli_bin_patch.start()
        self.addCleanup(self._opencli_bin_patch.stop)

    def test_opencli_missing_marks_warning(self):
        with patch("doctor_module._fetch_twitter.resolve_opencli_bin", side_effect=doctor._fetch_twitter.OpenCliBackendError(
            "opencli_missing",
            "OpenCLI executable not found.",
        )), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=[]), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value=None):
            report = doctor.run_doctor()

        self.assertEqual(report["status"], "warning")
        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli"]["status"], "warning")
        self.assertIn("API fallback", checks["opencli"]["action"])
        self.assertIn("GETX_API_KEY", checks["opencli"]["action"])
        self.assertEqual(checks["opencli_browser_bridge"]["status"], "warning")
        self.assertEqual(checks["opencli_x_login"]["status"], "warning")
        self.assertEqual(checks["web_brave"]["status"], "warning")
        self.assertEqual(checks["web_tavily"]["status"], "warning")
        self.assertIn("API fallback", checks["opencli_browser_bridge"]["action"])

    def test_x_login_auth_required(self):
        def _opencli(args, timeout):
            if args and args[:2] == ["--version"]:
                return _build_cp(args, stdout="opencli 1.8.0")
            if args and args[:1] == ["version"]:
                return _build_cp(args, stdout="opencli version 1.8.0")
            if args and args[:1] == ["-v"]:
                return _build_cp(args, stdout="1.8.0")
            if args and args[:1] == ["-V"]:
                return _build_cp(args, stdout="opencli 1.8.0")
            if args[:3] == ["list", "-f", "json"]:
                return _ok_cp(args)
            if args[:3] == ["browser", "tab", "list"]:
                return _build_cp(args, stdout="[]")
            if args == ["doctor"]:
                return _build_cp(args, returncode=77, stderr="authentication required")
            return _build_cp(args)

        with patch("doctor_module._run_opencli_command", side_effect=_opencli), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="t1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "ok", "total": 2}):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli_x_login"]["status"], "warning")
        self.assertEqual(checks["opencli_x_login"]["code"], "opencli_auth_required")

    def test_browser_bridge_not_healthy(self):
        def _opencli(args, timeout):
            if args and args[:2] == ["--version"]:
                return _build_cp(args, stdout="opencli 1.8.0")
            if args and args[:1] == ["version"]:
                return _build_cp(args, stdout="opencli version 1.8.0")
            if args and args[:1] == ["-v"]:
                return _build_cp(args, stdout="1.8.0")
            if args and args[:1] == ["-V"]:
                return _build_cp(args, stdout="opencli 1.8.0")
            if args[:3] == ["list", "-f", "json"]:
                return _ok_cp(args)
            if args[:3] == ["browser", "tab", "list"]:
                return _build_cp(args, returncode=69, stderr="browser bridge unavailable")
            if args == ["doctor"]:
                return _build_cp(args, stdout="ok")
            return _build_cp(args)

        with patch("doctor_module._run_opencli_command", side_effect=_opencli), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="t1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "ok", "total": 2}):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["opencli_browser_bridge"]["status"], "warning")
        self.assertEqual(checks["opencli_browser_bridge"]["code"], "opencli_browser_unavailable")

    def test_web_readiness_reports_missing_keys(self):
        with patch("doctor_module._run_opencli_command", side_effect=self._opencli_ok), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=[]), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value=None):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["web_brave"]["status"], "warning")
        self.assertEqual(checks["web_tavily"]["status"], "warning")
        self.assertIn(checks["web_brave"]["code"], {"brave_key_missing", "no_usable_key", "brave_no_usable_key"})

    def test_tavily_probe_failure(self):
        with patch("doctor_module._run_opencli_command", side_effect=self._opencli_ok), \
                patch("doctor_module._fetch_web.get_brave_api_keys", return_value=["k1"]), \
                patch("doctor_module._fetch_web.select_brave_key_and_limits", return_value=("k1", 5, 1)), \
                patch("doctor_module._fetch_web.get_tavily_api_key", return_value="t1"), \
                patch("doctor_module._fetch_web.search_tavily", return_value={"status": "error", "error": "auth failed"}):
            report = doctor.run_doctor()

        checks = {item["name"]: item for item in report["checks"]}
        self.assertEqual(checks["web_tavily"]["status"], "warning")
        self.assertEqual(checks["web_tavily"]["code"], "tavily_probe_failed")

    @staticmethod
    def _opencli_ok(args, timeout):
        if args and args[:2] == ["--version"]:
            return _build_cp(args, stdout="opencli 1.8.0")
        if args and args[:1] == ["version"]:
            return _build_cp(args, stdout="opencli version 1.8.0")
        if args and args[:1] == ["-v"]:
            return _build_cp(args, stdout="1.8.0")
        if args and args[:1] == ["-V"]:
            return _build_cp(args, stdout="opencli 1.8.0")
        if args[:3] == ["list", "-f", "json"]:
            return _ok_cp(args)
        if args[:3] == ["browser", "tab", "list"]:
            return _build_cp(args, stdout="[]")
        if args == ["doctor"]:
            return _build_cp(args, stdout="ok")
        return _build_cp(args)
