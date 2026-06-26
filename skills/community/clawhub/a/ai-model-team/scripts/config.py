"""
Configuration Module
P0/P2: Centralized configuration management with fail-fast validation

所有参数必须在启动时校验，不合法立即失败（fail-fast）
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass

# ============ Config Validation Error ============
class ConfigValidationError(Exception):
    """配置校验失败异常"""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))


# ============ Configuration ============
APP_ENV: str = os.getenv("APP_ENV", "dev")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
REQUEST_TIMEOUT_SEC: int = int(os.getenv("REQUEST_TIMEOUT_SEC", "20"))
MAX_RETRY: int = int(os.getenv("MAX_RETRY", "3"))
RETRY_BACKOFF_SEC: float = float(os.getenv("RETRY_BACKOFF_SEC", "0.5"))
TIMEZONE: str = os.getenv("TIMEZONE", "UTC")
DATA_ALIGN_TOLERANCE_SEC: int = int(os.getenv("DATA_ALIGN_TOLERANCE_SEC", "60"))
MIN_DATA_COMPLETENESS: float = float(os.getenv("MIN_DATA_COMPLETENESS", "0.98"))
MAX_DATA_STALENESS_SEC: int = int(os.getenv("MAX_DATA_STALENESS_SEC", "120"))

# ============ Risk (CRITICAL) ============
ENABLE_RISK_GATE: bool = os.getenv("ENABLE_RISK_GATE", "true").lower() == "true"
MAX_POSITION_PCT: float = float(os.getenv("MAX_POSITION_PCT", "0.10"))
MAX_LEVERAGE: float = float(os.getenv("MAX_LEVERAGE", "2.0"))
STOP_LOSS_PCT: float = float(os.getenv("STOP_LOSS_PCT", "0.02"))
TAKE_PROFIT_PCT: float = float(os.getenv("TAKE_PROFIT_PCT", "0.04"))
MAX_DAILY_DRAWDOWN_PCT: float = float(os.getenv("MAX_DAILY_DRAWDOWN_PCT", "0.03"))
MAX_CONSECUTIVE_LOSSES: int = int(os.getenv("MAX_CONSECUTIVE_LOSSES", "4"))
COOLDOWN_MINUTES: int = int(os.getenv("COOLDOWN_MINUTES", "60"))

# Signal
MIN_SIGNAL_CONFIDENCE: float = float(os.getenv("MIN_SIGNAL_CONFIDENCE", "0.60"))
BULLISH_THRESHOLD: float = float(os.getenv("BULLISH_THRESHOLD", "0.65"))
BEARISH_THRESHOLD: float = float(os.getenv("BEARISH_THRESHOLD", "0.35"))

# Ensemble
ENSEMBLE_MODE: str = os.getenv("ENSEMBLE_MODE", "dynamic_weighted")
WEIGHT_KRONOS: float = float(os.getenv("WEIGHT_KRONOS", "0.30"))
WEIGHT_CHRONOS2: float = float(os.getenv("WEIGHT_CHRONOS2", "0.25"))
WEIGHT_TIMESFM: float = float(os.getenv("WEIGHT_TIMESFM", "0.25"))
WEIGHT_FINBERT: float = float(os.getenv("WEIGHT_FINBERT", "0.20"))
CALIBRATION_METHOD: str = os.getenv("CALIBRATION_METHOD", "isotonic")

# Sentiment
SENTIMENT_ENABLE: bool = os.getenv("SENTIMENT_ENABLE", "true").lower() == "true"
SENTIMENT_HALF_LIFE_MIN: int = int(os.getenv("SENTIMENT_HALF_LIFE_MIN", "180"))
SENTIMENT_MIN_SOURCES: int = int(os.getenv("SENTIMENT_MIN_SOURCES", "2"))
SENTIMENT_SPAM_FILTER: bool = os.getenv("SENTIMENT_SPAM_FILTER", "true").lower() == "true"

# Execution
ORDER_TYPE_DEFAULT: str = os.getenv("ORDER_TYPE_DEFAULT", "limit")
SLIPPAGE_BPS: int = int(os.getenv("SLIPPAGE_BPS", "8"))
FEE_BPS: int = int(os.getenv("FEE_BPS", "10"))
MAX_ORDER_SPLITS: int = int(os.getenv("MAX_ORDER_SPLITS", "3"))

# Observability
METRICS_ENABLE: bool = os.getenv("METRICS_ENABLE", "true").lower() == "true"
ALERT_WEBHOOK: str = os.getenv("ALERT_WEBHOOK", "")
TRACE_SAMPLE_RATE: float = float(os.getenv("TRACE_SAMPLE_RATE", "0.10"))

# Security
MASK_SENSITIVE_LOGS: bool = os.getenv("MASK_SENSITIVE_LOGS", "true").lower() == "true"
ALLOW_WITHDRAWAL: bool = os.getenv("ALLOW_WITHDRAWAL", "false").lower() == "true"

# Release
MODEL_VERSION_PIN: str = os.getenv("MODEL_VERSION_PIN", "v2.0.0")
FEATURE_FLAGS: Dict = json.loads(os.getenv("FEATURE_FLAGS", "{}"))

# Paths
AI_HEDGE_PATH: str = os.environ.get('AI_HEDGE_PATH', 
    os.path.join(os.path.expanduser('~'), '.agents/skills/ai-hedge-fund-skill'))
AI_MODEL_TEAM_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ============ Validators ============
class Range:
    def __init__(self, min_val: float, max_val: float, name: str):
        self.min = min_val; self.max = max_val; self.name = name
    def __call__(self, value: float) -> bool:
        return self.min <= value <= self.max
    def error_msg(self, value: float) -> str:
        return f"{self.name} must be {self.min}-{self.max}, got {value}"


class SumToOne:
    def __init__(self):
        pass
    def __call__(self, values: List[float]) -> bool:
        return abs(sum(values) - 1.0) < 0.01
    def error_msg(self, values: List[float]) -> str:
        return f"Ensemble weights must sum to 1.0, got {sum(values):.4f}"


VALIDATION_RULES = [
    ("MAX_POSITION_PCT", Range(0.001, 1.0, "MAX_POSITION_PCT")),
    ("MAX_LEVERAGE", Range(1.0, 100.0, "MAX_LEVERAGE")),
    ("STOP_LOSS_PCT", Range(0.001, 1.0, "STOP_LOSS_PCT")),
    ("TAKE_PROFIT_PCT", Range(0.001, 1.0, "TAKE_PROFIT_PCT")),
    ("MAX_DAILY_DRAWDOWN_PCT", Range(0.001, 1.0, "MAX_DAILY_DRAWDOWN_PCT")),
    ("MAX_CONSECUTIVE_LOSSES", Range(1, 100, "MAX_CONSECUTIVE_LOSSES")),
    ("COOLDOWN_MINUTES", Range(1, 1440, "COOLDOWN_MINUTES")),
    ("MIN_SIGNAL_CONFIDENCE", Range(0.0, 1.0, "MIN_SIGNAL_CONFIDENCE")),
    ("BULLISH_THRESHOLD", Range(0.0, 1.0, "BULLISH_THRESHOLD")),
    ("BEARISH_THRESHOLD", Range(0.0, 1.0, "BEARISH_THRESHOLD")),
    ("WEIGHT_KRONOS", Range(0.0, 1.0, "WEIGHT_*")),
    ("WEIGHT_CHRONOS2", Range(0.0, 1.0, "WEIGHT_*")),
    ("WEIGHT_TIMESFM", Range(0.0, 1.0, "WEIGHT_*")),
    ("WEIGHT_FINBERT", Range(0.0, 1.0, "WEIGHT_*")),
    ("SLIPPAGE_BPS", Range(0, 1000, "SLIPPAGE_BPS")),
    ("FEE_BPS", Range(0, 1000, "FEE_BPS")),
    ("MAX_ORDER_SPLITS", Range(1, 100, "MAX_ORDER_SPLITS")),
    ("REQUEST_TIMEOUT_SEC", Range(1, 300, "REQUEST_TIMEOUT_SEC")),
    ("MIN_DATA_COMPLETENESS", Range(0.5, 1.0, "MIN_DATA_COMPLETENESS")),
]


def validate_config(fail_fast: bool = True) -> Dict[str, Any]:
    """验证配置完整性"""
    errors = []
    warnings = []
    
    # Weight sum check
    weights = [WEIGHT_KRONOS, WEIGHT_CHRONOS2, WEIGHT_TIMESFM, WEIGHT_FINBERT]
    if not SumToOne()(weights):
        errors.append(SumToOne().error_msg(weights))
    
    # Range checks
    for var_name, validator in VALIDATION_RULES:
        value = globals().get(var_name)
        if value is None:
            errors.append(f"{var_name} is not set")
            continue
        if not validator(value):
            errors.append(validator.error_msg(value))
    
    # Cross-field
    if BULLISH_THRESHOLD <= BEARISH_THRESHOLD:
        errors.append(f"BULLISH_THRESHOLD ({BULLISH_THRESHOLD}) must be > BEARISH_THRESHOLD ({BEARISH_THRESHOLD})")
    
    # Production safety
    if APP_ENV == "prod":
        if not MASK_SENSITIVE_LOGS:
            errors.append("MASK_SENSITIVE_LOGS must be true in production")
        if ALLOW_WITHDRAWAL:
            errors.append("ALLOW_WITHDRAWAL must be false in production")
        if not ENABLE_RISK_GATE:
            errors.append("ENABLE_RISK_GATE must be true in production")
    
    result = {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "config_summary": get_config_summary()
    }
    
    if fail_fast and errors:
        raise ConfigValidationError(errors)
    
    return result


def get_config_summary() -> Dict[str, Any]:
    """获取配置摘要"""
    return {
        "app_env": APP_ENV,
        "model_version": MODEL_VERSION_PIN,
        "risk_gate_enabled": ENABLE_RISK_GATE,
        "ensemble_weights": {
            "kronos": WEIGHT_KRONOS,
            "chronos2": WEIGHT_CHRONOS2,
            "timesfm": WEIGHT_TIMESFM,
            "finbert": WEIGHT_FINBERT
        }
    }


def load_env_file():
    """加载 .env 文件"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())


# ============ Startup Validation ============
load_env_file()
try:
    validate_config(fail_fast=True)
except ConfigValidationError as e:
    print(f"❌ Configuration Error:")
    for err in e.errors:
        print(f"   - {err}")
    sys.exit(1)
