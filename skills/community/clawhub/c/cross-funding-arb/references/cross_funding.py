#!/usr/bin/env python3
"""Cross-exchange funding rate arbitrage (HL + Binance).

Monolithic single-file strategy for distribution as a skill.
Merges: config, state, emit, circuit_breaker, hl_client, bn_client,
        varfunding_scanner, cross_funding_engine, hl_cross_funding.

Usage:
    python cross_funding.py tick
    python cross_funding.py report
    python cross_funding.py status
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import hmac
import json
import math
import os
import statistics
import tempfile
import time
import traceback
from datetime import datetime, timedelta, timezone
from decimal import ROUND_DOWN, Decimal
from pathlib import Path
from urllib.parse import urlencode

import eth_account
import requests
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

# ═══════════════════════════════════════════════════════════════════════════════
# Section 1: Config
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.json"


def load_config() -> dict:
    """Load config.json and return the full config dict."""
    with open(CONFIG_PATH) as f:
        return json.load(f)


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _env_bool(key: str, default: bool = False) -> bool:
    v = os.environ.get(key, "")
    if not v:
        return default
    return v.lower() in ("true", "1", "yes")


def hl_private_key() -> str:
    k = _env("HL_PRIVATE_KEY")
    if not k:
        raise RuntimeError("HL_PRIVATE_KEY not set")
    return k


def hl_testnet() -> bool:
    return _env_bool("HL_TESTNET", default=False)


def hl_vault_address() -> str:
    return _env("HL_VAULT_ADDRESS")


def state_dir() -> Path:
    d = _env("STATE_DIR")
    return Path(d) if d else SCRIPT_DIR


def binance_api_key() -> str:
    k = _env("BINANCE_API_KEY")
    if not k:
        raise RuntimeError("BINANCE_API_KEY not set")
    return k


def binance_secret_key() -> str:
    k = _env("BINANCE_SECRET_KEY")
    if not k:
        raise RuntimeError("BINANCE_SECRET_KEY not set")
    return k


def bn_testnet() -> bool:
    return _env_bool("BINANCE_TESTNET", default=False)


# ═══════════════════════════════════════════════════════════════════════════════
# Section 2: State Management
# ═══════════════════════════════════════════════════════════════════════════════


def state_path(name: str) -> Path:
    return state_dir() / f"{name}_state.json"


def load_state(name: str) -> dict:
    p = state_path(name)
    if not p.exists():
        return {}
    with open(p) as f:
        return json.load(f)


def save_state(name: str, data: dict) -> None:
    """Atomic state file write."""
    p = state_path(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, suffix=".json.tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# --- Process lock ---

_lock_fd = None


def acquire_lock(name: str) -> bool:
    """Acquire exclusive lock to prevent concurrent instances."""
    global _lock_fd
    lock_path = state_dir() / f".{name}.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    _lock_fd = open(lock_path, "w")
    try:
        fcntl.flock(_lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _lock_fd.write(str(os.getpid()))
        _lock_fd.flush()
        return True
    except (OSError, IOError):
        _lock_fd.close()
        _lock_fd = None
        return False


def release_lock() -> None:
    global _lock_fd
    if _lock_fd is not None:
        try:
            fcntl.flock(_lock_fd, fcntl.LOCK_UN)
            _lock_fd.close()
        except Exception:
            pass
        _lock_fd = None


# ═══════════════════════════════════════════════════════════════════════════════
# Section 3: Emit (structured JSON output + notifications)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Notification credentials ────────────────────────────────────────────────


def _parse_toml_section(text: str, section: str) -> dict[str, str]:
    """Extract key=value pairs from a TOML section. Simple parser, no deps."""
    result: dict[str, str] = {}
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_section = stripped.rstrip("]").lstrip("[").strip() == section
            continue
        if in_section and "=" in stripped and not stripped.startswith("#"):
            k, v = stripped.split("=", 1)
            result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def _read_daemon_configs() -> list[dict]:
    """Read all available daemon configs for bot token resolution.

    Returns a list of config sources (OpenClaw JSON + ZeroClaw TOML instances).
    Callers try each source in order until a token is found.
    """
    sources: list[dict] = []

    # OpenClaw: JSON format
    oc_path = Path.home() / ".openclaw" / "openclaw.json"
    if oc_path.exists():
        try:
            data = json.loads(oc_path.read_text())
            channels = data.get("channels", {})
            sources.append({"_type": "openclaw", "_data": channels})
        except Exception:
            pass

    # ZeroClaw: TOML format (try all instances)
    for instance in ["zeroclaw-strategy", "zeroclaw", "zeroclaw-data", "zeroclaw-ops"]:
        cfg_path = Path.home() / f".{instance}" / "config.toml"
        if cfg_path.exists():
            try:
                sources.append({"_type": "zeroclaw", "_text": cfg_path.read_text()})
            except Exception:
                pass
    return sources


_DAEMON_CONFIGS = _read_daemon_configs()


def _get_discord_token() -> str:
    """Discord bot token: env > first available daemon config."""
    env_token = os.environ.get("DISCORD_BOT_TOKEN", "")
    if env_token:
        return env_token
    for cfg in _DAEMON_CONFIGS:
        token = ""
        if cfg["_type"] == "openclaw":
            token = cfg.get("_data", {}).get("discord", {}).get("token", "")
        elif cfg["_type"] == "zeroclaw":
            section = _parse_toml_section(
                cfg.get("_text", ""), "channels_config.discord"
            )
            token = section.get("bot_token", "")
        if token:
            return token
    return ""


def _get_discord_channel_id() -> str:
    """Discord channel ID: only from env (each strategy configures its own)."""
    return os.environ.get("DISCORD_CHANNEL_ID", "")


def _get_telegram_config() -> tuple[str, str]:
    """Telegram creds: env > first available daemon config.

    bot_token falls back to daemon config, chat_id from env only.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token:
        for cfg in _DAEMON_CONFIGS:
            if cfg["_type"] == "openclaw":
                # OpenClaw uses camelCase "botToken"
                token = cfg.get("_data", {}).get("telegram", {}).get("botToken", "")
            elif cfg["_type"] == "zeroclaw":
                section = _parse_toml_section(
                    cfg.get("_text", ""), "channels_config.telegram"
                )
                token = section.get("bot_token", "")
            if token:
                break
    return token, chat_id


DISCORD_CHANNEL_ID = _get_discord_channel_id()
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID = _get_telegram_config()

# ── Notification card builder ────────────────────────────────────────────────

STRATEGY_LABEL = "Cross-Funding"
_EX_SHORT = {"hyperliquid": "HL", "binance": "BN"}


