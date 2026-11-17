"""
dnd_engine.runtime.detector — 运行时环境检测

通过环境变量、进程特征、工作目录检测当前运行环境。
不依赖任何外部包（仅需 Python 标准库）。
"""

import os
import sys
from dataclasses import dataclass, field

# ── 运行时常量 ──────────────────────────────────────────
RUNTIME_OPENCLAW = "openclaw"
RUNTIME_CLAUDE_CODE = "claude_code"
RUNTIME_CURSOR = "cursor"
RUNTIME_WINDSURF = "windsurf"
RUNTIME_CLINE = "cline"
RUNTIME_TERMINAL = "terminal"
RUNTIME_MCP = "mcp"
RUNTIME_UNKNOWN = "unknown"


@dataclass
class RuntimeInfo:
    """运行时环境信息"""
    runtime: str = RUNTIME_UNKNOWN
    name: str = "未知"
    features: dict = field(default_factory=lambda: {
        "supports_mcp": False,
        "supports_http": False,
        "supports_tool_call": False,
        "has_interactive_terminal": False,
        "uses_workspace": False,
        "auto_loads_skill": False,
    })
    metadata: dict = field(default_factory=dict)
    paths: dict = field(default_factory=dict)

    def is_openclaw(self) -> bool:
        return self.runtime == RUNTIME_OPENCLAW

    def is_mcp_ready(self) -> bool:
        return self.features.get("supports_mcp", False)

    def needs_setup_wizard(self) -> bool:
        """是否需要 setup wizard 引导配置"""
        return self.runtime in (RUNTIME_TERMINAL, RUNTIME_UNKNOWN)


def _check_env_vars() -> dict:
    """检测环境变量特征"""
    env = os.environ
    signals = {}

    # OpenClaw 特征
    if env.get("OPENCLAW_ACTIVE") or env.get("OPENCLAW_WORKSPACE"):
        signals[RUNTIME_OPENCLAW] = 0.9

    # Claude Code 特征
    if env.get("CLAUDE_CODE") or env.get("ANTHROPIC_API_KEY") or env.get("CLAUDE_API_KEY"):
        signals[RUNTIME_CLAUDE_CODE] = 0.6
    if env.get("CLAUDE_CODE_ACTIVE") or env.get("ANTHROPIC_PROMPT"):
        signals[RUNTIME_CLAUDE_CODE] = 0.8

    # Cursor 特征
    if env.get("CURSOR_ACTIVE") or "cursor" in env.get("TERM_PROGRAM", "").lower():
        signals[RUNTIME_CURSOR] = 0.8
    if "cursor" in env.get("VSCODE_IPC_HOOK_CLI", "").lower():
        signals[RUNTIME_CURSOR] = 0.9

    # Windsurf 特征
    if env.get("WINDSURF_ACTIVE"):
        signals[RUNTIME_WINDSURF] = 0.8
    if "windsurf" in env.get("VSCODE_IPC_HOOK_CLI", "").lower():
        signals[RUNTIME_WINDSURF] = 0.9

    # Cline 特征 (VS Code extension)
    if env.get("CLINE_ACTIVE") or env.get("CLINE_MCP"):
        signals[RUNTIME_CLINE] = 0.8

    return signals


def _check_process() -> dict:
    """检测进程特征"""
    signals = {}
    try:
        import psutil
        proc = psutil.Process()
        parent = proc.parent()
        grandparent = parent.parent() if parent else None

        cmdline = " ".join(proc.cmdline()).lower()
        parent_cmd = " ".join(parent.cmdline()).lower() if parent else ""
        gp_cmd = " ".join(grandparent.cmdline()).lower() if grandparent else ""

        # Claude Code
        if "claude" in cmdline or "claude" in parent_cmd:
            signals[RUNTIME_CLAUDE_CODE] = max(signals.get(RUNTIME_CLAUDE_CODE, 0), 0.85)

        # Cursor / Windsurf (VS Code forks)
        if "cursor" in gp_cmd or "cursor" in parent_cmd:
            signals[RUNTIME_CURSOR] = max(signals.get(RUNTIME_CURSOR, 0), 0.85)
        if "windsurf" in gp_cmd or "windsurf" in parent_cmd:
            signals[RUNTIME_WINDSURF] = max(signals.get(RUNTIME_WINDSURF, 0), 0.85)

        # Cline
        if "cline" in parent_cmd or "cline" in gp_cmd:
            signals[RUNTIME_CLINE] = max(signals.get(RUNTIME_CLINE, 0), 0.85)

    except ImportError:
        # psutil not available, fallback to env-only detection
        pass
    except Exception:
        pass

    return signals


