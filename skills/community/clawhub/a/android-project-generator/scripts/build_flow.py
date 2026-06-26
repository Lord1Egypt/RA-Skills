#!/usr/bin/env python3
"""
Android Gradle 构建流程控制

用于把“工程已生成”与“工程已成功编译出可运行 APK”明确区分开。
"""

import subprocess
from pathlib import Path


def choose_gradle_command(project_dir: Path, platform: str) -> list[str]:
    """根据平台选择 gradle 启动命令。"""
    project_dir = Path(project_dir)
    if platform == "win32":
        gradle_cmd = project_dir / "gradlew.bat"
    else:
        gradle_cmd = project_dir / "gradlew"
    return [str(gradle_cmd), "assembleDebug", "--no-daemon"]


def run_assemble_debug(project_dir: Path, platform: str, timeout: int = 600) -> dict:
    """执行 assembleDebug。"""
    command = choose_gradle_command(project_dir, platform)

    try:
        result = subprocess.run(
            command,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "returncode": -1,
            "stdout": "",
            "stderr": "assembleDebug timed out",
        }


def run_adb_command(args: list[str], timeout: int = 120) -> dict:
    """执行 adb 命令。"""
    command = ["adb", *args]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "returncode": -1,
            "stdout": "",
            "stderr": "adb command timed out",
        }


def install_debug_apk(apk_path: Path) -> dict:
    """安装 debug APK 到当前设备。"""
    return run_adb_command(["install", "-r", str(apk_path)])


def launch_main_activity(application_id: str, launch_activity: str) -> dict:
    """启动主 Activity。"""
    component = f"{application_id}/{launch_activity}"
    return run_adb_command(["shell", "am", "start", "-n", component])


def verify_apk_output(project_dir: Path) -> dict:
    """检查 debug APK 是否已生成。"""
    apk_path = Path(project_dir) / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
    if apk_path.exists():
        return {"exists": True, "path": str(apk_path)}
    return {"exists": False, "path": None}


def build_android_project(
    project_dir: Path,
    environment_assessment: dict,
    platform: str,
    application_id: str | None = None,
    launch_activity: str | None = None,
    verify_runnable: bool = False,
) -> dict:
    """按环境状态控制是否执行 Gradle 构建，并给出最终状态。"""
    if not environment_assessment.get("ready_for_build"):
        return {
            "status": "scaffolding_only",
            "reason": "Environment is blocked; project files may exist but build was not attempted.",
            "build": None,
            "apk": {"exists": False, "path": None},
            "install": None,
            "launch": None,
        }

    build_result = run_assemble_debug(project_dir, platform)
    apk_result = verify_apk_output(project_dir)

    if build_result["returncode"] == 0 and apk_result["exists"] and verify_runnable and application_id and launch_activity:
        install_result = install_debug_apk(apk_result["path"])
        if install_result["returncode"] != 0:
            return {
                "status": "install_failed",
                "reason": "APK was built, but installation on device/emulator failed.",
                "build": build_result,
                "apk": apk_result,
                "install": install_result,
                "launch": None,
            }

        launch_result = launch_main_activity(application_id, launch_activity)
        if launch_result["returncode"] == 0:
            return {
                "status": "runnable",
                "reason": "APK was built, installed, and main activity was launched.",
                "build": build_result,
                "apk": apk_result,
                "install": install_result,
                "launch": launch_result,
            }
        return {
            "status": "launch_failed",
            "reason": "APK was installed, but launching the main activity failed.",
            "build": build_result,
            "apk": apk_result,
            "install": install_result,
            "launch": launch_result,
        }

    if build_result["returncode"] == 0 and apk_result["exists"]:
        return {
            "status": "compiled",
            "reason": "assembleDebug succeeded and debug APK was found.",
            "build": build_result,
            "apk": apk_result,
            "install": None,
            "launch": None,
        }

    return {
        "status": "build_failed",
        "reason": "Gradle build did not produce a verified debug APK.",
        "build": build_result,
        "apk": apk_result,
        "install": None,
        "launch": None,
    }
