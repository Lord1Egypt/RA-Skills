"""
Unit tests for data-quality-validator.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts"))

import unittest
import pandas as pd
import numpy as np
from data_profiler import DataProfiler
from schema_validator import SchemaValidator
from anomaly_detector import AnomalyDetector

class TestDataProfiler(unittest.TestCase):
    def test_profile_basic(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        p = DataProfiler()
        r = p.profile(df)
        self.assertEqual(r["row_count"], 3)
        self.assertEqual(r["column_count"], 2)
        self.assertEqual(r["missing"]["a"], 0)

    def test_profile_outliers(self):
        df = pd.DataFrame({"a": [1, 2, 3, 100]})
        p = DataProfiler()
        r = p.profile(df)
        self.assertEqual(r["outliers"]["a"]["count"], 1)

class TestSchemaValidator(unittest.TestCase):
    def test_type_check(self):
        df = pd.DataFrame({"age": [1, 2, 3]})
        v = SchemaValidator({"age": {"type": "int"}})
        self.assertEqual(len(v.validate(df)), 0)

    def test_range_violation(self):
        df = pd.DataFrame({"age": [200]})
        v = SchemaValidator({"age": {"type": "int", "max": 150}})
        errs = v.validate(df)
        self.assertTrue(any(e["error"] == "max_violation" for e in errs))

    def test_regex_mismatch(self):
        df = pd.DataFrame({"email": ["bad"]})
        v = SchemaValidator({"email": {"type": "str", "regex": r"^\S+@\S+\.\S+$"}})
        errs = v.validate(df)
        self.assertTrue(any(e["error"] == "regex_mismatch" for e in errs))

    def test_unique_violation(self):
        df = pd.DataFrame({"id": [1, 1, 2]})
        v = SchemaValidator({"id": {"type": "int", "unique": True}})
        errs = v.validate(df)
        self.assertTrue(any(e["error"] == "duplicate_values" for e in errs))

class TestAnomalyDetector(unittest.TestCase):
    def test_iqr(self):
        s = pd.Series([1, 2, 3, 4, 5, 100])
        d = AnomalyDetector("iqr")
        mask = d.detect(s)
        self.assertTrue(mask.iloc[-1])

    def test_zscore(self):
        s = pd.Series([1, 2, 3, 4, 5, 500])
        d = AnomalyDetector("zscore", threshold=2.0)
        mask = d.detect(s)
        self.assertTrue(mask.iloc[-1])

    def test_report(self):
        df = pd.DataFrame({"a": [1, 2, 3, 100]})
        d = AnomalyDetector("iqr")
        r = d.report(df, columns=["a"])
        self.assertEqual(r["a"]["anomaly_count"], 1)

if __name__ == "__main__":
    unittest.main()
