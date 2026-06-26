#!/usr/bin/env python3
"""
Android 项目就绪度验证器

用于判断 AI 生成的工程是否具备真实构建前提，而不是只看目录结构是否像一个 Android 项目。
"""

from pathlib import Path
import re


def validate_package_name(package_name: str) -> bool:
    """校验 Android 包名是否符合基本规则。"""
    if not package_name or "." not in package_name:
        return False

    segments = package_name.split(".")
    for segment in segments:
        if not segment:
            return False
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", segment):
            return False

    return True


def validate_wrapper_files(project_dir: Path) -> dict:
    """验证 Gradle Wrapper 是否完整且不是占位脚本。"""
    project_dir = Path(project_dir)
    required_files = [
        "gradlew",
        "gradlew.bat",
        "gradle/wrapper/gradle-wrapper.properties",
        "gradle/wrapper/gradle-wrapper.jar",
    ]

    missing = [path for path in required_files if not (project_dir / path).exists()]
    issues = []

    gradlew = project_dir / "gradlew"
    if gradlew.exists():
        content = gradlew.read_text(encoding="utf-8", errors="ignore").lower()
        if "placeholder" in content or 'exec gradle "$@"' in content:
            issues.append("gradlew is a placeholder script, not a real wrapper launcher.")

    gradlew_bat = project_dir / "gradlew.bat"
    if gradlew_bat.exists():
        content = gradlew_bat.read_text(encoding="utf-8", errors="ignore").lower()
        if "placeholder" in content or "gradle %*" in content:
            issues.append("gradlew.bat is a placeholder script, not a real wrapper launcher.")

    return {
        "complete": not missing and not issues,
        "missing": missing,
        "issues": issues,
    }


def assess_project_readiness(project_dir: Path, package_name: str) -> dict:
    """评估项目是否具备进入 assembleDebug 的最低条件。"""
    project_dir = Path(project_dir)
    blocking_issues = []

    if not validate_package_name(package_name):
        blocking_issues.append("Package name is invalid for an Android application.")

    required_project_files = [
        "settings.gradle.kts",
        "build.gradle.kts",
        "app/build.gradle.kts",
        "app/src/main/AndroidManifest.xml",
    ]
    for relative_path in required_project_files:
        if not (project_dir / relative_path).exists():
            blocking_issues.append(f"Missing required project file: {relative_path}")

    wrapper_status = validate_wrapper_files(project_dir)
    for missing_file in wrapper_status["missing"]:
        blocking_issues.append(f"Missing required wrapper file: {missing_file}")
    blocking_issues.extend(wrapper_status["issues"])

    return {
        "ready": len(blocking_issues) == 0,
        "blocking_issues": blocking_issues,
        "wrapper_status": wrapper_status,
    }
