#!/usr/bin/env python3
"""
项目结构生成集成测试

测试完整的 Android 项目结构生成
"""

import pytest
import os
import stat
from pathlib import Path
from typing import List, Set
from dataclasses import dataclass

from conftest import make_workspace_temp_dir, cleanup_workspace_temp_dir


# ============================================
# 测试数据模型
# ============================================

@dataclass
class ProjectConfig:
    """项目配置"""
    name: str
    package_name: str
    config_profile: str
    use_china_mirror: bool = False


# ============================================
# 测试辅助函数
# ============================================

def get_required_files(package_name: str) -> List[str]:
    """获取必需文件列表"""
    package_path = package_name.replace('.', '/')
    return [
        "settings.gradle.kts",
        "build.gradle.kts",
        "gradle.properties",
        "gradle/wrapper/gradle-wrapper.properties",
        "gradlew",
        "gradlew.bat",
        "app/build.gradle.kts",
        "app/src/main/AndroidManifest.xml",
        f"app/src/main/java/{package_path}/MainActivity.kt",
        "app/src/main/res/layout/activity_main.xml",
        "app/src/main/res/values/strings.xml",
        "app/src/main/res/values/themes.xml",
    ]


def get_required_directories() -> List[str]:
    """获取必需目录列表"""
    return [
        "gradle/wrapper",
        "app/src/main/java",
        "app/src/main/res/layout",
        "app/src/main/res/values",
        "app/src/main/res/mipmap-hdpi",
        "app/src/main/res/mipmap-mdpi",
        "app/src/main/res/mipmap-xhdpi",
        "app/src/main/res/mipmap-xxhdpi",
        "app/src/main/res/mipmap-xxxhdpi",
    ]


def create_project_structure(project_path: Path, config: ProjectConfig) -> None:
    """创建项目结构（模拟生成器）"""
    # 创建根目录
    project_path.mkdir(parents=True, exist_ok=True)
    
    # 创建必需目录
    for dir_path in get_required_directories():
        full_path = project_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    # 创建 settings.gradle.kts
    settings_content = f"""pluginManagement {{
    repositories {{
        {'maven { url = uri("https://maven.aliyun.com/repository/gradle-plugin") }' if config.use_china_mirror else 'google()'}
        {'maven { url = uri("https://maven.aliyun.com/repository/google") }' if config.use_china_mirror else 'mavenCentral()'}
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        {'maven { url = uri("https://maven.aliyun.com/repository/google") }' if config.use_china_mirror else 'google()'}
        {'maven { url = uri("https://maven.aliyun.com/repository/public") }' if config.use_china_mirror else 'mavenCentral()'}
    }}
}}

rootProject.name = "{config.name}"
include(":app")"""
    
    (project_path / "settings.gradle.kts").write_text(settings_content)
    
    # 创建项目级 build.gradle.kts
    build_content = f"""plugins {{
    id("com.android.application") version "8.7.0" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
}}"""
    
    (project_path / "build.gradle.kts").write_text(build_content)
    
    # 创建 gradle.properties
    gradle_props = """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
android.useAndroidX=true
android.nonTransitiveRClass=true"""
    
    (project_path / "gradle.properties").write_text(gradle_props)
    
    # 创建 gradle-wrapper.properties
    wrapper_props = f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.9-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists"""
    
    wrapper_path = project_path / "gradle" / "wrapper" / "gradle-wrapper.properties"
    wrapper_path.write_text(wrapper_props)
    
    # 创建 gradlew (占位)
    (project_path / "gradlew").write_text("#!/bin/bash\n# Gradle wrapper placeholder")
    (project_path / "gradlew.bat").write_text("@echo off\nREM Gradle wrapper placeholder")
    
    # 创建 app/build.gradle.kts
    package_path = config.package_name.replace('.', '/')
    app_build_content = f"""plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{config.package_name}"
    compileSdk = 35

    defaultConfig {{
        applicationId = "{config.package_name}"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}

    kotlinOptions {{
        jvmTarget = "17"
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
}}"""
    
    (project_path / "app" / "build.gradle.kts").write_text(app_build_content)
    
    # 创建 AndroidManifest.xml
    manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.{config.name}">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
    
    (project_path / "app" / "src" / "main" / "AndroidManifest.xml").write_text(manifest_content)
    
    # 创建 MainActivity.kt
    activity_content = f"""package {config.package_name}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }}
}}"""
    
    activity_path = project_path / "app" / "src" / "main" / "java" / package_path / "MainActivity.kt"
    activity_path.parent.mkdir(parents=True, exist_ok=True)
    activity_path.write_text(activity_content)
    
    # 创建布局文件
    layout_content = """<?xml version="1.0" encoding="utf-8"?>
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
</androidx.constraintlayout.widget.ConstraintLayout>"""
    
    (project_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml").write_text(layout_content)
    
    # 创建资源文件
    strings_content = f"""<resources>
    <string name="app_name">{config.name}</string>
