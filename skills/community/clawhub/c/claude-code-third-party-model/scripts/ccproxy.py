#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccproxy - a minimal, zero-dependency Anthropic <-> OpenAI translation gateway.

Why this exists:
    claude-code-router 2.1.1 emits malformed Anthropic SSE (every event is
    written twice and `message_stop` is never sent), which makes Claude Code
    report "The response stream was malformed". Verified by feeding it a
    textbook-perfect OpenAI SSE stream: still malformed. So we replace it.

What it does:
    POST /v1/messages   (Anthropic Messages API, what Claude Code speaks)
      -> translated into an OpenAI /chat/completions request
      -> sent upstream with http.client, which does not read any of the
         proxy environment variables
      -> translated back, with a strictly spec-shaped Anthropic event stream
         (message_start / content_block_* / message_delta / message_stop).

Config: ~/.claude-code-proxy.json (see DEFAULT_CONFIG below)

Usage: python ccproxy.py [--port N] [--upstream URL] [--model NAME]
"""
import argparse
import hmac
import http.client
import json
import os
import secrets
import socket
import ssl
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".claude-code-proxy.json")

DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port": 3457,
    "upstream": {
        "url": "https://opencode.ai/zen/v1/chat/completions",
        "model": "space-bunny-free",
        "api_key": "",
    },
    "drop_reasoning": True,
    "timeout": 900,
    # Upstream retries for idempotent request shapes. Measured on2026-10-07:
    # a 183KB classifier payload takes the free endpoint 34-47s, and the
    # Cloudflare edge in front of it drops connections that are still being
    # processed at that age. Retrying is safe here because every retried
    # request is a pure ask-for-a-completion with no side effects.
    "retries": 2,
    "retry_backoff": 1.5,
    "verbose": False,
    # Shared secret that local clients must present. Auto-generated on first
    # start so that no other local process can silently use the upstream
    # credential this gateway is configured with. Keep it in sync with the
    # ANTHROPIC_AUTH_TOKEN your client sends (ccswitch.py does this for you).
    "client_token": "",
}

# Values that must never be accepted as a real token.
PLACEHOLDER_TOKENS = {"", "router-local", "local", "changeme", "your-token"}

STOP_MAP = {
    "stop": "end_turn",
    "length": "max_tokens",
    "tool_calls": "tool_use",
    "function_call": "tool_use",
    "content_filter": "end_turn",
}

VALID_STOP = {"end_turn", "max_tokens", "stop_sequence", "tool_use", "pause_turn", "refusal"}


def log(*a):
    if CONFIG.get("verbose"):
        sys.stderr.write("[ccproxy] " + " ".join(str(x) for x in a) + "\n")
        sys.stderr.flush()


def log_always(*a):
    """Like log(), but never suppressed by the verbose flag.

    Real faults must be visible in the default launcher, which does not pass
    --verbose; routine chatter stays behind verbose.
    """
    sys.stderr.write("[ccproxy] " + " ".join(str(x) for x in a) + "\n")
    sys.stderr.flush()


def load_config():
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                user = json.load(f)
            for k, v in user.items():
                if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                    cfg[k].update(v)
                else:
                    cfg[k] = v
        except Exception as e:
            sys.stderr.write("[ccproxy] bad config %s: %s\n" % (CONFIG_PATH, e))
    return cfg


def save_client_token(token):
    """Persist only the client token, leaving the user's other settings alone.

    Command-line overrides (port, upstream, verbose) must not leak into the
    config file, so we re-read what is on disk and patch a single key.
    """
    user = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                user = json.load(f)
        except Exception:
            user = {}
    if not isinstance(user, dict):
        user = {}
    user["client_token"] = token
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(user, f, indent=2, ensure_ascii=False)
            f.write("\n")
        try:
            os.chmod(CONFIG_PATH, 0o600)
        except OSError:
            pass
    except OSError as e:
        sys.stderr.write("[ccproxy] cannot persist token to %s: %s\n"
                         % (CONFIG_PATH, e))


def ensure_client_token(cfg):
    """Return the shared client token, generating one on first start.

    Without a token the gateway answers any local process, which could then
    spend the configured upstream credential on its own prompts. Generating it
    here keeps the default install safe without any setup step.
    """
    token = str(cfg.get("client_token") or "").strip()
    if token in PLACEHOLDER_TOKENS:
        token = secrets.token_urlsafe(24)
        cfg["client_token"] = token
        save_client_token(token)
        sys.stderr.write(
            "[ccproxy] generated a client token and saved it to %s\n"
            "[ccproxy] clients must present it as x-api-key "
            "(or Authorization: Bearer)\n" % CONFIG_PATH)
    return token


CONFIG = {}


# --------------------------------------------------------------- request side
def _text_of(content):
    """Flatten an Anthropic content value into plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for b in content:
            if not isinstance(b, dict):
                parts.append(str(b))
                continue
            t = b.get("type")
            if t == "text":
                parts.append(b.get("text", ""))
            elif t == "tool_result":
                parts.append(_text_of(b.get("content")))
            elif t == "image":
                parts.append("[image omitted]")
            else:
                parts.append(json.dumps(b, ensure_ascii=False))
    return "\n".join(p for p in parts if p)


