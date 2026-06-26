#!/usr/bin/env python3
"""
Gradle APK 构建流程控制测试
"""

import sys
from pathlib import Path
from unittest.mock import patch


scripts_path = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from build_flow import (
    choose_gradle_command,
    verify_apk_output,
    run_assemble_debug,
    run_adb_command,
    install_debug_apk,
    launch_main_activity,
    build_android_project,
)


class TestChooseGradleCommand:
    """Gradle 命令选择测试"""

    def test_prefers_gradlew_bat_on_windows(self, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        (project_dir / "gradlew.bat").write_text("@echo off")

        command = choose_gradle_command(project_dir, platform="win32")

        assert command == [str(project_dir / "gradlew.bat"), "assembleDebug", "--no-daemon"]

    def test_prefers_gradlew_on_unix(self, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        (project_dir / "gradlew").write_text("#!/bin/bash")

        command = choose_gradle_command(project_dir, platform="linux")

        assert command == [str(project_dir / "gradlew"), "assembleDebug", "--no-daemon"]


class TestVerifyApkOutput:
    """APK 输出验证测试"""

    def test_detects_debug_apk(self, temp_dir):
        project_dir = temp_dir / "app"
        apk_path = project_dir / "app" / "build" / "outputs" / "apk" / "debug"
        apk_path.mkdir(parents=True)
        (apk_path / "app-debug.apk").write_bytes(b"apk")

        result = verify_apk_output(project_dir)

        assert result["exists"] is True
        assert result["path"].endswith("app-debug.apk")

    def test_reports_missing_debug_apk(self, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()

        result = verify_apk_output(project_dir)

        assert result["exists"] is False
        assert result["path"] is None


class TestRunAssembleDebug:
    """assembleDebug 执行测试"""

    @patch("build_flow.subprocess.run")
    def test_run_assemble_debug_success(self, mock_run, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        (project_dir / "gradlew").write_text("#!/bin/bash")
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "BUILD SUCCESSFUL"
        mock_run.return_value.stderr = ""

        result = run_assemble_debug(project_dir, platform="linux")

        assert result["returncode"] == 0
        assert "BUILD SUCCESSFUL" in result["stdout"]

    @patch("build_flow.subprocess.run")
    def test_run_assemble_debug_timeout(self, mock_run, temp_dir):
        import subprocess

        project_dir = temp_dir / "app"
        project_dir.mkdir()
        (project_dir / "gradlew").write_text("#!/bin/bash")
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="gradlew", timeout=10)

        result = run_assemble_debug(project_dir, platform="linux", timeout=10)

        assert result["returncode"] == -1
        assert "timed out" in result["stderr"].lower()


class TestAdbFlow:
    """ADB 安装与启动流程测试"""

    @patch("build_flow.subprocess.run")
    def test_run_adb_command_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Success"
        mock_run.return_value.stderr = ""

        result = run_adb_command(["devices"])

        assert result["returncode"] == 0
        assert result["stdout"] == "Success"

    @patch("build_flow.run_adb_command")
    def test_install_debug_apk(self, mock_adb, temp_dir):
        apk_path = temp_dir / "app-debug.apk"
        apk_path.write_bytes(b"apk")
        mock_adb.return_value = {"returncode": 0, "stdout": "Success", "stderr": ""}

        result = install_debug_apk(apk_path)

        assert result["returncode"] == 0
        mock_adb.assert_called_once()
        assert "install" in mock_adb.call_args[0][0]

    @patch("build_flow.run_adb_command")
    def test_launch_main_activity(self, mock_adb):
        mock_adb.return_value = {"returncode": 0, "stdout": "Starting: Intent", "stderr": ""}

        result = launch_main_activity("com.example.app", ".MainActivity")

        assert result["returncode"] == 0
        assert "am" in mock_adb.call_args[0][0]
        assert "com.example.app/.MainActivity" in mock_adb.call_args[0][0]


class TestBuildAndroidProject:
    """完整构建流程测试"""

    @patch("build_flow.run_assemble_debug")
    @patch("build_flow.verify_apk_output")
    def test_marks_project_compiled_when_build_and_apk_succeed(self, mock_verify_apk, mock_build, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        mock_build.return_value = {"returncode": 0, "stdout": "ok", "stderr": ""}
        mock_verify_apk.return_value = {"exists": True, "path": "app/build/outputs/apk/debug/app-debug.apk"}

        env_assessment = {"ready_for_build": True, "status": "ready", "blocking_issues": [], "warnings": []}
        result = build_android_project(project_dir, env_assessment, platform="linux")

        assert result["status"] == "compiled"
        assert result["apk"]["exists"] is True

    @patch("build_flow.run_assemble_debug")
    def test_marks_project_scaffolding_only_when_environment_blocked(self, mock_build, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        env_assessment = {
            "ready_for_build": False,
            "status": "blocked",
            "blocking_issues": ["JDK not detected"],
            "warnings": [],
        }

        result = build_android_project(project_dir, env_assessment, platform="linux")

        assert result["status"] == "scaffolding_only"
        assert result["build"] is None
        mock_build.assert_not_called()

    @patch("build_flow.run_assemble_debug")
    @patch("build_flow.verify_apk_output")
    def test_marks_project_failed_when_build_fails(self, mock_verify_apk, mock_build, temp_dir):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        mock_build.return_value = {"returncode": 1, "stdout": "", "stderr": "AGP failed"}
        mock_verify_apk.return_value = {"exists": False, "path": None}

        env_assessment = {"ready_for_build": True, "status": "ready", "blocking_issues": [], "warnings": []}
        result = build_android_project(project_dir, env_assessment, platform="linux")

        assert result["status"] == "build_failed"
        assert "AGP failed" in result["build"]["stderr"]

    @patch("build_flow.launch_main_activity")
    @patch("build_flow.install_debug_apk")
    @patch("build_flow.run_assemble_debug")
    @patch("build_flow.verify_apk_output")
    def test_marks_project_runnable_when_install_and_launch_succeed(
        self,
        mock_verify_apk,
        mock_build,
        mock_install,
        mock_launch,
        temp_dir,
    ):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        mock_build.return_value = {"returncode": 0, "stdout": "ok", "stderr": ""}
        mock_verify_apk.return_value = {"exists": True, "path": str(project_dir / "app-debug.apk")}
        mock_install.return_value = {"returncode": 0, "stdout": "Success", "stderr": ""}
        mock_launch.return_value = {"returncode": 0, "stdout": "Starting: Intent", "stderr": ""}

        env_assessment = {"ready_for_build": True, "status": "ready", "blocking_issues": [], "warnings": []}
        result = build_android_project(
            project_dir,
            env_assessment,
            platform="linux",
            application_id="com.example.app",
            launch_activity=".MainActivity",
            verify_runnable=True,
        )

        assert result["status"] == "runnable"
        assert result["install"]["returncode"] == 0
        assert result["launch"]["returncode"] == 0

    @patch("build_flow.launch_main_activity")
    @patch("build_flow.install_debug_apk")
    @patch("build_flow.run_assemble_debug")
    @patch("build_flow.verify_apk_output")
    def test_marks_project_install_failed_when_apk_cannot_be_installed(
        self,
        mock_verify_apk,
        mock_build,
        mock_install,
        mock_launch,
        temp_dir,
    ):
        project_dir = temp_dir / "app"
        project_dir.mkdir()
        mock_build.return_value = {"returncode": 0, "stdout": "ok", "stderr": ""}
        mock_verify_apk.return_value = {"exists": True, "path": str(project_dir / "app-debug.apk")}
        mock_install.return_value = {"returncode": 1, "stdout": "", "stderr": "INSTALL_FAILED"}

        env_assessment = {"ready_for_build": True, "status": "ready", "blocking_issues": [], "warnings": []}
        result = build_android_project(
            project_dir,
            env_assessment,
            platform="linux",
            application_id="com.example.app",
            launch_activity=".MainActivity",
            verify_runnable=True,
        )

        assert result["status"] == "install_failed"
        mock_launch.assert_not_called()
