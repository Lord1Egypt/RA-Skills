#!/usr/bin/env python3
"""
agent-usage-stats — 选个 Agent 看它的 token 消耗

用法:
  agent-usage-stats                    交互式菜单：选 Agent → 看统计
  agent-usage-stats -a hermes          直接查看 Hermes
  agent-usage-stats -w / --watch            交互式菜单 → 实时监控
  agent-usage-stats --all              查看本机所有 Agent 的统计
  agent-usage-stats -a hermes --now    同默认（显式快照）

  时间段查询:
  agent-usage-stats -a hermes -t / --today
  agent-usage-stats -a hermes --yesterday
  agent-usage-stats -a hermes --week
  agent-usage-stats -a hermes --last-7d
  agent-usage-stats -a hermes -m / --month
  agent-usage-stats -a hermes -y / --year
  agent-usage-stats -a hermes --from 2025-01-01 --to 2025-01-31

  导出:
  agent-usage-stats -a hermes -e / --export
  agent-usage-stats -a hermes -t -e

  对比:
  agent-usage-stats -a hermes --compare --a today --b yesterday
  agent-usage-stats -a hermes --compare --a this-week --b last-week
  agent-usage-stats -a hermes --compare --a 2025-01-01 --b 2025-01-15
  agent-usage-stats -a hermes --compare --a 2025-01-01~2025-01-07 --b 2025-01-08~2025-01-14

  详细模式:
  agent-usage-stats -a hermes --detail

安装:
  clawhub install ai-agent-usage-stats
  agent-usage-stats setup              创建全局命令并自动加入 PATH
  agent-usage-stats --uninstall         删除全局命令并清理 PATH
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import sqlite3
import sys
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

VERSION = "2.6.1"

# 强制 stdout 行缓冲 + UTF-8，使 --watch 模式的输出实时可见
try:
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
except Exception:
    try:
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    except Exception:
        pass

# ── WSL 兼容 ──
# Windows 上 WSL2 中运行的 Agent 数据可通过 \\wsl$\ 访问

_WSL_HOMES_CACHE = None


def _get_wsl_homes():
    """Windows 上枚举 WSL 发行版中可能存放 Agent 数据的 home 目录。返回路径列表（缓存结果）。"""
    global _WSL_HOMES_CACHE
    if _WSL_HOMES_CACHE is not None:
        return _WSL_HOMES_CACHE
    if sys.platform != "win32":
        _WSL_HOMES_CACHE = []
        return []
    homes = []

    # 方式 1：wsl.exe 枚举（最可靠，UNC 目录列表在某些机器上不通）
    try:
        import subprocess
        distros_out = subprocess.run(
            ["wsl.exe", "-l", "-q"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5,
        )
        # wsl.exe 自身输出为 UTF-16LE
        for line in distros_out.stdout.decode("utf-16-le", errors="ignore").splitlines():
            distro = line.strip()
            if not distro:
                continue
            try:
                home_out = subprocess.run(
                    ["wsl.exe", "-d", distro, "--", "bash", "-c", "echo $HOME"],
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5,
                )
                # bash 命令输出为 UTF-8
                wsl_home = home_out.stdout.decode("utf-8", errors="ignore").strip()
                if wsl_home and wsl_home.startswith("/"):
                    homes.append(f"//wsl.localhost/{distro}{wsl_home}")
            except Exception:
                pass
    except Exception:
        pass

    # 方式 2：UNC 路径直接枚举（回退，某些机器上更快）
    if not homes:
        for wsl_root in [r"\\wsl.localhost", r"\\wsl$"]:
            try:
                for distro in os.listdir(wsl_root):
                    distro_dir = os.path.join(wsl_root, distro)
                    if not os.path.isdir(distro_dir):
                        continue
                    for sub in ["home", "root"]:
                        home_base = os.path.join(distro_dir, sub)
                        if os.path.isdir(home_base):
                            try:
                                for user in os.listdir(home_base):
                                    uh = os.path.join(home_base, user)
                                    if os.path.isdir(uh):
                                        homes.append(uh)
                            except (OSError, PermissionError):
                                pass
            except (OSError, PermissionError, FileNotFoundError):
                continue

    # 统一为正斜杠格式，Windows 下 Python 访问 WSL UNC 路径需要 /
    homes = [h.replace("\\", "/") for h in homes]
    _WSL_HOMES_CACHE = homes
    return homes


def _resolve_path(relative_path):
    """解析路径：先查本机 ~，再查 WSL home（Windows + wsl.exe 探测），返回首个存在的路径。"""
    native = os.path.join(os.path.expanduser("~"), relative_path)
    if os.path.exists(native):
        return native
    for wh in _get_wsl_homes():
        wp = os.path.join(wh, relative_path)
        if os.path.exists(wp):
            return wp
        # UNC 不通时，通过 wsl.exe 探测文件是否存在
        if sys.platform == "win32":
            try:
                import subprocess
                parts = wh.replace("\\", "/").strip("/").split("/")
                # wh = //wsl.localhost/Distro/home/user
                if len(parts) >= 4 and parts[0] in ("wsl.localhost", "wsl$"):
                    distro = parts[1]
                    wsl_path = "/" + "/".join(parts[3:]) + "/" + relative_path.lstrip(".")
                    probe = subprocess.run(
                        ["wsl.exe", "-d", distro, "--", "test", "-e", wsl_path],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3,
                    )
                    if probe.returncode == 0:
                        return wp  # 文件在 WSL 中存在，返回 UNC 路径
            except Exception:
                pass
    return native


def _is_wsl_unc(path: str) -> bool:
    """检测路径是否为 WSL UNC 路径（如 //wsl.localhost/Distro/...）。"""
    return path.replace("\\", "/").startswith("//wsl.")


def _wsl_unc_to_linux(unc_path):
    """WSL UNC 路径 → (distro, linux_path)。非 WSL 返回 (None, None)。"""
    p = unc_path.replace("\\", "/")
    for prefix in ("//wsl.localhost/", "//wsl$/"):
        if p.startswith(prefix):
            rest = p[len(prefix):]
            idx = rest.find("/")
            if idx > 0:
                return rest[:idx], "/" + rest[idx + 1:]
    return None, None


def _hermes_collect_via_wsl(db_path, from_ts=None, to_ts=None):
    """通过 wsl.exe 在 WSL 内查询 Hermes 数据库。返回 dict 或 None。"""
    import subprocess
    distro, linux_path = _wsl_unc_to_linux(db_path)
    if not distro:
        return None
    # 时间筛选（含 grace 期防止旧会话 ended_at=NULL 被误纳入）
    where = ""
    if from_ts or to_ts:
        parts = []
        if from_ts:
            grace = from_ts - 86400
            parts.append(f"(started_at >= {from_ts} OR (ended_at IS NULL AND started_at >= {grace}) OR ended_at >= {from_ts})")
        if to_ts:
            parts.append(f"started_at <= {to_ts}")
        where = " WHERE " + " AND ".join(parts)
    script = (
        "import sqlite3,json;c=sqlite3.connect(r'%s');c.row_factory=sqlite3.Row;"
        "cols={r[1] for r in c.execute('PRAGMA table_info(sessions)')};"
        "has_ac='api_call_count' in cols;has_tc='tool_call_count' in cols;"
        "ac='api_call_count' if has_ac else '0';tc='tool_call_count' if has_tc else '0';"
        "rows=[dict(r) for r in c.execute("
        "f'SELECT model,SUM(input_tokens) inp,SUM(output_tokens) out,SUM(cache_read_tokens) cache,'"
        "f'SUM('+ac+') calls,SUM('+tc+') tools,COUNT(*) cnt FROM sessions%s GROUP BY model')];"
        "sc=c.execute('SELECT COUNT(*) FROM sessions%s').fetchone()[0];"
        "c.close();print(json.dumps({'rows':rows,'sc':sc},default=str))"
    ) % (linux_path, where, where)
    try:
        r = subprocess.run(
            ["wsl.exe", "-d", distro, "--", "python3", "-c", script],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15,
        )
        return json.loads(r.stdout.decode("utf-8", errors="ignore"))
    except Exception:
        return None


def _codex_collect_via_wsl(db_path, from_ts=None, to_ts=None):
    """通过 wsl.exe 在 WSL 内查询 CodeX 数据库。返回 dict 或 None。"""
    import subprocess
    distro, linux_path = _wsl_unc_to_linux(db_path)
    if not distro:
        return None
    where = ""
    if from_ts or to_ts:
        parts = []
        if from_ts:
            parts.append(f"created_at >= {int(from_ts)}")
        if to_ts:
            parts.append(f"created_at <= {int(to_ts)}")
        where = " WHERE " + " AND ".join(parts)
    script = (
        "import sqlite3,json;c=sqlite3.connect(r'%s');c.row_factory=sqlite3.Row;"
        "rows=[dict(r) for r in c.execute("
        "'SELECT model,model_provider,SUM(tokens_used) tokens,COUNT(*) cnt FROM threads%s GROUP BY model,model_provider')];"
        "sc=c.execute('SELECT COUNT(*) FROM threads%s').fetchone()[0];"
        "c.close();print(json.dumps({'rows':rows,'sc':sc},default=str))"
    ) % (linux_path, where, where)
    try:
        r = subprocess.run(
            ["wsl.exe", "-d", distro, "--", "python3", "-c", script],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15,
        )
        return json.loads(r.stdout.decode("utf-8", errors="ignore"))
    except Exception:
        return None


# ── 路径配置系统 ──
# 支持 setup 时自动检测 Agent 路径，保存到配置文件
# 运行时优先读取配置，无配置时回退到标准路径

COMMAND_NAME = "agent-usage-stats"
LEGACY_COMMAND_NAMES = ("token-stats",)

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", COMMAND_NAME)
LEGACY_CONFIG_DIRS = [
    os.path.join(os.path.expanduser("~"), ".config", name)
    for name in LEGACY_COMMAND_NAMES
]
CONFIG_FILE = os.path.join(CONFIG_DIR, "paths.json")


def _load_agent_paths() -> dict:
    """加载已保存的 Agent 数据路径配置"""
    for path in [CONFIG_FILE] + [os.path.join(d, "paths.json") for d in LEGACY_CONFIG_DIRS]:
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    return {}


