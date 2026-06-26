#!/usr/bin/env python3
"""
detect_env.py 单元测试

测试环境检测脚本的各个功能模块
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# 添加 scripts 目录到路径
scripts_path = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from detect_env import (
    run_command,
    detect_jdk_version,
    detect_java_home,
    detect_path_java,
    detect_gradle_jdk_context,
    detect_android_sdk,
    detect_ndk,
    detect_native_intent,
    resolve_native_enabled,
    assess_environment,
    recommend_config,
    main
)


# ============================================
# 测试组：run_command
# ============================================

class TestRunCommand:
    """命令执行测试"""
    
    def test_run_command_success(self):
        """测试成功执行命令"""
        returncode, stdout, stderr = run_command([sys.executable, "-c", "print('test')"])
        assert returncode == 0
        assert "test" in stdout
    
    def test_run_command_not_found(self):
        """测试命令不存在"""
        returncode, stdout, stderr = run_command(["nonexistent_command_xyz"])
        assert returncode == -1
        assert "Command not found" in stderr
    
    @patch('subprocess.run')
    def test_run_command_timeout(self, mock_run):
        """测试命令超时"""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=1)
        
        returncode, stdout, stderr = run_command(["sleep", "10"])
        assert returncode == -1
        assert "timed out" in stderr


# ============================================
# 测试组：detect_jdk_version
# ============================================

class TestDetectJdkVersion:
    """JDK 版本检测测试"""
    
    @patch('detect_env.run_command')
    def test_detect_jdk_17(self, mock_run):
        """UT-JDK-001: 检测 JDK 17"""
        mock_run.return_value = (0, '', 'openjdk version "17.0.1" 2023-10-17')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 17
        assert "17.0.1" in result["raw"]
    
    @patch('detect_env.run_command')
    def test_detect_jdk_21(self, mock_run):
        """UT-JDK-002: 检测 JDK 21"""
        mock_run.return_value = (0, '', 'openjdk version "21.0.2" 2024-01-16')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 21
    
    @patch('detect_env.run_command')
    def test_detect_jdk_11(self, mock_run):
        """UT-JDK-003: 检测 JDK 11"""
        mock_run.return_value = (0, '', 'openjdk version "11.0.22" 2024-01-16')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 11
    
    @patch('detect_env.run_command')
    def test_detect_jdk_8_legacy_format(self, mock_run):
        """UT-JDK-004: 检测 JDK 8 (遗留格式 1.8.x)"""
        mock_run.return_value = (0, '', 'java version "1.8.0_312"\nJava(TM) SE Runtime Environment')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 8
    
    @patch('detect_env.run_command')
    def test_jdk_not_found(self, mock_run):
        """UT-JDK-005: JDK 未安装"""
        mock_run.return_value = (-1, '', '')
        
        result = detect_jdk_version()
        
        assert result["detected"] is False
    
    @patch('detect_env.run_command')
    def test_detect_jdk_malformed_output(self, mock_run):
        """UT-JDK-006: 解析异常输出"""
        mock_run.return_value = (0, '', 'This is not a valid java version output')
        
        result = detect_jdk_version()
        
        assert result["detected"] is False
        assert result["version"] is None
    
    @patch('detect_env.run_command')
    def test_detect_jdk_17_minor_version(self, mock_run):
        """UT-JDK-007: 检测 JDK 17 小版本"""
        mock_run.return_value = (0, '', 'openjdk version "17.0.13" 2024-10-15')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 17
    
    @patch('detect_env.run_command')
    def test_detect_jdk_oracle_format(self, mock_run):
        """测试 Oracle JDK 格式"""
        mock_run.return_value = (
            0, 
            '', 
            'java version "17.0.1" 2023-10-17 LTS\n'
            'Java(TM) SE Runtime Environment (build 17.0.1+12-LTS-16)'
        )
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 17
    
    @patch('detect_env.run_command')
    def test_detect_jdk_zulu_format(self, mock_run):
        """测试 Azul Zulu JDK 格式"""
        mock_run.return_value = (
            0, 
            '', 
            'openjdk version "17.0.9" 2023-10-17 LTS\n'
            'OpenJDK Runtime Environment Zulu17.46+19-CA (build 17.0.9+9-LTS)'
        )
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 17
    
    @patch('detect_env.run_command')
    def test_detect_jdk_error_in_stderr(self, mock_run):
        """测试 java -version 输出到 stderr 的情况"""
        # java -version 通常将版本信息输出到 stderr
        mock_run.return_value = (0, '', 'openjdk version "17.0.1" 2023-10-17')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 17


class TestDetectJavaHome:
    """JAVA_HOME 检测测试"""

    @patch.dict(os.environ, {"JAVA_HOME": "/jdks/temurin-17"}, clear=True)
    @patch("detect_env.run_command")
    def test_detect_java_home_when_configured(self, mock_run):
        mock_run.return_value = (0, "", 'openjdk version "17.0.10" 2024-01-16')

        result = detect_java_home()

        assert result["configured"] is True
        assert result["path"] == "/jdks/temurin-17"
        assert result["version"] == 17

    @patch.dict(os.environ, {}, clear=True)
    def test_detect_java_home_when_missing(self):
        result = detect_java_home()
        assert result["configured"] is False
        assert result["path"] is None


class TestDetectPathJava:
    """PATH 中 java 检测测试"""

    @patch("detect_env.run_command")
    def test_detect_path_java_when_available(self, mock_run):
        mock_run.side_effect = [
            (0, "/usr/bin/java\n", ""),
            (0, "", 'openjdk version "17.0.8" 2023-07-18'),
        ]

        result = detect_path_java()

        assert result["detected"] is True
        assert result["path"] == "/usr/bin/java"
        assert result["version"] == 17

    @patch("detect_env.run_command")
    def test_detect_path_java_when_missing(self, mock_run):
        mock_run.return_value = (-1, "", "Command not found")

        result = detect_path_java()

        assert result["detected"] is False
        assert result["path"] is None


class TestDetectGradleJdkContext:
    """Gradle JDK 来源检测测试"""

    def test_prefers_java_home_when_available(self):
        result = detect_gradle_jdk_context(
            {"configured": True, "path": "/jdks/17", "version": 17},
            {"detected": True, "path": "/usr/bin/java", "version": 11},
        )

        assert result["gradle_jdk_source"] == "JAVA_HOME"
        assert result["gradle_jdk_path"] == "/jdks/17"
        assert result["consistency_warning"] is not None

    def test_falls_back_to_path_java(self):
        result = detect_gradle_jdk_context(
            {"configured": False, "path": None, "version": None},
            {"detected": True, "path": "/usr/bin/java", "version": 17},
        )

        assert result["gradle_jdk_source"] == "PATH"
        assert result["gradle_jdk_path"] == "/usr/bin/java"

    def test_reports_missing_jdk_source(self):
        result = detect_gradle_jdk_context(
            {"configured": False, "path": None, "version": None},
            {"detected": False, "path": None, "version": None},
        )

        assert result["gradle_jdk_source"] == "none"
        assert result["gradle_jdk_path"] is None


# ============================================
# 测试组：detect_android_sdk
# ============================================

class TestDetectAndroidSdk:
    """Android SDK 检测测试"""
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.iterdir')
    @patch.dict(os.environ, {'ANDROID_HOME': '/custom/android/sdk'}, clear=True)
    def test_detect_android_home(self, mock_iterdir, mock_exists):
        """UT-SDK-001: 检测 ANDROID_HOME 环境变量"""
        mock_exists.return_value = True
        mock_iterdir.return_value = []
        
        result = detect_android_sdk()
        
        assert result["detected"] is True
        assert result["path"] == "/custom/android/sdk"
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.iterdir')
    @patch.dict(os.environ, {'ANDROID_SDK_ROOT': '/sdk/root/path'}, clear=True)
    def test_detect_android_sdk_root(self, mock_iterdir, mock_exists):
        """UT-SDK-002: 检测 ANDROID_SDK_ROOT 环境变量"""
        mock_exists.return_value = True
        mock_iterdir.return_value = []
        
        result = detect_android_sdk()
        
        assert result["detected"] is True
        assert result["path"] == "/sdk/root/path"

    @patch.dict(os.environ, {}, clear=True)
    def test_detect_android_sdk_collects_components(self, temp_dir):
        """检测 SDK 组件清单"""
        sdk_root = temp_dir / "sdk"
        (sdk_root / "build-tools" / "35.0.0").mkdir(parents=True)
        (sdk_root / "build-tools" / "34.0.0").mkdir(parents=True)
        (sdk_root / "platforms" / "android-35").mkdir(parents=True)
        (sdk_root / "platforms" / "android-34").mkdir(parents=True)
        (sdk_root / "cmdline-tools" / "latest").mkdir(parents=True)
        (sdk_root / "licenses").mkdir(parents=True)
        (sdk_root / "licenses" / "android-sdk-license").write_text("accepted")

        with patch.dict(os.environ, {"ANDROID_HOME": str(sdk_root)}, clear=True):
            result = detect_android_sdk()

        assert result["detected"] is True
        assert result["build_tools_versions"][:2] == ["35.0.0", "34.0.0"]
        assert result["platform_versions"][:2] == ["android-35", "android-34"]
        assert result["cmdline_tools_installed"] is True
        assert result["licenses_present"] is True


# ============================================
# 测试组：detect_ndk
# ============================================

class TestDetectNdk:
    """NDK 检测测试"""
    
    @patch('pathlib.Path.exists')
    @patch.dict(os.environ, {'ANDROID_NDK_HOME': '/ndk/path'}, clear=False)
    def test_detect_ndk_from_env(self, mock_exists):
        """测试从环境变量检测 NDK"""
        mock_exists.return_value = False  # source.properties 不存在
        
        result = detect_ndk()
        
        assert result["detected"] is True
        assert result["path"] == "/ndk/path"
    
    @patch('pathlib.Path.exists')
    @patch.dict(os.environ, {}, clear=True)
    def test_detect_ndk_from_sdk_bundle(self, mock_exists):
        """测试从 SDK ndk-bundle 检测 NDK"""
        mock_exists.return_value = False
        
        result = detect_ndk(sdk_path="/android/sdk")
        
        # 应该尝试查找 ndk-bundle
        assert result["detected"] is False
    
    @patch('pathlib.Path.read_text', return_value='Pkg.Revision = 25.2.9519653')
    @patch('pathlib.Path.exists')
    @patch.dict(os.environ, {'ANDROID_NDK_HOME': '/ndk/path'}, clear=False)
    def test_detect_ndk_version(self, mock_exists, mock_read_text):
        """测试解析 NDK 版本"""
        mock_exists.return_value = True
        
        result = detect_ndk()
        
        assert result["detected"] is True
        assert result["version"] == "25.2.9519653"
    
    @patch('pathlib.Path.exists')
    @patch.dict(os.environ, {}, clear=True)
    def test_ndk_not_found(self, mock_exists):
        """测试 NDK 未找到"""
        mock_exists.return_value = False
        
        result = detect_ndk()
        
        assert result["detected"] is False


# ============================================
# 测试组：recommend_config
# ============================================

class TestRecommendConfig:
    """配置推荐测试"""
    
    def test_jdk_17_recommends_stable(self):
        """UT-CFG-001: JDK 17+ 推荐 stable"""
        result = recommend_config(jdk_version=17)
        
        assert result["config"] == "stable"
        assert result["agp"] == "8.7.0"
        assert result["gradle"] == "8.9"
        assert result["kotlin"] == "2.0.21"
        assert result["jdk_required"] == "17"
        assert result["warning"] is None
    
    def test_jdk_21_recommends_stable(self):
        """UT-CFG-002: JDK 21 推荐 stable"""
        result = recommend_config(jdk_version=21)
        
        assert result["config"] == "stable"
        assert result["agp"] == "8.7.0"
        assert result["warning"] is None
    
    def test_jdk_11_recommends_compatible(self):
        """UT-CFG-003: JDK 11 推荐 compatible"""
        result = recommend_config(jdk_version=11)
        
        assert result["config"] == "compatible"
        assert result["agp"] == "7.4.2"
        assert result["gradle"] == "7.5"
        assert result["jdk_required"] == "11"
        assert "升级" in result["warning"]


class TestAssessEnvironment:
    """环境可构建性评估测试"""

    def test_assess_environment_ready(self):
        """完整环境应标记为可构建"""
        result = assess_environment(
            {"detected": True, "version": 17},
            {"configured": True, "path": "/jdks/17", "version": 17},
            {"detected": True, "path": "/usr/bin/java", "version": 17},
            {
                "gradle_jdk_source": "JAVA_HOME",
                "gradle_jdk_path": "/jdks/17",
                "consistency_warning": None,
            },
            {
                "detected": True,
                "path": "/sdk",
                "build_tools_versions": ["35.0.0"],
                "platform_versions": ["android-35"],
                "cmdline_tools_installed": True,
                "licenses_present": True,
            },
            {"detected": False, "path": None}
        )

        assert result["ready_for_build"] is True
        assert result["blocking_issues"] == []

    def test_assess_environment_reports_blockers(self):
        """缺少关键组件时应返回阻断项"""
        result = assess_environment(
            {"detected": False, "version": None},
            {"configured": False, "path": None, "version": None},
            {"detected": False, "path": None, "version": None},
            {
                "gradle_jdk_source": "none",
                "gradle_jdk_path": None,
                "consistency_warning": None,
            },
            {
                "detected": True,
                "path": "/sdk",
                "build_tools_versions": [],
                "platform_versions": [],
                "cmdline_tools_installed": False,
                "licenses_present": False,
            },
            {"detected": False, "path": None}
        )

        assert result["ready_for_build"] is False
        assert result["status"] == "blocked"
        assert any("JDK not detected" in issue for issue in result["blocking_issues"])
        assert any("build-tools" in issue for issue in result["blocking_issues"])
        assert any("platforms/android-35" in issue for issue in result["blocking_issues"])
        assert any("licenses" in issue for issue in result["blocking_issues"])

    def test_assess_environment_marks_missing_java_home_as_degraded(self):
        result = assess_environment(
            {"detected": True, "version": 17},
            {"configured": False, "path": None, "version": None},
            {"detected": True, "path": "/usr/bin/java", "version": 17},
            {
                "gradle_jdk_source": "PATH",
                "gradle_jdk_path": "/usr/bin/java",
                "consistency_warning": None,
            },
            {
                "detected": True,
                "path": "/sdk",
                "build_tools_versions": ["35.0.0"],
                "platform_versions": ["android-35"],
                "cmdline_tools_installed": True,
                "licenses_present": True,
            },
            {"detected": False, "path": None}
        )

        assert result["ready_for_build"] is True
        assert result["status"] == "degraded"
        assert any("JAVA_HOME" in warning for warning in result["warnings"])
    
    def test_jdk_8_recommends_legacy(self):
        """UT-CFG-004: JDK 8 推荐 legacy"""
        result = recommend_config(jdk_version=8)
        
        # JDK < 11 应该返回 legacy 或 compatible 配置
        assert result["config"] in ["legacy", "compatible"]
        assert result["agp"] == "7.4.2"
        assert result["jdk_required"] == "11"
        assert result["warning"] is not None
    
    def test_jdk_none_uses_conservative(self):
        """UT-CFG-005: 未检测到 JDK 使用保守配置"""
        result = recommend_config(jdk_version=None)
        
        assert result["config"] in ["legacy", "compatible"]
        assert result["warning"] is not None
    
    def test_jdk_15_recommends_compatible(self):
        """测试 JDK 15 (11 <= version < 17) 使用 compatible"""
        result = recommend_config(jdk_version=15)
        
        assert result["config"] == "compatible"
        assert result["agp"] == "7.4.2"
    
    def test_jdk_12_recommends_compatible(self):
        """测试 JDK 12 (11 <= version < 17) 使用 compatible"""
        result = recommend_config(jdk_version=12)
        
        assert result["config"] == "compatible"
        assert result["agp"] == "7.4.2"


class TestNativeIntent:
    """Native 触发判定测试"""

    def test_strong_keywords_enable_native(self):
        result = detect_native_intent("请创建一个包含 JNI 和 C++ 的 Android native工程")

        assert result["native_candidate"] is True
        assert result["native_enabled"] is True
        assert result["needs_confirmation"] is False
        assert "jni" in result["matched_strong_keywords"]

    def test_weak_keywords_require_confirmation(self):
        result = detect_native_intent("这个项目要做性能优化，可能涉及底层能力")

        assert result["native_candidate"] is True
        assert result["native_enabled"] is False
        assert result["needs_confirmation"] is True
        assert "性能优化" in result["matched_weak_keywords"]

    def test_explicit_override_has_priority(self):
        result = resolve_native_enabled("加入 JNI 与 CMake", explicit_native_enabled=False)

        assert result["native_enabled"] is False
        assert result["decision_source"] == "explicit_flag"


# ============================================
# 测试组：main 函数
# ============================================

class TestMain:
    """主函数测试"""
    
    @patch('detect_env.detect_jdk_version')
    @patch('detect_env.detect_java_home')
    @patch('detect_env.detect_path_java')
    @patch('detect_env.detect_gradle_jdk_context')
    @patch('detect_env.detect_android_sdk')
    @patch('detect_env.detect_ndk')
    @patch('detect_env.recommend_config')
    def test_main_returns_dict(
        self, 
        mock_recommend, 
        mock_ndk, 
        mock_sdk, 
        mock_gradle_context,
        mock_path_java,
        mock_java_home,
        mock_jdk
    ):
        """测试 main 函数返回完整字典"""
        mock_jdk.return_value = {"detected": True, "version": 17, "raw": "17.0.1"}
        mock_java_home.return_value = {"configured": True, "path": "/jdks/17", "version": 17}
        mock_path_java.return_value = {"detected": True, "path": "/usr/bin/java", "version": 17}
        mock_gradle_context.return_value = {"gradle_jdk_source": "JAVA_HOME", "gradle_jdk_path": "/jdks/17", "consistency_warning": None}
        mock_sdk.return_value = {"detected": True, "path": "/sdk", "build_tools_versions": []}
        mock_ndk.return_value = {"detected": False, "path": None}
        mock_recommend.return_value = {
            "config": "stable",
            "agp": "8.7.0",
            "gradle": "8.9",
            "kotlin": "2.0.21",
            "jdk_required": "17",
            "warning": None
        }
        
        result = main()
        
        assert "jdk" in result
        assert "java_home" in result
        assert "path_java" in result
        assert "gradle_jdk_context" in result
        assert "android_sdk" in result
        assert "ndk" in result
        assert "native_decision" in result
        assert "recommended_config" in result
        assert "environment_assessment" in result
        assert isinstance(result, dict)
    
    @patch('detect_env.detect_jdk_version')
    @patch('detect_env.detect_java_home')
    @patch('detect_env.detect_path_java')
    @patch('detect_env.detect_gradle_jdk_context')
    @patch('detect_env.detect_android_sdk')
    @patch('detect_env.detect_ndk')
    @patch('detect_env.recommend_config')
    def test_main_handles_missing_jdk(
        self, 
        mock_recommend, 
        mock_ndk, 
        mock_sdk, 
        mock_gradle_context,
        mock_path_java,
        mock_java_home,
        mock_jdk
    ):
        """测试 main 处理 JDK 缺失情况"""
        mock_jdk.return_value = {"detected": False, "error": "JDK not found", "version": None}
        mock_java_home.return_value = {"configured": False, "path": None, "version": None}
        mock_path_java.return_value = {"detected": False, "path": None, "version": None}
        mock_gradle_context.return_value = {"gradle_jdk_source": "none", "gradle_jdk_path": None, "consistency_warning": None}
        mock_sdk.return_value = {"detected": False, "path": None, "build_tools_versions": []}
        mock_ndk.return_value = {"detected": False, "path": None}
        mock_recommend.return_value = {
            "config": "unknown",
            "agp": "7.4.2",
            "gradle": "7.5",
            "kotlin": "1.9.22",
            "jdk_required": "11",
            "warning": "无法确定 JDK 版本，使用保守配置"
        }
        
        result = main()
        
        assert result["jdk"]["detected"] is False
        assert result["environment_assessment"]["ready_for_build"] is False


# ============================================
# 测试标记
# ============================================

# 标记慢速测试
@pytest.mark.slow
class TestSlowOperations:
    """慢速操作测试（需要实际环境）"""
    
    def test_actual_jdk_detection(self):
        """实际 JDK 检测（需要真实 JDK 环境）"""
        result = detect_jdk_version()
        
        # 如果环境中有 JDK，应该检测到
        # 否则应该返回 detected=False
        assert "detected" in result


# ============================================
# Pytest 配置
# ============================================

def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