def _check_workspace() -> dict:
    """检测工作目录特征"""
    signals = {}
    cwd = os.getcwd()

    # _meta.json — OpenClaw skill 特征
    meta_path = os.path.join(cwd, "_meta.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f:
                content = f.read()
            if "runtime" in content and "agent" in content:
                signals[RUNTIME_OPENCLAW] = max(signals.get(RUNTIME_OPENCLAW, 0), 0.7)
        except Exception:
            pass

    # SKILL.md — OpenClaw skill 特征
    if os.path.exists(os.path.join(cwd, "SKILL.md")):
        signals[RUNTIME_OPENCLAW] = signals.get(RUNTIME_OPENCLAW, 0) + 0.1

    return signals


def detect_runtime() -> RuntimeInfo:
    """
    综合检测当前运行环境。

    使用多线索检测（环境变量 + 进程特征 + 工作目录），
    取置信度最高的运行时为结果。
    """
    signals = {}
    for detector in (_check_env_vars, _check_process, _check_workspace):
        try:
            signals.update(detector())
        except Exception:
            continue

    # 置信度降序排序
    if not signals:
        runtime = RUNTIME_TERMINAL if sys.stdin.isatty() else RUNTIME_UNKNOWN
    else:
        runtime = max(signals, key=signals.get)

    # 构建 RuntimeInfo
    meta = {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "cwd": os.getcwd(),
        "signals": signals,
    }

    info = RuntimeInfo(runtime=runtime)
    info.metadata = meta

    # 按运行时填充特征
    if runtime == RUNTIME_OPENCLAW:
        info.name = "OpenClaw"
        info.features["supports_mcp"] = False
        info.features["supports_http"] = True
        info.features["supports_tool_call"] = True
        info.features["uses_workspace"] = True
        info.features["auto_loads_skill"] = True
        info.paths["workspace"] = os.getcwd()
        info.paths["meta"] = os.path.join(os.getcwd(), "_meta.json")
        info.paths["skill"] = os.path.join(os.getcwd(), "SKILL.md")

    elif runtime in (RUNTIME_CLAUDE_CODE, RUNTIME_CLINE):
        info.name = "Claude Code" if runtime == RUNTIME_CLAUDE_CODE else "Cline"
        info.features["supports_mcp"] = True
        info.features["supports_http"] = True
        info.features["supports_tool_call"] = True
        info.features["has_interactive_terminal"] = sys.stdin.isatty()

    elif runtime in (RUNTIME_CURSOR, RUNTIME_WINDSURF):
        info.name = "Cursor" if runtime == RUNTIME_CURSOR else "Windsurf"
        info.features["supports_mcp"] = True
        info.features["supports_http"] = True
        info.features["supports_tool_call"] = True
        info.features["has_interactive_terminal"] = False

    elif runtime == RUNTIME_TERMINAL:
        info.name = "终端 (Terminal)"
        info.features["has_interactive_terminal"] = True
        info.features["supports_http"] = True  # 可启动 HTTP 服务

    else:
        info.name = f"未知 ({runtime})"

    return info


def save_runtime_info(info: RuntimeInfo, path: str = None) -> str:
    """将 RuntimeInfo 保存为 JSON，供其他模块读取"""
    import json
    if path is None:
        path = os.path.join(os.getcwd(), "_runtime.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "runtime": info.runtime,
            "name": info.name,
            "features": info.features,
            "metadata": info.metadata,
            "paths": info.paths,
        }, f, ensure_ascii=False, indent=2)
    return path