---
name: auto-test
description: 自动生成单元测试。分析代码逻辑，自动生成 pytest (Python)、JUnit (Java)、Jest (JavaScript) 等测试框架的测试用例。支持覆盖率报告生成。
---

# Auto-Test - 自动单元测试生成

智能自动生成单元测试，提升代码覆盖率，减少手动测试工作量。

## 核心功能

- 🧪 **自动测试生成** - 分析函数/方法，生成对应测试用例
- 📊 **覆盖率报告** - 集成 pytest-cov, Jacoco, Istanbul 等
- 🔄 **多框架支持** - pytest, unittest, JUnit, Jest, Vitest
- 🎯 **边界测试** - 自动生成边界条件、异常测试
- 📝 **测试文档** - 生成测试说明和断言解释

## 使用场景

- 新功能开发后快速生成测试
- 遗留代码补充测试覆盖
- 重构前确保行为不变
- 代码审查时提供测试证据

## 快速开始

```bash
# 分析项目并生成测试
python3 scripts/generate-tests.py --path /path/to/project --framework pytest

# 生成覆盖率报告
python3 scripts/generate-tests.py --path . --coverage --output coverage.html

# 仅分析不生成（预览）
python3 scripts/generate-tests.py --path . --dry-run
```

## 配置选项

| 参数 | 说明 | 默认 |
|------|------|------|
| `--path` | 项目路径 | `.` |
| `--framework` | 测试框架 | `pytest` |
| `--coverage` | 生成覆盖率 | `false` |
| `--output` | 输出文件/目录 | `./tests/` |
| `--dry-run` | 仅预览 | `false` |
| `--exclude` | 排除目录 | `node_modules,vendor,target` |

## 支持的语言与框架

| 语言 | 框架 | 状态 |
|------|------|------|
| Python | pytest, unittest | ✅ 完整 |
| Java | JUnit 4/5, TestNG | ✅ 完整 |
| JavaScript/TypeScript | Jest, Vitest, Mocha | ✅ 完整 |
| Go | testing | ✅ 完整 |
| Rust | cargo test | ✅ 完整 |
| C# | NUnit, xUnit | 🚧 开发中 |

## 输出示例

```python
# 生成的测试 (pytest)
def test_process_order_valid():
    """测试有效订单处理"""
    order = Order(id=1, items=[...], total=100.0)
    result = process_order(order)
    assert result.status == "completed"
    assert result.processed_at is not None

def test_process_order_invalid_total():
    """测试无效订单总金额"""
    order = Order(id=2, items=[...], total=-10.0)
    with pytest.raises(InvalidOrderError):
        process_order(order)

def test_process_order_empty_items():
    """测试空购物车"""
    order = Order(id=3, items=[], total=0.0)
    with pytest.raises(EmptyCartError):
        process_order(order)
```

## 工作流程

1. **代码分析** - 解析 AST，识别函数、类、方法
2. **逻辑提取** - 理解输入、输出、副作用、异常
3. **测试生成** - 生成对应测试框架的测试代码
4. **覆盖率计算** - 运行测试，生成覆盖率报告
5. **结果输出** - 保存测试文件，提供总结

## 集成建议

- 结合 `pre-commit` hook，提交前自动生成测试
- 与 CI/CD 集成，确保新代码有测试覆盖
- 使用 `--dry-run` 预览，避免覆盖现有测试
