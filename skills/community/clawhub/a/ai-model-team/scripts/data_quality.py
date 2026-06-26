"""
Data Quality & Validation Module
P0: Data completeness, timezone alignment, schema validation
"""
import sys
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import numpy as np

# Configuration
TIMEZONE = "UTC"
DATA_ALIGN_TOLERANCE_SEC = 60  # 60 seconds tolerance
MIN_DATA_COMPLETENESS = 0.98  # 98% minimum completeness
MAX_DATA_STALENESS_SEC = 120   # 120 seconds max staleness


class DataSource(Enum):
    OKX_KLINE = "okx_kline"
    OKX_ORDERBOOK = "okx_orderbook"
    OKX_FUNDING = "okx_funding"
    CRYPTOPANIC = "cryptopanic"
    REDDIT = "reddit"
    RSS = "rss"


@dataclass
class DataQualityReport:
    """Data quality report for a single data source"""
    source: DataSource
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completeness: float = 1.0  # 0.0 to 1.0
    staleness_sec: float = 0.0
    alignment_status: str = "ok"  # ok, warning, error
    missing_fields: List[str] = field(default_factory=list)
    error_count: int = 0
    warning_count: int = 0
    
    def is_acceptable(self) -> bool:
        """Check if data quality is acceptable"""
        return (
            self.completeness >= MIN_DATA_COMPLETENESS and
            self.staleness_sec <= MAX_DATA_STALENESS_SEC and
            self.alignment_status != "error" and
            self.error_count == 0
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source.value,
            "timestamp": self.timestamp.isoformat(),
            "completeness": self.completeness,
            "staleness_sec": self.staleness_sec,
            "alignment_status": self.alignment_status,
            "missing_fields": self.missing_fields,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "is_acceptable": self.is_acceptable()
        }


@dataclass
class UnifiedTimestamp:
    """统一时间戳 (UTC)"""
    utc_time: datetime
    source: DataSource
    original_timezone: str = "UTC"
    offset_seconds: int = 0
    
    @classmethod
    def now(cls) -> "UnifiedTimestamp":
        return cls(utc_time=datetime.now(timezone.utc), source=DataSource.OKX_KLINE)
    
    def to_unix_ms(self) -> int:
        return int(self.utc_time.timestamp() * 1000)
    
    def is_stale(self, max_age_sec: float = MAX_DATA_STALENESS_SEC) -> bool:
        age = (datetime.now(timezone.utc) - self.utc_time).total_seconds()
        return age > max_age_sec


class TimezoneHandler:
    """统一时区处理器 - 所有数据强制使用 UTC"""
    
    @staticmethod
    def to_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    
    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)
    
    @staticmethod
    def format_iso(dt: datetime) -> str:
        return TimezoneHandler.to_utc(dt).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    @staticmethod
    def parse_iso(iso_str: str) -> datetime:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return TimezoneHandler.to_utc(dt)


class DataAlignment:
    """多源数据对齐器"""
    
    @staticmethod
    def align_timestamps(data_sources: List[Dict]) -> Tuple[bool, List[DataQualityReport]]:
        reports = []
        all_timestamps = []
        
        for source_data in data_sources:
            source = source_data.get("source", DataSource.OKX_KLINE)
            timestamp = source_data.get("timestamp")
            
            if timestamp is None:
                reports.append(DataQualityReport(
                    source=source,
                    completeness=0.0,
                    alignment_status="error",
                    missing_fields=["timestamp"]
                ))
                continue
            
            if isinstance(timestamp, (int, float)):
                utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            elif isinstance(timestamp, str):
                utc_time = TimezoneHandler.parse_iso(timestamp)
            else:
                utc_time = TimezoneHandler.to_utc(timestamp)
            
            all_timestamps.append(utc_time)
            age = (datetime.now(timezone.utc) - utc_time).total_seconds()
            
            report = DataQualityReport(
                source=source,
                timestamp=utc_time,
                staleness_sec=age,
                alignment_status="ok" if age <= MAX_DATA_STALENESS_SEC else "warning"
            )
            reports.append(report)
        
        if all_timestamps:
            min_ts = min(all_timestamps)
            max_ts = max(all_timestamps)
            spread = (max_ts - min_ts).total_seconds()
            
            is_aligned = spread <= DATA_ALIGN_TOLERANCE_SEC
            
            if not is_aligned:
                for report in reports:
                    if report.timestamp in [min_ts, max_ts]:
                        report.alignment_status = "warning"
                        report.warning_count += 1
            
            return is_aligned, reports
        
        return False, reports


