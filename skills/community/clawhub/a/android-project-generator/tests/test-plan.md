# Android Project Generator 测试计划

> 基于 TDD 方法设计的测试用例

## 测试策略

### 测试金字塔

```
        /\
       /  \    端到端测试（E2E）
      /----\   - 完整项目生成并编译验证
     /      \
    /--------\ 集成测试
   /          \ - 组件间协作验证
  /------------\
 /              \ 单元测试
/----------------\ - 函数级别验证
```

### 测试分层

| 层级 | 测试类型 | 数量 | 执行时间 | 覆盖目标 |
|------|---------|------|---------|---------|
| L1 | 单元测试 | 25+ | < 1s | 函数逻辑正确性 |
| L2 | 集成测试 | 10+ | < 5s | 组件协作正确性 |
| L3 | 端到端测试 | 5+ | 1-3 min | 完整流程验证 |

## 单元测试设计

### 1. detect_env.py 单元测试

#### 1.1 JDK 版本检测

**测试组：detect_jdk_version**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| UT-JDK-001 | 检测 JDK 17 | `java -version` 输出 "17.0.1" | `{"detected": true, "version": 17}` | P0 |
| UT-JDK-002 | 检测 JDK 21 | `java -version` 输出 "21.0.2" | `{"detected": true, "version": 21}` | P0 |
| UT-JDK-003 | 检测 JDK 11 | `java -version` 输出 "11.0.22" | `{"detected": true, "version": 11}` | P0 |
| UT-JDK-004 | 检测 JDK 8 (遗留格式) | `java -version` 输出 "1.8.0_312" | `{"detected": true, "version": 8}` | P0 |
| UT-JDK-005 | JDK 未安装 | `java -version` 命令不存在 | `{"detected": false, "error": "JDK not found"}` | P0 |
| UT-JDK-006 | 解析异常输出 | `java -version` 输出乱码 | `{"detected": false, "version": None}` | P1 |
| UT-JDK-007 | 检测 JDK 17 小版本 | `java -version` 输出 "17.0.13" | `{"detected": true, "version": 17}` | P1 |

**测试用例示例（Python pytest）：**

```python
# test_detect_env.py

import pytest
from unittest.mock import patch, MagicMock
from scripts.detect_env import detect_jdk_version

class TestDetectJdkVersion:
    """UT-JDK-001: 检测 JDK 17"""
    @patch('scripts.detect_env.run_command')
    def test_detect_jdk_17(self, mock_run):
        mock_run.return_value = (0, '', 'openjdk version "17.0.1" 2023-10-17')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 17

    """UT-JDK-002: 检测 JDK 21"""
    @patch('scripts.detect_env.run_command')
    def test_detect_jdk_21(self, mock_run):
        mock_run.return_value = (0, '', 'openjdk version "21.0.2" 2024-01-16')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 21

    """UT-JDK-004: 检测 JDK 8 (遗留格式)"""
    @patch('scripts.detect_env.run_command')
    def test_detect_jdk_8_legacy_format(self, mock_run):
        mock_run.return_value = (0, '', 'java version "1.8.0_312"')
        
        result = detect_jdk_version()
        
        assert result["detected"] is True
        assert result["version"] == 8

    """UT-JDK-005: JDK 未安装"""
    @patch('scripts.detect_env.run_command')
    def test_jdk_not_found(self, mock_run):
        mock_run.return_value = (-1, '', 'Command not found: java')
        
        result = detect_jdk_version()
        
        assert result["detected"] is False
        assert result["error"] == "JDK not found"
```

#### 1.2 Android SDK 检测

