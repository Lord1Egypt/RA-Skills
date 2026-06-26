"""
Tier-based access control for Multi-Source Data Cleanser.

Tiers:
  FREE   - 50 rows/month, 1 source, single format, no merge/AI/report
  BASIC  - 500 rows/month, 3 sources, basic dedup
  STD    - 3000 rows/month, unlimited sources, format unification + smart fill
  PRO    - unlimited, multi-source merge + AI classification + data quality report

Usage:
  from tier_limits import check_tier, TIER_LIMITS, TierLimitExceeded

  check_tier("free", rows=30)           # raises if over limit
  check_tier("basic", sources=2)        # raises if over limit
  has_feature("pro", "fuzzy_join")      # bool
  enforce_max_rows(tier, rows, count_key)  # updates monthly counter
"""

import os
import json
import time
from pathlib import Path
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

# ─── Constants ────────────────────────────────────────────────────────────────

class Tier(str, Enum):
    FREE  = "free"
    BASIC = "basic"
    STD   = "std"
    PRO   = "pro"

TIER_ORDER = [Tier.FREE, Tier.BASIC, Tier.STD, Tier.PRO]

# Monthly row limits per tier
TIER_MONTHLY_ROWS: Dict[Tier, int] = {
    Tier.FREE:  50,
    Tier.BASIC: 500,
    Tier.STD:   3000,
    Tier.PRO:   -1,   # unlimited
}

# Max data sources (files / pasted blocks)
TIER_MAX_SOURCES: Dict[Tier, int] = {
    Tier.FREE:  1,
    Tier.BASIC: 3,
    Tier.STD:   -1,
    Tier.PRO:   -1,
}

# Max columns allowed
TIER_MAX_COLUMNS: Dict[Tier, int] = {
    Tier.FREE:  10,
    Tier.BASIC: 50,
    Tier.STD:   200,
    Tier.PRO:   -1,
}

# Feature gates per tier
TIER_FEATURES: Dict[Tier, set] = {
    Tier.FREE: {
        "single_format",          # CSV or XLSX only
        "basic_dedup",            # exact match dedup
    },
    Tier.BASIC: {
        "single_format",
        "basic_dedup",
        "multi_format",           # CSV + XLSX + TSV
    },
    Tier.STD: {
        "single_format",
        "basic_dedup",
        "multi_format",
        "smart_fill",             # mean/mode/inference imputation
        "format_unification",     # phone/date/amount standardization
        "advanced_dedup",         # fuzzy dedup
    },
    Tier.PRO: {
        "single_format",
        "basic_dedup",
        "multi_format",
        "smart_fill",
        "format_unification",
        "advanced_dedup",
        "fuzzy_join",             # multi-source merge
        "ai_classification",      # AI tagging
        "data_quality_report",   # quality report → Feishu doc
        "bitable_output",         # write to Feishu Bitable
        "unlimited_rows",
    },
}

# ─── State file ────────────────────────────────────────────────────────────────

def _get_state_path() -> str:
    """Resolve state file path dynamically (env var may be set after import)."""
    return os.environ.get(
        "DATA_CLEANER_STATE_FILE",
        "/tmp/data_cleaner_state.json"
    )

def _load_state() -> Dict[str, Any]:
    try:
        with open(_get_state_path()) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_state(state: Dict[str, Any]) -> None:
    with open(_get_state_path(), "w") as f:
        json.dump(state, f, ensure_ascii=False)

def _get_month_key() -> str:
    """YYYY-MM string for monthly reset."""
    return time.strftime("%Y-%m")

# ─── Exceptions ─────────────────────────────────────────────────────────────────

class TierLimitExceeded(Exception):
    """Raised when user exceeds their tier quota."""
    def __init__(self, message: str, tier: Tier, limit_name: str):
        super().__init__(message)
        self.tier = tier
        self.limit_name = limit_name

class FeatureNotAvailable(Exception):
    """Raised when tier does not support a feature."""
    def __init__(self, feature: str, tier: Tier):
        super().__init__(
            f"功能「{feature}」仅在标准版/专业版可用。"
            f"当前版本：{tier.value}。"
            f"请升级以解锁此功能。"
        )
        self.feature = feature
        self.tier = tier

# ─── Core API ──────────────────────────────────────────────────────────────────

# ─── Token Verification ────────────────────────────────────────────────────────

VERIFY_URL = "https://api.yk-global.com/v1/verify"

VALID_PREFIXES = {
    "GEO", "PROFIT", "INV", "DATA", "MON",
    "PDF", "BANK", "CONTRACT", "EMAIL", "CONV",
    "RPT", "SENTIMENT",
}


def _get_cached(key: str) -> dict:
    """读取本地缓存（5分钟TTL）"""
    import time
    cache_dir = Path.home() / ".data_cleaner_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{key[:8].replace('/', '_')}.json"
    if not cache_file.exists():
        return None
    try:
        with open(cache_file) as f:
            data = json.load(f)
        if time.time() - data.get("_ts", 0) > 300:
            return None
        return data
    except Exception:
        return None


