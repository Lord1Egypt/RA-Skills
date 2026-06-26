"""Backward-compat shim — real code lives in ``lib.core.config_loader``."""
from .core.config_loader import *  # noqa: F401, F403
from .core.config_loader import _DEFAULTS, _clone_default  # noqa: F401