**测试组：detect_android_sdk**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| UT-SDK-001 | 检测 ANDROID_HOME 环境变量 | 设置 ANDROID_HOME=/path/to/sdk | `{"detected": true, "path": "/path/to/sdk"}` | P0 |
| UT-SDK-002 | 检测 ANDROID_SDK_ROOT 环境变量 | 设置 ANDROID_SDK_ROOT=/path/to/sdk | `{"detected": true, "path": "/path/to/sdk"}` | P0 |
| UT-SDK-003 | 检测常见路径 (Windows) | LOCALAPPDATA/Android/Sdk 存在 | 返回正确路径 | P0 |
| UT-SDK-004 | 检测常见路径 (macOS) | ~/Library/Android/sdk 存在 | 返回正确路径 | P0 |
| UT-SDK-005 | SDK 未安装 | 无环境变量，路径不存在 | `{"detected": false}` | P0 |
| UT-SDK-006 | 检测 build-tools 版本 | build-tools/ 包含多个版本 | 返回排序后的版本列表 | P1 |

```python
class TestDetectAndroidSdk:
    """UT-SDK-001: 检测 ANDROID_HOME 环境变量"""
    @patch.dict('os.environ', {'ANDROID_HOME': '/custom/sdk/path'})
    @patch('pathlib.Path.exists')
    def test_detect_android_home(self, mock_exists):
        mock_exists.return_value = True
        
        result = detect_android_sdk()
        
        assert result["detected"] is True
        assert result["path"] == "/custom/sdk/path"

    """UT-SDK-005: SDK 未安装"""
    @patch.dict('os.environ', {}, clear=True)
    @patch('pathlib.Path.exists')
    def test_sdk_not_found(self, mock_exists):
        mock_exists.return_value = False
        
        result = detect_android_sdk()
        
        assert result["detected"] is False
```

#### 1.3 配置推荐逻辑

**测试组：recommend_config**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| UT-CFG-001 | JDK 17+ 推荐 stable | `jdk_version=17` | `agp=8.7.0, gradle=8.9` | P0 |
| UT-CFG-002 | JDK 21 推荐 stable | `jdk_version=21` | `agp=8.7.0, gradle=8.9` | P0 |
| UT-CFG-003 | JDK 11 推荐 compatible | `jdk_version=11` | `agp=7.4.2, gradle=7.5` | P0 |
| UT-CFG-004 | JDK 8 推荐 legacy | `jdk_version=8` | `agp=7.4.2, gradle=7.5, warning` | P0 |
| UT-CFG-005 | 未检测到 JDK | `jdk_version=None` | 使用 conservative 配置 | P1 |

```python
class TestRecommendConfig:
    """UT-CFG-001: JDK 17+ 推荐 stable"""
    def test_jdk_17_recommends_stable(self):
        result = recommend_config(jdk_version=17)
        
        assert result["config"] == "stable"
        assert result["agp"] == "8.7.0"
        assert result["gradle"] == "8.9"
        assert result["warning"] is None

    """UT-CFG-003: JDK 11 推荐 compatible"""
    def test_jdk_11_recommends_compatible(self):
        result = recommend_config(jdk_version=11)
        
        assert result["config"] == "compatible"
        assert result["agp"] == "7.4.2"
        assert "升级" in result["warning"]

    """UT-CFG-004: JDK 8 推荐 legacy"""
    def test_jdk_8_recommends_legacy(self):
        result = recommend_config(jdk_version=8)
        
        assert "legacy" in result["config"]
        assert result["jdk_required"] == "11"
```

### 2. 配置生成单元测试

#### 2.1 版本兼容性验证

**测试组：version_compatibility**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| UT-VER-001 | AGP 8.7.0 需要 Gradle 8.9+ | AGP=8.7.0 | Gradle >= 8.9 | P0 |
| UT-VER-002 | AGP 9.1.0 需要 Gradle 9.3+ | AGP=9.1.0 | Gradle >= 9.3 | P0 |
| UT-VER-003 | AGP 8.x 需要 JDK 17 | AGP=8.x | JDK >= 17 | P0 |
| UT-VER-004 | 不兼容版本组合应报错 | AGP=8.7.0, Gradle=7.5 | 验证失败 | P0 |
| UT-VER-005 | Kotlin 与 AGP 兼容性 | AGP=8.7.0, Kotlin=2.0.21 | 验证通过 | P1 |

#### 2.2 配置模板渲染

