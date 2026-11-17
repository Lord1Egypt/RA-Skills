#!/usr/bin/env python3
"""MCP schema probe (stdlib only).

Measures the JSON byte size of the ``tools`` array returned by an MCP server.
Never prints or stores tokens, request messages, headers, or prompts.

Usage:
  mcp_probe.py --stdio --name lis-skill-bus -- /path/server serve
  mcp_probe.py --http https://host/mcp --name github --bearer-env GITHUB_PAT_TOKEN
  mcp_probe.py --disabled --name cua_repl --note "CLI disabled"

Output (single JSON object):
  server, transport, tool_count, tools_bytes, total_bytes,
  status(measured/disabled/unmeasurable), error
"""

from __future__ import annotations

import argparse
import codecs
import hashlib
import json
import os
import queue
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

PROTOCOL_VERSION = "2025-06-18"
CLIENT_INFO = {"name": "mcp-probe", "version": "1.0.0"}


def compact_bytes(value: Any) -> int:
    """UTF-8 bytes of compact JSON (no ASCII escaping)."""
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def tool_details(tools: List[Any]) -> Dict[str, Any]:
    names = [str(t.get("name")) for t in tools if isinstance(t, dict)]
    sizes = []
    for t in tools:
        if isinstance(t, dict):
            sizes.append({"name": str(t.get("name")), "bytes": compact_bytes(t)})
    sizes.sort(key=lambda x: -int(x["bytes"]))
    blob = json.dumps(tools, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return {
        "tool_names": names,
        "tools_sha256_12": hashlib.sha256(blob).hexdigest()[:12],
        "largest_tools": sizes[:5],
    }


def make_result(server: str, transport: str, status: str,
                tool_count: int = 0, tools_bytes: int = 0,
                total_bytes: int = 0, error: Optional[str] = None,
                extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "server": server,
        "transport": transport,
        "tool_count": tool_count,
        "tools_bytes": tools_bytes,
        "total_bytes": total_bytes,
        "status": status,
        "error": error,
    }
    if extra:
        out.update(extra)
    return out


def tools_from_messages(messages: List[Dict[str, Any]]) -> Tuple[List[Any], Optional[str]]:
    """Merge tools from one or more tools/list responses (pagination)."""
    tools: List[Any] = []
    cursor_seen = None
    for msg in messages:
        result = msg.get("result") if isinstance(msg, dict) else None
        if not isinstance(result, dict):
            continue
        page = result.get("tools")
        if isinstance(page, list):
            tools.extend(page)
        cursor_seen = result.get("nextCursor")
    return tools, cursor_seen


# --------------------------------------------------------------------------
# stdio transport
# --------------------------------------------------------------------------

class StdioSession:
    def __init__(self, cmd: List[str], timeout: float):
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=os.environ.copy(),
        )
        self.timeout = timeout
        self.lines: "queue.Queue[Optional[str]]" = queue.Queue()
        self.stderr_tail: List[str] = []
        self._buf = ""
        self._buf_lock = threading.Lock()
        threading.Thread(target=self._read_stdout, daemon=True).start()
        threading.Thread(target=self._read_stderr, daemon=True).start()

    def _read_stdout(self) -> None:
        # Some local servers (e.g. lis-skill-bus) flush JSON without a trailing
        # newline. Read raw chunks and keep a partial buffer so those replies
        # can still be parsed instead of hanging until timeout.
        assert self.proc.stdout is not None
        fd = self.proc.stdout.fileno()
        decoder = codecs.getincrementaldecoder("utf-8")("replace")
        while True:
            try:
                chunk = os.read(fd, 65536)
            except OSError:
                break
            if not chunk:
                break
            text = decoder.decode(chunk)
            with self._buf_lock:
                self._buf += text
                while "\n" in self._buf:
                    line, self._buf = self._buf.split("\n", 1)
                    self.lines.put(line)
        with self._buf_lock:
            tail, self._buf = self._buf, ""
        if tail.strip():
            self.lines.put(tail)
        self.lines.put(None)

    def _take_partial(self) -> Optional[str]:
        with self._buf_lock:
            if not self._buf.strip():
                return None
            candidate = self._buf
        try:
            json.loads(candidate)
        except json.JSONDecodeError:
            return None
        with self._buf_lock:
            if self._buf == candidate:
                self._buf = ""
                return candidate
        return None

    def _read_stderr(self) -> None:
        assert self.proc.stderr is not None
        for line in self.proc.stderr:
            self.stderr_tail.append(line.rstrip("\n"))
            if len(self.stderr_tail) > 40:
                del self.stderr_tail[:20]

    def send(self, obj: Dict[str, Any]) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(obj, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def read_message(self, deadline: float) -> Optional[Dict[str, Any]]:
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                return None
            try:
                line = self.lines.get(timeout=min(remaining, 0.25))
            except queue.Empty:
                line = self._take_partial()
                if line is None:
                    if self.proc.poll() is not None and self.lines.empty():
                        return None
                    continue
            if line is None:
                return None
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(msg, dict):
                return msg

    def wait_for_id(self, request_id: int, deadline: float) -> Optional[Dict[str, Any]]:
        while True:
            msg = self.read_message(deadline)
            if msg is None:
                return None
            if msg.get("id") == request_id and ("result" in msg or "error" in msg):
                return msg

    def close(self) -> None:
        try:
            if self.proc.stdin:
                self.proc.stdin.close()
        except OSError:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=3)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


