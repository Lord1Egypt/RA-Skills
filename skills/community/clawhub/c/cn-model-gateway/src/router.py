"""Model router - re-exports from llm_core for backward compatibility."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm_core.router import ModelRouter, ENV_KEY_MAP, HEALTH_CHECK_CACHE_TTL
from llm_core.error_map import (
    ERROR_PARAM_INVALID, ERROR_MODEL_UNAVAILABLE,
    ERROR_RATE_LIMITED, ERROR_INTERNAL, ERROR_PROVIDER_NOT_FOUND,
    ERROR_MAP,
)

__all__ = [
    "ModelRouter", "ENV_KEY_MAP", "HEALTH_CHECK_CACHE_TTL",
    "ERROR_PARAM_INVALID", "ERROR_MODEL_UNAVAILABLE",
    "ERROR_RATE_LIMITED", "ERROR_INTERNAL", "ERROR_PROVIDER_NOT_FOUND",
    "ERROR_MAP",
]