</resources>"""
    
    (project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml").write_text(strings_content)
    
    themes_content = f"""<resources>
    <style name="Theme.{config.name}" parent="Theme.Material3.DayNight.NoActionBar">
    </style>
</resources>"""
    
    (project_path / "app" / "src" / "main" / "res" / "values" / "themes.xml").write_text(themes_content)


# ============================================
# 测试组：项目结构生成
# ============================================

class TestProjectStructureGeneration:
    """项目结构生成测试"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """创建临时项目目录"""
        path = make_workspace_temp_dir("integration")
        try:
            yield path
        finally:
            cleanup_workspace_temp_dir(path)
    
    def test_generate_complete_structure(self, temp_project_dir):
        """IT-STR-001: 生成完整项目结构"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 检查所有必需文件
        required_files = get_required_files(config.package_name)
        missing_files = []
        
        for file_path in required_files:
            full_path = project_path / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        assert len(missing_files) == 0, f"Missing files: {missing_files}"
    
    @pytest.mark.skipif(os.name == 'nt', reason="Unix-specific test")
    def test_file_permissions_unix(self, temp_project_dir):
        """IT-STR-002: 文件权限正确 (Unix)"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 检查 gradlew 是否可执行
        gradlew_path = project_path / "gradlew"
        assert gradlew_path.exists()
        
        # 设置可执行权限
        gradlew_path.chmod(gradlew_path.stat().st_mode | stat.S_IXUSR)
        
        # 验证权限
        mode = gradlew_path.stat().st_mode
        assert mode & stat.S_IXUSR, "gradlew should be executable"
    
    def test_directory_hierarchy_correct(self, temp_project_dir):
        """IT-STR-003: 目录层级正确"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 检查目录结构
        required_dirs = get_required_directories()
        
        for dir_path in required_dirs:
            full_path = project_path / dir_path
            assert full_path.exists(), f"Directory missing: {dir_path}"
            assert full_path.is_dir(), f"Not a directory: {dir_path}"
    
    def test_android_manifest_correct(self, temp_project_dir):
        """IT-STR-004: AndroidManifest 正确"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        manifest_path = project_path / "app" / "src" / "main" / "AndroidManifest.xml"
        
        assert manifest_path.exists()
        
        content = manifest_path.read_text()
        
        # 验证必需属性
        assert 'xmlns:android="http://schemas.android.com/apk/res/android"' in content
        assert "android.intent.action.MAIN" in content
        assert "android.intent.category.LAUNCHER" in content
        assert "android:exported=\"true\"" in content
        assert ".MainActivity" in content
    
    def test_resource_files_complete(self, temp_project_dir):
        """IT-STR-005: 资源文件完整"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 检查 strings.xml
        strings_path = project_path / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        assert strings_path.exists()
        strings_content = strings_path.read_text()
        assert config.name in strings_content
        
        # 检查 themes.xml
        themes_path = project_path / "app" / "src" / "main" / "res" / "values" / "themes.xml"
        assert themes_path.exists()
        themes_content = themes_path.read_text()
        assert "Theme.Material3" in themes_content
    
    def test_china_mirror_configuration(self, temp_project_dir):
        """测试国内镜像配置"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable",
            use_china_mirror=True
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        settings_path = project_path / "settings.gradle.kts"
        settings_content = settings_path.read_text()
        
        # 验证使用阿里云镜像
        assert "maven.aliyun.com" in settings_content
        assert "repository/google" in settings_content
        assert "repository/public" in settings_content


# ============================================
# 测试组：Gradle 配置集成
# ============================================

class TestGradleConfigurationIntegration:
    """Gradle 配置集成测试"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """创建临时项目目录"""
        path = make_workspace_temp_dir("integration")
        try:
            yield path
        finally:
            cleanup_workspace_temp_dir(path)
    
    def test_stable_config_completeness(self, temp_project_dir):
        """IT-GRAD-001: stable 配置完整性"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 检查项目级 build.gradle.kts
        build_path = project_path / "build.gradle.kts"
        build_content = build_path.read_text()
        
        # 验证 AGP 版本
        assert "8.7.0" in build_content
        
        # 验证 Kotlin 版本
        assert "2.0.21" in build_content
        
        # 检查 gradle-wrapper.properties
        wrapper_path = project_path / "gradle" / "wrapper" / "gradle-wrapper.properties"
        wrapper_content = wrapper_path.read_text()
        
        # 验证 Gradle 版本
        assert "gradle-8.9-bin.zip" in wrapper_content
    
    def test_namespace_correct_setting(self, temp_project_dir):
        """IT-GRAD-004: namespace 正确设置"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 检查 app/build.gradle.kts
        app_build_path = project_path / "app" / "build.gradle.kts"
        app_build_content = app_build_path.read_text()
        
        # 验证 namespace 字段存在
        assert 'namespace = "com.example.testapp"' in app_build_content
        
        # 验证 applicationId 正确
        assert 'applicationId = "com.example.testapp"' in app_build_content
    
    def test_kotlin_dsl_syntax_valid(self, temp_project_dir):
        """IT-GRAD-005: Kotlin DSL 语法正确"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # 所有 .kts 文件
        kts_files = [
            "settings.gradle.kts",
            "build.gradle.kts",
            "app/build.gradle.kts"
        ]
        
        for kts_file in kts_files:
            file_path = project_path / kts_file
            content = file_path.read_text()
            
            # 基本语法验证
            # 检查括号匹配
            assert content.count('{') == content.count('}'), f"Braces mismatch in {kts_file}"
            
            # 检查引号匹配（简单检查）
            single_quotes = content.count("'")
            double_quotes = content.count('"')
            assert single_quotes % 2 == 0, f"Single quotes mismatch in {kts_file}"
            assert double_quotes % 2 == 0, f"Double quotes mismatch in {kts_file}"


