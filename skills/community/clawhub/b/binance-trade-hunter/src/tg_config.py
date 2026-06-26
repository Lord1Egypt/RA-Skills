"""
Auto-discover Telegram bot config.
Priority: config.yaml > OpenClaw config (~/.openclaw/openclaw.json)
Fallback: getUpdates API to find the most recent private chat_id
"""

import os
import json
import logging
from pathlib import Path

import requests

logger = logging.getLogger("tg-config")


def get_tg_config(cfg: dict = None) -> tuple[str, str]:
    """
    Get (bot_token, chat_id) from config or OpenClaw auto-discovery.

    Args:
        cfg: parsed config.yaml dict (optional)

    Returns:
        (bot_token, chat_id) - may be empty strings if not found
    """
    bot_token = ""
    chat_id = ""

    # 1. Try from config.yaml
    if cfg:
        tg = cfg.get("telegram", {}) or {}
        bot_token = tg.get("bot_token", "") or ""
        chat_id = str(tg.get("chat_id", "") or "")

    # 2. Auto-discover from OpenClaw if missing
    if not bot_token or not chat_id:
        oc = _load_openclaw_config()
        if oc:
            if not bot_token:
                bot_token = oc.get("bot_token", "")
            if not chat_id:
                chat_id = oc.get("chat_id", "")

    # 3. If we have token but no chat_id, try getUpdates to find it
    if bot_token and not chat_id:
        chat_id = _discover_chat_id(bot_token)

    return bot_token, chat_id


def _load_openclaw_config() -> dict | None:
    """Read TG bot token + chat_id from OpenClaw config"""
    oc_path = Path.home() / ".openclaw" / "openclaw.json"
    if not oc_path.exists():
        return None
    try:
        data = json.loads(oc_path.read_text(encoding="utf-8"))
        bot_token = (data.get("channels", {})
                         .get("telegram", {})
                         .get("botToken", ""))
        chat_id = os.environ.get("OPENCLAW_TG_CHAT_ID", "")
        if bot_token:
            return {"bot_token": bot_token, "chat_id": chat_id}
    except Exception:
        pass
    return None


def _discover_chat_id(bot_token: str) -> str:
    """Use getUpdates to find the most recent private chat_id"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        resp = requests.get(url, params={"limit": 10, "offset": -10}, timeout=10)
        data = resp.json()
        if not data.get("ok"):
            return ""

        # Find the most recent private chat
        for update in reversed(data.get("result", [])):
            msg = update.get("message", {})
            chat = msg.get("chat", {})
            if chat.get("type") == "private":
                cid = str(chat.get("id", ""))
                if cid:
                    logger.info(f"Auto-discovered chat_id: {cid}")
                    return cid
    except Exception as e:
        logger.warning(f"Failed to discover chat_id: {e}")
    return ""
