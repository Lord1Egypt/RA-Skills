"""
Statistical anomaly detection methods.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

class AnomalyDetector:
    def __init__(self, method: str = "iqr", threshold: Optional[float] = None):
        self.method = method
        self.threshold = threshold

    def detect(self, series: pd.Series) -> pd.Series:
        """Return boolean mask of anomalies."""
        if self.method == "iqr":
            return self._iqr(series)
        elif self.method == "zscore":
            return self._zscore(series, self.threshold or 3.0)
        elif self.method == "mad":
            return self._mad(series, self.threshold or 3.5)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _iqr(self, series: pd.Series) -> pd.Series:
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return (series < lower) | (series > upper)

    def _zscore(self, series: pd.Series, threshold: float = 3.0) -> pd.Series:
        mean = series.mean()
        std = series.std()
        if std == 0:
            return pd.Series([False] * len(series), index=series.index)
        z = (series - mean).abs() / std
        return z > threshold

    def _mad(self, series: pd.Series, threshold: float = 3.5) -> pd.Series:
        median = series.median()
        mad = (series - median).abs().median()
        if mad == 0:
            return pd.Series([False] * len(series), index=series.index)
        modified_z = 0.6745 * (series - median).abs() / mad
        return modified_z > threshold

    def report(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        target = columns or df.select_dtypes(include=[np.number]).columns.tolist()
        report = {}
        for col in target:
            mask = self.detect(df[col])
            report[col] = {
                "anomaly_count": mask.sum(),
                "anomaly_pct": round(mask.mean() * 100, 2),
                "threshold_method": self.method,
            }
        return report