def _next_settlement_countdown() -> dict[str, str]:
    """Calculate countdown to next funding rate settlement for both exchanges.

    HL: settles every hour (xx:00)
    Binance: settles every 8 hours (00:00 / 08:00 / 16:00 UTC)
    """
    now = datetime.now(timezone.utc)

    # HL: next whole hour
    hl_next = now.replace(minute=0, second=0, microsecond=0)
    if hl_next <= now:
        hl_next += timedelta(hours=1)
    hl_secs = (hl_next - now).total_seconds()
    hl_m = int(hl_secs // 60)
    hl_str = f"{hl_m}m"

    # Binance: next 0/8/16 hour mark
    bn_hours = [0, 8, 16, 24]  # 24 = next day 0:00
    for h in bn_hours:
        bn_next = now.replace(hour=h % 24, minute=0, second=0, microsecond=0)
        if h == 24:
            bn_next += timedelta(days=1)
            bn_next = bn_next.replace(hour=0)
        if bn_next > now:
            break
    bn_secs = (bn_next - now).total_seconds()
    bn_h = int(bn_secs // 3600)
    bn_m = int((bn_secs % 3600) // 60)
    bn_str = f"{bn_h}h{bn_m}m" if bn_h else f"{bn_m}m"

    return {"hl": hl_str, "bn": bn_str}


def _build_notification(tier: str, data: dict) -> dict | None:
    """Build dual-format notification (discord embed + text markdown).

    Returns {"tier": str, "discord": {...}, "text": str} or None if silent.
    """

    # ── Trade Alert (open / close) ───────────────────────────────────────
    if tier == "trade_alert":
        event = data.get("type", "")
        coin = data.get("coin", "?")
        long_ex = data.get("long_exchange", "?")
        short_ex = data.get("short_exchange", "?")

        if event == "position_opened":
            size = data.get("size", 0)
            price = data.get("entry_price", 0)
            notional = round(size * price, 2)
            leverage = data.get("leverage", 1)
            hl_rate = data.get("hl_rate", 0)
            bn_rate = data.get("bn_rate", 0)
            spread = abs(bn_rate - hl_rate)
            apr = spread * 3 * 365 * 100

            fields = [
                {
                    "name": "Long",
                    "value": _EX_SHORT.get(long_ex, long_ex),
                    "inline": True,
                },
                {
                    "name": "Short",
                    "value": _EX_SHORT.get(short_ex, short_ex),
                    "inline": True,
                },
                {"name": "杠杆", "value": f"{leverage}x", "inline": True},
                {"name": "Size", "value": f"{size:g} {coin}", "inline": True},
                {"name": "名义价值", "value": f"${notional:,.2f}", "inline": True},
                {"name": "Spread", "value": f"{spread:.4%}", "inline": True},
                {
                    "name": "预估 APR",
                    "value": f"{apr:.1f}%",
                    "inline": True,
                },
            ]

            text_lines = [
                f"🔄 **开仓 · {coin} · {STRATEGY_LABEL}**",
                f"📍 Long `{long_ex}` / Short `{short_ex}` | `{leverage}x`",
                f"📦 Size: `{size:g} {coin}` (`${notional:,.2f}`)",
                f"📈 Spread: `{spread:.4%}` → `{apr:.1f}%` APR",
            ]

            return {
                "tier": "trade_alert",
                "discord": {
                    "title": f"🔄 开仓 · {coin} · {STRATEGY_LABEL}",
                    "color": 0x00CC66,
                    "fields": fields,
                },
                "text": "\n".join(text_lines),
            }

        if event == "position_closed":
            funding = data.get("funding_earned", 0)

            text_lines = [
                f"📤 **平仓 · {coin} · {STRATEGY_LABEL}**",
                f"💵 Funding Earned: `${funding:,.2f}`",
            ]

            return {
                "tier": "trade_alert",
                "discord": {
                    "title": f"📤 平仓 · {coin} · {STRATEGY_LABEL}",
                    "color": 0xFF6600,
                    "fields": [
                        {
                            "name": "Funding Earned",
                            "value": f"${funding:,.2f}",
                            "inline": True,
                        },
                    ],
                },
                "text": "\n".join(text_lines),
            }

        if event == "switch_start":
            from_coin = data.get("from", "?")
            to_coin = data.get("to", "?")
            from_apr = data.get("from_apr", 0)
            to_apr = data.get("to_apr", 0)
            apr_gain = data.get("apr_gain", 0)
            trading_cost = data.get("trading_cost_pct", 0)
            bn_unreal = data.get("bn_unrealized_pct", 0)
            hl_unreal = data.get("hl_unrealized_pct", 0)
            sunk_cost = data.get("sunk_cost_pct", 0)
            total_cost = data.get("total_switch_cost", 0)
            bn_elapsed = data.get("bn_elapsed_h", 0)
            hl_elapsed = data.get("hl_elapsed_m", 0)

            # Show sunk sign: positive = forfeit earnings, negative = avoid losses
            bn_sign = "+" if bn_unreal >= 0 else ""
            hl_sign = "+" if hl_unreal >= 0 else ""
            sunk_sign = "+" if sunk_cost >= 0 else ""

            fields = [
                {
                    "name": "From",
                    "value": f"{from_coin} ({from_apr:.1f}%)",
                    "inline": True,
                },
                {"name": "To", "value": f"{to_coin} ({to_apr:.1f}%)", "inline": True},
                {"name": "净收益", "value": f"+{apr_gain:.1f}% APR", "inline": True},
                {
                    "name": "交易成本",
                    "value": f"{trading_cost:.2f}%",
                    "inline": True,
                },
                {
                    "name": "BN 未实现",
                    "value": f"{bn_sign}{bn_unreal:.4f}% ({bn_elapsed:.1f}h/8h)",
                    "inline": True,
                },
                {
                    "name": "HL 未实现",
                    "value": f"{hl_sign}{hl_unreal:.4f}% ({hl_elapsed:.0f}m/60m)",
                    "inline": True,
                },
                {
                    "name": "总成本",
                    "value": f"{total_cost:.2f}% (交易{trading_cost:.2f} + 沉没{sunk_sign}{sunk_cost:.4f})",
                    "inline": False,
                },
            ]
            text_lines = [
                f"🔄 **换仓 · {STRATEGY_LABEL}**",
                f"📉 `{from_coin}` ({from_apr:.1f}%) → 📈 `{to_coin}` ({to_apr:.1f}%)",
                f"💰 净收益: `+{apr_gain:.1f}%` APR",
                f"💸 交易: `{trading_cost:.2f}%` · BN未实现: `{bn_sign}{bn_unreal:.4f}%` ({bn_elapsed:.1f}h/8h) · HL未实现: `{hl_sign}{hl_unreal:.4f}%` ({hl_elapsed:.0f}m/60m)",
                f"📊 总成本: `{total_cost:.2f}%`",
            ]
            return {
                "tier": "trade_alert",
                "discord": {
                    "title": f"🔄 换仓 · {from_coin} → {to_coin} · {STRATEGY_LABEL}",
                    "color": 0x9B59B6,
                    "fields": fields,
                },
                "text": "\n".join(text_lines),
            }

        return None

    # ── Risk Alert ───────────────────────────────────────────────────────
    if tier == "risk_alert":
        coin = data.get("coin", "?")
        reason = data.get("reason", data.get("context", "unknown"))
        current_apr = data.get("current_apr", 0)
        delta_pct = data.get("delta_pct", 0)

        fields = [
            {"name": "原因", "value": str(reason), "inline": False},
            {"name": "当前 APR", "value": f"{current_apr:.1f}%", "inline": True},
            {"name": "Delta 偏差", "value": f"{delta_pct:.1f}%", "inline": True},
        ]

        text_lines = [
            f"🛑 **风险告警 · {coin} · {STRATEGY_LABEL}**",
            f"⚠️ 原因: `{reason}`",
            f"📊 APR: `{current_apr:.1f}%` | Delta: `{delta_pct:.1f}%`",
        ]

        return {
            "tier": "risk_alert",
            "discord": {
                "title": f"🛑 风险告警 · {coin} · {STRATEGY_LABEL}",
                "color": 0xFF0000,
                "fields": fields,
            },
            "text": "\n".join(text_lines),
        }

    # ── Opportunity Alert (APR ≥ 20%) ───────────────────────────────────
    if tier == "opportunity_alert":
        opps = data.get("opportunities", [])
        count = data.get("count", 0)

        # Build per-line list sorted by APR descending (already sorted)
        desc_lines = []
        text_lines = [f"🔍 **{count} 个套利机会 · APR ≥ 20%**"]
        for o in opps:
            coin = o["coin"]
            apr = o["apr"]
            long_ex = _EX_SHORT.get(o["long"], o["long"])
            short_ex = _EX_SHORT.get(o["short"], o["short"])
            desc_lines.append(
                f"`{coin}` — **{apr:.1f}%** APR · L:{long_ex} S:{short_ex}"
            )
            text_lines.append(
                f"• `{coin}` — `{apr:.1f}%` APR · Long `{long_ex}` / Short `{short_ex}`"
            )

        return {
            "tier": "opportunity_alert",
            "discord": {
                "title": f"🔍 {count} 个套利机会 · APR ≥ 20%",
                "color": 0x3498DB,
                "description": "\n".join(desc_lines),
            },
            "text": "\n".join(text_lines),
        }

    # ── Hourly Pulse ─────────────────────────────────────────────────────
    if tier == "hourly_pulse":
        healthy = data.get("healthy", True)
        position_count = data.get("position_count", 0)
        report_positions = data.get("positions", [])
        position_health = data.get("position_health", [])

        hl_bal = data.get("hl_balance", 0)
        bn_bal = data.get("bn_balance", 0)
        total = round(hl_bal + bn_bal, 2)

        pnl = data.get("pnl", 0)
        roi_pct = data.get("roi_pct", 0)

        health_icon = "✅" if healthy else "⚠️"
        countdown = _next_settlement_countdown()

        fields = [
            # Row 1: Assets
            {"name": "HL", "value": f"${hl_bal:,.2f}", "inline": True},
            {"name": "BN", "value": f"${bn_bal:,.2f}", "inline": True},
            {"name": "Total", "value": f"${total:,.2f}", "inline": True},
        ]

        # Add each position as a field
        for rp in report_positions:
            rp_coin = rp.get("coin", "?")
            rp_dir = rp.get("direction", {})
            rp_long_ex = rp_dir.get("long_exchange", "?")
            rp_short_ex = rp_dir.get("short_exchange", "?")
            rp_long_label = _EX_SHORT.get(rp_long_ex, rp_long_ex)
            rp_short_label = _EX_SHORT.get(rp_short_ex, rp_short_ex)
            rp_size = rp.get("size", 0)
            rp_price = rp.get("entry_price", 0)
            rp_notional = round(rp_size * rp_price, 2) if rp_size and rp_price else 0
            rp_apr = rp.get("current_apr", 0)
            rp_spread = rp.get("current_spread", 0)
            rp_healthy = rp.get("healthy", True)
            rp_health_icon = "✅" if rp_healthy else "⚠️"
            fields.append({
                "name": f"{rp_health_icon} {rp_coin}",
                "value": (
                    f"L:{rp_long_label}/S:{rp_short_label} · "
                    f"`{rp_size:g}` (${rp_notional:,.0f}) · "
                    f"{rp_spread:.4%}/8h → {rp_apr:.1f}% APR"
                ),
                "inline": False,
            })

        fields.append({
            "name": "结算倒计时",
            "value": f"HL `{countdown['hl']}` / BN `{countdown['bn']}`",
            "inline": False,
        })

        footer = f"PnL ${pnl:+,.2f} ({roi_pct:+.2f}%) · {health_icon} {position_count}仓"

        coins_str = "/".join(rp.get("coin", "?") for rp in report_positions) or "空仓"
        text_lines = [
            f"📊 **{coins_str} · {STRATEGY_LABEL} · 运行中**",
            f"💰 HL `${hl_bal:,.2f}` + BN `${bn_bal:,.2f}` = **`${total:,.2f}`**",
        ]
        for rp in report_positions:
            rp_coin = rp.get("coin", "?")
            rp_dir = rp.get("direction", {})
            rp_long_label = _EX_SHORT.get(rp_dir.get("long_exchange", "?"), "?")
            rp_short_label = _EX_SHORT.get(rp_dir.get("short_exchange", "?"), "?")
            rp_size = rp.get("size", 0)
            rp_price = rp.get("entry_price", 0)
            rp_notional = round(rp_size * rp_price, 2) if rp_size and rp_price else 0
            rp_apr = rp.get("current_apr", 0)
            rp_spread = rp.get("current_spread", 0)
            text_lines.append(
                f"📍 `{rp_coin}` L:`{rp_long_label}` S:`{rp_short_label}` | "
                f"`{rp_size:g}` (${rp_notional:,.0f}) | "
                f"{rp_spread:.4%}/8h ({rp_apr:.1f}% APR)"
            )
        text_lines += [
            f"⏱ 结算: HL `{countdown['hl']}` / BN `{countdown['bn']}`",
            f"_{footer}_",
        ]

        return {
            "tier": "hourly_pulse",
            "discord": {
                "title": f"📊 {coins_str} · {STRATEGY_LABEL} · 运行中",
                "color": 0x808080,
                "fields": fields,
                "footer": {"text": footer},
            },
            "text": "\n".join(text_lines),
        }

    # ── Daily Report ─────────────────────────────────────────────────────
    if tier == "daily_report":
        coin = data.get("coin", "—")
        direction = data.get("direction", {})
        long_ex = direction.get("long_exchange", "?")
        short_ex = direction.get("short_exchange", "?")

        hl_bal = data.get("hl_balance", 0)
        bn_bal = data.get("bn_balance", 0)
        total = data.get("current_total_balance", round(hl_bal + bn_bal, 2))
        entry_total = data.get("entry_total_balance", 0)

        pnl = data.get("pnl", 0)
        roi_pct = data.get("roi_pct", 0)

        rate_map = {
            "hyperliquid": data.get("hl_rate", 0),
            "binance": data.get("bn_rate", 0),
        }
        long_rate = rate_map.get(long_ex, 0)
        short_rate = rate_map.get(short_ex, 0)
        current_apr = data.get("current_apr", 0)
        current_spread = data.get("current_spread", 0)
        has_positions = data.get("has_positions", False)
        position_count = data.get("position_count", 0)
        report_positions = data.get("positions", [])

        today = datetime.now(timezone.utc).date().isoformat()

        if has_positions and report_positions:
            # Build fields for each position
            fields = []
            for rp in report_positions:
                rp_coin = rp.get("coin", "?")
                rp_dir = rp.get("direction", {})
                rp_long_ex = rp_dir.get("long_exchange", "?")
                rp_short_ex = rp_dir.get("short_exchange", "?")
                rp_long_label = _EX_SHORT.get(rp_long_ex, rp_long_ex)
                rp_short_label = _EX_SHORT.get(rp_short_ex, rp_short_ex)
                rp_apr = rp.get("current_apr", 0)
                rp_funding = rp.get("total_funding_earned", 0)
                rp_entry_time = rp.get("entry_time", "")
                rp_hours = 0.0
                if rp_entry_time:
                    try:
                        rp_hours = (
                            datetime.now(timezone.utc) - datetime.fromisoformat(rp_entry_time)
                        ).total_seconds() / 3600
                    except (ValueError, TypeError):
                        pass
                fields.append({
                    "name": f"{rp_coin}",
                    "value": (
                        f"L:{rp_long_label}/S:{rp_short_label} · "
                        f"{rp_apr:.1f}% APR · {rp_hours:.1f}h · "
                        f"funding ${rp_funding:+.2f}"
                    ),
                    "inline": False,
                })

            # Assets row
            fields += [
                {"name": "HL", "value": f"${hl_bal:,.2f}", "inline": True},
                {"name": "BN", "value": f"${bn_bal:,.2f}", "inline": True},
                {"name": "Total", "value": f"${total:,.2f}", "inline": True},
                {
                    "name": "💵 PnL",
                    "value": f"${pnl:+,.2f} ({roi_pct:+.2f}%)",
                    "inline": True,
                },
            ]
            footer = f"本金 ${entry_total:,.0f} · {position_count} 个持仓"
        else:
            fields = [
                {"name": "状态", "value": "空仓观望中", "inline": True},
                {"name": "HL", "value": f"${hl_bal:,.2f}", "inline": True},
                {
                    "name": "BN",
                    "value": f"${bn_bal:,.2f}",
                    "inline": True,
                },
                {
                    "name": "💰 总资产",
                    "value": f"${total:,.2f}",
                    "inline": True,
                },
            ]
            footer = "无持仓"

        text_lines = [
            f"📈 **日报 · {STRATEGY_LABEL} · {today}**",
            "",
        ]
        if has_positions and report_positions:
            text_lines.append(f"**持仓 ({position_count})**")
            for rp in report_positions:
                rp_coin = rp.get("coin", "?")
                rp_dir = rp.get("direction", {})
                rp_long_label = _EX_SHORT.get(rp_dir.get("long_exchange", "?"), "?")
                rp_short_label = _EX_SHORT.get(rp_dir.get("short_exchange", "?"), "?")
                rp_apr = rp.get("current_apr", 0)
                rp_spread = rp.get("current_spread", 0)
                text_lines.append(
                    f"  `{rp_coin}` | L:`{rp_long_label}` S:`{rp_short_label}` | "
                    f"Spread `{rp_spread:.4%}/8h` ({rp_apr:.1f}% APR)"
                )
            text_lines += [
                "",
                "**资产**",
                f"  HL: `${hl_bal:,.2f}` | BN: `${bn_bal:,.2f}` | Total: `${total:,.2f}`",
                f"  PnL: `${pnl:+,.2f}` (`{roi_pct:+.2f}%`)",
            ]
        else:
            text_lines += [
                "**状态**: 空仓观望中",
                f"**资产**: HL `${hl_bal:,.2f}` | BN `${bn_bal:,.2f}` | Total `${total:,.2f}`",
            ]
        text_lines.append(f"\n_{footer}_")

        return {
            "tier": "daily_report",
            "discord": {
                "title": f"📈 日报 · {STRATEGY_LABEL} · {today}",
                "color": 0x3399FF,
                "fields": fields,
                "footer": {"text": footer},
            },
            "text": "\n".join(text_lines),
        }

    return None


# ── Notification sending ─────────────────────────────────────────────────────


def _send_telegram(text: str) -> bool:
    import urllib.error
    import urllib.request

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False


def _send_notification(notif: dict) -> None:
    """Send notification to Discord (embed) and Telegram (text)."""
    import urllib.error
    import urllib.request

    discord_ok = False
    token = _get_discord_token()
    embed = notif.get("discord", {})
    if token and DISCORD_CHANNEL_ID and embed:
        url = f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages"
        payload = {"embeds": [embed]}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://openclaw.ai, 1.0)",
            },
        )
        try:
            urllib.request.urlopen(req, timeout=10)
            discord_ok = True
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            pass

    tg_ok = False
    text = notif.get("text", "")
    if text:
        tg_ok = _send_telegram(text)

    if not discord_ok and not tg_ok and (token or TELEGRAM_BOT_TOKEN):
        pass


# ── Public emit API ──────────────────────────────────────────────────────────


def emit(event_type: str, data: dict, *, notify: bool = False, tier: str = "") -> None:
    """Output one JSON event line to stdout, optionally push notification by tier.

    Args:
        event_type: Event type (tick, report, position_opened, etc.)
        data: Event data dict
        notify: Whether to mark as needing notification
        tier: Notification level (trade_alert, risk_alert, hourly_pulse, daily_report)
              Empty string means no push
    """
    payload = {
        "type": event_type,
        "ts": datetime.now(timezone.utc).isoformat(),
        "notify": notify or bool(tier),
        **data,
    }
    if tier:
        notif = _build_notification(tier, {**data, "type": event_type})
        if notif:
            payload["notification"] = notif
            _send_notification(notif)
    print(json.dumps(payload, ensure_ascii=False), flush=True)


def emit_error(context: str, error: Exception, *, notify: bool = False) -> None:
    data = {
        "context": context,
        "error": str(error),
        "traceback": traceback.format_exc(),
    }
    tier = "risk_alert" if notify else ""
    emit("error", data, notify=notify, tier=tier)


# ═══════════════════════════════════════════════════════════════════════════════
# Section 4: Circuit Breaker
# ═══════════════════════════════════════════════════════════════════════════════


class CircuitBreaker:
    def __init__(self) -> None:
        cfg = load_config()["shared"]
        self.max_errors: int = cfg["max_consecutive_errors"]
        self.cooldown: int = cfg["cooldown_after_errors"]
        self.consecutive_errors = 0
        self.cooldown_until = 0.0

    def is_open(self) -> bool:
        if time.time() < self.cooldown_until:
            return True
        if self.cooldown_until > 0 and time.time() >= self.cooldown_until:
            self.consecutive_errors = 0
            self.cooldown_until = 0.0
        return False

    def record_success(self) -> None:
        self.consecutive_errors = 0
        self.cooldown_until = 0.0

    def record_error(self, context: str = "") -> bool:
        """Record error, returns True if circuit breaker tripped."""
        self.consecutive_errors += 1
        if self.consecutive_errors >= self.max_errors:
            self.cooldown_until = time.time() + self.cooldown
            emit(
                "circuit_breaker",
                {
                    "status": "open",
                    "errors": self.consecutive_errors,
                    "cooldown_s": self.cooldown,
                    "context": context,
                },
                notify=True,
            )
            return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# Section 5: HLClient (Hyperliquid SDK wrapper)
# ═══════════════════════════════════════════════════════════════════════════════

# ---- Spot name mapping ----
_SPOT_TOKEN_MAP = {"BTC": "UBTC", "ETH": "UETH"}
_SPOT_TOKEN_REVERSE = {v: k for k, v in _SPOT_TOKEN_MAP.items()}


def _perp_to_spot_token(coin: str) -> str:
    return _SPOT_TOKEN_MAP.get(coin, coin)


def _perp_to_spot_pair(coin: str) -> str:
    return f"{_perp_to_spot_token(coin)}/USDC"


def _spot_token_to_perp(token: str) -> str:
    return _SPOT_TOKEN_REVERSE.get(token, token)


def _interval_to_ms(interval: str) -> int:
    unit = interval[-1]
    val = int(interval[:-1])
    multipliers = {"m": 60_000, "h": 3_600_000, "d": 86_400_000}
    return val * multipliers.get(unit, 3_600_000)


class HLClient:
    """Unified Hyperliquid read + write API wrapper."""

    def __init__(
        self, private_key: str, testnet: bool = False, vault_address: str = ""
    ) -> None:
        self.account = eth_account.Account.from_key(private_key)
        self.wallet_address = self.account.address
        base_url = constants.TESTNET_API_URL if testnet else constants.MAINNET_API_URL
        self.base_url = base_url
        self.testnet = testnet

        info_kwargs: dict = {"skip_ws": True}
        try:
            self.info = Info(base_url, **info_kwargs)
        except (IndexError, KeyError):
            self.info = Info(
                base_url, skip_ws=True, spot_meta={"tokens": [], "universe": []}
            )

        exchange_kwargs: dict = {}
        if vault_address:
            exchange_kwargs["account_address"] = vault_address

        try:
            self.exchange = Exchange(self.account, base_url, **exchange_kwargs)
        except (IndexError, KeyError):
            self.exchange = Exchange(
                self.account,
                base_url,
                spot_meta={"tokens": [], "universe": []},
                **exchange_kwargs,
            )

        if vault_address:
            self.address = vault_address
            self.balance_address = vault_address
        else:
            master = self._resolve_master_address()
            if master:
                self.address = master
                self.balance_address = master
            else:
                self.address = self.wallet_address
                self.balance_address = self.wallet_address

        self._meta: dict[str, object] | None = None
        self._spot_meta: dict | None = None
        self._sz_decimals: dict[str, int] = {}

    def _resolve_master_address(self) -> str | None:
        """Detect if current key is an agent wallet, return master address."""
        try:
            resp = requests.post(
                f"{self.base_url}/info",
                json={
                    "type": "userNonFundingLedgerUpdates",
                    "user": self.wallet_address,
                    "startTime": 0,
                },
                timeout=5,
            )
            updates = resp.json()
            for u in updates:
                delta = u.get("delta", {})
                if delta.get("type") == "send":
                    source = delta.get("user", "")
                    if source and source.lower() != self.wallet_address.lower():
                        emit(
                            "agent_wallet_detected",
                            {
                                "agent": self.wallet_address,
                                "master": source,
                            },
                        )
                        return source
        except Exception:
            pass
        return None

    # ---- Metadata ----

    def _ensure_meta(self) -> None:
        if self._meta is None:
            self._meta = self.info.meta()
            for asset in self._meta["universe"]:
                self._sz_decimals[asset["name"]] = asset["szDecimals"]

    def _ensure_spot_meta(self) -> None:
        if self._spot_meta is None:
            self._spot_meta = self.info.spot_meta()

    def sz_decimals(self, coin: str) -> int:
        self._ensure_meta()
        return self._sz_decimals.get(coin, 2)

    # ---- Market data ----

    def get_mid_price(self, coin: str) -> float:
        mids = self.info.all_mids()
        return float(mids[coin])

    def get_candles(
        self, coin: str, interval: str = "1h", count: int = 24
    ) -> list[dict]:
        now_ms = int(time.time() * 1000)
        interval_ms = _interval_to_ms(interval)
        start_ms = now_ms - interval_ms * count
        raw = self.info.candles_snapshot(coin, interval, start_ms, now_ms)
        result = []
        for c in raw:
            result.append(
                {
                    "t": c["t"],
                    "o": float(c["o"]),
                    "h": float(c["h"]),
                    "l": float(c["l"]),
                    "c": float(c["c"]),
                    "v": float(c["v"]),
                }
            )
        return result[-count:]

    def get_funding_rate(self, coin: str) -> float:
        """Get current funding rate for a coin (per 8h)."""
        ctx = self.info.meta_and_asset_ctxs()
        for asset_meta, asset_ctx in zip(ctx[0]["universe"], ctx[1]):
            if asset_meta["name"] == coin:
                return float(asset_ctx["funding"])
        return 0.0

    def get_all_funding_rates(self) -> dict[str, float]:
        ctx = self.info.meta_and_asset_ctxs()
        rates = {}
        for asset_meta, asset_ctx in zip(ctx[0]["universe"], ctx[1]):
            rates[asset_meta["name"]] = float(asset_ctx["funding"])
        return rates

    # ---- Account ----

    def get_usdc_balance(self) -> float:
        """Get total equity: spot USDC total (includes perp margin + unrealized PnL)."""
        try:
            spot_state = self.info.spot_user_state(self.balance_address)
            for bal in spot_state.get("balances", []):
                if bal["coin"] == "USDC":
                    return float(bal["total"])
        except Exception:
            pass
        # Fallback: perp accountValue only (spot API unavailable)
        state = self.info.user_state(self.balance_address)
        return float(state["marginSummary"]["accountValue"])

    def get_withdrawable(self) -> float:
        state = self.info.user_state(self.balance_address)
        return float(state["withdrawable"])

    def get_position(self, coin: str) -> dict | None:
        state = self.info.user_state(self.address)
        for pos in state.get("assetPositions", []):
            item = pos["position"]
            if item["coin"] == coin:
                return {
                    "coin": item["coin"],
                    "size": float(item["szi"]),
                    "entry_px": float(item["entryPx"]) if item.get("entryPx") else 0.0,
                    "unrealized_pnl": float(item["unrealizedPnl"]),
                    "cum_funding": float(item.get("cumFunding", {}).get("sinceOpen", 0.0)),
                    "leverage_type": item["leverage"]["type"],
                    "leverage_value": int(item["leverage"]["value"]),
                    "liquidation_px": float(item["liquidationPx"])
                    if item.get("liquidationPx")
                    else 0.0,
                    "mark_px": float(item.get("positionValue", 0)) / abs(float(item["szi"]))
                    if float(item["szi"]) != 0
                    else 0.0,
                }
        return None

    def get_all_positions(self) -> list[dict]:
        state = self.info.user_state(self.address)
        positions = []
        for pos in state.get("assetPositions", []):
            item = pos["position"]
            sz = float(item["szi"])
            if sz != 0:
                positions.append(
                    {
                        "coin": item["coin"],
                        "size": sz,
                        "entry_px": float(item["entryPx"])
                        if item.get("entryPx")
                        else 0.0,
                        "unrealized_pnl": float(item["unrealizedPnl"]),
                    }
                )
        return positions

    def get_spot_balance(self, coin: str) -> float:
        spot_coin = _perp_to_spot_token(coin)
        balances = self.info.spot_user_state(self.balance_address)
        for bal in balances.get("balances", []):
            if bal["coin"] == spot_coin:
                return float(bal["total"]) - float(bal["hold"])
        return 0.0

    def get_spot_usdc(self) -> float:
        balances = self.info.spot_user_state(self.balance_address)
        for bal in balances.get("balances", []):
            if bal["coin"] == "USDC":
                return float(bal["total"]) - float(bal["hold"])
        return 0.0

    def get_coins_with_spot_and_perp(self) -> set[str]:
        self._ensure_meta()
        self._ensure_spot_meta()
        perp_names = {a["name"] for a in self._meta["universe"]}  # type: ignore[index]
        spot_tokens = set()
        for token in self._spot_meta.get("tokens", []):  # type: ignore[union-attr]
            name = token["name"]
            if name == "USDC":
                continue
            perp_name = (
                name[1:] if name.startswith("U") and name[1:] in perp_names else name
            )
            if perp_name in perp_names:
                spot_tokens.add(perp_name)
        return spot_tokens

    def transfer_to_spot(self, usd_amount: float) -> dict:
        return self.exchange.usd_class_transfer(usd_amount, to_perp=False)

    def transfer_to_perp(self, usd_amount: float) -> dict:
        return self.exchange.usd_class_transfer(usd_amount, to_perp=True)

    def get_open_orders(self, coin: str | None = None) -> list[dict]:
        orders = self.info.open_orders(self.address)
        result = []
        for o in orders:
            if coin and o["coin"] != coin:
                continue
            result.append(
                {
                    "oid": o["oid"],
                    "coin": o["coin"],
                    "side": "buy" if o["side"] == "B" else "sell",
                    "size": float(o["sz"]),
                    "price": float(o["limitPx"]),
                    "order_type": o.get("orderType", "limit"),
                }
            )
        return result

    # ---- Trading ----

    def set_leverage(self, coin: str, leverage: int, cross: bool = False) -> None:
        self.exchange.update_leverage(leverage, coin, is_cross=cross)

    def limit_order(
        self,
        coin: str,
        is_buy: bool,
        size: float,
        price: float,
        *,
        reduce_only: bool = False,
    ) -> dict:
        size = self.round_size(coin, size)
        price = self._round_price(price)
        if size <= 0:
            return {"status": "error", "msg": "size too small"}
        result = self.exchange.order(
            coin,
            is_buy,
            size,
            price,
            {"limit": {"tif": "Gtc"}},
            reduce_only=reduce_only,
        )
        self._log_order("limit", coin, is_buy, size, price, result)
        return result

    def market_order(
        self,
        coin: str,
        is_buy: bool,
        size: float,
        *,
        slippage: float = 0.05,
    ) -> dict:
        size = self.round_size(coin, size)
        if size <= 0:
            return {"status": "error", "msg": "size too small"}
        mid = self.get_mid_price(coin)
        px = mid * (1 + slippage) if is_buy else mid * (1 - slippage)
        px = self._round_price(px)
        result = self.exchange.order(
            coin,
            is_buy,
            size,
            px,
            {"limit": {"tif": "Ioc"}},
        )
        self._log_order("market", coin, is_buy, size, px, result)
        return result

    def place_tp(self, coin: str, is_buy: bool, size: float, trigger_px: float) -> dict:
        size = self.round_size(coin, size)
        trigger_px = self._round_price(trigger_px)
        result = self.exchange.order(
            coin,
            is_buy,
            size,
            trigger_px,
            {"trigger": {"isMarket": True, "triggerPx": str(trigger_px), "tpsl": "tp"}},
            reduce_only=True,
        )
        self._log_order("tp", coin, is_buy, size, trigger_px, result)
        return result

    def place_sl(self, coin: str, is_buy: bool, size: float, trigger_px: float) -> dict:
        size = self.round_size(coin, size)
        trigger_px = self._round_price(trigger_px)
        result = self.exchange.order(
            coin,
            is_buy,
            size,
            trigger_px,
            {"trigger": {"isMarket": True, "triggerPx": str(trigger_px), "tpsl": "sl"}},
            reduce_only=True,
        )
        self._log_order("sl", coin, is_buy, size, trigger_px, result)
        return result

    def cancel_all(self, coin: str) -> None:
        orders = self.info.open_orders(self.address)
        for o in orders:
            if o["coin"] == coin:
                try:
                    self.exchange.cancel(coin, o["oid"])
                except Exception:
                    pass

    def spot_market_buy(
        self, coin: str, size: float, *, slippage: float = 0.05
    ) -> dict:
        spot_pair = _perp_to_spot_pair(coin)
        size = self.round_size(coin, size)
        if size <= 0:
            return {"status": "error", "msg": "size too small"}
        mid = self.get_mid_price(spot_pair)
        px = self._round_price(mid * (1 + slippage))
        result = self.exchange.order(
            spot_pair, True, size, px, {"limit": {"tif": "Ioc"}}
        )
        self._log_order("spot_buy", coin, True, size, px, result)
        return result

    def spot_market_sell(
        self, coin: str, size: float, *, slippage: float = 0.05
    ) -> dict:
        spot_pair = _perp_to_spot_pair(coin)
        size = self.round_size(coin, size)
        if size <= 0:
            return {"status": "error", "msg": "size too small"}
        mid = self.get_mid_price(spot_pair)
        px = self._round_price(mid * (1 - slippage))
        result = self.exchange.order(
            spot_pair, False, size, px, {"limit": {"tif": "Ioc"}}
        )
        self._log_order("spot_sell", coin, False, size, px, result)
        return result

    def close_position(self, coin: str, *, slippage: float = 0.001) -> dict | None:
        pos = self.get_position(coin)
        if not pos or pos["size"] == 0:
            return None
        is_buy = pos["size"] < 0
        size = abs(pos["size"])
        return self.market_order(coin, is_buy, size, slippage=slippage)

    # ---- Utils ----

    def round_size(self, coin: str, size: float) -> float:
        decimals = self.sz_decimals(coin)
        factor = 10**decimals
        return math.floor(size * factor) / factor

    def _round_price(self, price: float) -> float:
        if price <= 0:
            return 0.0
        magnitude = 10 ** math.floor(math.log10(price))
        return round(price / magnitude, 4) * magnitude

    def _log_order(
        self,
        kind: str,
        coin: str,
        is_buy: bool,
        size: float,
        price: float,
        result: dict,
    ) -> None:
        status = "ok"
        error = ""
        oid = None
        if result.get("status") == "err":
            status = "error"
            error = result.get("response", "")
        elif "response" in result and "data" in result["response"]:
            data = result["response"]["data"]
            if "statuses" in data and data["statuses"]:
                s = data["statuses"][0]
                if "error" in s:
                    status = "error"
                    error = s["error"]
                elif "resting" in s:
                    oid = s["resting"]["oid"]
                elif "filled" in s:
                    oid = s["filled"]["oid"]
        emit(
            "order",
            {
                "kind": kind,
                "coin": coin,
                "side": "buy" if is_buy else "sell",
                "size": size,
                "price": price,
                "status": status,
                "oid": oid,
                "error": error,
            },
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Section 6: BinanceClient (Binance USDS-M Futures REST)
# ═══════════════════════════════════════════════════════════════════════════════


class BinanceClient:
    """Binance USDS-M Futures REST API client."""

    MAINNET_URL = "https://fapi.binance.com"
    TESTNET_URL = "https://demo-fapi.binance.com"
    RECV_WINDOW = 10_000
    TIME_SYNC_TTL = 30

    def __init__(self, api_key: str, secret_key: str, testnet: bool = False) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = self.TESTNET_URL if testnet else self.MAINNET_URL

        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

        self._exchange_info_cache: dict | None = None
        self._exchange_info_ts: float = 0.0
        self._cache_ttl: float = 3600.0

        self._ts_offset_ms: int = 0
        self._ts_synced_at: float = 0.0

    # ---- Internal helpers ----

    def _get_timestamp(self) -> int:
        return int(time.time() * 1000) + self._ts_offset_ms

    def _sync_server_time(self, force: bool = False) -> None:
        now = time.time()
        if (
            not force
            and self._ts_synced_at
            and (now - self._ts_synced_at) < self.TIME_SYNC_TTL
        ):
            return

        url = f"{self.base_url}/fapi/v1/time"
        t0 = int(time.time() * 1000)
        resp = self.session.get(url, timeout=5)
        t1 = int(time.time() * 1000)
        resp.raise_for_status()

        server_time = int(resp.json()["serverTime"])
        midpoint = (t0 + t1) // 2
        self._ts_offset_ms = server_time - midpoint
        self._ts_synced_at = time.time()

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(
            self.secret_key.encode(),
            query_string.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        signed: bool = False,
    ) -> dict:
        url = f"{self.base_url}{endpoint}"
        base_params = dict(params or {})
        max_attempts = 2 if signed else 1

        for attempt in range(max_attempts):
            req_params = dict(base_params)

            if signed:
                self._sync_server_time(force=(attempt > 0))
                req_params["timestamp"] = self._get_timestamp()
                req_params["recvWindow"] = self.RECV_WINDOW
                req_params["signature"] = self._sign(req_params)

            if method == "GET":
                resp = self.session.get(url, params=req_params, timeout=10)
            else:
                resp = self.session.post(url, data=req_params, timeout=10)

            if resp.status_code != 200:
                try:
                    err = resp.json()
                except ValueError:
                    err = {}
                code = err.get("code", resp.status_code)
                msg = err.get("msg", resp.text)

                if (
                    signed
                    and attempt == 0
                    and (str(code) == "-1021" or "recvWindow" in str(msg))
                ):
                    self._ts_synced_at = 0.0
                    continue

                raise RuntimeError(f"Binance API Error {code}: {msg}")

            return resp.json()

        raise RuntimeError(f"Binance request failed after retries: {method} {endpoint}")

    def _to_symbol(self, coin: str) -> str:
        return f"{coin}USDT"

    def _get_exchange_info(self) -> dict:
        now = time.time()
        if (
            self._exchange_info_cache
            and (now - self._exchange_info_ts) < self._cache_ttl
        ):
            return self._exchange_info_cache
        self._exchange_info_cache = self._request("GET", "/fapi/v1/exchangeInfo")
        self._exchange_info_ts = now
        return self._exchange_info_cache

    def _get_precision(self, symbol: str) -> dict:
        info = self._get_exchange_info()
        for s in info.get("symbols", []):
            if s["symbol"] == symbol:
                result: dict = {
                    "tick_size": "0.01",
                    "step_size": "0.001",
                    "min_qty": "0.001",
                }
                for f in s.get("filters", []):
                    if f["filterType"] == "PRICE_FILTER":
                        result["tick_size"] = f["tickSize"]
                    elif f["filterType"] == "LOT_SIZE":
                        result["step_size"] = f["stepSize"]
                        result["min_qty"] = f["minQty"]
                return result
        raise RuntimeError(f"Symbol {symbol} not found in exchange info")

    # ---- Market Data ----

    def get_mid_price(self, coin: str) -> float:
        symbol = self._to_symbol(coin)
        data = self._request("GET", "/fapi/v1/premiumIndex", {"symbol": symbol})
        return float(data["markPrice"])

    def get_funding_rate(self, coin: str) -> float:
        symbol = self._to_symbol(coin)
        data = self._request("GET", "/fapi/v1/premiumIndex", {"symbol": symbol})
        return float(data["lastFundingRate"])

    def get_all_funding_rates(self) -> dict[str, float]:
        data = self._request("GET", "/fapi/v1/premiumIndex")
        rates: dict[str, float] = {}
        for item in data:
            symbol: str = item["symbol"]
            if symbol.endswith("USDT"):
                coin = symbol[: -len("USDT")]
                rates[coin] = float(item["lastFundingRate"])
        return rates

    # ---- Account ----

    def get_usdt_balance(self) -> float:
        """获取 USDT 账户权益（含未实现盈亏），与 HL accountValue 口径一致。"""
        data = self._request("GET", "/fapi/v2/balance", signed=True)
        for asset in data:
            if asset["asset"] == "USDT":
                balance = float(asset["balance"])
                unrealized_pnl = float(asset.get("crossUnPnl", 0))
                return balance + unrealized_pnl
        return 0.0

    def get_position(self, coin: str) -> dict | None:
        symbol = self._to_symbol(coin)
        data = self._request(
            "GET", "/fapi/v3/positionRisk", {"symbol": symbol}, signed=True
        )
        for pos in data:
            if pos["symbol"] == symbol:
                size = float(pos["positionAmt"])
                if size == 0:
                    return None
                return {
                    "coin": coin,
                    "size": size,
                    "entry_px": float(pos["entryPrice"]),
                    "unrealized_pnl": float(pos["unRealizedProfit"]),
                    "mark_px": float(pos.get("markPrice", 0)),
                }
        return None

    def get_all_positions(self) -> list[dict]:
        data = self._request("GET", "/fapi/v3/positionRisk", signed=True)
        positions = []
        for pos in data:
            size = float(pos["positionAmt"])
            if size != 0:
                symbol: str = pos["symbol"]
                coin = symbol[: -len("USDT")] if symbol.endswith("USDT") else symbol
                positions.append(
                    {
                        "coin": coin,
                        "size": size,
                        "entry_px": float(pos["entryPrice"]),
                        "unrealized_pnl": float(pos["unRealizedProfit"]),
                    }
                )
        return positions

    def get_funding_income(self, coin: str, start_time_ms: int) -> float:
        """Get total realized funding income since start_time_ms."""
        symbol = self._to_symbol(coin)
        total = 0.0
        current_start = start_time_ms
        while True:
            data = self._request(
                "GET",
                "/fapi/v1/income",
                {
                    "symbol": symbol,
                    "incomeType": "FUNDING_FEE",
                    "startTime": current_start,
                    "limit": 1000,
                },
                signed=True,
            )
            if not data:
                break
            for item in data:
                total += float(item["income"])
            if len(data) < 1000:
                break
            current_start = int(data[-1]["time"]) + 1
        return round(total, 4)

    # ---- Trading ----

    def set_leverage(self, coin: str, leverage: int) -> None:
        symbol = self._to_symbol(coin)
        self._request(
            "POST",
            "/fapi/v1/leverage",
            {"symbol": symbol, "leverage": leverage},
            signed=True,
        )

    def market_order(
        self, coin: str, is_buy: bool, size: float, *, slippage: float = 0.0
    ) -> dict:
        symbol = self._to_symbol(coin)
        size = self.round_size(coin, size)
        if slippage > 0:
            mid = self.get_mid_price(coin)
            px = mid * (1 + slippage) if is_buy else mid * (1 - slippage)
            px = self._round_price(coin, px)
            params = {
                "symbol": symbol,
                "side": "BUY" if is_buy else "SELL",
                "type": "LIMIT",
                "quantity": size,
                "price": px,
                "timeInForce": "IOC",
            }
        else:
            params = {
                "symbol": symbol,
                "side": "BUY" if is_buy else "SELL",
                "type": "MARKET",
                "quantity": size,
            }
        return self._request("POST", "/fapi/v1/order", params, signed=True)

    def close_position(self, coin: str, *, slippage: float = 0.001) -> dict | None:
        pos = self.get_position(coin)
        if not pos or pos["size"] == 0:
            return None
        is_buy = pos["size"] < 0
        size = abs(pos["size"])
        return self.market_order(coin, is_buy, size, slippage=slippage)

    # ---- Utils ----

    def round_size(self, coin: str, size: float) -> float:
        symbol = self._to_symbol(coin)
        precision = self._get_precision(symbol)
        step = Decimal(precision["step_size"])
        d_size = Decimal(str(size))
        rounded = (d_size / step).to_integral_value(rounding=ROUND_DOWN) * step
        return float(rounded)

    def _round_price(self, coin: str, price: float) -> float:
        symbol = self._to_symbol(coin)
        precision = self._get_precision(symbol)
        tick = Decimal(precision["tick_size"])
        d_price = Decimal(str(price))
        rounded = (d_price / tick).to_integral_value(rounding=ROUND_DOWN) * tick
        return float(rounded)


# ═══════════════════════════════════════════════════════════════════════════════
# Section 7: VarFunding Scanner
# ═══════════════════════════════════════════════════════════════════════════════

CONFIDENCE_LEVELS = {"high": 3, "medium": 2, "low": 1}
TARGET_EXCHANGES = {"hyperliquid", "binance"}


class VarFundingScanner:
    API_URL = "https://varfunding.xyz/api/funding"
    TIMEOUT = 15

    def __init__(
        self,
        min_apr: float = 10.0,
        min_confidence: str = "medium",
        stability_threshold: float = 0.3,
    ):
        self.min_apr = min_apr
        self.min_confidence_level = CONFIDENCE_LEVELS.get(min_confidence, 2)
        self.stability_threshold = stability_threshold

    def fetch_opportunities(
        self,
        exchanges: tuple[str, str] = ("hyperliquid", "binance"),
    ) -> list[dict]:
        """Fetch and filter arbitrage opportunities from VarFunding API."""
        resp = requests.get(
            self.API_URL,
            params={"exchanges": ",".join(exchanges)},
            timeout=self.TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()

        exchange_set = set(exchanges)
        results: list[dict] = []

        for market in data.get("markets", []):
            arb = market.get("arbitrageOpportunity")
            if not arb:
                continue

            long_ex = arb.get("longExchange", "")
            short_ex = arb.get("shortExchange", "")

            if long_ex not in exchange_set or short_ex not in exchange_set:
                continue

            confidence = arb.get("confidence", "low")
            if CONFIDENCE_LEVELS.get(confidence, 0) < self.min_confidence_level:
                continue

            estimated_apr = arb.get("estimatedApr", 0.0)
            if estimated_apr < self.min_apr:
                continue

            rate_map: dict[str, float] = {}
            var = market.get("variational")
            if var and var.get("exchange") in exchange_set:
                rate_map[var["exchange"]] = var.get("rate", 0.0)
            for comp in market.get("comparisons", []):
                if comp.get("exchange") in exchange_set:
                    rate_map[comp["exchange"]] = comp.get("rate", 0.0)

            results.append(
                {
                    "coin": market.get("baseAsset", ""),
                    "long_exchange": long_ex,
                    "short_exchange": short_ex,
                    "spread": arb.get("spread", 0.0),
                    "estimated_apr": estimated_apr,
                    "confidence": confidence,
                    "hl_rate": rate_map.get("hyperliquid", 0.0),
                    "bn_rate": rate_map.get("binance", 0.0),
                }
            )

        results.sort(key=lambda x: x["estimated_apr"], reverse=True)

        # Filter high-APR opportunities for notification
        hot = [r for r in results if r["estimated_apr"] >= 20.0]

        emit(
            "varfunding_scan",
            {
                "count": len(results),
                "top_5": [
                    {"coin": r["coin"], "apr": round(r["estimated_apr"], 1)}
                    for r in results[:5]
                ],
            },
        )

        if hot:
            emit(
                "opportunity_alert",
                {
                    "count": len(hot),
                    "opportunities": [
                        {
                            "coin": r["coin"],
                            "apr": round(r["estimated_apr"], 1),
                            "spread": round(r["spread"], 6),
                            "long": r["long_exchange"],
                            "short": r["short_exchange"],
                        }
                        for r in hot[:5]
                    ],
                },
                tier="opportunity_alert",
            )

        return results

    def check_stability(self, snapshots: list[dict]) -> dict:
        """Analyze multiple snapshots for rate stability."""
        count = len(snapshots)
        if count < 3:
            return {
                "stable": False,
                "count": count,
                "avg_spread": 0.0,
                "std_spread": 0.0,
                "std_ratio": 0.0,
            }

        spreads = [s["spread"] for s in snapshots]
        avg_spread = statistics.mean(spreads)
        std_spread = statistics.stdev(spreads)

        if avg_spread == 0:
            std_ratio = float("inf")
        else:
            std_ratio = std_spread / abs(avg_spread)

        return {
            "stable": std_ratio < self.stability_threshold,
            "count": count,
            "avg_spread": avg_spread,
            "std_spread": std_spread,
            "std_ratio": std_ratio,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Section 8: CrossFundingEngine
# ═══════════════════════════════════════════════════════════════════════════════

STATE_NAME = "cross_funding"


def _is_order_error(result: dict) -> bool:
    """Check if order result is an error. Compatible with HL and Binance formats."""
    if result.get("status") in ("error", "err"):
        return True
    try:
        s = result["response"]["data"]["statuses"][0]
        return "error" in s
    except (KeyError, IndexError, TypeError):
        pass
    if "code" in result and int(result.get("code", 0)) < 0:
        return True
    return False


class CrossFundingEngine:
    def __init__(
        self,
        hl_client: HLClient,
        bn_client: BinanceClient,
        scanner: VarFundingScanner,
        cfg: dict,
    ) -> None:
        self.hl = hl_client
        self.bn = bn_client
        self.scanner = scanner
        self.cfg = cfg
        self.hl_budget_cfg: float = cfg.get("hl_budget_usd", 0)
        self.bn_budget_cfg: float = cfg.get("bn_budget_usd", 0)
        self.leverage: int = cfg.get("leverage", 1)
        self.min_apr: float = cfg["min_apr_pct"]
        self.min_hold_apr: float = cfg.get("min_hold_apr_pct", self.min_apr)
        self.stability_snapshots: int = cfg.get("stability_snapshots", 3)
        self.close_spread_threshold: float = cfg.get("close_spread_threshold", 0.0001)
        self.switch_threshold_apr: float = cfg.get("switch_threshold_apr", 5.0)
        self.max_breakeven_days: float = cfg.get("max_breakeven_days", 3.0)
        self.max_price_basis_pct: float = cfg.get("max_price_basis_pct", 0.3)
        self.max_entry_breakeven_days: float = cfg.get("max_entry_breakeven_days", 5.0)
        self.round_trip_cost_pct: float = cfg.get("round_trip_cost_pct", 0.12)
        self.max_positions: int = cfg.get("max_positions", 3)
        self.min_position_usd: float = cfg.get("min_position_usd", 50)

        # PnL stop-loss and minimum hold time
        self.pnl_stop_loss_pct: float = cfg.get("pnl_stop_loss_pct", -1.0)
        self.min_hold_ticks: int = cfg.get("min_hold_ticks", 96)

        # Delta-aware exit parameters
        delta_exit_cfg = cfg.get("delta_exit", {})
        self.delta_exit_enabled: bool = delta_exit_cfg.get("enabled", True)
        # Delta % below which we consider the position "neutral" (safe to close)
        self.delta_neutral_threshold_pct: float = delta_exit_cfg.get("neutral_threshold_pct", 2.0)
        # Max ticks to wait for favorable delta before force-closing (12 × 5min = 1h)
        self.delta_max_defer_ticks: int = delta_exit_cfg.get("max_defer_ticks", 12)
        # Force close if delta exceeds this regardless of PnL
        self.delta_force_close_pct: float = delta_exit_cfg.get("force_close_delta_pct", 15.0)

    # ---- State management ----

    def _load(self) -> dict:
        state = load_state(STATE_NAME)
        # Migrate v1 → v2
        if "current_coin" in state and "positions" not in state:
            coin = state.pop("current_coin", None)
            positions: list[dict] = []
            if coin:
                pos = {
                    "coin": coin,
                    "direction": state.pop("direction", {}),
                    "size": state.pop("size", 0),
                    "entry_price": state.pop("entry_price", 0),
                    "entry_time": state.pop("entry_time", ""),
                    "entry_spread": state.pop("entry_spread", 0),
                    "total_funding_earned": state.pop("total_funding_earned", 0),
                }
                positions.append(pos)
            # Clean up other v1 fields that are now per-position
            for k in ["entry_hl_rate", "entry_bn_rate", "budget_hl", "budget_bn",
                       "entry_hl_balance", "entry_bn_balance"]:
                state.pop(k, None)
            state["positions"] = positions
            state["version"] = 2
            self._save(state)
        return state

    def _save(self, state: dict) -> None:
        state["last_tick"] = datetime.now(timezone.utc).isoformat()
        save_state(STATE_NAME, state)

    def _get_budgets(self) -> tuple[float, float]:
        """Return (hl_budget, bn_budget). If config is 0, read actual balance."""
        hl = (
            self.hl_budget_cfg if self.hl_budget_cfg > 0 else self.hl.get_usdc_balance()
        )
        bn = (
            self.bn_budget_cfg if self.bn_budget_cfg > 0 else self.bn.get_usdt_balance()
        )
        return hl, bn

    def _get_positions(self) -> list[dict]:
        return self._load().get("positions", [])

    def _get_position_by_coin(self, coin: str) -> dict | None:
        for p in self._get_positions():
            if p["coin"] == coin:
                return p
        return None

    def _occupied_coins(self) -> set[str]:
        return {p["coin"] for p in self._get_positions()}

    def _get_available_budgets(self) -> tuple[float, float]:
        """Return available (not margin-locked) balance per exchange."""
        hl_total = self.hl.get_usdc_balance()
        bn_total = self.bn.get_usdt_balance()
        positions = self._get_positions()

        # Calculate used margin per exchange
        hl_used = 0.0
        bn_used = 0.0
        for pos in positions:
            direction = pos.get("direction", {})
            notional = pos.get("size", 0) * pos.get("entry_price", 0)
            margin = notional / self.leverage if self.leverage > 0 else notional
            if direction.get("long_exchange") == "hyperliquid":
                hl_used += margin
                bn_used += margin
            else:
                bn_used += margin
                hl_used += margin

        hl_available = max(hl_total - hl_used * 1.1, 0)  # 10% safety buffer
        bn_available = max(bn_total - bn_used * 1.1, 0)
        return hl_available, bn_available

    # ---- Client routing ----

    def _get_client(self, exchange: str) -> HLClient | BinanceClient:
        if exchange == "hyperliquid":
            return self.hl
        return self.bn

    def _get_mid_price(self, exchange: str, coin: str) -> float:
        return self._get_client(exchange).get_mid_price(coin)

    def _get_funding_rate(self, exchange: str, coin: str) -> float:
        return self._get_client(exchange).get_funding_rate(coin)

    # ---- Scanning ----

    def scan_opportunities(self) -> list[dict]:
        return self.scanner.fetch_opportunities()

    def record_snapshot(self, opportunities: list[dict]) -> None:
        state = self._load()
        snapshots = state.get("rate_snapshots", [])

        now = datetime.now(timezone.utc).isoformat()
        for opp in opportunities[:5]:
            snapshots.append(
                {
                    "ts": now,
                    "coin": opp["coin"],
                    "spread": opp["spread"],
                    "estimated_apr": opp["estimated_apr"],
                    "long_exchange": opp["long_exchange"],
                    "short_exchange": opp["short_exchange"],
                }
            )

        state["rate_snapshots"] = snapshots[-20:]
        self._save(state)

    def get_stable_opportunity(self) -> dict | None:
        state = self._load()
        snapshots = state.get("rate_snapshots", [])
        if not snapshots:
            return None

        by_coin: dict[str, list[dict]] = {}
        for s in snapshots:
            coin = s["coin"]
            by_coin.setdefault(coin, []).append(s)

        best: dict | None = None
        best_apr = 0.0

        for coin, coin_snaps in by_coin.items():
            stability = self.scanner.check_stability(coin_snaps)
            if not stability["stable"]:
                continue

            latest = coin_snaps[-1]
            apr = latest.get("estimated_apr", 0.0)
            if apr > best_apr:
                best_apr = apr
                best = latest

        return best

    # ---- Deep verification ----

    def verify_opportunity(self, coin: str, direction: dict) -> dict:
        long_ex = direction["long_exchange"]
        short_ex = direction["short_exchange"]

        hl_rate = self.hl.get_funding_rate(coin)
        bn_rate = self.bn.get_funding_rate(coin)
        hl_price = self.hl.get_mid_price(coin)
        bn_price = self.bn.get_mid_price(coin)

        rate_map = {"hyperliquid": hl_rate, "binance": bn_rate}
        actual_spread = rate_map[short_ex] - rate_map[long_ex]

        avg_price = (hl_price + bn_price) / 2
        price_basis_pct = abs(hl_price - bn_price) / avg_price * 100 if avg_price else 0

        gross_annual = actual_spread * 3 * 365 * 100

        # Entry cost = trading fees + price basis (cross-exchange slippage)
        total_entry_cost_pct = self.round_trip_cost_pct + price_basis_pct
        # Daily funding income as % of notional
        daily_funding_pct = actual_spread * 3 * 100
        # Days needed for funding to recover all entry costs
        breakeven_days = total_entry_cost_pct / daily_funding_pct if daily_funding_pct > 0 else float("inf")
        # Net APR after amortizing entry cost over expected 30-day hold
        net_apr = gross_annual - total_entry_cost_pct / 30 * 365

        max_breakeven = getattr(self, "max_entry_breakeven_days", 5.0)
        reject_reason = None
        if actual_spread <= 0:
            reject_reason = f"spread non-positive: {actual_spread:.6f}"
        elif price_basis_pct > self.max_price_basis_pct:
            reject_reason = f"price basis too large: {price_basis_pct:.2f}%"
        elif breakeven_days > max_breakeven:
            reject_reason = (
                f"breakeven {breakeven_days:.1f}d > {max_breakeven}d "
                f"(basis={price_basis_pct:.2f}% + fees={self.round_trip_cost_pct:.2f}% "
                f"= {total_entry_cost_pct:.2f}%, daily={daily_funding_pct:.3f}%)"
            )
        elif net_apr < self.min_apr:
            reject_reason = f"net APR too low: {net_apr:.1f}%"

        result = {
            "valid": reject_reason is None,
            "hl_rate": hl_rate,
            "bn_rate": bn_rate,
            "actual_spread": actual_spread,
            "hl_price": hl_price,
            "bn_price": bn_price,
            "price_basis_pct": round(price_basis_pct, 4),
            "total_entry_cost_pct": round(total_entry_cost_pct, 4),
            "breakeven_days": round(breakeven_days, 1) if breakeven_days < 999 else None,
            "round_trip_cost_pct": self.round_trip_cost_pct,
            "net_apr_after_costs": round(net_apr, 2),
            "reject_reason": reject_reason,
        }

        emit("verify_opportunity", {"coin": coin, **result})
        return result

    # ---- Open position ----

    def _calculate_size(self, budget_per_exchange: float, price: float) -> float:
        if price <= 0:
            return 0.0
        effective = budget_per_exchange * 0.95
        return effective * self.leverage / price

    def open_position(self, coin: str, direction: dict) -> bool:
        """Atomic open: HL leg first (stricter limits), then Binance. Rollback on failure.

        HL tiered margin is strict for small coins; auto-halves size on retry (max 3x).
        Multi-position: appends to positions array. Checks duplicates and max slots.
        """
        state = self._load()
        positions = state.get("positions", [])

        # Guard: duplicate coin
        occupied = {p["coin"] for p in positions}
        if coin in occupied:
            emit(
                "warn",
                {"msg": f"already has position in {coin}, skip open"},
            )
            return False

        # Guard: max positions
        if len(positions) >= self.max_positions:
            emit(
                "warn",
                {"msg": f"max positions ({self.max_positions}) reached, skip open"},
            )
            return False

        long_ex = direction["long_exchange"]
        short_ex = direction["short_exchange"]

        hl_is_long = long_ex == "hyperliquid"
        hl_side = "long" if hl_is_long else "short"
        bn_side = "short" if hl_is_long else "long"

        price = self.hl.get_mid_price(coin)
        if price <= 0:
            emit_error("price", RuntimeError(f"invalid price for {coin}: {price}"))
            return False

        # Use available budgets (account for existing positions' margin)
        hl_available, bn_available = self._get_available_budgets()
        budget = min(hl_available, bn_available)

        # Guard: minimum budget
        if budget < self.min_position_usd:
            emit(
                "warn",
                {"msg": f"available budget ${budget:.0f} < min ${self.min_position_usd:.0f}, skip open"},
            )
            return False

        conservative = budget * 0.8
        raw_size = self._calculate_size(conservative, price)

        hl_rounded = self.hl.round_size(coin, raw_size)
        bn_rounded = self.bn.round_size(coin, raw_size)
        size = min(hl_rounded, bn_rounded)
        if size <= 0:
            emit_error("calc_size", RuntimeError(f"size=0 for {coin}"))
            return False

        emit(
            "open_sizing",
            {
                "coin": coin,
                "budget": budget,
                "conservative_budget": conservative,
                "price": price,
                "raw_size": raw_size,
                "final_size": size,
                "notional": round(size * price, 2),
                "position_slot": len(positions) + 1,
                "max_positions": self.max_positions,
            },
        )

        # 1) Set leverage on both exchanges
        try:
            self.hl.set_leverage(coin, self.leverage, cross=True)
        except Exception as e:
            emit_error("set_leverage_hl", e)
        try:
            self.bn.set_leverage(coin, self.leverage)
        except Exception as e:
            emit_error("set_leverage_bn", e)

        # 2) HL leg first (stricter, lower failure cost)
        arb_slippage = 0.001
        hl_is_buy = hl_is_long
        hl_result = None
        for attempt in range(4):
            try:
                hl_result = self.hl.market_order(
                    coin, is_buy=hl_is_buy, size=size, slippage=arb_slippage
                )
                if not _is_order_error(hl_result):
                    break
                err_msg = str(hl_result)
                if "Insufficient margin" in err_msg and attempt < 3:
                    size = self.hl.round_size(coin, size * 0.5)
                    size = min(size, self.bn.round_size(coin, size))
                    if size <= 0 or size * price < 10:
                        emit(
                            "size_retry",
                            {
                                "coin": coin,
                                "abort": True,
                                "reason": "size too small after halving",
                            },
                        )
                        break
                    emit(
                        "size_retry",
                        {
                            "coin": coin,
                            "attempt": attempt + 1,
                            "new_size": size,
                            "new_notional": round(size * price, 2),
                        },
                    )
                    continue
                break
            except Exception as e:
                emit_error(f"hl_{hl_side}_order", e)
                return False

        if hl_result is None or _is_order_error(hl_result):
            emit_error(
                f"hl_{hl_side}_order",
                RuntimeError(f"HL order failed after retries: {hl_result}"),
            )
            return False
        time.sleep(1)

        # 3) Binance leg (using HL's actual filled size)
        bn_is_buy = not hl_is_long
        bn_size = self.bn.round_size(coin, size)
        try:
            bn_result = self.bn.market_order(
                coin, is_buy=bn_is_buy, size=bn_size, slippage=arb_slippage
            )
            if _is_order_error(bn_result):
                emit_error(
                    f"bn_{bn_side}_order",
                    RuntimeError(f"BN order failed: {bn_result}"),
                )
                emit("rollback", {"reason": "BN leg failed", "coin": coin})
                try:
                    self.hl.close_position(coin)
                except Exception as re:
                    emit_error("rollback_hl", re, notify=True)
                return False
        except Exception as e:
            emit_error(f"bn_{bn_side}_order", e)
            emit("rollback", {"reason": "BN leg failed", "coin": coin})
            try:
                self.hl.close_position(coin)
            except Exception as re:
                emit_error("rollback_hl", re, notify=True)
            return False
        time.sleep(2)

        # Verify both legs are filled before saving state
        hl_pos = self.hl.get_position(coin)
        bn_pos = self.bn.get_position(coin)
        hl_filled = abs(hl_pos["size"]) if hl_pos else 0
        bn_filled = abs(bn_pos["size"]) if bn_pos else 0

        if hl_filled == 0 or bn_filled == 0:
            missing = "HL" if hl_filled == 0 else "BN"
            emit_error(
                "position_verify",
                RuntimeError(
                    f"leg verification failed: {missing} has no position "
                    f"(HL={hl_filled}, BN={bn_filled})"
                ),
                notify=True,
            )
            # Rollback: close whichever leg exists
            if hl_filled > 0:
                try:
                    self.hl.close_position(coin)
                except Exception as re:
                    emit_error("rollback_hl", re, notify=True)
            if bn_filled > 0:
                try:
                    self.bn.close_position(coin)
                except Exception as re:
                    emit_error("rollback_bn", re, notify=True)
            return False

        # Check delta — tolerate up to 10% size mismatch
        avg_size = (hl_filled + bn_filled) / 2
        delta_pct = abs(hl_filled - bn_filled) / avg_size * 100 if avg_size else 0
        if delta_pct > 10:
            emit(
                "position_verify_warn",
                {
                    "coin": coin,
                    "hl_size": hl_filled,
                    "bn_size": bn_filled,
                    "delta_pct": round(delta_pct, 2),
                    "msg": "size mismatch >10%, closing both legs",
                },
                notify=True,
                tier="risk_alert",
            )
            try:
                self.hl.close_position(coin)
            except Exception as re:
                emit_error("rollback_hl", re, notify=True)
            try:
                self.bn.close_position(coin)
            except Exception as re:
                emit_error("rollback_bn", re, notify=True)
            return False

        # Use verified size (smaller of the two, in case of rounding diffs)
        size = min(hl_filled, bn_filled)

        # Save state — append to positions array
        hl_rate = self.hl.get_funding_rate(coin)
        bn_rate = self.bn.get_funding_rate(coin)

        now_iso = datetime.now(timezone.utc).isoformat()

        new_pos = {
            "coin": coin,
            "direction": direction,
            "entry_time": now_iso,
            "entry_spread": abs(hl_rate - bn_rate),
            "entry_hl_rate": hl_rate,
            "entry_bn_rate": bn_rate,
            "size": size,
            "entry_price": price,
            "total_funding_earned": 0.0,
        }

        # Re-load state to avoid race; append position
        state = self._load()
        positions = state.get("positions", [])
        positions.append(new_pos)
        state["positions"] = positions
        state["version"] = 2

        # Strategy-level fields (set once on first open)
        if not state.get("strategy_start_time"):
            state["strategy_start_time"] = now_iso
        if not state.get("entry_total_balance"):
            entry_hl_balance = self.hl.get_usdc_balance()
            entry_bn_balance = self.bn.get_usdt_balance()
            state["entry_total_balance"] = round(entry_hl_balance + entry_bn_balance, 2)

        state["rate_snapshots"] = state.get("rate_snapshots", [])
        self._save(state)

        emit(
            "position_opened",
            {
                "coin": coin,
                "size": size,
                "long_exchange": long_ex,
                "short_exchange": short_ex,
                "leverage": self.leverage,
                "entry_price": price,
                "hl_rate": hl_rate,
                "bn_rate": bn_rate,
                "position_count": len(positions),
            },
            notify=True,
            tier="trade_alert",
        )
        return True

    # ---- Close position ----

    def _verify_leg_closed(self, client, coin: str) -> bool:
        """Check that a position on the given exchange is actually closed."""
        try:
            pos = client.get_position(coin)
            if pos and abs(pos.get("size", 0)) > 0:
                return False
            return True
        except Exception as e:
            emit_error("verify_leg_closed", e)
            return False

    def close_position(self, coin: str) -> bool:
        state = self._load()
        positions = state.get("positions", [])

        # Find the position for this coin
        pos_data = None
        pos_idx = -1
        for i, p in enumerate(positions):
            if p["coin"] == coin:
                pos_data = p
                pos_idx = i
                break

        if pos_data is None:
            emit("warn", {"msg": f"no position found for {coin}, skip close"})
            return False

        direction = pos_data.get("direction", {})
        long_ex = direction.get("long_exchange", "hyperliquid")
        short_ex = direction.get("short_exchange", "binance")
        long_client = self._get_client(long_ex)
        short_client = self._get_client(short_ex)

        # Capture pre-close balances for per-position PnL estimate
        pre_hl = self.hl.get_usdc_balance()
        pre_bn = self.bn.get_usdt_balance()

        short_ok = False
        long_ok = False

        try:
            short_client.close_position(coin)
        except Exception as e:
            emit_error("close_short", e)
        time.sleep(1)
        short_ok = self._verify_leg_closed(short_client, coin)

        try:
            long_client.close_position(coin)
        except Exception as e:
            emit_error("close_long", e)
        time.sleep(1)
        long_ok = self._verify_leg_closed(long_client, coin)

        if not short_ok or not long_ok:
            failed_legs = []
            if not short_ok:
                failed_legs.append(f"short({short_ex})")
            if not long_ok:
                failed_legs.append(f"long({long_ex})")
            emit(
                "close_incomplete",
                {
                    "coin": coin,
                    "failed_legs": failed_legs,
                    "short_closed": short_ok,
                    "long_closed": long_ok,
                },
                notify=True,
                tier="risk_alert",
            )
            # Do NOT remove from state — position needs manual intervention
            # or will be retried on next tick
            return False

        funding_earned = pos_data.get("total_funding_earned", 0.0)
        current_price = self.hl.get_mid_price(coin)

        # Per-position PnL: balance change from closing this specific position
        post_hl = self.hl.get_usdc_balance()
        post_bn = self.bn.get_usdt_balance()
        pnl = round((post_hl + post_bn) - (pre_hl + pre_bn), 2)

        emit(
            "position_closed",
            {
                "coin": coin,
                "long_exchange": long_ex,
                "short_exchange": short_ex,
                "funding_earned": funding_earned,
                "pnl": pnl,
                "remaining_positions": len(positions) - 1,
            },
            notify=True,
            tier="trade_alert",
        )

        log_trade(
            "close", coin, direction,
            size=pos_data.get("size", 0),
            entry_price=pos_data.get("entry_price", 0),
            exit_price=current_price,
            pnl=pnl,
            funding_pnl=round(funding_earned, 2),
            reason=f"funding earned: {funding_earned:.2f}",
        )

        # Remove position from array (do NOT clear entire state)
        positions.pop(pos_idx)
        state["positions"] = positions
        self._save(state)
        return True

    # ---- Reconciliation ----

    def reconcile_positions(self) -> list[dict]:
        """Compare state positions vs actual exchange positions.

        Returns a list of orphan positions (on-exchange but not in state).
        Emits risk_alert for each orphan found.
        """
        state_coins = {p["coin"] for p in self._get_positions()}

        orphans: list[dict] = []
        for exchange_name, client in [("hyperliquid", self.hl), ("binance", self.bn)]:
            try:
                actual = client.get_all_positions()
            except Exception as e:
                emit_error(f"reconcile_{exchange_name}", e)
                continue
            for pos in actual:
                if pos["coin"] not in state_coins:
                    orphan = {
                        "coin": pos["coin"],
                        "exchange": exchange_name,
                        "size": pos["size"],
                        "unrealized_pnl": pos.get("unrealized_pnl", 0),
                    }
                    orphans.append(orphan)
                    emit(
                        "orphan_position",
                        orphan,
                        notify=True,
                        tier="risk_alert",
                    )
        return orphans

    # ---- Health check ----

    def _check_position_health(self, pos_data: dict) -> dict:
        """Check health of a single position. Returns per-position health dict."""
        coin = pos_data["coin"]
        direction = pos_data.get("direction", {})
        long_ex = direction.get("long_exchange", "hyperliquid")
        short_ex = direction.get("short_exchange", "binance")
        long_client = self._get_client(long_ex)
        short_client = self._get_client(short_ex)

        long_pos = long_client.get_position(coin)
        short_pos = short_client.get_position(coin)

        long_size = abs(long_pos["size"]) if long_pos else 0.0
        short_size = abs(short_pos["size"]) if short_pos else 0.0

        # Notional-based delta: use each exchange's mark price to get USD exposure
        long_mark_px = long_pos.get("mark_px", 0.0) if long_pos else 0.0
        short_mark_px = short_pos.get("mark_px", 0.0) if short_pos else 0.0
        long_notional = long_size * long_mark_px if long_mark_px > 0 else 0.0
        short_notional = short_size * short_mark_px if short_mark_px > 0 else 0.0
        avg_notional = (long_notional + short_notional) / 2 if (long_notional + short_notional) > 0 else 1
        delta_notional = abs(long_notional - short_notional)
        delta_pct = delta_notional / avg_notional * 100

        hl_rate = self.hl.get_funding_rate(coin)
        bn_rate = self.bn.get_funding_rate(coin)
        rate_map = {"hyperliquid": hl_rate, "binance": bn_rate}
        current_spread = rate_map[short_ex] - rate_map[long_ex]
        current_apr = current_spread * 3 * 365 * 100

        spread_favorable = current_spread > self.close_spread_threshold
        has_both_legs = long_size > 0 and short_size > 0

        # PnL stop-loss: compute unrealized PnL as % of notional
        long_pnl = long_pos.get("unrealized_pnl", 0.0) if long_pos else 0.0
        short_pnl = short_pos.get("unrealized_pnl", 0.0) if short_pos else 0.0
        funding_earned = pos_data.get("total_funding_earned", 0.0)
        total_pnl_usd = long_pnl + short_pnl + funding_earned
        pnl_pct = total_pnl_usd / avg_notional * 100 if avg_notional > 1 else 0.0
        pnl_stop_triggered = pnl_pct < self.pnl_stop_loss_pct

        # Min hold time: count ticks since entry
        entry_time_str = pos_data.get("entry_time", "")
        hold_ticks = 0
        if entry_time_str:
            try:
                entry_dt = datetime.fromisoformat(entry_time_str)
                elapsed_s = (datetime.now(timezone.utc) - entry_dt).total_seconds()
                hold_ticks = int(elapsed_s / 300)  # 5 min per tick
            except (ValueError, TypeError):
                pass
        within_min_hold = hold_ticks < self.min_hold_ticks

        healthy = has_both_legs and spread_favorable and delta_pct < 20 and not pnl_stop_triggered

        result = {
            "coin": coin,
            "healthy": healthy,
            "long_exchange": long_ex,
            "short_exchange": short_ex,
            "long_size": long_size,
            "short_size": short_size,
            "long_mark_px": long_mark_px,
            "short_mark_px": short_mark_px,
            "delta_pct": round(delta_pct, 2),
            "delta_notional_usd": round(delta_notional, 4),
            "current_spread": current_spread,
            "current_apr": round(current_apr, 2),
            "spread_favorable": spread_favorable,
            "has_both_legs": has_both_legs,
            "hl_rate": hl_rate,
            "bn_rate": bn_rate,
            "pnl_pct": round(pnl_pct, 4),
            "pnl_stop_triggered": pnl_stop_triggered,
            "total_pnl_usd": round(total_pnl_usd, 4),
            "hold_ticks": hold_ticks,
            "within_min_hold": within_min_hold,
        }

        if not healthy:
            emit("health_warning", result, notify=True, tier="risk_alert")

        return result

    def _assess_delta_for_exit(self, pos_data: dict, health: dict) -> dict:
        """Assess whether delta conditions are favorable for closing a position.

        Weighs three cost components:
          1. Trading cost (fixed, incurred on close regardless of timing)
          2. Delta PnL (variable, depends on when we close)
          3. Funding bleed (ongoing cost of holding an unfavorable-spread position)

        If the adverse delta PnL is smaller than the funding we'd lose by
        waiting one more tick, deferring is not worth it — close now.

        Returns a dict with:
          - favorable: bool — True if delta state is good for exit
          - reason: str — human-readable reason
          - delta_pnl_usd: float — signed PnL from delta drift
          - trading_cost_usd: float — one-way trading cost to close
          - funding_bleed_per_tick: float — funding loss per tick if spread unfavorable
          - net_exit_cost_usd: float — trading_cost - delta_pnl (lower is better)
          - signed_delta_pct: float — positive = net long exposure
          - should_force: bool — True if delta is dangerously high
          - defer_count: int — how many times we've already deferred
        """
        coin = pos_data["coin"]
        entry_price = pos_data.get("entry_price", 0.0)
        long_size = health.get("long_size", 0.0)
        short_size = health.get("short_size", 0.0)

        # Use each exchange's mark price for notional-based delta
        long_mark_px = health.get("long_mark_px", 0.0)
        short_mark_px = health.get("short_mark_px", 0.0)
        current_price = self.hl.get_mid_price(coin)
        # Fallback to mid price if mark prices unavailable
        if long_mark_px <= 0:
            long_mark_px = current_price
        if short_mark_px <= 0:
            short_mark_px = current_price

        long_notional = long_size * long_mark_px
        short_notional = short_size * short_mark_px
        avg_notional = (long_notional + short_notional) / 2 if (long_notional + short_notional) > 0 else 1

        # Signed delta in notional USD: positive = net long exposure
        signed_delta_notional = long_notional - short_notional
        signed_delta_pct = signed_delta_notional / avg_notional * 100 if avg_notional else 0
        abs_delta_pct = abs(signed_delta_pct)

        # Delta PnL: actual unrealized PnL difference between the two legs
        # This captures the real USD impact of the delta drift
        long_pnl = (long_mark_px - entry_price) * long_size if long_size > 0 else 0
        short_pnl = (entry_price - short_mark_px) * short_size if short_size > 0 else 0
        delta_pnl_usd = long_pnl + short_pnl

        # Trading cost: notional × round_trip_cost_pct / 100 (one-way close)
        notional = avg_notional
        trading_cost_usd = notional * (self.round_trip_cost_pct / 100) / 2  # half of round-trip

        # Funding bleed per tick: how much we lose per 5-min tick when spread
        # is unfavorable. Spread is per 8h settlement, tick is 5 min.
        # bleed = |spread| × notional × (5min / 480min)
        current_spread = health.get("current_spread", 0.0)
        tick_minutes = 5.0
        bleed_per_tick = abs(current_spread) * notional * (tick_minutes / 480.0)

        # Pending funding: unrealized funding that would be forfeited if we
        # close before the next settlement. Binance settles every 8h
        # (00:00/08:00/16:00 UTC), Hyperliquid settles every 1h.
        direction = pos_data.get("direction", {})
        long_ex = direction.get("long_exchange", "hyperliquid")
        hl_rate = health.get("hl_rate", 0.0)
        bn_rate = health.get("bn_rate", 0.0)
        now = datetime.now(timezone.utc)

        bn_elapsed_h = (now.hour % 8) + now.minute / 60
        bn_fraction = bn_elapsed_h / 8.0
        hl_elapsed_m = now.minute + now.second / 60
        hl_fraction = hl_elapsed_m / 60.0

        # Pending funding for each leg (positive = we earn, negative = we pay)
        # For the short leg, we earn when rate > 0 (longs pay shorts)
        # For the long leg, we earn when rate < 0 (shorts pay longs)
        if long_ex == "binance":
            bn_pending = -bn_rate * bn_fraction * notional  # long BN: earn when rate < 0
            hl_pending = hl_rate * hl_fraction * notional   # short HL: earn when rate > 0
        else:
            hl_pending = -hl_rate * hl_fraction * notional  # long HL: earn when rate < 0
            bn_pending = bn_rate * bn_fraction * notional   # short BN: earn when rate > 0

        pending_funding_usd = bn_pending + hl_pending

        # Net exit cost = trading_cost - delta_pnl + forfeited_funding
        # - trading_cost: always paid on close
        # - delta_pnl: positive reduces cost, negative increases cost
        # - pending_funding: if positive, we forfeit earnings by closing now;
        #                    if negative, we avoid paying by closing now
        forfeited_funding = max(pending_funding_usd, 0.0)
        avoided_payment = max(-pending_funding_usd, 0.0)
        net_exit_cost_usd = trading_cost_usd - delta_pnl_usd + forfeited_funding - avoided_payment

        # Track how many times this position has been deferred
        defer_count = pos_data.get("delta_exit_defer_count", 0)

        # Cumulative bleed already lost from prior deferrals
        cumulative_bleed = bleed_per_tick * defer_count

        # Time until next settlement for each exchange
        bn_remaining_h = 8.0 - bn_elapsed_h
        bn_remaining_ticks = bn_remaining_h * 60 / tick_minutes
        hl_remaining_m = 60.0 - hl_elapsed_m
        hl_remaining_ticks = hl_remaining_m / tick_minutes
        # Use the nearest settlement that has positive pending
        nearest_remaining_ticks = min(
            bn_remaining_ticks if bn_pending > 0 else float("inf"),
            hl_remaining_ticks if hl_pending > 0 else float("inf"),
        )
        nearest_remaining_h = min(
            bn_remaining_h if bn_pending > 0 else float("inf"),
            hl_remaining_m / 60 if hl_pending > 0 else float("inf"),
        )

        # Decision logic — ordered by priority
        should_force = abs_delta_pct >= self.delta_force_close_pct
        exceeded_max_defer = defer_count >= self.delta_max_defer_ticks

        if should_force:
            favorable = True
            reason = (
                f"delta {signed_delta_pct:+.2f}% exceeds force-close "
                f"threshold {self.delta_force_close_pct}%"
            )
        elif exceeded_max_defer:
            favorable = True
            reason = (
                f"max defer ticks reached ({defer_count}/{self.delta_max_defer_ticks}), "
                f"delta PnL ${delta_pnl_usd:+.2f}, "
                f"cumulative bleed ${cumulative_bleed:.2f}, "
                f"forfeited funding ${forfeited_funding:.2f}"
            )
        elif forfeited_funding > 0 and nearest_remaining_ticks <= 3:
            # Near settlement with positive pending funding — wait to collect it
            # 3 ticks = 15 min, close enough to just hold on
            favorable = False
            reason = (
                f"settlement in {nearest_remaining_h:.2f}h "
                f"({nearest_remaining_ticks:.0f} ticks), "
                f"pending funding ${pending_funding_usd:+.2f} "
                f"(BN ${bn_pending:+.4f}, HL ${hl_pending:+.4f}) "
                f"would be forfeited, deferring to collect "
                f"(defer {defer_count+1}/{self.delta_max_defer_ticks})"
            )
        elif abs_delta_pct <= self.delta_neutral_threshold_pct:
            # Delta is near zero — ideal exit window
            favorable = True
            reason = (
                f"delta neutral ({signed_delta_pct:+.2f}% within "
                f"±{self.delta_neutral_threshold_pct}%), "
                f"net exit cost ${net_exit_cost_usd:+.2f}"
            )
        elif delta_pnl_usd >= trading_cost_usd + forfeited_funding:
            # Delta PnL covers trading cost + forfeited funding — close and profit
            net_gain = delta_pnl_usd - trading_cost_usd - forfeited_funding
            favorable = True
            reason = (
                f"delta PnL ${delta_pnl_usd:+.2f} covers trading cost "
                f"${trading_cost_usd:.2f} + forfeited funding "
                f"${forfeited_funding:.2f}, net +${net_gain:.2f}"
            )
        elif delta_pnl_usd >= 0:
            # Delta PnL is positive but doesn't fully cover all costs — still OK
            favorable = True
            reason = (
                f"delta PnL ${delta_pnl_usd:+.2f} partially offsets costs "
                f"(trade ${trading_cost_usd:.2f} + forfeit ${forfeited_funding:.2f}), "
                f"net exit cost ${net_exit_cost_usd:.2f}"
            )
        elif bleed_per_tick > 0 and abs(delta_pnl_usd) <= bleed_per_tick:
            # Adverse delta PnL is smaller than one tick of funding bleed —
            # deferring costs more than the delta loss, close now
            favorable = True
            reason = (
                f"adverse delta PnL ${delta_pnl_usd:+.2f} < bleed/tick "
                f"${bleed_per_tick:.4f}, deferring not worth it"
            )
        else:
            # Adverse delta PnL exceeds bleed/tick — worth waiting for recovery
            favorable = False
            remaining_ticks = self.delta_max_defer_ticks - defer_count
            max_total_bleed = bleed_per_tick * remaining_ticks
            reason = (
                f"delta PnL adverse ${delta_pnl_usd:+.2f} > bleed/tick "
                f"${bleed_per_tick:.4f}, deferring "
                f"(delta {signed_delta_pct:+.2f}%, "
                f"defer {defer_count+1}/{self.delta_max_defer_ticks}, "
                f"max bleed if waiting ${max_total_bleed:.2f}, "
                f"pending funding ${pending_funding_usd:+.2f})"
            )

        return {
            "favorable": favorable,
            "reason": reason,
            "delta_pnl_usd": round(delta_pnl_usd, 4),
            "trading_cost_usd": round(trading_cost_usd, 4),
            "pending_funding_usd": round(pending_funding_usd, 4),
            "forfeited_funding_usd": round(forfeited_funding, 4),
            "funding_bleed_per_tick": round(bleed_per_tick, 6),
            "net_exit_cost_usd": round(net_exit_cost_usd, 4),
            "cumulative_bleed_usd": round(cumulative_bleed, 4),
            "signed_delta_pct": round(signed_delta_pct, 2),
            "abs_delta_pct": round(abs_delta_pct, 2),
            "should_force": should_force,
            "defer_count": defer_count,
            "current_price": current_price,
            "entry_price": entry_price,
            "bn_remaining_h": round(bn_remaining_h, 2),
            "hl_remaining_m": round(hl_remaining_m, 2),
            "nearest_settlement_ticks": round(nearest_remaining_ticks, 1),
        }

    def _increment_defer_count(self, coin: str) -> None:
        """Increment the delta exit defer counter for a position in state."""
        state = self._load()
        for pos in state.get("positions", []):
            if pos["coin"] == coin:
                pos["delta_exit_defer_count"] = pos.get("delta_exit_defer_count", 0) + 1
                break
        self._save(state)

    def _reset_defer_count(self, coin: str) -> None:
        """Reset the delta exit defer counter (e.g. when spread becomes favorable again)."""
        state = self._load()
        for pos in state.get("positions", []):
            if pos["coin"] == coin:
                pos.pop("delta_exit_defer_count", None)
                break
        self._save(state)

    def check_health(self) -> dict:
        """Check health for ALL positions. Returns aggregate + per-position health."""
        positions = self._get_positions()
        if not positions:
            return {
                "healthy": True,
                "has_positions": False,
                "position_count": 0,
                "position_health": [],
            }

        position_health = []
        all_healthy = True
        for pos in positions:
            ph = self._check_position_health(pos)
            position_health.append(ph)
            if not ph["healthy"]:
                all_healthy = False

        return {
            "healthy": all_healthy,
            "has_positions": True,
            "position_count": len(positions),
            "position_health": position_health,
        }

    # ---- Position management ----

    def _evaluate_switch_candidate(
        self, coin: str, current_apr: float, health: dict,
        opportunities: list[dict],
    ) -> dict | None:
        """Evaluate if a better opportunity justifies switching out of `coin`.

        Returns the best verified candidate dict or None if no switch warranted.
        Uses time-cost breakeven model with settlement deferral.
        """
        hl_rate = health.get("hl_rate", 0.0)
        bn_rate = health.get("bn_rate", 0.0)
        long_ex = health.get("long_exchange", "binance")

        now = datetime.now(timezone.utc)

        # --- Cost component 1: Trading fees ---
        trading_cost_pct = self.round_trip_cost_pct * 2  # close + open

        # --- Cost component 2: Sunk funding (unrealized since last settlement) ---
        bn_elapsed_h = (now.hour % 8) + now.minute / 60
        bn_fraction = bn_elapsed_h / 8.0
        bn_remaining_h = 8.0 - bn_elapsed_h
        hl_elapsed_m = now.minute + now.second / 60
        hl_fraction = hl_elapsed_m / 60.0
        hl_remaining_m = 60.0 - hl_elapsed_m

        if long_ex == "binance":
            bn_unrealized = -bn_rate * bn_fraction * 100
            hl_unrealized = hl_rate * hl_fraction * 100
        else:
            hl_unrealized = -hl_rate * hl_fraction * 100
            bn_unrealized = bn_rate * bn_fraction * 100

        sunk_cost_pct = bn_unrealized + hl_unrealized

        # --- Cost component 3: Realized price PnL ---
        long_client = self._get_client(long_ex)
        short_ex_name = "binance" if long_ex == "hyperliquid" else "hyperliquid"
        short_client = self._get_client(short_ex_name)
        long_pos = long_client.get_position(coin)
        short_pos = short_client.get_position(coin)

        long_pnl = long_pos.get("unrealized_pnl", 0.0) if long_pos else 0.0
        short_pnl = short_pos.get("unrealized_pnl", 0.0) if short_pos else 0.0
        price_pnl = long_pnl + short_pnl

        long_notional = abs(long_pos["size"]) * long_pos.get("mark_px", 0) if long_pos else 0
        short_notional = abs(short_pos["size"]) * short_pos.get("mark_px", 0) if short_pos else 0
        avg_notional = (long_notional + short_notional) / 2 if (long_notional + short_notional) > 0 else 1
        price_pnl_pct = price_pnl / avg_notional * 100

        total_cost_pct = trading_cost_pct + sunk_cost_pct - price_pnl_pct

        max_breakeven_days = self.max_breakeven_days
        occupied = self._occupied_coins()

        best = None
        best_breakeven = float("inf")
        for opp in opportunities:
            if opp["coin"] == coin or opp["coin"] in occupied:
                continue
            apr_gain = opp["estimated_apr"] - current_apr
            if apr_gain <= 0:
                continue
            daily_gain_pct = apr_gain / 365.0
            if daily_gain_pct > 0:
                quick_breakeven = total_cost_pct / daily_gain_pct
                if quick_breakeven <= max_breakeven_days and quick_breakeven < best_breakeven:
                    best = opp
                    best_breakeven = quick_breakeven

        if not best:
            return None

        # Deep-verify the candidate
        direction = {
            "long_exchange": best["long_exchange"],
            "short_exchange": best["short_exchange"],
        }
        verification = self.verify_opportunity(best["coin"], direction)
        if not verification["valid"]:
            emit(
                "switch_rejected",
                {"from": coin, "to": best["coin"], "reason": verification["reject_reason"]},
            )
            return None

        verified_apr = verification["net_apr_after_costs"]
        apr_gain = verified_apr - current_apr
        if apr_gain <= 0:
            emit(
                "switch_rejected",
                {"from": coin, "to": best["coin"], "reason": f"verified APR gain <= 0: {apr_gain:.1f}%"},
            )
            return None

        daily_gain_pct = apr_gain / 365.0
        breakeven_days = total_cost_pct / daily_gain_pct if daily_gain_pct > 0 else float("inf")

        if breakeven_days > max_breakeven_days:
            emit(
                "switch_rejected",
                {
                    "from": coin, "to": best["coin"],
                    "reason": f"breakeven {breakeven_days:.1f}d > max {max_breakeven_days}d "
                    f"(cost={total_cost_pct:.3f}%, gain={apr_gain:.1f}%/yr, "
                    f"trading={trading_cost_pct:.2f}%, sunk={sunk_cost_pct:.3f}%, "
                    f"price_pnl={price_pnl_pct:.3f}%)",
                },
            )
            return None

        # --- Settlement deferral check ---
        if long_ex == "binance":
            bn_pending = -bn_rate * (1 - bn_fraction) * 100
            hl_pending = hl_rate * (1 - hl_fraction) * 100
        else:
            hl_pending = -hl_rate * (1 - hl_fraction) * 100
            bn_pending = bn_rate * (1 - bn_fraction) * 100

        bn_wait_hours = bn_remaining_h
        bn_funding_gain = bn_pending
        bn_opportunity_cost = apr_gain / 365.0 / 24.0 * bn_wait_hours
        defer_for_bn = bn_funding_gain > 0 and bn_funding_gain > bn_opportunity_cost

        if defer_for_bn:
            emit(
                "switch_deferred",
                {
                    "from": coin, "to": best["coin"],
                    "reason": f"BN settlement in {bn_remaining_h:.1f}h, "
                    f"pending funding {bn_funding_gain:.4f}% > "
                    f"opportunity cost {bn_opportunity_cost:.4f}%",
                    "breakeven_days": round(breakeven_days, 1),
                },
            )
            return None

        return {
            "candidate": best,
            "direction": direction,
            "verified_apr": verified_apr,
            "apr_gain": apr_gain,
            "breakeven_days": breakeven_days,
            "trading_cost_pct": trading_cost_pct,
            "sunk_cost_pct": sunk_cost_pct,
            "price_pnl_pct": price_pnl_pct,
            "total_cost_pct": total_cost_pct,
            "bn_elapsed_h": bn_elapsed_h,
            "hl_elapsed_m": hl_elapsed_m,
        }

    def check_and_manage(self, opportunities: list[dict] | None = None) -> bool:
        """Manage all positions: close unhealthy, open new with idle funds, switch worst.

        Returns True if any action was taken.
        """
        acted = False
        positions = self._get_positions()

        if not positions and not opportunities:
            return False

        # 1) Close unhealthy positions
        for pos in list(positions):
            coin = pos["coin"]
            ph = self._check_position_health(pos)

            # Reset defer counter when spread recovers to favorable
            if ph["spread_favorable"] and pos.get("delta_exit_defer_count", 0) > 0:
                self._reset_defer_count(coin)

            # PnL stop-loss: force close regardless of spread or delta
            if ph["pnl_stop_triggered"]:
                emit(
                    "manage_close",
                    {
                        "coin": coin,
                        "reason": "pnl_stop_loss",
                        "pnl_pct": ph["pnl_pct"],
                        "total_pnl_usd": ph["total_pnl_usd"],
                        "threshold": self.pnl_stop_loss_pct,
                        "hold_ticks": ph["hold_ticks"],
                    },
                    notify=True,
                    tier="risk_alert",
                )
                self._reset_defer_count(coin)
                self.close_position(coin)
                acted = True
                continue

            if not ph["spread_favorable"]:
                # Delta-aware exit: defer close if delta PnL is adverse
                if self.delta_exit_enabled:
                    delta_assessment = self._assess_delta_for_exit(pos, ph)
                    if delta_assessment["favorable"]:
                        emit(
                            "manage_close",
                            {
                                "coin": coin,
                                "reason": "spread unfavorable, delta favorable for exit",
                                "current_spread": ph["current_spread"],
                                "current_apr": ph["current_apr"],
                                "delta_reason": delta_assessment["reason"],
                                "delta_pnl_usd": delta_assessment["delta_pnl_usd"],
                                "signed_delta_pct": delta_assessment["signed_delta_pct"],
                            },
                            notify=True,
                            tier="risk_alert",
                        )
                        self._reset_defer_count(coin)
                        self.close_position(coin)
                        acted = True
                    else:
                        # Defer: delta PnL is adverse, wait for better window
                        self._increment_defer_count(coin)
                        emit(
                            "exit_deferred_delta",
                            {
                                "coin": coin,
                                "reason": delta_assessment["reason"],
                                "delta_pnl_usd": delta_assessment["delta_pnl_usd"],
                                "signed_delta_pct": delta_assessment["signed_delta_pct"],
                                "defer_count": delta_assessment["defer_count"] + 1,
                                "max_defer": self.delta_max_defer_ticks,
                                "current_spread": ph["current_spread"],
                                "current_apr": ph["current_apr"],
                            },
                            notify=True,
                            tier="info",
                        )
                else:
                    # Delta exit disabled — close immediately as before
                    emit(
                        "manage_close",
                        {
                            "coin": coin,
                            "reason": "spread unfavorable",
                            "current_spread": ph["current_spread"],
                            "current_apr": ph["current_apr"],
                        },
                        notify=True,
                        tier="risk_alert",
                    )
                    self.close_position(coin)
                    acted = True
            elif not ph["has_both_legs"]:
                emit(
                    "manage_close",
                    {
                        "coin": coin,
                        "reason": "missing leg",
                        "long_size": ph["long_size"],
                        "short_size": ph["short_size"],
                    },
                    notify=True,
                    tier="risk_alert",
                )
                self.close_position(coin)
                acted = True
            elif ph["current_apr"] < self.min_hold_apr:
                # APR decayed below minimum hold threshold — exit
                if self.delta_exit_enabled:
                    delta_assessment = self._assess_delta_for_exit(pos, ph)
                    if not delta_assessment["favorable"]:
                        self._increment_defer_count(coin)
                        emit(
                            "exit_deferred_delta",
                            {
                                "coin": coin,
                                "reason": f"APR decayed ({ph['current_apr']:.1f}% < "
                                f"{self.min_hold_apr:.1f}%), "
                                + delta_assessment["reason"],
                                "current_apr": ph["current_apr"],
                                "min_hold_apr": self.min_hold_apr,
                                "defer_count": delta_assessment["defer_count"] + 1,
                                "max_defer": self.delta_max_defer_ticks,
                            },
                            notify=True,
                            tier="info",
                        )
                        continue
                emit(
                    "manage_close",
                    {
                        "coin": coin,
                        "reason": "APR decayed below minimum",
                        "current_apr": ph["current_apr"],
                        "min_hold_apr": self.min_hold_apr,
                    },
                    notify=True,
                    tier="risk_alert",
                )
                self.close_position(coin)
                acted = True

        if not opportunities:
            return acted

        # Refresh positions after potential closes
        positions = self._get_positions()
        occupied = {p["coin"] for p in positions}

        # 2) Open new positions with idle funds if below max
        if len(positions) < self.max_positions:
            hl_avail, bn_avail = self._get_available_budgets()
            available_budget = min(hl_avail, bn_avail)

            if available_budget >= self.min_position_usd:
                # Find best opportunity not already held
                for opp in opportunities:
                    if opp["coin"] in occupied:
                        continue
                    if len(self._get_positions()) >= self.max_positions:
                        break

                    direction = {
                        "long_exchange": opp["long_exchange"],
                        "short_exchange": opp["short_exchange"],
                    }
                    verification = self.verify_opportunity(opp["coin"], direction)
                    if not verification["valid"]:
                        continue

                    emit(
                        "manage_open",
                        {
                            "coin": opp["coin"],
                            "apr": verification["net_apr_after_costs"],
                            "direction": direction,
                            "slot": len(self._get_positions()) + 1,
                        },
                    )
                    success = self.open_position(opp["coin"], direction)
                    if success:
                        acted = True
                        occupied.add(opp["coin"])
                        log_trade(
                            "open", opp["coin"], direction,
                            size=self._get_position_by_coin(opp["coin"]).get("size", 0),
                            entry_price=self._get_position_by_coin(opp["coin"]).get("entry_price", 0),
                            reason=f"APR {verification['net_apr_after_costs']:.1f}%",
                        )
                        # Re-check budget for next slot
                        hl_avail, bn_avail = self._get_available_budgets()
                        available_budget = min(hl_avail, bn_avail)
                        if available_budget < self.min_position_usd:
                            break
                    else:
                        break  # Don't keep trying if open failed

            return acted

        # 3) At max positions — try to switch the worst one
        positions = self._get_positions()
        if not positions:
            return acted

        # Find worst position by current APR
        worst_coin = None
        worst_apr = float("inf")
        worst_health = None
        for pos in positions:
            ph = self._check_position_health(pos)
            if ph["current_apr"] < worst_apr:
                worst_apr = ph["current_apr"]
                worst_coin = pos["coin"]
                worst_health = ph

        if worst_coin and worst_health:
            # Min hold time: skip switch if position is too young
            if worst_health.get("within_min_hold", False):
                emit(
                    "switch_skipped_min_hold",
                    {
                        "coin": worst_coin,
                        "hold_ticks": worst_health["hold_ticks"],
                        "min_hold_ticks": self.min_hold_ticks,
                    },
                )
                return acted

            switch = self._evaluate_switch_candidate(
                worst_coin, worst_apr, worst_health, opportunities,
            )
            if switch:
                # Delta-aware exit check before switching
                worst_pos = self._get_position_by_coin(worst_coin)
                if self.delta_exit_enabled and worst_pos:
                    delta_assessment = self._assess_delta_for_exit(worst_pos, worst_health)
                    if not delta_assessment["favorable"]:
                        self._increment_defer_count(worst_coin)
                        emit(
                            "switch_deferred_delta",
                            {
                                "from": worst_coin,
                                "to": switch["candidate"]["coin"],
                                "reason": delta_assessment["reason"],
                                "delta_pnl_usd": delta_assessment["delta_pnl_usd"],
                                "signed_delta_pct": delta_assessment["signed_delta_pct"],
                                "defer_count": delta_assessment["defer_count"] + 1,
                                "max_defer": self.delta_max_defer_ticks,
                            },
                            notify=True,
                            tier="info",
                        )
                        return acted

                candidate = switch["candidate"]
                direction = switch["direction"]
                emit(
                    "switch_start",
                    {
                        "from": worst_coin,
                        "from_apr": worst_apr,
                        "to": candidate["coin"],
                        "to_apr": switch["verified_apr"],
                        "apr_gain": round(switch["apr_gain"], 1),
                        "breakeven_days": round(switch["breakeven_days"], 1),
                        "trading_cost_pct": round(switch["trading_cost_pct"], 2),
                        "sunk_cost_pct": round(switch["sunk_cost_pct"], 4),
                        "price_pnl_pct": round(switch["price_pnl_pct"], 4),
                        "total_cost_pct": round(switch["total_cost_pct"], 3),
                        "bn_elapsed_h": round(switch["bn_elapsed_h"], 1),
                        "hl_elapsed_m": round(switch["hl_elapsed_m"], 1),
                    },
                    notify=True,
                    tier="trade_alert",
                )
                self._reset_defer_count(worst_coin)
                self.close_position(worst_coin)
                time.sleep(2)
                success = self.open_position(candidate["coin"], direction)
                if success:
                    log_trade(
                        "open", candidate["coin"], direction,
                        size=self._get_position_by_coin(candidate["coin"]).get("size", 0),
                        entry_price=self._get_position_by_coin(candidate["coin"]).get("entry_price", 0),
                        reason=f"switch from {worst_coin}, APR {switch['verified_apr']:.1f}%",
                    )
                else:
                    emit(
                        "switch_failed",
                        {"from": worst_coin, "to": candidate["coin"], "reason": "open_position failed"},
                        notify=True,
                        tier="risk_alert",
                    )
                acted = True

        return acted

    # ---- Report ----

    def get_status(self) -> dict:
        state = self._load()
        positions = state.get("positions", [])
        health = self.check_health()

        hl_balance = self.hl.get_usdc_balance()
        bn_balance = self.bn.get_usdt_balance()

        if not positions:
            return {
                "has_positions": False,
                "position_count": 0,
                "positions": [],
                "hl_balance": hl_balance,
                "bn_balance": bn_balance,
            }

        position_statuses = []
        health_by_coin = {
            ph["coin"]: ph for ph in health.get("position_health", [])
        }
        for pos in positions:
            coin = pos["coin"]
            ph = health_by_coin.get(coin, {})
            position_statuses.append({
                "coin": coin,
                "direction": pos.get("direction"),
                "entry_time": pos.get("entry_time"),
                "size": pos.get("size"),
                "entry_price": pos.get("entry_price"),
                "entry_spread": pos.get("entry_spread"),
                "current_spread": ph.get("current_spread"),
                "current_apr": ph.get("current_apr"),
                "hl_rate": ph.get("hl_rate"),
                "bn_rate": ph.get("bn_rate"),
                "long_size": ph.get("long_size"),
                "short_size": ph.get("short_size"),
                "delta_pct": ph.get("delta_pct"),
                "healthy": ph.get("healthy"),
                "total_funding_earned": pos.get("total_funding_earned", 0.0),
            })

        return {
            "has_positions": True,
            "position_count": len(positions),
            "positions": position_statuses,
            "healthy": health.get("healthy"),
            "hl_balance": hl_balance,
            "bn_balance": bn_balance,
        }

    def get_report(self) -> dict:
        """Generate full report with real balance-based PnL (aggregate across all positions)."""
        status = self.get_status()
        state = self._load()

        entry_total = state.get("entry_total_balance", 0.0)

        current_hl = status.get("hl_balance", 0.0)
        current_bn = status.get("bn_balance", 0.0)
        current_total = round(current_hl + current_bn, 2)

        pnl = round(current_total - entry_total, 2) if entry_total else 0.0
        roi_pct = round(pnl / entry_total * 100, 4) if entry_total else 0.0

        # Aggregate funding earned across all positions
        total_funding = sum(
            p.get("total_funding_earned", 0.0)
            for p in state.get("positions", [])
        )

        annualized_roi_pct = 0.0
        strategy_start = state.get("strategy_start_time")
        if strategy_start and entry_total:
            try:
                hours_running = (
                    datetime.now(timezone.utc) - datetime.fromisoformat(strategy_start)
                ).total_seconds() / 3600
                effective_hours = max(hours_running, 24.0)
                if effective_hours > 0:
                    annualized_roi_pct = round(roi_pct / effective_hours * 24 * 365, 2)
            except (ValueError, TypeError):
                pass

        return {
            **status,
            "entry_total_balance": entry_total,
            "current_total_balance": current_total,
            "total_funding_earned": round(total_funding, 2),
            "pnl": pnl,
            "roi_pct": roi_pct,
            "annualized_roi_pct": annualized_roi_pct,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Section 9: Entry point (tick / report / status CLI)
# ═══════════════════════════════════════════════════════════════════════════════

LOCK_NAME = "cross_funding"
PULSE_INTERVAL_SECONDS = 3600  # 1h

_cb: CircuitBreaker | None = None


def _get_cb() -> CircuitBreaker:
    """Lazy-init circuit breaker (config must be loaded after dotenv)."""
    global _cb
    if _cb is None:
        _cb = CircuitBreaker()
    return _cb


def _build_engine() -> CrossFundingEngine:
    cfg = load_config()
    cross_cfg = cfg["cross_funding"]

    hl_client = HLClient(
        hl_private_key(), testnet=hl_testnet(), vault_address=hl_vault_address()
    )
    bn_client = BinanceClient(
        binance_api_key(), binance_secret_key(), testnet=bn_testnet()
    )
    scanner = VarFundingScanner(
        min_apr=cross_cfg["min_apr_pct"],
        min_confidence=cross_cfg.get("min_confidence", "medium"),
        stability_threshold=cross_cfg.get("stability_max_std_ratio", 0.3),
    )
    return CrossFundingEngine(hl_client, bn_client, scanner, cross_cfg)


def _should_pulse(state: dict) -> bool:
    """Check if enough time has passed since last hourly pulse."""
    last_pulse = state.get("last_pulse_ts")
    if not last_pulse:
        return True
    try:
        last_dt = datetime.fromisoformat(last_pulse)
        elapsed = (datetime.now(timezone.utc) - last_dt).total_seconds()
        return elapsed >= PULSE_INTERVAL_SECONDS
    except (ValueError, TypeError):
        return True


TRADE_HISTORY_PATH = SCRIPT_DIR / "trade_history.json"
DASHBOARD_PATH = SCRIPT_DIR / "dashboard_data.json"


def _load_trade_history() -> list[dict]:
    if TRADE_HISTORY_PATH.exists():
        try:
            return json.loads(TRADE_HISTORY_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return []


def _save_trade_history(trades: list[dict]) -> None:
    # Keep last 200 trades
    trades = trades[-200:]
    TRADE_HISTORY_PATH.write_text(json.dumps(trades, indent=2, ensure_ascii=False))


def log_trade(
    trade_type: str, coin: str, direction: dict, size: float, entry_price: float,
    exit_price: float | None = None, pnl: float | None = None,
    funding_pnl: float | None = None, reason: str = "",
) -> None:
    """Append a trade record to trade_history.json."""
    trades = _load_trade_history()
    record: dict = {
        "time": datetime.now(timezone.utc).isoformat(),
        "type": trade_type,
        "coin": coin,
        "direction": direction,
        "size": size,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "pnl": pnl,
        "reason": reason,
    }
    if funding_pnl is not None:
        record["funding_pnl"] = funding_pnl
    trades.append(record)
    _save_trade_history(trades)


def _build_position_dashboard(
    engine: CrossFundingEngine, pos_data: dict, roi_pct: float,
) -> dict:
    """Build dashboard data for a single position."""
    coin = pos_data["coin"]
    direction = pos_data.get("direction", {})
    long_ex = direction.get("long_exchange", "hyperliquid")
    short_ex = direction.get("short_exchange", "binance")
    long_client = engine._get_client(long_ex)
    short_client = engine._get_client(short_ex)

    long_pos = long_client.get_position(coin)
    short_pos = short_client.get_position(coin)

    long_size = abs(long_pos["size"]) if long_pos else 0.0
    short_size = abs(short_pos["size"]) if short_pos else 0.0

    hl_rate = engine.hl.get_funding_rate(coin)
    bn_rate = engine.bn.get_funding_rate(coin)

    current_price = engine.hl.get_mid_price(coin)
    entry_price = pos_data.get("entry_price", 0.0)

    rate_map = {"hyperliquid": hl_rate, "binance": bn_rate}
    current_spread = rate_map[short_ex] - rate_map[long_ex]

    # Settlement countdown
    now = datetime.now(timezone.utc)
    hl_next_min = 60 - now.minute
    bn_next_secs = 0
    for h in [0, 8, 16, 24]:
        bn_next = now.replace(hour=h % 24, minute=0, second=0, microsecond=0)
        if h == 24:
            bn_next += timedelta(days=1)
            bn_next = bn_next.replace(hour=0)
        if bn_next > now:
            bn_next_secs = (bn_next - now).total_seconds()
            break
    bn_next_min = int(bn_next_secs / 60)

    # Funding payments count
    entry_time = pos_data.get("entry_time", "")
    hours_held = 0.0
    if entry_time:
        try:
            hours_held = (
                now - datetime.fromisoformat(entry_time)
            ).total_seconds() / 3600
        except (ValueError, TypeError):
            pass
    hl_payments = int(hours_held)
    bn_payments = int(hours_held / 8)

    long_entry_px = long_pos.get("entry_px", entry_price) if long_pos else entry_price
    short_entry_px = short_pos.get("entry_px", entry_price) if short_pos else entry_price

    long_pnl = long_pos.get("unrealized_pnl", 0.0) if long_pos else 0.0
    short_pnl = short_pos.get("unrealized_pnl", 0.0) if short_pos else 0.0
    total_price_pnl = round(long_pnl + short_pnl, 2)

    # Real funding PnL from exchange APIs
    hl_cum_funding = 0.0
    bn_cum_funding = 0.0
    if long_ex == "hyperliquid":
        hl_cum_funding = -(long_pos.get("cum_funding", 0.0)) if long_pos else 0.0
    else:
        hl_cum_funding = -(short_pos.get("cum_funding", 0.0)) if short_pos else 0.0

    entry_time_val = pos_data.get("entry_time", "")
    if entry_time_val:
        try:
            entry_ms = int(datetime.fromisoformat(entry_time_val).timestamp() * 1000)
            bn_cum_funding = engine.bn.get_funding_income(coin, entry_ms)
        except (ValueError, TypeError):
            pass

    if long_ex == "hyperliquid":
        hl_funding_share = round(hl_cum_funding, 4)
        bn_funding_share = round(bn_cum_funding, 4)
    else:
        hl_funding_share = round(hl_cum_funding, 4)
        bn_funding_share = round(bn_cum_funding, 4)

    total_funding = round(hl_funding_share + bn_funding_share, 2)

    # Build leg data
    hl_leg_data = {
        "exchange": "hyperliquid",
        "leverage": engine.leverage,
        "funding_rate": hl_rate,
        "settlement_cycle_h": 1,
        "next_settlement_min": hl_next_min,
    }
    bn_leg_data = {
        "exchange": "binance",
        "leverage": engine.leverage,
        "funding_rate": bn_rate,
        "settlement_cycle_h": 8,
        "next_settlement_min": bn_next_min,
    }

    if long_ex == "hyperliquid":
        long_leg_extra = hl_leg_data
        short_leg_extra = bn_leg_data
        long_funding = hl_funding_share
        short_funding = bn_funding_share
        long_payments = hl_payments
        short_payments = bn_payments
    else:
        long_leg_extra = bn_leg_data
        short_leg_extra = hl_leg_data
        long_funding = bn_funding_share
        short_funding = hl_funding_share
        long_payments = bn_payments
        short_payments = hl_payments

    long_mark_px = long_pos.get("mark_px", current_price) if long_pos else current_price
    short_mark_px = short_pos.get("mark_px", current_price) if short_pos else current_price
    long_notional = round(long_size * long_mark_px, 2)
    short_notional = round(short_size * short_mark_px, 2)

    # Pending (unrealized) funding: rate * notional * elapsed fraction
    # Sign: positive rate means longs pay shorts
    def _pending_funding(rate: float, notional: float, side: str, cycle_h: int, next_min: int) -> float:
        elapsed_min = cycle_h * 60 - next_min
        fraction = elapsed_min / (cycle_h * 60) if cycle_h > 0 else 0
        # Funding payment = rate * notional; longs pay when rate > 0
        raw = rate * notional * fraction
        return round(-raw if side == "long" else raw, 4)

    long_pending = _pending_funding(
        long_leg_extra["funding_rate"], long_notional, "long",
        long_leg_extra["settlement_cycle_h"], long_leg_extra["next_settlement_min"],
    )
    short_pending = _pending_funding(
        short_leg_extra["funding_rate"], short_notional, "short",
        short_leg_extra["settlement_cycle_h"], short_leg_extra["next_settlement_min"],
    )

    avg_notional = (long_notional + short_notional) / 2 if (long_notional + short_notional) > 0 else 1
    delta_exposure = abs(long_notional - short_notional)
    delta_pct = round(delta_exposure / avg_notional * 100, 2)

    # APR & daily projection based on actual funding PnL
    total_funding_with_pending = total_funding + long_pending + short_pending
    if hours_held > 0 and avg_notional > 0:
        actual_rate_per_hour = total_funding_with_pending / avg_notional / hours_held
        current_apr = round(actual_rate_per_hour * 8760 * 100, 2)
        projected_daily = round(actual_rate_per_hour * 24 * avg_notional, 2)
    else:
        current_apr = 0.0
        projected_daily = 0.0

    return {
        "has_position": True,
        "coin": coin,
        "direction": direction,
        "entry_time": entry_time,
        "entry_spread": pos_data.get("entry_spread", 0.0),
        "current_spread": current_spread,
        "long_leg": {
            **long_leg_extra,
            "side": "long",
            "size": long_size,
            "entry_price": long_entry_px,
            "current_price": current_price,
            "notional": long_notional,
            "unrealized_pnl": round(long_pnl, 2),
            "accumulated_funding": long_funding,
            "pending_funding": long_pending,
            "funding_payments": long_payments,
        },
        "short_leg": {
            **short_leg_extra,
            "side": "short",
            "size": short_size,
            "entry_price": short_entry_px,
            "current_price": current_price,
            "notional": short_notional,
            "unrealized_pnl": round(short_pnl, 2),
            "accumulated_funding": short_funding,
            "pending_funding": short_pending,
            "funding_payments": short_payments,
        },
        "delta_neutral": delta_pct < 5,
        "delta_exposure": round(delta_exposure, 6),
        "delta_exposure_pct": delta_pct,
        "total_funding_pnl": total_funding,
        "total_pending_funding": round(long_pending + short_pending, 4),
        "total_price_pnl": total_price_pnl,
        "total_pnl": round(total_funding + total_price_pnl, 2),
        "roi_pct": roi_pct,
        "current_apr": current_apr,
        "projected_daily_usd": projected_daily,
    }, total_funding


def export_dashboard(
    engine: CrossFundingEngine,
    opportunities: list[dict] | None = None,
) -> None:
    """Write dashboard_data.json for the frontend."""
    try:
        state = engine._load()
        positions = state.get("positions", [])

        # Balances
        hl_bal = engine.hl.get_usdc_balance()
        bn_bal = engine.bn.get_usdt_balance()
        entry_total = state.get("entry_total_balance", 0.0)
        current_total = round(hl_bal + bn_bal, 2)

        # Build positions array first to get live funding PnL
        dashboard_positions: list[dict] = []
        live_funding_total = 0.0
        for pos_data in positions:
            pos_dashboard, pos_funding = _build_position_dashboard(
                engine, pos_data, 0.0,
            )
            dashboard_positions.append(pos_dashboard)
            live_funding_total += pos_funding
            live_funding_total += pos_dashboard.get("total_pending_funding", 0.0)

            # Update per-position funding in state
            for sp in state.get("positions", []):
                if sp["coin"] == pos_data["coin"]:
                    sp["total_funding_earned"] = pos_funding
                    break

        if positions:
            engine._save(state)

        # PnL & ROI: closed trades + live positions funding
        trades = _load_trade_history()
        closed_pnl = sum(
            t.get("funding_pnl", 0) for t in trades
            if t.get("funding_pnl") is not None
        )
        total_pnl = round(closed_pnl + live_funding_total, 2)
        roi_pct = round(total_pnl / entry_total * 100, 4) if entry_total else 0.0

        annualized_roi_pct = 0.0
        strategy_start = state.get("strategy_start_time", "")
        if strategy_start and entry_total:
            try:
                hours_running = (
                    datetime.now(timezone.utc) - datetime.fromisoformat(strategy_start)
                ).total_seconds() / 3600
                effective_hours = max(hours_running, 24.0)
                if effective_hours > 0:
                    annualized_roi_pct = round(roi_pct / effective_hours * 24 * 365, 2)
            except (ValueError, TypeError):
                pass

        # Update roi_pct in position dashboards
        for pd in dashboard_positions:
            pd["roi_pct"] = roi_pct

        summary = {
            "total_invested": entry_total or current_total,
            "current_value": current_total,
            "total_pnl": total_pnl,
            "roi_pct": round(roi_pct, 2),
            "annualized_roi_pct": annualized_roi_pct,
            "hl_balance": round(hl_bal, 2),
            "bn_balance": round(bn_bal, 2),
            "position_count": len(positions),
            "max_positions": engine.max_positions,
        }

        # Opportunities
        opps = opportunities or []

        # Trade history
        trades = _load_trade_history()

        dashboard = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "summary": summary,
            "positions": dashboard_positions,
            "opportunities": opps[:20],
            "trades": trades[-50:],
        }

        DASHBOARD_PATH.write_text(json.dumps(dashboard, indent=2, ensure_ascii=False))
    except Exception as e:
        emit_error("export_dashboard", e)


def tick() -> None:
    """Main loop tick: scan → manage positions (close/open/switch) + pulse."""
    if not acquire_lock(LOCK_NAME):
        emit("skip", {"reason": "another instance running"})
        return

    cb = _get_cb()
    try:
        if cb.is_open():
            emit("skip", {"reason": "circuit breaker open"})
            return

        engine = _build_engine()

        # Reconcile state vs actual exchange positions every tick
        orphans = engine.reconcile_positions()
        if orphans:
            emit(
                "reconciliation_alert",
                {
                    "orphan_count": len(orphans),
                    "orphans": orphans,
                    "action": "manual intervention required",
                },
                notify=True,
                tier="risk_alert",
            )

        state = engine._load()
        positions = state.get("positions", [])
        opportunities: list[dict] = []

        # Always scan opportunities
        opportunities = engine.scan_opportunities()

        if not positions:
            # No positions: stability check flow for first position
            if not opportunities:
                emit("tick", {"action": "idle", "reason": "no opportunities"})
                export_dashboard(engine, opportunities)
                cb.record_success()
                return

            engine.record_snapshot(opportunities)

            stable_opp = engine.get_stable_opportunity()
            if not stable_opp:
                emit(
                    "tick",
                    {
                        "action": "accumulating",
                        "reason": "waiting for rate stability",
                        "top_coin": opportunities[0]["coin"],
                        "top_apr": opportunities[0]["estimated_apr"],
                    },
                )
                export_dashboard(engine, opportunities)
                cb.record_success()
                return

            # Deep verification
            direction = {
                "long_exchange": stable_opp["long_exchange"],
                "short_exchange": stable_opp["short_exchange"],
            }
            verification = engine.verify_opportunity(stable_opp["coin"], direction)
            if not verification["valid"]:
                emit(
                    "tick",
                    {
                        "action": "rejected",
                        "coin": stable_opp["coin"],
                        "reason": verification["reject_reason"],
                    },
                )
                export_dashboard(engine, opportunities)
                cb.record_success()
                return

            emit(
                "tick",
                {
                    "action": "opening",
                    "coin": stable_opp["coin"],
                    "apr": verification["net_apr_after_costs"],
                    "direction": direction,
                },
            )
            success = engine.open_position(stable_opp["coin"], direction)
            if not success:
                cb.record_error("open_position")
                export_dashboard(engine, opportunities)
                return
            opened_pos = engine._get_position_by_coin(stable_opp["coin"])
            log_trade(
                "open", stable_opp["coin"], direction,
                size=opened_pos.get("size", 0) if opened_pos else 0,
                entry_price=opened_pos.get("entry_price", 0) if opened_pos else 0,
                reason=f"APR {verification['net_apr_after_costs']:.1f}%",
            )
        else:
            # Has positions: manage all (close unhealthy, open new, switch worst)
            acted = engine.check_and_manage(opportunities)
            if not acted:
                health = engine.check_health()
                report_data = engine.get_report()
                snapshot = {**report_data, **health}

                # Cache snapshot every tick for fast status queries
                state = engine._load()
                state["cached_snapshot"] = snapshot
                state["cached_snapshot_ts"] = datetime.now(timezone.utc).isoformat()

                # Push hourly pulse notification
                if _should_pulse(state):
                    emit("tick", snapshot, tier="hourly_pulse")
                    state["last_pulse_ts"] = datetime.now(timezone.utc).isoformat()
                else:
                    pos_coins = [p["coin"] for p in engine._get_positions()]
                    emit(
                        "tick",
                        {
                            "action": "hold",
                            "positions": pos_coins,
                            "position_count": len(pos_coins),
                            "healthy": health.get("healthy"),
                        },
                    )

                engine._save(state)

        # Export dashboard data every tick
        export_dashboard(engine, opportunities)

        cb.record_success()

    except Exception as e:
        emit_error("tick", e, notify=cb.record_error("tick"))
    finally:
        release_lock()


def report() -> None:
    """Generate and output report (with daily report notification card)."""
    try:
        engine = _build_engine()
        data = engine.get_report()
        emit("report", data, notify=True, tier="daily_report")
    except Exception as e:
        emit_error("report", e, notify=True)


def status() -> None:
    """Output current status card. Reads cache first (tick updates every 5 min)."""
    try:
        state = load_state("cross_funding")
        cached = state.get("cached_snapshot")
        if cached:
            cached["_cached_ts"] = state.get("cached_snapshot_ts", "")
            emit("status", cached, tier="hourly_pulse")
        else:
            engine = _build_engine()
            data = engine.get_report()
            emit("status", data, tier="hourly_pulse")
    except Exception as e:
        emit_error("status", e)


def main() -> None:
    from dotenv import load_dotenv

    script_dir = Path(__file__).resolve().parent
    load_dotenv(script_dir / ".env")

    parser = argparse.ArgumentParser(
        description="Cross-exchange funding rate arbitrage (HL + Binance)"
    )
    parser.add_argument(
        "command", choices=["tick", "report", "status"], help="subcommand to run"
    )
    args = parser.parse_args()

    commands = {
        "tick": tick,
        "report": report,
        "status": status,
    }
    commands[args.command]()


if __name__ == "__main__":
    main()
