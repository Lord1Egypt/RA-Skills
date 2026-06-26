# REPORTING

## 生成报告

```bash
python scripts/generate_report.py tests/unit
python scripts/generate_report.py tests/integration
python scripts/generate_report.py tests
```

## 报告输出

- HTML 报告：`reports/test-report.html`
- 摘要数据：`reports/test-results.json`
- 覆盖率报告：`reports/htmlcov/index.html`

## 重新渲染已有报告

```bash
python scripts/run_tests.py --report-only
```

这会基于 `reports/test-results.json` 重新生成 `reports/test-report.html`。

## 报告特性

- 默认英文
- 支持中英文切换
- 使用 Material 3 风格布局
- 使用相对路径显示报告位置

## 常用命令

```bash
python scripts/run_tests.py --unit
python scripts/run_tests.py --integration
python -m pytest tests -q
```

## 目的

这份文档只回答一件事：如何生成、重建和查看测试报告。
