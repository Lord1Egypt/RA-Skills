"""Backward-compat shim — real code lives in ``lib.convert.converter``."""
from .convert.converter import *  # noqa: F401, F403
from .convert.converter import (  # noqa: F401
    _convert_tools_to_openai,
    _build_user_or_tool_content,
)
