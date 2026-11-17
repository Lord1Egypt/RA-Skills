#!/usr/bin/env python3
"""
buzz-acp.py — ACP ↔ OpenClaw bridge for Buzz

Speaks ACP (JSON-RPC 2.0 over stdio) on one end.
Calls OpenClaw /v1/chat/completions on the other.
Posts replies to Buzz channels using buzz-cli.

Architecture:
  buzz-acp (Rust) → stdio JSON-RPC → this shim → OpenClaw /v1/chat/completions
                                                → buzz-cli messages send (posts reply to channel)

The shim receives the user's message via session/prompt, calls OpenClaw for
the reply, then posts the reply to the Buzz channel using buzz-cli.

Environment variables:
    OPENCLAW_URL            OpenClaw base URL  (default: http://localhost:18789)
    OPENCLAW_API_KEY        OpenClaw API key   (required if auth is enabled)
    OPENCLAW_SESSION_KEY    Session key        (default: agent:main:buzz:marvin)
    OPENCLAW_AGENT_NAME     Display name for logs (default: Marvin)
    BUZZ_RELAY_URL          Buzz relay URL     (for buzz-cli)
    BUZZ_PRIVATE_KEY        Agent Nostr private key (for buzz-cli)

ACP protocol: JSON-RPC 2.0 over stdin/stdout. One JSON object per line.

Author:  Marvin (OpenClaw agent) + Darren Robinson
Repo:    https://github.com/darrenjrobinson/buzz-acp
License: Apache 2.0
"""

import sys
import json
import os
import re
import subprocess
import threading
import uuid
import logging
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OPENCLAW_URL      = os.environ.get("OPENCLAW_URL", "http://localhost:18789")
OPENCLAW_API_KEY  = os.environ.get("OPENCLAW_API_KEY", "")
SESSION_KEY       = os.environ.get("OPENCLAW_SESSION_KEY", "agent:main:buzz:marvin")
AGENT_NAME        = os.environ.get("OPENCLAW_AGENT_NAME", "Marvin")

# Path to buzz-cli binary
BUZZ_CLI = os.environ.get("BUZZ_CLI", "/home/marvin/.local/bin/buzz")

# ---------------------------------------------------------------------------
# Logging — stderr only (stdout is the ACP wire)
# ---------------------------------------------------------------------------
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format=f"[{AGENT_NAME}-shim] %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ACP constants
# ---------------------------------------------------------------------------
ACP_VERSION   = "2.0.0"   # Protocol v2 — buzz-acp delivers base_prompt via session/new systemPrompt
CAPABILITIES  = {"streaming": True, "cancellation": True, "sessions": True}

# ---------------------------------------------------------------------------
# Per-session state
# Map: acp_session_id → {"history": [...], "system_prompt": str}
# ---------------------------------------------------------------------------
_sessions: dict[str, dict] = {}
_sessions_lock = threading.Lock()

# Active run cancel events: req_id → threading.Event
_active_runs: dict = {}

# ---------------------------------------------------------------------------
# Wire helpers
# ---------------------------------------------------------------------------
_write_lock = threading.Lock()

def _send(obj: dict) -> None:
    line = json.dumps(obj, ensure_ascii=False) + "\n"
    with _write_lock:
        sys.stdout.write(line)
        sys.stdout.flush()

def _respond(req_id, result: dict) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})

def _error(req_id, code: int, msg: str) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": msg}})

def _notify(method: str, params: dict) -> None:
    _send({"jsonrpc": "2.0", "method": method, "params": params})


# ---------------------------------------------------------------------------
# Context parsing — extract channel UUID and reply-to from prompt text
# ---------------------------------------------------------------------------
def _parse_context(prompt_text: str) -> dict:
    """Extract channel UUID, reply-to event ID, and scope from the [Context] block.

    The [Context] block looks like:
        [Context]
        Scope: channel
        Channel: Marvin (#a96ac6ed-11df-4398-8448-dd6fbe28451a)
        Hint: Use `buzz messages get --channel <UUID>` for recent messages if needed.
        Reply to: <event_id>

    Or for threads:
        [Context]
        Scope: thread
        Channel: Brainstorming (#cc8e0c2a-9afe-47bb-9c2f-1b2329b49195)
        Thread root: <event_id>
        Reply to: <event_id>
    """
    ctx = {"channel_id": None, "reply_to": None, "scope": "channel"}

    # Find [Context] block
    ctx_match = re.search(
        r'\[Context\]\s*\n(.*?)(?:\n\[|\Z)',
        prompt_text,
        re.DOTALL
    )
    if not ctx_match:
        return ctx

    ctx_block = ctx_match.group(1)

    # Extract channel UUID from "Channel: <name> (#<uuid>)"
    channel_match = re.search(r'Channel:.*?#([0-9a-f-]{36})', ctx_block)
    if channel_match:
        ctx["channel_id"] = channel_match.group(1)

    # Extract scope
    scope_match = re.search(r'Scope:\s*(\w+)', ctx_block)
    if scope_match:
        ctx["scope"] = scope_match.group(1)

    # Extract "Reply to:" event ID
    reply_match = re.search(r'Reply to:\s*([0-9a-f]{64})', ctx_block)
    if reply_match:
        ctx["reply_to"] = reply_match.group(1)

    return ctx