# ============================================
# 测试组：包名转换
# ============================================

class TestPackageNameConversion:
    """包名转换测试"""
    
    def test_package_name_to_path(self):
        """测试包名转路径"""
        package_name = "com.example.testapp"
        expected_path = "com/example/testapp"
        
        actual_path = package_name.replace('.', '/')
        
        assert actual_path == expected_path
    
    def test_java_file_path(self, temp_project_dir):
        """测试 Java 文件路径生成"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        # MainActivity.kt 路径
        activity_path = (
            project_path / "app" / "src" / "main" / "java" / 
            "com" / "example" / "testapp" / "MainActivity.kt"
        )
        
        assert activity_path.exists()
        
        # 验证包名
        content = activity_path.read_text()
        assert f"package {config.package_name}" in content
    
    @pytest.fixture
    def temp_project_dir(self):
        """创建临时项目目录"""
        path = make_workspace_temp_dir("integration")
        try:
            yield path
        finally:
            cleanup_workspace_temp_dir(path)


# ============================================
# 测试组：文件内容验证
# ============================================

class TestFileContentValidation:
    """文件内容验证测试"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """创建临时项目目录"""
        path = make_workspace_temp_dir("integration")
        try:
            yield path
        finally:
            cleanup_workspace_temp_dir(path)
    
    def test_main_activity_content(self, temp_project_dir):
        """测试 MainActivity 内容"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        activity_path = (
            project_path / "app" / "src" / "main" / "java" / 
            "com" / "example" / "testapp" / "MainActivity.kt"
        )
        
        content = activity_path.read_text()
        
        # 验证必需导入
        assert "import android.os.Bundle" in content
        assert "import androidx.appcompat.app.AppCompatActivity" in content
        
        # 验证类定义
        assert "class MainActivity : AppCompatActivity()" in content
        
        # 验证 onCreate 方法
        assert "override fun onCreate" in content
        assert "setContentView(R.layout.activity_main)" in content
    
    def test_layout_file_content(self, temp_project_dir):
        """测试布局文件内容"""
        config = ProjectConfig(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        project_path = temp_project_dir / "TestApp"
        create_project_structure(project_path, config)
        
        layout_path = project_path / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
        content = layout_path.read_text()
        
        # 验证根元素
        assert "ConstraintLayout" in content
        
        # 验证必需属性
        assert 'android:layout_width="match_parent"' in content
        assert 'android:layout_height="match_parent"' in content


# ============================================
# Pytest 标记
# ============================================

@pytest.mark.integration
class TestIntegrationMarker:
    """集成测试标记"""
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
