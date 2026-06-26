"""配置管理 - 环境变量驱动"""
from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent.parent / "config.env"
    if _env_path.exists():
        load_dotenv(_env_path)
    else:
        load_dotenv()
except ImportError:
    pass

def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

def _env_float(key: str, default: float = 0.0) -> float:
    try:
        return float(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default

def _env_int(key: str, default: int = 0) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default

@dataclass(frozen=True)
class Config:
    tushare_token: str = field(default_factory=lambda: _env("TUSHARE_TOKEN", ""))
    longport_app_key: str = field(default_factory=lambda: _env("LONGPORT_APP_KEY", ""))
    longport_app_secret: str = field(default_factory=lambda: _env("LONGPORT_APP_SECRET", ""))
    longport_access_token: str = field(default_factory=lambda: _env("LONGPORT_ACCESS_TOKEN", ""))
    max_single_position: float = field(default_factory=lambda: _env_float("MAX_SINGLE_POSITION", 0.30))
    max_total_position: float = field(default_factory=lambda: _env_float("MAX_TOTAL_POSITION", 0.80))
    min_market_score: float = field(default_factory=lambda: _env_float("MIN_MARKET_SCORE", 4.0))
    vol_multi: float = field(default_factory=lambda: _env_float("VOL_MULTI", 1.8))
    target_rate: float = field(default_factory=lambda: _env_float("TARGET_RATE", 0.06))
    stop_loss_rate: float = field(default_factory=lambda: _env_float("STOP_LOSS_RATE", -0.04))
    hold_days: int = field(default_factory=lambda: _env_int("HOLD_DAYS", 5))
    backtest_days: int = field(default_factory=lambda: _env_int("BACKTEST_DAYS", 250))
    commission_rate: float = field(default_factory=lambda: _env_float("COMMISSION_RATE", 0.0003))
    stamp_tax_rate: float = field(default_factory=lambda: _env_float("STAMP_TAX_RATE", 0.001))
    slippage_rate: float = field(default_factory=lambda: _env_float("SLIPPAGE_RATE", 0.001))
    circuit_breaker_drop: float = field(default_factory=lambda: _env_float("CIRCUIT_BREAKER_DROP", -0.05))
    correlation_threshold: float = field(default_factory=lambda: _env_float("CORRELATION_THRESHOLD", 0.7))
    poll_interval: int = field(default_factory=lambda: _env_int("POLL_INTERVAL", 60))
    http_timeout: int = field(default_factory=lambda: _env_int("HTTP_TIMEOUT", 10))
    max_retries: int = field(default_factory=lambda: _env_int("MAX_RETRIES", 3))
    db_path: str = field(default_factory=lambda: _env("DB_PATH", str(Path(__file__).parent.parent / ".data" / "stock_skill.db")))
    log_level: str = field(default_factory=lambda: _env("LOG_LEVEL", "INFO"))
    default_watchlist: List[str] = field(default_factory=lambda: ["600036.SH","601318.SH","000001.SZ","300750.SZ","688008.SH"])
    index_codes: List[str] = field(default_factory=lambda: ["000001.SH","399001.SZ","399006.SZ"])

    def validate(self) -> List[str]:
        """验证必需配置（无必填项，tushare 为可选）"""
        return []

    def validate_longport(self) -> List[str]:
        """验证长桥配置（可选，用于港股/美股）"""
        issues = []
        if not self.longport_app_key or self.longport_app_key == "your_longport_app_key_here":
            issues.append("LONGPORT_APP_KEY 未配置")
        if not self.longport_app_secret or self.longport_app_secret == "your_longport_app_secret_here":
            issues.append("LONGPORT_APP_SECRET 未配置")
        if not self.longport_access_token or self.longport_access_token == "your_longport_access_token_here":
            issues.append("LONGPORT_ACCESS_TOKEN 未配置")
        return issues

_config: Config | None = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config

def reload_config() -> Config:
    global _config
    _config = Config()
    return _config
