"""Telegram push helpers for the negotiate_safe skill.

These shell out to `openclaw message send`, which is the channel-agnostic CLI
primitive OpenClaw exposes for skills to send messages and file attachments
back to the user's chat.

Unused until PR 5.3 wires streaming into run_safe.py. This module is pure
(side effects only via subprocess.run) and exhaustively unit-tested.
"""
from __future__ import annotations

import json
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from typing_loop import get_bot_token


DEFAULT_SESSIONS_PATH = Path("/root/.openclaw/agents/main/sessions/sessions.json")


@dataclass(frozen=True)
class SendResult:
    ok: bool
    message_id: str | None
    error: str | None


class SigningUrlTargetError(ValueError):
    """Raised when send_signing_url_to_dm is called with a non-DM target.

    A signing URL is a bearer handle: anyone with the link can walk through
    the browser approval flow for that user. It is delivered to
    the signer's private DM. A group chat_id in Telegram is negative; a DM
    chat_id equals the recipient's numeric user_id and is positive. The
    primitive enforces this at the call boundary — runtime proof that no
    code path accidentally routes a signing URL to a shared venue.
    """


def _normalize_telegram_target(chat_id: str | int) -> str:
    """Return the raw Telegram chat id expected by OpenClaw/Telegram.

    OpenClaw envelopes sometimes label chat ids as ``group:-123`` or
    ``telegram:-123``. The transport boundary must pass the numeric id to
    ``openclaw message send``; leaking the label through produces Telegram
    API 400s for group sends.
    """
    target = str(chat_id).strip()
    if ":" in target:
        target = target.rsplit(":", 1)[-1].strip()
    return target


def _parse_bot_api_result(body: str) -> SendResult:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return SendResult(ok=False, message_id=None, error="non-JSON response from Telegram")
    if isinstance(payload, dict) and payload.get("ok"):
        result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
        mid = result.get("message_id")
        return SendResult(ok=True, message_id=str(mid) if mid is not None else None, error=None)
    return SendResult(ok=False, message_id=None, error=json.dumps(payload))


def _parse_bot_api_edit_result(body: str) -> SendResult:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return SendResult(ok=False, message_id=None, error="non-JSON response from Telegram")
    if isinstance(payload, dict) and payload.get("ok"):
        result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
        mid = result.get("message_id")
        return SendResult(ok=True, message_id=str(mid) if mid is not None else None, error=None)
    return SendResult(ok=False, message_id=None, error=json.dumps(payload))


def _multipart_body(
    fields: dict[str, str],
    file_field: str,
    file_path: Path,
    boundary: str,
) -> bytes:
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        )
        chunks.append(str(value).encode())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}\r\n".encode())
    chunks.append(
        (
            f'Content-Disposition: form-data; name="{file_field}"; '
            f'filename="{file_path.name}"\r\n'
            "Content-Type: application/octet-stream\r\n\r\n"
        ).encode()
    )
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks)


def _infer_parse_mode(message: str | None) -> str | None:
    if not message:
        return None
    html_markers = ("<b>", "</b>", "<code>", "</code>", "<pre>", "</pre>", "<i>", "</i>")
    if any(marker in message for marker in html_markers):
        return "HTML"
    return None