def probe_stdio(server: str, cmd: List[str], timeout: float) -> Dict[str, Any]:
    session = None
    try:
        session = StdioSession(cmd, timeout)
        deadline = time.time() + timeout
        session.send({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": CLIENT_INFO,
            },
        })
        init = session.wait_for_id(1, deadline)
        if init is None:
            err = "no initialize response"
            if session.stderr_tail:
                err += ": " + " | ".join(session.stderr_tail[-3:])
            return make_result(server, "stdio", "unmeasurable", error=err[:500])
        if "error" in init:
            return make_result(server, "stdio", "unmeasurable",
                               error="initialize error: " + json.dumps(init["error"], ensure_ascii=False)[:400])
        session.send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        all_tools: List[Any] = []
        total_raw = 0
        cursor: Optional[str] = None
        for page in range(50):
            req: Dict[str, Any] = {"jsonrpc": "2.0", "id": 2 + page, "method": "tools/list"}
            if cursor:
                req["params"] = {"cursor": cursor}
            session.send(req)
            msg = session.wait_for_id(2 + page, time.time() + timeout)
            if msg is None:
                if page == 0:
                    err = "no tools/list response"
                    if session.stderr_tail:
                        err += ": " + " | ".join(session.stderr_tail[-3:])
                    return make_result(server, "stdio", "unmeasurable", error=err[:500])
                break
            if "error" in msg:
                return make_result(server, "stdio", "unmeasurable",
                                   error="tools/list error: " + json.dumps(msg["error"], ensure_ascii=False)[:400])
            total_raw += len(json.dumps(msg, ensure_ascii=False).encode("utf-8"))
            result = msg.get("result") or {}
            page_tools = result.get("tools") or []
            if isinstance(page_tools, list):
                all_tools.extend(page_tools)
            cursor = result.get("nextCursor")
            if not cursor:
                break
        extra = {"protocol_version": init.get("result", {}).get("protocolVersion")}
        extra.update(tool_details(all_tools))
        return make_result(server, "stdio", "measured",
                           tool_count=len(all_tools),
                           tools_bytes=compact_bytes(all_tools),
                           total_bytes=total_raw,
                           extra=extra)
    except FileNotFoundError:
        return make_result(server, "stdio", "unmeasurable", error="command not found")
    except Exception as exc:  # noqa: BLE001 - probe must always return JSON
        return make_result(server, "stdio", "unmeasurable", error=f"{type(exc).__name__}: {exc}"[:500])
    finally:
        if session is not None:
            session.close()


# --------------------------------------------------------------------------
# HTTP transport (Streamable HTTP, JSON or SSE responses)
# --------------------------------------------------------------------------

def parse_http_body(content_type: str, raw: bytes) -> List[Dict[str, Any]]:
    text = raw.decode("utf-8", "replace").strip()
    if not text:
        return []
    if "text/event-stream" in content_type.lower() or text.startswith("event:") or "\ndata:" in text:
        msgs: List[Dict[str, Any]] = []
        data_lines: List[str] = []
        for line in text.splitlines():
            if line.startswith("data:"):
                data_lines.append(line[5:].lstrip())
            elif not line.strip() and data_lines:
                blob = "\n".join(data_lines)
                data_lines = []
                try:
                    obj = json.loads(blob)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    msgs.append(obj)
        if data_lines:
            try:
                obj = json.loads("\n".join(data_lines))
                if isinstance(obj, dict):
                    msgs.append(obj)
            except json.JSONDecodeError:
                pass
        return msgs
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return []
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        return [obj]
    return []