def anthropic_to_openai(req):
    """Anthropic Messages request -> OpenAI chat.completions request."""
    msgs = []

    system = req.get("system")
    if system:
        msgs.append({"role": "system", "content": _text_of(system)})

    for m in req.get("messages", []):
        role = m.get("role")
        content = m.get("content")

        if isinstance(content, str):
            msgs.append({"role": role, "content": content})
            continue

        if not isinstance(content, list):
            msgs.append({"role": role, "content": _text_of(content)})
            continue

        # A user turn may carry tool_result blocks; OpenAI wants those as
        # separate role="tool" messages, so we split them out in order.
        texts, tool_results, tool_calls = [], [], []
        for b in content:
            if not isinstance(b, dict):
                texts.append(str(b))
                continue
            t = b.get("type")
            if t == "text":
                texts.append(b.get("text", ""))
            elif t == "tool_result":
                tool_results.append(b)
            elif t == "tool_use":
                tool_calls.append(b)
            elif t == "image":
                texts.append("[image omitted]")

        joined = "\n".join(x for x in texts if x)

        if tool_results:
            if joined:
                msgs.append({"role": role, "content": joined})
            for tr in tool_results:
                body = tr.get("content")
                out = _text_of(body)
                if tr.get("is_error"):
                    out = "ERROR: " + out
                msgs.append({
                    "role": "tool",
                    "tool_call_id": tr.get("tool_use_id") or "unknown",
                    "content": out or "(empty)",
                })
            continue

        if tool_calls:
            oa_calls = []
            for tc in tool_calls:
                args = tc.get("input")
                oa_calls.append({
                    "id": tc.get("id") or ("call_" + uuid.uuid4().hex[:20]),
                    "type": "function",
                    "function": {
                        "name": tc.get("name", ""),
                        "arguments": json.dumps(args if args is not None else {},
                                                ensure_ascii=False),
                    },
                })
            msg = {"role": "assistant", "tool_calls": oa_calls}
            if joined:
                msg["content"] = joined
            msgs.append(msg)
            continue

        msgs.append({"role": role, "content": joined})

    out = {
        "model": CONFIG["upstream"].get("model", "unknown"),
        "messages": msgs,
        "stream": bool(req.get("stream")),
    }

    if req.get("max_tokens"):
        out["max_tokens"] = req["max_tokens"]
    for k in ("temperature", "top_p"):
        if req.get(k) is not None:
            out[k] = req[k]
    if req.get("stop_sequences"):
        out["stop"] = req["stop_sequences"]

    tools = req.get("tools")
    if tools:
        oa_tools = []
        for t in tools:
            oa_tools.append({
                "type": "function",
                "function": {
                    "name": t.get("name", ""),
                    "description": t.get("description", ""),
                    "parameters": t.get("input_schema") or {"type": "object", "properties": {}},
                },
            })
        out["tools"] = oa_tools
        tc = req.get("tool_choice") or {}
        ct = tc.get("type")
        if ct == "any":
            out["tool_choice"] = "required"
        elif ct == "tool" and tc.get("name"):
            out["tool_choice"] = {"type": "function", "function": {"name": tc["name"]}}
        elif ct == "none":
            out["tool_choice"] = "none"
        else:
            out["tool_choice"] = "auto"

    # Reasoning hints: map Anthropic's thinking budget onto reasoning_effort.
    th = req.get("thinking") or {}
    if isinstance(th, dict) and th.get("type") == "enabled":
        budget = th.get("budget_tokens") or 0
        out["reasoning_effort"] = "high" if budget >= 8000 else (
            "medium" if budget >= 2000 else "low")

    out["messages"] = _repair_message_sequence(msgs)

    return out


def _repair_message_sequence(msgs):
    """Fix tool-result ordering the upstream rejects with a bare 400.

    Claude Code legitimately emits a user turn *between* an assistant's
    tool_use block and its tool_result blocks (AskUserQuestion answers, hook
    output, interrupt-style input). Flattening that into OpenAI form produces

        assistant(tool_calls) -> user -> tool

    where the ``user`` message separates the assistant from its own tool
    result. Strict OpenAI-compatible gateways reject that shape, and some
    (OpenCode Zen's anonymous ``space-bunny-free``) answer only
    ``invalid_request_error: invalid request`` with no hint about which message
    is at fault -- so the request just fails intermittently mid-session.

    The fix is to let the tool results follow their assistant directly, keeping
    whatever the interrupting user turn said. Nothing is dropped: the tool
    result becomes the assistant's answer and the user's text is prepended to
    it, which preserves both the tool output and the user's input.

    Returns a new list; the input is left untouched.
    """
    out = []
    i = 0
    n = len(msgs)
    while i < n:
        m = msgs[i]
        if m.get("role") != "tool":
            out.append(m)
            i += 1
            continue

        # A run of consecutive tool messages starting here.
        run = []
        while i < n and msgs[i].get("role") == "tool":
            run.append(msgs[i])
            i += 1

        # If the tail of what we emitted so far is a user/system run, it was
        # pushed in front of these results. Move that whole run back after
        # them, folding its text into the first result so nothing is lost.
        tail = []
        while out and out[-1].get("role") in ("user", "system"):
            tail.insert(0, out.pop())
        if tail:
            text = "\n\n".join(
                str(x.get("content", "")).strip() for x in tail
                if str(x.get("content", "")).strip()
            )
            if text:
                first = dict(run[0])
                first["content"] = text + "\n\n" + str(first.get("content", ""))
                run[0] = first
        out.extend(run)
    return out


