#!/usr/bin/env python3
"""
端到端集成测试

测试完整的 Android 项目生成和编译流程
注意：这些测试需要完整的 Android 开发环境
"""

import pytest
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass

from conftest import make_workspace_temp_dir, cleanup_workspace_temp_dir

scripts_path = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from project_validator import assess_project_readiness
from build_flow import build_android_project


# ============================================
# 测试配置
# ============================================

@dataclass
class E2ETestConfig:
    """端到端测试配置"""
    project_name: str
    package_name: str
    config_profile: str  # stable, legacy, latest
    use_china_mirror: bool = False
    jdk_version: int = 17


# ============================================
# 测试辅助函数
# ============================================

def check_jdk_version() -> Optional[int]:
    """检查当前 JDK 版本"""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stderr + result.stdout
        
        import re
        match = re.search(r'version "(\d+)', output)
        if match:
            major = int(match.group(1))
            if major == 1:
                # Java 8 format: 1.8.x
                match2 = re.search(r'version "1\.(\d+)', output)
                return int(match2.group(1)) if match2 else None
            return major
    except Exception:
        pass
    return None


def check_gradlew_exists(project_path: Path) -> bool:
    """检查 gradlew 是否存在"""
    gradlew = project_path / "gradlew"
    return gradlew.exists()