**测试组：template_rendering**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| UT-TPL-001 | 替换项目名称 | 模板 + "MyApp" | 所有占位符替换为 MyApp | P0 |
| UT-TPL-002 | 替换包名 | 模板 + "com.example.myapp" | 包名正确替换 | P0 |
| UT-TPL-003 | 保留格式缩进 | 模板缩进 4 空格 | 输出保持缩进 | P1 |
| UT-TPL-004 | 处理特殊字符 | 项目名包含空格 | 正确处理或报错 | P1 |

## 集成测试设计

### 3. 项目结构生成测试

**测试组：project_structure_generation**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| IT-STR-001 | 生成完整项目结构 | 项目名=TestApp, stable 配置 | 所有必需文件存在 | P0 |
| IT-STR-002 | 文件权限正确 (Unix) | 生成 gradlew | 可执行权限 | P1 |
| IT-STR-003 | 目录层级正确 | 检查 app/src/main/... | 路径结构完整 | P0 |
| IT-STR-004 | AndroidManifest 正确 | 检查 manifest 文件 | 包含必需属性 | P0 |
| IT-STR-005 | 资源文件完整 | 检查 res/values/ | strings.xml, themes.xml 存在 | P0 |

```python
class TestProjectStructureGeneration:
    """IT-STR-001: 生成完整项目结构"""
    def test_generate_complete_structure(self, tmp_path):
        generator = ProjectGenerator(
            name="TestApp",
            package_name="com.example.testapp",
            config_profile="stable"
        )
        
        generator.generate(tmp_path)
        
        # 检查必需文件
        required_files = [
            "settings.gradle.kts",
            "build.gradle.kts",
            "gradle.properties",
            "gradle/wrapper/gradle-wrapper.properties",
            "gradlew",
            "gradlew.bat",
            "app/build.gradle.kts",
            "app/src/main/AndroidManifest.xml",
            "app/src/main/java/com/example/testapp/MainActivity.kt",
            "app/src/main/res/layout/activity_main.xml",
            "app/src/main/res/values/strings.xml",
            "app/src/main/res/values/themes.xml",
        ]
        
        for file_path in required_files:
            assert (tmp_path / file_path).exists(), f"Missing: {file_path}"
```

### 4. Gradle 配置集成测试

**测试组：gradle_configuration_integration**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| IT-GRAD-001 | stable 配置完整性 | 生成 stable 配置 | AGP/Gradle/Kotlin 版本匹配 | P0 |
| IT-GRAD-002 | legacy 配置完整性 | 生成 legacy 配置 | AGP 7.x / JDK 11 兼容 | P0 |
| IT-GRAD-003 | 国内镜像配置 | 指定 use_china_mirror=true | 使用阿里云镜像 | P0 |
| IT-GRAD-004 | namespace 正确设置 | 生成 app/build.gradle.kts | namespace 字段存在 | P0 |
| IT-GRAD-005 | Kotlin DSL 语法正确 | 所有 .kts 文件 | 语法可解析 | P0 |

## 端到端测试设计

### 5. 完整流程测试

**测试组：end_to_end**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| E2E-001 | stable 配置编译成功 | JDK 17, stable 配置 | `assembleDebug` 成功 | P0 |
| E2E-002 | legacy 配置编译成功 | JDK 11, legacy 配置 | `assembleDebug` 成功 | P0 |
| E2E-003 | 国内镜像编译成功 | 国内网络环境 + 镜像配置 | `assembleDebug` 成功 | P0 |
| E2E-004 | 多模块项目生成 | 指定多模块结构 | 项目编译成功 | P1 |
| E2E-005 | 项目名包含中文 | 项目名="我的应用" | 正确处理或友好报错 | P2 |