def estimate_tokens(text):
    if not text:
        return 0
    return max(1, int(len(text) / 3.5))


# -------------------------------------------------------------- debug helper
# Upstream 400s are intermittent and the wrapped error text is useless
# ("invalid request" tells us nothing). When the upstream rejects a request we
# dump the exact OpenAI body we sent plus a little context to
# ~/.claude-code-proxy-failures.jsonl so the real cause can be inspected
# offline instead of guessed at. Purely diagnostic: never touches the reply
# path, and the file only grows when the upstream actually errors.
FAIL_LOG_PATH = os.path.join(os.path.expanduser("~"), ".claude-code-proxy-failures.jsonl")
_FAIL_DUMP_ENABLED = os.environ.get("CCPROXY_DUMP_FAILED", "1") not in ("0", "false", "no")
_FAIL_DUMP_MAX_BYTES = 256 * 1024


def _summarize_oa_body(oa_req):
    """Field-level overview so a huge body is readable at a glance."""
    msgs = oa_req.get("messages") or []
    roles = [m.get("role") for m in msgs]
    out = {
        "model": oa_req.get("model"),
        "stream": oa_req.get("stream"),
        "max_tokens": oa_req.get("max_tokens"),
        "reasoning_effort": oa_req.get("reasoning_effort"),
        "tool_choice": oa_req.get("tool_choice"),
        "n_tools": len(oa_req.get("tools") or []),
        "n_messages": len(msgs),
        "roles": roles,
        "stop": oa_req.get("stop"),
        "top_keys": sorted(oa_req.keys()),
    }
    # Anything that is not a plain string is a shape risk worth flagging.
    odd = []
    for i, m in enumerate(msgs):
        c = m.get("content")
        if c is None:
            odd.append({"i": i, "role": m.get("role"), "issue": "content=null"})
        elif not isinstance(c, str):
            odd.append({"i": i, "role": m.get("role"), "issue": "content not a string",
                        "type": type(c).__name__})
        if m.get("role") == "tool" and not m.get("tool_call_id"):
            odd.append({"i": i, "role": "tool", "issue": "missing tool_call_id"})
    out["anomalies"] = odd
    return out


def _dump_failed_request(oa_req, anthropic_req, status, detail):
    if not _FAIL_DUMP_ENABLED:
        return
    try:
        rec = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "upstream_status": status,
            "upstream_error": detail[:600],
            "anthropic_model": anthropic_req.get("model"),
            "anthropic_stream": anthropic_req.get("stream"),
            "anthropic_top_keys": sorted(anthropic_req.keys()),
            "summary": _summarize_oa_body(oa_req),
            "openai_body": oa_req,
        }
        # Keep the file bounded: truncate the body if it has grown huge.
        body = json.dumps(rec, ensure_ascii=False)
        if len(body) > _FAIL_DUMP_MAX_BYTES:
            rec["openai_body"] = "<omitted: body too large, %d bytes>" % len(
                json.dumps(oa_req, ensure_ascii=False))
            rec["summary"]["openai_body_bytes"] = len(
                json.dumps(oa_req, ensure_ascii=False))
            body = json.dumps(rec, ensure_ascii=False)
        with open(FAIL_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(body + "\n")
    except Exception as e:
        sys.stderr.write("[ccproxy] failed-request dump skipped: %s\n" % e)


# -------------------------------------------------------------- response side
def resolve_upstream_proxy(u):
    """Decide whether to reach the upstream through a proxy.

    Explicit config wins; otherwise fall back to the standard proxy
    environment variables. Returns (use_proxy, proxy_url).
    """
    up = CONFIG.get("upstream", {})
    explicit = up.get("proxy")
    if explicit is not None:
        if not explicit:
            return False, ""
        return True, explicit

    scheme_key = "HTTPS_PROXY" if u.scheme == "https" else "HTTP_PROXY"
    for k in (scheme_key, scheme_key.lower()):
        v = os.environ.get(k) or ""
        if v:
            return True, v
    # A generic all_proxy should still work for the http scheme fallback.
    if u.scheme != "https":
        v = os.environ.get("ALL_PROXY") or os.environ.get("all_proxy") or ""
        if v:
            return True, v
    return False, ""


def upstream_request(oa_req):
    u = urlparse(CONFIG["upstream"]["url"])
    timeout = CONFIG.get("timeout", 900)
    scheme = u.scheme
    host = u.hostname
    port = u.port or (443 if scheme == "https" else 80)
    use_proxy, proxy_url = resolve_upstream_proxy(u)

    if use_proxy:
        # CONNECT tunnel: we speak TLS end-to-end with the origin, so the
        # proxy only relays bytes. This keeps the request-target in origin
        # form, which streaming requires, while still using the proxy path.
        pc = urlparse(proxy_url)
        pport = pc.port or (443 if pc.scheme == "https" else 80)
        conn = http.client.HTTPSConnection(
            pc.hostname, pport, timeout=timeout,
            context=ssl.create_default_context())
        conn.set_tunnel(host, port)
    elif scheme == "https":
        conn = http.client.HTTPSConnection(
            host, port, timeout=timeout,
            context=ssl.create_default_context())
    else:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
    path = u.path or "/"
    if u.query:
        path += "?" + u.query
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream" if oa_req.get("stream") else "application/json",
        # Required. Python's client stack is identified as a known bot by
        # Cloudflare's WAF, which answers with 403 "error code: 1010" when the
        # request leaves via a proxy egress IP. The refusal surfaces here as an
        # opaque reset/timeout, which is easy to misread as "upstream down".
        # Note: bare http.client may send no User-Agent at all, in which case the
        # refusal looks like a plain connection failure rather than a 403.
        "User-Agent": "ccproxy/1.0 (+local gateway)",
    }
    key = CONFIG["upstream"].get("api_key") or ""
    if key:
        headers["Authorization"] = "Bearer " + key
    body = json.dumps(oa_req, ensure_ascii=False).encode("utf-8")
    conn.request("POST", path, body=body, headers=headers)
    return conn, conn.getresponse()