def _parse_event_id(prompt_text: str) -> str | None:
    """Extract the triggering event ID from the [Event] block."""
    match = re.search(r'Event ID:\s*([0-9a-f]{64})', prompt_text)
    return match.group(1) if match else None


def _extract_user_message(prompt_text: str) -> str:
    """Extract the actual user message content from the [Event] block.

    The prompt contains [Base], [System], [Context], [Event] sections.
    The actual user message is in the [Event] block under "Content:".
    """
    # Try to find Content: in the [Event] block
    # The event block is the last section, starts with [Buzz event: ...] or [Event]
    content_match = re.search(
        r'(?:\[Buzz event[^\]]*\]|\[Event\])\s*\n.*?\nContent:\s*(.*?)(?:\nTags:|\n\n\[|\Z)',
        prompt_text,
        re.DOTALL
    )
    if content_match:
        return content_match.group(1).strip()

    # Fallback: if no [Event] block, the entire prompt is the message
    # (this happens for non-mention events or direct prompts)
    # Strip [Base] and [System] sections if present
    cleaned = re.sub(r'\[Base\]\s*\n.*?(?:\n\[|\Z)', '', prompt_text, flags=re.DOTALL)
    cleaned = re.sub(r'\[System\]\s*\n.*?(?:\n\[|\Z)', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\[Context\]\s*\n.*?(?:\n\[|\Z)', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\[Agent Memory[^\]]*\]\s*\n.*?(?:\n\[|\Z)', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\[Thread Context\]\s*\n.*?(?:\n\[|\Z)', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\[Conversation Context\]\s*\n.*?(?:\n\[|\Z)', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'^\[Buzz event[^\]]*\]\s*\n', '', cleaned)
    cleaned = re.sub(r'^Event ID:.*?\n', '', cleaned)
    cleaned = re.sub(r'^Channel:.*?\n', '', cleaned)
    cleaned = re.sub(r'^Kind:.*?\n', '', cleaned)
    cleaned = re.sub(r'^From:.*?\n', '', cleaned)
    cleaned = re.sub(r'^Time:.*?\n', '', cleaned)
    cleaned = re.sub(r'^Content:\s*', '', cleaned)
    cleaned = re.sub(r'^Tags:.*\Z', '', cleaned, flags=re.DOTALL)
    return cleaned.strip()


# ---------------------------------------------------------------------------
# Buzz CLI — post reply to channel
# ---------------------------------------------------------------------------
def _post_to_buzz(channel_id: str, content: str, reply_to: str | None = None) -> bool:
    """Post a reply to a Buzz channel using buzz-cli."""
    if not channel_id:
        log.error("cannot post to buzz: no channel_id in context")
        return False

    cmd = [BUZZ_CLI, "messages", "send",
           "--channel", channel_id,
           "--content", "-"]

    if reply_to:
        cmd.extend(["--reply-to", reply_to])

    try:
        result = subprocess.run(
            cmd,
            input=content,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            log.info("posted reply to channel %s (reply_to=%s)", channel_id, reply_to or "none")
            return True
        else:
            log.error("buzz-cli failed (rc=%d): %s", result.returncode, result.stderr.strip())
            return False
    except Exception as exc:
        log.error("buzz-cli exception: %s", exc)
        return False


# ---------------------------------------------------------------------------
# OpenClaw call
# ---------------------------------------------------------------------------
def _call_openclaw(session_id: str, user_text: str, system_prompt: str,
                   cancel: threading.Event) -> str:
    with _sessions_lock:
        session = _sessions.setdefault(session_id, {"history": [], "system_prompt": system_prompt})
        history = session["history"]
        # Build messages: system prompt first, then conversation history
        messages = []
        sys_content = session["system_prompt"] or system_prompt
        if sys_content:
            messages.append({"role": "system", "content": sys_content})
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})

    url     = f"{OPENCLAW_URL.rstrip('/')}/v1/chat/completions"
    payload = json.dumps({
        "model":       "openclaw",
        "messages":    messages,
        "stream":      True,
        "session_key": SESSION_KEY,
    }).encode()
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream"}
    if OPENCLAW_API_KEY:
        headers["Authorization"] = f"Bearer {OPENCLAW_API_KEY}"

    req    = Request(url, data=payload, headers=headers, method="POST")
    chunks = []

    try:
        with urlopen(req, timeout=300) as resp:
            for raw in resp:
                if cancel.is_set():
                    break
                line = raw.decode("utf-8").rstrip()
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                token = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if token:
                    chunks.append(token)
                    _notify("agent/stream", {"session_id": session_id, "content": token})
    except (HTTPError, URLError) as exc:
        log.error("OpenClaw request failed: %s", exc)
        raise

    reply = "".join(chunks)
    with _sessions_lock:
        _sessions[session_id]["history"].append({"role": "user", "content": user_text})
        _sessions[session_id]["history"].append({"role": "assistant", "content": reply})
    return reply


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def _handle_initialize(req_id, params: dict) -> None:
    log.info("initialize from %s", params.get("client_info", {}).get("name", "?"))
    _respond(req_id, {
        "protocolVersion": ACP_VERSION,
        "serverInfo": {"name": f"buzz-acp ({AGENT_NAME})", "version": "1.1.0"},
        "capabilities": CAPABILITIES,
    })


def _handle_session_new(req_id, params: dict) -> None:
    """Handle session/new — buzz-acp sends systemPrompt with base_prompt.md."""
    session_id = str(uuid.uuid4())
    system_prompt = params.get("systemPrompt", "") or ""

    # For legacy agents (protocol v1), buzz-acp delivers base_prompt inside
    # the prompt text instead of via systemPrompt. For v2 agents, it's here.
    # We handle both: capture systemPrompt if present, and also parse [Base]
    # from the prompt text if not.
    with _sessions_lock:
        _sessions[session_id] = {"history": [], "system_prompt": system_prompt}

    log.info("session/new id=%s sysprompt_len=%d params_keys=%s",
             session_id, len(system_prompt), list(params.keys()))
    if system_prompt:
        log.info("session/new systemPrompt preview: %s", system_prompt[:200])

    _respond(req_id, {"sessionId": session_id})


def _extract_user_text(params: dict) -> str:
    """Extract user text from session/prompt prompt array or agent/run messages."""
    # session/prompt: params.prompt is a list of {type, text} blocks
    prompt = params.get("prompt")
    if prompt is not None:
        parts = []
        for block in prompt:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)

    # agent/run: params.messages is a list of {role, content}
    messages = params.get("messages", [])
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "")
    return ""


