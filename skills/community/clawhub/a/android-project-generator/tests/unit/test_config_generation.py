#!/usr/bin/env python3
"""
配置生成功能测试

测试 Gradle 配置文件的生成和验证
"""

import pytest
import re
from pathlib import Path
from typing import Dict, Any


# ============================================
# 测试数据：版本兼容性矩阵
# ============================================

VERSION_MATRIX = {
    "stable": {
        "agp": "8.7.0",
        "gradle": "8.9",
        "jdk": 17,
        "kotlin": "2.0.21",
        "compileSdk": 35
    },
    "latest": {
        "agp": "9.1.0",
        "gradle": "9.3.1",
        "jdk": 17,
        "kotlin": "2.1.0",
        "compileSdk": 36
    },
    "legacy": {
        "agp": "7.4.2",
        "gradle": "7.5",
        "jdk": 11,
        "kotlin": "1.9.22",
        "compileSdk": 33
    }
}

# 最小版本要求
MINIMUM_REQUIREMENTS = {
    "agp_8": {"gradle": "8.0", "jdk": 17},
    "agp_8_7": {"gradle": "8.9", "jdk": 17},
    "agp_9": {"gradle": "9.1", "jdk": 17},
    "agp_7": {"gradle": "7.0", "jdk": 11},
}


# ============================================
# 测试组：版本兼容性验证
# ============================================

class TestVersionCompatibility:
    """版本兼容性测试"""
    
    def test_agp_87_requires_gradle_89(self):
        """UT-VER-001: AGP 8.7.0 需要 Gradle 8.9+"""
        agp_version = "8.7.0"
        minimum_gradle = "8.9"
        
        # 验证配置矩阵
        assert VERSION_MATRIX["stable"]["agp"] == agp_version
        assert VERSION_MATRIX["stable"]["gradle"] == minimum_gradle
        
        # 验证最小要求
        assert MINIMUM_REQUIREMENTS["agp_8_7"]["gradle"] == minimum_gradle
    
    def test_agp_91_requires_gradle_93(self):
        """UT-VER-002: AGP 9.1.0 需要 Gradle 9.3+"""
        agp_version = "9.1.0"
        minimum_gradle = "9.3.1"
        
        assert VERSION_MATRIX["latest"]["agp"] == agp_version
        assert VERSION_MATRIX["latest"]["gradle"] == minimum_gradle
    
    def test_agp_8x_requires_jdk_17(self):
        """UT-VER-003: AGP 8.x 需要 JDK 17"""
        # 所有 AGP 8.x 版本都要求 JDK 17
        assert MINIMUM_REQUIREMENTS["agp_8"]["jdk"] == 17
        assert MINIMUM_REQUIREMENTS["agp_8_7"]["jdk"] == 17
        
        # stable 配置使用 AGP 8.7.0
        assert VERSION_MATRIX["stable"]["jdk"] == 17
    
    def test_incompatible_version_combination(self):
        """UT-VER-004: 不兼容版本组合应验证失败"""
        # AGP 8.7.0 + Gradle 7.5 应该失败
        agp = "8.7.0"
        gradle = "7.5"
        
        # 模拟验证函数
        def validate_version_combo(agp: str, gradle: str) -> bool:
            """验证 AGP/Gradle 版本组合"""
            agp_major = int(agp.split('.')[0])
            gradle_major = int(gradle.split('.')[0])
            
            # AGP 8.x 需要 Gradle 8+
            if agp_major == 8 and gradle_major < 8:
                return False
            
            # AGP 9.x 需要 Gradle 9+
            if agp_major == 9 and gradle_major < 9:
                return False
            
            return True
        
        assert validate_version_combo(agp, gradle) is False
    
    def test_kotlin_agp_compatibility(self):
        """UT-VER-005: Kotlin 与 AGP 兼容性"""
        kotlin_agp_compat = {
            "2.1.x": ["8.7+", "9.x"],
            "2.0.x": ["8.5+", "9.x"],
            "1.9.x": ["8.0+", "9.x"],
        }
        
        # stable 配置: AGP 8.7.0 + Kotlin 2.0.21
        agp = VERSION_MATRIX["stable"]["agp"]
        kotlin = VERSION_MATRIX["stable"]["kotlin"]
        
        # Kotlin 2.0.x 应该兼容 AGP 8.5+
        assert kotlin.startswith("2.0")
        assert agp == "8.7.0"
        
        # 验证兼容性逻辑
        def is_kotlin_compatible(kotlin_version: str, agp_version: str) -> bool:
            """检查 Kotlin 与 AGP 兼容性"""
            kotlin_major = int(kotlin_version.split('.')[0])
            kotlin_minor = int(kotlin_version.split('.')[1])
            
            agp_major = int(agp_version.split('.')[0])
            agp_minor = int(agp_version.split('.')[1])
            
            # Kotlin 2.0+ 需要 AGP 8.5+
            if kotlin_major >= 2 and kotlin_minor >= 0:
                if agp_major == 8 and agp_minor < 5:
                    return False
                if agp_major < 8:
                    return False
            
            return True
        
        assert is_kotlin_compatible(kotlin, agp) is True
    
    def test_gradle_version_comparison(self):
        """测试 Gradle 版本号比较"""
        def compare_versions(v1: str, v2: str) -> int:
            """比较版本号，返回 1 (v1>v2), 0 (v1==v2), -1 (v1<v2)"""
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            
            for i in range(max(len(parts1), len(parts2))):
                p1 = parts1[i] if i < len(parts1) else 0
                p2 = parts2[i] if i < len(parts2) else 0
                
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            
            return 0
        
        assert compare_versions("8.9", "8.7") == 1
        assert compare_versions("8.9", "8.9") == 0
        assert compare_versions("7.5", "8.0") == -1
        assert compare_versions("9.1.0", "9.0") == 1