class SchemaValidator:
    """输入 schema 校验"""
    
    KLINE_SCHEMA = {
        "required": ["ts", "open", "high", "low", "close", "vol"],
        "types": {
            "ts": (int, float, str, datetime),
            "open": (int, float),
            "high": (int, float),
            "low": (int, float),
            "close": (int, float),
            "vol": (int, float)
        },
        "ranges": {
            "open": (0, float('inf')),
            "high": (0, float('inf')),
            "low": (0, float('inf')),
            "close": (0, float('inf')),
            "vol": (0, float('inf'))
        }
    }
    
    @classmethod
    def validate_kline(cls, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        errors = []
        
        for col in cls.KLINE_SCHEMA["required"]:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")
        
        if errors:
            return False, errors
        
        for col, expected_types in cls.KLINE_SCHEMA["types"].items():
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    errors.append(f"Invalid type for {col}: {df[col].dtype}")
        
        for col, (min_val, max_val) in cls.KLINE_SCHEMA["ranges"].items():
            if col in df.columns:
                if df[col].min() < min_val:
                    errors.append(f"{col} below minimum: {df[col].min()} < {min_val}")
        
        if all(c in df.columns for c in ["open", "high", "low", "close"]):
            if not (df["high"] >= df["low"]).all():
                errors.append("High must be >= Low")
            if not (df["high"] >= df["open"]).all():
                errors.append("High must be >= Open")
            if not (df["high"] >= df["close"]).all():
                errors.append("High must be >= Close")
            if not (df["low"] <= df["open"]).all():
                errors.append("Low must be <= Open")
            if not (df["low"] <= df["close"]).all():
                errors.append("Low must be <= Close")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_complete(cls, data: Dict, schema_name: str = "default") -> Tuple[bool, List[str]]:
        errors = []
        if data is None:
            return False, ["Data is None"]
        if not isinstance(data, dict):
            return False, [f"Expected dict, got {type(data)}"]
        return len(errors) == 0, errors


class DataCompletenessChecker:
    """数据完整率校验"""
    
    @staticmethod
    def check_dataframe(df: pd.DataFrame, source: DataSource) -> DataQualityReport:
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isna().sum().sum()
        
        completeness = 1.0 - (missing_cells / total_cells) if total_cells > 0 else 0.0
        
        dup_count = df["ts"].duplicated().sum() if "ts" in df.columns else 0
        
        report = DataQualityReport(
            source=source,
            completeness=completeness,
            staleness_sec=0.0,
            alignment_status="ok" if completeness >= MIN_DATA_COMPLETENESS else "error"
        )
        
        if dup_count > 0:
            report.warning_count += 1
        
        if completeness < MIN_DATA_COMPLETENESS:
            report.error_count += 1
            report.missing_fields.append(f"Missing {missing_cells} cells ({1-completeness:.1%})")
        
        return report
    
    @staticmethod
    def fill_missing_strategy(df: pd.DataFrame, strategy: str = "forward") -> pd.DataFrame:
        if strategy == "forward":
            return df.ffill()
        elif strategy == "backward":
            return df.bfill()
        elif strategy == "drop":
            return df.dropna()
        else:
            return df


def validate_data_quality(data_sources: List[Dict]) -> Dict[str, Any]:
    is_aligned, alignment_reports = DataAlignment.align_timestamps(data_sources)
    all_acceptable = all(r.is_acceptable() for r in alignment_reports)
    
    return {
        "is_usable": all_acceptable,
        "is_aligned": is_aligned,
        "reports": [r.to_dict() for r in alignment_reports],
        "summary": {
            "total_sources": len(alignment_reports),
            "acceptable_count": sum(1 for r in alignment_reports if r.is_acceptable()),
            "warning_count": sum(r.warning_count for r in alignment_reports),
            "error_count": sum(r.error_count for r in alignment_reports)
        }
    }
