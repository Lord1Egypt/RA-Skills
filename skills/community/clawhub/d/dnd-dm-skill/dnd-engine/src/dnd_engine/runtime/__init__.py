"""
dnd_engine.runtime — 运行时环境检测与适配

提供跨运行时的环境检测能力，支持：
- OpenClaw (原生的 AI skill 平台)
- Claude Code (Anthropic CLI)
- Cursor / Windsurf (IDE agent)
- Cline (VS Code extension)
- MCP-compatible clients
- 纯终端交互模式
"""

from .detector import detect_runtime, RuntimeInfo, RUNTIME_OPENCLAW, RUNTIME_CLAUDE_CODE, RUNTIME_CURSOR, RUNTIME_WINDSURF, RUNTIME_CLINE, RUNTIME_TERMINAL, RUNTIME_MCP, RUNTIME_UNKNOWN
from .paths import (
    SRD_ENV,
    SrdModules,
    candidate_roots,
    describe_srd,
    load_srd_modules,
    resolve_srd_dir,
)

__all__ = [
    "detect_runtime",
    "RuntimeInfo",
    "RUNTIME_OPENCLAW",
    "RUNTIME_CLAUDE_CODE",
    "RUNTIME_CURSOR",
    "RUNTIME_WINDSURF",
    "RUNTIME_CLINE",
    "RUNTIME_TERMINAL",
    "RUNTIME_MCP",
    "RUNTIME_UNKNOWN",
    "SRD_ENV",
    "SrdModules",
    "candidate_roots",
    "describe_srd",
    "load_srd_modules",
    "resolve_srd_dir",
]