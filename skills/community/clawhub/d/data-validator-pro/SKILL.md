---
name: data-quality-validator
description: Data quality validation and profiling toolkit for tabular data. Use when checking data completeness, detecting anomalies, validating schemas, profiling datasets, or assessing data cleanliness. Triggers on phrases like "data quality", "data validation", "schema validation", "data profiling", "missing data", "anomaly detection", "data completeness", "dirty data".
---

# Data Quality Validator

Toolkit for validating and profiling tabular data quality.

## Features

- **Schema validation** - Check column types, constraints, and rules
- **Completeness analysis** - Missing value detection and reporting
- **Anomaly detection** - Statistical outlier detection
- **Profiling** - Summary statistics and distribution analysis
- **Constraint checking** - Range checks, uniqueness, regex patterns

## Quick Start

```python
from scripts.data_profiler import DataProfiler
from scripts.schema_validator import SchemaValidator

# Profile a dataset
profiler = DataProfiler()
report = profiler.profile(df)  # pandas DataFrame
print(report["missing"])
print(report["outliers"])

# Validate against schema
schema = {
    "age": {"type": "int", "min": 0, "max": 150},
    "email": {"type": "str", "regex": r"^\S+@\S+\.\S+$"},
    "id": {"type": "int", "unique": True}
}
validator = SchemaValidator(schema)
errors = validator.validate(df)
for err in errors:
    print(err)
```

## Scripts

- `scripts/data_profiler.py` - Dataset profiling and summary stats
- `scripts/schema_validator.py` - Schema-based validation engine
- `scripts/anomaly_detector.py` - Statistical anomaly detection

## References

- `references/validation_rules.md` - Common validation patterns