def _is_retryable_upstream_error(e):
    """Only retry transport faults, never a decision the upstream made.

    A 4xx/5xx that arrived as a real response is excluded on purpose: those
    are answers, not accidents, and replaying them wastes the user's time.
    """
    if isinstance(e, (ConnectionResetError, ConnectionAbortedError,
                      BrokenPipeError, ConnectionRefusedError)):
        return True
    if isinstance(e, http.client.RemoteDisconnected):
        return True
    if isinstance(e, http.client.IncompleteRead):
        return True
    if isinstance(e, (socket.timeout, TimeoutError)):
        return True
    if isinstance(e, OSError):
        # Connection-not-established and friends. SSL errors are deliberately
        # excluded: a TLS failure is usually a proxy misconfiguration and
        # retrying through the same path just repeats it.
        return e.errno in (10054, 10060, 10061, 10065, 111, 113)
    return False


def open_upstream_with_retry(oa_req):
    """Open the upstream, retrying transport faults.

    Returns (conn, resp, attempts). Raises the last error if every attempt
    failed. The caller must close whichever conn it ends up with, so failed
    attempts are closed here rather than leaked.
    """
    attempts = CONFIG.get("retries", 0)
    if not isinstance(attempts, int) or attempts < 0:
        attempts = 0
    backoff = CONFIG.get("retry_backoff", 1.5)
    try:
        backoff = float(backoff)
    except (TypeError, ValueError):
        backoff = 1.5

    last = None
    for i in range(attempts + 1):
        conn = None
        try:
            conn, resp = upstream_request(oa_req)
            return conn, resp, i + 1
        except Exception as e:
            last = e
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
            if i >= attempts or not _is_retryable_upstream_error(e):
                raise
            delay = backoff * (2 ** i)
            log_always("upstream %s on attempt %d/%d, retrying in %.1fs: %s"
                       % (type(e).__name__, i + 1, attempts + 1, delay, e))
            time.sleep(delay)
    raise last


