# 测试套件使用指南

## 测试结构

```
tests/
├── conftest.py                 # Pytest 共享配置
├── test-plan.md                # 测试计划文档
├── unit/                       # 单元测试
│   ├── test_detect_env.py      # 环境检测脚本测试
│   └── test_config_generation.py # 配置生成测试
├── integration/                # 集成测试
│   └── test_project_structure.py # 项目结构生成测试
└── e2e/                        # 端到端测试
    └── test_e2e_compilation.py   # 完整编译流程测试
```

## 快速开始

### 安装依赖

```bash
pip install pytest pytest-cov pytest-mock
```

### 运行测试

```bash
# 运行所有单元测试
python -m pytest tests/unit -v

# 运行集成测试
python -m pytest tests/integration -v

# 运行端到端测试（需要完整环境）
python -m pytest tests/e2e -v --runslow

# 运行所有测试
python -m pytest tests/ -v

# 只运行 P0 优先级测试
python -m pytest tests/ -v -m p0

# 跳过慢速测试
python -m pytest tests/ -v -m "not slow"

# 生成覆盖率报告
python -m pytest tests/ --cov=scripts --cov-report=html:reports/htmlcov
```

## 测试分类

### 单元测试 (Unit Tests)
- **速度**: < 1 秒
- **目的**: 验证单个函数/类的行为
- **依赖**: 无外部依赖，使用 Mock
- **文件**: `tests/unit/test_*.py`

### 集成测试 (Integration Tests)
- **速度**: 1-5 秒
- **目的**: 验证组件间协作
- **依赖**: 文件系统，临时目录
- **文件**: `tests/integration/test_*.py`

### 端到端测试 (E2E Tests)
- **速度**: 1-3 分钟
- **目的**: 验证完整流程
- **依赖**: JDK 17+, Android SDK, Gradle
- **文件**: `tests/e2e/test_*.py`
- **标记**: `@pytest.mark.slow`

## 测试标记

使用 pytest 标记分类测试：

| 标记 | 说明 | 示例 |
|------|------|------|
| `@pytest.mark.unit` | 单元测试 | 快速验证 |
| `@pytest.mark.integration` | 集成测试 | 组件协作 |
| `@pytest.mark.e2e` | 端到端测试 | 完整流程 |
| `@pytest.mark.slow` | 慢速测试 | 编译测试 |
| `@pytest.mark.p0` | 关键测试 | 核心功能 |
| `@pytest.mark.requires_jdk17` | 需要 JDK 17 | 环境依赖 |

## 测试数据

测试数据定义在 `conftest.py` 和测试文件中：

### JDK 版本输出样本
- `sample_jdk_output_jdk17`: JDK 17 输出
- `sample_jdk_output_jdk11`: JDK 11 输出
- `sample_jdk_output_jdk8`: JDK 8 输出（遗留格式）

### 配置数据
- `stable_config`: stable 配置
- `legacy_config`: legacy 配置
- `china_mirror_repos`: 国内镜像仓库

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install pytest pytest-cov
      - name: Run unit tests
        run: python -m pytest tests/unit -v --cov=scripts

  integration-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - name: Run integration tests
        run: python -m pytest tests/integration -v

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: android-actions/setup-android@v3
      - name: Run E2E tests
        run: python -m pytest tests/e2e -v --runslow
```

## 测试覆盖率目标

| 模块 | 目标覆盖率 | 当前覆盖率 |
|------|-----------|-----------|
| detect_env.py | >= 90% | 待测量 |
| 配置生成 | >= 85% | 待测量 |
| 版本验证 | >= 95% | 待测量 |

查看覆盖率报告：

```bash
python -m pytest tests/ --cov=scripts --cov-report=html:reports/htmlcov
open reports/htmlcov/index.html
```

## 编写新测试

### TDD 流程

按照 **Red-Green-Refactor** 循环：

1. **Red**: 编写失败的测试
   ```python
   def test_new_feature():
       # 描述期望行为
       result = new_function()
       assert result == expected_value
   ```

2. **运行测试，确认失败**
   ```bash
   pytest tests/unit/test_new.py -v
   # 应该看到 FAIL
   ```

3. **Green**: 编写最小代码使测试通过
   ```python
   def new_function():
       return expected_value
   ```

4. **确认测试通过**
   ```bash
   pytest tests/unit/test_new.py -v
   # 应该看到 PASS
   ```

5. **Refactor**: 重构代码，保持测试通过

### 测试命名规范

- 测试文件: `test_<module_name>.py`
- 测试类: `Test<FeatureName>`
- 测试函数: `test_<scenario>_<expected_result>`

示例：
```python
# test_detect_env.py
class TestDetectJdkVersion:
    def test_jdk_17_detected_correctly(self):
        """UT-JDK-001: 检测 JDK 17"""
        pass
```

### 使用 Fixtures

```python
def test_with_fixture(temp_dir, stable_config):
    """使用共享 fixture"""
    # temp_dir 是临时目录
    # stable_config 是配置字典
    project_path = temp_dir / "TestApp"
    # ...
```

## 故障排查

### 常见问题

1. **ImportError: No module named 'scripts'**
   ```bash
   # 确保在项目根目录运行
   cd android-project-generator
   pytest tests/
   ```

2. **JDK 未检测到**
   ```bash
   # 检查 JDK 安装
   java -version
   
   # 设置 JAVA_HOME
   export JAVA_HOME=/path/to/jdk
   ```

3. **测试超时**
   ```bash
   # 增加超时时间
   pytest tests/e2e --timeout=300
   ```

4. **权限错误 (Unix)**
   ```bash
   # 给 gradlew 添加执行权限
   chmod +x gradlew
   ```

## 最佳实践

1. **测试隔离**: 每个测试独立，不依赖执行顺序
2. **使用 Mock**: 避免依赖外部资源（网络、文件系统）
3. **明确断言**: 一个测试验证一个行为
4. **有意义的名称**: 测试名称描述场景和期望
5. **保持快速**: 单元测试 < 100ms，集成测试 < 5s

## 参考资料

- [pytest 文档](https://docs.pytest.org/)
- [pytest-cov 文档](https://pytest-cov.readthedocs.io/)
- [测试驱动开发 (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)
