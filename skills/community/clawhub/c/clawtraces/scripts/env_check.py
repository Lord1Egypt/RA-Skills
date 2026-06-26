#!/usr/bin/env python3
# FILE_META
# INPUT:  OpenClaw config file (openclaw.json)
# OUTPUT: JSON status report (fixes applied, restart flag)
# POS:    skill scripts — Step 1, called first in workflow
# MISSION: Validate and auto-fix OpenClaw configuration for data collection.
"""Check and auto-fix OpenClaw environment for ClawTraces.

Ensures:
  1. diagnostics.cacheTrace is enabled with includeSystem=true
  2. agents.defaults.thinkingDefault is at least "high"
  3. per-agent thinkingDefault (agents.list[].thinkingDefault) is at least "high"
  4. models matching ClawTraces whitelist have reasoning=true in providers

Modifies openclaw.json automatically if needed.

Usage:
    python env_check.py
"""

from __future__ import annotations

import json
import os
import re
import sys

# Thinking levels ordered from lowest to highest
THINKING_LEVEL_ORDER = ["off", "minimal", "low", "medium", "high", "xhigh"]
MIN_THINKING_LEVEL = "high"

# Model patterns that ClawTraces collects — same as session_index.py
TRAJECTORY_MODEL_PATTERNS = [
    re.compile(r"sonnet[_\-.]?4[_\-.]?6", re.IGNORECASE),
    re.compile(r"opus[_\-.]?4[_\-.]?5", re.IGNORECASE),
    re.compile(r"opus[_\-.]?4[_\-.]?6", re.IGNORECASE),
]


def _is_trajectory_model(model_id: str) -> bool:
    """Check if a model ID matches the ClawTraces collection whitelist."""
    return any(p.search(model_id) for p in TRAJECTORY_MODEL_PATTERNS)


def get_openclaw_config_path() -> str:
    """Get openclaw.json path."""
    state_dir = os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))
    return os.path.join(state_dir, "openclaw.json")


def load_config(config_path: str) -> dict:
    """Load openclaw.json, returning empty dict if not found."""
    if not os.path.isfile(config_path):
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to parse {config_path}: {e}", file=sys.stderr)
        return {"_parse_error": str(e)}


def save_config(config_path: str, config: dict):
    """Save config back to openclaw.json."""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")


def check_and_fix(config_path: str | None = None) -> dict:
    """Check environment config and auto-fix if needed.

    Returns dict with:
        - ok: bool — whether config is now correct
        - changed: bool — whether config was modified
        - needs_restart: bool — whether OpenClaw needs restart
        - message: str — human-readable status
        - fixes: list[str] — what was fixed
    """
    if config_path is None:
        config_path = get_openclaw_config_path()

    config = load_config(config_path)

    if "_parse_error" in config:
        return {
            "ok": False,
            "changed": False,
            "needs_restart": False,
            "fixes": [],
            "message": f"openclaw.json 解析失败：{config['_parse_error']}。请手动检查文件格式。",
            "parse_error": config["_parse_error"],
        }

    fixes = []

    # ── 1. Ensure diagnostics.cacheTrace ──────────────────────
    if "diagnostics" not in config:
        config["diagnostics"] = {}
    if "cacheTrace" not in config["diagnostics"]:
        config["diagnostics"]["cacheTrace"] = {}

    cache_trace = config["diagnostics"]["cacheTrace"]

    if cache_trace.get("enabled") is not True:
        cache_trace["enabled"] = True
        fixes.append("开启 diagnostics.cacheTrace.enabled（记录完整对话日志）")

    if cache_trace.get("includeSystem") is not True:
        cache_trace["includeSystem"] = True
        fixes.append("开启 diagnostics.cacheTrace.includeSystem（记录 system prompt）")

    # ── 2. Ensure thinking level >= "high" ────────────────────
    min_idx = THINKING_LEVEL_ORDER.index(MIN_THINKING_LEVEL)

    def _needs_upgrade(current: str | None) -> bool:
        if current is None or current not in THINKING_LEVEL_ORDER:
            return True
        return THINKING_LEVEL_ORDER.index(current) < min_idx

    # 2a. Global default
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}

    global_thinking = config["agents"]["defaults"].get("thinkingDefault")
    if _needs_upgrade(global_thinking):
        config["agents"]["defaults"]["thinkingDefault"] = MIN_THINKING_LEVEL
        fixes.append(
            f"全局 agents.defaults.thinkingDefault: "
            f"{global_thinking or 'unset'} → {MIN_THINKING_LEVEL}（提升推理质量）"
        )

    # 2b. Per-agent overrides
    for agent in config.get("agents", {}).get("list", []):
        agent_thinking = agent.get("thinkingDefault")
        if agent_thinking is not None and _needs_upgrade(agent_thinking):
            agent_id = agent.get("id", "unknown")
            agent["thinkingDefault"] = MIN_THINKING_LEVEL
            fixes.append(
                f"Agent「{agent_id}」thinkingDefault: "
                f"{agent_thinking} → {MIN_THINKING_LEVEL}（提升推理质量）"
            )

    # ── 3. Ensure reasoning=true for whitelist models in providers ─
    providers = config.get("models", {}).get("providers", {})
    for provider_name, provider_cfg in providers.items():
        for model in provider_cfg.get("models", []):
            model_id = model.get("id", "")
            if _is_trajectory_model(model_id) and model.get("reasoning") is not True:
                old_val = model.get("reasoning", "unset")
                model["reasoning"] = True
                fixes.append(
                    f"模型 {model_id}（{provider_name}）reasoning: "
                    f"{old_val} → true（启用推理能力）"
                )

    if fixes:
        save_config(config_path, config)
        return {
            "ok": True,
            "changed": True,
            "needs_restart": True,
            "fixes": fixes,
            "message": (
                f"已自动修改 {config_path}，具体变更：\n"
                + "\n".join(f"  • {f}" for f in fixes)
                + "\n\n需要重启 OpenClaw 使配置生效。"
            ),
        }

    return {
        "ok": True,
        "changed": False,
        "needs_restart": False,
        "fixes": [],
        "message": "配置正常（cache-trace 已开启，thinking level 已达标，模型 reasoning 已启用）。",
    }


MIN_PYTHON_VERSION = (3, 9)


def check_python_version() -> dict | None:
    """Check if Python version meets minimum requirement.

    Returns error dict if version is too low, None if OK.
    """
    if sys.version_info < MIN_PYTHON_VERSION:
        required = ".".join(str(v) for v in MIN_PYTHON_VERSION)
        current = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        return {
            "ok": False,
            "changed": False,
            "needs_restart": False,
            "fixes": [],
            "message": (
                f"Python 版本不满足要求：当前 {current}，最低需要 {required}。\n"
                f"当前 python3 路径：{sys.executable}\n"
                f"请升级 Python 后重试。macOS 推荐用 Homebrew：brew install python@3.12"
            ),
        }
    return None


def main():
    # Check Python version first
    version_error = check_python_version()
    if version_error:
        print(json.dumps(version_error, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = check_and_fix()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["changed"]:
        print(f"\n{result['message']}", file=sys.stderr)


if __name__ == "__main__":
    main()
