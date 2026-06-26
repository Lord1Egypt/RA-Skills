#!/usr/bin/env python3
"""
Basic usage examples for data-quality-validator.
"""
import sys
sys.path.insert(0, "../scripts")

import pandas as pd
from data_profiler import DataProfiler
from schema_validator import SchemaValidator
from anomaly_detector import AnomalyDetector

def demo_profiler():
    df = pd.DataFrame({
        "age": [25, 30, None, 200, 45],
        "name": ["Alice", "Bob", "Charlie", "Dave", "Eve"],
        "salary": [50000, 60000, 55000, None, 70000],
    })
    profiler = DataProfiler()
    report = profiler.profile(df)
    print("Profile report:", report)

def demo_validator():
    df = pd.DataFrame({
        "age": [25, 30, 200, -5],
        "email": ["a@b.com", "bad", "c@d.com", "e@f.com"],
    })
    schema = {
        "age": {"type": "int", "min": 0, "max": 150},
        "email": {"type": "str", "regex": r"^\S+@\S+\.\S+$"},
    }
    validator = SchemaValidator(schema)
    errors = validator.validate(df)
    print("Validation errors:", errors)

def demo_anomaly():
    df = pd.DataFrame({"value": [1, 2, 3, 4, 5, 100]})
    detector = AnomalyDetector(method="iqr")
    report = detector.report(df, columns=["value"])
    print("Anomaly report:", report)

if __name__ == "__main__":
    demo_profiler()
    demo_validator()
    demo_anomaly()
