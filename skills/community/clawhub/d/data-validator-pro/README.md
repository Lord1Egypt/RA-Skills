# Data Quality Validator

Data quality validation and profiling toolkit for tabular data.

## 功能 | Features

- 数据画像 | Data profiling (statistics, distributions)
- 模式验证 | Schema validation (types, ranges, regex)
- 缺失值分析 | Missing value analysis
- 异常检测 | Anomaly detection (IQR, Z-score)
- 约束检查 | Constraint checking (uniqueness, enums)

## 安装 | Installation

```bash
pip install -r requirements.txt
```

## 快速开始 | Quick Start

```python
from scripts.data_profiler import DataProfiler
from scripts.schema_validator import SchemaValidator

profiler = DataProfiler()
report = profiler.profile(df)

schema = {"age": {"type": "int", "min": 0, "max": 120}}
validator = SchemaValidator(schema)
errors = validator.validate(df)
```

## 目录结构 | Structure

```
data-quality-validator/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── data_profiler.py
│   ├── schema_validator.py
│   └── anomaly_detector.py
├── examples/
│   └── basic_usage.py
└── tests/
    └── test_validator.py
```
