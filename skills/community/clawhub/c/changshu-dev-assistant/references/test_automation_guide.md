# 昌叔助手测试自动化功能使用指南

## 概述

昌叔助手的测试自动化功能为软件开发提供了完整的测试解决方案，包括测试用例生成、测试运行和覆盖率分析。

## 核心功能

### 1. 测试用例生成
- 支持pytest和unittest框架
- 基于源代码自动生成测试用例
- 支持类和函数的测试用例生成

### 2. 测试运行
- 集成主流测试框架
- 提供详细的测试报告
- 支持多种测试框架

### 3. 覆盖率分析
- 分析代码覆盖率
- 识别未覆盖的代码区域
- 提供覆盖率改进建议

## 使用方法

### 命令行使用
```bash
# 生成测试用例
changshu-assistant test-generate --file <source_file> --type <framework>

# 运行测试
changshu-assistant test-run --file <test_file> --type <framework>

# 分析测试覆盖率
changshu-assistant test-analyze --file <source_file> --test-file <test_file>
```

## 配置说明

在昌叔助手的配置文件中添加以下配置:
```yaml
features:
  test_automation: true

testing:
  frameworks:
    - pytest
    - unittest
```

## 验证结果

测试自动化功能已成功集成并验证，可以为昌叔提供完整的测试自动化解决方案。