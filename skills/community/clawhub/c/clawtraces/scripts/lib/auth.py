"""Backward-compat shim — real code lives in ``lib.core.auth``."""
from .core.auth import *  # noqa: F401, F403
from .core.auth import _format_connection_error  # noqa: F401
