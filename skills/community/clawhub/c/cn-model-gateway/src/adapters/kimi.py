"""Kimi adapter - re-exported from llm_core."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm_core.adapters.kimi import KimiAdapter

__all__ = ["KimiAdapter"]