# ============================================
# 测试组：配置模板渲染
# ============================================

class TestTemplateRendering:
    """配置模板渲染测试"""
    
    def test_replace_project_name(self):
        """UT-TPL-001: 替换项目名称"""
        template = 'rootProject.name = "MyApp"'
        project_name = "TestApp"
        
        rendered = template.replace("MyApp", project_name)
        
        assert rendered == 'rootProject.name = "TestApp"'
    
    def test_replace_package_name(self):
        """UT-TPL-002: 替换包名"""
        templates = [
            'namespace = "com.example.myapp"',
            'applicationId = "com.example.myapp"',
            'package com.example.myapp',
        ]
        
        old_package = "com.example.myapp"
        new_package = "com.test.app"
        
        for template in templates:
            rendered = template.replace(old_package, new_package)
            assert new_package in rendered
            assert old_package not in rendered
    
    def test_preserve_indentation(self):
        """UT-TPL-003: 保留格式缩进"""
        template = """plugins {
    id("com.android.application") version "8.7.0" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
}"""
        
        # 验证缩进格式
        lines = template.split('\n')
        for line in lines[1:3]:  # 跳过首行
            assert line.startswith('    '), f"Line should have 4-space indent: {line}"
    
    def test_handle_special_characters(self):
        """UT-TPL-004: 处理特殊字符"""
        def sanitize_project_name(name: str) -> str:
            """清理项目名称"""
            # 移除或替换非法字符
            import re
            # 只允许字母、数字、下划线
            sanitized = re.sub(r'[^a-zA-Z0-9_]', '', name)
            return sanitized or "MyApp"
        
        test_cases = [
            ("My App", "MyApp"),
            ("Test-App", "TestApp"),
            ("App@2024", "App2024"),
            ("我的应用", ""),
        ]
        
        for input_name, expected in test_cases:
            result = sanitize_project_name(input_name)
            if expected:
                assert result == expected
            else:
                # 中文应该被移除，返回默认值
                assert result == "MyApp"
    
    def test_render_settings_gradle_kts(self):
        """测试 settings.gradle.kts 渲染"""
        template = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "MyApp"
include(":app")"""
        
        project_name = "TestApp"
        rendered = template.replace('rootProject.name = "MyApp"', f'rootProject.name = "{project_name}"')
        
        assert f'rootProject.name = "{project_name}"' in rendered
        assert "pluginManagement" in rendered
        assert "google()" in rendered
    
    def test_render_build_gradle_kts(self):
        """测试 build.gradle.kts 渲染"""
        template = """plugins {
    id("com.android.application") version "AGP_VERSION" apply false
    id("org.jetbrains.kotlin.android") version "KOTLIN_VERSION" apply false
}"""
        
        replacements = {
            "AGP_VERSION": "8.7.0",
            "KOTLIN_VERSION": "2.0.21"
        }
        
        rendered = template
        for key, value in replacements.items():
            rendered = rendered.replace(key, value)
        
        assert 'version "8.7.0"' in rendered
        assert 'version "2.0.21"' in rendered
    
    def test_render_app_build_gradle_kts(self):
        """测试 app/build.gradle.kts 渲染"""
        template = """android {
    namespace = "com.example.myapp"
    compileSdk = COMPILE_SDK

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 24
        targetSdk = TARGET_SDK
    }
}"""
        
        replacements = {
            "com.example.myapp": "com.test.app",
            "COMPILE_SDK": "35",
            "TARGET_SDK": "35"
        }
        
        rendered = template
        for key, value in replacements.items():
            rendered = rendered.replace(key, value)
        
        assert 'namespace = "com.test.app"' in rendered
        assert 'compileSdk = 35' in rendered
        assert 'applicationId = "com.test.app"' in rendered


# ============================================
# 测试组：Gradle Wrapper 配置
# ============================================

class TestGradleWrapperConfig:
    """Gradle Wrapper 配置测试"""
    
    def test_gradle_wrapper_properties_format(self):
        """测试 gradle-wrapper.properties 格式"""
        template = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-{VERSION}-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists"""
        
        gradle_version = "8.9"
        rendered = template.replace("{VERSION}", gradle_version)
        
        assert f"gradle-{gradle_version}-bin.zip" in rendered
        assert "GRADLE_USER_HOME" in rendered
    
    def test_gradle_wrapper_url_valid(self):
        """测试 Gradle Wrapper URL 格式"""
        url_template = "https://services.gradle.org/distributions/gradle-{version}-bin.zip"
        
        for config_name, config in VERSION_MATRIX.items():
            gradle_version = config["gradle"]
            url = url_template.format(version=gradle_version)
            
            # 验证 URL 格式
            assert url.startswith("https://")
            assert gradle_version in url
            assert url.endswith("-bin.zip")


