"""Adapters for sshsign history rows used by the local negotiation engine."""
from __future__ import annotations

import json
import subprocess
import urllib.parse


def ssh_history(
    negotiation_id: str,
    sshsign_host: str = "sshsign.dev",
    runner=subprocess.run,
) -> list[dict] | None:
    """Return sshsign's `history --negotiation-id` rows, or None on error."""
    try:
        result = runner(
            ["ssh", sshsign_host, "history", "--negotiation-id", negotiation_id],
            capture_output=True, text=True, timeout=15,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0 or not (result.stdout or "").strip():
        return None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, list) else None


def synthesize_offer_event(entry: dict) -> dict | None:
    """Translate a sshsign history row into the skill's event shape."""
    if not isinstance(entry, dict):
        return None
    etype = entry.get("type")
    if etype not in ("offer", "counter", "accept"):
        return None
    try:
        round_num = int(entry.get("round", 0))
    except (TypeError, ValueError):
        return None
    if round_num < 0:
        return None
    party = entry.get("from") or ""
    if party not in ("founder", "investor"):
        return None

    raw_meta = entry.get("metadata")
    terms: dict = {}
    message = ""
    if isinstance(raw_meta, str) and raw_meta.strip():
        try:
            parsed = json.loads(raw_meta)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            message = str(parsed.pop("_message", "") or "")
            terms = parsed
    elif isinstance(raw_meta, dict):
        meta_copy = dict(raw_meta)
        message = str(meta_copy.pop("_message", "") or "")
        terms = meta_copy

    return {
        "type": etype,
        "party": party,
        "round": round_num,
        "terms": terms,
        "message": message,
    }


def augment_signing_url(event: dict, bot_username: str) -> dict:
    """Append a bare Telegram deep-link callback to a signing event URL."""
    url = (event.get("approval_url") or "").strip()
    if not url or not bot_username:
        return event
    callback = urllib.parse.quote(f"https://t.me/{bot_username}")
    sep = "&" if "?" in url else "?"
    return {**event, "approval_url": f"{url}{sep}callback={callback}"}