def _send_telegram_bot_api(
    chat_id: str,
    message: str | None = None,
    media_path: str | Path | None = None,
    bot_token: str | None = None,
    reply_markup: dict | None = None,
    opener=urllib.request.urlopen,
) -> SendResult:
    token = bot_token or get_bot_token()
    if not token:
        return SendResult(ok=False, message_id=None, error="Telegram bot token not available")

    target = _normalize_telegram_target(chat_id)
    try:
        if media_path:
            path = Path(media_path)
            boundary = "----claw-negotiate-boundary"
            fields = {"chat_id": target}
            if message:
                fields["caption"] = message
                parse_mode = _infer_parse_mode(message)
                if parse_mode:
                    fields["parse_mode"] = parse_mode
            if reply_markup:
                fields["reply_markup"] = json.dumps(reply_markup)
            body = _multipart_body(fields, "document", path, boundary)
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendDocument",
                data=body,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
                method="POST",
            )
        else:
            payload = {"chat_id": target, "text": message or ""}
            parse_mode = _infer_parse_mode(message)
            if parse_mode:
                payload["parse_mode"] = parse_mode
            if reply_markup:
                payload["reply_markup"] = reply_markup
            body = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
        with opener(req, timeout=30) as resp:
            return _parse_bot_api_result(resp.read().decode())
    except Exception as e:
        return SendResult(ok=False, message_id=None, error=f"Telegram Bot API send failed: {e}")


def _edit_telegram_bot_api(
    chat_id: str,
    message_id: str | int,
    message: str,
    bot_token: str | None = None,
    opener=urllib.request.urlopen,
) -> SendResult:
    token = bot_token or get_bot_token()
    if not token:
        return SendResult(ok=False, message_id=None, error="Telegram bot token not available")

    try:
        numeric_message_id = int(message_id)
    except (TypeError, ValueError):
        return SendResult(ok=False, message_id=None, error="invalid Telegram message_id")

    payload = {
        "chat_id": _normalize_telegram_target(chat_id),
        "message_id": numeric_message_id,
        "text": message,
    }
    parse_mode = _infer_parse_mode(message)
    if parse_mode:
        payload["parse_mode"] = parse_mode
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/editMessageText",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with opener(req, timeout=30) as resp:
            return _parse_bot_api_edit_result(resp.read().decode())
    except Exception as e:
        return SendResult(ok=False, message_id=None, error=f"Telegram Bot API edit failed: {e}")


