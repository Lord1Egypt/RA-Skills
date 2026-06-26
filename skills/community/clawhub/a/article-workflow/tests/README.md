# Tests

单元测试目录。

## 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_dedup.py

# 详细输出
python -m pytest tests/ -v

# 覆盖率报告
python -m pytest tests/ --cov=core
```

## 测试文件

- `test_dedup.py` - URL 去重和混合去重测试
- `test_scorer.py` - 质量评分测试（待创建）
- `test_analyzer.py` - 文章分析测试（待创建）

## 依赖

```bash
pip install pytest pytest-cov
```
