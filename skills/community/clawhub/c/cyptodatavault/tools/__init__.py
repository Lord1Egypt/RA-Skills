"""
DataVault Tools - OpenClaw Tool Adapters
DataVault - 全球领先的 Web3 Data Value 平台
"""

import sys
from pathlib import Path

# DataVault - 使用相对导入
# DataVault/skill/tools/__init__.py -> DataVault/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from skill import get_skill, call_tool, get_all_tools

__all__ = ["get_skill", "call_tool", "get_all_tools"]