def openai_to_anthropic(resp, model):
    """Non-streaming OpenAI completion -> Anthropic message."""
    choice = (resp.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    content = []

    text = msg.get("content")
    if text:
        content.append({"type": "text", "text": text})

    for tc in (msg.get("tool_calls") or []):
        fn = tc.get("function") or {}
        try:
            args = json.loads(fn.get("arguments") or "{}")
        except Exception:
            args = {"_raw": fn.get("arguments")}
        content.append({
            "type": "tool_use",
            "id": tc.get("id") or ("toolu_" + uuid.uuid4().hex[:20]),
            "name": fn.get("name", ""),
            "input": args,
        })

    if not content:
        content.append({"type": "text", "text": ""})

    fr = choice.get("finish_reason") or "stop"
    usage = resp.get("usage") or {}
    return {
        "id": "msg_" + uuid.uuid4().hex[:24],
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": content,
        "stop_reason": STOP_MAP.get(fr, "end_turn"),
        "stop_sequence": None,
        "usage": {
            "input_tokens": usage.get("prompt_tokens") or 0,
            "output_tokens": usage.get("completion_tokens") or 0,
        },
    }


class StreamTranslator(object):
    """Turn an OpenAI SSE stream into a strictly-shaped Anthropic event stream.

    Invariants enforced (the exact things claude-code-router got wrong):
      * exactly one message_start, and it is the first event
      * content blocks are opened, filled and closed in index order
      * exactly one message_delta carrying a real stop_reason
      * exactly one message_stop, always emitted, even on upstream failure
      * every event is written once
    """

    def __init__(self, model, input_chars):
        self.model = model
        self.msg_id = "msg_" + uuid.uuid4().hex[:24]
        self.input_tokens = estimate_tokens(" " * input_chars)
        self.out_chars = 0
        self.blocks = []          # list of {"idx":int,"kind":"text"|"tool","open":bool}
        self.text_idx = None
        self.tool_by_slot = {}    # upstream tool_call index -> our block index
        self.stop_reason = "end_turn"
        self.started = False
        self.finished = False

    # -- low level ---------------------------------------------------------
    @staticmethod
    def ev(name, data):
        return ("event: %s\ndata: %s\n\n" % (name, json.dumps(data, ensure_ascii=False))
                ).encode("utf-8")

    def start(self):
        self.started = True
        return self.ev("message_start", {
            "type": "message_start",
            "message": {
                "id": self.msg_id, "type": "message", "role": "assistant",
                "model": self.model, "content": [], "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": self.input_tokens, "output_tokens": 0},
            },
        })

    def _open_text(self):
        if self.text_idx is not None:
            return b""
        idx = len(self.blocks)
        self.text_idx = idx
        self.blocks.append({"idx": idx, "kind": "text", "open": True})
        return self.ev("content_block_start", {
            "type": "content_block_start", "index": idx,
            "content_block": {"type": "text", "text": ""},
        })

    def _close(self, idx):
        for b in self.blocks:
            if b["idx"] == idx and b["open"]:
                b["open"] = False
                return self.ev("content_block_stop",
                               {"type": "content_block_stop", "index": idx})
        return b""

    def close_open_blocks(self):
        out = b""
        for b in self.blocks:
            if b["open"]:
                out += self._close(b["idx"])
        return out

    # -- per-chunk ---------------------------------------------------------
    def feed(self, chunk):
        out = b""
        choices = chunk.get("choices") or []
        if not choices:
            return out
        ch = choices[0]
        delta = ch.get("delta") or {}

        text = delta.get("content")
        if text:
            if self.text_idx is None:
                out += self._open_text()
            self.out_chars += len(text)
            out += self.ev("content_block_delta", {
                "type": "content_block_delta", "index": self.text_idx,
                "delta": {"type": "text_delta", "text": text},
            })

        for tc in (delta.get("tool_calls") or []):
            slot = tc.get("index")
            if slot is None:
                slot = len(self.tool_by_slot)
            fn = tc.get("function") or {}

            if slot not in self.tool_by_slot:
                # Do NOT close other open blocks here: upstreams interleave
                # argument deltas across parallel tool calls, so every block
                # stays open until the stream ends (they are closed in index
                # order by finish()).
                idx = len(self.blocks)
                self.tool_by_slot[slot] = idx
                self.blocks.append({
                    "idx": idx, "kind": "tool", "open": True,
                    "id": tc.get("id") or ("toolu_" + uuid.uuid4().hex[:20]),
                    "name": fn.get("name") or "",
                })
                blk = self.blocks[-1]
                out += self.ev("content_block_start", {
                    "type": "content_block_start", "index": idx,
                    "content_block": {
                        "type": "tool_use", "id": blk["id"],
                        "name": blk["name"], "input": {},
                    },
                })
            else:
                idx = self.tool_by_slot[slot]
                blk = self.blocks[idx] if idx < len(self.blocks) else None
                # Some upstreams send the name only on a later chunk.
                if blk and not blk.get("name") and fn.get("name"):
                    blk["name"] = fn["name"]

            args = fn.get("arguments")
            if args:
                out += self.ev("content_block_delta", {
                    "type": "content_block_delta", "index": self.tool_by_slot[slot],
                    "delta": {"type": "input_json_delta", "partial_json": args},
                })

        fr = ch.get("finish_reason")
        if fr:
            self.stop_reason = STOP_MAP.get(fr, "end_turn")

        return out

    # -- tail --------------------------------------------------------------
    def finish(self):
        if self.finished:
            return b""
        self.finished = True
        out = self.close_open_blocks()
        if self.text_idx is None and not self.blocks:
            # Upstream produced nothing usable: still emit a valid empty block
            # so the stream stays well-formed instead of "malformed".
            out += self._open_text() + self._close(0)
        if self.stop_reason not in VALID_STOP:
            self.stop_reason = "end_turn"
        out += self.ev("message_delta", {
            "type": "message_delta",
            "delta": {"stop_reason": self.stop_reason, "stop_sequence": None},
            "usage": {"output_tokens": estimate_tokens(" " * self.out_chars)},
        })
        out += self.ev("message_stop", {"type": "message_stop"})
        return out


