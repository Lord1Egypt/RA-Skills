#!/usr/bin/env python3
"""
项目就绪度验证测试

验证 AI 生成的 Android 项目是否具备真实构建条件。
"""

import sys
from pathlib import Path


scripts_path = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from project_validator import (
    validate_package_name,
    validate_wrapper_files,
    assess_project_readiness,
)


class TestValidatePackageName:
    """包名校验测试"""

    def test_accepts_valid_package_name(self):
        assert validate_package_name("com.example.app") is True
        assert validate_package_name("org.company.my_app") is True

    def test_rejects_invalid_package_name(self):
        assert validate_package_name("123.invalid") is False
        assert validate_package_name("com..app") is False
        assert validate_package_name("single") is False


class TestValidateWrapperFiles:
    """Gradle Wrapper 完整性测试"""

    def test_reports_missing_wrapper_jar(self, temp_dir):
        project_dir = temp_dir / "MissingJar"
        (project_dir / "gradle" / "wrapper").mkdir(parents=True)
        (project_dir / "gradlew").write_text("#!/bin/bash\n./gradle")
        (project_dir / "gradlew.bat").write_text("@echo off\r\ngradle %*")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties").write_text("distributionUrl=https://...")

        result = validate_wrapper_files(project_dir)

        assert result["complete"] is False
        assert "gradle/wrapper/gradle-wrapper.jar" in result["missing"]

    def test_rejects_placeholder_wrapper_scripts(self, temp_dir):
        project_dir = temp_dir / "PlaceholderWrapper"
        (project_dir / "gradle" / "wrapper").mkdir(parents=True)
        (project_dir / "gradlew").write_text("#!/bin/bash\n# placeholder\nexec gradle \"$@\"")
        (project_dir / "gradlew.bat").write_text("@echo off\r\nREM placeholder\r\ngradle %*")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties").write_text("distributionUrl=https://...")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.jar").write_bytes(b"jar")

        result = validate_wrapper_files(project_dir)

        assert result["complete"] is False
        assert any("placeholder" in issue.lower() for issue in result["issues"])

    def test_accepts_complete_wrapper(self, temp_dir):
        project_dir = temp_dir / "CompleteWrapper"
        (project_dir / "gradle" / "wrapper").mkdir(parents=True)
        (project_dir / "gradlew").write_text("#!/bin/bash\nAPP_HOME=$(cd \"${0%/*}\" && pwd)")
        (project_dir / "gradlew.bat").write_text("@echo off\r\nset APP_HOME=%~dp0")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties").write_text("distributionUrl=https://...")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.jar").write_bytes(b"jar")

        result = validate_wrapper_files(project_dir)

        assert result["complete"] is True
        assert result["issues"] == []


class TestAssessProjectReadiness:
    """项目构建就绪度评估测试"""

    def test_reports_project_ready_when_core_files_exist(self, temp_dir):
        project_dir = temp_dir / "ReadyProject"
        (project_dir / "gradle" / "wrapper").mkdir(parents=True)
        (project_dir / "app" / "src" / "main").mkdir(parents=True)
        (project_dir / "gradlew").write_text("#!/bin/bash\nAPP_HOME=$(cd \"${0%/*}\" && pwd)")
        (project_dir / "gradlew.bat").write_text("@echo off\r\nset APP_HOME=%~dp0")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties").write_text("distributionUrl=https://...")
        (project_dir / "gradle" / "wrapper" / "gradle-wrapper.jar").write_bytes(b"jar")
        (project_dir / "settings.gradle.kts").write_text("include(\":app\")")
        (project_dir / "build.gradle.kts").write_text("plugins {}")
        (project_dir / "app" / "build.gradle.kts").write_text("namespace = \"com.example.ready\"")
        (project_dir / "app" / "src" / "main" / "AndroidManifest.xml").write_text("<manifest />")

        result = assess_project_readiness(project_dir, "com.example.ready")

        assert result["ready"] is True
        assert result["blocking_issues"] == []

    def test_reports_invalid_package_name_as_blocker(self, temp_dir):
        project_dir = temp_dir / "InvalidPackage"
        project_dir.mkdir(parents=True)

        result = assess_project_readiness(project_dir, "123.invalid")

        assert result["ready"] is False
        assert any("package name" in issue.lower() for issue in result["blocking_issues"])