def _handle_session_prompt(req_id, params: dict) -> None:
    """Handle session/prompt — buzz-acp's main message delivery method.

    Flow:
    1. Extract the full prompt text (contains [Base], [Context], [Event] blocks)
    2. Parse channel UUID and reply-to from [Context]
    3. Extract the actual user message from [Event]
    4. If no systemPrompt was delivered in session/new, parse [Base] from the prompt
    5. Call OpenClaw for the reply
    6. Post the reply to the Buzz channel using buzz-cli
    7. Return stopReason to buzz-acp
    """
    session_id = params.get("sessionId") or params.get("session_id") or str(uuid.uuid4())
    raw_prompt = _extract_user_text(params)

    # Ensure session exists
    with _sessions_lock:
        if session_id not in _sessions:
            _sessions[session_id] = {"history": [], "system_prompt": ""}

    if not raw_prompt:
        _respond(req_id, {"stopReason": "end_turn"})
        return

    log.info("session/prompt session=%s prompt_len=%d", session_id, len(raw_prompt))

    # Parse context from the prompt
    ctx = _parse_context(raw_prompt)
    event_id = _parse_event_id(raw_prompt)
    channel_id = ctx["channel_id"]
    reply_to = ctx["reply_to"] or event_id

    log.info("context: channel=%s scope=%s reply_to=%s",
             channel_id, ctx["scope"], reply_to or "none")

    # If no systemPrompt was delivered via session/new, try to extract [Base] from prompt
    with _sessions_lock:
        if not _sessions[session_id]["system_prompt"]:
            # Legacy agent path: base_prompt is in the prompt text as [Base] section
            base_match = re.search(
                r'\[Base\]\s*\n(.*?)(?:\n\[|\Z)',
                raw_prompt,
                re.DOTALL
            )
            if base_match:
                _sessions[session_id]["system_prompt"] = base_match.group(1).strip()
                log.info("extracted [Base] section (%d chars) from prompt text",
                         len(_sessions[session_id]["system_prompt"]))

    # Extract the actual user message
    user_message = _extract_user_message(raw_prompt)

    if not user_message:
        log.warning("could not extract user message from prompt, using raw prompt")
        user_message = raw_prompt

    log.info("user message: %s", user_message[:200])

    cancel = threading.Event()
    _active_runs[req_id] = cancel

    try:
        # 1. Get reply from OpenClaw
        system_prompt = _sessions.get(session_id, {}).get("system_prompt", "")
        reply = _call_openclaw(session_id, user_message, system_prompt, cancel)

        if cancel.is_set():
            _respond(req_id, {"stopReason": "cancelled"})
            return

        log.info("openclaw reply (%d chars): %s", len(reply), reply[:200])

        # 2. Post the reply to the Buzz channel
        if channel_id and reply.strip():
            posted = _post_to_buzz(channel_id, reply.strip(), reply_to)
            if posted:
                log.info("reply posted to buzz channel %s", channel_id)
            else:
                log.error("failed to post reply to buzz channel %s", channel_id)
        else:
            log.warning("no channel_id or empty reply — cannot post to buzz (channel=%s, reply_len=%d)",
                       channel_id, len(reply))

        _respond(req_id, {"stopReason": "end_turn"})

    except Exception as exc:
        log.error("session/prompt failed: %s", exc)
        _error(req_id, -32000, f"OpenClaw error: {exc}")
    finally:
        _active_runs.pop(req_id, None)


