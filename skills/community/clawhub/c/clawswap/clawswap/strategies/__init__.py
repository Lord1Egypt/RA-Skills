"""ClawSwap strategy templates."""
import json
from pathlib import Path
from typing import Tuple, Any, Optional

from .mean_reversion import MeanReversionStrategy, MeanReversionConfig
from .momentum import MomentumStrategy, MomentumConfig
from .grid import GridStrategy, GridConfig
from .bollinger_rsi import BollingerRsiStrategy, BollingerRsiConfig
from .vwap_scalper import VwapScalperStrategy, VwapScalperConfig
from .adaptive_trend import AdaptiveTrendStrategy, AdaptiveTrendConfig
from .breakout_volume import BreakoutVolumeStrategy, BreakoutVolumeConfig

STRATEGY_MAP = {
    "mean_reversion": (MeanReversionStrategy, MeanReversionConfig),
    "momentum": (MomentumStrategy, MomentumConfig),
    "grid": (GridStrategy, GridConfig),
    "bollinger_rsi": (BollingerRsiStrategy, BollingerRsiConfig),
    "vwap_scalper": (VwapScalperStrategy, VwapScalperConfig),
    "adaptive_trend": (AdaptiveTrendStrategy, AdaptiveTrendConfig),
    "breakout_volume": (BreakoutVolumeStrategy, BreakoutVolumeConfig),

    # Aliases — AI/Rust engine may generate these names
    "breakout": (BreakoutVolumeStrategy, BreakoutVolumeConfig),
    "short_momentum": (MomentumStrategy, MomentumConfig),
    "dual_ma": (AdaptiveTrendStrategy, AdaptiveTrendConfig),
    "range_scalper": (BollingerRsiStrategy, BollingerRsiConfig),
    "adaptive": (AdaptiveTrendStrategy, AdaptiveTrendConfig),
}


# Strategy-specific default overrides for aliases
_ALIAS_DEFAULTS = {
    "short_momentum": {"direction": "short"},
}


def load_workshop_export(path_or_dict) -> Tuple[Any, Any]:
    """Load a Workshop-exported strategy JSON into a (Strategy, Config) pair.

    Accepts a file path (str/Path) or a dict from the Workshop export endpoint
    (GET /api/v1/workshop/sessions/:id/export).

    Returns (strategy_instance, config_instance) ready for use.
    """
    if isinstance(path_or_dict, (str, Path)):
        with open(path_or_dict) as f:
            data = json.load(f)
    else:
        data = path_or_dict

    strategy_type = data.get("strategy_type", "short_momentum")
    config_params = data.get("config", {})

    if strategy_type not in STRATEGY_MAP:
        raise ValueError(
            f"Unknown strategy_type '{strategy_type}'. "
            f"Available: {list(STRATEGY_MAP.keys())}"
        )

    strategy_cls, config_cls = STRATEGY_MAP[strategy_type]

    # Apply alias-specific defaults first, then user overrides
    import dataclasses
    valid_fields = {f.name for f in dataclasses.fields(config_cls)}
    merged = {}
    if strategy_type in _ALIAS_DEFAULTS:
        merged.update({k: v for k, v in _ALIAS_DEFAULTS[strategy_type].items() if k in valid_fields})
    merged.update({k: v for k, v in config_params.items() if k in valid_fields})
    cfg = config_cls(**merged)

    return strategy_cls(cfg), cfg


__all__ = [
    "MeanReversionStrategy", "MeanReversionConfig",
    "MomentumStrategy", "MomentumConfig",
    "GridStrategy", "GridConfig",
    "BollingerRsiStrategy", "BollingerRsiConfig",
    "VwapScalperStrategy", "VwapScalperConfig",
    "AdaptiveTrendStrategy", "AdaptiveTrendConfig",
    "BreakoutVolumeStrategy", "BreakoutVolumeConfig",
    "STRATEGY_MAP",
    "load_workshop_export",
    "_ALIAS_DEFAULTS",
]