def resolve_chat_id(
    flag_value: str | None,
    sessions_path: Path = DEFAULT_SESSIONS_PATH,
) -> str | None:
    """Resolve a Telegram chat_id.

    Primary source: explicit --chat-id flag value passed by the caller.
    Fallback: the most recently updated `agent:main:telegram:direct:*` entry
    in OpenClaw's sessions.json (keyed by `updatedAt`).

    Returns None if neither source yields a value.
    """
    if flag_value:
        return str(flag_value).strip() or None

    try:
        data = json.loads(sessions_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(data, dict):
        return None

    best: tuple[int, str] | None = None
    for key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        if not key.startswith("agent:main:telegram:direct:"):
            continue
        chat_id = key.rsplit(":", 1)[-1]
        if not chat_id:
            continue
        updated = entry.get("updatedAt")
        if not isinstance(updated, (int, float)):
            continue
        if best is None or updated > best[0]:
            best = (int(updated), chat_id)

    return best[1] if best else None


def send_telegram(
    chat_id: str,
    message: str | None = None,
    media_path: str | Path | None = None,
    force_document: bool = False,
    reply_markup: dict | None = None,
    openclaw_bin: str = "openclaw",
    runner=subprocess.run,
    opener=urllib.request.urlopen,
) -> SendResult:
    """Send a message and/or file attachment to a Telegram chat via openclaw CLI.

    At least one of `message` or `media_path` must be provided.
    `force_document` sends images/GIFs uncompressed (Telegram-only flag);
    PDFs are already treated as documents, so the flag is a no-op for them
    but harmless to set.

    `runner` is injectable for testing (default: subprocess.run).
    """
    if not message and not media_path:
        raise ValueError("send_telegram requires message and/or media_path")

    token = get_bot_token()
    if token:
        return _send_telegram_bot_api(
            chat_id=chat_id,
            message=message,
            media_path=media_path,
            bot_token=token,
            reply_markup=reply_markup,
            opener=opener,
        )

    cmd = [
        openclaw_bin, "message", "send",
        "--channel", "telegram",
        "--target", _normalize_telegram_target(chat_id),
        "--json",
    ]
    if message:
        cmd.extend(["--message", message])
    if media_path:
        cmd.extend(["--media", str(media_path)])
    if force_document:
        cmd.append("--force-document")

    try:
        result = runner(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        fallback = _send_telegram_bot_api(
            chat_id=chat_id,
            message=message,
            media_path=media_path,
            reply_markup=reply_markup,
            opener=opener,
        )
        if fallback.ok:
            return fallback
        return SendResult(ok=False, message_id=None, error=f"timeout; fallback: {fallback.error}")
    except FileNotFoundError:
        fallback = _send_telegram_bot_api(
            chat_id=chat_id,
            message=message,
            media_path=media_path,
            reply_markup=reply_markup,
            opener=opener,
        )
        if fallback.ok:
            return fallback
        return SendResult(ok=False, message_id=None, error=f"{openclaw_bin} not found on PATH; fallback: {fallback.error}")

    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip() or f"exit {result.returncode}"
        fallback = _send_telegram_bot_api(
            chat_id=chat_id,
            message=message,
            media_path=media_path,
            reply_markup=reply_markup,
            opener=opener,
        )
        if fallback.ok:
            return fallback
        return SendResult(ok=False, message_id=None, error=f"{err}; fallback: {fallback.error}")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return SendResult(ok=False, message_id=None, error="non-JSON response from openclaw")

    inner = payload.get("payload") if isinstance(payload, dict) else None
    if isinstance(inner, dict) and inner.get("ok"):
        mid = inner.get("messageId")
        return SendResult(ok=True, message_id=str(mid) if mid is not None else None, error=None)

    return SendResult(ok=False, message_id=None, error=json.dumps(payload))


def edit_telegram_message(
    chat_id: str,
    message_id: str | int,
    message: str,
    opener=urllib.request.urlopen,
) -> SendResult:
    """Edit a bot-sent Telegram text message via the official Bot API.

    OpenClaw's generic message CLI currently gives this skill a send
    primitive. Editing is Telegram-specific, so use the Bot API directly when
    a bot token is available and let callers fall back to sending a new card.
    """
    return _edit_telegram_bot_api(
        chat_id=chat_id,
        message_id=message_id,
        message=message,
        opener=opener,
    )


def send_signing_url_to_dm(
    dm_chat_id: int | str,
    message: str,
    openclaw_bin: str = "openclaw",
    runner=subprocess.run,
) -> SendResult:
    """Send a signing URL message to a user's DM.

    This is the supported code path for delivering a sshsign.dev
    approval link. The parameter name is `dm_chat_id` — not a generic
    `target` or `chat_id` — because the API contract is "send to this
    user's private DM, never to a group". The runtime check asserts
    the target is a positive integer (Telegram convention: private
    chat_id == user_id > 0; group chat_id < 0). Any attempt to pass a
    group chat_id raises SigningUrlTargetError BEFORE any subprocess
    call happens, so the URL never touches a shared venue.

    Structural privacy: the signature prevents misuse. There is no
    parameter that accepts a group id; the name embeds the invariant;
    a reviewer inspecting a call site sees "send_signing_url_to_dm" and
    knows the target cannot be a group. This replaces the runtime
    substring-scanning "guard" design from an earlier K4 plan — privacy
    is a property of the function signature, not a filter on message
    bodies.

    Raises
    ------
    SigningUrlTargetError
        If dm_chat_id is not parseable as a positive integer.
    """
    try:
        parsed = int(str(dm_chat_id).strip())
    except (TypeError, ValueError) as e:
        raise SigningUrlTargetError(
            f"dm_chat_id must be an integer, got {dm_chat_id!r}: {e}"
        )
    if parsed <= 0:
        raise SigningUrlTargetError(
            f"signing URL target must be a positive DM chat_id "
            f"(negative ids are groups): got {parsed}"
        )
    return send_telegram(
        chat_id=str(parsed),
        message=message,
        openclaw_bin=openclaw_bin,
        runner=runner,
    )