class QuietThreadingHTTPServer(ThreadingHTTPServer):
    """ThreadingHTTPServer that treats client disconnects as routine.

    ``socketserver`` prints a full traceback for *any* exception escaping a
    request thread. A client hanging up mid-request is normal traffic, not a
    bug, so classify it here: routine disconnects get a one-line note, and
    anything else is still reported (never silently swallowed).
    """

    CLIENT_GONE = (ConnectionResetError, ConnectionAbortedError, BrokenPipeError)

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, self.CLIENT_GONE):
            log("client %s disconnected" % (client_address,))
            return
        # Timeouts are routine too -- an idle keep-alive socket reaped by the
        # peer looks exactly like this.
        if isinstance(exc, TimeoutError):
            log("client %s timed out" % (client_address,))
            return
        # Anything else is a genuine fault: report it loudly, with a marker
        # that makes it greppable, and still fall back to socketserver's
        # traceback so nothing is lost.
        log_always("UNEXPECTED ERROR handling request from %r: %s: %s"
                   % (client_address, type(exc).__name__, exc))
        super().handle_error(request, client_address)


# -------------------------------------------------------------------- server
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "ccproxy/1.0"

    # -- connection lifecycle ---------------------------------------------
    # Claude Code opens a socket, may abandon it mid-request (Esc, Ctrl-C,
    # a tool it no longer needs), and Windows then reports
    #   ConnectionResetError: [WinError 10054]
    # from socketserver's worker thread. That is normal client behaviour, not
    # a gateway fault -- but left unhandled it dumps a full traceback per
    # occurrence, which buries the log lines that actually matter (real
    # upstream errors). Swallow it and emit one compact line instead.
    def handle_one_request(self):
        try:
            BaseHTTPRequestHandler.handle_one_request(self)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            self.close_connection = True
            log_always("client disconnected before the response was sent "
                       "(harmless - it cancelled the request)")

    def log_message(self, fmt, *args):
        if CONFIG.get("verbose"):
            sys.stderr.write("[ccproxy] " + (fmt % args) + "\n")
            sys.stderr.flush()

    # -- helpers -----------------------------------------------------------
    def _send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self._responded = True

    def _send_error_anthropic(self, code, kind, message):
        self._send_json(code, {"type": "error",
                               "error": {"type": kind, "message": message}})

    def _send_stream_error(self, kind, message):
        """Emit an Anthropic-shaped ``error`` event on an open SSE stream.

        A truncated stream closed with a normal ``message_stop`` is the one
        failure mode clients cannot detect: the turn looks complete, so the
        client shows a half-written answer and quietly stops instead of
        retrying. An ``error`` event is the documented way to say "this
        attempt failed", which is what makes the client retry.
        """
        self.wfile.write(b"event: error\n" + json.dumps({
            "type": "error",
            "error": {"type": kind, "message": message},
        }, ensure_ascii=False).encode("utf-8") + b"\n\n")
        self.wfile.flush()

    # -- auth --------------------------------------------------------------
    def _presented_token(self):
        tok = (self.headers.get("x-api-key") or "").strip()
        if not tok:
            auth = self.headers.get("Authorization") or ""
            if auth.lower().startswith("bearer "):
                tok = auth[7:].strip()
        return tok

    def _authorized(self):
        """Only callers that know the shared token may use this gateway."""
        want = str(CONFIG.get("client_token") or "")
        if not want:
            return False
        got = self._presented_token()
        try:
            return hmac.compare_digest(got, want)
        except TypeError:            # non-ASCII token: fall back to ==
            return got == want

    def _reject_unauthorized(self):
        self._send_error_anthropic(
            401, "authentication_error",
            "missing or invalid client token: send the `client_token` from "
            "%s as x-api-key (or Authorization: Bearer). Trusted local "
            "clients only." % CONFIG_PATH)

    def do_GET(self):
        if urlparse(self.path).path in ("/health", "/", "/status"):
            if not self._authorized():
                self._reject_unauthorized()
                return
            self._send_json(200, {
                "ok": True,
                "service": "ccproxy",
                "pid": os.getpid(),
                "auth": "token",
                "upstream": CONFIG["upstream"].get("url"),
                "model": CONFIG["upstream"].get("model"),
            })
        else:
            self._send_json(404, {"error": "not found"})

    def _drain_request_body(self):
        """Read the request body and return it, keeping the socket reusable.

        With HTTP/1.1 keep-alive, any bytes we fail to consume stay in the
        socket. The next request on that same socket then starts parsing in the
        middle of the leftover body and the client sees
        ``code 400, message Bad request syntax ('{"model":...')`` -- which looks
        like a client bug but is really our leftover. Always call this before
        replying, even on the error paths.

        Returns the raw bytes (b"" when there was no body).
        """
        buf = []
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except (TypeError, ValueError):
            n = 0
        if n > 0:
            remaining = n
            while remaining > 0:
                chunk = self.rfile.read(min(remaining, 65536))
                if not chunk:
                    break
                remaining -= len(chunk)
                buf.append(chunk)
        if (self.headers.get("Transfer-Encoding") or "").lower() == "chunked":
            # De-chunk so the next request starts on a clean boundary.
            while True:
                line = self.rfile.readline(65536).strip()
                if not line:
                    break
                try:
                    size = int(line.split(b";")[0], 16)
                except ValueError:
                    break
                if size == 0:
                    self.rfile.readline(65536)
                    break
                remaining = size
                while remaining > 0:
                    got = self.rfile.read(min(remaining, 65536))
                    if not got:
                        break
                    remaining -= len(got)
                    buf.append(got)
                self.rfile.readline(65536)
        return b"".join(buf)

    # -- token counting ----------------------------------------------------
    def _count_tokens(self, raw):
        """Local token estimate for /v1/messages/count_tokens.

        Claude Code calls this before every request to decide when to
        auto-compact, so it has to return something plausible and, above all,
        must not 404 (a 404 here strands the request body on a keep-alive
        socket and corrupts the *next* request). No tokenizer is available
        offline, so reuse the same char/3.5 heuristic the stream estimator
        uses; it is only ever used for a threshold comparison.
        """
        try:
            req = json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            return 0
        text = _text_of(req.get("system") or "")
        for m in req.get("messages", []):
            text += _text_of(m.get("content") or "")
        for t in req.get("tools", []):
            text += str(t.get("name", "")) + str(t.get("description", ""))
            text += json.dumps(t.get("input_schema") or {}, ensure_ascii=False)
        return estimate_tokens(text)

    def do_POST(self):
        # Reset per-request reply tracking. The error handler uses this to
        # tell "client is still waiting for a response" from "we already
        # answered, nothing more to say" -- getting that backwards either
        # wedges the client or corrupts an in-flight stream.
        self._responded = False
        path = urlparse(self.path).path

        # Always consume the body first: leaving it behind corrupts keep-alive.
        raw = self._drain_request_body()

        # Claude Code calls this to size its context budget. It is a local
        # computation -- we never forwarded it upstream -- so answer it here
        # instead of 404ing and leaving the body on the wire.
        if path == "/v1/messages/count_tokens":
            if not self._authorized():
                self._reject_unauthorized()
                return
            self._send_json(200, {"input_tokens": self._count_tokens(raw)})
            return

        if path != "/v1/messages":
            self._send_error_anthropic(404, "not_found_error", "unsupported path " + path)
            return

        if not self._authorized():
            self._reject_unauthorized()
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw = raw if raw else (self.rfile.read(length) if length else b"{}")
        try:
            req = json.loads(raw.decode("utf-8"))
        except Exception as e:
            self._send_error_anthropic(400, "invalid_request_error", "bad json: %s" % e)
            return

        want_stream = bool(req.get("stream"))
        try:
            oa_req = anthropic_to_openai(req)
        except Exception as e:
            self._send_error_anthropic(400, "invalid_request_error", "translate: %s" % e)
            return

        prompt_chars = sum(len(str(m.get("content", ""))) for m in oa_req["messages"])
        model_for_reply = req.get("model") or CONFIG["upstream"].get("model")

        conn = resp = None
        try:
            conn, resp, _attempts = open_upstream_with_retry(oa_req)
        except Exception as e:
            log_always("upstream connect failed after retries: %s: %s"
                       % (type(e).__name__, e))
            _dump_failed_request(oa_req, req, 599,
                                 "%s: %s" % (type(e).__name__, e))
            self._send_error_anthropic(502, "api_error", "upstream connect failed: %s" % e)
            if conn:
                conn.close()
            return

        try:
            if resp.status != 200:
                detail = resp.read().decode("utf-8", "replace")[:800]
                log("upstream", resp.status, detail)
                _dump_failed_request(oa_req, req, resp.status, detail)
                kind = "authentication_error" if resp.status in (401, 403) else "api_error"
                self._send_error_anthropic(resp.status, kind,
                                           "upstream %s: %s" % (resp.status, detail))
                return

            if not want_stream:
                # A non-streaming upstream can still die mid-body: it may
                # promise a Content-Length and then reset the connection.
                # ``resp.read()`` then blocks forever, the client never gets
                # a reply and never sees an error, so the whole session
                # stalls with no way to recover. Bound the read by the
                # declared length and fail loudly instead of hanging.
                try:
                    raw_body = resp.read()
                except Exception as e:
                    log_always("upstream body read failed mid-flight: %s: %s"
                               % (type(e).__name__, e))
                    self._send_error_anthropic(
                        502, "api_error",
                        "upstream response was truncated: %s" % e)
                    return
                try:
                    data = json.loads(raw_body.decode("utf-8"))
                except Exception as e:
                    log_always("upstream sent unparseable body: %s" % e)
                    self._send_error_anthropic(
                        502, "api_error",
                        "upstream sent an invalid body: %s" % e)
                    return
                self._send_json(200, openai_to_anthropic(data, model_for_reply))
                return

            # ---- streaming ----
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True
            self._responded = True

            tr = StreamTranslator(model_for_reply, prompt_chars)
            self.wfile.write(tr.start())
            self.wfile.flush()

            # Streamed output is already committed to the client once we write
            # a chunk, so a mid-stream retry would duplicate text. Track the
            # high-water mark and only replay while nothing has been emitted;
            # past that point failing loudly beats silently repeating.
            emitted = 0
            mid_retries = CONFIG.get("retries", 0)
            try:
                mid_retries = int(mid_retries)
            except (TypeError, ValueError):
                mid_retries = 0
            attempt = 0
            while True:
                try:
                    for line in resp:
                        line = line.strip()
                        if not line.startswith(b"data:"):
                            continue
                        payload = line[5:].strip()
                        if payload == b"[DONE]":
                            break
                        try:
                            chunk = json.loads(payload.decode("utf-8"))
                        except Exception:
                            continue
                        out = tr.feed(chunk)
                        if out:
                            self.wfile.write(out)
                            self.wfile.flush()
                            emitted += len(out)
                    break
                except Exception as e:
                    # Only safe to replay while the client has seen nothing.
                    # Once bytes are out the only honest options are to fail or
                    # to append -- and appending would repeat the answer.
                    if emitted or attempt >= mid_retries \
                            or not _is_retryable_upstream_error(e):
                        raise
                    attempt += 1
                    delay = float(CONFIG.get("retry_backoff", 1.5)) * (2 ** (attempt - 1))
                    log_always("stream broke before any output (%s), "
                               "reopening upstream attempt %d/%d in %.1fs: %s"
                               % (type(e).__name__, attempt, mid_retries + 1, delay, e))
                    try:
                        resp.close()
                    except Exception:
                        pass
                    time.sleep(delay)
                    conn, resp, _ = open_upstream_with_retry(oa_req)

            self.wfile.write(tr.finish())
            self.wfile.flush()
        except Exception as e:
            log_always("stream error: %s: %s" % (type(e).__name__, e))
            _dump_failed_request(oa_req, req, 599, "%s: %s" % (type(e).__name__, e))
            # Never leave the client hanging. But do NOT close the stream with
            # a normal message_stop: that makes a truncated answer look
            # complete, so the client keeps it and silently stops instead of
            # retrying. Tell the client the attempt failed.
            try:
                if want_stream and getattr(self, "wfile", None):
                    self._send_stream_error(
                        "api_error",
                        "upstream stream failed after %d characters: %s"
                        % (getattr(locals().get("tr"), "out_chars", 0), e))
                elif not getattr(self, "_responded", False):
                    # Nothing has been written yet, so the client is still
                    # waiting for a response that will never come unless we
                    # send one. Sending nothing is what wedges the session.
                    self._send_error_anthropic(
                        502, "api_error",
                        "upstream request failed: %s: %s"
                        % (type(e).__name__, e))
            except Exception:
                # The client is already gone; nothing left to tell it.
                pass
            finally:
                # Whatever happened, do not leave the socket half-open: a
                # keep-alive connection with no response stalls the client
                # until its own timeout expires.
                self.close_connection = True
        finally:
            try:
                if resp:
                    resp.close()
            except Exception:
                pass
            try:
                if conn:
                    conn.close()
            except Exception:
                pass