```python
import subprocess
import tempfile
from pathlib import Path

class TestEndToEnd:
    """E2E-001: stable 配置编译成功"""
    @pytest.mark.slow
    def test_stable_profile_compiles(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_path = Path(tmp_dir) / "TestApp"
            
            # 生成项目
            generator = ProjectGenerator(
                name="TestApp",
                package_name="com.example.testapp",
                config_profile="stable"
            )
            generator.generate(project_path)
            
            # 运行编译
            result = subprocess.run(
                ["./gradlew", "assembleDebug"],
                cwd=project_path,
                capture_output=True,
                timeout=300
            )
            
            assert result.returncode == 0, f"Build failed: {result.stderr.decode()}"
            assert (project_path / "app/build/outputs/apk/debug/app-debug.apk").exists()
```

### 6. 错误处理测试

**测试组：error_handling**

| 测试ID | 测试场景 | 输入/前置条件 | 预期输出 | 优先级 |
|--------|---------|--------------|---------|--------|
| ERR-001 | JDK 版本不匹配 | JDK 11 + AGP 8.x 配置 | 友好错误提示 | P0 |
| ERR-002 | Gradle 版本不匹配 | AGP 8.7 + Gradle 7.5 | 配置验证失败 | P0 |
| ERR-003 | 无效包名 | 包名="123.invalid" | 验证失败提示 | P0 |
| ERR-004 | 磁盘空间不足 | 模拟磁盘满 | 清晰错误信息 | P1 |
| ERR-005 | 网络超时 | 模拟网络故障 | 重试或降级提示 | P1 |

## 测试数据准备

### Mock 数据

```python
# fixtures/jdk_versions.py
JDK_VERSION_FIXTURES = {
    "jdk_8": {
        "stdout": "",
        "stderr": 'java version "1.8.0_312"\nJava(TM) SE Runtime Environment'
    },
    "jdk_11": {
        "stdout": "",
        "stderr": 'openjdk version "11.0.22" 2024-01-16'
    },
    "jdk_17": {
        "stdout": "",
        "stderr": 'openjdk version "17.0.1" 2023-10-17'
    },
    "jdk_21": {
        "stdout": "",
        "stderr": 'openjdk version "21.0.2" 2024-01-16'
    }
}

# fixtures/sdk_paths.py
SDK_PATH_FIXTURES = {
    "windows": Path("C:/Users/Test/AppData/Local/Android/Sdk"),
    "macos": Path("/Users/test/Library/Android/sdk"),
    "linux": Path("/home/test/Android/Sdk")
}
```

## 测试执行策略

### CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run unit tests
        run: |
          pip install pytest pytest-cov
          pytest tests/unit -v --cov=scripts

  integration-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - name: Run integration tests
        run: pytest tests/integration -v

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3
      - name: Run E2E tests
        run: pytest tests/e2e -v -m slow
```

### 测试覆盖率目标

| 模块 | 目标覆盖率 | 关键路径 |
|------|-----------|---------|
| detect_env.py | >= 90% | JDK/SDK 检测逻辑 |
| 配置生成 | >= 85% | 模板渲染 |
| 版本验证 | >= 95% | 兼容性检查 |

## 测试环境要求

### 必需环境

- Python 3.11+
- JDK 17 (用于运行 gradlew)
- Android SDK (用于 E2E 测试)
- pytest >= 7.0

### 可选环境

- NDK (测试 NDK 相关功能)
- 多个 JDK 版本 (测试兼容性)

## 测试执行命令

```bash
# 运行所有单元测试
pytest tests/unit -v

# 运行集成测试
pytest tests/integration -v

# 运行 E2E 测试 (需要完整环境)
pytest tests/e2e -v -m slow

# 生成覆盖率报告
pytest tests/ --cov=scripts --cov-report=html

# 只运行 P0 优先级测试
pytest tests/ -v -m p0
```

## 测试维护计划

### 定期更新

- [ ] 每季度更新版本兼容性测试数据
- [ ] 新增 AGP 版本时添加对应测试用例
- [ ] 监控测试执行时间，超过阈值需优化

### 测试债务管理

- 发现 Bug 必须先写失败测试
- 测试覆盖率低于目标时禁止新增功能
- 每月审查跳过的测试（@pytest.mark.skip）

---

**文档版本**: 1.0.0  
**创建日期**: 2026-03-28  
**维护者**: oahcfly