# ============================================
# 测试组：中国镜像配置
# ============================================

class TestChinaMirrorConfig:
    """国内镜像配置测试"""
    
    def test_china_mirror_settings_template(self):
        """测试国内镜像 settings.gradle.kts 模板"""
        template = """pluginManagement {
    repositories {
        maven { url = uri("https://maven.aliyun.com/repository/gradle-plugin") }
        maven { url = uri("https://maven.aliyun.com/repository/google") }
        maven { url = uri("https://maven.aliyun.com/repository/public") }
        gradlePluginPortal()
    }
}"""
        
        # 验证阿里云镜像 URL
        assert "maven.aliyun.com" in template
        assert "gradle-plugin" in template
        assert "google" in template
        assert "public" in template
    
    def test_mirror_url_valid(self):
        """测试镜像 URL 格式"""
        mirror_urls = [
            "https://maven.aliyun.com/repository/gradle-plugin",
            "https://maven.aliyun.com/repository/google",
            "https://maven.aliyun.com/repository/public",
        ]
        
        for url in mirror_urls:
            assert url.startswith("https://")
            assert "maven.aliyun.com" in url
    
    def test_international_vs_china_mirror(self):
        """测试国际版与国内版配置差异"""
        international_repos = ["google()", "mavenCentral()"]
        china_repos = [
            'maven { url = uri("https://maven.aliyun.com/repository/google") }',
            'maven { url = uri("https://maven.aliyun.com/repository/public") }'
        ]
        
        # 两者应该都提供相同的仓库（只是镜像不同）
        assert len(international_repos) == len(china_repos)


# ============================================
# 测试组：配置验证函数
# ============================================

class TestConfigValidation:
    """配置验证函数测试"""
    
    def test_validate_namespace(self):
        """测试 namespace 验证"""
        def is_valid_namespace(namespace: str) -> bool:
            """验证 namespace 格式"""
            if not namespace:
                return False
            
            # 至少包含一个点
            if '.' not in namespace:
                return False
            
            # 每个段必须是有效的标识符
            segments = namespace.split('.')
            for segment in segments:
                if not segment:
                    return False
                # 必须以字母开头
                if not segment[0].isalpha():
                    return False
                # 只能包含字母、数字、下划线
                if not all(c.isalnum() or c == '_' for c in segment):
                    return False
            
            return True
        
        valid_namespaces = [
            "com.example.app",
            "com.test.myapp",
            "org.company.project",
        ]
        
        invalid_namespaces = [
            "example",  # 缺少点
            "123.app",  # 以数字开头
            "com..app",  # 空段
            "",  # 空
            "com.example.my app",  # 包含空格
        ]
        
        for ns in valid_namespaces:
            assert is_valid_namespace(ns), f"Should be valid: {ns}"
        
        for ns in invalid_namespaces:
            assert not is_valid_namespace(ns), f"Should be invalid: {ns}"
    
    def test_validate_application_id(self):
        """测试 applicationId 验证"""
        # applicationId 规则与 namespace 类似
        def is_valid_application_id(app_id: str) -> bool:
            """验证 applicationId 格式"""
            if not app_id:
                return False
            
            # 可以包含字母、数字、下划线、点
            pattern = r'^[a-zA-Z][a-zA-Z0-9_\.]*$'
            return bool(re.match(pattern, app_id))
        
        valid_ids = [
            "com.example.app",
            "com.test.app123",
            "org.my_app",
        ]
        
        for app_id in valid_ids:
            assert is_valid_application_id(app_id), f"Should be valid: {app_id}"


# ============================================
# 测试组：配置文件完整性
# ============================================

class TestConfigCompleteness:
    """配置文件完整性测试"""
    
    def test_stable_config_completeness(self):
        """测试 stable 配置完整性"""
        config = VERSION_MATRIX["stable"]
        
        required_keys = ["agp", "gradle", "jdk", "kotlin", "compileSdk"]
        
        for key in required_keys:
            assert key in config, f"Missing key: {key}"
            assert config[key] is not None, f"Value is None for key: {key}"
    
    def test_legacy_config_compatibility(self):
        """测试 legacy 配置与 JDK 11 兼容"""
        config = VERSION_MATRIX["legacy"]
        
        # legacy 配置应该支持 JDK 11
        assert config["jdk"] == 11
        # AGP 应该是 7.x
        assert config["agp"].startswith("7.")
        # Gradle 应该是 7.x
        assert config["gradle"].startswith("7.")


# ============================================
# 测试标记
# ============================================

@pytest.mark.unit
class TestFastUnitTests:
    """快速单元测试标记"""
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