def main():
    global CONFIG
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--port", type=int)
    ap.add_argument("--host")
    ap.add_argument("--upstream")
    ap.add_argument("--model")
    ap.add_argument("--key")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    CONFIG = load_config()
    if args.port:
        CONFIG["port"] = args.port
    if args.host:
        CONFIG["host"] = args.host
    if args.upstream:
        CONFIG["upstream"]["url"] = args.upstream
    if args.model:
        CONFIG["upstream"]["model"] = args.model
    if args.key is not None:
        CONFIG["upstream"]["api_key"] = args.key
    if args.verbose:
        CONFIG["verbose"] = True

    ensure_client_token(CONFIG)

    # Print the resolved upstream path at startup. A proxy that resolves at
    # start but dies later is otherwise invisible: every request fails with a
    # bare 10061 and the log never says a proxy was even involved.
    _u = urlparse(CONFIG["upstream"]["url"])
    _use_proxy, _proxy = resolve_upstream_proxy(_u)
    sys.stderr.write("[ccproxy] upstream route: %s\n"
                     % (("proxy %s" % _proxy) if _use_proxy else "direct"))
    sys.stderr.write("[ccproxy] upstream retries: %s (backoff %s)\n"
                     % (CONFIG.get("retries"), CONFIG.get("retry_backoff")))

    host, port = CONFIG["host"], CONFIG["port"]
    srv = QuietThreadingHTTPServer((host, port), Handler)
    srv.daemon_threads = True
    sys.stderr.write(
        "[ccproxy] listening on http://%s:%d  ->  %s (%s)\n"
        % (host, port, CONFIG["upstream"]["url"], CONFIG["upstream"]["model"]))
    sys.stderr.write("[ccproxy] auth required: send the client token from %s\n"
                     % CONFIG_PATH)
    if host not in ("127.0.0.1", "localhost", "::1"):
        sys.stderr.write(
            "[ccproxy] WARNING: %s is not a loopback address - this gateway "
            "would be reachable from the network and could spend your "
            "upstream credential. Prefer 127.0.0.1.\n" % host)
    if not CONFIG["upstream"].get("api_key"):
        sys.stderr.write("[ccproxy] upstream api_key is empty (keyless upstream)\n")
    sys.stderr.flush()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
