"""
Ghostclaw services package — high-level orchestrators for analysis, PR creation, plugin management, and config.
"""

# === Shared imports (re-exported for backward compatibility with old services.py namespace) ===
import asyncio
import subprocess
import datetime
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional

# === Core class re-exports ===
from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.cache import LocalCache
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.agent import GhostAgent, AgentEvent

# Rich availability flag
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.status import Status
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# Adapter registry (used by PluginService tests)
from ghostclaw.core.adapters.registry import registry

# Migration utility (was in old services.py)
from ghostclaw.core.migration import migrate_legacy_storage

# === Public service classes (the actual new modules) ===
from .analyzer import AnalyzerService
from .pr import PRService
from .plugin import PluginService
from .config import ConfigService

__all__ = [
    # Services
    'AnalyzerService', 'PRService', 'PluginService', 'ConfigService',
    # Core classes
    'GhostAgent', 'AgentEvent', 'CodebaseAnalyzer', 'LocalCache', 'GhostclawConfig',
    # Utilities
    'asyncio', 'subprocess', 'datetime', 'sys', 'json', 'shutil', 'Path',
    'HAS_RICH', 'registry', 'migrate_legacy_storage',
    # Types
    'Dict', 'Any', 'List', 'Optional',
]