def post_json(url: str, payload: Dict[str, Any], token: Optional[str],
              session_id: Optional[str], timeout: float,
              protocol_version: Optional[str]) -> Tuple[int, Dict[str, str], bytes, List[Dict[str, Any]]]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "mcp-probe/1.0",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    if protocol_version:
        headers["MCP-Protocol-Version"] = protocol_version
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, hdrs, raw, parse_http_body(hdrs.get("content-type", ""), raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read()[:4096]
        hdrs = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        return exc.code, hdrs, raw, parse_http_body(hdrs.get("content-type", ""), raw)


def probe_http(server: str, url: str, bearer_env: str, timeout: float) -> Dict[str, Any]:
    token = os.environ.get(bearer_env) if bearer_env else None
    if bearer_env and not token:
        return make_result(server, "http", "unmeasurable",
                           error=f"environment variable {bearer_env} is empty or unset")
    try:
        status, headers, raw, msgs = post_json(url, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": CLIENT_INFO,
            },
        }, token, None, timeout, None)
        session_id = headers.get("mcp-session-id")
        init = next((m for m in msgs if m.get("id") == 1), None)
        if init is None:
            return make_result(server, "http", "unmeasurable",
                               error=f"no initialize response (HTTP {status})")
        if "error" in init:
            return make_result(server, "http", "unmeasurable",
                               error="initialize error: " + json.dumps(init["error"], ensure_ascii=False)[:400])
        proto = (init.get("result") or {}).get("protocolVersion") or PROTOCOL_VERSION

        # initialized notification; some servers answer 202/204 with no body
        post_json(url, {"jsonrpc": "2.0", "method": "notifications/initialized"},
                  token, session_id, timeout, proto)

        all_tools: List[Any] = []
        total_raw = 0
        cursor: Optional[str] = None
        for page in range(50):
            payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": 2 + page, "method": "tools/list"}
            if cursor:
                payload["params"] = {"cursor": cursor}
            status, headers, raw, msgs = post_json(url, payload, token, session_id, timeout, proto)
            msg = next((m for m in msgs if m.get("id") == 2 + page), None)
            if msg is None:
                if page == 0:
                    return make_result(server, "http", "unmeasurable",
                                       error=f"no tools/list response (HTTP {status})")
                break
            if "error" in msg:
                return make_result(server, "http", "unmeasurable",
                                   error="tools/list error: " + json.dumps(msg["error"], ensure_ascii=False)[:400])
            total_raw += len(raw)
            result = msg.get("result") or {}
            page_tools = result.get("tools") or []
            if isinstance(page_tools, list):
                all_tools.extend(page_tools)
            cursor = result.get("nextCursor")
            if not cursor:
                break
        extra = {"protocol_version": proto}
        extra.update(tool_details(all_tools))
        return make_result(server, "http", "measured",
                           tool_count=len(all_tools),
                           tools_bytes=compact_bytes(all_tools),
                           total_bytes=total_raw,
                           extra=extra)
    except Exception as exc:  # noqa: BLE001
        return make_result(server, "http", "unmeasurable", error=f"{type(exc).__name__}: {exc}"[:500])


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Measure MCP tools/list schema bytes")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stdio", action="store_true", help="spawn a stdio MCP server")
    group.add_argument("--http", metavar="URL", help="Streamable HTTP MCP endpoint")
    group.add_argument("--disabled", action="store_true", help="record a disabled server as 0 B")
    parser.add_argument("--name", required=True)
    parser.add_argument("--bearer-env", default="", help="env var holding the bearer token (never printed)")
    parser.add_argument("--note", default="")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--out", default="", help="write JSON to this file in addition to stdout")
    parser.add_argument("cmd", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.disabled:
        result = make_result(args.name, "none", "disabled", 0, 0, 0,
                             extra={"note": args.note or "disabled"})
    elif args.http:
        result = probe_http(args.name, args.http, args.bearer_env, args.timeout)
    else:
        cmd = list(args.cmd)
        if cmd and cmd[0] == "--":
            cmd = cmd[1:]
        if not cmd:
            parser.error("--stdio requires a command after --")
        result = probe_stdio(args.name, cmd, args.timeout)

    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    return 0 if result["status"] in ("measured", "disabled") else 1


if __name__ == "__main__":
    sys.exit(main())
