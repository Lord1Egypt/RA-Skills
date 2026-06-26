#!/usr/bin/env python3
"""
pytest 配置文件

提供共享 fixtures 和配置
"""

import pytest
import sys
import tempfile
import shutil
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CACHE_ROOT = PROJECT_ROOT / "cache"
CACHE_ROOT.mkdir(parents=True, exist_ok=True)
sys.pycache_prefix = str(CACHE_ROOT / "pycache")

# 添加 scripts 目录到 Python 路径
scripts_path = PROJECT_ROOT / "scripts"
if scripts_path.exists():
    sys.path.insert(0, str(scripts_path))

# 将 pytest 产生的临时目录固定到 cache 下，避免污染项目根目录
workspace_temp_dir = CACHE_ROOT / "tmp" / "pytest"
workspace_temp_dir.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(workspace_temp_dir)


def make_workspace_temp_dir(prefix: str = "case") -> Path:
    """在工作区内创建稳定的测试目录，避免系统临时目录权限问题。"""
    path = workspace_temp_dir / f"{prefix}_{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def cleanup_workspace_temp_dir(path: Path) -> None:
    """清理测试目录；失败时忽略，避免因为清理权限导致测试报错。"""
    shutil.rmtree(path, ignore_errors=True)


# 注册标记
def pytest_configure(config):
    """配置 pytest"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# 共享 fixtures
@pytest.fixture
def temp_dir():
    """创建临时目录"""
    path = make_workspace_temp_dir("shared")
    try:
        yield path
    finally:
        cleanup_workspace_temp_dir(path)


@pytest.fixture
def sample_jdk_output_jdk17():
    """JDK 17 版本输出样本"""
    return '''openjdk version "17.0.1" 2023-10-17
OpenJDK Runtime Environment (build 17.0.1+12-39)
OpenJDK 64-Bit Server VM (build 17.0.1+12-39, mixed mode, sharing)'''


@pytest.fixture
def sample_jdk_output_jdk11():
    """JDK 11 版本输出样本"""
    return '''openjdk version "11.0.22" 2024-01-16
OpenJDK Runtime Environment (build 11.0.22+7-post-Debian-1deb11u1)
OpenJDK 64-Bit Server VM (build 11.0.22+7-post-Debian-1deb11u1, mixed mode, sharing)'''


@pytest.fixture
def sample_jdk_output_jdk8():
    """JDK 8 版本输出样本（旧格式）"""
    return '''java version "1.8.0_312"
Java(TM) SE Runtime Environment (build 1.8.0_312-b07)
Java HotSpot(TM) 64-Bit Server VM (build 25.312-b07, mixed mode)'''


@pytest.fixture
def sample_android_sdk_path():
    """Android SDK 路径样本"""
    return "/path/to/android/sdk"


@pytest.fixture
def sample_config_stable():
    """stable 配置样本"""
    return {
        "config": "stable",
        "agp": "8.7.0",
        "gradle": "8.9",
        "kotlin": "2.0.21",
        "jdk_required": "17",
        "warning": None
    }