def _handle_session_end(req_id, params: dict) -> None:
    """Clean up a session."""
    session_id = params.get("sessionId") or params.get("session_id", "")
    with _sessions_lock:
        _sessions.pop(session_id, None)
    log.info("session/end id=%s", session_id)
    _respond(req_id, {})


def _handle_session_cancel(req_id, params: dict) -> None:
    """Cancel an in-flight prompt (notification — may not have req_id)."""
    target = params.get("id") or params.get("req_id")
    ev = _active_runs.get(target)
    if ev:
        ev.set()
        log.info("session/cancel: cancelled %s", target)
    if req_id is not None:
        _respond(req_id, {"cancelled": ev is not None})


def _handle_session_set_config_option(req_id, params: dict) -> None:
    """No-op — acknowledge and ignore."""
    _respond(req_id, {})


def _handle_session_set_model(req_id, params: dict) -> None:
    """No-op — acknowledge and ignore."""
    _respond(req_id, {})


def _handle_agent_run(req_id, params: dict) -> None:
    """Legacy agent/run handler (some ACP clients still use this)."""
    session_id = params.get("session_id") or str(uuid.uuid4())
    user_text = _extract_user_text(params)

    with _sessions_lock:
        if session_id not in _sessions:
            _sessions[session_id] = {"history": [], "system_prompt": ""}

    if not user_text:
        _respond(req_id, {"session_id": session_id, "content": "", "stop_reason": "end_turn"})
        return

    log.info("agent/run session=%s len=%d", session_id, len(user_text))
    cancel = threading.Event()
    _active_runs[req_id] = cancel

    try:
        system_prompt = _sessions.get(session_id, {}).get("system_prompt", "")
        reply = _call_openclaw(session_id, user_text, system_prompt, cancel)
        stop_reason = "cancelled" if cancel.is_set() else "end_turn"
        _respond(req_id, {"session_id": session_id, "content": reply, "stop_reason": stop_reason})
    except Exception as exc:
        _error(req_id, -32000, f"OpenClaw error: {exc}")
    finally:
        _active_runs.pop(req_id, None)


def _handle_agent_cancel(req_id, params: dict) -> None:
    """Legacy cancel handler."""
    target = params.get("id")
    ev = _active_runs.get(target)
    if ev:
        ev.set()
        log.info("agent/cancel: cancelled %s", target)
    _respond(req_id, {"cancelled": ev is not None})


HANDLERS = {
    "initialize":                  _handle_initialize,
    "session/new":                _handle_session_new,
    "session/prompt":             _handle_session_prompt,
    "session/end":                _handle_session_end,
    "session/cancel":             _handle_session_cancel,
    "session/set_config_option":  _handle_session_set_config_option,
    "session/set_model":           _handle_session_set_model,
    "agent/run":                  _handle_agent_run,
    "agent/cancel":               _handle_agent_cancel,
}


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main() -> None:
    log.info("starting — agent=%s relay=%s session=%s buzz_cli=%s",
             AGENT_NAME, OPENCLAW_URL, SESSION_KEY, BUZZ_CLI)
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            msg = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            log.warning("bad JSON: %s", exc)
            continue

        req_id  = msg.get("id")
        method  = msg.get("method", "")
        params  = msg.get("params", {})
        handler = HANDLERS.get(method)

        if handler is None:
            log.warning("unknown method: %s", method)
            if req_id is not None:
                _error(req_id, -32601, f"Method not found: {method}")
            continue

        # Each request in its own thread — keeps read loop unblocked
        threading.Thread(target=handler, args=(req_id, params), daemon=True).start()

    log.info("stdin closed — exiting")


if __name__ == "__main__":
    main()