def _set_cached(key: str, data: dict) -> None:
    """写入本地缓存"""
    import time
    cache_dir = Path.home() / ".data_cleaner_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{key[:8].replace('/', '_')}.json"
    try:
        data["_ts"] = time.time()
        with open(cache_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def _prefix_to_tier(api_key: str) -> Tier:
    """Infer Tier from key prefix."""
    if not api_key:
        return Tier.FREE
    upper = api_key.upper()
    if "ENT" in upper:
        return Tier.PRO
    if "MAX" in upper:
        return Tier.PRO
    if "PRO" in upper:
        return Tier.PRO
    if "STD" in upper:
        return Tier.STD
    if "BSC" in upper:
        return Tier.BASIC
    if "FREE" in upper:
        return Tier.FREE
    return Tier.FREE


def _verify_token(api_key: str) -> dict:
    """
    验证 API key via geo-api.yk-global.com。
    降级：网络错误/验证失败 → FREE，不阻断使用。
    """
    if not api_key:
        return {"valid": False, "error": "No API key"}

    prefix = api_key.split("-")[0].upper() if "-" in api_key else api_key[:4].upper()
    if prefix not in VALID_PREFIXES:
        return {"valid": False, "error": "Not a 91Skillhub key"}

    cached = _get_cached(api_key)
    if cached:
        return cached

    try:
        import urllib.request
        import urllib.error
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=b"{}",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("valid", False):
                result = {"valid": True, "tier": _prefix_to_tier(api_key)}
            else:
                result = {"valid": False, "error": data.get("error", "Invalid key")}
            _set_cached(api_key, result)
            return result
    except Exception:
        return {"valid": False, "error": "Network/validation error"}


# ─── Core API ──────────────────────────────────────────────────────────────────

def get_user_tier() -> Tier:
    """
    Resolve current user's subscription tier.

    推断优先级：
    1. 优先用 DATA_CLEANER_API_KEY 环境变量验证 yk global token
    2. 验证成功 → 对应 tier
    3. 其次用 DATA_CLEANER_TIER 环境变量（手动指定）
    4. 最终降级到 FREE
    """
    api_key = os.environ.get("DATA_CLEANER_API_KEY", "")
    if api_key:
        result = _verify_token(api_key)
        if result["valid"]:
            return result["tier"]

    # 降级到手动指定的环境变量
    raw = os.environ.get("DATA_CLEANER_TIER", Tier.FREE.value).lower()
    try:
        return Tier(raw)
    except ValueError:
        return Tier.FREE

def has_feature(tier: Tier, feature: str) -> bool:
    """Check if a tier supports a named feature."""
    return feature in TIER_FEATURES.get(tier, set())

def check_feature(tier: Tier, feature: str) -> None:
    """Raise FeatureNotAvailable if feature is not available for tier."""
    if not has_feature(tier, feature):
        raise FeatureNotAvailable(feature, tier)

def check_tier(
    tier: Tier,
    *,
    rows: Optional[int] = None,
    sources: Optional[int] = None,
    columns: Optional[int] = None,
) -> None:
    """
    Validate that the requested operation fits within tier limits.
    Raises TierLimitExceeded if not.
    """
    state = _load_state()
    month = _get_month_key()

    # ── Monthly rows ──
    if rows is not None:
        limit = TIER_MONTHLY_ROWS[tier]
        used  = state.get("usage", {}).get(month, {}).get("rows", 0)
        if limit > 0 and (used + rows) > limit:
            raise TierLimitExceeded(
                f"本月已使用 {used} 条，剩余 {limit - used} 条。"
                f"免费版每月限额 50 条。",
                tier,
                "monthly_rows",
            )

    # ── Data sources ──
    if sources is not None:
        limit = TIER_MAX_SOURCES[tier]
        if limit > 0 and sources > limit:
            raise TierLimitExceeded(
                f"免费版最多支持 1 个数据源，基础版支持 3 个。"
                f"当前操作涉及 {sources} 个数据源。",
                tier,
                "max_sources",
            )

    # ── Columns ──
    if columns is not None:
        limit = TIER_MAX_COLUMNS[tier]
        if limit > 0 and columns > limit:
            raise TierLimitExceeded(
                f"免费版最多支持 10 列，当前数据有 {columns} 列。",
                tier,
                "max_columns",
            )

def record_usage(*, rows: int = 0) -> Dict[str, Any]:
    """
    Increment monthly usage counters. Returns updated state.
    Call after each successful清洗 operation.
    """
    state     = _load_state()
    month     = _get_month_key()
    usage     = state.setdefault("usage", {})
    month_data = usage.setdefault(month, {"rows": 0})

    month_data["rows"] = month_data.get("rows", 0) + rows
    state["usage"][month] = month_data

    _save_state(state)
    return month_data

def get_usage_summary(tier: Tier) -> Dict[str, Any]:
    """Return current month usage stats for display."""
    state      = _load_state()
    month      = _get_month_key()
    month_data = state.get("usage", {}).get(month, {"rows": 0})
    limit      = TIER_MONTHLY_ROWS[tier]

    return {
        "month":       month,
        "rows_used":   month_data.get("rows", 0),
        "rows_limit":  limit if limit > 0 else "unlimited",
        "tier":        tier.value,
    }

def tier_display_name(tier: Tier) -> str:
    names = {
        Tier.FREE:  "免费版",
        Tier.BASIC: "基础版",
        Tier.STD:   "标准版",
        Tier.PRO:   "专业版",
    }
    return names.get(tier, tier.value)