def _save_agent_paths(paths: dict):
    """保存 Agent 数据路径配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(paths, f, indent=2, ensure_ascii=False)


def _scan_all_agent_paths() -> dict:
    """扫描本机所有 Agent 的数据路径（含 WSL），返回 {agent_name: data_path}"""
    homes = [os.path.expanduser("~")] + _get_wsl_homes()
    paths = {}
    # Hermes
    for h in homes:
        for p in [os.path.join(h, ".hermes", "state.db"),
                  os.path.join(h, ".config", "hermes", "state.db")]:
            if os.path.exists(p):
                paths["hermes_db"] = p
                break
        if "hermes_db" in paths:
            break
    for h in homes:
        for p in [os.path.join(h, ".hermes", "sessions", "sessions.json"),
                  os.path.join(h, ".config", "hermes", "sessions", "sessions.json")]:
            if os.path.exists(p):
                paths["hermes_sessions"] = p
                break
        if "hermes_sessions" in paths:
            break
    # Claude Code
    for h in homes:
        p = os.path.join(h, ".claude")
        if os.path.isdir(os.path.join(p, "projects")):
            paths["claude_dir"] = p
            break
    # CodeX
    for h in homes:
        p = os.path.join(h, ".codex")
        if os.path.isdir(p):
            paths["codex_dir"] = p
            break
    # OpenClaw
    for h in homes:
        p = os.path.join(h, ".openclaw", "agents", "main", "sessions", "sessions.json")
        if os.path.exists(p):
            paths["openclaw_sessions"] = p
            break
    return paths


# ═══════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════

def _fmt_float(v: float) -> str:
    """保留最多 2 位小数，去掉尾部多余的零。"""
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def fmt_num(n: int) -> str:
    if abs(n) < 1000:
        return str(n)
    elif abs(n) < 1_000_000:
        return f"{_fmt_float(n/1000)}K"
    else:
        return f"{_fmt_float(n/1_000_000)}M"


def fmt_pct(pct: float) -> str:
    if pct >= 100:
        return ">100%"
    elif pct >= 90:
        return f"{pct:.1f}% 🚨"
    elif pct >= 60:
        return f"{pct:.1f}% ⚠️"
    else:
        return f"{pct:.1f}% ✅"


# ═══════════════════════════════════════════════════
#  价格与缓存率
# ═══════════════════════════════════════════════════

_model_prices_cache = None


def _load_model_prices() -> dict:
    """加载 model_prices.toml，失败返回 {}。结果缓存。"""
    global _model_prices_cache
    if _model_prices_cache is not None:
        return _model_prices_cache
    # 查找配置文件：先找项目根目录，再找脚本所在目录
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_prices.toml"),
        os.path.join(os.getcwd(), "model_prices.toml"),
    ]
    for cp in candidates:
        if os.path.isfile(cp):
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                    with open(cp, "rb") as f:
                        data = tomllib.load(f)
                else:
                    data = {}
            except Exception:
                data = {}
            _model_prices_cache = data
            return data
    _model_prices_cache = {}
    return {}


def _get_model_price(model: str) -> dict | None:
    """获取指定模型的价格配置。先精确匹配，再前缀匹配"""
    prices = _load_model_prices()
    if not prices:
        return None
    if model in prices:
        return prices[model]
    # 前缀匹配：如 deepseek-v4-pro-20250219 → deepseek-v4-pro
    for key in sorted(prices.keys(), key=lambda k: -len(k)):
        if model.startswith(key):
            return prices[key]
    return None


def _calc_cache_rate(inp: int, cache: int) -> float | None:
    """计算缓存命中率（百分比）。
    自适应公式：cache > input → cache/(cache+input), 否则 cache/input。
    返回 None 表示无法计算。"""
    if cache <= 0 or inp <= 0:
        return None
    if cache > inp:
        return cache / (cache + inp) * 100
    return cache / inp * 100


def _fmt_cache_val(cache: int, inp: int) -> str:
    """格式化缓存展示，含缓存命中率。eg: 缓 162.18K (85.5%)"""
    base = f"缓 {fmt_num(cache)}"
    rate = _calc_cache_rate(inp, cache)
    if rate is not None:
        return f"{base} ({min(rate, 99.9):.1f}%)"
    return base


def _calc_cost(inp: int, out: int, cache: int, price: dict) -> float:
    """计算预估费用。自适应缓存模型：cache>inp 时 inp=cacheMiss，否则 inp 含 cacheHit"""
    if cache > inp:
        no_cache = inp
        cache_tokens = cache
    else:
        no_cache = inp - cache
        cache_tokens = cache
    return (no_cache * price.get("input_no_cache_price", 0) +
            cache_tokens * price.get("input_cache_price", 0) +
            out * price.get("output_price", 0)) / 1_000_000


def _fmt_cost(inp: int, out: int, cache: int, price: dict) -> str:
    """格式化预估费用，统一为人民币"""
    total = _calc_cost(inp, out, cache, price)
    currency = price.get("currency", "CNY")
    if currency == "USD":
        total *= _USD_TO_CNY
    return f"≈¥{total:.2f}"


def _calc_total_cost(per_model_list: list) -> dict[str, float]:
    """计算 per_model 列表中所有有价格模型的费用总和。返回 {currency: cost}"""
    totals: dict[str, float] = {}
    for pm in (per_model_list or []):
        pc = _get_model_price(pm.get("model", ""))
        if pc:
            inp = pm.get("input", 0) or 0
            out = pm.get("output", 0) or 0
            cache = pm.get("cache", 0) or 0
            cur = pc.get("currency", "CNY")
            totals[cur] = totals.get(cur, 0.0) + _calc_cost(inp, out, cache, pc)
    return totals


# USD → CNY 汇率
_USD_TO_CNY = 7.25


def _to_cny(cost: float, currency: str) -> float:
    """将费用统一转为人民币"""
    return cost * _USD_TO_CNY if currency == "USD" else cost


def _fmt_total_cost(totals: dict[str, float]) -> str:
    """格式化总费用，统一转人民币。eg: ≈¥87.29"""
    if not totals:
        return ""
    # 统一换算为 CNY
    total_cny = totals.get("CNY", 0.0) + totals.get("USD", 0.0) * _USD_TO_CNY
    if total_cny <= 0:
        return ""
    return f"≈¥{total_cny:.2f}"


def _has_any_price(per_model_data: list) -> bool:
    """检查 per_model 列表中是否至少有一个模型配置了价格"""
    for pm in (per_model_data or []):
        mn = pm.get("model", "")
        if _get_model_price(mn):
            return True
    return False


def fmt_today_lines(per_model: list, fmt_num_fn) -> list:
    """Format per-model today data. Returns [first_line, ...] for printing.
    Uses 📅 今日 prefix for single-model, or header + per-model + 合计 for multi."""
    if not per_model:
        return []
    filtered = [pm for pm in per_model if not _skip_model(pm)]
    if not filtered:
        return []
    models = []
    ti = to = tc = tca = 0
    for pm in filtered:
        m = pm.get("model", "unknown")
        i = pm.get("input", 0) or 0
        o = pm.get("output", 0) or 0
        c = pm.get("cache", 0) or 0
        ca = pm.get("calls", 0) or 0
        models.append((m, i, o, c, ca))
        ti += i
        to += o
        tc += c
        tca += ca

    has_price = _has_any_price(filtered)

    lines = []
    if len(models) == 1:
        m, i, o, c, ca = models[0]
        t = i + o
        parts = [f"入 {fmt_num_fn(i)}",
                 f"出 {fmt_num_fn(o)}",
                 _fmt_cache_val(c, i),
                 f"总计/+缓存 {fmt_num_fn(t)}/{fmt_num_fn(t + c)}",
                 f"调用 {ca} 次"]
        if has_price:
            price_cfg = _get_model_price(m)
            parts.append(_fmt_cost(i, o, c, price_cfg) if price_cfg else "-")
        lines.append(f"  📅 今日 | {' | '.join(parts)}")
    else:
        rows = []
        for m, i, o, c, ca in models:
            t = i + o
            cols = [
                f"入 {fmt_num_fn(i)}",
                f"出 {fmt_num_fn(o)}",
                _fmt_cache_val(c, i),
                f"总计/+缓存 {fmt_num_fn(t)}/{fmt_num_fn(t + c)}",
                f"调用 {ca} 次",
            ]
            if has_price:
                price_cfg = _get_model_price(m)
                cols.append(_fmt_cost(i, o, c, price_cfg) if price_cfg else "-")
            rows.append((m, cols))
        cols_total = [
            f"入 {fmt_num_fn(ti)}",
            f"出 {fmt_num_fn(to)}",
            _fmt_cache_val(tc, ti),
            f"总计/+缓存 {fmt_num_fn(ti + to)}/{fmt_num_fn(ti + to + tc)}",
            f"调用 {tca} 次",
        ]
        if has_price:
            total_cost_str = _fmt_total_cost(_calc_total_cost(filtered))
            if total_cost_str:
                cols_total.append(f"{total_cost_str} (仅供参考)")
        rows.append(("今日合计", cols_total))
        col_count = len(cols_total)
        col_widths = [0] * (col_count + 1)
        col_widths[0] = max(_display_width(r[0]) for r in rows)
        for ci in range(col_count):
            col_widths[ci + 1] = max(_display_width(r[1][ci]) for r in rows)
        lines.append("  📅 今日")
        for label, cols in rows:
            parts = [_pad_to(label, col_widths[0])]
            for ci, col_text in enumerate(cols):
                parts.append(_pad_to(col_text, col_widths[ci + 1], ">"))
            lines.append(f"    {' | '.join(parts)}")
    return lines
MODEL_CONTEXT_MAP = {
    # ── Anthropic / Claude (all 200K) ──
    "claude-opus-4-7": 200_000,
    "claude-opus-4-5": 200_000,
    "claude-opus-4": 200_000,
    "claude-sonnet-4-6": 200_000,
    "claude-sonnet-4-5": 200_000,
    "claude-sonnet-4": 200_000,
    "claude-haiku-4-5": 200_000,
    "claude-haiku-4-5-20251001": 200_000,
    "claude-haiku-3.5": 200_000,
    "claude-3.5-sonnet": 200_000,
    "claude-3.5-haiku": 200_000,
    "claude-3-opus": 200_000,
    "claude-3-sonnet": 200_000,
    "claude-3-haiku": 200_000,

    # ── OpenAI / GPT ──
    "gpt-4.1": 1_048_576,
    "gpt-4.1-mini": 1_048_576,
    "gpt-4.1-nano": 1_048_576,
    "gpt-4o": 131_072,
    "gpt-4o-mini": 131_072,
    "gpt-4-turbo": 131_072,
    "gpt-4": 131_072,
    "o4-mini": 200_000,
    "o3": 200_000,
    "o3-mini": 200_000,
    "o1": 200_000,
    "o1-pro": 200_000,

    # ── Google / Gemini (all 1M) ──
    "gemini-2.5-pro": 1_048_576,
    "gemini-2.5-flash": 1_048_576,
    "gemini-2.5-flash-lite": 1_048_576,
    "gemini-2.0-flash": 1_048_576,

    # ── DeepSeek ──
    "deepseek-v4-flash": 1_048_576,
    "deepseek-v4-pro": 1_048_576,
    "deepseek-v4": 1_048_576,
    "deepseek-chat": 1_048_576,
    "deepseek-reasoner": 1_048_576,
    "deepseek-r1": 1_048_576,
    "deepseek-v3": 131_072,

    # ── Meta / Llama ──
    "llama-4": 131_072,
    "llama-3.1": 131_072,
    "llama-3": 131_072,

    # ── Mistral ──
    "mistral-large-2": 131_072,
    "mistral-large": 131_072,
    "mistral-small": 131_072,

    # ── 通义千问 / Qwen ──
    "qwen3.6-plus": 1_048_576,
    "qwen3": 131_072,
    "qwen3-coder": 131_072,
    "qwen2.5-coder": 131_072,
    "qwen-plus": 131_072,
    "qwen-max": 131_072,
    "qwen-turbo": 131_072,

    # ── Kimi / 月之暗面 (Moonshot) ──
    "moonshot-v1-128k": 131_072,
    "moonshot-v1-32k": 32_768,
    "moonshot-v1-8k": 8_192,
    "kimi-latest": 131_072,

    # ── GLM / 智谱 ──
    "glm-4-plus": 131_072,
    "glm-4-long": 1_048_576,
    "glm-4-air": 131_072,
    "glm-4-flash": 131_072,
    "glm-4": 131_072,
    "glm-3-turbo": 131_072,

    # ── Doubao / 字节豆包 ──
    "doubao-pro-128k": 131_072,
    "doubao-pro-32k": 32_768,
    "doubao-lite-32k": 32_768,

    # ── 文心 / 百度 (ERNIE) ──
    "ernie-4.0-turbo": 131_072,
    "ernie-4.0": 8_192,
    "ernie-3.5": 8_192,

    # ── 零一万物 / Yi ──
    "yi-large": 32_768,
    "yi-lightning": 16_384,

    # ── xAI / Grok ──
    "grok-3": 131_072,
    "grok-2": 131_072,
}

DEFAULT_CONTEXT = 131_072


def detect_context(model_name: str) -> int:
    if not model_name:
        return DEFAULT_CONTEXT
    m = model_name.lower().strip()
    if m in MODEL_CONTEXT_MAP:
        return MODEL_CONTEXT_MAP[m]
    for key, val in sorted(MODEL_CONTEXT_MAP.items(), key=lambda x: -len(x[0])):
        if m.startswith(key):
            return val
    return DEFAULT_CONTEXT


def parse_date(s: str) -> tuple:
    """Parse 'YYYY-MM-DD' → (start_ts, end_ts)"""
    dt = datetime.strptime(s.strip(), "%Y-%m-%d")
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end = dt.replace(hour=23, minute=59, second=59, microsecond=0)
    return start.timestamp(), end.timestamp()


def parse_time_label(label: str) -> tuple:
    """Parse a time label → (start_ts, end_ts).

    Supports:
      today, yesterday, this-week / week, last-week, last-7d
      YYYY-MM-DD (single day)
      YYYY-MM-DD~YYYY-MM-DD (date range)
    """
    s = label.strip().lower()
    now = datetime.now()

    if s == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "yesterday":
        d = now - timedelta(days=1)
        start = d.replace(hour=0, minute=0, second=0, microsecond=0)
        end = d.replace(hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    if s in ("this-week", "week"):
        monday = now - timedelta(days=now.weekday())
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-week":
        monday = now - timedelta(days=now.weekday() + 7)
        sunday = monday + timedelta(days=6)
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        end = sunday.replace(hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    if s == "last-7d":
        start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s in ("this-month", "month"):
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-month":
        first_of_this = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_last = first_of_this - timedelta(seconds=1)
        start_of_last = end_of_last.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start_of_last.timestamp(), end_of_last.timestamp()

    if s in ("this-year", "year"):
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-year":
        start = now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(year=now.year - 1, month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    # Date range: YYYY-MM-DD~YYYY-MM-DD
    if "~" in s:
        parts = s.split("~", 1)
        start_ts, _ = parse_date(parts[0])
        _, end_ts = parse_date(parts[1])
        return start_ts, end_ts

    # Single date
    return parse_date(s)


def _split_months(from_ts, to_ts):
    """Split a time range into calendar month buckets.
    Returns [(label, start_ts, end_ts), ...]"""
    from_dt = datetime.fromtimestamp(from_ts)
    to_dt = datetime.fromtimestamp(to_ts)
    months = []
    current = from_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    while current <= to_dt:
        month_start = current
        if current.month == 12:
            next_month = current.replace(year=current.year + 1, month=1)
        else:
            next_month = current.replace(month=current.month + 1)
        month_end = min(next_month - timedelta(seconds=1), to_dt)
        label = month_start.strftime('%Y-%m')
        months.append((label, month_start.timestamp(), month_end.timestamp()))
        current = next_month
    return months


def _progress_bar(pct: float) -> str:
    """10 段上下文进度条，带 ANSI 颜色。累计模式下 pct 可能超过 100%"""
    n = min(10, max(0, round(min(pct, 100) / 10)))
    bar = "█" * n + "░" * (10 - n)
    # ANSI 颜色：绿(<60%) / 黄(60-90%) / 红(>90%)
    if pct >= 90:
        color = "\033[31m"  # 红
    elif pct >= 60:
        color = "\033[33m"  # 黄
    else:
        color = "\033[32m"  # 绿
    if pct > 100:
        return f"{color}[{bar}]\033[0m >100%"
    return f"{color}[{bar}]\033[0m {pct}%"


def _display_width(s: str) -> int:
    """计算终端显示宽度（CJK 字符算 2 列，ASCII 算 1 列）。"""
    w = 0
    for c in s:
        code = ord(c)
        if (0x1100 <= code <= 0x115F or    # Hangul Jamo
            0x2E80 <= code <= 0xA4CF or    # CJK Radicals ~ Yi
            0xAC00 <= code <= 0xD7A3 or    # Hangul Syllables
            0xF900 <= code <= 0xFAFF or    # CJK Compatibility Ideographs
            0xFE30 <= code <= 0xFE4F or    # CJK Compatibility Forms
            0xFF01 <= code <= 0xFF60 or    # Fullwidth Forms
            0xFFE0 <= code <= 0xFFE6 or    # Fullwidth Signs
            0x20000 <= code <= 0x2FFFF or  # CJK Extension
            0x30000 <= code <= 0x3FFFF):   # CJK Extension
            w += 2
        else:
            w += 1
    return w


def _pad_to(s: str, width: int, align: str = "<") -> str:
    """按显示宽度填充到指定列宽。"""
    dw = _display_width(s)
    pad = max(0, width - dw)
    if align == ">":
        return " " * pad + s
    else:
        return s + " " * pad


def _strip_ansi(s: str) -> str:
    """移除 ANSI 转义序列，用于显示宽度计算。"""
    return re.sub(r'\033\[[0-9;]*m', '', s)


def _pad_ansi(s: str, width: int, align: str = "<") -> str:
    """按可见宽度填充（忽略 ANSI 码）。"""
    dw = _display_width(_strip_ansi(s))
    pad = max(0, width - dw)
    if align == ">":
        return " " * pad + s
    else:
        return s + " " * pad


def _align_rows(rows):
    """rows: list of list of str。每列按最大宽度左对齐。"""
    if not rows:
        return rows
    n_cols = max(len(r) for r in rows)
    widths = [0] * n_cols
    for row in rows:
        for i, col in enumerate(row):
            w = _display_width(_strip_ansi(col))
            if w > widths[i]:
                widths[i] = w
    result = []
    for row in rows:
        padded = []
        for i, col in enumerate(row):
            padded.append(_pad_ansi(col, widths[i], '<'))
        result.append(padded)
    return result


def label_to_display(label: str) -> str:
    """将时间标签转为人类可读的日期字符串，用于对比模式列头。"""
    s = label.strip().lower()
    now = datetime.now()
    if s == "today":
        return now.strftime("%Y-%m-%d")
    if s == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    if s in ("this-week", "week"):
        monday = now - timedelta(days=now.weekday())
        return f"{monday.strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s == "last-week":
        monday = now - timedelta(days=now.weekday() + 7)
        sunday = monday + timedelta(days=6)
        return f"{monday.strftime('%Y-%m-%d')}~{sunday.strftime('%Y-%m-%d')}"
    if s == "last-7d":
        start = now - timedelta(days=7)
        return f"{start.strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s in ("this-month", "month"):
        start = now.replace(day=1)
        return f"{start.strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s == "last-month":
        first_of_this = now.replace(day=1)
        end_of_last = first_of_this - timedelta(days=1)
        return f"{end_of_last.replace(day=1).strftime('%Y-%m-%d')}~{end_of_last.strftime('%Y-%m-%d')}"
    if s in ("this-year", "year"):
        return f"{now.replace(month=1, day=1).strftime('%Y-%m-%d')}~{now.strftime('%Y-%m-%d')}"
    if s == "last-year":
        return f"{now.year - 1}-01-01~{now.year - 1}-12-31"
    # 已经是日期或日期段格式，直接返回
    return label


def _skip_model(pm: dict) -> bool:
    """过滤掉 unknown 且无数据的模型条目（输出/导出/监控通用）。"""
    model = (pm.get("model", "") or "").strip()
    if not model or model == "unknown":
        inp = pm.get("input", 0) or 0
        out = pm.get("output", 0) or 0
        cache = pm.get("cache", 0) or 0
        calls = pm.get("calls", 0) or 0
        if inp == 0 and out == 0 and cache == 0 and calls == 0:
            return True
    return False


def format_model_line(model_name: str, inp: int, out: int, cache: int, calls: int,
                      context_window: int = None, session_count: int = None,
                      extra: str = None) -> str:
    """单行模型输出格式。若全为 0 则返回空字符串。"""
    if inp == 0 and out == 0 and cache == 0 and calls == 0:
        return ""

    parts = []
    total = inp + out
    if context_window:
        pct = round(total / context_window * 100, 1) if context_window else 0
        parts.append(f"上下文 {fmt_num(total)}/{fmt_num(context_window)} ({fmt_pct(pct)})")
        parts.append(f"入 {fmt_num(inp)}")
        parts.append(f"出 {fmt_num(out)}")
        parts.append(_fmt_cache_val(cache, inp))
        parts.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache)}")
    else:
        parts.append(f"入 {fmt_num(inp)}")
        parts.append(f"出 {fmt_num(out)}")
        parts.append(_fmt_cache_val(cache, inp))
        parts.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache)}")
    if calls > 0 and session_count != calls:
        parts.append(f"调用 {calls} 次")
    if session_count:
        parts.append(f"{session_count} 轮会话")
    if extra:
        parts.append(extra)
    # 价格
    pc = _get_model_price(model_name)
    if pc:
        parts.append(_fmt_cost(inp, out, cache, pc))
    if not parts:
        parts.append("无数据")
    return f"  {model_name} | {' | '.join(parts)}"


def _build_aligned_raw(agent_display: str, per_model_list: list,
                        has_context: bool = False,
                        extra_footer: str = None) -> str:
    """从 per_model 数据构建列对齐的原始输出（含 Agent 合计行）。"""
    per_model_list = [pm for pm in (per_model_list or []) if not _skip_model(pm)]
    if not per_model_list:
        return f"📊 {agent_display}"

    rows = []
    ti = to = tc = tca = 0
    has_price = _has_any_price(per_model_list)
    for pm in per_model_list:
        mn = pm.get("model", "unknown")
        inp = pm.get("input", 0) or 0
        out = pm.get("output", 0) or 0
        cache = pm.get("cache", 0) or 0
        calls = pm.get("calls", 0) or 0
        total = inp + out
        ti += inp; to += out; tc += cache; tca += calls

        cols = [mn]
        if has_context:
            cw = detect_context(mn)
            if cw:
                pct = round(total / cw * 100, 1) if cw else 0
                cols.append(_progress_bar(pct))
                cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
            else:
                cols.append("")
                cols.append(f"{fmt_num(total)}/-")
        cols.append(f"入 {fmt_num(inp)}")
        cols.append(f"出 {fmt_num(out)}")
        cols.append(_fmt_cache_val(cache, inp))
        cols.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache)}")
        if calls > 0:
            cols.append(f"调用 {calls} 次")
        if has_price:
            pc = _get_model_price(mn)
            cols.append(_fmt_cost(inp, out, cache, pc) if pc else "-")
        rows.append(cols)

    # Agent 合计行
    if len(per_model_list) > 1:
        total_all = ti + to
        subtotal_cols = ["合计"]
        if has_context:
            subtotal_cols.append("")
            subtotal_cols.append("")
        subtotal_cols.append(f"入 {fmt_num(ti)}")
        subtotal_cols.append(f"出 {fmt_num(to)}")
        subtotal_cols.append(_fmt_cache_val(tc, ti))
        subtotal_cols.append(f"总计/+缓存 {fmt_num(total_all)}/{fmt_num(total_all + tc)}")
        subtotal_cols.append(f"调用 {tca} 次")
        if has_price:
            total_cost_str = _fmt_total_cost(_calc_total_cost(per_model_list))
            if total_cost_str:
                subtotal_cols.append(f"{total_cost_str} (仅供参考)")
        rows.append(subtotal_cols)

    aligned = _align_rows(rows)
    lines = [f"📊 {agent_display}"]
    for row in aligned:
        lines.append("  " + " | ".join(row))

    if extra_footer:
        lines.append("  " + "─" * 36)
        lines.append(extra_footer)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════
#  Agent 基类与数据模型
# ═══════════════════════════════════════════════════

@dataclass
class AgentData:
    """单个 Agent 的统计数据"""
    name: str
    display_name: str
    stats: dict
    raw: str
    per_model: list = None  # [{"model": ..., "input": N, "output": N, "calls": N, "cache": N}, ...]


class BaseAgent(ABC):
    """Agent 检测器基类"""

    # 支持实时上下文占比显示（会话型 Agent 为 True，累计型为 False）
    _has_live_context = False

    @staticmethod
    @abstractmethod
    def name() -> str: ...

    @staticmethod
    @abstractmethod
    def display_name() -> str: ...

    @staticmethod
    @abstractmethod
    def detect() -> bool: ...

    @abstractmethod
    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData: ...

    def watch(self, interval: int = 5) -> None:
        """实时监控模式"""
        stop_event = threading.Event()

        def _on_signal(sig, frame):
            stop_event.set()

        old_sigint = signal.signal(signal.SIGINT, _on_signal)
        old_sigterm = None
        try:
            old_sigterm = signal.signal(signal.SIGTERM, _on_signal)
        except (ValueError, AttributeError):
            pass  # Windows 上 SIGTERM 不可用

        def _interruptible_sleep(seconds: float) -> bool:
            """中断式睡眠，返回 False 表示被中断"""
            return not stop_event.wait(timeout=seconds)

        watch_start = time.time()
        # 今日起始时间戳，用于 📅 今日合计查询
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        yesterday_start = None  # 跨天时记录上一个 today_start，用于汇总拆分
        print(f"\n📡 实时监控 [{self.display_name()}] — 每 {interval} 秒刷新 (Ctrl+C 停止)\n")

        # ── 首次基线 ──
        try:
            data_first = self.collect()
        except Exception as e:
            print(f"  ⚠️ 无法读取数据: {e}")
            print("👋 监控已停止")
            return
        bl_models = {}
        if data_first.per_model:
            for pm in data_first.per_model:
                bl_models[pm["model"]] = {
                    "input": pm.get("input", 0),
                    "output": pm.get("output", 0),
                    "calls": pm.get("calls", 0),
                    "cache": pm.get("cache", 0),
                }
        else:
            m = data_first.stats.get("model", "")
            if m and m != "?" and data_first.stats.get("input_tokens", 0) > 0:
                bl_models[m] = {
                    "input": data_first.stats.get("input_tokens", 0),
                    "output": data_first.stats.get("output_tokens", 0),
                    "calls": data_first.stats.get("api_calls", 0),
                    "cache": data_first.stats.get("cache_read", 0),
                }

        # ── 初始状态 ──
        bl_initial = {k: dict(v) for k, v in bl_models.items()}
        print("初始状态:")
        has_data = False
        has_cache = any(mv.get("cache", 0) for mv in bl_models.values())
        # 检查是否有配置了价格的模型
        bl_has_price = any(_get_model_price(mn) for mn in bl_models)
        if bl_models:
            init_rows = []
            for mn, mv in bl_models.items():
                total = mv["input"] + mv["output"]
                cols = [mn]
                cache_val = mv.get('cache', 0)
                if self._has_live_context:
                    cw = detect_context(mn)
                    pct = round(total / cw * 100, 1) if cw else 0
                    cols.append(_progress_bar(pct))
                    cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
                cols.append(f"入 {fmt_num(mv['input'])}")
                cols.append(f"出 {fmt_num(mv['output'])}")
                cols.append(_fmt_cache_val(cache_val, mv['input']))
                cols.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache_val)}")
                cols.append(f"调用 {mv['calls']}")
                if bl_has_price:
                    pc = _get_model_price(mn)
                    cols.append(_fmt_cost(mv['input'], mv['output'], cache_val, pc) if pc else "-")
                init_rows.append(cols)
                has_data = True
            aligned = _align_rows(init_rows)
            for row in aligned:
                print(f"  {' | '.join(row)}")
        if not has_data:
            print("  (暂无数据，等待会话开始...)")
        print()

        # ── 监控循环（先采集再 sleep，保证间隔准确）──
        tick_count = 0
        while not stop_event.is_set():
            tick_start = time.monotonic()
            tick_count += 1
            try:
                data = self.collect()
            except Exception as e:
                print(f"  ⚠️ {e}")
                if not _interruptible_sleep(interval):
                    break
                continue

            now_models = {}
            if data.per_model:
                for pm in data.per_model:
                    now_models[pm["model"]] = {
                        "input": pm.get("input", 0),
                        "output": pm.get("output", 0),
                        "calls": pm.get("calls", 0),
                        "cache": pm.get("cache", 0),
                    }
            else:
                m = data.stats.get("model", "?")
                now_models[m] = {
                    "input": data.stats.get("input_tokens", 0),
                    "output": data.stats.get("output_tokens", 0),
                    "calls": data.stats.get("api_calls", 0),
                    "cache": data.stats.get("cache_read", 0),
                }

            # 对比上一次状态，列出增量
            changed_models = []
            total_delta_tok = 0
            total_delta_calls = 0
            for mn, mv in now_models.items():
                bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                d_in = mv["input"] - bl["input"]
                d_out = mv["output"] - bl["output"]
                d_calls = mv["calls"] - bl["calls"]
                d_cache = mv["cache"] - bl["cache"]
                d_tok = d_in + d_out
                if d_tok > 0 or d_calls > 0 or d_cache > 0:
                    changed_models.append((mn, d_in, d_out, d_tok, d_calls, d_cache))
                    total_delta_tok += d_tok
                    total_delta_calls += d_calls
                elif d_tok < 0 or d_calls < 0:
                    bl_models[mn] = mv

            ts = datetime.now().strftime("%H:%M:%S")

            # 跨天检测：午夜过后自动切换"今日"基准
            new_today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            if new_today_start > today_start:
                yesterday_start = today_start
                today_start = new_today_start
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print()
                print("  " + "═" * 58)
                print(f"  跨天切换 — 当前时间 {now_str}")
                print("  新的一天开始，\"今日\"数据已重置")
                print("  " + "═" * 58)
                print()

            any_delta = bool(changed_models)
            if any_delta:
                summary_parts = []
                if total_delta_tok > 0:
                    summary_parts.append(f"+{fmt_num(total_delta_tok)} tokens")
                elif total_delta_tok < 0:
                    summary_parts.append(f"{fmt_num(total_delta_tok)} tokens")
                if total_delta_calls > 0:
                    summary_parts.append(f"+{total_delta_calls} 调用")
                elif total_delta_calls < 0:
                    summary_parts.append(f"{total_delta_calls} 调用")
                # 增量费用
                delta_cost = 0.0
                delta_currency = "CNY"
                for mn, mv in now_models.items():
                    bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                    d_in = mv["input"] - bl["input"]
                    d_out = mv["output"] - bl["output"]
                    d_cache = mv.get("cache", 0) - bl.get("cache", 0)
                    pc = _get_model_price(mn)
                    if pc and (d_in or d_out or d_cache):
                        delta_cost += _to_cny(_calc_cost(d_in, d_out, d_cache, pc), pc.get("currency", "CNY"))
                if delta_cost > 0:
                    summary_parts.append(f"≈¥{delta_cost:.4f}")
                print(f"── [{ts}] {' '.join(summary_parts)} ──")

                # 增量行（仅展示本轮有变化的模型）
                print("  ╌" * 30)
                any_cache_now = any(
                    mv.get("cache", 0) or (mv.get("cache", 0) - bl_models.get(mn, {}).get("cache", 0))
                    for mn, mv in now_models.items()
                )
                delta_has_price = any(_get_model_price(mn) for mn in now_models)
                delta_rows = []
                idle_models = []
                for mn, mv in now_models.items():
                    bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                    d_in = mv["input"] - bl["input"]
                    d_out = mv["output"] - bl["output"]
                    d_tok = d_in + d_out
                    d_cache = mv.get("cache", 0) - bl.get("cache", 0)
                    d_calls = mv["calls"] - bl["calls"]
                    has_delta = d_tok > 0 or d_cache > 0 or d_calls > 0
                    total = mv["input"] + mv["output"]

                    if total == 0 and mv["calls"] == 0:
                        idle_models.append(mn)
                        bl_models[mn] = mv
                        continue

                    if not has_delta:
                        continue

                    cols = [mn]
                    if self._has_live_context:
                        cw = detect_context(mn)
                        pct = round(total / cw * 100, 1) if cw else 0
                        cols.append(_progress_bar(pct))
                        cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
                    cols.append(f"入 +{fmt_num(d_in)}")
                    cols.append(f"出 +{fmt_num(d_out)}")
                    if any_cache_now:
                        rate = _calc_cache_rate(d_in, d_cache)
                        if rate is not None:
                            cols.append(f"缓 +{fmt_num(d_cache)} ({min(rate, 99.9):.1f}%)")
                        else:
                            cols.append(f"缓 +{fmt_num(d_cache)}")
                    d_total = d_in + d_out
                    cols.append(f"总计/+缓存 +{fmt_num(d_total)}/+{fmt_num(d_total + d_cache)}")
                    cols.append(f"调用 +{d_calls}")
                    if delta_has_price:
                        pc = _get_model_price(mn)
                        if pc and (d_in or d_out or d_cache):
                            dc = _to_cny(_calc_cost(d_in, d_out, d_cache, pc), pc.get("currency", "CNY"))
                            cols.append(f"≈¥{dc:.4f}")
                        else:
                            cols.append("-")

                    delta_rows.append((cols, mn, mv))

                if delta_rows:
                    aligned = _align_rows([r[0] for r in delta_rows])
                    for (cols, mn, mv), aligned_cols in zip(delta_rows, aligned):
                        print(f"  {' | '.join(aligned_cols)}")
                        bl_models[mn] = mv
                if idle_models:
                    print(f"  (未使用: {', '.join(idle_models)})")
                print("  ╌" * 30)

                # 📅 今日合计
                try:
                    today_data = self.collect(from_ts=today_start)
                    print(f"  ╌╌╌╌╌ 📅 今日 ╌╌╌╌╌")
                    ti = to = tc = tca = 0
                    today_models = today_data.per_model or []
                    today_rows = []
                    today_has_price = _has_any_price(today_models)
                    for pm in today_models:
                        m = pm.get("model", "?")
                        i = pm.get("input", 0) or 0
                        o = pm.get("output", 0) or 0
                        c = pm.get("cache", 0) or 0
                        ca = pm.get("calls", 0) or 0
                        if i == 0 and o == 0 and ca == 0:
                            continue
                        ti += i; to += o; tc += c; tca += ca
                        t = i + o
                        cols = [m, f"入 {fmt_num(i)}", f"出 {fmt_num(o)}",
                                _fmt_cache_val(c, i),
                                f"总计/+缓存 {fmt_num(t)}/{fmt_num(t + c)}", f"调用 {ca}"]
                        if today_has_price:
                            pc = _get_model_price(m)
                            cols.append(_fmt_cost(i, o, c, pc) if pc else "-")
                        today_rows.append(cols)
                    if today_rows:
                        if len(today_models) > 1:
                            sum_row = ["今日合计", f"入 {fmt_num(ti)}", f"出 {fmt_num(to)}",
                                       _fmt_cache_val(tc, ti),
                                       f"总计/+缓存 {fmt_num(ti + to)}/{fmt_num(ti + to + tc)}", f"调用 {tca}"]
                            if today_has_price:
                                tc_sum_str = _fmt_total_cost(_calc_total_cost(today_models))
                                if tc_sum_str:
                                    sum_row.append(f"{tc_sum_str} (仅供参考)")
                            today_rows.append(sum_row)
                        aligned = _align_rows(today_rows)
                        for row in aligned:
                            print(f"  {' | '.join(row)}")
                    print("  ╌" * 30)
                except Exception:
                    pass
            else:
                print(f"── [{ts}] 无新活动 ──")

            # 每轮无条件更新 baseline，防止因数据竞态导致 delta 累积假 spike
            for mn, mv in now_models.items():
                bl_models[mn] = mv
            for mn in list(bl_models.keys()):
                if mn not in now_models:
                    del bl_models[mn]

            # 精确间隔补偿
            elapsed = time.monotonic() - tick_start
            if elapsed < interval and not stop_event.is_set():
                _interruptible_sleep(interval - elapsed)

        # ── 停止汇总：基于最新累计值 ──
        print()
        print("━" * 60)
        print("  📊 本次监控汇总")
        print("━" * 60)

        # 最终累计状态
        if bl_models:
            print("  最终状态:")
            final_rows = []
            bl_has_price = any(_get_model_price(mn) for mn in bl_models)
            for mn, mv in sorted(bl_models.items()):
                total = mv["input"] + mv["output"]
                cache_v = mv.get("cache", 0)
                cols = [mn]
                if self._has_live_context:
                    cw = detect_context(mn)
                    pct = round(total / cw * 100, 1) if cw else 0
                    cols.append(_progress_bar(pct))
                    cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
                cols.append(f"入 {fmt_num(mv['input'])}")
                cols.append(f"出 {fmt_num(mv['output'])}")
                cols.append(_fmt_cache_val(cache_v, mv['input']))
                cols.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache_v)}")
                cols.append(f"调用 {mv['calls']}")
                if bl_has_price:
                    pc = _get_model_price(mn)
                    cols.append(_fmt_cost(mv['input'], mv['output'], cache_v, pc) if pc else "-")
                final_rows.append(cols)
            aligned = _align_rows(final_rows)
            for row in aligned:
                print(f"  {' | '.join(row)}")

            # 📅 今日累计
            try:
                today_data = self.collect(from_ts=today_start)
                ti = to = tc = tca = 0
                today_models = today_data.per_model or []
                today_rows = []
                today_has_price = _has_any_price(today_models)
                for pm in today_models:
                    m = pm.get("model", "?")
                    i = pm.get("input", 0) or 0
                    o = pm.get("output", 0) or 0
                    c = pm.get("cache", 0) or 0
                    ca = pm.get("calls", 0) or 0
                    if i == 0 and o == 0 and ca == 0:
                        continue
                    ti += i; to += o; tc += c; tca += ca
                    t = i + o
                    cols = [m, f"入 {fmt_num(i)}", f"出 {fmt_num(o)}",
                            _fmt_cache_val(c, i),
                            f"总计/+缓存 {fmt_num(t)}/{fmt_num(t + c)}", f"调用 {ca}"]
                    if today_has_price:
                        pc = _get_model_price(m)
                        cols.append(_fmt_cost(i, o, c, pc) if pc else "-")
                    today_rows.append(cols)
                if today_rows:
                    today_label = datetime.fromtimestamp(today_start).strftime("%Y-%m-%d")
                    print(f"\n  ╌╌╌╌╌ 📅 今日累计 ({today_label}) ╌╌╌╌╌")
                    if len(today_models) > 1:
                        sum_row = ["今日合计", f"入 {fmt_num(ti)}", f"出 {fmt_num(to)}",
                                   _fmt_cache_val(tc, ti),
                                   f"总计/+缓存 {fmt_num(ti + to)}/{fmt_num(ti + to + tc)}", f"调用 {tca}"]
                        if today_has_price:
                            tcs_str = _fmt_total_cost(_calc_total_cost(today_models))
                            if tcs_str:
                                sum_row.append(f"{tcs_str} (仅供参考)")
                        today_rows.append(sum_row)
                    aligned = _align_rows(today_rows)
                    for row in aligned:
                        print(f"  {' | '.join(row)}")
                    print("  ╌" * 30)
            except Exception:
                pass

            # 📅 昨日累计（仅在跨天时显示）
            if yesterday_start is not None:
                try:
                    yesterday_data = self.collect(from_ts=yesterday_start, to_ts=today_start - 1)
                    yti = yto = ytc = ytca = 0
                    yesterday_models = yesterday_data.per_model or []
                    yesterday_rows = []
                    yest_has_price = _has_any_price(yesterday_models)
                    for pm in yesterday_models:
                        m = pm.get("model", "?")
                        i = pm.get("input", 0) or 0
                        o = pm.get("output", 0) or 0
                        c = pm.get("cache", 0) or 0
                        ca = pm.get("calls", 0) or 0
                        if i == 0 and o == 0 and ca == 0:
                            continue
                        yti += i; yto += o; ytc += c; ytca += ca
                        t = i + o
                        cols = [m, f"入 {fmt_num(i)}", f"出 {fmt_num(o)}",
                                _fmt_cache_val(c, i),
                                f"总计/+缓存 {fmt_num(t)}/{fmt_num(t + c)}", f"调用 {ca}"]
                        if yest_has_price:
                            pc = _get_model_price(m)
                            cols.append(_fmt_cost(i, o, c, pc) if pc else "-")
                        yesterday_rows.append(cols)
                    if yesterday_rows:
                        yesterday_label = datetime.fromtimestamp(yesterday_start).strftime("%Y-%m-%d")
                        print(f"\n  ╌╌╌╌╌ 📅 昨日累计 ({yesterday_label}) ╌╌╌╌╌")
                        if len(yesterday_rows) > 1:
                            sum_row = ["昨日合计", f"入 {fmt_num(yti)}", f"出 {fmt_num(yto)}",
                                       _fmt_cache_val(ytc, yti),
                                       f"总计/+缓存 {fmt_num(yti + yto)}/{fmt_num(yti + yto + ytc)}", f"调用 {ytca}"]
                            if yest_has_price:
                                ycs_str = _fmt_total_cost(_calc_total_cost(yesterday_models))
                                if ycs_str:
                                    sum_row.append(f"{ycs_str} (仅供参考)")
                            yesterday_rows.append(sum_row)
                        aligned = _align_rows(yesterday_rows)
                        for row in aligned:
                            print(f"  {' | '.join(row)}")
                        print("  ╌" * 30)
                except Exception:
                    pass

            # 总增量（最新累计 - 初始基线）
            total_d_tok = total_d_cache = total_d_calls = 0
            total_d_in = total_d_out = 0
            total_d_cost = 0.0
            any_d_cache = False
            delta_data = []
            for mn, mv in sorted(bl_models.items()):
                init = bl_initial.get(mn, {"input": 0, "output": 0, "cache": 0, "calls": 0})
                d_in = mv["input"] - init["input"]
                d_out = mv["output"] - init["output"]
                d_tok = d_in + d_out
                d_cache = mv.get("cache", 0) - init.get("cache", 0)
                d_calls = mv["calls"] - init["calls"]
                total_d_in += d_in; total_d_out += d_out
                total_d_tok += d_tok; total_d_cache += d_cache; total_d_calls += d_calls
                if d_tok > 0 or d_cache > 0 or d_calls > 0:
                    if d_cache:
                        any_d_cache = True
                    pc = _get_model_price(mn)
                    if pc:
                        dc = _to_cny(_calc_cost(d_in, d_out, d_cache, pc), pc.get("currency", "CNY"))
                        total_d_cost += dc
                    delta_data.append((mn, d_tok, d_in, d_out, d_cache, d_calls, pc))

            if delta_data:
                print(f"\n  监控期间增量:")
                print("  ╌" * 30)
                inc_rows = []
                for (mn, d_tok, d_in, d_out, d_cache, d_calls, pc) in delta_data:
                    cols = [mn, f"+{fmt_num(d_tok)}总计", f"+{fmt_num(d_in)}入", f"+{fmt_num(d_out)}出"]
                    if any_d_cache:
                        cols.append(f"+{fmt_num(d_cache)}存")
                    cols.append(f"+{d_calls}调用")
                    if pc and (d_in or d_out or d_cache):
                        dc = _to_cny(_calc_cost(d_in, d_out, d_cache, pc), pc.get("currency", "CNY"))
                        cols.append(f"≈¥{dc:.4f}")
                    inc_rows.append(cols)
                aligned = _align_rows(inc_rows)
                for row in aligned:
                    print(f"  {' | '.join(row)}")
                if len(delta_data) > 1:
                    sum_parts = [f"+{fmt_num(total_d_tok)}总计",
                                 f"+{fmt_num(total_d_in)}入",
                                 f"+{fmt_num(total_d_out)}出"]
                    if total_d_cache:
                        sum_parts.append(f"+{fmt_num(total_d_cache)}存")
                    sum_parts.append(f"+{total_d_calls}调用")
                    if total_d_cost > 0:
                        sum_parts.append(f"≈¥{total_d_cost:.4f}")
                    print(f"  增量合计 | {' | '.join(sum_parts)}")
                print("  ╌" * 30)
        else:
            print("  监控期间无数据")

        duration = time.time() - watch_start
        if duration < 60:
            dur_str = f"{duration:.0f} 秒"
        elif duration < 3600:
            dur_str = f"{duration / 60:.0f} 分 {duration % 60:.0f} 秒"
        else:
            dur_str = f"{duration / 3600:.0f} 时 {(duration % 3600) / 60:.0f} 分"
        print(f"  监控时长: {dur_str} | 采集 {tick_count} 轮")
        if yesterday_start is not None:
            yesterday_label = datetime.fromtimestamp(yesterday_start).strftime("%Y-%m-%d")
            today_label = datetime.fromtimestamp(today_start).strftime("%Y-%m-%d")
            print(f"  ⚠️ 监控跨越 {yesterday_label} → {today_label}，跨天时\"今日\"数据已重置")
        print("👋 监控已停止")


# ═══════════════════════════════════════════════════
#  Hermes
# ═══════════════════════════════════════════════════

def _find_hermes_db() -> str:
    """获取 Hermes 数据库路径，优先从配置读取"""
    cfg = _load_agent_paths()
    if "hermes_db" in cfg:
        return cfg["hermes_db"]
    return _resolve_path(".hermes/state.db")


def _find_hermes_sessions() -> str:
    """获取 Hermes sessions 文件路径，优先从配置读取"""
    cfg = _load_agent_paths()
    if "hermes_sessions" in cfg:
        return cfg["hermes_sessions"]
    return _resolve_path(".hermes/sessions/sessions.json")


def _hermes_current_session_id() -> str | None:
    """从 sessions.json 读取当前活跃会话 ID。"""
    sessions_path = _find_hermes_sessions()
    try:
        with open(sessions_path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        for key, val in data.items():
            if isinstance(val, dict) and val.get("session_id"):
                return val["session_id"]
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return None


class HermesAgent(BaseAgent):
    _has_live_context = True  # 有当前会话概念，上下文占比有意义

    @staticmethod
    def name() -> str:
        return "hermes"

    @staticmethod
    def display_name() -> str:
        return "Hermes"

    @staticmethod
    def detect() -> bool:
        db = _find_hermes_db()
        if os.path.exists(db):
            return True
        # WSL 路径可能 UNC 不通但 wsl.exe 已验证存在（_resolve_path 已处理）
        return db != os.path.join(os.path.expanduser("~"), ".hermes", "state.db")

    def _try_wsl_fallback(self, hermes_db, error_msg, from_ts=None, to_ts=None):
        """WSL 路径 DB 不可用时，通过 wsl.exe 在 WSL 内读取。"""
        distro, _ = _wsl_unc_to_linux(hermes_db)
        if not distro:
            return None
        if "locked" not in error_msg.lower() and "unable to open" not in error_msg.lower():
            return None
        result = _hermes_collect_via_wsl(hermes_db, from_ts, to_ts)
        if not result:
            return None
        if not result.get("rows"):
            # WSL 查询成功但该时段无数据，返回空 AgentData
            label = "Hermes (WSL)"
            return AgentData(name="hermes", display_name=label,
                             stats={}, raw=f"{label}: 该时间段内无会话记录", per_model=[])
        rows = result["rows"]
        per_model_list = []
        ti = to = tc = tca = tsess = 0
        for r in rows:
            m = r.get("model") or "unknown"
            inp = int(r.get("inp") or 0)
            out = int(r.get("out") or 0)
            cache = int(r.get("cache") or 0)
            calls = int(r.get("calls") or 0)
            cnt = int(r.get("cnt") or 0)
            ti += inp; to += out; tc += cache; tca += calls; tsess += cnt
            per_model_list.append({"model": m, "input": inp, "output": out, "calls": calls, "cache": cache})
        extra_footer = f"  会话: {tsess} 轮"
        raw = _build_aligned_raw("Hermes (WSL)", per_model_list,
                                 has_context=True,
                                 extra_footer=extra_footer)
        stats = {
            "model": ", ".join(sorted({(r.get("model") or "unknown") for r in rows})),
            "input_tokens": ti, "output_tokens": to, "cache_read": tc,
            "api_calls": tca, "total_tokens": ti + to, "session_count": tsess,
        }
        return AgentData(name="hermes", display_name="Hermes", stats=stats, raw=raw, per_model=per_model_list)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        hermes_db = _find_hermes_db()
        # WSL UNC 路径跳过直连（通过 UNC 打开 SQLite 极慢，timeout 会被放大到 ~30s）
        if _is_wsl_unc(hermes_db):
            fb = self._try_wsl_fallback(hermes_db, "database is locked (WSL UNC)", from_ts, to_ts)
            if fb:
                return fb
            # WSL fallback 不可用，回退到直连尝试
        try:
            return self._collect_impl(hermes_db, from_ts, to_ts)
        except Exception as e:
            fb = self._try_wsl_fallback(hermes_db, str(e), from_ts, to_ts)
            if fb:
                return fb
            raise

    def _collect_impl(self, hermes_db, from_ts, to_ts):
        conn = sqlite3.connect(hermes_db, timeout=10)
        conn.row_factory = sqlite3.Row

        # ── schema 兼容：检测旧版 Hermes 缺少的列 ──
        has_api_calls = True
        has_tool_calls = True
        try:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(sessions)").fetchall()}
            if "api_call_count" not in cols:
                has_api_calls = False
            if "tool_call_count" not in cols:
                has_tool_calls = False
        except Exception:
            pass

        if from_ts is not None or to_ts is not None:
            # ── 时间段统计 ──
            where = []
            params = []
            if from_ts is not None:
                # ended_at IS NULL 仅对 1 天内的会话放行，避免旧会话 ended_at 残留 NULL
                grace = from_ts - 86400
                where.append("(started_at >= ? OR (ended_at IS NULL AND started_at >= ?) OR (ended_at IS NOT NULL AND ended_at >= ?))")
                params.append(from_ts)
                params.append(grace)
                params.append(from_ts)
            if to_ts is not None:
                where.append("started_at <= ?")
                params.append(to_ts)
            clause = " AND ".join(where)

            calls_expr = "SUM(api_call_count)" if has_api_calls else "0"
            tools_expr = "SUM(tool_call_count)" if has_tool_calls else "0"
            cur = conn.execute(
                f"SELECT model, SUM(input_tokens) as inp, SUM(output_tokens) as out, "
                f"SUM(cache_read_tokens) as cache, {calls_expr} as calls, "
                f"{tools_expr} as tools, COUNT(*) as cnt "
                f"FROM sessions WHERE {clause} GROUP BY model",
                params
            )
            rows = cur.fetchall()
            conn.close()

            if not rows:
                return AgentData(
                    name="hermes", display_name="Hermes",
                    stats={}, raw="Hermes: 该时间段内无会话记录"
                )

            total_inp = sum(r["inp"] or 0 for r in rows)
            total_out = sum(r["out"] or 0 for r in rows)
            total_cache = sum(r["cache"] or 0 for r in rows)
            total_calls = sum(r["calls"] or 0 for r in rows)
            total_sessions = sum(r["cnt"] or 0 for r in rows)

            per_model_list = []
            for r in rows:
                m = r["model"] or "unknown"
                inp = r["inp"] or 0
                out = r["out"] or 0
                cache = r["cache"] or 0
                calls = r["calls"] or 0
                per_model_list.append({"model": m, "input": inp, "output": out,
                                        "calls": calls, "cache": cache})

            extra_footer = f"  会话: {total_sessions} 轮"
            raw = _build_aligned_raw("Hermes", per_model_list,
                                     has_context=True,
                                     extra_footer=extra_footer)

            stats = {
                "model": ", ".join(sorted({r["model"] or "unknown" for r in rows})),
                "input_tokens": total_inp,
                "output_tokens": total_out,
                "cache_read": total_cache,
                "api_calls": total_calls,
                "total_tokens": total_inp + total_out,
                "session_count": total_sessions,
            }

            return AgentData(name="hermes", display_name="Hermes",
                             stats=stats, raw=raw, per_model=per_model_list)

        # ── 全部会话统计（无时间筛选）──
        calls_expr = "SUM(api_call_count)" if has_api_calls else "0"
        tools_expr = "SUM(tool_call_count)" if has_tool_calls else "0"
        cur = conn.execute(
            f"SELECT model, SUM(input_tokens) as inp, SUM(output_tokens) as out, "
            f"SUM(cache_read_tokens) as cache, {calls_expr} as calls, "
            f"{tools_expr} as tools, COUNT(*) as cnt "
            f"FROM sessions GROUP BY model"
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return AgentData(
                name="hermes", display_name="Hermes",
                stats={}, raw="Hermes: 尚无会话记录"
            )

        total_inp = sum(r["inp"] or 0 for r in rows)
        total_out = sum(r["out"] or 0 for r in rows)
        total_cache = sum(r["cache"] or 0 for r in rows)
        total_calls = sum(r["calls"] or 0 for r in rows)
        total_sessions = sum(r["cnt"] or 0 for r in rows)

        per_model_list = []
        for r in rows:
            m = r["model"] or "unknown"
            inp = r["inp"] or 0
            out = r["out"] or 0
            cache = r["cache"] or 0
            calls = r["calls"] or 0
            per_model_list.append({"model": m, "input": inp, "output": out,
                                    "calls": calls, "cache": cache})

        extra_footer = f"  会话: {total_sessions} 轮"
        raw = _build_aligned_raw("Hermes", per_model_list,
                                 has_context=True,
                                 extra_footer=extra_footer)

        stats = {
            "model": ", ".join(sorted({r["model"] or "unknown" for r in rows})),
            "input_tokens": total_inp,
            "output_tokens": total_out,
            "cache_read": total_cache,
            "api_calls": total_calls,
            "total_tokens": total_inp + total_out,
            "session_count": total_sessions,
        }

        return AgentData(name="hermes", display_name="Hermes",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  Claude Code
# ═══════════════════════════════════════════════════

def _find_claude_dir() -> str:
    """获取 Claude Code 目录，优先从配置读取"""
    cfg = _load_agent_paths()
    if "claude_dir" in cfg:
        return cfg["claude_dir"]
    return _resolve_path(".claude")


class ClaudeCodeAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "claude-code"

    @staticmethod
    def display_name() -> str:
        return "Claude Code"

    @staticmethod
    def detect() -> bool:
        cd = _find_claude_dir()
        if os.path.isdir(os.path.join(cd, "projects")):
            return True
        native = os.path.join(os.path.expanduser("~"), ".claude")
        return cd != native

    def _find_sessions(self, from_ts: float = None, to_ts: float = None):
        projects_dir = os.path.join(_find_claude_dir(), "projects")
        if not os.path.isdir(projects_dir):
            return []
        sessions = []
        for proj in os.listdir(projects_dir):
            proj_dir = os.path.join(projects_dir, proj)
            if not os.path.isdir(proj_dir):
                continue
            for root, _dirs, files in os.walk(proj_dir):
                for fname in files:
                    if fname.endswith(".jsonl") and not fname.endswith(".trajectory.jsonl"):
                        fpath = os.path.join(root, fname)
                        sessions.append((proj, fname, fpath))
        return sorted(sessions, key=lambda x: os.path.getmtime(x[2]), reverse=True)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        # 缓存策略：带时间筛选时优先用缓存；无筛选时从磁盘重读并更新缓存
        want_cache = from_ts is not None or to_ts is not None

        if want_cache and hasattr(self, '_cache') and self._cache is not None:
            # 带时间筛选 + 缓存存在 → 直接复用（导出场景按月拆分、watch 今日合计）
            messages = self._cache
        else:
            # 从磁盘重新读取并更新缓存
            sessions = self._find_sessions()
            self._cached_session_count = len(sessions)
            self._cached_sub_count = 0
            self._cached_project_count = 0
            messages = []
            projects = set()

            if sessions:
                for proj, fname, fpath in sessions:
                    projects.add(proj)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if not line:
                                    continue
                                try:
                                    msg = json.loads(line)
                                except json.JSONDecodeError:
                                    continue
                                if msg.get("toolUseResult") and "usage" in msg["toolUseResult"]:
                                    self._cached_sub_count += 1
                                if msg.get("type") != "assistant":
                                    continue
                                model = msg.get("message", {}).get("model") or msg.get("model", "unknown")
                                usage = msg.get("message", {}).get("usage") or msg.get("usage", {})
                                ts_str = msg.get("timestamp", "")
                                try:
                                    dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                                    msg_ts = dt.timestamp()
                                except (ValueError, TypeError):
                                    msg_ts = None
                                messages.append({
                                    'ts': msg_ts,
                                    'model': model,
                                    'input': usage.get('input_tokens', 0),
                                    'output': usage.get('output_tokens', 0),
                                    'cache': usage.get('cache_read_input_tokens', 0),
                                })
                    except Exception:
                        continue
                self._cached_project_count = len(projects)
            # 总是缓存，方便后续复用（如 watch 模式的今日合计查询）
            self._cache = messages

        # 按时间范围过滤
        per_model_data = {}
        for msg in messages:
            if msg['ts'] is not None:
                if from_ts is not None and msg['ts'] < from_ts:
                    continue
                if to_ts is not None and msg['ts'] > to_ts:
                    continue
            model = msg['model']
            if model.startswith("<"):
                model = "subagent"
            if model not in per_model_data:
                per_model_data[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
            per_model_data[model]["input"] += msg['input']
            per_model_data[model]["output"] += msg['output']
            per_model_data[model]["cache"] += msg['cache']
            per_model_data[model]["calls"] += 1

        if not per_model_data:
            return AgentData(
                name="claude-code", display_name="Claude Code",
                stats={}, raw="Claude Code: 会话文件中未解析到有效数据"
            )

        total_calls = sum(d["calls"] for d in per_model_data.values())
        total_input = sum(d["input"] for d in per_model_data.values())
        total_output = sum(d["output"] for d in per_model_data.values())
        total_cache = sum(d["cache"] for d in per_model_data.values())
        models_sorted = sorted(per_model_data.keys())

        meaningful_models = [
            mn for mn in models_sorted
            if per_model_data[mn]["input"] + per_model_data[mn]["output"] > 0
        ]

        per_model_list = []
        for mn in meaningful_models:
            md = per_model_data[mn]
            per_model_list.append({
                "model": mn,
                "input": md["input"],
                "output": md["output"],
                "calls": md["calls"],
                "cache": md["cache"],
            })

        extra_footer = f"  子代理: {self._cached_sub_count} 次 | 会话: {self._cached_session_count} 个 | 项目: {self._cached_project_count} 个"
        raw = _build_aligned_raw("Claude Code", per_model_list,
                                 has_context=False,
                                 extra_footer=extra_footer)

        stats = {
            "model": ", ".join(models_sorted),
            "input_tokens": total_input,
            "output_tokens": total_output,
            "cache_read": total_cache,
            "api_calls": total_calls,
            "sub_calls": self._cached_sub_count,
            "total_tokens": total_input + total_output,
            "session_count": self._cached_session_count,
            "projects": self._cached_project_count,
        }

        return AgentData(name="claude-code", display_name="Claude Code",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  CodeX
# ═══════════════════════════════════════════════════

def _find_codex_db() -> Optional[str]:
    """获取 CodeX 数据库路径，优先从配置读取"""
    cfg = _load_agent_paths()
    if "codex_dir" in cfg:
        codex_dir = cfg["codex_dir"]
        if os.path.isdir(codex_dir):
            dbs = sorted(
                [f for f in os.listdir(codex_dir) if re.match(r'^state_\d+\.sqlite$', f)],
                reverse=True
            )
            return os.path.join(codex_dir, dbs[0]) if dbs else None
    # 回退到标准路径（含 WSL）
    codex_dir = _resolve_path(".codex")
    if not os.path.isdir(codex_dir):
        return None
    dbs = sorted(
        [f for f in os.listdir(codex_dir) if re.match(r'^state_\d+\.sqlite$', f)],
        reverse=True
    )
    return os.path.join(codex_dir, dbs[0]) if dbs else None


class CodeXAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "codex"

    @staticmethod
    def display_name() -> str:
        return "CodeX"

    @staticmethod
    def detect() -> bool:
        db = _find_codex_db()
        if db is not None:
            if os.path.isdir(db) or os.path.exists(db):
                return True
            native = os.path.join(os.path.expanduser("~"), ".codex")
            return db != native
        return False

    def _codex_wsl_fallback(self, db, from_ts, to_ts):
        """WSL UNC 路径：通过 wsl.exe 在 WSL 内查询 CodeX 数据库。"""
        result = _codex_collect_via_wsl(db, from_ts, to_ts)
        if not result or not result.get("rows"):
            return AgentData(
                name="codex", display_name="CodeX (WSL)",
                stats={}, raw="CodeX (WSL): 该时间段内无会话记录", per_model=[]
            )
        rows = result["rows"]
        per_model_list = []
        total_tok = total_cnt = 0
        for r in rows:
            model = r.get("model") or r.get("model_provider") or "codex-default"
            ts = int(r.get("tokens") or 0)
            cnt = int(r.get("cnt") or 0)
            per_model_list.append({"model": model, "input": ts, "output": 0, "calls": cnt, "cache": 0})
            total_tok += ts
            total_cnt += cnt
        stats = {
            "model": ", ".join(sorted({pm["model"] for pm in per_model_list})),
            "total_tokens": total_tok, "session_count": total_cnt,
        }
        raw = _build_aligned_raw("CodeX (WSL)", per_model_list)
        return AgentData(name="codex", display_name="CodeX", stats=stats, raw=raw, per_model=per_model_list)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        db = _find_codex_db()
        if not db:
            return AgentData(
                name="codex", display_name="CodeX",
                stats={}, raw="CodeX: 未检测到数据库文件"
            )
        # WSL UNC 路径跳过直连
        if _is_wsl_unc(db):
            return self._codex_wsl_fallback(db, from_ts, to_ts)
        try:
            conn = sqlite3.connect(db, timeout=5)
            conn.row_factory = sqlite3.Row

            if from_ts is not None or to_ts is not None:
                where = []
                params = []
                if from_ts is not None:
                    where.append("created_at >= ?")
                    params.append(int(from_ts))
                if to_ts is not None:
                    where.append("created_at <= ?")
                    params.append(int(to_ts))
                clause = " AND ".join(where)

                cur = conn.execute(
                    f"SELECT model, model_provider, SUM(tokens_used) as tokens, COUNT(*) as cnt "
                    f"FROM threads WHERE {clause} GROUP BY model, model_provider",
                    params
                )
                rows = cur.fetchall()
                conn.close()

                if not rows:
                    return AgentData(
                        name="codex", display_name="CodeX",
                        stats={}, raw="CodeX: 该时间段内无会话记录"
                    )

                per_model_list = []
                raw_lines = ["📊 CodeX"]
                total_tok = 0
                total_cnt = 0
                for r in rows:
                    model = r["model"] or r["model_provider"] or "codex-default"
                    ts = r["tokens"] or 0
                    cnt = r["cnt"] or 0
                    per_model_list.append({"model": model, "input": ts, "output": 0,
                                            "calls": cnt, "cache": 0})
                    # CodeX 不区分输入/输出，仅显示总计；thread=session
                    if ts > 0 or cnt > 0:
                        parts = [f"总计 {fmt_num(ts)}"] if ts > 0 else []
                        parts.append(f"{cnt} 轮会话")
                        raw_lines.append(f"  {model} | {' | '.join(parts)}")
                    total_tok += ts
                    total_cnt += cnt

                raw = "\n".join(raw_lines)
                stats = {
                    "model": ", ".join(sorted({r["model"] or "unknown" for r in rows if r["model"]})),
                    "total_tokens": total_tok,
                    "session_count": total_cnt,
                }
                return AgentData(name="codex", display_name="CodeX",
                                 stats=stats, raw=raw, per_model=per_model_list)

            # ── 默认：汇总所有线程（按模型） ──
            cur = conn.execute(
                "SELECT model, model_provider, SUM(tokens_used) as tokens, COUNT(*) as cnt "
                "FROM threads GROUP BY model, model_provider"
            )
            rows = cur.fetchall()

            cur2 = conn.execute("SELECT COUNT(*) as cnt FROM threads")
            total_sessions = cur2.fetchone()["cnt"] or 0
            conn.close()

            if not rows:
                return AgentData(
                    name="codex", display_name="CodeX",
                    stats={}, raw="CodeX: 尚无会话记录"
                )

            per_model_list = []
            raw_lines = ["📊 CodeX"]
            total_tok = 0
            total_cnt = 0
            model_count = 0
            for r in rows:
                model = r["model"] or r["model_provider"] or "codex-default"
                ts = r["tokens"] or 0
                cnt = r["cnt"] or 0
                per_model_list.append({"model": model, "input": ts, "output": 0,
                                        "calls": cnt, "cache": 0})
                # CodeX 不区分输入/输出，仅显示总计；thread=session
                if ts > 0 or cnt > 0:
                    parts = [f"总计 {fmt_num(ts)}"] if ts > 0 else []
                    parts.append(f"{cnt} 轮会话")
                    raw_lines.append(f"  {model} | {' | '.join(parts)}")
                    model_count += 1
                total_tok += ts
                total_cnt += cnt

            # ── 合计（多模型时显示） ──
            if model_count > 1:
                raw_lines.append(f"  {'─' * 36}")
                raw_lines.append(f"  合计 | 总计 {fmt_num(total_tok)} | {total_cnt} 轮会话")

            if len(rows) == 1 and total_sessions > rows[0]["cnt"]:
                raw_lines[-1] = raw_lines[-1].rstrip() + f" | 共 {total_sessions} 次会话"

            raw = "\n".join(raw_lines)
            stats = {
                "model": ", ".join(sorted({r["model"] or "unknown" for r in rows if r["model"]})),
                "total_tokens": total_tok,
                "session_count": total_sessions,
            }
            return AgentData(name="codex", display_name="CodeX",
                             stats=stats, raw=raw, per_model=per_model_list)

        except Exception as e:
            return AgentData(
                name="codex", display_name="CodeX",
                stats={}, raw=f"CodeX: 读取失败 — {e}"
            )


# ═══════════════════════════════════════════════════
#  OpenClaw
# ═══════════════════════════════════════════════════

def _find_openclaw_sessions_dir() -> Optional[str]:
    """获取 OpenClaw 会话目录（含 .jsonl 文件），优先从配置读取"""
    cfg = _load_agent_paths()
    if "openclaw_sessions" in cfg:
        p = cfg["openclaw_sessions"]
        # 可能是 sessions.json 路径（取父目录）或目录路径
        if p.endswith(".json"):
            d = os.path.dirname(p)
            if os.path.isdir(d):
                return d
        elif os.path.isdir(p):
            return p
    candidates = [
        _resolve_path(".openclaw/agents/main/sessions"),
    ]
    for d in candidates:
        if os.path.isdir(d):
            return d
    return None


def _find_openclaw_sessions() -> Optional[str]:
    """检测 OpenClaw 会话索引文件（sessions.json），用于 detect()"""
    cfg = _load_agent_paths()
    if "openclaw_sessions" in cfg:
        p = cfg["openclaw_sessions"]
        if os.path.exists(p):
            return p
    candidates = [
        _resolve_path(".openclaw/agents/main/sessions/sessions.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _openclaw_parse_jsonl(fpath: str, from_ts: float = None, to_ts: float = None) -> dict:
    """解析单个 OpenClaw .jsonl 文件，返回 {model: {input, output, cache, calls}}"""
    per_model = {}
    current_model = "unknown"
    current_provider = ""
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = msg.get("type", "")

                # 跟踪模型切换
                if t == "model_change":
                    p = msg.get("provider", "")
                    m = msg.get("modelId", "")
                    if m:
                        current_model = f"{m} ({p})" if p else m
                        current_provider = p
                    continue

                # 仅处理 assistant 消息
                if t != "message":
                    continue
                mrole = msg.get("message", {}).get("role", "")
                if mrole != "assistant":
                    continue

                # 时间过滤
                ts_str = msg.get("timestamp", "")
                if ts_str and (from_ts is not None or to_ts is not None):
                    try:
                        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        msg_ts = dt.timestamp()
                        if from_ts is not None and msg_ts < from_ts:
                            continue
                        if to_ts is not None and msg_ts > to_ts:
                            continue
                    except (ValueError, TypeError):
                        pass

                usage = msg.get("message", {}).get("usage", {})
                inp = usage.get("input", 0) or 0
                out = usage.get("output", 0) or 0
                cache = usage.get("cacheRead", 0) or 0

                # 获取本次消息的模型名（优先级：msg.model > current_model）
                model = msg.get("message", {}).get("model", "") or current_model
                if model not in per_model:
                    per_model[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                per_model[model]["input"] += inp
                per_model[model]["output"] += out
                per_model[model]["cache"] += cache
                per_model[model]["calls"] += 1
    except Exception:
        return {}
    return per_model


class OpenClawAgent(BaseAgent):
    _has_live_context = True  # 有当前会话概念，上下文占比有意义

    @staticmethod
    def name() -> str:
        return "openclaw"

    @staticmethod
    def display_name() -> str:
        return "OpenClaw"

    @staticmethod
    def detect() -> bool:
        sd = _find_openclaw_sessions_dir()
        sf = _find_openclaw_sessions()
        if sd is not None and os.path.isdir(sd):
            return True
        if sf is not None and os.path.exists(sf):
            return True
        native = os.path.join(os.path.expanduser("~"), ".openclaw")
        if sd and sd != os.path.join(native, "agents", "main", "sessions"):
            return True
        if sf and sf != os.path.join(native, "agents", "main", "sessions", "sessions.json"):
            return True
        return False

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        # ── 模式 A：优先从 .jsonl 文件解析（含真实 usage 数据） ──
        sess_dir = _find_openclaw_sessions_dir()
        if sess_dir is not None:
            try:
                jsonl_files = sorted(
                    [f for f in os.listdir(sess_dir)
                     if f.endswith(".jsonl") and not f.endswith(".trajectory.jsonl")]
                )
            except OSError:
                jsonl_files = []
            if jsonl_files:
                per_model_data = {}
                for fname in jsonl_files:
                    fpath = os.path.join(sess_dir, fname)
                    pm = _openclaw_parse_jsonl(fpath, from_ts, to_ts)
                    for model, d in pm.items():
                        if model not in per_model_data:
                            per_model_data[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                        per_model_data[model]["input"] += d["input"]
                        per_model_data[model]["output"] += d["output"]
                        per_model_data[model]["calls"] += d["calls"]
                        per_model_data[model]["cache"] += d["cache"]

                if not per_model_data:
                    return AgentData(
                        name="openclaw", display_name="OpenClaw",
                        stats={}, raw="OpenClaw: 尚无会话" if from_ts is None else "OpenClaw: 该时间段内无会话"
                    )

                total_input = sum(d["input"] for d in per_model_data.values())
                total_output = sum(d["output"] for d in per_model_data.values())
                total_cache = sum(d["cache"] for d in per_model_data.values())
                total_calls = sum(d["calls"] for d in per_model_data.values())

                models_sorted = sorted(per_model_data.keys())
                per_model_list = []
                raw_lines = ["📊 OpenClaw"]
                for mn in models_sorted:
                    md = per_model_data[mn]
                    per_model_list.append({
                        "model": mn, "input": md["input"], "output": md["output"],
                        "calls": md["calls"], "cache": md["cache"],
                    })
                    cw = detect_context(mn)
                    if from_ts is not None or to_ts is not None:
                        line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                                  md["calls"], session_count=md["calls"])
                    else:
                        line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                                  md["calls"], context_window=cw)
                    if line:
                        raw_lines.append(line)

                raw = "\n".join(raw_lines)
                model_list = ", ".join(models_sorted)
                stats = {
                    "model": model_list,
                    "input_tokens": total_input,
                    "output_tokens": total_output,
                    "cache_read": total_cache,
                    "api_calls": total_calls,
                    "total_tokens": total_input + total_output,
                    "session_count": len(jsonl_files),
                }
                if from_ts is None and to_ts is None:
                    first_model = models_sorted[0] if models_sorted else "unknown"
                    cw = detect_context(first_model)
                    stats["context_window"] = cw
                    stats["context_pct"] = round((total_input + total_output) / cw * 100, 1) if cw else 0

                return AgentData(name="openclaw", display_name="OpenClaw",
                                 stats=stats, raw=raw, per_model=per_model_list)
            # 有目录但无 .jsonl → 降级读 sessions.json

        # ── 模式 B：从 sessions.json 读取（回退方案） ──
        oc_path = _find_openclaw_sessions()
        if oc_path is None:
            return AgentData(
                name="openclaw", display_name="OpenClaw",
                stats={}, raw="OpenClaw: 数据文件不存在"
            )
        try:
            with open(oc_path, encoding="utf-8") as f:
                data = json.load(f)

            agents = []
            if isinstance(data, dict):
                for agent_key, session in data.items():
                    if isinstance(session, dict):
                        if from_ts is not None or to_ts is not None:
                            ts = session.get("startedAt", 0) or session.get("updatedAt", 0)
                            if from_ts is not None and ts < from_ts:
                                continue
                            if to_ts is not None and ts > to_ts:
                                continue
                        agents.append(session)
            elif isinstance(data, list):
                for session in data:
                    if isinstance(session, dict):
                        if from_ts is not None or to_ts is not None:
                            ts = session.get("startedAt", 0) or session.get("updatedAt", 0)
                            if from_ts is not None and ts < from_ts:
                                continue
                            if to_ts is not None and ts > to_ts:
                                continue
                        agents.append(session)

            if not agents:
                return AgentData(
                    name="openclaw", display_name="OpenClaw",
                    stats={}, raw="OpenClaw: 尚无会话" if from_ts is None else "OpenClaw: 该时间段内无会话"
                )

            # 按模型分组聚合（sessions.json 中每个 session 有 model 字段）
            per_model_data = {}
            for s in agents:
                model = s.get("model", "unknown")
                provider = s.get("modelProvider", "")
                model_display = f"{model} ({provider})" if provider else model
                inp = s.get("inputTokens", 0) or 0
                out = s.get("outputTokens", 0) or 0
                cache = s.get("cacheRead", 0) or 0
                if model_display not in per_model_data:
                    per_model_data[model_display] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                per_model_data[model_display]["input"] += inp
                per_model_data[model_display]["output"] += out
                per_model_data[model_display]["cache"] += cache
                per_model_data[model_display]["calls"] += 1

            total_input = sum(d["input"] for d in per_model_data.values())
            total_output = sum(d["output"] for d in per_model_data.values())
            total_cache = sum(d["cache"] for d in per_model_data.values())

            latest = max(agents, key=lambda s: s.get("startedAt", 0) or s.get("updatedAt", 0))
            context = latest.get("contextTokens", DEFAULT_CONTEXT)

            models_sorted = sorted(per_model_data.keys())
            per_model_list = []
            raw_lines = ["📊 OpenClaw"]
            for mn in models_sorted:
                md = per_model_data[mn]
                per_model_list.append({
                    "model": mn, "input": md["input"], "output": md["output"],
                    "calls": md["calls"], "cache": md["cache"],
                })
                cw = context
                if from_ts is not None or to_ts is not None:
                    line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                              md["calls"], session_count=md["calls"])
                else:
                    line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                              md["calls"], context_window=cw)
                if line:
                    raw_lines.append(line)

            raw = "\n".join(raw_lines)
            model_list = ", ".join(models_sorted)
            stats = {
                "model": model_list,
                "input_tokens": total_input,
                "output_tokens": total_output,
                "cache_read": total_cache,
                "total_tokens": total_input + total_output,
                "context_window": context,
                "agent_count": len(agents),
            }
            if from_ts is None and to_ts is None:
                stats["context_pct"] = round((total_input + total_output) / context * 100, 1) if context else 0

            return AgentData(name="openclaw", display_name="OpenClaw",
                             stats=stats, raw=raw, per_model=per_model_list)

        except Exception as e:
            return AgentData(
                name="openclaw", display_name="OpenClaw",
                stats={}, raw=f"OpenClaw: 读取失败 — {e}"
            )


# ═══════════════════════════════════════════════════
#  Reasonix
# ═══════════════════════════════════════════════════

def _find_reasonix_usage() -> Optional[str]:
    """获取 Reasonix usage.jsonl 路径"""
    p = os.path.join(os.path.expanduser("~"), ".reasonix", "usage.jsonl")
    return p if os.path.isfile(p) else None


class ReasonixAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "reasonix"

    @staticmethod
    def display_name() -> str:
        return "Reasonix"

    @staticmethod
    def detect() -> bool:
        return _find_reasonix_usage() is not None

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        usage_path = _find_reasonix_usage()
        if not usage_path:
            return AgentData(
                name="reasonix", display_name="Reasonix",
                stats={}, raw="Reasonix: 未找到 usage.jsonl"
            )

        per_model_data: dict[str, dict] = {}
        session_names: set[str] = set()

        try:
            with open(usage_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # 时间过滤（ts 是 epoch 毫秒）
                    rec_ts = rec.get("ts", 0) / 1000.0
                    if from_ts is not None and rec_ts < from_ts:
                        continue
                    if to_ts is not None and rec_ts > to_ts:
                        continue

                    model = rec.get("model", "unknown")
                    session_names.add(rec.get("session", ""))

                    if model not in per_model_data:
                        per_model_data[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                    per_model_data[model]["input"] += rec.get("promptTokens", 0)
                    per_model_data[model]["output"] += rec.get("completionTokens", 0)
                    per_model_data[model]["cache"] += rec.get("cacheHitTokens", 0)
                    per_model_data[model]["calls"] += 1
        except Exception as e:
            return AgentData(
                name="reasonix", display_name="Reasonix",
                stats={}, raw=f"Reasonix: 读取失败 — {e}"
            )

        if not per_model_data:
            return AgentData(
                name="reasonix", display_name="Reasonix",
                stats={}, raw="Reasonix: usage.jsonl 中无有效数据"
            )

        total_calls = sum(d["calls"] for d in per_model_data.values())
        total_input = sum(d["input"] for d in per_model_data.values())
        total_output = sum(d["output"] for d in per_model_data.values())
        total_cache = sum(d["cache"] for d in per_model_data.values())
        models_sorted = sorted(per_model_data.keys())

        per_model_list = []
        for mn in models_sorted:
            md = per_model_data[mn]
            if md["input"] + md["output"] + md["cache"] + md["calls"] == 0:
                continue
            per_model_list.append({
                "model": mn,
                "input": md["input"],
                "output": md["output"],
                "calls": md["calls"],
                "cache": md["cache"],
            })

        raw = _build_aligned_raw("Reasonix", per_model_list, has_context=False,
                                 extra_footer=f"  会话: {len(session_names)} 个")
        stats = {
            "model": ", ".join(models_sorted),
            "input_tokens": total_input,
            "output_tokens": total_output,
            "cache_read": total_cache,
            "total_tokens": total_input + total_output,
            "api_calls": total_calls,
            "session_count": len(session_names),
        }

        return AgentData(name="reasonix", display_name="Reasonix",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  DeepSeek TUI
# ═══════════════════════════════════════════════════

def _find_deepseek_tui_sessions() -> Optional[str]:
    """获取 DeepSeek TUI sessions 目录"""
    p = os.path.join(os.path.expanduser("~"), ".deepseek", "sessions")
    return p if os.path.isdir(p) else None


class DeepSeekTUIAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "deepseek-tui"

    @staticmethod
    def display_name() -> str:
        return "DeepSeek TUI"

    @staticmethod
    def detect() -> bool:
        d = _find_deepseek_tui_sessions()
        if not d:
            return False
        # 检查是否有 .json 会话文件
        for fname in os.listdir(d):
            if fname.endswith(".json"):
                return True
        return False

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        sessions_dir = _find_deepseek_tui_sessions()
        if not sessions_dir:
            return AgentData(
                name="deepseek-tui", display_name="DeepSeek TUI",
                stats={}, raw="DeepSeek TUI: 未找到 sessions 目录"
            )

        per_model_data: dict[str, dict] = {}
        total_sessions = 0
        total_tool_calls = 0
        total_cost_usd = 0.0
        total_cost_cny = 0.0

        try:
            for fname in sorted(os.listdir(sessions_dir)):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(sessions_dir, fname)
                if not os.path.isfile(fpath):
                    continue
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    continue

                metadata = data.get("metadata")
                if not metadata:
                    continue

                # 时间过滤
                created_str = metadata.get("created_at", "")
                try:
                    created_ts = datetime.fromisoformat(created_str.replace("Z", "+00:00")).timestamp()
                except (ValueError, TypeError):
                    created_ts = None

                if from_ts is not None and created_ts is not None and created_ts < from_ts:
                    continue
                if to_ts is not None and created_ts is not None and created_ts > to_ts:
                    continue

                model = metadata.get("model", "unknown")
                tokens = metadata.get("total_tokens", 0) or 0

                # 统计工具调用次数（messages 中 type=tool_use）
                tool_count = 0
                for msg in data.get("messages", []):
                    for item in msg.get("content", []):
                        if isinstance(item, dict) and item.get("type") == "tool_use":
                            tool_count += 1

                # 提取费用
                cost = metadata.get("cost", {}) or {}
                session_cost_usd = cost.get("session_cost_usd", 0) or 0
                session_cost_cny = cost.get("session_cost_cny", 0) or 0

                if model not in per_model_data:
                    per_model_data[model] = {"tokens": 0, "sessions": 0, "tool_calls": 0,
                                              "cost_usd": 0.0, "cost_cny": 0.0}
                per_model_data[model]["tokens"] += tokens
                per_model_data[model]["sessions"] += 1
                per_model_data[model]["tool_calls"] += tool_count
                per_model_data[model]["cost_usd"] += session_cost_usd
                per_model_data[model]["cost_cny"] += session_cost_cny
                total_sessions += 1
                total_tool_calls += tool_count
                total_cost_usd += session_cost_usd
                total_cost_cny += session_cost_cny
        except Exception as e:
            return AgentData(
                name="deepseek-tui", display_name="DeepSeek TUI",
                stats={}, raw=f"DeepSeek TUI: 读取失败 — {e}"
            )

        if not per_model_data:
            return AgentData(
                name="deepseek-tui", display_name="DeepSeek TUI",
                stats={}, raw="DeepSeek TUI: 尚无会话记录"
            )

        models_sorted = sorted(per_model_data.keys())
        per_model_list = []
        raw_lines = ["📊 DeepSeek TUI"]
        total_tok = 0
        total_cnt = 0
        model_count = 0

        for mn in models_sorted:
            md = per_model_data[mn]
            ts = md["tokens"]
            cnt = md["sessions"]
            per_model_list.append({"model": mn, "input": ts, "output": 0,
                                    "calls": cnt, "cache": 0})
            if ts > 0 or cnt > 0:
                parts = [f"总计 {fmt_num(ts)}"] if ts > 0 else []
                parts.append(f"{cnt} 轮会话")
                if md["tool_calls"] > 0:
                    parts.append(f"工具调用 {md['tool_calls']} 次")
                if md["cost_cny"] > 0:
                    parts.append(f"≈¥{md['cost_cny']:.4f}")
                raw_lines.append(f"  {mn} | {' | '.join(parts)}")
                model_count += 1
            total_tok += ts
            total_cnt += cnt

        if model_count > 1:
            raw_lines.append(f"  {'─' * 36}")
            cost_part = f" | ≈¥{total_cost_cny:.4f}" if total_cost_cny > 0 else ""
            raw_lines.append(f"  合计 | 总计 {fmt_num(total_tok)} | {total_cnt} 轮会话{cost_part}")

        raw = "\n".join(raw_lines)
        stats = {
            "model": ", ".join(models_sorted),
            "total_tokens": total_tok,
            "session_count": total_sessions,
            "tool_calls": total_tool_calls,
            "cost_usd": round(total_cost_usd, 6),
            "cost_cny": round(total_cost_cny, 4),
        }

        return AgentData(name="deepseek-tui", display_name="DeepSeek TUI",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  Agent 注册表
# ═══════════════════════════════════════════════════

ALL_AGENTS: list[type[BaseAgent]] = [
    ClaudeCodeAgent,
    CodeXAgent,
    HermesAgent,
    OpenClawAgent,
    ReasonixAgent,
    DeepSeekTUIAgent,
]


def detect_installed() -> list[type[BaseAgent]]:
    return [cls for cls in ALL_AGENTS if cls.detect()]


def get_agent(name: str) -> BaseAgent:
    for cls in ALL_AGENTS:
        if cls.name() == name.lower().strip():
            return cls()
    raise ValueError(f"不支持的 Agent: {name}")


# ═══════════════════════════════════════════════════
#  交互式菜单
# ═══════════════════════════════════════════════════

def show_menu(installed: list[type[BaseAgent]], *, allow_all: bool = True):
    """交互式菜单。返回 BaseAgent 实例 / 'all' / None(退出)。"""
    print("\n🔍 选择你要查看的 AI 助手：")
    print("─" * 40)
    for i, cls in enumerate(installed, 1):
        print(f"  [{i}] {cls.display_name()}")
    if allow_all:
        print("  [a] 所有")
    print("  [q] 退出")
    print("─" * 40)

    while True:
        try:
            try:
                choice = input("请选择：").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if choice == "q":
                return None
            if allow_all and choice == "a":
                return "all"
            idx = int(choice) - 1
            if 0 <= idx < len(installed):
                return installed[idx]()
            valid = f"1-{len(installed)}"
            if allow_all:
                valid += "、a"
            valid += " 或 q"
            print(f"请输入 {valid}")
        except (ValueError, EOFError):
            valid = f"1-{len(installed)}"
            if allow_all:
                valid += "、a"
            valid += " 或 q"
            print(f"请输入 {valid}")


# ═══════════════════════════════════════════════════
#  导出 — 纯 stdlib XLSX 写入器 + 交互式导出函数
# ═══════════════════════════════════════════════════

import zipfile
import xml.etree.ElementTree as ET

_METRIC_LABELS = {'input': '输入', 'output': '输出', 'cache': '缓存',
                  'cache_ratio': '缓存率', 'calls': '调用',
                  'total': '总计', 'total_with_cache': '总计(含缓存)',
                  'cost': '预估费用'}
_METRIC_ORDER = ['input', 'output', 'cache', 'cache_ratio', 'calls', 'total', 'total_with_cache', 'cost']

_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', _NS)


def _xml_tag(tag):
    return f'{{{_NS}}}{tag}'


class _XLSXWriter:
    """纯 stdlib XLSX 写入器。"""

    def __init__(self):
        self.sheets = {}
        self.col_widths = {}
        self.merges = {}
        self.freezes = {}
        self._strings = []
        self._str_idx = {}

    def _add_str(self, s):
        s = str(s)
        if s not in self._str_idx:
            self._str_idx[s] = len(self._strings)
            self._strings.append(s)
        return self._str_idx[s]

    def add_sheet(self, name, col_widths=None, merges=None, freeze=None):
        name = name[:31]
        self.sheets[name] = []
        if col_widths:
            self.col_widths[name] = col_widths
        if merges:
            self.merges[name] = merges
        if freeze:
            self.freezes[name] = freeze

    def add_row(self, sheet, values):
        self.sheets[sheet].append(values)

    def _col_letter(self, n):
        s = ''
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s

    def _build_styles_xml(self):
        fonts_el = ET.Element(_xml_tag('fonts'), count='3')
        ET.SubElement(fonts_el, _xml_tag('font'))
        fb = ET.SubElement(fonts_el, _xml_tag('font'))
        ET.SubElement(fb, _xml_tag('b'))
        ET.SubElement(fb, _xml_tag('color'), rgb='FFFFFFFF')
        fb2 = ET.SubElement(fonts_el, _xml_tag('font'))
        ET.SubElement(fb2, _xml_tag('b'))
        fills_el = ET.Element(_xml_tag('fills'), count='5')
        ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(ET.SubElement(fills_el, _xml_tag('fill')), _xml_tag('patternFill'), patternType='gray125')
        fh = ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(fh, _xml_tag('patternFill'), patternType='solid').append(
            ET.Element(_xml_tag('fgColor'), rgb='FF4472C4'))
        ft = ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(ft, _xml_tag('patternFill'), patternType='solid').append(
            ET.Element(_xml_tag('fgColor'), rgb='FFD9E2F3'))
        fg = ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(fg, _xml_tag('patternFill'), patternType='solid').append(
            ET.Element(_xml_tag('fgColor'), rgb='FFF2F2F2'))
        borders_el = ET.Element(_xml_tag('borders'), count='1')
        ET.SubElement(borders_el, _xml_tag('border'))
        style_xml = ET.Element(_xml_tag('styleSheet'))
        style_xml.append(fonts_el)
        style_xml.append(fills_el)
        style_xml.append(borders_el)
        ET.SubElement(style_xml, _xml_tag('cellStyleXfs'), count='1').append(
            ET.Element(_xml_tag('xf'), numFmtId='0', fontId='0', fillId='0', borderId='0'))
        xfs = ET.SubElement(style_xml, _xml_tag('cellXfs'), count='5')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='0', fillId='0', borderId='0', xfId='0')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='1', fillId='2', borderId='0', xfId='0', applyFont='1', applyFill='1')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='2', fillId='3', borderId='0', xfId='0', applyFont='1', applyFill='1')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='2', fillId='0', borderId='0', xfId='0', applyFont='1')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='0', fillId='4', borderId='0', xfId='0', applyFill='1')
        return ET.tostring(style_xml, encoding='utf-8', xml_declaration=True)

    def _build_shared_strings_xml(self):
        sst = ET.Element(_xml_tag('sst'), count=str(len(self._strings)),
                         uniqueCount=str(len(self._strings)))
        for s in self._strings:
            si = ET.SubElement(sst, _xml_tag('si'))
            ET.SubElement(si, _xml_tag('t')).text = s
        return ET.tostring(sst, encoding='utf-8', xml_declaration=True)

    def _build_sheet_xml(self, name):
        ws = ET.Element(_xml_tag('worksheet'))
        rows = self.sheets[name]
        if name in self.col_widths:
            cols_el = ET.SubElement(ws, _xml_tag('cols'))
            for letter, width in sorted(self.col_widths[name].items()):
                col_num = 0
                for ch in letter:
                    col_num = col_num * 26 + (ord(ch.upper()) - 64)
                ET.SubElement(cols_el, _xml_tag('col'), min=str(col_num), max=str(col_num),
                              width=str(width), customWidth='1')
        sd = ET.SubElement(ws, _xml_tag('sheetData'))
        for row_idx, row_data in enumerate(rows, 1):
            row_el = ET.SubElement(sd, _xml_tag('row'), r=str(row_idx))
            for col_idx, item in enumerate(row_data, 1):
                val, style = item if isinstance(item, tuple) else (item, 0)
                ref = f'{self._col_letter(col_idx)}{row_idx}'
                if isinstance(val, str):
                    idx = self._add_str(val)
                    v_el = ET.Element(_xml_tag('v'))
                    v_el.text = str(idx)
                    ET.SubElement(row_el, _xml_tag('c'), r=ref, t='s', s=str(style)).append(v_el)
                elif isinstance(val, (int, float)):
                    v_el = ET.Element(_xml_tag('v'))
                    v_el.text = str(int(val))
                    ET.SubElement(row_el, _xml_tag('c'), r=ref, s=str(style)).append(v_el)
        if name in self.merges:
            mc_el = ET.SubElement(ws, _xml_tag('mergeCells'), count=str(len(self.merges[name])))
            for r1, c1, r2, c2 in self.merges[name]:
                ref = f'{self._col_letter(c1)}{r1}:{self._col_letter(c2)}{r2}'
                ET.SubElement(mc_el, _xml_tag('mergeCell'), ref=ref)
        if name in self.freezes:
            fp = self.freezes[name]
            sv = ET.SubElement(ws, _xml_tag('sheetViews'))
            sv_el = ET.SubElement(sv, _xml_tag('sheetView'), tabSelected='1', workbookViewId='0')
            pane_el = ET.SubElement(sv_el, _xml_tag('pane'))
            cl = ''.join(c for c in fp if c.isalpha())
            rn = int(''.join(c for c in fp if c.isdigit()))
            pane_el.set('ySplit', str(rn - 1))
            pane_el.set('topLeftCell', fp)
            pane_el.set('activePane', 'bottomRight')
            pane_el.set('state', 'frozen')
        return ET.tostring(ws, encoding='utf-8', xml_declaration=True)

    def save(self, filepath):
        # 安全检查：确保有数据可写
        for name, rows in self.sheets.items():
            if not rows:
                raise ValueError(f"Sheet \"{name}\" 没有数据行，请先调用 add_row()")
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            ct_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                      '<Default Extension="xml" ContentType="application/xml"/>'
                      '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>')
            for name in list(self.sheets.keys()):
                safe = name.replace(' ', '')
                ct_xml += f'<Override PartName="/xl/worksheets/{safe}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            ct_xml += ('<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                       '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
                       '</Types>')
            zf.writestr('[Content_Types].xml', ct_xml)
            zf.writestr('_rels/.rels',
                        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                        '</Relationships>')
            wb_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                      '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
                      ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>')
            for i, name in enumerate(self.sheets.keys(), 1):
                safe = name.replace(' ', '')
                wb_xml += f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>'
            wb_xml += '</sheets></workbook>'
            zf.writestr('xl/workbook.xml', wb_xml)
            rels_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">')
            for i, name in enumerate(self.sheets.keys(), 1):
                safe = name.replace(' ', '')
                rels_xml += f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/{safe}.xml"/>'
            rels_xml += ('<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                         '<Relationship Id="rIdStrings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
                         '</Relationships>')
            zf.writestr('xl/_rels/workbook.xml.rels', rels_xml)
            zf.writestr('xl/styles.xml', self._build_styles_xml())
            # 先构建所有 sheet XML（填充 shared strings）
            sheet_xmls = {}
            for name in self.sheets.keys():
                safe = name.replace(' ', '')
                sheet_xmls[safe] = self._build_sheet_xml(name)
            # 再写 shared strings（此时已填充完毕）
            zf.writestr('xl/sharedStrings.xml', self._build_shared_strings_xml())
            # 最后写 sheet XML
            for safe, sxml in sheet_xmls.items():
                zf.writestr(f'xl/worksheets/{safe}.xml', sxml)
        # 写入后检查文件大小
        try:
            fsize = os.path.getsize(filepath)
            if fsize < 200:
                print(f"⚠️ 警告: 导出文件异常小 ({fsize} bytes)，可能缺少数据")
        except Exception:
            pass


HDR_STYLE = 1  # 白字蓝底
TOT_STYLE = 2  # 加粗蓝底


def _write_xlsx_simple(filepath, agent_name, agent_display, filtered_models):
    """单 Agent 简单 XLSX（含 Agent 列 + 合并单元格 + 合计行）。"""
    wb = _XLSXWriter()
    col_widths = {'A': 18, 'B': 22}
    for i in range(3, 9):
        col_widths[wb._col_letter(i)] = 16
    merges = []
    wb.add_sheet(agent_display, col_widths=col_widths, merges=merges, freeze='C2')
    headers = ['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用']
    wb.add_row(agent_display, [(h, HDR_STYLE) for h in headers])
    row_num = 2
    ms = row_num
    for pm in filtered_models:
        inp = int(pm.get('input', 0))
        out = int(pm.get('output', 0))
        cache = int(pm.get('cache', 0))
        calls = int(pm.get('calls', 0))
        model = pm.get('model', 'unknown')
        cr = _calc_cache_rate(inp, cache)
        cr_str = f"{cr:.1f}%" if cr is not None else "-"
        pc = _get_model_price(model)
        if pc:
            cost_val = _calc_cost(inp, out, cache, pc)
            cost_str = f"≈¥{_to_cny(cost_val, pc.get('currency', 'CNY')):.4f}"
        else:
            cost_str = "-"
        wb.add_row(agent_display, [agent_display, model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cost_str])
        row_num += 1
    if filtered_models:
        merges.append((ms, 1, row_num - 1, 1))
    # 多模型时展示 Agent 合计（单模型则跳过，避免重复）
    if len(filtered_models) > 1:
        ti = int(sum(pm.get('input', 0) for pm in filtered_models))
        to = int(sum(pm.get('output', 0) for pm in filtered_models))
        tc = int(sum(pm.get('cache', 0) for pm in filtered_models))
        tca = int(sum(pm.get('calls', 0) for pm in filtered_models))
        tcr = _calc_cache_rate(ti, tc)
        tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
        tcost_str = _fmt_total_cost(_calc_total_cost(filtered_models))
        tcost_str = f"{tcost_str} (仅供参考)" if tcost_str else "-"
        wb.add_row(agent_display, [
            (f'{agent_display} 合计', TOT_STYLE), ('', TOT_STYLE), (ti, TOT_STYLE), (to, TOT_STYLE),
            (tc, TOT_STYLE), (tcr_str, TOT_STYLE), (tca, TOT_STYLE),
            (ti + to, TOT_STYLE), (ti + to + tc, TOT_STYLE), (tcost_str, TOT_STYLE)])
    wb.merges[agent_display] = merges
    wb.save(filepath)


def _write_xlsx_multi_simple(filepath, results):
    """多 Agent 简单 XLSX（Agent 列合并单元格 + 每个 Agent 单独合计 + 总合计）。"""
    wb = _XLSXWriter()
    col_widths = {'A': 18, 'B': 22}
    for i in range(3, 9):
        col_widths[wb._col_letter(i)] = 16
    merges = []
    wb.add_sheet('MultiAgent', col_widths=col_widths, merges=merges, freeze='C2')
    headers = ['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用']
    wb.add_row('MultiAgent', [(h, HDR_STYLE) for h in headers])
    row_num = 2
    grand_ti = grand_to = grand_tc = grand_tca = 0
    grand_cost = 0.0
    grand_cur = "CNY"
    total_agents = 0
    for agent, data in results:
        agent_models = [pm for pm in (data.per_model or []) if not _skip_model(pm)]
        if not agent_models:
            continue
        total_agents += 1
        ms = row_num
        ti = to = tc = tca = 0
        at_cost = 0.0
        at_cur = "CNY"
        for pm in agent_models:
            inp = int(pm.get('input', 0))
            out = int(pm.get('output', 0))
            cache = int(pm.get('cache', 0))
            calls = int(pm.get('calls', 0))
            model = pm.get('model', 'unknown')
            cr = _calc_cache_rate(inp, cache)
            cr_str = f"{cr:.1f}%" if cr is not None else "-"
            pc = _get_model_price(model)
            if pc:
                cv = _calc_cost(inp, out, cache, pc)
                cs = f"≈¥{_to_cny(cv, pc.get('currency', 'CNY')):.4f}"
                at_cost += cv; at_cur = pc.get("currency","CNY")
            else:
                cs = "-"
            wb.add_row('MultiAgent', [agent.display_name(), model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cs])
            ti += inp; to += out; tc += cache; tca += calls
            row_num += 1
        merges.append((ms, 1, row_num - 1, 1))
        # 多模型时展示 Agent 合计
        if len(agent_models) > 1:
            tcr = _calc_cache_rate(ti, tc)
            tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
            at_sy = "¥" if at_cur=="CNY" else "$"
            at_cs = f"≈{at_sy}{at_cost:.4f} (仅供参考)" if at_cost > 0 else "-"
            wb.add_row('MultiAgent', [
                (f'{agent.display_name()} 合计', TOT_STYLE), ('', TOT_STYLE), (ti, TOT_STYLE),
                (to, TOT_STYLE), (tc, TOT_STYLE), (tcr_str, TOT_STYLE), (tca, TOT_STYLE),
                (ti + to, TOT_STYLE), (ti + to + tc, TOT_STYLE), (at_cs, TOT_STYLE)])
            row_num += 1
        grand_ti += ti; grand_to += to; grand_tc += tc; grand_tca += tca
        grand_cost += at_cost
        if at_cost > 0: grand_cur = at_cur
    # 全部总计
    if total_agents > 1:
        gtt = grand_ti + grand_to
        gtcr = _calc_cache_rate(grand_ti, grand_tc)
        gtcr_str = f"{gtcr:.1f}%" if gtcr is not None else "-"
        gsy = "¥" if grand_cur=="CNY" else "$"
        gcs = f"≈{gsy}{grand_cost:.4f} (仅供参考)" if grand_cost > 0 else "-"
        wb.add_row('MultiAgent', [
            ('全部总计', TOT_STYLE), ('', TOT_STYLE), (grand_ti, TOT_STYLE),
            (grand_to, TOT_STYLE), (grand_tc, TOT_STYLE), (gtcr_str, TOT_STYLE), (grand_tca, TOT_STYLE),
            (gtt, TOT_STYLE), (gtt + grand_tc, TOT_STYLE), (gcs, TOT_STYLE)])
    wb.merges['MultiAgent'] = merges
    wb.save(filepath)


def _write_xlsx_monthly(filepath, agent_name, agent_display, monthly_data, all_months):
    """单 Agent 年度 XLSX，按月拆分列，含 Agent 列合并 + 合计。"""
    wb = _XLSXWriter()
    month_count = len(all_months)
    all_models = sorted({m for d in monthly_data.values() for m in d})
    # A=Agent, B=Model, C=Metric, then months, then 合计
    col_widths = {'A': 18, 'B': 22, 'C': 14}
    for i in range(month_count):
        col_widths[wb._col_letter(4 + i)] = 16
    col_widths[wb._col_letter(4 + month_count)] = 16
    merges = []
    wb.add_sheet(agent_display, col_widths=col_widths, merges=merges, freeze='D2')
    headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
    wb.add_row(agent_display, [(h, HDR_STYLE) for h in headers])
    row_num = 2
    ag_ms = row_num  # agent merge start
    for model in all_models:
        ms = row_num
        for metric in _METRIC_ORDER:
            vals = [
                ('' if (model == all_models[0] and metric == 'input') else '', 0),
                ('' if metric != 'input' else model, 0),
                (_METRIC_LABELS[metric], 0)]
            tot = 0
            for m_label in all_months:
                md = monthly_data[m_label].get(model, {})
                if metric == 'total':
                    v = md.get('input', 0) + md.get('output', 0)
                elif metric == 'total_with_cache':
                    v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                else:
                    v = md.get(metric, 0)
                tot += v
                vals.append((int(v), 0))
            vals.append((int(tot), 0))
            wb.add_row(agent_display, vals)
            row_num += 1
        merges.append((ms, 2, row_num - 1, 2))  # Model merge
    if all_models:
        merges.append((ag_ms, 1, row_num - 1, 1))  # Agent merge
    # 多模型时展示合计（单模型跳过避免重复）
    if len(all_models) > 1:
        gt = row_num
        for metric in _METRIC_ORDER:
            vals = [
                ('' if metric != 'input' else f'{agent_display} 合计', TOT_STYLE),
                ('' if metric != 'input' else '合计', TOT_STYLE),
                (_METRIC_LABELS[metric], TOT_STYLE)]
            gt_all = 0
            for m_label in all_months:
                ct = 0
                for model in all_models:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        ct += md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        ct += md.get(metric, 0)
                gt_all += ct
                vals.append((int(ct), TOT_STYLE))
            vals.append((int(gt_all), TOT_STYLE))
            wb.add_row(agent_display, vals)
            row_num += 1
        merges.append((gt, 1, row_num - 1, 1))
    wb.merges[agent_display] = merges
    wb.save(filepath)


def _write_xlsx_multi_monthly(filepath, agents_monthly, all_months, agent_order):
    """多 Agent 年度 XLSX，全部 Agent 在一个 Sheet，含每个 Agent 单独合计 + 总合计。"""
    wb = _XLSXWriter()
    month_count = len(all_months)
    col_widths = {'A': 18, 'B': 22, 'C': 14}
    for i in range(month_count):
        col_widths[wb._col_letter(4 + i)] = 16
    col_widths[wb._col_letter(4 + month_count)] = 16
    merges = []
    sheet_name = 'YearlyStats'
    wb.add_sheet(sheet_name, col_widths=col_widths, merges=merges, freeze='D2')
    headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
    # 手动管理行列表，避免插入时行号计算错误
    rows_data = []  # [(row_values, row_type), ...]
    for agent_name, agent_display, monthly_data in agent_order:
        all_models = sorted({m for d in monthly_data.values() for m in d})
        if not all_models:
            continue
        for model in all_models:
            for metric in _METRIC_ORDER:
                vals = [
                    ('' if metric != 'input' else agent_display, 0),
                    ('' if metric != 'input' else model, 0),
                    (_METRIC_LABELS[metric], 0)]
                tot = 0
                for m_label in all_months:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        v = md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        v = md.get(metric, 0)
                    tot += v
                    vals.append((int(v), 0))
                vals.append((int(tot), 0))
                rows_data.append((vals, 'data', agent_name, agent_display, model))
        # 多模型时展示 Agent 合计
        if len(all_models) > 1:
            for metric in _METRIC_ORDER:
                vals = [
                    ('' if metric != 'input' else f'{agent_display} 合计', TOT_STYLE),
                    ('' if metric != 'input' else '合计', TOT_STYLE),
                    (_METRIC_LABELS[metric], TOT_STYLE)]
                ag_total = 0
                for m_label in all_months:
                    ct = 0
                    for model in all_models:
                        md = monthly_data[m_label].get(model, {})
                        if metric == 'total':
                            ct += md.get('input', 0) + md.get('output', 0)
                        elif metric == 'total_with_cache':
                            ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                        else:
                            ct += md.get(metric, 0)
                    ag_total += ct
                    vals.append((int(ct), TOT_STYLE))
                vals.append((int(ag_total), TOT_STYLE))
                rows_data.append((vals, 'agent_subtotal', agent_name, agent_display, None))

    # 写入 header
    wb.add_row(sheet_name, [(h, HDR_STYLE) for h in headers])
    row_num = 2
    # 追踪 merge ranges：数据行 Agent+Model、合计行 Agent+Model
    agent_ranges = {}  # agent_name -> (start_row, end_row) — 仅数据行
    model_ranges = {}  # (agent_name, model) -> (start_row, end_row)
    subtotal_agent_ranges = {}  # agent_name -> (start_row, end_row) — 合计行 Agent 列
    subtotal_model_ranges = {}  # agent_name -> (start_row, end_row) — 合计行 Model 列
    current_agent = None
    current_model = None
    agent_start = None
    model_start = None

    subtotal_start = None
    subtotal_agent = None

    def _close_data_ranges():
        nonlocal current_agent, current_model, agent_start, model_start
        if current_agent is not None:
            agent_ranges[current_agent] = (agent_start, row_num - 1)
        if current_model is not None and current_agent is not None:
            model_ranges[(current_agent, current_model)] = (model_start, row_num - 1)

    def _close_subtotal_ranges():
        nonlocal subtotal_agent, subtotal_start
        if subtotal_agent is not None and subtotal_start is not None:
            subtotal_agent_ranges[subtotal_agent] = (subtotal_start, row_num - 1)
            subtotal_model_ranges[subtotal_agent] = (subtotal_start, row_num - 1)
            subtotal_agent = None
            subtotal_start = None

    for vals, rtype, ag_name, ag_display, model in rows_data:
        wb.add_row(sheet_name, vals)
        if rtype == 'data':
            _close_subtotal_ranges()
            if ag_name != current_agent:
                _close_data_ranges()
                current_agent = ag_name
                agent_start = row_num
                current_model = None
                model_start = None
            if model != current_model or current_model is None:
                if current_model is not None and current_agent == ag_name:
                    model_ranges[(current_agent, current_model)] = (model_start, row_num - 1)
                current_model = model
                model_start = row_num
        elif rtype == 'agent_subtotal':
            _close_data_ranges()
            current_agent = None
            current_model = None
            if subtotal_start is None:
                subtotal_start = row_num
                subtotal_agent = ag_name
        row_num += 1

    _close_subtotal_ranges()

    # 构建 merges
    for ag_name, (sr, er) in agent_ranges.items():
        merges.append((sr, 1, er, 1))
    for (ag_name, model), (sr, er) in model_ranges.items():
        merges.append((sr, 2, er, 2))
    for ag_name, (sr, er) in subtotal_agent_ranges.items():
        merges.append((sr, 1, er, 1))
    for ag_name, (sr, er) in subtotal_model_ranges.items():
        merges.append((sr, 2, er, 2))

    # 全部总计
    gt = row_num
    for metric in _METRIC_ORDER:
        vals = [('', TOT_STYLE) if metric != 'input' else ('全部总计', TOT_STYLE), ('', TOT_STYLE),
                (_METRIC_LABELS[metric], TOT_STYLE)]
        gt_all = 0
        for m_label in all_months:
            ct = 0
            for ag_name, ag_display, monthly_data in agent_order:
                for model in sorted({m for d in monthly_data.values() for m in d}):
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        ct += md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        ct += md.get(metric, 0)
            gt_all += ct
            vals.append((int(ct), TOT_STYLE))
        vals.append((int(gt_all), TOT_STYLE))
        wb.add_row(sheet_name, vals)
        row_num += 1
    merges.append((gt, 1, row_num - 1, 1))
    merges.append((gt, 2, row_num - 1, 2))
    wb.merges[sheet_name] = merges
    wb.save(filepath)


# ═══════════════════════════════════════════════════
#  CSV 导出
# ═══════════════════════════════════════════════════

def _write_csv_simple(filepath, agent_name, agent_display, filtered_models):
    """单 Agent 简单 CSV。"""
    import csv
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用'])
        ti = to = tc = tca = 0
        at_cost = 0.0; at_cur = "CNY"
        for pm in filtered_models:
            inp = int(pm.get('input', 0))
            out = int(pm.get('output', 0))
            cache = int(pm.get('cache', 0))
            calls = int(pm.get('calls', 0))
            model = pm.get('model', 'unknown')
            cr = _calc_cache_rate(inp, cache)
            cr_str = f"{cr:.1f}%" if cr is not None else "-"
            pc = _get_model_price(model)
            if pc:
                cv = _calc_cost(inp, out, cache, pc)
                cs = f"≈¥{_to_cny(cv, pc.get('currency', 'CNY')):.4f}"
                at_cost += cv; at_cur = pc.get("currency","CNY")
            else:
                cs = "-"
            w.writerow([agent_display, model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cs])
            ti += inp; to += out; tc += cache; tca += calls
        if len(filtered_models) > 1:
            tcr = _calc_cache_rate(ti, tc)
            tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
            at_sy = "¥" if at_cur=="CNY" else "$"
            at_cs = f"≈{at_sy}{at_cost:.4f} (仅供参考)" if at_cost > 0 else "-"
            w.writerow([f'{agent_display} 合计', '', ti, to, tc, tcr_str, tca, ti + to, ti + to + tc, at_cs])


def _write_csv_multi_simple(filepath, results):
    """多 Agent 简单 CSV，含每个 Agent 单独合计 + 总合计。"""
    import csv
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用'])
        grand_ti = grand_to = grand_tc = grand_tca = 0
        grand_cost = 0.0; grand_cur = "CNY"
        total_agents = 0
        for agent, data in results:
            agent_models = [pm for pm in (data.per_model or []) if not _skip_model(pm)]
            if not agent_models:
                continue
            total_agents += 1
            ti = to = tc = tca = 0
            at_cost = 0.0; at_cur = "CNY"
            for pm in agent_models:
                inp = int(pm.get('input', 0))
                out = int(pm.get('output', 0))
                cache = int(pm.get('cache', 0))
                calls = int(pm.get('calls', 0))
                model = pm.get('model', 'unknown')
                cr = _calc_cache_rate(inp, cache)
                cr_str = f"{cr:.1f}%" if cr is not None else "-"
                pc = _get_model_price(model)
                if pc:
                    cv = _calc_cost(inp, out, cache, pc)
                    cs = f"≈¥{_to_cny(cv, pc.get('currency', 'CNY')):.4f}"
                    at_cost += cv; at_cur = pc.get("currency","CNY")
                else:
                    cs = "-"
                w.writerow([agent.display_name(), model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cs])
                ti += inp; to += out; tc += cache; tca += calls
            if len(agent_models) > 1:
                tcr = _calc_cache_rate(ti, tc)
                tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
                at_sy = "¥" if at_cur=="CNY" else "$"
                at_cs = f"≈{at_sy}{at_cost:.4f} (仅供参考)" if at_cost > 0 else "-"
                w.writerow([f'{agent.display_name()} 合计', '', ti, to, tc, tcr_str, tca, ti + to, ti + to + tc, at_cs])
            grand_ti += ti; grand_to += to; grand_tc += tc; grand_tca += tca
            grand_cost += at_cost
            if at_cost > 0: grand_cur = at_cur
        if total_agents > 1:
            gtt = grand_ti + grand_to
            gtcr = _calc_cache_rate(grand_ti, grand_tc)
            gtcr_str = f"{gtcr:.1f}%" if gtcr is not None else "-"
            gsy = "¥" if grand_cur=="CNY" else "$"
            gcs = f"≈{gsy}{grand_cost:.4f} (仅供参考)" if grand_cost > 0 else "-"
            w.writerow(['全部总计', '', grand_ti, grand_to, grand_tc, gtcr_str, grand_tca, gtt, gtt + grand_tc, gcs])


def _write_csv_monthly(filepath, agent_name, agent_display, monthly_data, all_months):
    """单 Agent 年度 CSV，按月拆分列。"""
    import csv
    all_models = sorted({m for d in monthly_data.values() for m in d})
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
        w.writerow(headers)
        for model in all_models:
            for metric in _METRIC_ORDER:
                row = [agent_display if metric == 'input' else '', model if metric == 'input' else '', _METRIC_LABELS[metric]]
                tot = 0
                for m_label in all_months:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        v = md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        v = md.get(metric, 0)
                    tot += v
                    row.append(int(v))
                row.append(int(tot))
                w.writerow(row)
        # 多模型时展示合计
        if len(all_models) > 1:
            for metric in _METRIC_ORDER:
                row = [f'{agent_display} 合计' if metric == 'input' else '',
                       '合计' if metric == 'input' else '',
                       _METRIC_LABELS[metric]]
            gt_all = 0
            for m_label in all_months:
                ct = 0
                for model in all_models:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        ct += md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        ct += md.get(metric, 0)
                gt_all += ct
                row.append(int(ct))
            row.append(int(gt_all))
            w.writerow(row)


def _write_csv_multi_monthly(filepath, agent_order, all_months):
    """多 Agent 年度 CSV，含每个 Agent 单独合计 + 总合计。"""
    import csv
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
        w.writerow(headers)
        for agent_name, agent_display, monthly_data in agent_order:
            all_models = sorted({m for d in monthly_data.values() for m in d})
            if not all_models:
                continue
            for model in all_models:
                for metric in _METRIC_ORDER:
                    row = [agent_display if metric == 'input' else '', model if metric == 'input' else '', _METRIC_LABELS[metric]]
                    tot = 0
                    for m_label in all_months:
                        md = monthly_data[m_label].get(model, {})
                        if metric == 'total':
                            v = md.get('input', 0) + md.get('output', 0)
                        elif metric == 'total_with_cache':
                            v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                        else:
                            v = md.get(metric, 0)
                        tot += v
                        row.append(int(v))
                    row.append(int(tot))
                    w.writerow(row)
            # 多模型时展示 Agent 合计
            if len(all_models) > 1:
                for metric in _METRIC_ORDER:
                    row = [f'{agent_display} 合计' if metric == 'input' else '',
                           '合计' if metric == 'input' else '',
                           _METRIC_LABELS[metric]]
                    ag_total = 0
                    for m_label in all_months:
                        ct = 0
                        for model in all_models:
                            md = monthly_data[m_label].get(model, {})
                            if metric == 'total':
                                ct += md.get('input', 0) + md.get('output', 0)
                            elif metric == 'total_with_cache':
                                ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                            else:
                                ct += md.get(metric, 0)
                        ag_total += ct
                        row.append(int(ct))
                    row.append(int(ag_total))
                    w.writerow(row)
        # 全部总计
        if len(agent_order) > 1:
            for metric in _METRIC_ORDER:
                row = ['全部总计' if metric == 'input' else '', '', _METRIC_LABELS[metric]]
                gt_all = 0
                for m_label in all_months:
                    ct = 0
                    for ag_name, ag_display, monthly_data in agent_order:
                        for model in sorted({m for d in monthly_data.values() for m in d}):
                            md = monthly_data[m_label].get(model, {})
                            if metric == 'total':
                                ct += md.get('input', 0) + md.get('output', 0)
                            elif metric == 'total_with_cache':
                                ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                            else:
                                ct += md.get(metric, 0)
                    gt_all += ct
                    row.append(int(ct))
                row.append(int(gt_all))
                w.writerow(row)


def export_interactive(data: AgentData, agent: BaseAgent,
                       from_ts: float = None, to_ts: float = None,
                       is_year: bool = False, export_dir: str = None):
    """交互式导出统计。is_year=True 时按月拆分，导出 XLSX/CSV/JSON。"""
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # ── 年度导出：预先收集月度数据（仅一次，避免重复收集）──
        monthly_data = None
        month_labels = None
        if is_year and from_ts is not None and to_ts is not None:
            months = _split_months(from_ts, to_ts)
            month_labels = [label for label, _, _ in months]
            monthly_data = {}
            total_months = len(months)
            for idx, (label, m_start, m_end) in enumerate(months, 1):
                print(f"  ⏳ 正在收集 {label} 数据 ({idx}/{total_months})...", end="\r", flush=True)
                m_data = agent.collect(from_ts=m_start, to_ts=m_end)
                monthly_data[label] = {
                    pm.get("model", "unknown"): {
                        "input": pm.get("input", 0), "output": pm.get("output", 0),
                        "cache": pm.get("cache", 0), "calls": pm.get("calls", 0),
                    }
                    for pm in (m_data.per_model or []) if not _skip_model(pm)
                }
            print(" " * 40, end="\r")
            # 从月度数据汇总 filtered_models
            all_models = sorted({m for d in monthly_data.values() for m in d})
            agg = {}
            for model in all_models:
                agg[model] = {"input": 0, "output": 0, "cache": 0, "calls": 0}
                for label in month_labels:
                    md = monthly_data[label].get(model, {})
                    agg[model]["input"] += md.get("input", 0)
                    agg[model]["output"] += md.get("output", 0)
                    agg[model]["cache"] += md.get("cache", 0)
                    agg[model]["calls"] += md.get("calls", 0)
            filtered_models = [{"model": m, **v} for m, v in agg.items()]
        else:
            filtered_models = [pm for pm in (data.per_model or []) if not _skip_model(pm)]

        # ── 显示格式化汇总 ──
        print()
        print(f"📊 {data.display_name if data else agent.display_name()} — 导出 ({date_str})")
        print("═" * 52)
        for pm in filtered_models:
            m = pm.get("model", "unknown")
            inp = pm.get("input", 0)
            out = pm.get("output", 0)
            cache = pm.get("cache", 0)
            calls = pm.get("calls", 0)
            total_tok = inp + out
            total_w_cache = total_tok + cache
            print(f"  {m}")
            if agent._has_live_context:
                cw = detect_context(m)
                pct = round(total_tok / cw * 100, 1) if cw else 0
                print(f"    上下文          {fmt_num(total_tok):>8} / {fmt_num(cw):<8} ({pct}%)")
            print(f"    输入 tokens     {fmt_num(inp):>8}")
            print(f"    输出 tokens     {fmt_num(out):>8}")
            print(f"    缓存 tokens     {fmt_num(cache):>8}")
            print(f"    调用次数        {calls} 次")
            print(f"    ─────────────────────────────────────")
            print(f"    总计/+缓存     {fmt_num(total_tok)}/{fmt_num(total_w_cache)}")

        # ── 合计（多模型时显示） ──
        if filtered_models and len(filtered_models) > 1:
            ti = sum(pm.get("input", 0) for pm in filtered_models)
            to = sum(pm.get("output", 0) for pm in filtered_models)
            tc = sum(pm.get("cache", 0) for pm in filtered_models)
            tca = sum(pm.get("calls", 0) for pm in filtered_models)
            tt = ti + to
            print(f"  {'─' * 42}")
            print(f"  合计")
            print(f"    输入 tokens     {fmt_num(ti):>8}")
            print(f"    输出 tokens     {fmt_num(to):>8}")
            print(f"    缓存 tokens     {fmt_num(tc):>8}")
            print(f"    调用次数        {tca} 次")
            print(f"    ─────────────────────────────────────")
            print(f"    总计/+缓存     {fmt_num(tt)}/{fmt_num(tt + tc)}")
        print()

        # Step 1: 输入目录（如果已提供路径则跳过交互）
        if export_dir:
            dir_path = os.path.expanduser(export_dir)
            if not os.path.isdir(dir_path):
                print(f"⚠️ 目录不存在: {dir_path}，使用当前目录")
                dir_path = os.getcwd()
        else:
            dir_path = os.getcwd()
            try:
                while True:
                    dir_input = input("\n请输入导出目录路径 (回车=当前目录, q=取消): ").strip()
                    if not dir_input:
                        break
                    if dir_input.lower() == "q":
                        print("已取消导出")
                        return
                    p = os.path.expanduser(dir_input)
                    if os.path.isdir(p):
                        dir_path = p
                        break
                    print(f"⚠️ 目录不存在: {p}, 请重试")
            except EOFError:
                pass

        # Step 2: 选择格式
        print("\n选择导出格式:")
        print("  [1] XLSX（默认）")
        print("  [2] CSV")
        print("  [3] JSON")
        fmt = "xlsx"
        try:
            fmt_choice = input("请选择 (1/2/3, 回车=1): ").strip().lower()
            if fmt_choice in ("2", "csv"):
                fmt = "csv"
            elif fmt_choice in ("3", "json"):
                fmt = "json"
        except EOFError:
            pass

        # Step 3: 写文件
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        if is_year:
            prefix = f"agent-usage-stats_{agent.name()}_yearly"
        else:
            prefix = f"agent-usage-stats_{agent.name()}"
        filename = f"{prefix}_{timestamp}.{fmt}"
        filepath = os.path.join(dir_path, filename)

        if fmt == "json":
            export_data = {
                "tool": "agent-usage-stats",
                "version": VERSION,
                "agent": agent.name(),
                "agent_display": agent.display_name(),
                "export_date": date_str,
                "exported_at": now.isoformat(),
                "per_model": [{
                    "model": pm.get("model", "unknown"),
                    "input_tokens": pm.get("input", 0),
                    "output_tokens": pm.get("output", 0),
                    "cache_tokens": pm.get("cache", 0),
                    "cache_ratio": round(_calc_cache_rate(pm.get("input",0), pm.get("cache",0)), 1) if _calc_cache_rate(pm.get("input",0), pm.get("cache",0)) is not None else None,
                    "calls": pm.get("calls", 0),
                    "total_tokens": pm.get("input", 0) + pm.get("output", 0),
                    "total_with_cache": pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0),
                } for pm in filtered_models],
                "summary": (
                    {
                        "total_input_tokens": sum(pm.get("input", 0) for pm in filtered_models),
                        "total_output_tokens": sum(pm.get("output", 0) for pm in filtered_models),
                        "total_cache_tokens": sum(pm.get("cache", 0) for pm in filtered_models),
                        "total_calls": sum(pm.get("calls", 0) for pm in filtered_models),
                        "total_tokens": sum(pm.get("input", 0) + pm.get("output", 0) for pm in filtered_models),
                        "total_with_cache": sum(pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0) for pm in filtered_models),
                    }
                    if filtered_models and len(filtered_models) > 1
                    else None
                ),
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        elif fmt == "csv":
            if is_year and monthly_data is not None:
                _write_csv_monthly(filepath, agent.name(), agent.display_name(),
                                   monthly_data, month_labels)
            else:
                _write_csv_simple(filepath, agent.name(), agent.display_name(),
                                  filtered_models)
        else:
            if is_year and monthly_data is not None:
                _write_xlsx_monthly(filepath, agent.name(), agent.display_name(),
                                    monthly_data, month_labels)
            else:
                _write_xlsx_simple(filepath, agent.name(), agent.display_name(),
                                   filtered_models)

        print(f"✅ 已导出到: {filepath}")
    except KeyboardInterrupt:
        print()
        print("已取消导出")


def export_multi(results: list[tuple[BaseAgent, AgentData]],
                  is_year: bool = False, from_ts: float = None, to_ts: float = None,
                  export_dir: str = None):
    """导出多个 Agent 的统计（合并输出）。is_year=True 时按月拆分。"""
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # ── 年度导出：预先收集月度数据（仅一次，避免重复收集）──
        agent_order = None
        month_labels = None
        if is_year and from_ts is not None and to_ts is not None:
            months = _split_months(from_ts, to_ts)
            month_labels = [label for label, _, _ in months]
            agent_order = []
            total_agents = len(results)
            agent_idx = 0
            for agent, data in results:
                agent_idx += 1
                agent_models = [pm for pm in (data.per_model or []) if not _skip_model(pm)]
                if not agent_models:
                    continue
                monthly_data = {}
                total_months = len(months)
                for idx, (label, m_start, m_end) in enumerate(months, 1):
                    print(f"  ⏳ 正在收集 {agent.display_name()} {label} 数据 ({idx}/{total_months}) [{agent_idx}/{total_agents}]...", end="\r", flush=True)
                    m_data = agent.collect(from_ts=m_start, to_ts=m_end)
                    monthly_data[label] = {
                        pm.get("model", "unknown"): {
                            "input": pm.get("input", 0), "output": pm.get("output", 0),
                            "cache": pm.get("cache", 0), "calls": pm.get("calls", 0),
                        }
                        for pm in (m_data.per_model or []) if not _skip_model(pm)
                    }
                print(" " * 60, end="\r")
                agent_order.append((agent.name(), agent.display_name(), monthly_data))
            print(" " * 60, end="\r")

        # ── 显示格式化汇总 ──
        print()
        print(f"📊 多 Agent 导出 ({date_str})")
        print("═" * 52)
        grand_ti = grand_to = grand_tc = grand_tca = 0
        for agent, data in results:
            print(f"\n  🤖 {agent.display_name()}")
            agent_models = [pm for pm in (data.per_model or []) if not _skip_model(pm)]
            for pm in agent_models:
                m = pm.get("model", "unknown")
                inp = pm.get("input", 0)
                out = pm.get("output", 0)
                cache = pm.get("cache", 0)
                calls = pm.get("calls", 0)
                total_tok = inp + out
                total_w_cache = total_tok + cache
                print(f"    {m}")
                if agent._has_live_context:
                    cw = detect_context(m)
                    pct = round(total_tok / cw * 100, 1) if cw else 0
                    print(f"      上下文          {fmt_num(total_tok):>8} / {fmt_num(cw):<8} ({pct}%)")
                print(f"      输入 tokens     {fmt_num(inp):>8}")
                print(f"      输出 tokens     {fmt_num(out):>8}")
                print(f"      缓存 tokens     {fmt_num(cache):>8}")
                print(f"      调用次数        {calls} 次")
                print(f"      ─────────────────────────────────────")
                print(f"      总计/+缓存     {fmt_num(total_tok)}/{fmt_num(total_w_cache)}")

            # Agent 内合计
            if agent_models and len(agent_models) > 1:
                ti = sum(pm.get("input", 0) for pm in agent_models)
                to = sum(pm.get("output", 0) for pm in agent_models)
                tc = sum(pm.get("cache", 0) for pm in agent_models)
                tca = sum(pm.get("calls", 0) for pm in agent_models)
                tt = ti + to
                print(f"    {'─' * 42}")
                print(f"    合计")
                print(f"      输入 tokens     {fmt_num(ti):>8}")
                print(f"      输出 tokens     {fmt_num(to):>8}")
                print(f"      缓存 tokens     {fmt_num(tc):>8}")
                print(f"      调用次数        {tca} 次")
                print(f"      ─────────────────────────────────────")
                print(f"      总计/+缓存     {fmt_num(tt)}/{fmt_num(tt + tc)}")
                grand_ti += ti; grand_to += to; grand_tc += tc; grand_tca += tca
            else:
                pm = agent_models[0] if agent_models else {}
                grand_ti += pm.get("input", 0)
                grand_to += pm.get("output", 0)
                grand_tc += pm.get("cache", 0)
                grand_tca += pm.get("calls", 0)

        # 所有 Agent 总计
        if len(results) > 1:
            gtt = grand_ti + grand_to
            print(f"\n  {'═' * 42}")
            print(f"  全部 Agent 总计")
            print(f"    输入 tokens     {fmt_num(grand_ti):>8}")
            print(f"    输出 tokens     {fmt_num(grand_to):>8}")
            print(f"    缓存 tokens     {fmt_num(grand_tc):>8}")
            print(f"    调用次数        {grand_tca} 次")
            print(f"    ─────────────────────────────────────")
            print(f"    总计/+缓存     {fmt_num(gtt)}/{fmt_num(gtt + grand_tc)}")

        # Step 1: 输入目录
        if export_dir:
            dir_path = os.path.expanduser(export_dir)
            if not os.path.isdir(dir_path):
                print(f"⚠️ 目录不存在: {dir_path}，使用当前目录")
                dir_path = os.getcwd()
        else:
            dir_path = os.getcwd()
            try:
                while True:
                    dir_input = input("\n请输入导出目录路径 (回车=当前目录, q=取消): ").strip()
                    if not dir_input:
                        break
                    if dir_input.lower() == "q":
                        print("已取消导出")
                        return
                    p = os.path.expanduser(dir_input)
                    if os.path.isdir(p):
                        dir_path = p
                        break
                    print(f"⚠️ 目录不存在: {p}, 请重试")
            except EOFError:
                pass

        # Step 2: 选择格式
        fmt = "xlsx"
        try:
            print("\n选择导出格式:")
            print("  [1] XLSX（默认）")
            print("  [2] CSV")
            print("  [3] JSON")
            fmt_choice = input("请选择 (1/2/3, 回车=1): ").strip().lower()
            if fmt_choice in ("2", "csv"):
                fmt = "csv"
            elif fmt_choice in ("3", "json"):
                fmt = "json"
        except EOFError:
            pass

        # Step 3: 写文件
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        agent_names = "+".join(agent.name() for agent, _ in results)
        if is_year:
            filename = f"agent-usage-stats_{agent_names}_yearly_{timestamp}.{fmt}"
        else:
            filename = f"agent-usage-stats_{agent_names}_{timestamp}.{fmt}"
        filepath = os.path.join(dir_path, filename)

        if fmt == "json":
            agents_json = []
            for agent, data in results:
                agent_models = [pm for pm in (data.per_model or []) if not _skip_model(pm)]
                per_model = [{
                    "model": pm.get("model", "unknown"),
                    "input_tokens": pm.get("input", 0),
                    "output_tokens": pm.get("output", 0),
                    "cache_tokens": pm.get("cache", 0),
                    "cache_ratio": round(_calc_cache_rate(pm.get("input",0), pm.get("cache",0)), 1) if _calc_cache_rate(pm.get("input",0), pm.get("cache",0)) is not None else None,
                    "calls": pm.get("calls", 0),
                    "total_tokens": pm.get("input", 0) + pm.get("output", 0),
                    "total_with_cache": pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0),
                } for pm in agent_models]
                entry = {
                    "agent": agent.name(),
                    "agent_display": agent.display_name(),
                    "per_model": per_model,
                }
                if agent_models and len(agent_models) > 1:
                    entry["summary"] = {
                        "total_input_tokens": sum(pm.get("input", 0) for pm in agent_models),
                        "total_output_tokens": sum(pm.get("output", 0) for pm in agent_models),
                        "total_cache_tokens": sum(pm.get("cache", 0) for pm in agent_models),
                        "total_calls": sum(pm.get("calls", 0) for pm in agent_models),
                        "total_tokens": sum(pm.get("input", 0) + pm.get("output", 0) for pm in agent_models),
                        "total_with_cache": sum(pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0) for pm in agent_models),
                    }
                agents_json.append(entry)

            export_data = {
                "tool": "agent-usage-stats",
                "version": VERSION,
                "export_date": date_str,
                "exported_at": now.isoformat(),
                "agents": agents_json,
            }
            if len(results) > 1:
                export_data["grand_total"] = {
                    "total_input_tokens": grand_ti,
                    "total_output_tokens": grand_to,
                    "total_cache_tokens": grand_tc,
                    "total_calls": grand_tca,
                    "total_tokens": grand_ti + grand_to,
                    "total_with_cache": grand_ti + grand_to + grand_tc,
                }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"  {filepath}")
            print(f"多 Agent 数据已合并导出")
        elif fmt == "csv":
            if is_year and agent_order is not None:
                _write_csv_multi_monthly(filepath, agent_order, month_labels)
                print(f"  {filepath}")
                print(f"多 Agent 数据已合并导出")
            else:
                _write_csv_multi_simple(filepath, results)
        else:
            if is_year and agent_order is not None:
                _write_xlsx_multi_monthly(filepath, agent_order, month_labels, agent_order)
                print(f"  {filepath}")
                print(f"多 Agent 数据已合并导出")
            else:
                _write_xlsx_multi_simple(filepath, results)
                print(f"  {filepath}")
                print(f"多 Agent 数据已合并导出")
    except KeyboardInterrupt:
        print()
        print("已取消导出")


# ═══════════════════════════════════════════════════
#  对比
# ═══════════════════════════════════════════════════

def run_compare(agent: BaseAgent, a_label: str, b_label: str):
    """对比两个时间段的统计 — 按模型 × 指标完整对比"""
    a_start, a_end = parse_time_label(a_label)
    b_start, b_end = parse_time_label(b_label)

    print("  ⏳ 正在收集对比数据...", end="\r", flush=True)
    data_a = agent.collect(from_ts=a_start, to_ts=a_end)
    data_b = agent.collect(from_ts=b_start, to_ts=b_end)
    print(" " * 30, end="\r")

    models_a = {pm["model"]: pm for pm in (data_a.per_model or []) if not _skip_model(pm)}
    models_b = {pm["model"]: pm for pm in (data_b.per_model or []) if not _skip_model(pm)}
    all_models = sorted(set(list(models_a.keys()) + list(models_b.keys())))

    if not all_models:
        print("两个时间段均无数据")
        return

    a_disp = label_to_display(a_label)
    b_disp = label_to_display(b_label)
    print(f"\n📊 对比: {a_disp} vs {b_disp}  [{agent.display_name()}]")

    # 构建对齐行列表：每个 (模型, 指标) 一行
    rows = []
    def _delta(va, vb):
        d = vb - va
        return f"+{fmt_num(d)}" if d > 0 else fmt_num(d) if d < 0 else "0"

    grand_ai = grand_ao = grand_ac = grand_acall = grand_bi = grand_bo = grand_bc = grand_bcall = 0
    for mn in all_models:
        ma = models_a.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
        mb = models_b.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
        ai = ma.get("input", 0) or 0
        ao = ma.get("output", 0) or 0
        ac = ma.get("cache", 0) or 0
        a_calls = ma.get("calls", 0) or 0
        a_total = ai + ao
        a_total_cache = a_total + ac
        bi = mb.get("input", 0) or 0
        bo = mb.get("output", 0) or 0
        bc = mb.get("cache", 0) or 0
        b_calls = mb.get("calls", 0) or 0
        b_total = bi + bo
        b_total_cache = b_total + bc
        if a_total == 0 and b_total == 0:
            continue
        grand_ai += ai; grand_ao += ao; grand_ac += ac; grand_acall += a_calls
        grand_bi += bi; grand_bo += bo; grand_bc += bc; grand_bcall += b_calls

        # 费用（仅在有价格时展示）
        pc = _get_model_price(mn)
        a_cost_str = f"≈¥{_to_cny(_calc_cost(ai, ao, ac, pc), pc.get('currency','CNY')):.2f}" if pc and (ai or ao or ac) else "-"
        b_cost_str = f"≈¥{_to_cny(_calc_cost(bi, bo, bc, pc), pc.get('currency','CNY')):.2f}" if pc and (bi or bo or bc) else "-"
        metrics = [
            ("入", ai, bi),
            ("出", ao, bo),
            ("缓", ac, bc),
            ("缓存率", f"{_calc_cache_rate(ai, ac):.1f}%" if _calc_cache_rate(ai, ac) is not None else "-",
                      f"{_calc_cache_rate(bi, bc):.1f}%" if _calc_cache_rate(bi, bc) is not None else "-"),
            ("总计", a_total, b_total),
            ("总计(含缓存)", a_total_cache, b_total_cache),
            ("调用", a_calls, b_calls),
            ("费用", a_cost_str, b_cost_str),
        ]
        for i, (metric_name, va, vb) in enumerate(metrics):
            if metric_name == "缓存率":
                d_val = ""
            elif metric_name == "费用":
                # 费用差：都有效时计算差值
                if isinstance(va, str) and va.startswith("≈¥") and isinstance(vb, str) and vb.startswith("≈¥"):
                    try:
                        fa = float(va[2:])
                        fb = float(vb[2:])
                        d = fb - fa
                        d_val = f"+¥{d:.2f}" if d > 0 else f"-¥{abs(d):.2f}" if d < 0 else "0"
                    except ValueError:
                        d_val = ""
                else:
                    d_val = ""
            else:
                d_val = _delta(va, vb)
            cols = ["" if i != 0 else mn, metric_name,
                    str(va), str(vb), d_val]
            rows.append(cols)

    # Agent 合计
    # 每个模型有 8 个指标行（入/出/缓/缓存率/总计/总计含缓存/调用/费用）
    metrics_per_model = 8
    model_count = len(rows) // metrics_per_model if rows else 0
    if model_count > 1:
        grand_a_total = grand_ai + grand_ao
        grand_b_total = grand_bi + grand_bo
        grand_a_total_cache = grand_a_total + grand_ac
        grand_b_total_cache = grand_b_total + grand_bc
        # 合计费用
        gt_a_cost = sum(_to_cny(_calc_cost(
            models_a.get(mn, {}).get("input",0) or 0,
            models_a.get(mn, {}).get("output",0) or 0,
            models_a.get(mn, {}).get("cache",0) or 0, pc),
            pc.get("currency","CNY"))
            for mn in all_models if (pc := _get_model_price(mn)))
        gt_b_cost = sum(_to_cny(_calc_cost(
            models_b.get(mn, {}).get("input",0) or 0,
            models_b.get(mn, {}).get("output",0) or 0,
            models_b.get(mn, {}).get("cache",0) or 0, pc),
            pc.get("currency","CNY"))
            for mn in all_models if (pc := _get_model_price(mn)))
        gt_a_cost_str = f"≈¥{gt_a_cost:.2f}" if gt_a_cost > 0 else "-"
        gt_b_cost_str = f"≈¥{gt_b_cost:.2f}" if gt_b_cost > 0 else "-"
        metrics = [
            ("入", grand_ai, grand_bi),
            ("出", grand_ao, grand_bo),
            ("缓", grand_ac, grand_bc),
            ("缓存率", f"{_calc_cache_rate(grand_ai, grand_ac):.1f}%" if _calc_cache_rate(grand_ai, grand_ac) is not None else "-",
                      f"{_calc_cache_rate(grand_bi, grand_bc):.1f}%" if _calc_cache_rate(grand_bi, grand_bc) is not None else "-"),
            ("总计", grand_a_total, grand_b_total),
            ("总计(含缓存)", grand_a_total_cache, grand_b_total_cache),
            ("调用", grand_acall, grand_bcall),
            ("费用", gt_a_cost_str, gt_b_cost_str),
        ]
        for i, (metric_name, va, vb) in enumerate(metrics):
            if metric_name == "缓存率":
                d_val = ""
            elif metric_name == "费用":
                if isinstance(va, str) and va.startswith("≈¥") and isinstance(vb, str) and vb.startswith("≈¥"):
                    try:
                        fa = float(va[2:])
                        fb = float(vb[2:])
                        d = fb - fa
                        d_val = f"+¥{d:.2f}" if d > 0 else f"-¥{abs(d):.2f}" if d < 0 else "0"
                    except ValueError:
                        d_val = ""
                else:
                    d_val = ""
            else:
                d_val = _delta(va, vb)
            cols = ["" if i != 0 else "合计", metric_name,
                    str(va), str(vb), d_val]
            rows.append(cols)

    if not rows:
        print("  (两侧均无有效数据)")
        print()
        return

    aligned = _align_rows(rows)
    # 将表头与数据一起对齐，确保列宽一致
    headers = ["模型", "指标", f"{a_disp}", f"{b_disp}", "变化"]
    aligned = _align_rows([headers] + rows)
    header_row = aligned[0]
    data_rows = aligned[1:]
    sep_w = sum(_display_width(_strip_ansi(c)) for c in header_row) + 3 * (len(header_row) - 1) + 4
    # 追踪模型边界，用于分隔线
    model_boundaries = set()
    cur_model = None
    for i, row in enumerate(rows):
        mn = row[0]
        if mn and mn != cur_model:
            if cur_model is not None:
                model_boundaries.add(i)
            cur_model = mn
    print("=" * sep_w)
    print(f"  {' | '.join(header_row)}")
    print("─" * sep_w)
    for i, row in enumerate(data_rows):
        if i in model_boundaries:
            print("  " + "·" * (sep_w - 2))
        print(f"  {' | '.join(row)}")
    print("─" * sep_w)
    print()


# ═══════════════════════════════════════════════════
#  全部统计 (--all)
# ═══════════════════════════════════════════════════

def show_all(*, from_ts: float = None, to_ts: float = None):
    """显示本机所有 Agent 的统计"""
    installed = detect_installed()
    if not installed:
        print("❌ 本机未检测到任何支持的 AI 助手")
        return

    print("\n📊 本机 Agent 统计汇总")
    print("═" * 50)

    any_data = False
    grand_ti = grand_to = grand_tc = grand_tca = 0
    grand_costs: dict[str, float] = {}
    agent_count = 0
    for cls in ALL_AGENTS:
        detected = cls.detect()
        status = "✅" if detected else "❌"
        name = cls.display_name()
        print(f"\n{status} {name}")

        if detected:
            try:
                agent = cls()
                print(f"  ⏳ 正在收集 {cls.display_name()} 数据...", end="\r", flush=True)
                data = agent.collect(from_ts=from_ts, to_ts=to_ts)
                print(" " * 40, end="\r")
                if data.stats:
                    any_data = True
                    for pm in (data.per_model or []):
                        if _skip_model(pm):
                            continue
                        inp = pm.get("input", 0) or 0
                        out = pm.get("output", 0) or 0
                        cache = pm.get("cache", 0) or 0
                        calls = pm.get("calls", 0) or 0
                        grand_ti += inp
                        grand_to += out
                        grand_tc += cache
                        grand_tca += calls
                        pc = _get_model_price(pm.get("model", ""))
                        if pc:
                            cur = pc.get("currency", "CNY")
                            grand_costs[cur] = grand_costs.get(cur, 0.0) + _calc_cost(inp, out, cache, pc)
                    agent_count += 1
                print(data.raw)
            except Exception as e:
                msg = str(e)
                if "locked" in msg.lower():
                    msg = "数据库被锁定（Agent 正在运行，请先关闭 Agent）"
                print(f"  ⚠️ 读取失败: {msg}")
        else:
            print("  (未安装)")

    # Grand Total
    if agent_count > 1:
        gtt = grand_ti + grand_to
        print(f"\n{'═' * 50}")
        print("  全部 Agent 总计")
        parts = f"  入 {fmt_num(grand_ti)} | 出 {fmt_num(grand_to)} | {_fmt_cache_val(grand_tc, grand_ti)} | 总计/+缓存 {fmt_num(gtt)}/{fmt_num(gtt + grand_tc)} | 调用 {grand_tca} 次"
        total_cost_str = _fmt_total_cost(grand_costs)
        if total_cost_str:
            parts += f" | {total_cost_str} (仅供参考)"
        print(parts)

    if not any_data:
        print("\n（所有 Agent 均无数据）")
    print()


# ═══════════════════════════════════════════════════
#  PATH 管理（--setup / --uninstall 共用）
# ═══════════════════════════════════════════════════

PATH_MARKER_START = "# >>> agent-usage-stats PATH >>>"
PATH_MARKER_END = "# <<< agent-usage-stats PATH <<<"


def _detect_rc_file():
    """根据 $SHELL 检测当前用户的 shell 配置文件。"""
    shell = os.environ.get("SHELL", "")
    shell_name = os.path.basename(shell)
    if shell_name == "zsh":
        return "~/.zshrc"
    elif shell_name == "bash":
        return "~/.bashrc"
    elif shell_name == "fish":
        return "~/.config/fish/config.fish"
    else:
        # Fallback: 按优先级尝试存在的 rc 文件
        for rc in ["~/.zshrc", "~/.bashrc", "~/.bash_profile", "~/.profile"]:
            if os.path.exists(os.path.expanduser(rc)):
                return rc
        return "~/.bashrc"


def _add_to_path_windows(bin_dir):
    """将目录添加到用户 PATH（注册表），广播变更消息。返回 True/False。"""
    import ctypes
    import winreg
    bin_dir = os.path.normpath(bin_dir)  # 标准化为 Windows 反斜杠路径
    key = None
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            current, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            current = ""
        entries = [os.path.normpath(e) for e in current.split(";") if e]
        if bin_dir.lower() in (e.lower() for e in entries):  # Windows 大小写不敏感
            return False
        entries.append(bin_dir)
        new_path = ";".join(entries)
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 2, 5000, None)
        return True
    except Exception:
        return False
    finally:
        if key is not None:
            winreg.CloseKey(key)


def _remove_from_path_windows(bin_dir):
    """从用户 PATH 中移除目录（注册表），广播变更消息。"""
    import ctypes
    import winreg
    bin_dir = os.path.normpath(bin_dir)  # 标准化为 Windows 反斜杠路径
    key = None
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        current, _ = winreg.QueryValueEx(key, "PATH")
        entries = [e for e in current.split(";") if e and os.path.normpath(e).lower() != bin_dir.lower()]
        new_path = ";".join(entries)
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 2, 5000, None)
        return True
    except Exception:
        return False
    finally:
        if key is not None:
            winreg.CloseKey(key)


def _add_to_path_unix(bin_dir, rc_file):
    """将 PATH 行（带标记）追加到 shell 配置文件。若已存在则跳过。"""
    rc_path = os.path.expanduser(rc_file)
    is_fish = rc_file.endswith(".fish") or "fish" in rc_file
    if is_fish:
        export_line = f"fish_add_path {bin_dir}"
    else:
        export_line = f'export PATH="$PATH:{bin_dir}"'
    block = f"\n{PATH_MARKER_START}\n{export_line}\n{PATH_MARKER_END}\n"
    try:
        if os.path.exists(rc_path):
            with open(rc_path, "r", encoding="utf-8") as f:
                if PATH_MARKER_START in f.read():
                    return False  # 已存在，跳过
        with open(rc_path, "a", encoding="utf-8") as f:
            f.write(block)
        return True
    except Exception:
        return False


def _remove_from_path_unix(bin_dir, rc_file):
    """从 shell 配置文件中移除当前和旧命令名的 PATH 标记块。"""
    rc_path = os.path.expanduser(rc_file)
    if not os.path.exists(rc_path):
        return False
    is_fish = rc_file.endswith(".fish") or "fish" in rc_file
    if is_fish:
        export_line = f"fish_add_path {bin_dir}"
    else:
        export_line = f'export PATH="$PATH:{bin_dir}"'
    try:
        with open(rc_path, "r", encoding="utf-8") as f:
            content = f.read()
        marker_pairs = [(PATH_MARKER_START, PATH_MARKER_END)]
        marker_pairs.extend(
            (f"# >>> {name} PATH >>>", f"# <<< {name} PATH <<<")
            for name in LEGACY_COMMAND_NAMES
        )
        for marker_start, marker_end in marker_pairs:
            for prefix in ("\n", ""):
                pattern = f"{prefix}{marker_start}\n{export_line}\n{marker_end}\n"
                if pattern in content:
                    content = content.replace(pattern, "")
        with open(rc_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════
#  CLI 入口
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="agent-usage-stats — 选个 Agent 看它的 token 消耗",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
命令大全:
  基础:
    agent-usage-stats                       交互式菜单选择 Agent → 查看统计
    agent-usage-stats -a <name>             直接指定 Agent: hermes/claude-code/codex/openclaw
    agent-usage-stats -v / --version        显示版本号
    agent-usage-stats -a <name> --detail    详细模式（同默认）
    agent-usage-stats -a <name> --now       当前快照（同默认）

  快速时间段:
    agent-usage-stats -a <name> -t / --today     今日统计
    agent-usage-stats -a <name> --yesterday 昨日统计
    agent-usage-stats -a <name> --week      本周统计（周一起）
    agent-usage-stats -a <name> --last-7d   最近 7 天
    agent-usage-stats -a <name> -m / --month 本月统计
    agent-usage-stats -a <name> -y / --year 本年统计
    agent-usage-stats -a <name> --from 2025-01-01 --to 2025-01-31  自定义时间段

  对比:
    agent-usage-stats -a <name> --compare --a today --b yesterday
        快捷标签对比
    agent-usage-stats -a <name> --compare --a 2025-01-01~2025-01-07 --b 2025-01-08~2025-01-14
        自定义时间段对比
    标签支持: today / yesterday / this-week / last-week / this-month / last-month / this-year / last-year / YYYY-MM-DD / YYYY-MM-DD~YYYY-MM-DD

  导出:
    agent-usage-stats -a <name> -e / --export    导出当前统计（交互式选目录和格式）
    agent-usage-stats -a <name> -t -e            导出今日统计

  实时监控:
    agent-usage-stats -a <name> -w / --watch     实时监控，默认 5 秒刷新 (Ctrl+C 停止)
    agent-usage-stats -a <name> -w 10            自定义间隔秒数
    停止后自动展示监控时间段内的完整统计数据（模型、输入、输出、缓存、调用次数）

  多 Agent:
    agent-usage-stats --all                 查看本机所有 Agent 统计
    agent-usage-stats --list-backends       列出已安装的 Agent

  安装与卸载:
    clawhub install ai-agent-usage-stats  从 ClawHub 安装
    agent-usage-stats --setup                创建全局命令 + 自动加入 PATH
    agent-usage-stats --uninstall            删除全局命令 + 自动清理 PATH
    agent-usage-stats update                 通过 clawhub update 更新到最新版本
        """,
    )
    parser.add_argument("-v", "--version", action="store_true", help="显示版本号")
    parser.add_argument("-l", "--list-backends", action="store_true", help="列出本机已安装的 Agent")
    parser.add_argument("--list-prices", action="store_true", help="列出 model_prices.toml 中已配置价格的模型")
    parser.add_argument("-a", "--agent", help="直接指定 Agent: claude-code/codex/hermes/openclaw/reasonix/deepseek-tui")
    parser.add_argument("-w", "--watch", nargs="?", type=int, const=5, default=None, metavar="秒",
                        help="实时监控模式（默认每 5 秒轮询）")
    parser.add_argument("setup_pos", nargs="?", const=True, help=argparse.SUPPRESS)

    # 时间段
    parser.add_argument("-t", "--today", action="store_true", help="今日统计")
    parser.add_argument("--yesterday", action="store_true", help="昨日统计")
    parser.add_argument("--week", action="store_true", help="本周统计")
    parser.add_argument("--last-7d", action="store_true", help="最近 7 天统计")
    parser.add_argument("-m", "--month", action="store_true", help="本月统计")
    parser.add_argument("-y", "--year", action="store_true", help="本年统计")
    parser.add_argument("--from", dest="from_date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="结束日期 (YYYY-MM-DD)")

    # 功能
    parser.add_argument("-e", "--export", nargs="?", const=True, default=None, metavar="目录",
                        help="导出统计（交互式选择目录和格式）")
    parser.add_argument("--compare", action="store_true", help="对比模式")
    parser.add_argument("--a", help="对比时间段 A（today/yesterday/this-week/last-week/日期/日期段）")
    parser.add_argument("--b", help="对比时间段 B")
    parser.add_argument("--detail", action="store_true", help="详细信息模式")
    parser.add_argument("--now", action="store_true", help="当前快照（同默认）")
    parser.add_argument("--all", action="store_true", help="查看本机所有 Agent 统计")
    parser.add_argument("--setup", action="store_true", help="创建 ~/.local/bin/agent-usage-stats 并自动加入 PATH")
    parser.add_argument("--uninstall", action="store_true", help="删除全局命令并清理 PATH")
    parser.add_argument("--update", action="store_true", help="通过 clawhub update 更新到最新版本")

    args = parser.parse_args()

    # 兼容旧用法：agent-usage-stats setup / uninstall / update → 当作对应 flag
    if args.setup_pos is True or args.setup_pos == "setup":
        args.setup = True
    if args.setup_pos == "uninstall":
        args.uninstall = True
    if args.setup_pos == "update":
        args.update = True

    # ── version ──
    if args.version:
        print(f"agent-usage-stats v{VERSION}")
        return

    # ── setup ──
    if args.setup:
        is_win = sys.platform == "win32"
        is_mac = sys.platform == "darwin"
        bin_dir = os.path.join(os.path.expanduser("~"), ".local", "bin")
        script_path = os.path.abspath(__file__)
        os.makedirs(bin_dir, exist_ok=True)

        # 1. 创建包装器
        if is_win:
            target = os.path.join(bin_dir, f"{COMMAND_NAME}.cmd")
            wrapper = f'@python "{script_path}" %*\n'
            with open(target, "w", encoding="utf-8") as f:
                f.write(wrapper)
        else:
            target = os.path.join(bin_dir, COMMAND_NAME)
            wrapper = (
                "#!/bin/sh\n"
                f'exec python3 "{script_path}" "$@"\n'
            )
            with open(target, "w", encoding="utf-8") as f:
                f.write(wrapper)
            os.chmod(target, 0o755)

        print(f"✅ 已创建全局命令: {target}")

        # 清理旧命令包装器，避免旧名字继续可用。
        for old_name in LEGACY_COMMAND_NAMES:
            old_target = os.path.join(bin_dir, f"{old_name}.cmd" if is_win else old_name)
            if old_target != target and os.path.exists(old_target):
                os.remove(old_target)
                print(f"✅ 已移除旧命令: {old_target}")

        # 2. 自动添加 PATH
        print("⏳ 正在添加到系统 PATH...", end="", flush=True)
        path_ok = bin_dir in os.environ.get("PATH", "").split(os.pathsep)
        if not path_ok:
            if is_win:
                _add_to_path_windows(bin_dir)
            else:
                rc = _detect_rc_file()
                _add_to_path_unix(bin_dir, rc)
        print("\r✅ 已添加到系统 PATH                    ")

        # 3. 检查旧 alias（仅 Unix）
        if not is_win:
            rc = _detect_rc_file()
            rc_files = list(dict.fromkeys([rc, "~/.zshrc", "~/.bashrc", "~/.bash_profile"]))
            for rc_file in rc_files:
                rc_path = os.path.expanduser(rc_file)
                if os.path.exists(rc_path):
                    with open(rc_path, encoding="utf-8") as f:
                        content = f.read()
                    alias_lines = []
                    for i, line in enumerate(content.splitlines(), 1):
                        stripped = line.strip()
                        if any(f"alias {name}" in stripped for name in (COMMAND_NAME, *LEGACY_COMMAND_NAMES)):
                            alias_lines.append(f"  {rc_file} 第 {i} 行: {line.strip()}")
                    if alias_lines:
                        print()
                        print("⚠️  检测到旧的 alias，会覆盖全局命令，建议删除：")
                        for al in alias_lines:
                            print(al)
                        print("   删除方法: 手动编辑或用 sed 删除对应行，然后 source ~/.zshrc")

        # 4. 扫描并保存 Agent 数据路径
        agent_paths = _scan_all_agent_paths()
        if agent_paths:
            _save_agent_paths(agent_paths)
            detected = []
            for key in agent_paths:
                label = key.replace("_dir", "").replace("_db", "").replace("_sessions", "")
                detected.append(label.capitalize())
            print(f"✅ 已自动检测并保存 Agent 路径: {', '.join(sorted(set(detected)))}")
        else:
            print("ℹ️  未检测到任何 Agent 数据文件，运行后会自动尝试标准路径")

        print()
        print("现在可以在新终端窗口中直接运行: agent-usage-stats --version")
        return

    # ── uninstall ──
    if args.uninstall:
        is_win = sys.platform == "win32"
        is_mac = sys.platform == "darwin"
        bin_dir = os.path.join(os.path.expanduser("~"), ".local", "bin")

        # 1. 删除包装器
        removed_any = False
        for name in (COMMAND_NAME, *LEGACY_COMMAND_NAMES):
            target = os.path.join(bin_dir, f"{name}.cmd" if is_win else name)
            if os.path.exists(target):
                os.remove(target)
                removed_any = True
                print(f"✅ 已删除: {target}")
        if not removed_any:
            print(f"ℹ️  全局命令不存在: {os.path.join(bin_dir, COMMAND_NAME)}")

        # 2. 清理 PATH
        print("⏳ 正在清理系统 PATH...", end="", flush=True)
        if is_win:
            _remove_from_path_windows(bin_dir)
        else:
            rc = _detect_rc_file()
            _remove_from_path_unix(bin_dir, rc)
        print("\r✅ 已清理系统 PATH                    ")

        # 3. 清理配置文件
        config_dirs = [CONFIG_DIR, *LEGACY_CONFIG_DIRS]
        for config_dir in config_dirs:
            if not os.path.exists(config_dir):
                continue
            import shutil
            shutil.rmtree(config_dir, ignore_errors=True)
            print(f"✅ 已清理配置文件: {config_dir}")

        print()
        print("卸载完成。如需彻底删除技能文件，请执行: clawhub uninstall ai-agent-usage-stats")
        return

    # ── update ──
    if getattr(args, 'update', False):
        print("⏳ 正在通过 ClawHub 更新 agent-usage-stats...")
        import subprocess, shutil
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        clawhub_exe = shutil.which("clawhub") or shutil.which("clawhub.cmd") or "clawhub"

        def _copy_updated_files(src_dir, dst_dir):
            """从 src_dir 复制更新后的文件到 dst_dir。"""
            if not os.path.isdir(src_dir):
                return False
            if os.path.normpath(src_dir) == os.path.normpath(dst_dir):
                return True  # 同目录，无需复制
            copied = False
            for fname in os.listdir(src_dir):
                src = os.path.join(src_dir, fname)
                dst = os.path.join(dst_dir, fname)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    copied = True
            return copied

        def _refresh_wrapper():
            """刷新 ~/.local/bin 下的 wrapper 脚本。"""
            bin_dir = os.path.join(os.path.expanduser("~"), ".local", "bin")
            unix_target = os.path.join(bin_dir, COMMAND_NAME)
            win_target = os.path.join(bin_dir, f"{COMMAND_NAME}.cmd")
            legacy_targets = [
                os.path.join(bin_dir, name)
                for name in LEGACY_COMMAND_NAMES
            ] + [
                os.path.join(bin_dir, f"{name}.cmd")
                for name in LEGACY_COMMAND_NAMES
            ]
            target = unix_target if os.path.exists(unix_target) else win_target if os.path.exists(win_target) else None
            if target is None and any(os.path.exists(p) for p in legacy_targets):
                target = win_target if sys.platform == "win32" else unix_target
            if target is None:
                return
            with open(target, "w", encoding="utf-8") as f:
                script_path = os.path.abspath(__file__)
                if target.endswith(".cmd"):
                    f.write(f'@python "{script_path}" %*\n')
                else:
                    f.write("#!/bin/sh\n"
                            f'exec python3 "{script_path}" "$@"\n')
                    os.chmod(target, 0o755)
            for old_target in legacy_targets:
                if old_target != target and os.path.exists(old_target):
                    os.remove(old_target)

        def _read_version(path):
            """从 agent-usage-stats.py 读取 VERSION 字符串。"""
            try:
                fpath = os.path.join(path, "agent-usage-stats.py")
                if not os.path.isfile(fpath):
                    return None
                with open(fpath, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith('VERSION = "'):
                            return line.split('"')[1]
            except Exception:
                pass
            return None

        try:
            old_ver = VERSION
            result = subprocess.run(
                [clawhub_exe, "update", "agent-usage-stats", "--no-input"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=120,
            )
            output = result.stdout.decode("utf-8", errors="ignore").strip()
            if output:
                print(output)

            if result.returncode != 0:
                print(f"⚠️ 更新可能失败 (exit {result.returncode})，请手动执行: clawhub update ai-agent-usage-stats")
                return

            # 搜索 ClawHub 安装的新文件（不同平台/版本路径可能不同）
            script_dir = os.path.dirname(os.path.abspath(__file__))
            search_dirs = [
                os.path.join(script_dir, "skills", "agent-usage-stats"),
                os.path.join(os.path.expanduser("~"), "skills", "agent-usage-stats"),
                os.path.join(os.path.expanduser("~"), ".clawhub", "skills", "ai-agent-usage-stats"),
            ]
            updated_src = None
            for d in search_dirs:
                ver = _read_version(d)
                if ver and ver != old_ver:
                    updated_src = d
                    break

            # 如果 update 没生效（ClawHub 在某些环境不写文件），改用 install --force
            if updated_src is None:
                print("  ⏳ 常规更新未生效，尝试强制重装...")
                result2 = subprocess.run(
                    [clawhub_exe, "install", "agent-usage-stats", "--force"],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    timeout=120,
                )
                out2 = result2.stdout.decode("utf-8", errors="ignore").strip()
                if out2:
                    print(out2)
                for d in search_dirs:
                    ver = _read_version(d)
                    if ver and ver != old_ver:
                        updated_src = d
                        break

            # 复制到脚本目录
            if updated_src:
                _copy_updated_files(updated_src, skill_dir)
                new_ver = _read_version(skill_dir)
                if new_ver and new_ver != old_ver:
                    _refresh_wrapper()
                    print(f"✅ 已更新到 v{new_ver}，请运行 agent-usage-stats --version 确认")
                else:
                    print(f"⚠️ 文件复制后版本仍为 v{old_ver}，请手动执行: cd ~ && clawhub install ai-agent-usage-stats --force")
            else:
                # 找不到更新文件，但 clawhub 返回成功，可能同目录已更新
                new_ver = _read_version(skill_dir)
                if new_ver and new_ver != old_ver:
                    _refresh_wrapper()
                    print(f"✅ 已更新到 v{new_ver}，请运行 agent-usage-stats --version 确认")
                else:
                    print(f"⚠️ 版本未变化 (仍为 v{old_ver})，请手动执行: clawhub install ai-agent-usage-stats --force")
        except FileNotFoundError:
            print("❌ 未找到 clawhub CLI，请先安装: npm install -g clawhub")
            print("   然后手动执行: clawhub update ai-agent-usage-stats")
        except subprocess.TimeoutExpired:
            print("⚠️ 更新超时，请检查网络后手动执行: clawhub update ai-agent-usage-stats")
        except Exception as e:
            print(f"⚠️ 更新失败: {e}")
            print("   请手动执行: clawhub update ai-agent-usage-stats")
        return

    # ── list-backends ──
    if args.list_backends:
        print("\n本机已安装的 AI 助手：")
        for cls in ALL_AGENTS:
            ok = "✅" if cls.detect() else "❌"
            print(f"  {ok} {cls.display_name()}")
        print()
        return

    # ── list-prices ──
    if args.list_prices:
        prices = _load_model_prices()
        if not prices:
            print("\n未找到 model_prices.toml 或无有效配置\n")
            return
        # 按 provider 分组
        groups: dict[str, list[tuple[str, dict]]] = {}
        for model, cfg in prices.items():
            if not isinstance(cfg, dict):
                continue
            provider = cfg.get("provider", "Other")
            groups.setdefault(provider, []).append((model, cfg))
        print(f"\n模型价格配置 (model_prices.toml) — {len(prices)} 个模型\n")
        for provider in sorted(groups.keys()):
            print(f"── {provider} ──")
            for model, cfg in groups[provider]:
                cur = cfg.get("currency", "CNY")
                sym = "¥" if cur == "CNY" else "$"
                no_cache = cfg.get("input_no_cache_price", "-")
                cache_p = cfg.get("input_cache_price", "-")
                out_p = cfg.get("output_price", "-")
                note = cfg.get("note", "")
                parts = [
                    f"  {model}",
                    f"输入 {sym}{no_cache}" if no_cache != "-" and no_cache != 0 else None,
                    f"缓存命中 {sym}{cache_p}" if cache_p != "-" and cache_p != 0 else None,
                    f"输出 {sym}{out_p}",
                ]
                line = " | ".join(p for p in parts if p)
                if note:
                    line += f"  ({note})"
                print(line)
            print()
        print("  价格单位: 每百万 (1M) tokens | USD 模型展示按 $，实际计算按 ¥7.25 换算")
        print()
        return

    # ── 解析时间段参数 ──
    from_ts = None
    to_ts = None

    if args.from_date:
        if args.to_date:
            from_ts, _ = parse_date(args.from_date)
            _, to_ts = parse_date(args.to_date)
        else:
            from_ts, _ = parse_date(args.from_date)
            to_ts = from_ts + 86399  # end of that day
    elif args.to_date and not args.from_date:
        _, to_ts = parse_date(args.to_date)
        # no from_ts means "from beginning"

    if args.today:
        from_ts, to_ts = parse_time_label("today")
    elif args.yesterday:
        from_ts, to_ts = parse_time_label("yesterday")
    elif args.week:
        from_ts, to_ts = parse_time_label("this-week")
    elif args.last_7d:
        from_ts, to_ts = parse_time_label("last-7d")
    elif args.month:
        from_ts, to_ts = parse_time_label("this-month")
    elif args.year:
        from_ts, to_ts = parse_time_label("this-year")

    # 导出目录：-e /path 时直接使用，否则 None（函数内会交互式询问）
    export_dir = args.export if isinstance(args.export, str) else None

    # ── Helper: collect agent data ──
    def _collect_agent_data(agents_list):
        results = []
        for agent in agents_list:
            try:
                print(f"  ⏳ 正在收集 {agent.display_name()} 数据...", end="\r", flush=True)
                data = agent.collect(from_ts=from_ts, to_ts=to_ts)
                print(" " * 40, end="\r")
                results.append((agent, data))
            except Exception as e:
                print(f"❌ {agent.display_name()}: {e}")
        return results

    # ── --all (所有 Agent) ──
    if args.all:
        if args.watch is not None:
            print("⚠️ --watch 仅支持单个 Agent，请使用 -a <name> --watch")
            return
        if args.compare:
            print("⚠️ --compare 仅支持单个 Agent")
            return
        installed = detect_installed()
        if not installed:
            print("❌ 本机未检测到任何支持的 AI 助手")
            return
        agents = [cls() for cls in ALL_AGENTS if cls.detect()]
        if args.export:
            results = _collect_agent_data(agents)
            if results:
                export_multi(results, is_year=args.year, from_ts=from_ts, to_ts=to_ts,
                             export_dir=export_dir)
        else:
            show_all(from_ts=from_ts, to_ts=to_ts)
        return

    # ── 选择 Agent(s) ──
    installed = detect_installed()
    if not installed:
        print("❌ 本机未检测到任何支持的 AI 助手")
        print("   支持的 Agent: Hermes, Claude Code, CodeX, OpenClaw")
        print("   请先使用并运行一个 Agent 后再来查看统计。")
        return

    if args.agent:
        backends = [b.strip() for b in args.agent.split(',')]
        agents = []
        for name in backends:
            try:
                agents.append(get_agent(name))
            except ValueError as e:
                print(f"❌ {e}")
                print(f"   可选: {', '.join(cls.name() for cls in ALL_AGENTS)}")
                return
        if len(agents) > 1:
            if args.watch is not None:
                print("⚠️ --watch 仅支持单个 Agent")
                return
            if args.compare:
                print("⚠️ --compare 仅支持单个 Agent")
                return
            results = _collect_agent_data(agents)
            if args.export:
                export_multi(results, is_year=args.year, from_ts=from_ts, to_ts=to_ts,
                             export_dir=export_dir)
            else:
                for agent, data in results:
                    print(f"\n{'─'*50}")
                    print(f"  {agent.display_name()}")
                    print(f"{'─'*50}")
                    print(data.raw)
                if len(results) > 1:
                    gti = gto = gtc = gtca = 0
                    gt_costs: dict[str, float] = {}
                    for _, d in results:
                        for pm in (d.per_model or []):
                            if _skip_model(pm):
                                continue
                            inp = pm.get("input", 0) or 0
                            out = pm.get("output", 0) or 0
                            cache = pm.get("cache", 0) or 0
                            gti += inp
                            gto += out
                            gtc += cache
                            gtca += pm.get("calls", 0) or 0
                            pc = _get_model_price(pm.get("model", ""))
                            if pc:
                                cur = pc.get("currency", "CNY")
                                gt_costs[cur] = gt_costs.get(cur, 0.0) + _calc_cost(inp, out, cache, pc)
                    gtt = gti + gto
                    print(f"\n{'═'*50}")
                    print("  全部 Agent 总计")
                    parts = f"  入 {fmt_num(gti)} | 出 {fmt_num(gto)} | {_fmt_cache_val(gtc, gti)} | 总计/+缓存 {fmt_num(gtt)}/{fmt_num(gtt + gtc)} | 调用 {gtca} 次"
                    gt_cost_str = _fmt_total_cost(gt_costs)
                    if gt_cost_str:
                        parts += f" | {gt_cost_str} (仅供参考)"
                    print(parts)
            return
        agent = agents[0]
    elif len(installed) == 1:
        agent = installed[0]()
        print(f"\n（本机仅安装了 {agent.display_name()}，直接显示统计）")
    else:
        agent = show_menu(installed, allow_all=args.watch is None)
        if agent == "all":
            show_all(from_ts=from_ts, to_ts=to_ts)
            return
        if agent is None:
            print("再见 👋")
            return

    # ── --compare (对比) ──
    if args.compare:
        a_label = args.a
        b_label = args.b
        if not a_label or not b_label:
            print("❌ --compare 需要 --a 和 --b 参数")
            print("   示例: agent-usage-stats -a hermes --compare --a today --b yesterday")
            return
        run_compare(agent, a_label, b_label)
        return

    # ── --watch (实时监控) ──
    if args.watch is not None:
        agent.watch(args.watch)
        return

    # ── 收集并展示 ──
    # 年度导出时跳过初始全量收集，由 export_interactive 统一收集月度数据
    if args.export and args.year:
        data = None
    else:
        try:
            print("  ⏳ 正在收集数据...", end="\r", flush=True)
            data = agent.collect(from_ts=from_ts, to_ts=to_ts)
            print(" " * 30, end="\r")  # clear progress line
            print()
            print(data.raw)
            print()
        except Exception as e:
            print(f"❌ 获取 {agent.display_name()} 统计失败: {e}")
            return

    # ── --export (导出) ──
    if args.export:
        export_interactive(data, agent, from_ts=from_ts, to_ts=to_ts,
                            is_year=args.year, export_dir=export_dir)

    # --detail 在下一步也可能有用，但当前 collect() 已含 per_model 详情
    # detail 主要用于 watch/collect 输出内容更丰富，当前 collect 实现已包含
    # 后续可通过 stats 或 per_model 扩展


if __name__ == "__main__":
    main()
