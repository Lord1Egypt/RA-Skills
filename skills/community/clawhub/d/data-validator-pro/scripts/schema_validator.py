"""
Schema validator for constraint checking.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import re

class SchemaValidator:
    def __init__(self, schema: Dict[str, Dict[str, Any]]):
        self.schema = schema

    def validate(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        errors = []
        for col, rules in self.schema.items():
            if col not in df.columns:
                errors.append({"column": col, "error": "missing_column", "message": f"Column '{col}' not found"})
                continue
            series = df[col]
            # Type check
            expected_type = rules.get("type")
            if expected_type:
                valid = self._check_type(series, expected_type)
                if not valid["ok"]:
                    errors.append({"column": col, "error": "type_mismatch", "message": valid["message"]})
            # Range check
            if "min" in rules:
                invalid = series[series < rules["min"]]
                if not invalid.empty:
                    errors.append({"column": col, "error": "min_violation", "count": len(invalid), "min": rules["min"]})
            if "max" in rules:
                invalid = series[series > rules["max"]]
                if not invalid.empty:
                    errors.append({"column": col, "error": "max_violation", "count": len(invalid), "max": rules["max"]})
            # Regex
            if "regex" in rules and (series.dtype == object or pd.api.types.is_string_dtype(series)):
                pattern = re.compile(rules["regex"])
                invalid = series[~series.astype(str).apply(lambda x: bool(pattern.match(x)) if pd.notna(x) else True)]
                if not invalid.empty:
                    errors.append({"column": col, "error": "regex_mismatch", "count": len(invalid), "regex": rules["regex"]})
            # Uniqueness
            if rules.get("unique"):
                dups = series[series.duplicated(keep=False)]
                if not dups.empty:
                    errors.append({"column": col, "error": "duplicate_values", "count": len(dups)})
            # Enum
            if "enum" in rules:
                invalid = series[~series.isin(rules["enum"])]
                if not invalid.empty:
                    errors.append({"column": col, "error": "enum_violation", "count": len(invalid), "allowed": rules["enum"]})
        return errors

    def _check_type(self, series: pd.Series, expected: str) -> Dict[str, Any]:
        mapping = {
            "int": pd.api.types.is_integer_dtype,
            "float": pd.api.types.is_float_dtype,
            "str": pd.api.types.is_string_dtype,
            "bool": pd.api.types.is_bool_dtype,
            "datetime": pd.api.types.is_datetime64_any_dtype,
        }
        checker = mapping.get(expected)
        if checker is None:
            return {"ok": True, "message": f"Unknown type '{expected}'"}
        ok = checker(series)
        return {"ok": ok, "message": f"Expected {expected}, got {series.dtype}"}