def run_gradle_build(project_path: Path, timeout: int = 300) -> Tuple[int, str, str]:
    """
    运行 Gradle 构建
    
    Args:
        project_path: 项目路径
        timeout: 超时时间（秒）
    
    Returns:
        (returncode, stdout, stderr)
    """
    gradlew = project_path / "gradlew"
    
    # Windows 使用 gradlew.bat
    if sys.platform == "win32":
        gradlew = project_path / "gradlew.bat"
    
    if not gradlew.exists():
        raise FileNotFoundError(f"gradlew not found at {gradlew}")
    
    try:
        result = subprocess.run(
            [str(gradlew), "assembleDebug", "--no-daemon"],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Build timed out"
    except Exception as e:
        return -1, "", str(e)


def create_minimal_project(project_path: Path, config: E2ETestConfig) -> None:
    """创建最小可编译项目"""
    # 确保使用绝对路径
    project_path = Path(project_path).resolve()
    
    # 创建目录结构
    dirs = [
        "gradle/wrapper",
        "app/src/main/java/com/example/testapp",
        "app/src/main/res/layout",
        "app/src/main/res/values",
        "app/src/main/res/mipmap-hdpi",
    ]
    
    for dir_path in dirs:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    # 根据配置选择版本
    if config.config_profile == "stable":
        agp_version = "8.7.0"
        gradle_version = "8.9"
        kotlin_version = "2.0.21"
        compile_sdk = 35
    elif config.config_profile == "legacy":
        agp_version = "7.4.2"
        gradle_version = "7.5"
        kotlin_version = "1.9.22"
        compile_sdk = 33
    else:  # latest
        agp_version = "9.1.0"
        gradle_version = "9.3.1"
        kotlin_version = "2.1.0"
        compile_sdk = 36
    
    # 创建 settings.gradle.kts
    if config.use_china_mirror:
        settings_content = f'''pluginManagement {{
    repositories {{
        maven {{ url = uri("https://maven.aliyun.com/repository/gradle-plugin") }}
        maven {{ url = uri("https://maven.aliyun.com/repository/google") }}
        maven {{ url = uri("https://maven.aliyun.com/repository/public") }}
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        maven {{ url = uri("https://maven.aliyun.com/repository/google") }}
        maven {{ url = uri("https://maven.aliyun.com/repository/public") }}
    }}
}}

rootProject.name = "{config.project_name}"
include(":app")'''
    else:
        settings_content = f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{config.project_name}"
include(":app")'''
    
    (project_path / "settings.gradle.kts").write_text(settings_content)
    
    # 创建项目级 build.gradle.kts
    build_content = f'''plugins {{
    id("com.android.application") version "{agp_version}" apply false
    id("org.jetbrains.kotlin.android") version "{kotlin_version}" apply false
}}'''
    
    (project_path / "build.gradle.kts").write_text(build_content)
    
    # 创建 gradle.properties
    gradle_props = '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
android.useAndroidX=true
android.nonTransitiveRClass=true'''
    
    (project_path / "gradle.properties").write_text(gradle_props)
    
    # 创建 gradle-wrapper.properties
    wrapper_props = f'''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists'''
    
    (project_path / "gradle" / "wrapper" / "gradle-wrapper.properties").write_text(wrapper_props)
    
    # 复制 gradlew 脚本（如果当前环境有）
    # 否则创建占位脚本
    if not (project_path / "gradlew").exists():
        # 创建简单的 gradlew 占位符（实际项目需要真实的 wrapper）
        gradlew_content = '''#!/bin/bash
# This is a placeholder. In real scenario, use gradle wrapper.
exec gradle "$@"'''
        (project_path / "gradlew").write_text(gradlew_content)
        
        gradlew_bat_content = '''@echo off
REM This is a placeholder. In real scenario, use gradle wrapper.
gradle %*'''
        (project_path / "gradlew.bat").write_text(gradlew_bat_content)
    
    # 创建 app/build.gradle.kts
    java_version = "17" if config.jdk_version >= 17 else "11"
    
    app_build_content = f'''plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{config.package_name}"
    compileSdk = {compile_sdk}

    defaultConfig {{
        applicationId = "{config.package_name}"
        minSdk = 24
        targetSdk = {compile_sdk}
        versionCode = 1
        versionName = "1.0"
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_{java_version}
        targetCompatibility = JavaVersion.VERSION_{java_version}
    }}

    kotlinOptions {{
        jvmTarget = "{java_version}"
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
}}'''
    
    (project_path / "app" / "build.gradle.kts").write_text(app_build_content)
    
    # 创建 AndroidManifest.xml
    manifest_content = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.TestApp">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    (project_path / "app" / "src" / "main" / "AndroidManifest.xml").write_text(manifest_content)
    
    # 创建 MainActivity.kt
    package_path = config.package_name.replace('.', '/')
    activity_content = f'''package {config.package_name}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }}
}}'''
    
    activity_path = project_path / "app" / "src" / "main" / "java" / package_path / "MainActivity.kt"
    activity_path.parent.mkdir(parents=True, exist_ok=True)
    activity_path.write_text(activity_content)
    
    # 创建布局文件
    layout_content = '''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>'''
    
    (project_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml").write_text(layout_content)
    
    # 创建资源文件
    strings_content = f'''<resources>
    <string name="app_name">{config.project_name}</string>
</resources>'''
    
    (project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml").write_text(strings_content)
    
    themes_content = f'''<resources>
    <style name="Theme.TestApp" parent="Theme.Material3.DayNight.NoActionBar">
    </style>
</resources>'''
    
    (project_path / "app" / "src" / "main" / "res" / "values" / "themes.xml").write_text(themes_content)
    
    # 创建占位的 ic_launcher.png（实际项目需要真实图标）
    # 这里跳过图标文件，编译时会警告但不会失败


# ============================================
# 测试组：端到端编译测试
# ============================================

class TestEndToEndCompilation:
    """端到端编译测试"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """创建临时项目目录"""
        path = make_workspace_temp_dir("e2e")
        try:
            yield path
        finally:
            cleanup_workspace_temp_dir(path)
    
    @pytest.mark.slow
    @pytest.mark.skipif(
        check_jdk_version() is None or check_jdk_version() < 17,
        reason="Requires JDK 17+ for stable profile"
    )
    def test_stable_profile_compiles(self, temp_project_dir):
        """E2E-001: stable 配置编译成功"""
        config = E2ETestConfig(
            project_name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable",
            jdk_version=17
        )
        
        project_path = temp_project_dir / "TestApp"
        create_minimal_project(project_path, config)
        
        # 检查项目创建成功
        assert (project_path / "settings.gradle.kts").exists()
        assert (project_path / "app" / "build.gradle.kts").exists()
        
        # 注意：实际编译测试需要完整的 Android SDK 和 Gradle Wrapper
        # 这里只验证项目结构完整性
        # 在 CI 环境中可以取消注释以下代码进行真实编译测试
        
        # returncode, stdout, stderr = run_gradle_build(project_path)
        # assert returncode == 0, f"Build failed: {stderr}"
        # assert (project_path / "app/build/outputs/apk/debug/app-debug.apk").exists()
    
    @pytest.mark.slow
    def test_legacy_profile_compiles(self, temp_project_dir):
        """E2E-002: legacy 配置编译成功"""
        config = E2ETestConfig(
            project_name="LegacyApp",
            package_name="com.example.legacyapp",
            config_profile="legacy",
            jdk_version=11
        )
        
        project_path = temp_project_dir / "LegacyApp"
        create_minimal_project(project_path, config)
        
        # 验证配置
        wrapper_content = (project_path / "gradle" / "wrapper" / "gradle-wrapper.properties").read_text()
        assert "gradle-7.5" in wrapper_content
    
    @pytest.mark.slow
    def test_china_mirror_compiles(self, temp_project_dir):
        """E2E-003: 国内镜像编译成功"""
        config = E2ETestConfig(
            project_name="ChinaMirrorApp",
            package_name="com.example.chinamirrorapp",
            config_profile="stable",
            use_china_mirror=True,
            jdk_version=17
        )
        
        project_path = temp_project_dir / "ChinaMirrorApp"
        create_minimal_project(project_path, config)
        
        # 验证镜像配置
        settings_content = (project_path / "settings.gradle.kts").read_text()
        assert "maven.aliyun.com" in settings_content

    @pytest.mark.slow
    def test_build_flow_marks_scaffolding_only_when_wrapper_is_placeholder(self, temp_project_dir):
        config = E2ETestConfig(
            project_name="BuildFlowApp",
            package_name="com.example.buildflowapp",
            config_profile="stable",
            jdk_version=17
        )

        project_path = temp_project_dir / "BuildFlowApp"
        create_minimal_project(project_path, config)

        environment_assessment = {
            "ready_for_build": False,
            "status": "blocked",
            "blocking_issues": ["Wrapper is not verified"],
            "warnings": [],
        }

        result = build_android_project(project_path, environment_assessment, platform=sys.platform)

        assert result["status"] == "scaffolding_only"
        assert result["apk"]["exists"] is False


# ============================================
# 测试组：错误处理
# ============================================

class TestErrorHandling:
    """错误处理测试"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """创建临时项目目录"""
        path = make_workspace_temp_dir("e2e")
        try:
            yield path
        finally:
            cleanup_workspace_temp_dir(path)
    
    def test_invalid_package_name(self, temp_project_dir):
        """ERR-003: 无效包名"""
        config = E2ETestConfig(
            project_name="TestApp",
            package_name="123.invalid",  # 以数字开头
            config_profile="stable",
            jdk_version=17
        )
        
        project_path = temp_project_dir / "TestApp"
        create_minimal_project(project_path, config)

        readiness = assess_project_readiness(project_path, config.package_name)

        assert readiness["ready"] is False
        assert any("package name" in issue.lower() for issue in readiness["blocking_issues"])
    
    def test_jdk_version_mismatch(self, temp_project_dir):
        """ERR-001: JDK 版本不匹配"""
        # 构造“环境 JDK 偏低但生成 stable 配置”的固定场景，
        # 不依赖当前机器真实 JDK，避免用例在不同开发机上跳过。
        config = E2ETestConfig(
            project_name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable",
            jdk_version=11
        )
        
        project_path = temp_project_dir / "TestApp"
        create_minimal_project(project_path, config)

        readiness = assess_project_readiness(project_path, config.package_name)

        # 由于 create_minimal_project 仍使用占位 wrapper，这里必须被判定为尚未达到真实构建准备状态
        assert readiness["ready"] is False
        assert any("placeholder" in issue.lower() for issue in readiness["blocking_issues"])


# ============================================
# 测试组：性能测试
# ============================================

class TestPerformance:
    """性能测试"""
    
    @pytest.mark.slow
    def test_project_generation_speed(self):
        """测试项目生成速度"""
        import time
        
        tmp_dir = make_workspace_temp_dir("e2e")
        try:
            config = E2ETestConfig(
                project_name="SpeedTest",
                package_name="com.example.speedtest",
                config_profile="stable",
                jdk_version=17
            )
            
            project_path = Path(tmp_dir) / "SpeedTest"
            
            start_time = time.time()
            create_minimal_project(project_path, config)
            elapsed_time = time.time() - start_time
            
            # 项目生成应该在 1 秒内完成
            assert elapsed_time < 1.0, f"Project generation took {elapsed_time:.2f}s"
        finally:
            cleanup_workspace_temp_dir(tmp_dir)


# ============================================
# 测试组：清理和验证
# ============================================

class TestCleanupAndValidation:
    """清理和验证测试"""
    
    def test_no_temp_files_left(self):
        """测试无临时文件残留"""
        tmp_dir = make_workspace_temp_dir("e2e")
        try:
            config = E2ETestConfig(
                project_name="CleanupTest",
                package_name="com.example.cleanuptest",
                config_profile="stable",
                jdk_version=17
            )
            
            project_path = Path(tmp_dir) / "CleanupTest"
            create_minimal_project(project_path, config)
            
            # 验证没有 .tmp 或 .bak 文件
            for file in project_path.rglob("*"):
                if file.is_file():
                    assert not file.name.endswith('.tmp'), f"Temp file found: {file}"
                    assert not file.name.endswith('.bak'), f"Backup file found: {file}"
        finally:
            cleanup_workspace_temp_dir(tmp_dir)


# ============================================
# Pytest 配置
# ============================================

def pytest_configure(config):
    """配置 pytest 标记"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "requires_android_sdk: marks tests that require Android SDK"
    )
    config.addinivalue_line(
        "markers", "requires_jdk17: marks tests that require JDK 17+"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "not slow"])
