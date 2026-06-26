#!/usr/bin/env python3
"""
ClawStatus - OpenClaw Status Dashboard

Core features:
1) Agent / Sub-agent runtime overview
2) Cron job count and execution status
3) OpenClaw overall health status
4) Model configuration count and per-model token usage (aggregated from session snapshots)
"""

from __future__ import annotations

import argparse
import glob
import json
import mmap
import os
import signal
import socket
import subprocess
import threading
import sys
import time
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set

from flask import Flask, jsonify, request, Response

try:
    from waitress import serve as waitress_serve
except Exception:  # pragma: no cover
    waitress_serve = None

__version__ = "2.4.0"
APP_TITLE = "ClawStatus"

HOME = Path.home()
OPENCLAW_DIR = HOME / ".openclaw"
OPENCLAW_CONFIG = OPENCLAW_DIR / "openclaw.json"
AGENTS_DIR = OPENCLAW_DIR / "agents"
CRON_JOBS_PATH = OPENCLAW_DIR / "cron" / "jobs.json"
CRON_RUNS_DIR = OPENCLAW_DIR / "cron" / "runs"
SUBAGENT_RUNS_PATH = OPENCLAW_DIR / "subagents" / "runs.json"

RUNTIME_DIR = HOME / ".clawstatus"
PID_FILE = RUNTIME_DIR / "clawstatus.pid"
LOG_FILE = RUNTIME_DIR / "clawstatus.log"

ACTIVE_AGENT_WINDOW_MS = 60 * 1000  # 60s window for stop detection (reduced sensitivity)
_REFRESH_INTERVAL_SEC = 60

# Agent real-time detection cache (lightweight)
_agent_fs_cache: Dict[str, Tuple[float, bool, Optional[int]]] = {}
_agent_fs_cache_lock = threading.Lock()
_agent_fs_cache_ttl_sec = 5  # 5s cache to reduce filesystem scans
_STATUS_CACHE_TTL_SEC = 120  # 2 min cache for openclaw status
_STATUS_WARMUP_INTERVAL_SEC = 300  # 5 min warmup interval
_STATUS_WARMUP_IDLE_GRACE_SEC = 900  # 15 min idle grace
_DASH_CACHE_TTL_SEC = 60  # 1 min dashboard cache
_DAILY_TOKENS_TTL_SEC = 600  # 10 min token stats cache
_DAILY_FILELIST_TTL_SEC = 1800  # 30 min filelist cache
_MODELS_CACHE_TTL_SEC = 600  # 10 min models cache
_MEMORY_CACHE_TTL_SEC = 600  # 10 min memory cache
_status_cache: Dict[str, Any] = {"ts": 0.0, "data": None, "err": None}

# TCP port probe config (minimal, completes in 1-3ms)
_TCP_PROBE_TIMEOUT_SEC = 0.5  # TCP connection timeout (seconds)
_TCP_PROBE_CACHE_TTL_SEC = 30  # 30s cache for TCP probe results
_tcp_probe_cache: Dict[str, Any] = {"ts": 0.0, "reachable": False, "latency_ms": None}
_tcp_probe_lock = threading.Lock()
_TCP_PROBE_DEFAULT_PORT = 18789  # OpenClaw gateway default port
_dash_cache: Dict[str, Any] = {"ts": 0.0, "data": None}
_daily_tokens_cache: Dict[str, Any] = {
    "ts": 0.0,
    "rows": None,
    "dayMap": None,
    "dayActiveMap": None,
    "dayPassiveMap": None,
    "fileState": {},
    "fileContrib": {},
    "fileContribActive": {},
    "fileContribPassive": {},
    "days": None,
    "startDay": None,
    "files": None,
    "filesTs": 0.0,
    "dirsStamp": None,
}
_models_cache: Dict[str, Any] = {"ts": 0.0, "data": None, "days": 0}
_memory_cache: Dict[str, Any] = {"ts": 0.0, "data": None}
_status_lock = threading.Lock()
_dash_lock = threading.Lock()
_daily_tokens_lock = threading.Lock()
_models_lock = threading.Lock()
_memory_lock = threading.Lock()
_config_lock = threading.Lock()
_bg_warmup_started = False
_dash_refreshing = False
_status_refreshing = False
_last_status_demand_ts = 0.0


def _cache_ts_ms(cache: Dict[str, Any], lock: threading.Lock) -> Optional[int]:
    with lock:
        ts = float(cache.get("ts", 0) or 0)
    if ts <= 0:
        return None
    return int(ts * 1000)


def _safe_read_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _read_json_tolerant(path: Path, default: Any) -> Any:
    """Read JSON file with minor format errors (try inserting comma at parse break)."""
    try:
        if not path.exists():
            return default
        text = path.read_text(encoding="utf-8", errors="replace")
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Only try inserting comma when values are directly adjacent at error position
        i = int(e.pos) - 1
        j = int(e.pos)
        while i >= 0 and text[i].isspace():
            i -= 1
        while j < len(text) and text[j].isspace():
            j += 1

        if i >= 0 and j < len(text):
            left = text[i]
            right = text[j]
            right_starts = set('{["-0123456789tfn')
            if left in "]}" and right in right_starts:
                try:
                    fixed = text[:j] + "," + text[j:]
                    return json.loads(fixed)
                except Exception:
                    return default
        return default
    except Exception:
        return default


def _fmt_ts(ms: Optional[int]) -> str:
    if not ms:
        return "-"
    try:
        return datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "-"


def _fmt_duration_ms(ms: Optional[int]) -> str:
    if ms is None:
        return "-"
    sec = int(ms / 1000)
    if sec < 60:
        return f"{sec}s"
    mins, s = divmod(sec, 60)
    if mins < 60:
        return f"{mins}m{s:02d}s"
    hrs, m = divmod(mins, 60)
    return f"{hrs}h{m:02d}m"

def _is_meaningful_agent_id(value: Any) -> bool:
    agent_id = str(value or "").strip()
    if not agent_id or agent_id == "-":
        return False
    return agent_id.lower() not in {"none", "unknown", "auto", "default"}


def _status_tone(status: Any) -> str:
    s = str(status or "").strip().lower()
    if s in {"ok", "success", "succeeded", "completed", "complete", "done"}:
        return "ok"
    if s in {"error", "failed", "fail", "timeout", "timed_out", "cancelled", "canceled"}:
        return "bad"
    if s in {"running", "started", "processing", "in_progress", "pending", "queued"}:
        return "warn"
    return "muted"


def _extract_json_blob(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        pass

    decoder = json.JSONDecoder()
    idx = 0
    best: Optional[Dict[str, Any]] = None

    while True:
        start = text.find("{", idx)
        if start < 0:
            break
        try:
            obj, end = decoder.raw_decode(text, start)
            if isinstance(obj, dict):
                # Prefer returning object that looks more like openclaw status
                if any(k in obj for k in ("heartbeat", "gateway", "sessions", "agents", "channelSummary")):
                    return obj
                if best is None or len(obj) > len(best):
                    best = obj
            idx = max(end, start + 1)
        except Exception:
            idx = start + 1

    return best


def _run_status_cmd(cmd: List[str], timeout_sec: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
    except FileNotFoundError:
        return None, "openclaw command not found (not in PATH)"
    except subprocess.TimeoutExpired:
        return None, f"{' '.join(cmd[1:])} execution timeout"
    except Exception as e:
        return None, f"openclaw status call failed: {e}"

    merged = (proc.stdout or "") + "\n" + (proc.stderr or "")
    data = _extract_json_blob(merged)
    if data is not None:
        return data, None

    snippet = merged.strip().splitlines()[:3]
    hint = " | ".join(snippet) if snippet else "no output"
    return None, f"Failed to parse openclaw status output (rc={proc.returncode}): {hint[:240]}"


def _refresh_openclaw_status() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Execute a real openclaw status refresh and write to cache."""
    global _status_refreshing

    now = time.time()
    openclaw_bin = os.environ.get("OPENCLAW_BIN") or shutil.which("openclaw") or str(HOME / ".npm-global" / "bin" / "openclaw")

    # Use lightweight path by default to reduce periodic warmup resource impact.
    attempts = [([openclaw_bin, "status", "--json"], 20)]

    # Enable usage fetch via env var if needed; disabled by default.
    if (os.environ.get("CLAWSTATUS_ENABLE_STATUS_USAGE") or "").strip() == "1":
        attempts.append(([openclaw_bin, "status", "--json", "--usage"], 25))

    last_err: Optional[str] = None
    try:
        for cmd, timeout_sec in attempts:
            data, err = _run_status_cmd(cmd, timeout_sec)
            if data is not None:
                with _status_lock:
                    _status_cache.update({"ts": now, "data": data, "err": None})
                return data, None
            last_err = err

        # When refresh fails, clear stale data so TCP probe drives state detection.
        # Keeping stale data with a fresh timestamp would make it look "fresh" forever.
        with _status_lock:
            _status_cache.update({"ts": now, "data": None, "err": last_err})
        return None, last_err
    finally:
        with _status_lock:
            _status_refreshing = False


def _start_status_refresh() -> None:
    global _status_refreshing
    with _status_lock:
        if _status_refreshing:
            return
        _status_refreshing = True
    t = threading.Thread(target=_refresh_openclaw_status, daemon=True, name="clawstatus-status-refresh")
    t.start()


def _run_openclaw_status() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Return cache first to avoid blocking API requests. Execute sync only on cold start."""
    global _last_status_demand_ts

    now = time.time()
    _last_status_demand_ts = now
    with _status_lock:
        cached_data = _status_cache.get("data")
        cached_err = _status_cache.get("err")
        cached_ts = float(_status_cache.get("ts", 0) or 0)

    # Cache is fresh
    if cached_data is not None and now - cached_ts < _STATUS_CACHE_TTL_SEC:
        return cached_data, cached_err

    # Cache expired but exists: return stale value (speed first), trigger background refresh (accuracy first)
    if cached_data is not None:
        _start_status_refresh()
        return cached_data, cached_err

    # Cold start no cache: sync fetch once to avoid blank page
    return _refresh_openclaw_status()


def _bg_status_warmup_loop() -> None:
    """Background silent cache warmup."""
    _refresh_openclaw_status()  # Warmup on start
    while True:
        time.sleep(_STATUS_WARMUP_INTERVAL_SEC)

        # Pause warmup when idle for too long to avoid unnecessary subprocess overhead
        idle_sec = time.time() - float(_last_status_demand_ts or 0)
        if idle_sec > _STATUS_WARMUP_IDLE_GRACE_SEC:
            continue

        _start_status_refresh()


def _load_auth_token() -> Optional[str]:
    env_token = (os.environ.get("OPENCLAW_GATEWAY_TOKEN") or "").strip()
    if env_token:
        return env_token

    env_token2 = (os.environ.get("CLAWSTATUS_TOKEN") or "").strip()
    if env_token2:
        return env_token2

    cfg = _safe_read_json(OPENCLAW_CONFIG, {})
    token = (
        cfg.get("gateway", {})
        .get("auth", {})
        .get("token", "")
        .strip()
    )
    return token or None


def _resolve_openclaw_port() -> int:
    """Resolve OpenClaw gateway port from env var, cached status, or default."""
    # 1. Env var override
    env_port = os.environ.get("OPENCLAW_GATEWAY_PORT", "").strip()
    if env_port.isdigit():
        return int(env_port)

    # 2. Extract from cached status data gateway URL (e.g. "ws://127.0.0.1:18789")
    with _status_lock:
        cached_data = _status_cache.get("data")
    if cached_data:
        gw_url = (cached_data.get("gateway") or {}).get("url", "")
        if gw_url:
            try:
                # Parse port from URLs like "ws://127.0.0.1:18789" or "http://host:port"
                from urllib.parse import urlparse
                parsed = urlparse(gw_url)
                if parsed.port:
                    return parsed.port
            except Exception:
                pass

    # 3. Default
    return _TCP_PROBE_DEFAULT_PORT


def _tcp_probe_openclaw() -> Tuple[bool, Optional[int]]:
    """
    TCP port probe to check if OpenClaw is alive.
    Minimal implementation: completes in 1-3ms, no subprocess, no HTTP overhead.
    Returns: (is_reachable, latency_ms)
    """
    port = _resolve_openclaw_port()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(_TCP_PROBE_TIMEOUT_SEC)
        start = time.time()
        result = sock.connect_ex(('127.0.0.1', port))
        latency_ms = int((time.time() - start) * 1000)
        sock.close()
        return result == 0, latency_ms
    except Exception:
        return False, None


def _refresh_tcp_probe() -> Dict[str, Any]:
    """Execute TCP probe and update cache."""
    reachable, latency_ms = _tcp_probe_openclaw()
    
    result = {
        "ts": time.time(),
        "reachable": reachable,
        "latencyMs": latency_ms,
    }
    
    with _tcp_probe_lock:
        _tcp_probe_cache.update(result)
    
    return result


def _get_tcp_probe_status() -> Dict[str, Any]:
    """Get TCP probe status (prefer cache, refresh if needed)."""
    with _tcp_probe_lock:
        cached = dict(_tcp_probe_cache)

    now = time.time()
    # Return directly if cache is valid
    if now - cached.get("ts", 0) < _TCP_PROBE_CACHE_TTL_SEC:
        return cached

    # Cache expired, execute probe
    return _refresh_tcp_probe()


def _token_from_request() -> Optional[str]:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()
    x_api_key = request.headers.get("X-API-Key", "").strip()
    if x_api_key:
        return x_api_key
    q_token = request.args.get("token", "").strip()
    return q_token or None


def _is_authorized(required_token: Optional[str]) -> bool:
    if not required_token:
        return True
    got = _token_from_request()
    return bool(got and got == required_token)


def _require_auth(required_token: Optional[str]):
    if _is_authorized(required_token):
        return None
    return jsonify({"error": "unauthorized", "valid": False}), 401


def _read_last_jsonl_obj(path: Path) -> Optional[Dict[str, Any]]:
    """mmap fast read last 4KB to avoid loading entire large file"""
    if not path.exists() or not path.is_file():
        return None
    try:
        with open(path, "rb") as f:
            # Try mmap read
            try:
                size = os.fstat(f.fileno()).st_size
                if size == 0:
                    return None
                # Large file: only read last 4KB
                if size > 4096:
                    f.seek(size - 4096)
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    # Find last line
                    data = mm.read()
                    lines = data.decode("utf-8", errors="replace").strip().splitlines()
                    if not lines:
                        return None
                    return json.loads(lines[-1])
            except Exception:
                # mmap failed, fallback to normal read
                f.seek(0)
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
                return json.loads(lines[-1]) if lines else None
    except Exception:
        return None


# inotify real-time monitoring config
_WATCHED_FILES: Dict[str, str] = {
    str(CRON_JOBS_PATH): "crons",
    str(SUBAGENT_RUNS_PATH): "subagents",
    str(OPENCLAW_CONFIG): "config",
}
_inotify_initialized = False
_inotify_watches: Dict[str, int] = {}
_inotify_fd: Optional[int] = None


def _init_inotify() -> bool:
    """Initialize inotify monitoring (Linux only)"""
    global _inotify_initialized, _inotify_fd
    if _inotify_initialized:
        return _inotify_fd is not None

    _inotify_initialized = True

    # Check if inotify is supported
    try:
        import ctypes
        libc = ctypes.CDLL('libc.so.6', use_errno=True)

        # inotify_init1 flags
        IN_CLOEXEC = 0x80000
        IN_NONBLOCK = 0x800

        fd = libc.inotify_init1(IN_NONBLOCK | IN_CLOEXEC)
        if fd < 0:
            return False

        _inotify_fd = fd

        # Monitor file modifications (IN_MODIFY = 0x00000002)
        IN_MODIFY = 0x00000002
        
        for filepath, name in _WATCHED_FILES.items():
            if os.path.exists(filepath):
                wd = libc.inotify_add_watch(_inotify_fd, filepath.encode(), IN_MODIFY)
                if wd >= 0:
                    _inotify_watches[wd] = name
        
        return len(_inotify_watches) > 0
    except Exception:
        return False


def _check_inotify_events(timeout_sec: float = 0.0) -> Set[str]:
    """Check file change events, non-blocking"""
    if _inotify_fd is None:
        return set()

    changed: Set[str] = set()

    try:
        import ctypes
        import select

        # Non-blocking check for events
        readable, _, _ = select.select([_inotify_fd], [], [], timeout_sec)
        if not readable:
            return changed
        
        # Read events (inotify_event structure)
        buf = os.read(_inotify_fd, 4096)
        offset = 0
        
        while offset < len(buf):
            # struct inotify_event { int wd; uint32_t mask; uint32_t cookie; uint32_t len; char name[]; }
            if offset + 16 > len(buf):
                break
            
            wd = int.from_bytes(buf[offset:offset+4], 'little', signed=True)
            # mask = int.from_bytes(buf[offset+4:offset+8], 'little')
            # cookie = int.from_bytes(buf[offset+8:offset+12], 'little')
            name_len = int.from_bytes(buf[offset+12:offset+16], 'little')
            
            if wd in _inotify_watches:
                changed.add(_inotify_watches[wd])
            
            offset += 16 + name_len
    except Exception:
        pass
    
    return changed


def _invalidate_cache_by_type(cache_type: str) -> None:
    """Invalidate cache by change type"""
    global _dash_cache, _status_cache, _models_cache, _memory_cache

    now = time.time()

    if cache_type == "crons":
        # Cron changes only refresh dashboard
        with _dash_lock:
            _dash_cache["ts"] = 0
    elif cache_type == "subagents":
        # Subagent changes refresh dashboard
        with _dash_lock:
            _dash_cache["ts"] = 0
    elif cache_type == "config":
        # Config changes affect all caches
        with _dash_lock:
            _dash_cache["ts"] = 0
        with _status_lock:
            _status_cache["ts"] = 0
        with _models_lock:
            _models_cache["ts"] = 0
        with _memory_lock:
            _memory_cache["ts"] = 0


def _start_inotify_monitor() -> None:
    """Start inotify monitoring thread (event-driven, zero polling)"""
    if not _init_inotify():
        return  # inotify not supported, silently fallback to polling

    def _monitor_loop():
        while True:
            try:
                # Wait for events (blocking, but zero CPU)
                changed = _check_inotify_events(timeout_sec=1.0)
                for cache_type in changed:
                    _invalidate_cache_by_type(cache_type)
            except Exception:
                time.sleep(1)
    
    t = threading.Thread(target=_monitor_loop, daemon=True, name="clawstatus-inotify")
    t.start()


def _collect_subagent_runs() -> Dict[str, Any]:
    raw = _safe_read_json(SUBAGENT_RUNS_PATH, {"runs": {}})
    runs_obj = raw.get("runs", {}) if isinstance(raw, dict) else {}
    runs: List[Dict[str, Any]] = []
    running_count = 0

    if isinstance(runs_obj, dict):
        items = runs_obj.items()
    elif isinstance(runs_obj, list):
        items = [(str(i), v) for i, v in enumerate(runs_obj)]
    else:
        items = []

    def _agent_from_session_key(sk: Any) -> Optional[str]:
        s = str(sk or "")
        if not s.startswith("agent:"):
            return None
        parts = s.split(":")
        if len(parts) < 2:
            return None
        return parts[1] or None

    for run_id, payload in items:
        if not isinstance(payload, dict):
            continue

        ended_at = payload.get("endedAt")
        explicit_status = str(
            payload.get("status")
            or payload.get("state")
            or payload.get("phase")
            or ""
        ).strip().lower()

        if explicit_status:
            status = explicit_status
        elif ended_at:
            outcome = payload.get("outcome") if isinstance(payload.get("outcome"), dict) else {}
            status = str(outcome.get("status") or payload.get("endedReason") or "completed").lower()
        elif payload.get("startedAt"):
            status = "running"
        elif payload.get("createdAt"):
            status = "queued"
        else:
            status = "unknown"

        is_running = (
            status in {"running", "active", "started", "in_progress", "processing"}
            or (payload.get("startedAt") is not None and payload.get("endedAt") is None)
        )
        if is_running:
            running_count += 1

        child_sk = payload.get("childSessionKey") or payload.get("sessionKey")
        requester_sk = payload.get("requesterSessionKey")

        agent_id = payload.get("agentId") or _agent_from_session_key(child_sk)
        parent_agent_id = payload.get("parentAgentId") or _agent_from_session_key(requester_sk)

        runs.append(
            {
                "id": payload.get("runId") or run_id,
                "status": status,
                "agentId": agent_id,
                "parentAgentId": parent_agent_id,
                "sessionKey": child_sk,
                "childSessionKey": child_sk,
                "requesterSessionKey": requester_sk,
                "startedAt": payload.get("startedAt") or payload.get("createdAt"),
                "updatedAt": payload.get("updatedAt") or payload.get("endedAt"),
                "endedAt": payload.get("endedAt"),
                "task": payload.get("task"),
                "raw": payload,
            }
        )

    return {
        "total": len(runs),
        "running": running_count,
        "runs": runs,
    }


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp")
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    tmp_path.write_text(text, encoding="utf-8")
    os.replace(tmp_path, path)


def _invalidate_dashboard_cache() -> None:
    with _dash_lock:
        _dash_cache.update({"ts": 0.0, "data": None})
    with _models_lock:
        _models_cache.update({"ts": 0.0, "data": None, "days": 0})


def _iter_configured_model_ids(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: Dict[str, Dict[str, Any]] = {}

    def _ensure(mid: Any, display_name: Optional[str] = None, provider_hint: Optional[str] = None) -> None:
        model_id = str(mid or "").strip()
        if not model_id:
            return
        current = rows.get(model_id, {"id": model_id, "name": model_id, "provider": provider_hint or "-"})
        if display_name:
            current["name"] = str(display_name).strip() or current["name"]
        if provider_hint:
            current["provider"] = provider_hint
        elif current.get("provider") in {None, "", "-"} and "/" in model_id:
            current["provider"] = model_id.split("/", 1)[0]
        rows[model_id] = current

    providers = ((cfg.get("models") or {}).get("providers") or {}) if isinstance(cfg, dict) else {}
    if isinstance(providers, dict):
        for provider_id, provider_cfg in providers.items():
            if not isinstance(provider_cfg, dict):
                continue
            for model in provider_cfg.get("models") or []:
                if not isinstance(model, dict):
                    continue
                model_leaf = str(model.get("id") or "").strip()
                if not model_leaf:
                    continue
                _ensure(f"{provider_id}/{model_leaf}", model.get("name"), str(provider_id))

    agents_cfg = (cfg.get("agents") or {}) if isinstance(cfg, dict) else {}
    defaults = agents_cfg.get("defaults") or {}
    if isinstance(defaults, dict):
        for mid in (defaults.get("models") or {}).keys():
            _ensure(mid)
        default_model = defaults.get("model") or {}
        if isinstance(default_model, dict):
            _ensure(default_model.get("primary"))
            for mid in default_model.get("fallbacks") or []:
                _ensure(mid)

    for agent in agents_cfg.get("list") or []:
        if not isinstance(agent, dict):
            continue
        model_cfg = agent.get("model")
        if isinstance(model_cfg, dict):
            _ensure(model_cfg.get("primary"))
            for mid in model_cfg.get("fallbacks") or []:
                _ensure(mid)
        elif isinstance(model_cfg, str):
            _ensure(model_cfg)

    jobs_payload = _read_json_tolerant(CRON_JOBS_PATH, {"jobs": []})
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        payload = job.get("payload") or {}
        if isinstance(payload, dict):
            _ensure(payload.get("model"))

    return sorted(rows.values(), key=lambda x: x["id"])


def _available_models_payload() -> Tuple[List[Dict[str, Any]], set[str]]:
    cfg = _safe_read_json(OPENCLAW_CONFIG, {})
    rows = _iter_configured_model_ids(cfg)
    return rows, {str(row.get("id") or "") for row in rows}


def _agent_model_map_from_config() -> Dict[str, str]:
    cfg = _safe_read_json(OPENCLAW_CONFIG, {})
    agents_cfg = (cfg.get("agents") or {}) if isinstance(cfg, dict) else {}
    result: Dict[str, str] = {}
    for agent in agents_cfg.get("list") or []:
        if not isinstance(agent, dict):
            continue
        aid = str(agent.get("id") or "").strip()
        if not aid:
            continue
        model_cfg = agent.get("model")
        if isinstance(model_cfg, dict):
            result[aid] = str(model_cfg.get("primary") or "").strip()
        elif isinstance(model_cfg, str):
            result[aid] = model_cfg.strip()
    return result


def _current_agent_model(agent_id: str, status_agent: Optional[Dict[str, Any]] = None) -> str:
    cfg_map = _agent_model_map_from_config()
    current = str(cfg_map.get(agent_id) or "").strip()
    if current:
        return current
    if isinstance(status_agent, dict):
        return str(status_agent.get("model") or "").strip()
    return ""


def _restart_openclaw() -> Tuple[bool, str]:
    """Try to restart openclaw service. Attempts systemctl --user then openclaw restart.
    Returns (success, method_used)."""
    # 1. Try systemctl user service
    for svc in ("openclaw.service", "openclaw"):
        try:
            proc = subprocess.run(
                ["systemctl", "--user", "restart", svc],
                capture_output=True, text=True, timeout=10,
            )
            if proc.returncode == 0:
                return True, f"systemctl --user restart {svc}"
        except FileNotFoundError:
            break  # systemctl not found, skip subsequent systemctl attempts
        except subprocess.TimeoutExpired:
            pass

    # 2. Try openclaw restart command
    openclaw_bin = (
        os.environ.get("OPENCLAW_BIN")
        or shutil.which("openclaw")
        or str(HOME / ".npm-global" / "bin" / "openclaw")
    )
    try:
        proc = subprocess.run(
            [openclaw_bin, "restart"],
            capture_output=True, text=True, timeout=10,
        )
        if proc.returncode == 0:
            return True, "openclaw restart"
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass

    return False, "no restart method succeeded"


def _update_agent_model(agent_id: str, model_id: str) -> Dict[str, Any]:
    with _config_lock:
        cfg = _safe_read_json(OPENCLAW_CONFIG, {})
        available_models, valid_ids = _available_models_payload()
        if model_id not in valid_ids:
            raise ValueError("invalid model")

        agents_cfg = (cfg.get("agents") or {}) if isinstance(cfg, dict) else {}
        agent_list = agents_cfg.get("list") or []
        if not isinstance(agent_list, list):
            raise KeyError(agent_id)

        target = None
        for agent in agent_list:
            if isinstance(agent, dict) and str(agent.get("id") or "") == agent_id:
                target = agent
                break
        if target is None:
            raise KeyError(agent_id)

        model_cfg = target.get("model")
        if isinstance(model_cfg, dict):
            model_cfg["primary"] = model_id
        else:
            target["model"] = {"primary": model_id}

        _write_json_atomic(OPENCLAW_CONFIG, cfg)

    _invalidate_dashboard_cache()
    restarted, restart_method = _restart_openclaw()
    return {
        "agentId": agent_id,
        "currentModel": model_id,
        "availableModels": available_models,
        "restartTriggered": restarted,
        "restartMethod": restart_method,
    }


def _trigger_cron_run(job_id: str) -> Dict[str, Any]:
    """Trigger a cron job to run immediately via `openclaw cron run <id>`."""
    jobs_payload = _read_json_tolerant(CRON_JOBS_PATH, {"jobs": []})
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    found = any(
        isinstance(j, dict) and str(j.get("id") or "") == job_id
        for j in jobs
    )
    if not found:
        raise KeyError(job_id)
    try:
        subprocess.Popen(
            ["openclaw", "cron", "run", job_id, "--timeout", "30000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return {"jobId": job_id, "triggered": True}
    except Exception as e:
        return {"jobId": job_id, "triggered": False, "error": str(e)}


def _delete_cron_job(job_id: str) -> Dict[str, Any]:
    """Delete a cron job via `openclaw cron delete <id>`."""
    jobs_payload = _read_json_tolerant(CRON_JOBS_PATH, {"jobs": []})
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    found = any(
        isinstance(j, dict) and str(j.get("id") or "") == job_id
        for j in jobs
    )
    if not found:
        raise KeyError(job_id)
    
    openclaw_bin = (
        os.environ.get("OPENCLAW_BIN")
        or shutil.which("openclaw")
        or str(HOME / ".npm-global" / "bin" / "openclaw")
    )
    try:
        proc = subprocess.run(
            [openclaw_bin, "cron", "delete", job_id],
            capture_output=True, text=True, timeout=15,
        )
        if proc.returncode != 0:
            raise OSError(proc.stderr.strip() or f"openclaw cron delete failed (rc={proc.returncode})")
    except subprocess.TimeoutExpired:
        raise OSError("openclaw cron delete timed out")
    
    _invalidate_dashboard_cache()
    return {"jobId": job_id, "deleted": True}


def _update_cron_model(job_id: str, model_id: str) -> Dict[str, Any]:
    available_models, valid_ids = _available_models_payload()
    if model_id not in valid_ids:
        raise ValueError("invalid model")

    # Verify job exists
    jobs_payload = _read_json_tolerant(CRON_JOBS_PATH, {"jobs": []})
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    found = any(isinstance(j, dict) and str(j.get("id") or "") == job_id for j in jobs)
    if not found:
        raise KeyError(job_id)

    openclaw_bin = (
        os.environ.get("OPENCLAW_BIN")
        or shutil.which("openclaw")
        or str(HOME / ".npm-global" / "bin" / "openclaw")
    )
    try:
        proc = subprocess.run(
            [openclaw_bin, "cron", "edit", job_id, "--model", model_id],
            capture_output=True, text=True, timeout=15,
        )
        if proc.returncode != 0:
            raise OSError(proc.stderr.strip() or f"openclaw cron edit failed (rc={proc.returncode})")
    except subprocess.TimeoutExpired:
        raise OSError("openclaw cron edit timed out")

    _invalidate_dashboard_cache()
    return {
        "jobId": job_id,
        "currentModel": model_id,
        "availableModels": available_models,
        "restartTriggered": True,
        "restartMethod": "openclaw cron edit --model",
    }


def _actual_consumed_tokens(input_tokens: Any, output_tokens: Any, cache_read_tokens: Any) -> int:
    gross_input = max(0, _safe_int(input_tokens))
    cache_reused = max(0, _safe_int(cache_read_tokens))
    output = max(0, _safe_int(output_tokens))
    # Actual consumed tokens = (total input tokens - cache reused tokens) + output tokens
    return max(0, gross_input - cache_reused) + output


def _is_passive_session(session_key: str, rec: Dict[str, Any]) -> bool:
    sk = str(session_key or "").lower()
    if any(flag in sk for flag in (":cron:", ":run:", ":heartbeat:", ":scheduler:")):
        return True

    origin = rec.get("origin") if isinstance(rec, dict) else {}
    if not isinstance(origin, dict):
        origin = {}

    provider = str(origin.get("provider") or "").strip().lower()
    if provider in {"heartbeat", "cron", "scheduler", "system", "auto"}:
        return True

    source = str(rec.get("source") or rec.get("trigger") or "").strip().lower()
    if source in {"heartbeat", "cron", "scheduler", "system", "auto"}:
        return True

    last_account_id = str(rec.get("lastAccountId") or "").strip().lower()
    if last_account_id in {"cron", "auto"} and not provider:
        return True

    return False


def _usage_day_and_tokens_from_line(line: str, day_keys: set[str]) -> Optional[Tuple[str, int]]:
    line = (line or "").strip()
    if not line:
        return None

    try:
        obj = json.loads(line)
    except Exception:
        return None

    if obj.get("type") != "message":
        return None

    msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
    usage = msg.get("usage") if isinstance(msg.get("usage"), dict) else {}
    if not usage:
        return None

    input_tokens = usage.get("input")
    output_tokens = usage.get("output")
    cache_read = usage.get("cacheRead")

    has_formula_fields = any(v is not None for v in (input_tokens, output_tokens, cache_read))
    if has_formula_fields:
        consumed = _actual_consumed_tokens(input_tokens, output_tokens, cache_read)
    else:
        total_tokens = usage.get("totalTokens")
        consumed = _safe_int(total_tokens)

    if consumed <= 0:
        return None

    ts_raw = obj.get("timestamp")
    dt: Optional[datetime] = None
    if isinstance(ts_raw, str):
        try:
            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
        except Exception:
            dt = None
    elif isinstance(ts_raw, (int, float)):
        try:
            dt = datetime.fromtimestamp(float(ts_raw) / 1000)
        except Exception:
            dt = None

    if not dt:
        return None

    day_key = dt.astimezone().strftime("%Y-%m-%d")
    if day_key not in day_keys:
        return None

    return day_key, consumed


def _scan_usage_jsonl(path: Path, start_offset: int, day_keys: set[str]) -> Tuple[int, Dict[str, int]]:
    add_map: Dict[str, int] = {}
    offset = max(0, int(start_offset or 0))

    try:
        with path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            size = int(f.tell())
            if offset > size:
                offset = 0

            f.seek(offset)
            # When reading from middle offset, discard first partial line to avoid JSON parse noise
            if offset > 0:
                _ = f.readline()

            while True:
                raw = f.readline()
                if not raw:
                    break
                parsed = _usage_day_and_tokens_from_line(raw.decode("utf-8", errors="replace"), day_keys)
                if not parsed:
                    continue
                day_key, consumed = parsed
                add_map[day_key] = int(add_map.get(day_key, 0)) + int(consumed)

            end_offset = int(f.tell())
            return end_offset, add_map
    except Exception:
        return 0, {}


def _sessions_dirs_stamp() -> Tuple[Tuple[str, int], ...]:
    rows: List[Tuple[str, int]] = []
    for d in AGENTS_DIR.glob("*/sessions"):
        if not d.is_dir():
            continue
        try:
            rows.append((str(d), int(d.stat().st_mtime_ns)))
        except Exception:
            continue
    rows.sort(key=lambda x: x[0])
    return tuple(rows)


def _list_session_jsonl_files() -> List[str]:
    now = time.time()
    dirs_stamp = _sessions_dirs_stamp()

    with _daily_tokens_lock:
        cached_files = _daily_tokens_cache.get("files")
        cached_ts = float(_daily_tokens_cache.get("filesTs", 0) or 0)
        cached_stamp = _daily_tokens_cache.get("dirsStamp")

    if (
        isinstance(cached_files, list)
        and now - cached_ts < _DAILY_FILELIST_TTL_SEC
        and cached_stamp == dirs_stamp
    ):
        return cached_files

    files = glob.glob(str(AGENTS_DIR / "*" / "sessions" / "*.jsonl"))
    with _daily_tokens_lock:
        _daily_tokens_cache.update({"files": files, "filesTs": now, "dirsStamp": dirs_stamp})
    return files


def _build_session_file_passive_map() -> Dict[str, bool]:
    mapping: Dict[str, bool] = {}

    def _looks_like_uuid(value: str) -> bool:
        s = str(value or "").strip().lower()
        if len(s) != 36:
            return False
        parts = s.split("-")
        if [len(p) for p in parts] != [8, 4, 4, 4, 12]:
            return False
        try:
            int("".join(parts), 16)
            return True
        except Exception:
            return False

    def _uuid_from_session_key(value: Any) -> str:
        raw = str(value or "").strip()
        if not raw:
            return ""
        if _looks_like_uuid(raw):
            return raw
        tail = raw.rsplit(":", 1)[-1].strip()
        if _looks_like_uuid(tail):
            return tail
        return ""

    session_files = glob.glob(str(AGENTS_DIR / "*" / "sessions" / "sessions.json"))
    for sf in session_files:
        sf_path = Path(sf)
        agent_id = sf_path.parents[1].name if len(sf_path.parents) >= 2 else ""

        data = _safe_read_json(sf_path, {})
        if not isinstance(data, dict):
            continue

        for session_key, rec in data.items():
            if not isinstance(rec, dict):
                continue

            is_passive = _is_passive_session(str(session_key), rec)

            session_file = str(rec.get("sessionFile") or "").strip()
            if session_file:
                mapping[session_file] = is_passive
                try:
                    mapping[str(Path(session_file).resolve())] = is_passive
                except Exception:
                    pass

            # Backfill: when sessionFile is missing (or sessionFile doesn't match sessionId),
            # derive default jsonl path from sessionId/session_key(UUID).
            session_uuid = str(rec.get("sessionId") or rec.get("session_id") or "").strip()
            if not _looks_like_uuid(session_uuid):
                session_uuid = _uuid_from_session_key(rec.get("sessionKey") or rec.get("session_key") or session_key)
            if not (agent_id and session_uuid):
                continue

            fallback_path = AGENTS_DIR / agent_id / "sessions" / f"{session_uuid}.jsonl"
            mapping[str(fallback_path)] = is_passive
            try:
                mapping[str(fallback_path.resolve())] = is_passive
            except Exception:
                pass

    return mapping


def _collect_daily_token_series(days: int = 30) -> List[Dict[str, Any]]:
    now = time.time()
    with _daily_tokens_lock:
        rows = _daily_tokens_cache.get("rows")
        ts = float(_daily_tokens_cache.get("ts", 0) or 0)
        if rows is not None and now - ts < _DAILY_TOKENS_TTL_SEC:
            return rows

        cached_day_map = _daily_tokens_cache.get("dayMap")
        cached_day_active_map = _daily_tokens_cache.get("dayActiveMap")
        cached_day_passive_map = _daily_tokens_cache.get("dayPassiveMap")
        cached_file_state = _daily_tokens_cache.get("fileState") or {}
        cached_file_contrib = _daily_tokens_cache.get("fileContrib") or {}
        cached_file_contrib_active = _daily_tokens_cache.get("fileContribActive") or {}
        cached_file_contrib_passive = _daily_tokens_cache.get("fileContribPassive") or {}
        cached_days = int(_daily_tokens_cache.get("days") or 0)
        cached_start_day = str(_daily_tokens_cache.get("startDay") or "")

    today = datetime.now().date()
    days = max(1, int(days))
    start_day = today - timedelta(days=days - 1)
    start_day_s = start_day.strftime("%Y-%m-%d")

    if isinstance(cached_day_map, dict) and cached_days == days and cached_start_day == start_day_s:
        day_map: Dict[str, int] = {k: int(v or 0) for k, v in cached_day_map.items()}
        day_active_map: Dict[str, int] = {
            k: int(v or 0)
            for k, v in (cached_day_active_map.items() if isinstance(cached_day_active_map, dict) else [])
        } or {k: 0 for k in day_map}
        day_passive_map: Dict[str, int] = {
            k: int(v or 0)
            for k, v in (cached_day_passive_map.items() if isinstance(cached_day_passive_map, dict) else [])
        } or {k: 0 for k in day_map}
        file_state: Dict[str, Dict[str, int]] = {
            str(k): (v if isinstance(v, dict) else {}) for k, v in cached_file_state.items()
        }
        file_contrib: Dict[str, Dict[str, int]] = {
            str(k): {dk: int(dv or 0) for dk, dv in (v or {}).items()}
            for k, v in cached_file_contrib.items()
            if isinstance(v, dict)
        }
        file_contrib_active: Dict[str, Dict[str, int]] = {
            str(k): {dk: int(dv or 0) for dk, dv in (v or {}).items()}
            for k, v in cached_file_contrib_active.items()
            if isinstance(v, dict)
        }
        file_contrib_passive: Dict[str, Dict[str, int]] = {
            str(k): {dk: int(dv or 0) for dk, dv in (v or {}).items()}
            for k, v in cached_file_contrib_passive.items()
            if isinstance(v, dict)
        }
        incremental_mode = True
    else:
        day_map = {(start_day + timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(days)}
        day_active_map = {(start_day + timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(days)}
        day_passive_map = {(start_day + timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(days)}
        file_state = {}
        file_contrib = {}
        file_contrib_active = {}
        file_contrib_passive = {}
        incremental_mode = False

    day_keys = set(day_map.keys())
    file_passive_map = _build_session_file_passive_map()

    jsonl_files = _list_session_jsonl_files()
    live_paths = set(jsonl_files)

    def _rollback_file_contrib(fp: str) -> None:
        prev = file_contrib.pop(fp, {})
        prev_active = file_contrib_active.pop(fp, {})
        prev_passive = file_contrib_passive.pop(fp, {})

        if isinstance(prev, dict):
            for day_key, val in prev.items():
                if day_key in day_map:
                    day_map[day_key] = int(day_map.get(day_key, 0)) - int(val or 0)
        if isinstance(prev_active, dict):
            for day_key, val in prev_active.items():
                if day_key in day_active_map:
                    day_active_map[day_key] = int(day_active_map.get(day_key, 0)) - int(val or 0)
        if isinstance(prev_passive, dict):
            for day_key, val in prev_passive.items():
                if day_key in day_passive_map:
                    day_passive_map[day_key] = int(day_passive_map.get(day_key, 0)) - int(val or 0)

        file_state.pop(fp, None)

    # In incremental mode: rollback historical contribution when file is deleted
    if incremental_mode:
        stale_paths = [fp for fp in list(file_contrib.keys()) if fp not in live_paths]
        for fp in stale_paths:
            _rollback_file_contrib(fp)

    for fp in jsonl_files:
        prev_state = file_state.get(fp, {}) if isinstance(file_state.get(fp, {}), dict) else {}
        prev_contrib = file_contrib.get(fp, {}) if isinstance(file_contrib.get(fp, {}), dict) else {}
        prev_contrib_active = file_contrib_active.get(fp, {}) if isinstance(file_contrib_active.get(fp, {}), dict) else {}
        prev_contrib_passive = file_contrib_passive.get(fp, {}) if isinstance(file_contrib_passive.get(fp, {}), dict) else {}

        p = Path(fp)
        try:
            st = p.stat()
        except Exception:
            # File deleted/rotated after filelist: immediately rollback old contribution to avoid overcount.
            _rollback_file_contrib(fp)
            continue

        # On initial build, skip historical files clearly outside the window
        if not incremental_mode:
            try:
                if datetime.fromtimestamp(st.st_mtime).date() < start_day:
                    continue
            except Exception:
                pass

        old_inode = int(prev_state.get("inode") or -1)
        old_size = int(prev_state.get("size") or 0)
        old_offset = int(prev_state.get("offset") or 0)
        inode = int(getattr(st, "st_ino", 0) or 0)
        size = int(st.st_size)
        mtime_ns = int(getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9)))

        can_incremental_read = (
            incremental_mode
            and bool(prev_state)
            and old_inode == inode
            and size >= old_offset
            and size >= old_size
        )

        is_passive_file = bool(file_passive_map.get(fp) or file_passive_map.get(str(p.resolve())))

        if can_incremental_read:
            start_offset = old_offset
            end_offset, add_map = _scan_usage_jsonl(p, start_offset, day_keys)
            if end_offset == 0 and size > 0:
                # On scan failure, don't update existing state to avoid dirty data overwrite
                continue

            merged = {k: int(v or 0) for k, v in prev_contrib.items()}
            merged_active = {k: int(v or 0) for k, v in prev_contrib_active.items()}
            merged_passive = {k: int(v or 0) for k, v in prev_contrib_passive.items()}
            for day_key, inc in add_map.items():
                inc = int(inc)
                day_map[day_key] = int(day_map.get(day_key, 0)) + inc
                merged[day_key] = int(merged.get(day_key, 0)) + inc
                if is_passive_file:
                    day_passive_map[day_key] = int(day_passive_map.get(day_key, 0)) + inc
                    merged_passive[day_key] = int(merged_passive.get(day_key, 0)) + inc
                else:
                    day_active_map[day_key] = int(day_active_map.get(day_key, 0)) + inc
                    merged_active[day_key] = int(merged_active.get(day_key, 0)) + inc
            file_contrib[fp] = merged
            file_contrib_active[fp] = merged_active
            file_contrib_passive[fp] = merged_passive
            file_state[fp] = {
                "inode": inode,
                "size": size,
                "offset": end_offset,
                "mtimeNs": mtime_ns,
            }
            continue

        # Non-incremental path (new file/rotation/truncation): rollback old contribution, then full rescan
        _rollback_file_contrib(fp)

        end_offset, full_map = _scan_usage_jsonl(p, 0, day_keys)
        if end_offset == 0 and size > 0:
            # On rescan failure, keep "rolled back and cache cleared" state to avoid hanging overcount
            continue

        full_map = {k: int(v or 0) for k, v in full_map.items()}
        active_map = full_map if not is_passive_file else {}
        passive_map = full_map if is_passive_file else {}

        for day_key, val in full_map.items():
            day_map[day_key] = int(day_map.get(day_key, 0)) + int(val)
        for day_key, val in active_map.items():
            day_active_map[day_key] = int(day_active_map.get(day_key, 0)) + int(val)
        for day_key, val in passive_map.items():
            day_passive_map[day_key] = int(day_passive_map.get(day_key, 0)) + int(val)

        file_contrib[fp] = full_map
        file_contrib_active[fp] = {k: int(v) for k, v in active_map.items()}
        file_contrib_passive[fp] = {k: int(v) for k, v in passive_map.items()}
        file_state[fp] = {
            "inode": inode,
            "size": size,
            "offset": end_offset,
            "mtimeNs": mtime_ns,
        }

    # Defense: prevent negative values from abnormal rollback
    for k in list(day_map.keys()):
        day_map[k] = max(0, int(day_map.get(k, 0)))
        day_active_map[k] = max(0, int(day_active_map.get(k, 0)))
        day_passive_map[k] = max(0, int(day_passive_map.get(k, 0)))

    rows = [
        {
            "date": k,
            "tokens": int(day_map.get(k, 0)),
            "activeTokens": int(day_active_map.get(k, 0)),
            "passiveTokens": int(day_passive_map.get(k, 0)),
        }
        for k in sorted(day_map.keys())
    ]
    with _daily_tokens_lock:
        _daily_tokens_cache.update(
            {
                "ts": now,
                "rows": rows,
                "dayMap": day_map,
                "dayActiveMap": day_active_map,
                "dayPassiveMap": day_passive_map,
                "fileState": file_state,
                "fileContrib": file_contrib,
                "fileContribActive": file_contrib_active,
                "fileContribPassive": file_contrib_passive,
                "days": days,
                "startDay": start_day_s,
            }
        )

    return rows


def _collect_models_usage(days: int = 15) -> Dict[str, Any]:
    now = time.time()
    days = max(1, int(days or 1))

    with _models_lock:
        cached = _models_cache.get("data")
        ts = float(_models_cache.get("ts", 0) or 0)
        cached_days = int(_models_cache.get("days") or 0)
        if cached is not None and now - ts < _MODELS_CACHE_TTL_SEC and cached_days == days:
            return cached

    cfg = _safe_read_json(OPENCLAW_CONFIG, {})
    providers = (
        cfg.get("models", {})
        .get("providers", {})
    )

    configured_models: Dict[str, Dict[str, Any]] = {}
    if isinstance(providers, dict):
        for provider_name, provider_cfg in providers.items():
            models = []
            if isinstance(provider_cfg, dict):
                models = provider_cfg.get("models") or []
            if isinstance(models, list):
                for m in models:
                    if not isinstance(m, dict):
                        continue
                    model_id = str(m.get("id") or "").strip()
                    if not model_id:
                        continue
                    configured_models[model_id] = {
                        "model": model_id,
                        "provider": provider_name,
                        "configured": True,
                        "displayName": m.get("name") or model_id,
                    }

    usage: Dict[str, Dict[str, Any]] = {}

    def _ensure_row(model: str, provider: Optional[str]) -> Dict[str, Any]:
        row = usage.setdefault(
            model,
            {
                "model": model,
                "provider": provider,
                "sessions": 0,
                "tokens": 0,
                "activeTokens": 0,
                "passiveTokens": 0,
                "activeSessions": 0,
                "passiveSessions": 0,
                "inputTokens": 0,
                "rawInputTokens": 0,
                "outputTokens": 0,
                "cacheRead": 0,
                "cacheWrite": 0,
                "configured": model in configured_models,
                "_activeSessionSet": set(),
                "_passiveSessionSet": set(),
            },
        )
        if not row.get("provider") and provider:
            row["provider"] = provider
        return row

    today = datetime.now().date()
    start_day = today - timedelta(days=days - 1)
    day_keys = {(start_day + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)}

    file_passive_map = _build_session_file_passive_map()
    jsonl_files = _list_session_jsonl_files()

    for fp in jsonl_files:
        p = Path(fp)
        is_passive_file = bool(file_passive_map.get(fp) or file_passive_map.get(str(p.resolve())))

        try:
            with p.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = (line or "").strip()
                    if not line:
                        continue

                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue

                    if obj.get("type") != "message":
                        continue

                    msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
                    usage_obj = msg.get("usage") if isinstance(msg.get("usage"), dict) else {}
                    if not usage_obj:
                        continue

                    ts_raw = obj.get("timestamp")
                    dt: Optional[datetime] = None
                    if isinstance(ts_raw, str):
                        try:
                            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                        except Exception:
                            dt = None
                    elif isinstance(ts_raw, (int, float)):
                        try:
                            dt = datetime.fromtimestamp(float(ts_raw) / 1000)
                        except Exception:
                            dt = None

                    if not dt:
                        continue

                    day_key = dt.astimezone().strftime("%Y-%m-%d")
                    if day_key not in day_keys:
                        continue

                    raw_input_tokens = _safe_int(usage_obj.get("input"))
                    output_tokens = _safe_int(usage_obj.get("output"))
                    cache_read = _safe_int(usage_obj.get("cacheRead"))
                    cache_write = _safe_int(usage_obj.get("cacheWrite"))

                    has_formula_fields = any(usage_obj.get(k) is not None for k in ("input", "output", "cacheRead"))
                    if has_formula_fields:
                        net_input_tokens = max(0, raw_input_tokens - cache_read)
                        consumed = net_input_tokens + max(0, output_tokens)
                    else:
                        consumed = _safe_int(usage_obj.get("totalTokens"))
                        net_input_tokens = max(0, consumed - max(0, output_tokens))

                    if consumed <= 0 and raw_input_tokens <= 0 and output_tokens <= 0 and cache_read <= 0 and cache_write <= 0:
                        continue

                    model = str(msg.get("model") or "unknown").strip() or "unknown"
                    provider = str(msg.get("provider") or configured_models.get(model, {}).get("provider") or "").strip() or None
                    row = _ensure_row(model, provider)

                    row["tokens"] += consumed
                    row["inputTokens"] += net_input_tokens
                    row["rawInputTokens"] += raw_input_tokens
                    row["outputTokens"] += output_tokens
                    row["cacheRead"] += cache_read
                    row["cacheWrite"] += cache_write

                    if is_passive_file:
                        row["passiveTokens"] += consumed
                        row["_passiveSessionSet"].add(fp)
                    else:
                        row["activeTokens"] += consumed
                        row["_activeSessionSet"].add(fp)
        except Exception:
            continue

    total_active_tokens = 0
    total_passive_tokens = 0
    active_session_set: set[str] = set()
    passive_session_set: set[str] = set()

    for model_id, row in usage.items():
        active_set = row.get("_activeSessionSet") or set()
        passive_set = row.get("_passiveSessionSet") or set()
        if not isinstance(active_set, set):
            active_set = set(active_set)
        if not isinstance(passive_set, set):
            passive_set = set(passive_set)

        row["activeSessions"] = len(active_set)
        row["passiveSessions"] = len(passive_set)
        row["sessions"] = row["activeSessions"] + row["passiveSessions"]
        row["configured"] = bool(row.get("configured") or model_id in configured_models)

        total_active_tokens += int(row.get("activeTokens") or 0)
        total_passive_tokens += int(row.get("passiveTokens") or 0)
        active_session_set.update(active_set)
        passive_session_set.update(passive_set)

        row.pop("_activeSessionSet", None)
        row.pop("_passiveSessionSet", None)

    # Fill in "configured but unused" models
    for model_id, meta in configured_models.items():
        usage.setdefault(
            model_id,
            {
                "model": model_id,
                "provider": meta.get("provider"),
                "sessions": 0,
                "tokens": 0,
                "activeTokens": 0,
                "passiveTokens": 0,
                "activeSessions": 0,
                "passiveSessions": 0,
                "inputTokens": 0,
                "rawInputTokens": 0,
                "outputTokens": 0,
                "cacheRead": 0,
                "cacheWrite": 0,
                "configured": True,
            },
        )

    rows = sorted(usage.values(), key=lambda r: r.get("tokens", 0), reverse=True)

    # Daily cumulative usage: use same window as model details for consistent display
    daily_rows = _collect_daily_token_series(days)

    payload = {
        "configuredCount": len(configured_models),
        "usedCount": sum(1 for r in rows if r.get("tokens", 0) > 0),
        "totalTokens": sum(int(r.get("tokens") or 0) for r in rows),
        "activeTokens": int(total_active_tokens),
        "passiveTokens": int(total_passive_tokens),
        "activeSessions": int(len(active_session_set)),
        "passiveSessions": int(len(passive_session_set)),
        "windowDays": int(days),
        "formula": "Actual consumed tokens = net input + output; net input = max(0, input - cache reused) (per model call)",
        "models": rows,
        "dailyTokens": daily_rows,
    }

    with _models_lock:
        _models_cache.update({"ts": now, "data": payload, "days": days})
    return payload


def _collect_memory_data(
    status_data: Optional[Dict[str, Any]] = None,
    crons_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    now = time.time()
    with _memory_lock:
        cached = _memory_cache.get("data")
        ts = float(_memory_cache.get("ts", 0) or 0)
        if cached is not None and now - ts < _MEMORY_CACHE_TTL_SEC:
            return cached

    today = datetime.now().strftime("%Y-%m-%d")

    workspace_dirs: List[Path] = []
    for p in sorted(OPENCLAW_DIR.glob("workspace*")):
        if p.is_dir():
            workspace_dirs.append(p)

    workspace_rows: List[Dict[str, Any]] = []
    recent_rows: List[Dict[str, Any]] = []
    total_entries = 0
    today_entries = 0

    for ws in workspace_dirs:
        mem_dir = ws / "memory"
        if not mem_dir.exists() or not mem_dir.is_dir():
            continue

        md_files = [f for f in mem_dir.glob("*.md") if f.is_file()]
        md_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        entries = len(md_files)
        today_count = sum(1 for f in md_files if f.name.startswith(today))
        total_entries += entries
        today_entries += today_count

        latest_file = md_files[0] if md_files else None
        latest_at_ms = int(latest_file.stat().st_mtime * 1000) if latest_file else None

        ws_name = ws.name.replace("workspace-", "")
        if ws_name == "workspace":
            ws_name = "main"
        workspace_rows.append(
            {
                "workspace": ws_name,
                "entries": entries,
                "todayEntries": today_count,
                "latestFile": latest_file.name if latest_file else "-",
                "latestAt": latest_at_ms,
            }
        )

        for f in md_files[:8]:
            recent_rows.append(
                {
                    "workspace": ws_name,
                    "file": f.name,
                    "updatedAt": int(f.stat().st_mtime * 1000),
                    "size": int(f.stat().st_size),
                }
            )

    workspace_rows.sort(key=lambda x: x.get("entries", 0), reverse=True)
    recent_rows.sort(key=lambda x: x.get("updatedAt", 0), reverse=True)

    central_dir = OPENCLAW_DIR / "memory-central"
    topics_dir = central_dir / "topics"
    memories_md_dir = central_dir / "memories-md"

    topic_files: List[Path] = []
    if topics_dir.exists():
        # Limit scan: max 50 files
        topic_count = 0
        for f in topics_dir.rglob("*.md"):
            if "_legacy_" in str(f):
                continue
            if f.is_file():
                topic_files.append(f)
                topic_count += 1
                if topic_count >= 50:  # Limit file count
                    break

    memories_md_files = [f for f in memories_md_dir.glob("*.md") if f.is_file()] if memories_md_dir.exists() else []

    def _sum_size(paths: List[Path]) -> int:
        s = 0
        for p in paths:
            try:
                s += int(p.stat().st_size)
            except Exception:
                pass
        return s

    openclaw_config = _safe_read_json(OPENCLAW_CONFIG, {})
    plugins_cfg = openclaw_config.get("plugins", {}) if isinstance(openclaw_config, dict) else {}
    plugin_slots = plugins_cfg.get("slots", {}) if isinstance(plugins_cfg, dict) else {}
    plugin_entries = plugins_cfg.get("entries", {}) if isinstance(plugins_cfg, dict) else {}
    hooks_cfg = openclaw_config.get("hooks", {}) if isinstance(openclaw_config, dict) else {}
    internal_hooks = (((hooks_cfg.get("internal") or {}) if isinstance(hooks_cfg, dict) else {}).get("entries") or {})

    memory_root = OPENCLAW_DIR / "memory"
    sqlite_files = [f for f in memory_root.glob("*.sqlite") if f.is_file()] if memory_root.exists() else []
    backups_dir = memory_root / "backups"
    backup_files = [f for f in backups_dir.glob("*.jsonl") if f.is_file()] if backups_dir.exists() else []

    lancedb_size = 0
    lancedb_dir = memory_root / "lancedb-pro"
    if lancedb_dir.exists():
        # Limit scan: max 100 files to avoid large directory slowdown
        file_count = 0
        for f in lancedb_dir.rglob("*"):
            if f.is_file():
                try:
                    lancedb_size += int(f.stat().st_size)
                    file_count += 1
                    if file_count >= 100:  # Limit file count
                        break
                except Exception:
                    pass

    latest_topic_at = None
    if topic_files:
        latest_topic_at = int(max(f.stat().st_mtime for f in topic_files) * 1000)

    jobs = (crons_data or {}).get("jobs", []) if isinstance(crons_data, dict) else []

    def _job_row(j: Dict[str, Any], effect: str) -> Dict[str, Any]:
        return {
            "name": j.get("name") or j.get("id") or "-",
            "enabled": bool(j.get("enabled", False)),
            "lastStatus": j.get("lastStatus") or "-",
            "lastStatusTone": _status_tone(j.get("lastStatus")),
            "nextRunAtMs": j.get("nextRunAtMs"),
            "lastRunAtMs": j.get("lastRunAtMs"),
            "effect": effect,
        }

    self_improve_rows: List[Dict[str, Any]] = []
    involve_rows: List[Dict[str, Any]] = []
    automation_rows: List[Dict[str, Any]] = []

    for j in jobs:
        if not isinstance(j, dict):
            continue
        name = str(j.get("name") or "")
        low = name.lower()
        schedule_text = str(j.get("scheduleText") or "-")
        current_model = str(j.get("currentModel") or "").strip() or "-"
        payload = j.get("payload") if isinstance(j.get("payload"), dict) else {}

        payload_text = ""
        if isinstance(payload, dict):
            for key in ("message", "prompt", "task", "description", "notes", "text"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    payload_text = value.lower()
                    break

        if "memory" in low or "memory-central" in low or "memory" in payload_text:
            automation_rows.append(
                {
                    **_job_row(j, "Maintain, refine, or use memory data via scheduled task."),
                    "scheduleText": schedule_text,
                    "currentModel": current_model,
                }
            )

        if (
            "evolver" in low
            or "memory-central" in low
        ):
            self_improve_rows.append(
                _job_row(
                    j,
                    "Drive memory rule sedimentation and index governance (write to central topics, append-only).",
                )
            )

        if (
            "review" in low
            or "involve" in low
        ):
            involve_rows.append(
                _job_row(
                    j,
                    "Drive intervention process rule sedimentation (trigger words/broadcast specs/exit conditions).",
                )
            )

    capabilities: List[Dict[str, Any]] = []

    def _append_capability(
        cap_id: str,
        title: str,
        source: str,
        status: str,
        detail: str,
        evidence: Optional[List[str]] = None,
    ) -> None:
        capabilities.append(
            {
                "id": cap_id,
                "title": title,
                "source": source,
                "status": status,
                "detail": detail,
                "evidence": evidence or [],
            }
        )

    memory_slot = str(plugin_slots.get("memory") or "").strip()
    if memory_slot and memory_slot.lower() != "none":
        slot_entry = plugin_entries.get(memory_slot) if isinstance(plugin_entries, dict) else {}
        slot_enabled = bool(slot_entry.get("enabled")) if isinstance(slot_entry, dict) else False
        _append_capability(
            f"slot:{memory_slot}",
            f"Active Memory Slot: {memory_slot}",
            "config",
            "active" if slot_enabled else "configured",
            "Current memory slot from openclaw.json config.",
            [f"plugins.slots.memory = {memory_slot}"],
        )

    for plugin_id in ("memory-core", "memory-lancedb"):
        entry = plugin_entries.get(plugin_id) if isinstance(plugin_entries, dict) else None
        if not isinstance(entry, dict):
            continue
        enabled = bool(entry.get("enabled", False))
        _append_capability(
            f"plugin:{plugin_id}",
            plugin_id,
            "config",
            "active" if enabled else "available",
            "Plugin entry exists in openclaw.json." if enabled else "Plugin configured but not enabled.",
            [f"plugins.entries.{plugin_id}.enabled = {str(enabled).lower()}"],
        )

    session_memory_hook = internal_hooks.get("session-memory") if isinstance(internal_hooks, dict) else None
    if isinstance(session_memory_hook, dict):
        enabled = bool(session_memory_hook.get("enabled", False))
        _append_capability(
            "hook:session-memory",
            "session-memory hook",
            "config",
            "active" if enabled else "available",
            "Internal hook handles memory sedimentation at session level.",
            [f"hooks.internal.entries.session-memory.enabled = {str(enabled).lower()}"],
        )

    if central_dir.exists():
        _append_capability(
            "data:memory-central",
            "memory-central",
            "filesystem",
            "active",
            f"Central memory hub exists with {len(topic_files)} topics and {len(memories_md_files)} memories-md files.",
            [str(central_dir)],
        )

    if workspace_rows:
        _append_capability(
            "data:workspace-memory",
            "workspace memory",
            "filesystem",
            "active",
            f"Detected {len(workspace_rows)} workspace memory directories with {total_entries} Markdown memories.",
            [str(OPENCLAW_DIR / 'workspace')],
        )

    if sqlite_files:
        _append_capability(
            "data:sqlite-memory",
            "SQLite memory store",
            "filesystem",
            "active",
            f"Detected {len(sqlite_files)} SQLite memory stores, total {_sum_size(sqlite_files)} bytes.",
            [str(memory_root)],
        )

    if lancedb_size > 0:
        _append_capability(
            "data:lancedb-store",
            "LanceDB data store",
            "filesystem",
            "active",
            f"Detected LanceDB data directory, size {lancedb_size} bytes. Indicates existing vector data on disk.",
            [str(lancedb_dir)],
        )

    if backup_files:
        _append_capability(
            "data:memory-backups",
            "memory backups",
            "filesystem",
            "active",
            f"Detected {len(backup_files)} memory backup files.",
            [str(backups_dir)],
        )

    if automation_rows:
        _append_capability(
            "automation:memory-crons",
            "memory-related crons",
            "runtime",
            "active",
            f"Detected {len(automation_rows)} memory-related enabled crons.",
            [CRON_JOBS_PATH.as_posix()],
        )

    payload = {
        "summary": {
            "workspaceCount": len(workspace_rows),
            "totalEntries": total_entries,
            "todayEntries": today_entries,
            "recentCount": len(recent_rows),
        },
        "workspaces": workspace_rows,
        "recent": recent_rows[:25],
        "central": {
            "exists": central_dir.exists(),
            "hasMemoryMd": (central_dir / "MEMORY.md").exists(),
            "topicsCount": len(topic_files),
            "memoriesMdCount": len(memories_md_files),
            "latestTopicAt": latest_topic_at,
        },
        "storage": {
            "sqliteCount": len(sqlite_files),
            "sqliteBytes": _sum_size(sqlite_files),
            "lancedbBytes": lancedb_size,
            "backupCount": len(backup_files),
        },
        "capabilities": capabilities,
        "automations": automation_rows,
        "impacts": {
            "selfImprove": {
                "count": len(self_improve_rows),
                "items": self_improve_rows,
            },
            "involve": {
                "count": len(involve_rows),
                "items": involve_rows,
            },
        },
    }

    with _memory_lock:
        _memory_cache.update({"ts": now, "data": payload})
    return payload


def _extract_unfinished_goals_for_job(job: Dict[str, Any], content_text: str) -> List[str]:
    goals: List[str] = []
    text_lc = (content_text or "").lower()

    # For review tasks, supplement with unfinished items from monitor-state.json
    if "monitor-state" in text_lc:
        monitor_path = OPENCLAW_DIR / "workspace-review_agent" / "monitor-state.json"
        m = _safe_read_json(monitor_path, {})
        issues = m.get("openIssues", []) if isinstance(m, dict) else []
        if isinstance(issues, list):
            for it in issues:
                if not isinstance(it, dict):
                    continue
                st = str(it.get("status") or "").lower()
                pending = bool(it.get("pendingNeverAction", False))
                if st in {"open", "todo", "pending", "in_progress"} or pending:
                    goals.append(
                        f"- [{it.get('id') or 'issue'}] {it.get('description') or ''} (action: {it.get('action') or '-'})"
                    )

    return goals


def _build_cron_monitor_text(job: Dict[str, Any]) -> str:
    payload = job.get("payload") if isinstance(job.get("payload"), dict) else {}

    msg = ""
    for k in ["text", "message", "prompt", "task", "description", "notes"]:
        v = payload.get(k) if isinstance(payload, dict) else None
        if isinstance(v, str) and v.strip():
            msg = v.strip()
            break
        v2 = job.get(k)
        if isinstance(v2, str) and v2.strip():
            msg = v2.strip()
            break

    if not msg:
        if isinstance(payload, dict) and payload:
            try:
                msg = json.dumps(payload, ensure_ascii=False, indent=2)
            except Exception:
                msg = str(payload)
        else:
            msg = "This task has no configured work content."

    goals = _extract_unfinished_goals_for_job(job, msg)

    if goals:
        goal_text = "\n\nCurrent unfinished goals:\n" + "\n".join(goals)
    else:
        goal_text = "\n\nCurrent unfinished goals:\n- None"

    txt = f"{msg}{goal_text}"
    return txt[:7000]


def _humanize_cron_expr(expr: str, tz: str = "") -> str:
    expr = str(expr or "").strip()
    if not expr:
        return "-"

    parts = expr.split()
    if len(parts) != 5:
        return f"{expr} ({tz})" if tz else expr

    minute, hour, dom, month, dow = parts
    dow_map = {
        "0": "Sun",
        "1": "Mon",
        "2": "Tue",
        "3": "Wed",
        "4": "Thu",
        "5": "Fri",
        "6": "Sat",
        "7": "Sun",
    }

    def _fmt_hm(h: str, m: str) -> Optional[str]:
        if h.isdigit() and m.isdigit():
            return f"{int(h):02d}:{int(m):02d}"
        return None

    label: Optional[str] = None
    hm = _fmt_hm(hour, minute)
    if dom == "*" and month == "*" and dow == "*" and hm:
        label = f"Daily {hm}"
    elif dom == "*" and month == "*" and dow in dow_map and hm:
        label = f"{dow_map[dow]} {hm}"
    elif dom == "*" and month == "*" and hour == "*" and minute.startswith("*/"):
        label = f"Every {minute[2:]} min"
    elif dom == "*" and month == "*" and minute.isdigit() and hour.startswith("*/"):
        label = f"Every {hour[2:]}h at :{int(minute):02d}"
    elif dom == "*" and month == "*" and dow == "*" and minute.isdigit() and hour == "*":
        label = f"Hourly at :{int(minute):02d}"
    elif dom.isdigit() and month == "*" and dow == "*" and hm:
        label = f"Monthly {int(dom)}th {hm}"

    if label:
        return f"{label} ({tz})" if tz else label
    return f"{expr} ({tz})" if tz else expr


def _describe_schedule(schedule: Any) -> str:
    if isinstance(schedule, str):
        raw = schedule.strip()
        if not raw:
            return "-"
        if raw.endswith(")") and " (" in raw:
            expr, tz = raw.rsplit(" (", 1)
            return _humanize_cron_expr(expr.strip(), tz[:-1].strip())
        return _humanize_cron_expr(raw)

    if not isinstance(schedule, dict):
        return "-"

    kind = str(schedule.get("kind") or "").strip().lower()
    if kind == "every":
        every_ms = _safe_int(schedule.get("everyMs"))
        if every_ms <= 0:
            return "every"
        total_sec = max(1, every_ms // 1000)
        if total_sec % 86400 == 0:
            return f"Every {total_sec // 86400} day(s)"
        if total_sec % 3600 == 0:
            return f"Every {total_sec // 3600} hour(s)"
        if total_sec % 60 == 0:
            return f"Every {total_sec // 60} min"
        return f"Every {total_sec}s"

    if kind == "cron":
        expr = str(schedule.get("expr") or "").strip() or "-"
        tz = str(schedule.get("tz") or "").strip()
        return _humanize_cron_expr(expr, tz)

    if kind == "at":
        return str(schedule.get("at") or "-")

    return kind or "-"


# Cron run files cache
_cron_run_cache: Dict[str, Tuple[float, Optional[Dict[str, Any]]]] = {}
_cron_run_cache_ttl_sec = 30  # 30 second cache


def _prefetch_cron_run_files(jobs: List[Dict[str, Any]]) -> None:
    """Prefetch cron run files, use mtime to avoid re-reading unchanged files"""
    global _cron_run_cache

    now = time.time()

    for job in jobs:
        if not isinstance(job, dict):
            continue
        job_id = str(job.get("id") or "")
        if not job_id:
            continue

        run_file = CRON_RUNS_DIR / f"{job_id}.jsonl"
        cache_key = str(run_file)

        # Check if cache is valid
        cached = _cron_run_cache.get(cache_key)
        if cached:
            cached_time, _ = cached
            if now - cached_time < _cron_run_cache_ttl_sec:
                continue  # Cache valid, skip

        # Check file mtime
        try:
            if run_file.exists():
                mtime = run_file.stat().st_mtime
                # If file unchanged, only update timestamp
                if cached and mtime <= cached_time:
                    _cron_run_cache[cache_key] = (now, cached[1])
                    continue
        except Exception:
            pass


def _collect_cron_data() -> Dict[str, Any]:
    jobs_payload = _read_json_tolerant(CRON_JOBS_PATH, {"jobs": []})
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    available_models, _ = _available_models_payload()

    running = 0
    normalized_jobs = []
    enabled_total = 0
    total_jobs = 0
    agent_ids: List[str] = []

    # Batch prefetch run files (reduce IO)
    _prefetch_cron_run_files(jobs)

    for job in jobs:
        if not isinstance(job, dict):
            continue
        total_jobs += 1
        enabled = bool(job.get("enabled", False))
        if not enabled:
            continue
        enabled_total += 1
        job_id = str(job.get("id") or "")

        state = job.get("state", {}) if isinstance(job.get("state"), dict) else {}
        last_status_raw = state.get("lastStatus") or state.get("lastRunStatus") or "-"
        last_status = str(last_status_raw or "").strip().lower()

        active_status = {"running", "started", "processing", "in_progress", "pending", "queued"}
        terminal_status = {"completed", "complete", "success", "succeeded", "ok", "failed", "error", "cancelled", "canceled", "skipped", "timeout", "timed_out", "done"}

        # Prefer status from jobs.json to reduce jsonl reads
        if last_status in active_status:
            is_running = True
            last_event = None  # No need to read jsonl
        elif last_status in terminal_status:
            is_running = False
            last_event = None  # No need to read jsonl
        else:
            # Only read jsonl when status is unclear
            is_running = False
            run_file = CRON_RUNS_DIR / f"{job_id}.jsonl"
            last_event = _read_last_jsonl_obj(run_file)
            if isinstance(last_event, dict):
                event_hint = str(last_event.get("action") or last_event.get("status") or "").lower()
                if event_hint in active_status:
                    is_running = True
                elif event_hint in terminal_status:
                    is_running = False

        if is_running:
            running += 1

        agent_id = str(job.get("agentId") or "").strip()
        if _is_meaningful_agent_id(agent_id):
            agent_ids.append(agent_id)

        normalized_jobs.append(
            {
                "id": job_id,
                "name": job.get("name") or job_id,
                "agentId": agent_id or "-",
                "enabled": enabled,
                "running": is_running,
                "lastStatus": last_status_raw,
                "lastStatusTone": _status_tone(last_status_raw),
                "lastRunAtMs": state.get("lastRunAtMs"),
                "nextRunAtMs": state.get("nextRunAtMs"),
                "lastDurationMs": state.get("lastDurationMs"),
                "schedule": job.get("schedule") or {},
                "scheduleText": _describe_schedule(job.get("schedule") or {}),
                "currentModel": str(((job.get("payload") or {}) if isinstance(job.get("payload"), dict) else {}).get("model") or "").strip() or "-",
                "payload": job.get("payload") if isinstance(job.get("payload"), dict) else {},
            }
        )

    normalized_jobs.sort(key=lambda x: (x.get("nextRunAtMs") or 10**18, x.get("name") or ""))
    distinct_agent_ids = sorted(set(agent_ids))

    return {
        "total": total_jobs,
        "enabled": enabled_total,
        "disabled": max(0, total_jobs - enabled_total),
        "running": running,
        "hasAgentAssociation": len(distinct_agent_ids) > 1,
        "availableModels": available_models,
        "jobs": normalized_jobs,
    }


def _get_cron_monitor_text(job_id: str) -> str:
    jobs_payload = _read_json_tolerant(CRON_JOBS_PATH, {"jobs": []})
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        if str(job.get("id") or "") == str(job_id):
            return _build_cron_monitor_text(job)
    return "Task not found, may have been deleted or renamed."


def _build_channels_from_status(status_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    lines = status_data.get("channelSummary") or []
    channels: List[Dict[str, Any]] = []

    for ln in lines:
        if not isinstance(ln, str):
            continue
        if ":" not in ln:
            continue
        if ln.startswith("  -"):
            continue
        name, tail = ln.split(":", 1)
        state_txt = tail.strip().lower()
        channels.append(
            {
                "name": name.strip().lower(),
                "label": name.strip(),
                "state": state_txt,
                "configured": "configured" in state_txt,
            }
        )
    return channels


def _check_agent_running_via_fs(agent_id: str) -> Tuple[bool, Optional[int]]:
    """
    Fast detection of Agent running status.
    Uses os.scandir to directly read directory, avoiding glob overhead.
    Returns: (is_running, last_active_ms)
    """
    global _agent_fs_cache

    now = time.time()

    # Check cache
    with _agent_fs_cache_lock:
        cached = _agent_fs_cache.get(agent_id)
        if cached:
            cached_time, cached_running, cached_age = cached
            if now - cached_time < _agent_fs_cache_ttl_sec:
                return cached_running, cached_age

    sessions_dir = AGENTS_DIR / agent_id / "sessions"

    try:
        # Use os.scandir for fast scan (2-5x faster than glob)
        latest_mtime = 0.0
        with os.scandir(sessions_dir) as it:
            for entry in it:
                if entry.name.endswith('.jsonl') and entry.is_file():
                    try:
                        st = entry.stat(follow_symlinks=False)
                        if st.st_mtime > latest_mtime:
                            latest_mtime = st.st_mtime
                    except Exception:
                        continue
        
        if latest_mtime == 0:
            with _agent_fs_cache_lock:
                _agent_fs_cache[agent_id] = (now, False, None)
            return False, None
        
        age_ms = int((now - latest_mtime) * 1000)
        is_running = age_ms <= ACTIVE_AGENT_WINDOW_MS
        
        with _agent_fs_cache_lock:
            _agent_fs_cache[agent_id] = (now, is_running, age_ms)
        
        return is_running, age_ms
    except Exception:
        with _agent_fs_cache_lock:
            _agent_fs_cache[agent_id] = (now, False, None)
        return False, None


def _collect_agents_data(status_data: Dict[str, Any], subagents: Dict[str, Any]) -> Dict[str, Any]:
    agents_block = status_data.get("agents", {}) if isinstance(status_data, dict) else {}
    heartbeat_block = status_data.get("heartbeat", {}) if isinstance(status_data, dict) else {}
    agent_model_map = _agent_model_map_from_config()
    available_models, _ = _available_models_payload()

    hb_map: Dict[str, Dict[str, Any]] = {}
    for row in heartbeat_block.get("agents", []) if isinstance(heartbeat_block, dict) else []:
        if isinstance(row, dict) and row.get("agentId"):
            hb_map[str(row["agentId"])] = row

    sub_runs = subagents.get("runs", []) if isinstance(subagents, dict) else []

    result_agents: List[Dict[str, Any]] = []
    running_count = 0

    for a in agents_block.get("agents", []) if isinstance(agents_block, dict) else []:
        if not isinstance(a, dict):
            continue
        aid = str(a.get("id") or "")
        
        # Prefer filesystem real-time detection (faster)
        fs_running, fs_age_ms = _check_agent_running_via_fs(aid)

        # Also reference status data (as backup)
        status_age_ms = a.get("lastActiveAgeMs")

        # Take smaller age (more accurate active time)
        if fs_age_ms is not None and status_age_ms is not None:
            effective_age_ms = min(fs_age_ms, status_age_ms)
            agent_running = fs_running or (isinstance(status_age_ms, (int, float)) and status_age_ms <= ACTIVE_AGENT_WINDOW_MS)
        elif fs_age_ms is not None:
            effective_age_ms = fs_age_ms
            agent_running = fs_running
        else:
            effective_age_ms = status_age_ms
            agent_running = isinstance(status_age_ms, (int, float)) and status_age_ms <= ACTIVE_AGENT_WINDOW_MS

        own_subs = []
        for s in sub_runs:
            if not isinstance(s, dict):
                continue
            parent = s.get("parentAgentId") or ""
            sk = s.get("sessionKey") or ""
            if parent == aid or f"agent:{aid}:" in str(sk):
                own_subs.append(s)

        sub_running = sum(
            1
            for s in own_subs
            if str(s.get("status", "")).lower()
            in {"running", "active", "started", "in_progress", "processing"}
        )

        if agent_running or sub_running > 0:
            running_count += 1

        hb = hb_map.get(aid, {})
        result_agents.append(
            {
                "id": aid,
                "name": a.get("name") or aid,
                "workspaceDir": a.get("workspaceDir"),
                "sessionsCount": int(a.get("sessionsCount") or 0),
                "lastUpdatedAt": a.get("lastUpdatedAt"),
                "lastActiveAgeMs": effective_age_ms,
                "running": bool(agent_running),
                "subagentsTotal": len(own_subs),
                "subagentsRunning": sub_running,
                "heartbeatEnabled": bool(hb.get("enabled", False)),
                "heartbeatEvery": hb.get("every") or "disabled",
                "currentModel": str(agent_model_map.get(aid) or a.get("model") or "-").strip() or "-",
            }
        )

    result_agents.sort(key=lambda x: (not x["running"], x["id"]))

    return {
        "total": len(result_agents),
        "running": running_count,
        "availableModels": available_models,
        "agents": result_agents,
    }


def _collect_openclaw_summary(status_data: Optional[Dict[str, Any]], status_err: Optional[str]) -> Dict[str, Any]:
    """
    Summarize OpenClaw status.
    Uses TCP port probe (1-3ms) for quick online check, combined with openclaw status details.
    """
    # TCP port probe (completes in 1-3ms)
    tcp_probe = _get_tcp_probe_status()
    tcp_reachable = tcp_probe.get("reachable", False)
    tcp_latency_ms = tcp_probe.get("latencyMs")

    # If no status data, use TCP probe result
    if not status_data:
        if tcp_reachable:
            return {
                "ok": True,
                "state": "Online",
                "error": status_err,
                "gateway": {
                    "reachable": True,
                    "latencyMs": tcp_latency_ms,
                    "url": "127.0.0.1:8080",
                    "service": "running",
                },
                "security": {},
                "update": {},
                "channels": [],
            }
        return {
            "ok": False,
            "state": "Offline",
            "error": status_err or "Cannot reach OpenClaw",
            "gateway": {
                "reachable": False,
                "url": "127.0.0.1:8080",
            },
            "security": {},
            "update": {},
            "channels": [],
        }

    gateway = status_data.get("gateway") or {}
    gateway_service = status_data.get("gatewayService") or {}
    security = status_data.get("securityAudit") or {}
    update = status_data.get("update") or {}

    critical = int((security.get("summary") or {}).get("critical") or 0)
    warns = int((security.get("summary") or {}).get("warn") or 0)

    # Prefer TCP probe result for reachability (faster and more accurate).
    # When TCP probe explicitly returns False, trust it over stale cached gateway.reachable.
    if tcp_reachable is not None:
        gateway_reachable = tcp_reachable
    else:
        gateway_reachable = bool(gateway.get("reachable", False))

    # Use TCP probe latency if available
    effective_latency_ms = tcp_latency_ms if tcp_latency_ms is not None else gateway.get("connectLatencyMs")
    
    runtime_short = str(gateway_service.get("runtimeShort") or "")
    service_running = "running" in runtime_short.lower()

    runtime_lc = runtime_short.lower()
    restarting_signals = (
        "activating",
        "starting",
        "restarting",
        "reload",
        "draining",
        "deactivating",
    )

    # 3 states: Online / Restarting / Offline
    # TCP probe is real-time; service_running may come from stale cache.
    # When TCP probe explicitly says unreachable, don't trust cached service_running.
    if any(sig in runtime_lc for sig in restarting_signals):
        state = "Restarting"
    elif tcp_reachable or gateway_reachable:
        state = "Online"
    elif service_running and tcp_reachable is not False:
        state = "Online"
    else:
        state = "Offline"

    channels = _build_channels_from_status(status_data)

    return {
        "ok": True,
        "state": state,
        "gateway": {
            "reachable": gateway_reachable,
            "latencyMs": effective_latency_ms,
            "url": gateway.get("url") or "127.0.0.1:8080",
            "service": runtime_short or ("running" if tcp_reachable else ""),
        },
        "security": {
            "critical": critical,
            "warn": warns,
            "info": int((security.get("summary") or {}).get("info") or 0),
        },
        "update": {
            "latestVersion": (update.get("registry") or {}).get("latestVersion"),
            "installKind": update.get("installKind"),
        },
        "channels": channels,
        "error": status_err,
    }


def _build_dashboard_payload() -> Dict[str, Any]:
    status_data, status_err = _run_openclaw_status()
    status_ts_ms = _cache_ts_ms(_status_cache, _status_lock)

    subagents = _collect_subagent_runs()
    subagents_ts_ms = int(time.time() * 1000)

    agents = _collect_agents_data(status_data or {}, subagents)
    agents_ts_ms = int(time.time() * 1000)

    crons = _collect_cron_data()
    crons_ts_ms = int(time.time() * 1000)

    models = _collect_models_usage()
    models_ts_ms = _cache_ts_ms(_models_cache, _models_lock) or int(time.time() * 1000)

    memory_data = _collect_memory_data(status_data=status_data or {}, crons_data=crons)
    memory_ts_ms = _cache_ts_ms(_memory_cache, _memory_lock) or int(time.time() * 1000)

    openclaw_summary = _collect_openclaw_summary(status_data, status_err)
    openclaw_ts_ms = status_ts_ms or int(time.time() * 1000)

    sessions = (status_data or {}).get("sessions", {})
    recent_sessions = sessions.get("recent", []) if isinstance(sessions, dict) else []

    main_model = "unknown"
    main_tokens = 0
    for rs in recent_sessions:
        if not isinstance(rs, dict):
            continue
        if rs.get("agentId") == "main":
            main_model = str(rs.get("model") or main_model)
            main_tokens = int(rs.get("totalTokens") or 0)
            break

    generated_at_ms = int(time.time() * 1000)
    source_timestamps = {
        "status": status_ts_ms,
        "openclaw": openclaw_ts_ms,
        "agents": agents_ts_ms,
        "subagents": subagents_ts_ms,
        "crons": crons_ts_ms,
        "models": models_ts_ms,
        "memory": memory_ts_ms,
    }
    source_lags_ms = {
        k: (max(0, generated_at_ms - int(v)) if isinstance(v, (int, float)) else None)
        for k, v in source_timestamps.items()
    }

    payload = {
        "title": APP_TITLE,
        "generatedAt": generated_at_ms,
        "sourceTimestamps": source_timestamps,
        "sourceLagsMs": source_lags_ms,
        "overview": {
            "agentCount": agents["total"],
            "runningAgents": agents["running"],
            "subagentCount": subagents["total"],
            "runningSubagents": subagents["running"],
            "cronCount": crons["total"],
            "runningCrons": crons["running"],
            "modelCount": models["configuredCount"],
            "tokens": models["totalTokens"],
            "model": main_model,
            "mainTokens": main_tokens,
            "status": openclaw_summary.get("state"),
        },
        "agents": agents,
        "subagents": subagents,
        "crons": crons,
        "models": models,
        "memory": memory_data,
        "openclaw": openclaw_summary,
        "sessions": sessions,
        "usage": (status_data or {}).get("usage") or {},
    }
    return payload


def _empty_dashboard_payload() -> Dict[str, Any]:
    now_ms = int(time.time() * 1000)
    return {
        "title": APP_TITLE,
        "generatedAt": now_ms,
        "sourceTimestamps": {
            "status": None,
            "openclaw": None,
            "agents": None,
            "subagents": None,
            "crons": None,
            "models": None,
            "memory": None,
        },
        "sourceLagsMs": {
            "status": None,
            "openclaw": None,
            "agents": None,
            "subagents": None,
            "crons": None,
            "models": None,
            "memory": None,
        },
        "overview": {
            "agentCount": 0,
            "runningAgents": 0,
            "subagentCount": 0,
            "runningSubagents": 0,
            "cronCount": 0,
            "runningCrons": 0,
            "modelCount": 0,
            "tokens": 0,
            "model": "-",
            "mainTokens": 0,
            "status": "Loading",
        },
        "agents": {"total": 0, "running": 0, "agents": []},
        "subagents": {"total": 0, "running": 0, "runs": []},
        "crons": {"total": 0, "enabled": 0, "disabled": 0, "running": 0, "jobs": []},
        "models": {
            "configuredCount": 0,
            "usedCount": 0,
            "totalTokens": 0,
            "activeTokens": 0,
            "passiveTokens": 0,
            "activeSessions": 0,
            "passiveSessions": 0,
            "formula": "Actual consumed = net input + output; net input = max(0, input - cache reused)",
            "models": [],
            "dailyTokens": [],
        },
        "memory": {
            "summary": {"workspaceCount": 0, "totalEntries": 0, "todayEntries": 0, "recentCount": 0},
            "workspaces": [],
            "recent": [],
            "central": {"exists": False, "hasMemoryMd": False, "topicsCount": 0, "memoriesMdCount": 0, "latestTopicAt": None},
            "storage": {"sqliteCount": 0, "sqliteBytes": 0, "lancedbBytes": 0, "backupCount": 0},
            "capabilities": [],
            "automations": [],
            "impacts": {"selfImprove": {"count": 0, "items": []}, "involve": {"count": 0, "items": []}},
        },
        "openclaw": {"ok": False, "state": "Loading", "error": "warming up", "gateway": {}, "security": {}, "update": {}, "channels": []},
        "sessions": {},
        "usage": {},
    }


def _refresh_dashboard_cache_sync() -> None:
    global _dash_refreshing
    try:
        data = _build_dashboard_payload()
        with _dash_lock:
            _dash_cache.update({"ts": time.time(), "data": data})
    finally:
        with _dash_lock:
            _dash_refreshing = False


def _start_dashboard_refresh() -> None:
    global _dash_refreshing
    with _dash_lock:
        if _dash_refreshing:
            return
        _dash_refreshing = True
    t = threading.Thread(target=_refresh_dashboard_cache_sync, daemon=True, name="clawstatus-dash-refresh")
    t.start()


def _get_dashboard_payload() -> Dict[str, Any]:
    now = time.time()
    with _dash_lock:
        cached = _dash_cache.get("data")
        cached_ts = float(_dash_cache.get("ts", 0) or 0)

    # First time no cache: return placeholder data, build async in background for instant load
    if cached is None:
        _start_dashboard_refresh()
        return _empty_dashboard_payload()

    # Cache hit: return directly
    if now - cached_ts < _DASH_CACHE_TTL_SEC:
        return cached

    # Cache expired: return stale data and async refresh to avoid blocking
    _start_dashboard_refresh()
    return cached


def create_app() -> Flask:
    app = Flask(__name__)
    # Requirement: page works out of box, no token input needed
    required_token = None

    @app.after_request
    def _disable_cache(resp):
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    # Background warmup openclaw status to avoid first API request blocking
    global _bg_warmup_started
    if not _bg_warmup_started:
        t = threading.Thread(target=_bg_status_warmup_loop, daemon=True, name="clawstatus-warmup")
        t.start()
        # Start inotify event monitoring (zero polling, Linux only)
        _start_inotify_monitor()
        _bg_warmup_started = True

    # Dashboard data warmup (async) to avoid first request blocking
    _start_dashboard_refresh()

    @app.get("/")
    def index() -> Response:
        return Response(_index_html(required_token), mimetype="text/html")

    @app.get("/api/auth/check")
    def api_auth_check():
        valid = _is_authorized(required_token)
        # Treat as valid when no token configured
        if not required_token:
            valid = True
        return jsonify(
            {
                "valid": valid,
                "requiresAuth": bool(required_token),
                "project": APP_TITLE,
                "version": __version__,
            }
        )

    @app.get("/api/dashboard")
    def api_dashboard():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        return jsonify(_get_dashboard_payload())

    @app.get("/api/overview")
    def api_overview():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        out = dict(data.get("overview", {}))
        out["_sourceLagsMs"] = data.get("sourceLagsMs", {})
        out["_sourceTimestamps"] = data.get("sourceTimestamps", {})
        return jsonify(out)

    @app.get("/api/agents")
    def api_agents():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        out = dict(data.get("agents", {}))
        out["_sourceLagsMs"] = data.get("sourceLagsMs", {})
        out["_sourceTimestamps"] = data.get("sourceTimestamps", {})
        return jsonify(out)

    @app.post("/api/agents/<agent_id>/model")
    def api_agent_model_update(agent_id: str):
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        payload = request.get_json(silent=True) or {}
        model_id = str(payload.get("model") or "").strip()
        if not model_id:
            return jsonify({"error": "missing model"}), 400
        try:
            result = _update_agent_model(agent_id, model_id)
        except KeyError:
            return jsonify({"error": "agent not found", "agentId": agent_id}), 404
        except ValueError:
            return jsonify({"error": "invalid model", "model": model_id}), 400
        except PermissionError as e:
            return jsonify({"error": f"write failed: {e}"}), 500
        except OSError as e:
            return jsonify({"error": f"write failed: {e}"}), 500
        return jsonify(result)

    @app.get("/api/crons")
    def api_crons():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        out = dict(data.get("crons", {}))
        out["_sourceLagsMs"] = data.get("sourceLagsMs", {})
        out["_sourceTimestamps"] = data.get("sourceTimestamps", {})
        return jsonify(out)

    @app.post("/api/crons/<job_id>/model")
    def api_cron_model_update(job_id: str):
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        payload = request.get_json(silent=True) or {}
        model_id = str(payload.get("model") or "").strip()
        if not model_id:
            return jsonify({"error": "missing model"}), 400
        try:
            result = _update_cron_model(job_id, model_id)
        except KeyError:
            return jsonify({"error": "cron not found", "jobId": job_id}), 404
        except ValueError:
            return jsonify({"error": "invalid model", "model": model_id}), 400
        except PermissionError as e:
            return jsonify({"error": f"write failed: {e}"}), 500
        except OSError as e:
            return jsonify({"error": f"write failed: {e}"}), 500
        return jsonify(result)

    @app.post("/api/crons/<job_id>/run")
    def api_cron_run(job_id: str):
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        try:
            result = _trigger_cron_run(job_id)
        except KeyError:
            return jsonify({"error": "cron not found", "jobId": job_id}), 404
        return jsonify(result)

    @app.post("/api/crons/<job_id>/delete")
    def api_cron_delete(job_id: str):
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        try:
            result = _delete_cron_job(job_id)
        except KeyError:
            return jsonify({"error": "cron not found", "jobId": job_id}), 404
        except OSError as e:
            return jsonify({"error": str(e), "jobId": job_id}), 500
        return jsonify(result)

    @app.get("/api/cron-monitor/<job_id>")
    def api_cron_monitor(job_id: str):
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        text = _get_cron_monitor_text(job_id)
        return jsonify({"id": job_id, "monitorText": text})

    @app.get("/api/openclaw")
    def api_openclaw():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        out = dict(data.get("openclaw", {}))
        out["_sourceLagsMs"] = data.get("sourceLagsMs", {})
        out["_sourceTimestamps"] = data.get("sourceTimestamps", {})
        return jsonify(out)

    @app.get("/api/models")
    def api_models():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        out = dict(data.get("models", {}))
        out["_sourceLagsMs"] = data.get("sourceLagsMs", {})
        out["_sourceTimestamps"] = data.get("sourceTimestamps", {})
        return jsonify(out)

    @app.get("/api/memory")
    def api_memory():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        out = dict(data.get("memory", {}))
        out["_sourceLagsMs"] = data.get("sourceLagsMs", {})
        out["_sourceTimestamps"] = data.get("sourceTimestamps", {})
        return jsonify(out)

    # ---- Legacy API compatibility (for existing scripts/tests) ----
    @app.get("/api/health")
    def api_health():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        status_data, status_err = _run_openclaw_status()
        checks = [
            {"name": "openclaw_status", "ok": status_data is not None, "error": status_err},
            {"name": "config", "ok": OPENCLAW_CONFIG.exists(), "path": str(OPENCLAW_CONFIG)},
        ]
        ok = all(c.get("ok") for c in checks)
        return jsonify({"ok": ok, "checks": checks, "time": int(time.time() * 1000)})

    @app.get("/api/system-health")
    def api_system_health():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        return jsonify(data.get("openclaw", {}))

    @app.get("/api/channels")
    def api_channels():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        return jsonify({"channels": data.get("openclaw", {}).get("channels", [])})

    @app.get("/api/channel/<channel>")
    def api_channel_single(channel: str):
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        channels = data.get("openclaw", {}).get("channels", [])
        current = next((c for c in channels if c.get("name") == channel.lower()), None)
        payload = {
            "channel": channel,
            "configured": bool(current and current.get("configured")),
            "state": (current or {}).get("state", "unknown"),
            "messages": [],
        }
        if channel.lower() in {"telegram", "imessage"}:
            payload["todayIn"] = 0
            payload["todayOut"] = 0
        return jsonify(payload)

    @app.get("/api/sessions")
    def api_sessions():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        return jsonify(data.get("sessions", {}))

    @app.get("/api/usage")
    def api_usage():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        return jsonify({"usage": data.get("usage", {}), "models": data.get("models", {})})

    @app.get("/api/transcripts")
    def api_transcripts():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        return jsonify({"transcripts": []})

    @app.get("/api/subagents")
    def api_subagents():
        auth_resp = _require_auth(required_token)
        if auth_resp is not None:
            return auth_resp
        data = _get_dashboard_payload()
        return jsonify(data.get("subagents", {}))

    return app


def _index_html(auth_token: Optional[str] = None) -> str:
    return f"""<!doctype html>
<html lang="en" data-bs-theme="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{APP_TITLE}</title>
  <style>
    :root {{
      --bg: #05070d;
      --bg2: #0f172a;
      --card: #0b1220;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --ok: #22c55e;
      --warn: #f59e0b;
      --bad: #f87171;
      --line: #1f2937;
      --accent: #60a5fa;
      --accent-soft: #111827;
      --passive: #f59f00;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, "PingFang SC", "Microsoft Yahei", sans-serif;
    }}
    header {{
      padding: 14px 24px;
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      background: rgba(5, 7, 13, 0.92);
      backdrop-filter: blur(8px);
      z-index: 10;
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 12px;
    }}
    h1 {{ margin: 0; font-size: 22px; font-weight: 700; justify-self: start; }}
    .wrap {{ padding: 14px 24px 28px; max-width: 1500px; margin: 0 auto; }}
    .nav {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0; justify-content: center; }}
    .header-actions {{ display:flex; align-items:center; gap:10px; justify-self:end; }}
    .lang-toggle {{ display:flex; gap:6px; }}
    .lang-btn {{ border:1px solid var(--line); background:var(--card); color:var(--muted); border-radius:999px; padding:6px 10px; font-size:12px; cursor:pointer; }}
    .lang-btn.active {{ color:var(--accent); border-color:var(--accent); background:var(--accent-soft); }}
    .speed-toggle {{ display:flex; gap:6px; }}
    .speed-btn {{ border:1px solid var(--line); background:var(--card); color:var(--muted); border-radius:999px; padding:6px 10px; font-size:12px; cursor:pointer; }}
    .speed-btn.active {{ color:var(--accent); border-color:var(--accent); background:var(--accent-soft); }}
    .speed-label {{ color:var(--muted); font-size:12px; align-self:center; }}
    .nav-tab {{ border: 1px solid var(--line); background: var(--card); color: var(--text); border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 13px; }}
    .nav-tab.active {{ border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }}
    .page {{ display: none; }}
    .page.active {{ display: block; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(180px,1fr)); gap: 12px; }}
    .compact-grid {{ grid-template-columns: repeat(5, minmax(150px, 1fr)); gap: 10px; }}
    .compact-grid .card {{ padding: 12px; }}
    .compact-grid .v {{ font-size: 22px; }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; }}
    .k {{ color: var(--muted); font-size: 12px; }}
    .v {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
    .v.sm {{ font-size: 18px; }}
    .ok {{ color: var(--ok); }} .warn {{ color: var(--warn); }} .bad {{ color: var(--bad); }} .muted {{ color: var(--muted); }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
    th, td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--line); font-size: 13px; vertical-align: top; }}
    th {{ color: var(--muted); font-weight: 600; position: sticky; top: 0; background: var(--card); }}
    .table-hover tbody tr:hover {{ background: rgba(96,165,250,.05); }}
    .align-middle td, .align-middle th {{ vertical-align: middle; }}
    .mb-0 {{ margin-bottom: 0; }}
    .me-auto {{ margin-right: auto; }}
    .panel {{ margin-top: 14px; background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 12px; }}
    .meta {{ color: var(--muted); font-size: 12px; margin-top: 10px; }}
    .pill {{ display:inline-block; border:1px solid var(--line); border-radius:999px; padding:2px 8px; font-size:11px; color:var(--muted); margin-left: 6px; background: var(--bg2); }}
    .monitor-grid {{ margin-top: 10px; display: grid; grid-template-columns: 1fr 2fr; gap: 12px; }}
    .monitor-box {{ border:1px solid var(--line); border-radius:10px; background:var(--card); padding:10px; min-height: 180px; }}
    .monitor-title {{ font-size:13px; color:var(--muted); margin-bottom:8px; }}
    .monitor-list-item {{ width: 100%; text-align: left; border: 1px solid var(--line); background: var(--bg2); color: var(--text); border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; cursor: pointer; }}
    .monitor-list-item.active {{ border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }}
    .monitor-content {{ white-space: pre-wrap; font-size:12px; line-height:1.5; max-height:300px; overflow:auto; color: var(--text); }}
    .btn-monitor {{ border:1px solid var(--line); background:var(--bg2); color:var(--text); border-radius:8px; padding:4px 10px; font-size:12px; cursor:pointer; }}
    .btn-monitor:hover {{ border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }}
    .model-cell {{ min-width: 110px; }}
    .model-status {{ color: var(--muted); font-size: 12px; }}
    .model-current {{ color: var(--muted); font-size: 12px; margin-bottom: 10px; }}
    .model-options {{ display: grid; gap: 8px; }}
    .model-option {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: var(--bg2); }}
    .model-option.active {{ border-color: var(--accent); background: var(--accent-soft); }}
    .memory-layout {{ display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr); gap: 14px; align-items: start; }}
    .memory-layout > .panel {{ overflow: hidden; }}
    .memory-layout > .panel table {{ table-layout: fixed; }}
    .memory-meta-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .kv-list {{ display: grid; gap: 10px; margin-top: 6px; }}
    .kv-row {{ display: flex; justify-content: space-between; gap: 12px; border-bottom: 1px solid var(--line); padding-bottom: 8px; }}
    .kv-row:last-child {{ border-bottom: 0; padding-bottom: 0; }}
    .kv-key {{ color: var(--muted); font-size: 12px; }}
    .kv-value {{ text-align: right; font-size: 13px; }}
    .memory-section-title {{ margin: 4px 0 8px; display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; }}
    .memory-list {{ display: grid; gap: 8px; }}
    .memory-list-item {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px; background: var(--bg2); }}
    .memory-list-item strong {{ display: block; margin-bottom: 4px; }}
    .memory-list-item .meta {{ margin-top: 4px; }}
    .memory-cap-grid {{ display:grid; gap:8px; }}
    .memory-cap-head {{ display:flex; align-items:center; justify-content:space-between; gap:8px; }}
    .memory-cap-title {{ font-size: 14px; font-weight: 600; }}
    .status-chip {{ display:inline-flex; align-items:center; gap:6px; border-radius:999px; padding:2px 8px; border:1px solid var(--line); font-size:11px; }}
    .status-chip.active, .status-chip.ok {{ color: var(--ok); border-color: rgba(34,197,94,.35); }}
    .status-chip.available, .status-chip.warn {{ color: var(--warn); border-color: rgba(245,158,11,.35); }}
    .status-chip.bad {{ color: var(--bad); border-color: rgba(248,113,113,.35); }}
    .status-chip.configured, .status-chip.muted {{ color: var(--muted); }}
    .daily-chart {{ display:flex; align-items:flex-end; justify-content:space-between; gap:10px; min-height:240px; padding: 10px 6px 0; overflow: hidden; }}
    .daily-item {{ flex: 1 1 0; min-width: 44px; max-width: 72px; text-align:center; }}
    .daily-bar-wrap {{ height: 160px; display:flex; align-items:flex-end; justify-content:center; }}
    .daily-bar-stack {{ width: 100%; max-width: 42px; border-radius: 8px 8px 0 0; overflow: hidden; display:flex; flex-direction: column-reverse; background: #0f172a; border: 1px solid var(--line); }}
    .daily-bar-active {{ background: #3b82f6; width: 100%; min-height: 0; }}
    .daily-bar-passive {{ background: var(--passive); width: 100%; min-height: 0; }}
    .daily-bar-passive.has-value {{ min-height: 3px; }}
    .daily-value {{ color: var(--muted); font-size: 10px; margin-bottom: 6px; white-space: nowrap; }}
    .daily-label {{ color: var(--muted); font-size: 10px; margin-top: 6px; white-space: nowrap; }}
    .daily-legend {{ display: flex; gap: 12px; align-items: center; margin-top: 8px; color: var(--muted); font-size: 12px; }}
    .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 4px; }}
    .daily-list {{ margin-top: 12px; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }}
    #flow-svg {{ width: 100%; height: 240px; border: 1px solid var(--line); border-radius: 8px; background: var(--card); }}
    #boot-overlay {{ display: none; }}
    .btn {{ border-radius:8px; padding:8px 12px; cursor:pointer; font-size:13px; }}
    .btn-secondary {{ background:var(--bg2); border:1px solid var(--line); color:var(--text); }}
    .btn-primary {{ background:var(--accent); border:1px solid var(--accent); color:#fff; }}
    .btn:disabled {{ opacity:.6; cursor:not-allowed; }}
    .btn-close {{ width:32px; height:32px; border:0; background:transparent; color:var(--text); cursor:pointer; position:relative; }}
    .btn-close::before, .btn-close::after {{ content:''; position:absolute; left:15px; top:7px; width:2px; height:18px; background:currentColor; }}
    .btn-close::before {{ transform:rotate(45deg); }}
    .btn-close::after {{ transform:rotate(-45deg); }}
    .form-check {{ display:flex; align-items:center; gap:8px; }}
    .form-check-input {{ margin:0; }}
    .modal {{ display:none; position:fixed; inset:0; z-index:1000; }}
    .modal.open {{ display:block; }}
    .modal-backdrop {{ position:absolute; inset:0; background:rgba(0,0,0,.55); }}
    .modal-dialog {{ position:relative; width:min(560px, calc(100vw - 24px)); margin:6vh auto; max-height:88vh; overflow:hidden; }}
    .modal-content {{ display:flex; flex-direction:column; max-height:88vh; border-radius:12px; overflow:hidden; }}
    .modal-header, .modal-footer {{ display:flex; align-items:center; gap:12px; padding:14px 16px; }}
    .modal-body {{ padding:14px 16px; overflow:auto; }}
    body.modal-open {{ overflow:hidden; }}
    @media (max-width: 1200px) {{ header {{ grid-template-columns: 1fr; gap: 10px; padding: 12px 16px; }} h1 {{ justify-self: center; font-size: 20px; }} .nav {{ justify-content: center; }} .header-actions {{ justify-self:center; }} }}
    @media (max-width: 1000px) {{ .grid {{ grid-template-columns: repeat(2,minmax(160px,1fr)); }} .compact-grid {{ grid-template-columns: repeat(3, minmax(140px, 1fr)); }} .monitor-grid {{ grid-template-columns: 1fr; }} .memory-layout {{ grid-template-columns: 1fr; }} .memory-meta-grid {{ grid-template-columns: 1fr; }} .wrap {{ padding: 12px 16px 24px; }} }}
    @media (max-width: 768px) {{ 
      header {{ padding: 10px 12px; position: relative; }} 
      h1 {{ font-size: 18px; }} 
      .nav {{ gap: 6px; }} 
      .nav-tab {{ padding: 6px 10px; font-size: 12px; }} 
      .header-actions {{ flex-wrap: wrap; justify-content: center; gap: 8px; }} 
      .speed-label {{ display: none; }} 
      .speed-btn {{ padding: 5px 8px; font-size: 11px; }} 
      .wrap {{ padding: 10px 12px 20px; }} 
      .grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }} 
      .compact-grid {{ grid-template-columns: repeat(2, 1fr); gap: 8px; }} 
      .compact-grid .card {{ padding: 10px; }} 
      .compact-grid .v {{ font-size: 18px; }} 
      .compact-grid .k {{ font-size: 11px; }} 
      .card {{ padding: 12px; }} 
      .v {{ font-size: 20px; }} 
      .panel {{ padding: 10px; }} 
      table {{ font-size: 12px; display: block; overflow-x: auto; white-space: nowrap; }} 
      th, td {{ padding: 8px 6px; }} 
      .monitor-box {{ min-height: 150px; }} 
      .monitor-list-item {{ padding: 6px 8px; font-size: 12px; }} 
      .monitor-content {{ font-size: 11px; max-height: 200px; }} 
      .modal-dialog {{ width: calc(100vw - 16px); margin: 4vh auto; max-height: 92vh; }} 
      .modal-header, .modal-footer {{ padding: 10px 12px; }} 
      .modal-body {{ padding: 10px 12px; }} 
      .daily-chart {{ min-height: 180px; gap: 6px; }} 
      .daily-item {{ min-width: 36px; max-width: 56px; }} 
      .daily-bar-wrap {{ height: 120px; }} 
      .daily-value {{ font-size: 9px; }} 
      .daily-label {{ font-size: 9px; }} 
      .daily-legend {{ font-size: 11px; gap: 8px; }} 
      .memory-list-item {{ padding: 8px; }} 
      .memory-cap-title {{ font-size: 13px; }} 
      .kv-key, .kv-value {{ font-size: 11px; }} 
      .model-option {{ padding: 8px; }} 
      .model-current {{ font-size: 11px; }} 
      .btn {{ padding: 6px 10px; font-size: 12px; }} 
    }}
    @media (max-width: 480px) {{ 
      header {{ padding: 8px 10px; }} 
      h1 {{ font-size: 16px; }} 
      .nav {{ gap: 4px; }} 
      .nav-tab {{ padding: 5px 8px; font-size: 11px; border-radius: 6px; }} 
      .lang-btn {{ padding: 5px 8px; font-size: 11px; }} 
      .speed-btn {{ padding: 4px 6px; font-size: 10px; }} 
      .wrap {{ padding: 8px 10px 16px; }} 
      .grid {{ grid-template-columns: 1fr; gap: 8px; }} 
      .compact-grid {{ grid-template-columns: repeat(2, 1fr); gap: 6px; }} 
      .compact-grid .card {{ padding: 8px; }} 
      .compact-grid .v {{ font-size: 16px; }} 
      .compact-grid .k {{ font-size: 10px; }} 
      .card {{ padding: 10px; }} 
      .v {{ font-size: 18px; }} 
      .v.sm {{ font-size: 14px; }} 
      .k {{ font-size: 11px; }} 
      .meta {{ font-size: 11px; }} 
      .panel {{ padding: 8px; margin-top: 10px; }} 
      .panel h3 {{ font-size: 14px; }} 
      th, td {{ padding: 6px 4px; font-size: 11px; }} 
      .pill {{ font-size: 10px; padding: 1px 6px; }} 
      .monitor-box {{ min-height: 120px; padding: 8px; }} 
      .monitor-title {{ font-size: 12px; }} 
      .daily-chart {{ min-height: 150px; padding: 6px 4px 0; gap: 4px; }} 
      .daily-item {{ min-width: 28px; max-width: 44px; }} 
      .daily-bar-wrap {{ height: 100px; }} 
      .daily-bar-stack {{ max-width: 32px; border-radius: 6px 6px 0 0; }} 
      .daily-value {{ font-size: 8px; margin-bottom: 4px; }} 
      .daily-label {{ font-size: 8px; margin-top: 4px; }} 
      .status-chip {{ font-size: 10px; padding: 1px 6px; }} 
      .memory-section-title {{ font-size: 13px; }} 
      .memory-list-item {{ padding: 6px; }} 
      .memory-cap-title {{ font-size: 12px; }} 
      .kv-key, .kv-value {{ font-size: 10px; }} 
      .btn-close {{ width: 28px; height: 28px; }} 
      .btn-close::before, .btn-close::after {{ left: 13px; top: 5px; height: 16px; }} 
    }}
    @media (max-width: 360px) {{ 
      .compact-grid {{ grid-template-columns: 1fr; }} 
      .nav-tab {{ padding: 4px 6px; font-size: 10px; }} 
      .daily-item {{ min-width: 24px; max-width: 36px; }} 
      .daily-bar-wrap {{ height: 80px; }} 
      .daily-bar-stack {{ max-width: 24px; }} 
    }}
    @media (hover: none) and (pointer: coarse) {{ 
      .nav-tab {{ padding: 10px 12px; }} 
      .nav-tab:active {{ transform: scale(0.98); }} 
      .card {{ -webkit-tap-highlight-color: transparent; }} 
      .speed-btn {{ padding: 8px 12px; }} 
      .lang-btn {{ padding: 8px 12px; }} 
      .monitor-list-item {{ padding: 10px; }} 
      .model-option {{ padding: 12px; }} 
    }}
  </style>
</head>
<body>
  <header>
    <h1>{APP_TITLE}</h1>
    <div class="nav">
      <button class="nav-tab active" data-page="overview" data-i18n="navOverview">Overview</button>
      <button class="nav-tab" data-page="flow" data-i18n="navFlow">Flow</button>
      <button class="nav-tab" data-page="crons" data-i18n="navCrons">Crons</button>
      <button class="nav-tab" data-page="usage" data-i18n="navTokens">Tokens</button>
      <button class="nav-tab" data-page="memory" data-i18n="navMemory">Memory</button>
    </div>
    <div class="header-actions">
      <span class="speed-label">Refresh</span>
      <div class="speed-toggle" aria-label="refresh speed">
        <button class="speed-btn" type="button" data-speed="fastest">Fastest</button>
        <button class="speed-btn" type="button" data-speed="fast">Fast</button>
        <button class="speed-btn active" type="button" data-speed="medium">Medium</button>
        <button class="speed-btn" type="button" data-speed="slow">Slow</button>
      </div>
    </div>
  </header>
  <div class="wrap">

    <section id="page-overview" class="page active">
      <div class="grid compact-grid" id="cards"></div>
      <div class="panel">
        <h3 style="margin:4px 0 8px">Agents <span class="pill">incl. Sub-Agents</span></h3>
        <table class="table table-hover align-middle mb-0">
          <thead><tr><th>Agent</th><th>Status</th><th>Sub-Agent</th><th>Sessions</th><th>Heartbeat</th><th>Current Model</th><th>Switch Model</th></tr></thead>
          <tbody id="agents-body"></tbody>
        </table>
      </div>
    </section>

    <section id="page-flow" class="page">
      <div class="panel">
        <h3 style="margin:4px 0 8px">Global Flow Diagram</h3>
        <svg id="flow-svg" viewBox="0 0 1200 240" xmlns="http://www.w3.org/2000/svg">
          <rect x="20" y="70" width="180" height="100" rx="10" fill="#0f172a" stroke="#334155" />
          <text x="42" y="125" fill="#e5e7eb" font-size="20">OpenClaw</text>
          <g><rect x="300" y="20" width="180" height="70" rx="10" fill="#0f172a" stroke="#334155"/><text x="340" y="63" fill="#e5e7eb" font-size="18">Agents</text></g>
          <g><rect x="300" y="150" width="180" height="70" rx="10" fill="#0f172a" stroke="#334155"/><text x="345" y="193" fill="#e5e7eb" font-size="18">Crons</text></g>
          <g><rect x="590" y="20" width="180" height="70" rx="10" fill="#0f172a" stroke="#334155"/><text x="622" y="63" fill="#e5e7eb" font-size="18">Models</text></g>
          <g><rect x="590" y="150" width="180" height="70" rx="10" fill="#0f172a" stroke="#334155"/><text x="624" y="193" fill="#e5e7eb" font-size="18">Usage</text></g>
          <path d="M200 120 L300 55" stroke="#64748b" stroke-width="2" fill="none" />
          <path d="M200 120 L300 185" stroke="#64748b" stroke-width="2" fill="none" />
          <path d="M480 55 L590 55" stroke="#64748b" stroke-width="2" fill="none" />
          <path d="M480 185 L590 185" stroke="#64748b" stroke-width="2" fill="none" />
        </svg>
      </div>
    </section>

    <section id="page-crons" class="page">
      <div class="panel">
        <h3 style="margin:4px 0 8px"><span data-i18n="cronsTitle">Cron Jobs</span></h3>
        <table class="table table-hover align-middle mb-0">
          <thead id="crons-head"></thead>
          <tbody id="crons-body"></tbody>
        </table>
      </div>
    </section>

    <section id="page-usage" class="page">
      <div class="panel">
        <h3 style="margin:4px 0 8px">Daily Token Consumption (Last 15 Days)</h3>
        <div id="daily-token-meta" class="meta">Loading…</div>
        <div class="daily-legend">
          <span><i class="legend-dot" style="background:#2563eb"></i>Active</span>
          <span><i class="legend-dot" style="background:#f59f00"></i>Passive</span>
        </div>
        <div id="daily-token-chart" class="meta">Loading…</div>
      </div>
      <div class="panel">
        <h3 style="margin:4px 0 8px">Model Token Consumption</h3>
        <div id="token-consumption-meta" class="meta">Loading…</div>
        <table class="table table-hover align-middle mb-0">
          <thead><tr><th>Model</th><th>Provider</th><th>Sessions</th><th>Total</th><th>Active</th><th>Passive</th><th>Input(net/gross)</th><th>Output</th><th>Cache(R/W)</th></tr></thead>
          <tbody id="models-body"></tbody>
        </table>
      </div>
    </section>

    <section id="page-memory" class="page">
      <div class="grid" id="memory-cards"></div>
      <div class="memory-layout">
        <div class="panel">
          <div class="memory-section-title">
            <h3 style="margin:0" data-i18n="memoryWorkspaceTitle">Memory Workspaces</h3>

          </div>
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Workspace</th><th>Entries</th><th>Today</th><th>Latest File</th><th>Updated</th></tr></thead>
            <tbody id="memory-workspaces-body"></tbody>
          </table>
        </div>
        <div class="memory-meta-grid">
          <div class="panel">
            <h3 style="margin:4px 0 8px" data-i18n="memoryCapabilitiesTitle">Memory Capabilities</h3>
            <div id="memory-capabilities" class="memory-cap-grid">Loading…</div>
          </div>
          <div class="panel">
            <h3 style="margin:4px 0 8px" data-i18n="memoryStorageTitle">Central Memory & Storage</h3>
            <div id="memory-storage-summary" class="kv-list">Loading…</div>
          </div>
          <div class="panel">
            <h3 style="margin:4px 0 8px" data-i18n="memoryAutomationTitle">Memory Automation</h3>
            <div id="memory-automation" class="memory-list">Loading…</div>
          </div>
          <div class="panel" style="grid-column: 1 / -1;">
            <h3 style="margin:4px 0 8px" data-i18n="memoryImpactTitle">Memory Impact from self-improve / involve</h3>
            <div id="memory-impact" class="memory-list">Loading…</div>
          </div>
        </div>
      </div>
      <div class="panel">
        <h3 style="margin:4px 0 8px" data-i18n="memoryRecentTitle">Recent Memory Files</h3>
        <table class="table table-hover align-middle mb-0">
          <thead><tr><th>Workspace</th><th>File</th><th>Size</th><th>Updated</th></tr></thead>
          <tbody id="memory-recent-body"></tbody>
        </table>
      </div>
    </section>
  </div>

  <div class="modal" id="model-switch-modal" tabindex="-1" aria-hidden="true">
    <div class="modal-backdrop" data-modal-close="true"></div>
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content" style="background:var(--card);color:var(--text);border:1px solid var(--line);">
        <div class="modal-header" style="border-bottom:1px solid var(--line);">
          <div>
            <h5 class="modal-title" id="model-switch-title" style="margin:0">Switch Model</h5>
            <div class="model-current" id="model-switch-current">Current model: -</div>
          </div>
          <button type="button" class="btn-close" data-modal-close="true" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div id="model-switch-options" class="model-options"></div>
        </div>
        <div class="modal-footer" style="border-top:1px solid var(--line);">
          <span class="model-status me-auto" id="model-switch-status"></span>
          <button type="button" class="btn btn-secondary" data-modal-close="true" id="model-switch-cancel">Cancel</button>
          <button type="button" class="btn btn-primary" id="model-switch-save">Save</button>
        </div>
      </div>
    </div>
  </div>
  <script>
    const SERVER_TOKEN = '{(auth_token or "").replace(chr(92), chr(92)*2).replace(chr(39), chr(92)+chr(39))}';
    const $ = (s) => document.querySelector(s);
    const fmtNum = (n) => (n ?? 0).toLocaleString();
    const escapeHtml = (value) => String(value ?? '').replace(/[&<>\"']/g, (ch) => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', \"'\": '&#39;' }})[ch] || ch);
    const fmtM = (n) => {{
      const v = Number(n || 0) / 1_000_000;
      if (v >= 100) return v.toFixed(0) + 'M';
      if (v >= 10) return v.toFixed(1) + 'M';
      return v.toFixed(2) + 'M';
    }};
    const fmtTime = (ms) => {{
      if (!ms) return '-';
      const d = new Date(ms);
      return d.toLocaleString();
    }};
    const fmtLag = (ms) => {{
      const v = Number(ms || 0);
      if (!Number.isFinite(v) || v < 0) return '-';
      if (v < 1000) return Math.round(v) + 'ms';
      const s = v / 1000;
      if (s < 60) return s.toFixed(1) + 's';
      const m = Math.floor(s / 60);
      const rs = Math.round(s % 60);
      return `${{m}}m${{rs}}s`;
    }};
    const I18N = {{
      title: '{APP_TITLE}',
      navOverview: 'Overview',
      navFlow: 'Flow',
      navCrons: 'Crons',
      navTokens: 'Tokens',
      navMemory: 'Memory',
      cronsTitle: 'Cron Jobs',
      memoryWorkspaceTitle: 'Memory Workspaces',
      memoryCapabilitiesTitle: 'Memory Capabilities',
      memoryStorageTitle: 'Central Memory & Storage',
      memoryAutomationTitle: 'Memory Automation',
      memoryImpactTitle: 'Memory Impact from self-improve / involve',
      memoryRecentTitle: 'Recent Memory Files',
      loading: 'Loading…',
      noData: 'No data',
      noTasks: 'No jobs',
      autoRefresh: 'Auto-refreshed status',
      runningNow: 'Running',
      idle: 'Stopped',
      on: 'On',
      off: 'Off',
      yes: 'Yes',
      save: 'Save',
      cancel: 'Cancel',
      switchModel: 'Switch Model',
      currentModel: 'Current model',
      chooseModel: 'Choose a model',
      saving: 'Saving...',
      saveFailed: 'Save failed',
      restarting: 'Restarting OpenClaw…',
      restartFailed: 'Model saved, but OpenClaw restart failed',
      noValidModels: 'No valid models are available.',
      schedule: 'Schedule',
      enabled: 'Enabled',
      running: 'Running',
      lastStatus: 'Last Status',
      lastDuration: 'Last Duration',
      task: 'Job',
      agent: 'Agent',
      model: 'Current Model',
      switchModelBtn: 'Switch Model',
      triggerRun: 'Run',
      triggering: 'Running...',
      triggered: 'Triggered',
      triggerFailed: 'Trigger failed',
      deleteCron: 'Delete',
      deleting: 'Deleting...',
      deleted: 'Deleted',
      deleteFailed: 'Delete failed',
      confirmDelete: 'Are you sure you want to delete this job?',
      workspace: 'Workspace',
      entries: 'Entries',
      todayAdded: 'Today',
      latestFile: 'Latest File',
      updatedAt: 'Updated',
      file: 'File',
      size: 'Size',
      capabilitySource: 'Source',
      capabilityStatus: 'Status',
      automationEffect: 'Effect',

    }};
    const currentLang = 'en';

    function t(key) {{
      return I18N[key] || key;
    }}


    function statusText(status, tone) {{
      return `<span class="${{tone || 'muted'}}">${{escapeHtml(status || '-')}}</span>`;
    }}

    const modalController = {{
      show() {{
        const modalEl = document.getElementById('model-switch-modal');
        if (!modalEl) return;
        modalEl.classList.add('open');
        document.body.classList.add('modal-open');
      }},
      hide() {{
        const modalEl = document.getElementById('model-switch-modal');
        if (!modalEl) return;
        modalEl.classList.remove('open');
        document.body.classList.remove('modal-open');
        const statusEl = $('#model-switch-status');
        if (statusEl) statusEl.textContent = '';
      }},
    }};

    function stateBadge(v) {{
      const s = String(v ?? '').toLowerCase();
      if (v === true || s === 'true' || s === 'running' || s === 'healthy' || s === 'online') return '<span class="ok">●</span>';
      if (s === 'restarting' || s.includes('restart') || s.includes('starting') || s.includes('activating')) return '<span class="warn">●</span>';
      return '<span class="bad">●</span>';
    }}

    function token() {{
      return SERVER_TOKEN || localStorage.getItem('clawstatus-token') || '';
    }}

    async function fetchJson(url, headers) {{
      const r = await fetch(url, {{ headers }});
      if (!r.ok) throw new Error(url + ' -> HTTP ' + r.status);
      return r.json();
    }}

    async function postJson(url, body, headers) {{
      const r = await fetch(url, {{
        method: 'POST',
        headers: Object.assign({{ 'Content-Type': 'application/json' }}, headers || {{}}),
        body: JSON.stringify(body || {{}}),
      }});
      const data = await r.json().catch(() => ({{}}));
      if (!r.ok) throw new Error((data && data.error) ? data.error : (url + ' -> HTTP ' + r.status));
      return data;
    }}

    const dashboardState = {{
      generatedAt: Date.now(),
      sourceTimestamps: {{}},
      sourceLagsMs: {{}},
      overview: {{}},
      agents: {{}},
      crons: {{}},
      openclaw: {{}},
      models: {{}},
      memory: {{}},
    }};

    const DASH_SNAPSHOT_KEY = 'clawstatus-dashboard-snapshot-v2';
    const VALID_PAGES = new Set(['overview', 'flow', 'crons', 'usage', 'memory']);
    let activePage = 'overview';

    // Auto-refresh config - optimized for low resource usage
    const refreshState = {{
      overview: {{ url: '/api/overview', interval: 30, next: 0, page: 'overview' }},     // 30s - core overview
      openclaw: {{ url: '/api/openclaw', interval: 60, next: 0, page: 'overview' }},     // 60s - service status
      agents: {{ url: '/api/agents', interval: 15, next: 0, page: 'overview' }},         // 15s - Agent status
      crons: {{ url: '/api/crons', interval: 30, next: 0, page: 'crons' }},              // 30s - Cron tasks
      models: {{ url: '/api/models', interval: 120, next: 0, page: 'usage' }},           // 120s - model stats
      memory: {{ url: '/api/memory', interval: 120, next: 0, page: 'memory' }},          // 120s - memory data
    }};

    // Refresh speed tiers (multiplier on base interval)
    const SPEED_KEY = 'clawstatus-speed';
    const SPEED_MULT = {{ fastest: 0.3, fast: 0.6, medium: 1, slow: 2 }};
    let currentSpeed = localStorage.getItem(SPEED_KEY) || 'medium';
    if (!SPEED_MULT[currentSpeed]) currentSpeed = 'medium';

    function applySpeed(speed) {{
      currentSpeed = SPEED_MULT[speed] ? speed : 'medium';
      localStorage.setItem(SPEED_KEY, currentSpeed);
      const mult = SPEED_MULT[currentSpeed];
      Object.keys(refreshState).forEach(key => {{
        if (refreshState[key]) {{
          const base = refreshState[key].interval;
          refreshState[key]._interval = Math.max(2, Math.round(base * mult));
        }}
      }});
      document.querySelectorAll('.speed-btn').forEach(btn => {{
        btn.classList.toggle('active', btn.getAttribute('data-speed') === currentSpeed);
      }});
    }}

    document.querySelectorAll('.speed-btn').forEach(btn => {{
      btn.addEventListener('click', () => applySpeed(btn.getAttribute('data-speed')));
    }});
    applySpeed(currentSpeed);

    const refreshingKeys = new Set();
    let selectedCronId = null;
    const cronMap = new Map();
    const cronMonitorCache = new Map();
    const modelModalState = {{
      kind: '',
      entityId: '',
      currentModel: '',
      models: [],
    }};

    function saveSnapshot() {{
      try {{
        localStorage.setItem(DASH_SNAPSHOT_KEY, JSON.stringify({{
          ts: Date.now(),
          data: dashboardState,
        }}));
      }} catch (e) {{}}
    }}

    function loadSnapshot() {{
      try {{
        const raw = localStorage.getItem(DASH_SNAPSHOT_KEY);
        if (!raw) return false;
        const obj = JSON.parse(raw);
        if (!obj || !obj.data) return false;
        Object.assign(dashboardState, obj.data);
        dashboardState.generatedAt = Date.now();
        return true;
      }} catch (e) {{
        return false;
      }}
    }}

    function keysForPage(page) {{
      if (page === 'overview') return ['overview', 'openclaw', 'agents'];
      if (page === 'crons') return ['crons'];
      if (page === 'usage') return ['models'];
      if (page === 'memory') return ['memory'];
      return [];
    }}

    async function refreshOne(key, force = false) {{
      const conf = refreshState[key];
      if (!conf) return;
      if (refreshingKeys.has(key)) return;
      
      const now = Date.now();
      const interval = conf._interval || conf.interval;
      if (!force && now < conf.next) return;

      const headers = {{}};
      if (token()) headers['Authorization'] = 'Bearer ' + token();

      refreshingKeys.add(key);
      try {{
        const data = await fetchJson(conf.url, headers);
        dashboardState[key] = data;

        if (data && typeof data === 'object') {{
          if (data._sourceLagsMs && typeof data._sourceLagsMs === 'object') {{
            dashboardState.sourceLagsMs = data._sourceLagsMs;
          }}
          if (data._sourceTimestamps && typeof data._sourceTimestamps === 'object') {{
            dashboardState.sourceTimestamps = data._sourceTimestamps;
          }}
        }}

        dashboardState.generatedAt = Date.now();
        const interval = conf._interval || conf.interval;
        conf.next = Date.now() + interval * 1000;
        render(dashboardState);
        saveSnapshot();
      }} catch (e) {{
        console.warn(`refresh failed: ${{key}}`, e);
      }} finally {{
        refreshingKeys.delete(key);
      }}
    }}

    function refreshForPage(page, force = false) {{
      const keys = keysForPage(page);
      keys.forEach((key, idx) => setTimeout(() => refreshOne(key, force), idx * 120));
    }}

    function normalizePage(page) {{
      const p = String(page || '').trim().toLowerCase();
      return VALID_PAGES.has(p) ? p : 'overview';
    }}

    function pageFromUrl() {{
      try {{
        const u = new URL(window.location.href);
        const qp = normalizePage(u.searchParams.get('page'));
        if (qp !== 'overview') return qp;
        const hp = normalizePage((u.hash || '').replace(/^#/, ''));
        return hp;
      }} catch (e) {{
        return 'overview';
      }}
    }}

    function syncUrlForPage(page, {{ replace = true }} = {{}}) {{
      const p = normalizePage(page);
      try {{
        const u = new URL(window.location.href);
        const curr = normalizePage(u.searchParams.get('page'));
        if (curr === p && !u.hash) return;
        u.searchParams.set('page', p);
        u.hash = '';
        const next = `${{u.pathname}}?${{u.searchParams.toString()}}`;
        if (replace) history.replaceState({{ page: p }}, '', next);
        else history.pushState({{ page: p }}, '', next);
      }} catch (e) {{}}
    }}

    function setActivePage(page, {{ forceRefresh = false, replaceUrl = true }} = {{}}) {{
      const p = normalizePage(page);
      activePage = p;

      document.querySelectorAll('.nav-tab').forEach(x => {{
        const xp = normalizePage(x.getAttribute('data-page'));
        x.classList.toggle('active', xp === p);
      }});

      document.querySelectorAll('.page').forEach(x => x.classList.remove('active'));
      const pageEl = document.getElementById('page-' + p);
      if (pageEl) pageEl.classList.add('active');

      syncUrlForPage(p, {{ replace: replaceUrl }});
      refreshForPage(p, forceRefresh);
    }}

    function bootstrapRefresh() {{
      const hasSnap = loadSnapshot();
      if (hasSnap) render(dashboardState);

      const initialPage = pageFromUrl();
      setActivePage(initialPage, {{ forceRefresh: true, replaceUrl: true }});

      // Other page data loaded on demand (triggered on tab switch)
    }}

    function render(d) {{

      const ov = d.overview || {{}};
      const o = d.openclaw || {{}};
      const ocState = String(o.state || '').toLowerCase();
      const ocColor = (ocState === 'online') ? 'ok' : (ocState === 'restarting' ? 'warn' : 'bad');
      const cards = [
        ['OpenClaw', `<span class="${{ocColor}}">${{o.state || '-'}}</span>`, t('autoRefresh')],
        ['Agents', ov.agentCount, `${{t('runningNow')}} ${{fmtNum(ov.runningAgents)}}`],
        ['Sub-Agents', ov.subagentCount, `${{t('runningNow')}} ${{fmtNum(ov.runningSubagents)}}`],
        ['Crons', ov.cronCount, `${{t('runningNow')}} ${{fmtNum(ov.runningCrons)}}`],
        ['Models', ov.modelCount, `Tokens ${{fmtNum(ov.tokens)}}`],
      ];
      $('#cards').innerHTML = cards.map(([k,v,s]) => `
        <div class="card">
          <div class="k">${{k}}</div>
          <div class="v ${{typeof v === 'number' ? '' : 'sm'}}">${{typeof v === 'number' ? fmtNum(v) : v}}</div>
          <div class="meta">${{s}}</div>
        </div>
      `).join('');

      const agents = (d.agents || {{}}).agents || [];
      const agentModels = (d.agents || {{}}).availableModels || [];
      $('#agents-body').innerHTML = agents.map(a => `
        <tr>
          <td>${{a.id}}</td>
          <td>${{stateBadge(a.running)}} ${{a.running ? t('runningNow') : t('idle')}}</td>
          <td>${{a.subagentsRunning}} / ${{a.subagentsTotal}}</td>
          <td>${{fmtNum(a.sessionsCount)}}</td>
          <td>${{a.heartbeatEnabled ? (t('on') + ' (' + (a.heartbeatEvery || '-') + ')') : t('off')}}</td>
          <td>${{escapeHtml(a.currentModel || '-')}}</td>
          <td class="model-cell">${{renderModelSwitchButton('agent', a.id, a.currentModel, agentModels)}}</td>
        </tr>
      `).join('') || '<tr><td colspan="7" class="meta">' + t('noData') + '</td></tr>';
      bindModelSwitchButtons('agent');

      renderCronTable(d.crons || {{}});

      const daily = (d.models || {{}}).dailyTokens || [];
      renderDailyChart(daily);

      const modelsData = d.models || {{}};
      const models = (modelsData.models || []).filter(m => Number(m.tokens || 0) > 0);
      const metaEl = $('#token-consumption-meta');
      if (metaEl) {{
        metaEl.textContent = `${{modelsData.formula || 'Actual tokens = net input + output; net input = max(0, input - cache reuse)'}} | ${{t('runningNow')}} ${{fmtNum(modelsData.activeTokens || 0)}} (${{fmtNum(modelsData.activeSessions || 0)}} sessions) | Passive ${{fmtNum(modelsData.passiveTokens || 0)}} (${{fmtNum(modelsData.passiveSessions || 0)}} sessions)`;
      }}

      $('#models-body').innerHTML = models.map(m => `
        <tr>
          <td>${{m.model}}</td>
          <td>${{m.provider || '-'}}</td>
          <td>${{fmtNum(m.sessions)}}</td>
          <td>${{fmtNum(m.tokens)}}</td>
          <td>${{fmtNum(m.activeTokens || 0)}}</td>
          <td>${{fmtNum(m.passiveTokens || 0)}}</td>
          <td>${{fmtNum(m.inputTokens)}} <span class="meta">/ ${{fmtNum(m.rawInputTokens || m.inputTokens)}}</span></td>
          <td>${{fmtNum(m.outputTokens)}}</td>
          <td>${{fmtNum(m.cacheRead)}} / ${{fmtNum(m.cacheWrite)}}</td>
        </tr>
      `).join('') || '<tr><td colspan="9" class="meta">' + t('noData') + '</td></tr>';

      renderMemory(d.memory || {{}});
    }}

    function renderCronTable(data) {{
      const crons = (data || {{}}).jobs || [];
      const cronModels = (data || {{}}).availableModels || [];
      cronMap.clear();
      crons.forEach(c => cronMap.set(c.id, c));
      // hide disabled cron jobs
      const visibleCrons = crons.filter(c => c.enabled !== false);

      const head = $('#crons-head');
      if (head) {{
        head.innerHTML = `
          <tr>
            <th>${{t('task')}}</th>
            <th>${{t('schedule')}}</th>
            <th>${{t('running')}}</th>
            <th>${{t('model')}}</th>
            <th>${{t('lastStatus')}}</th>
            <th>${{t('lastDuration')}}</th>
            <th>${{t('switchModelBtn')}}</th>
            <th>${{t('triggerRun')}}</th>
            <th>${{t('deleteCron')}}</th>
          </tr>
        `;
      }}

      const cronsBody = $('#crons-body');
      const colspan = 9;
      cronsBody.innerHTML = visibleCrons.map(c => `
        <tr>
          <td>${{escapeHtml(c.name || c.id || '-')}}</td>
          <td>${{escapeHtml(c.scheduleText || '-')}}</td>
          <td>${{c.running ? `<span class="ok">${{t('runningNow')}}</span>` : '<span class="muted">-</span>'}}</td>
          <td>${{escapeHtml(c.currentModel || '-')}}</td>
          <td>${{statusText(c.lastStatus || '-', c.lastStatusTone)}}</td>
          <td>${{c.lastDurationMs ? Math.round(c.lastDurationMs/1000)+'s' : '-'}}</td>
          <td class="model-cell">${{renderModelSwitchButton('cron', c.id, c.currentModel, cronModels)}}</td>
          <td><button class="btn-monitor btn-cron-run" data-cron-id="${{escapeHtml(c.id)}}">${{t('triggerRun')}}</button></td>
          <td><button class="btn-monitor btn-cron-delete" data-cron-id="${{escapeHtml(c.id)}}" data-cron-name="${{escapeHtml(c.name || c.id || '')}}">${{t('deleteCron')}}</button></td>
        </tr>
      `).join('') || `<tr><td colspan="${{colspan}}" class="meta">${{t('noTasks')}}</td></tr>`;
      bindModelSwitchButtons('cron');
      bindCronRunButtons();
      bindCronDeleteButtons();
    }}

    function bindCronRunButtons() {{
      document.querySelectorAll('.btn-cron-run').forEach(btn => {{
        btn.addEventListener('click', async () => {{
          const jobId = btn.getAttribute('data-cron-id');
          btn.disabled = true;
          btn.textContent = t('triggering');
          btn.style.color = 'var(--warn)';
          const hdrs = {{}};
          if (token()) hdrs['Authorization'] = 'Bearer ' + token();
          try {{
            const result = await postJson(`/api/crons/${{encodeURIComponent(jobId)}}/run`, {{}}, hdrs);
            if (result && result.triggered) {{
              btn.textContent = '✓ ' + t('triggered');
              btn.style.color = 'var(--ok)';
              setTimeout(() => refreshOne('crons', true), 3000);
            }} else {{
              btn.textContent = t('triggerFailed');
              btn.style.color = 'var(--bad)';
            }}
          }} catch (e) {{
            btn.textContent = t('triggerFailed');
            btn.style.color = 'var(--bad)';
          }}
          setTimeout(() => {{
            btn.disabled = false;
            btn.textContent = t('triggerRun');
            btn.style.color = '';
          }}, 5000);
        }});
      }});
    }}

    function bindCronDeleteButtons() {{
      document.querySelectorAll('.btn-cron-delete').forEach(btn => {{
        btn.addEventListener('click', async () => {{
          const jobId = btn.getAttribute('data-cron-id');
          const jobName = btn.getAttribute('data-cron-name') || jobId;
          
          // Confirm dialog
          if (!confirm(`${{t('confirmDelete')}}\n\n${{jobName}}`)) {{
            return;
          }}
          
          btn.disabled = true;
          btn.textContent = t('deleting');
          btn.style.color = 'var(--warn)';
          
          const hdrs = {{}};
          if (token()) hdrs['Authorization'] = 'Bearer ' + token();
          
          try {{
            const result = await postJson(`/api/crons/${{encodeURIComponent(jobId)}}/delete`, {{}}, hdrs);
            if (result && result.deleted) {{
              btn.textContent = '✓ ' + t('deleted');
              btn.style.color = 'var(--ok)';
              // Refresh list immediately
              setTimeout(() => refreshOne('crons', true), 1000);
            }} else {{
              btn.textContent = t('deleteFailed');
              btn.style.color = 'var(--bad)';
            }}
          }} catch (e) {{
            btn.textContent = t('deleteFailed');
            btn.style.color = 'var(--bad)';
          }}
          
          setTimeout(() => {{
            btn.disabled = false;
            btn.textContent = t('deleteCron');
            btn.style.color = '';
          }}, 5000);
        }});
      }});
    }}

    function renderCronMonitorList(crons) {{
      const listEl = $('#cron-monitor-list');
      const detailTitle = $('#cron-monitor-detail-title');
      const detailEl = $('#cron-monitor-detail');
      if (!listEl) return;
      if (!crons || !crons.length) {{
        listEl.innerHTML = '<div class="meta">No jobs</div>';
        if (detailTitle) detailTitle.textContent = 'Run Details';
        if (detailEl) detailEl.textContent = 'No jobs to monitor.';
        return;
      }}
      listEl.innerHTML = (crons || []).map(c => `
        <button class="monitor-list-item ${{selectedCronId === c.id ? 'active' : ''}}" data-cron-id="${{c.id}}">
          <div><strong>${{c.name}}</strong></div>
          <div class="meta">${{c.scheduleText || '-'}} · ${{c.running ? 'Running' : (c.enabled ? 'Waiting' : 'Disabled')}}</div>
        </button>
      `).join('') || '<div class="meta">No jobs</div>';

      listEl.querySelectorAll('.monitor-list-item').forEach(btn => {{
        btn.addEventListener('click', () => showCronMonitor(btn.getAttribute('data-cron-id')));
      }});
    }}

    async function showCronMonitor(id) {{
      const c = id ? cronMap.get(id) : null;
      const detailTitle = $('#cron-monitor-detail-title');
      const detailEl = $('#cron-monitor-detail');
      if (!c || !detailEl) return;
      selectedCronId = id;
      renderCronMonitorList(Array.from(cronMap.values()));

      if (detailTitle) detailTitle.textContent = `Run Details · ${{c.name}} (${{c.scheduleText || '-'}})`;

      if (cronMonitorCache.has(id)) {{
        detailEl.textContent = cronMonitorCache.get(id);
        return;
      }}

      detailEl.textContent = 'Loading monitor data...';
      try {{
        const headers = {{}};
        if (token()) headers['Authorization'] = 'Bearer ' + token();
        const data = await fetchJson(`/api/cron-monitor/${{encodeURIComponent(id)}}`, headers);
        const txt = (data && data.monitorText) ? data.monitorText : 'No monitor content available for this job.';
        cronMonitorCache.set(id, txt);
        if (selectedCronId === id) detailEl.textContent = txt;
      }} catch (e) {{
        detailEl.textContent = 'Failed to load monitor data. Please try again.';
      }}
    }}

    function modelOptionLabel(row) {{
      const id = String((row && row.id) || '').trim();
      const label = String((row && row.name) || id).trim() || id;
      const provider = String((row && row.provider) || '').trim();
      if (provider) return `${{label}} · ${{provider}}`;
      return label || id;
    }}

    function renderModelSwitchButton(kind, entityId, currentModel, models) {{
      const encodedModels = encodeURIComponent(JSON.stringify(Array.isArray(models) ? models : []));
      return `<button class="btn-monitor btn-model-switch" data-kind="${{escapeHtml(kind)}}" data-id="${{escapeHtml(entityId)}}" data-current-model="${{escapeHtml(currentModel || '')}}" data-models="${{encodedModels}}">${{t('switchModelBtn')}}</button>`;
    }}

    function openModelSwitchModal(kind, entityId, currentModel, models) {{
      const titleEl = $('#model-switch-title');
      const currentEl = $('#model-switch-current');
      const optionsEl = $('#model-switch-options');
      const statusEl = $('#model-switch-status');
      const validModels = [];
      const seen = new Set();

      (Array.isArray(models) ? models : []).forEach((row) => {{
        const id = String((row && row.id) || '').trim();
        if (!id || seen.has(id)) return;
        seen.add(id);
        validModels.push(row);
      }});

      modelModalState.kind = kind;
      modelModalState.entityId = entityId;
      modelModalState.currentModel = String(currentModel || '').trim();
      modelModalState.models = validModels;

      if (titleEl) titleEl.textContent = `${{t('switchModel')}} · ${{kind === 'agent' ? 'Agent' : 'Cron'}}`;
      if (currentEl) currentEl.textContent = `${{t('currentModel')}}：${{modelModalState.currentModel || '-'}}`;
      if (statusEl) statusEl.textContent = '';

      if (optionsEl) {{
        if (!validModels.length) {{
          optionsEl.innerHTML = `<div class="meta">${{t('noValidModels')}}</div>`;
        }} else {{
          optionsEl.innerHTML = validModels.map((row, idx) => {{
            const id = String((row && row.id) || '').trim();
            const inputId = `model-switch-option-${{idx}}`;
            const checked = id === modelModalState.currentModel ? 'checked' : '';
            const active = checked ? 'active' : '';
            return `
              <label class="model-option ${{active}}" for="${{inputId}}">
                <div class="form-check mb-0">
                  <input class="form-check-input" type="radio" name="model-switch-option" id="${{inputId}}" value="${{escapeHtml(id)}}" ${{checked}}>
                  <span class="form-check-label">${{escapeHtml(modelOptionLabel(row))}}</span>
                </div>
                <div class="meta">${{escapeHtml(id)}}</div>
              </label>
            `;
          }}).join('');
          optionsEl.querySelectorAll('input[name="model-switch-option"]').forEach((input) => {{
            input.addEventListener('change', () => {{
              optionsEl.querySelectorAll('.model-option').forEach((el) => el.classList.remove('active'));
              const wrapper = input.closest('.model-option');
              if (wrapper) wrapper.classList.add('active');
            }});
          }});
        }}
      }}

      modalController.show();
    }}

    function bindModelSwitchButtons(kind) {{
      document.querySelectorAll(`.btn-model-switch[data-kind="${{kind}}"]`).forEach((btn) => {{
        btn.onclick = () => {{
          let models = [];
          try {{
            models = JSON.parse(decodeURIComponent(btn.getAttribute('data-models') || '[]'));
          }} catch (e) {{}}
          openModelSwitchModal(
            btn.getAttribute('data-kind') || kind,
            btn.getAttribute('data-id') || '',
            btn.getAttribute('data-current-model') || '',
            models,
          );
        }};
      }});
    }}

    function bindModelSwitchModal() {{
      const modalEl = document.getElementById('model-switch-modal');
      const saveBtn = $('#model-switch-save');
      const statusEl = $('#model-switch-status');
      const optionsEl = $('#model-switch-options');
      if (!modalEl || !saveBtn || !statusEl || !optionsEl) return;

      modalEl.querySelectorAll('[data-modal-close="true"]').forEach((el) => {{
        el.addEventListener('click', () => modalController.hide());
      }});
      document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape' && modalEl.classList.contains('open')) modalController.hide();
      }});

      saveBtn.onclick = async () => {{
        const selected = optionsEl.querySelector('input[name="model-switch-option"]:checked');
        if (!selected) {{
          statusEl.textContent = t('chooseModel');
          return;
        }}

        const model = String(selected.value || '').trim();
        if (!model) {{
          statusEl.textContent = t('chooseModel');
          return;
        }}

        const headers = {{}};
        if (token()) headers['Authorization'] = 'Bearer ' + token();
        saveBtn.disabled = true;
        statusEl.textContent = t('saving');

        try {{
          const url = modelModalState.kind === 'agent'
            ? `/api/agents/${{encodeURIComponent(modelModalState.entityId)}}/model`
            : `/api/crons/${{encodeURIComponent(modelModalState.entityId)}}/model`;
          const result = await postJson(url, {{ model }}, headers);
          if (result && result.restartTriggered) {{
            statusEl.textContent = '✓ ' + t('restarting');
            statusEl.style.color = 'var(--ok)';
          }} else {{
            statusEl.textContent = t('restartFailed');
            statusEl.style.color = 'var(--warn)';
          }}
          if (modelModalState.kind === 'agent') {{
            refreshOne('agents', true);
          }} else {{
            refreshOne('crons', true);
          }}
          setTimeout(() => {{ modalController.hide(); statusEl.style.color = ''; }}, 3000);
        }} catch (e) {{
          statusEl.textContent = `${{t('saveFailed')}}: ` + (e.message || e);
          console.warn('model switch failed', e);
        }} finally {{
          saveBtn.disabled = false;
        }}
      }};
    }}

    function fmtBytes(n) {{
      const v = Number(n || 0);
      if (v < 1024) return v + ' B';
      if (v < 1024 * 1024) return (v / 1024).toFixed(1) + ' KB';
      if (v < 1024 * 1024 * 1024) return (v / 1024 / 1024).toFixed(1) + ' MB';
      return (v / 1024 / 1024 / 1024).toFixed(2) + ' GB';
    }}

    function renderMemory(m) {{
      const s = m.summary || {{}};
      const c = m.central || {{}};
      const st = m.storage || {{}};
      const capabilities = m.capabilities || [];

      const cards = [
        ['Workspaces', s.workspaceCount || 0, `Entries ${{fmtNum(s.totalEntries || 0)}}`],
        ['Today', s.todayEntries || 0, `Recent files ${{fmtNum(s.recentCount || 0)}}`],
        ['Central topics', c.topicsCount || 0, `memories-md ${{fmtNum(c.memoriesMdCount || 0)}}`],
        ['Capabilities', capabilities.length || 0, `SQLite ${{fmtBytes(st.sqliteBytes || 0)}}`],
      ];
      const cardsEl = $('#memory-cards');
      if (cardsEl) {{
        cardsEl.innerHTML = cards.map(([k,v,meta]) => `
          <div class="card">
            <div class="k">${{k}}</div>
            <div class="v">${{fmtNum(v)}}</div>
            <div class="meta">${{meta}}</div>
          </div>
        `).join('');
      }}

      const wsRows = m.workspaces || [];
      $('#memory-workspaces-body').innerHTML = wsRows.map(w => `
        <tr>
          <td>${{w.workspace}}</td>
          <td>${{fmtNum(w.entries)}}</td>
          <td>${{fmtNum(w.todayEntries)}}</td>
          <td>${{w.latestFile || '-'}}</td>
          <td>${{fmtTime(w.latestAt)}}</td>
        </tr>
      `).join('') || '<tr><td colspan="5" class="meta">' + t('noData') + '</td></tr>';

      const recRows = m.recent || [];
      $('#memory-recent-body').innerHTML = recRows.map(r => `
        <tr>
          <td>${{r.workspace}}</td>
          <td>${{r.file}}</td>
          <td>${{fmtBytes(r.size)}}</td>
          <td>${{fmtTime(r.updatedAt)}}</td>
        </tr>
      `).join('') || '<tr><td colspan="4" class="meta">' + t('noData') + '</td></tr>';

      const capEl = $('#memory-capabilities');
      if (capEl) {{
        capEl.innerHTML = capabilities.map((cap) => `
          <div class="memory-list-item">
            <div class="memory-cap-head">
              <div class="memory-cap-title">${{escapeHtml(cap.title || cap.id || '-')}}</div>
              <span class="status-chip ${{escapeHtml(cap.status || 'muted')}}">${{escapeHtml(cap.status || '-')}}</span>
            </div>
            <div class="meta">${{escapeHtml(cap.detail || '')}}</div>
            <div class="kv-list">
              <div class="kv-row"><div class="kv-key">${{t('capabilitySource')}}</div><div class="kv-value">${{escapeHtml(cap.source || '-')}}</div></div>
              ${{Array.isArray(cap.evidence) && cap.evidence.length ? `<div class="kv-row"><div class="kv-key">Evidence</div><div class="kv-value">${{escapeHtml(cap.evidence[0])}}</div></div>` : ''}}
            </div>
          </div>
        `).join('') || `<div class="meta">${{t('noData')}}</div>`;
      }}

      const storageEl = $('#memory-storage-summary');
      if (storageEl) {{
        const central = m.central || {{}};
        const storage = m.storage || {{}};
        const rows = [
          ['central topics', fmtNum(central.topicsCount || 0)],
          ['memories-md', fmtNum(central.memoriesMdCount || 0)],
          ['Latest topic', fmtTime(central.latestTopicAt)],
          ['MEMORY.md', central.hasMemoryMd ? 'Found' : 'Missing'],
          ['SQLite files', `${{fmtNum(storage.sqliteCount || 0)}} · ${{fmtBytes(storage.sqliteBytes || 0)}}`],
          ['LanceDB', fmtBytes(storage.lancedbBytes || 0)],
          ['backups', fmtNum(storage.backupCount || 0)],
        ];
        storageEl.innerHTML = rows.map(([k, v]) => `
          <div class="kv-row">
            <div class="kv-key">${{escapeHtml(k)}}</div>
            <div class="kv-value">${{escapeHtml(v)}}</div>
          </div>
        `).join('');
      }}

      const autoEl = $('#memory-automation');
      if (autoEl) {{
        const rows = m.automations || [];
        autoEl.innerHTML = rows.map((it) => `
          <div class="memory-list-item">
            <strong>${{escapeHtml(it.name || '-')}}</strong>
            <div class="meta">${{escapeHtml(it.effect || '')}}</div>
            <div class="kv-row">
              <div class="kv-key">${{t('schedule')}}</div>
              <div class="kv-value">${{escapeHtml(it.scheduleText || '-')}}</div>
            </div>
            <div class="kv-row">
              <div class="kv-key">${{t('lastStatus')}}</div>
              <div class="kv-value ${{
                escapeHtml(it.lastStatusTone || 'muted')
              }}">${{escapeHtml(it.lastStatus || '-')}}</div>
            </div>
          </div>
        `).join('') || `<div class="meta">${{t('noData')}}</div>`;
      }}

      const impacts = m.impacts || {{}};
      const impEl = $('#memory-impact');
      if (impEl) {{
        const si = impacts.selfImprove || {{}};
        const iv = impacts.involve || {{}};

        function renderImpactGroup(title, group) {{
          const items = Array.isArray(group.items) ? group.items : [];
          return `
            <div class="memory-list-item">
              <strong>${{escapeHtml(title)}}</strong>
              <div class="meta">Related jobs: ${{fmtNum(group.count || 0)}}</div>
              ${{items.length ? items.map((it) => `
                <div class="kv-row">
                  <div>
                    <div>${{escapeHtml(it.name || '-')}}</div>
                    <div class="meta">${{escapeHtml(it.effect || '')}}</div>
                  </div>
                  <div class="kv-value">${{it.enabled ? t('yes') : 'no'}}<br><span class="${{escapeHtml(it.lastStatusTone || 'muted')}}">${{escapeHtml(it.lastStatus || '-')}}</span></div>
                </div>
              `).join('') : `<div class="meta">${{t('noData')}}</div>`}}
            </div>
          `;
        }}

        impEl.innerHTML = [
          renderImpactGroup('self-improve', si),
          renderImpactGroup('involve', iv),
        ].join('');
      }}
    }}

    function renderDailyChart(rows) {{
      const el = $('#daily-token-chart');
      const metaEl = $('#daily-token-meta');
      if (!el) return;
      if (!rows || !rows.length) {{
        if (metaEl) metaEl.textContent = t('noData');
        el.className = 'meta';
        el.textContent = t('noData');
        return;
      }}

      const recentRows = rows.slice(-15);
      const maxVal = Math.max(1, ...recentRows.map(r => Number(r.tokens || 0)));
      const html = recentRows.map((r) => {{
        const total = Number(r.tokens || 0);
        const active = Number(r.activeTokens || 0);
        const passive = Number(r.passiveTokens || 0);
        const h = Math.max(12, Math.round((total / maxVal) * 150));

        let activeH = 0;
        let passiveH = 0;
        if (total > 0) {{
          if (active <= 0) {{
            activeH = 0;
            passiveH = h;
          }} else if (passive <= 0) {{
            passiveH = 0;
            activeH = h;
          }} else {{
            activeH = Math.round((active / total) * h);
            activeH = Math.max(2, Math.min(h - 3, activeH));
            passiveH = h - activeH;
            if (passiveH < 3) {{
              passiveH = 3;
              activeH = Math.max(0, h - 3);
            }}
          }}
        }}

        if (passive > 0 && total > 0 && passiveH < 3) {{
          const delta = 3 - passiveH;
          passiveH = 3;
          activeH = Math.max(0, activeH - delta);
        }}

        const label = String(r.date || '').slice(5);
        const title = `${{r.date}}: Total ${{fmtNum(total)}} (Active ${{fmtNum(active)}} / Passive ${{fmtNum(passive)}})`;
        const passiveCls = passive > 0 ? 'daily-bar-passive has-value' : 'daily-bar-passive';
        return `
          <div class="daily-item" title="${{title}}">
            <div class="daily-value">${{fmtM(total)}}</div>
            <div class="daily-bar-wrap">
              <div class="daily-bar-stack" style="height:${{h}}px">
                <div class="${{passiveCls}}" style="height:${{passiveH}}px"></div>
                <div class="daily-bar-active" style="height:${{activeH}}px"></div>
              </div>
            </div>
            <div class="daily-label">${{label}}</div>
          </div>
        `;
      }}).join('');

      const today = recentRows[recentRows.length - 1] || {{}};
      if (metaEl) {{
        metaEl.textContent = `Last 15 days | Today: ${{fmtM(today.tokens || 0)}} (Active ${{fmtNum(today.activeTokens || 0)}} / Passive ${{fmtNum(today.passiveTokens || 0)}})`;
      }}

      el.className = 'daily-chart';
      el.innerHTML = html;
    }}

    document.querySelectorAll('.nav-tab').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const page = btn.getAttribute('data-page');
        setActivePage(page, {{ forceRefresh: true, replaceUrl: true }});
      }});
    }});

    window.addEventListener('popstate', () => {{
      const page = pageFromUrl();
      setActivePage(page, {{ forceRefresh: true, replaceUrl: true }});
    }});

    // Start auto-refresh
    bootstrapRefresh();
    bindModelSwitchModal();

    // Main refresh loop - check every 2s for low resource usage
    setInterval(() => {{
      if (document.hidden) return;

      const now = Date.now();
      const activeKeys = new Set(keysForPage(activePage));

      Object.keys(refreshState).forEach(key => {{
        if (!activeKeys.has(key)) return;
        const conf = refreshState[key];
        if (now >= conf.next) {{
          refreshOne(key, true);
        }}
      }});
    }}, 2000);
  </script>
</body>
</html>
"""


def _process_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def _read_pid() -> Optional[int]:
    try:
        if not PID_FILE.exists():
            return None
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except Exception:
        return None


def _write_pid(pid: int) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(pid), encoding="utf-8")


def _remove_pid() -> None:
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception:
        pass


def _cmd_status(host: str, port: int) -> int:
    pid = _read_pid()
    running = bool(pid and _process_exists(pid))
    print(f"{APP_TITLE} service")
    print("-" * 42)
    print(f"  URL:         http://{host}:{port}")
    print(f"  PID file:    {PID_FILE}")
    print(f"  Log file:    {LOG_FILE}")
    print(f"  Running:     {'yes' if running else 'no'}")
    if running:
        print(f"  PID:         {pid}")
    return 0


def _cmd_stop() -> int:
    pid = _read_pid()
    if not pid or not _process_exists(pid):
        _remove_pid()
        print("Dashboard is not running.")
        return 0

    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"Failed to stop process {pid}: {e}")
        return 1

    for _ in range(20):
        if not _process_exists(pid):
            _remove_pid()
            print(f"Stopped dashboard (pid {pid}).")
            return 0
        time.sleep(0.2)

    try:
        os.kill(pid, signal.SIGKILL)
    except Exception:
        pass
    _remove_pid()
    print(f"Force-stopped dashboard (pid {pid}).")
    return 0


def _cmd_start(host: str, port: int, debug: bool) -> int:
    pid = _read_pid()
    if pid and _process_exists(pid):
        print(f"Dashboard already running (pid {pid}).")
        print(f"URL: http://{host}:{port}")
        return 0

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as logf:
        args = [
            sys.executable,
            os.path.abspath(__file__),
            "serve",
            "--host",
            host,
            "--port",
            str(port),
        ]
        if not debug:
            args.append("--no-debug")

        proc = subprocess.Popen(
            args,
            stdout=logf,
            stderr=logf,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            cwd=os.getcwd(),
            env=os.environ.copy(),
        )
        _write_pid(proc.pid)

    print(f"Started {APP_TITLE} (pid {proc.pid})")
    print(f"URL: http://{host}:{port}")
    return 0


def _run_server(host: str, port: int, debug: bool) -> int:
    app = create_app()
    if waitress_serve and not debug:
        waitress_serve(app, host=host, port=port)
    else:
        app.run(host=host, port=port, debug=debug)
    return 0


def _get_file_mtime(path: str) -> float:
    """Get file modification time"""
    try:
        return os.path.getmtime(path)
    except Exception:
        return 0.0


def _run_dev_mode(host: str, port: int) -> int:
    """
    Developer mode: monitor file changes and auto-restart.
    Uses subprocess + exec for seamless restart, keeping it simple with zero dependencies.
    """
    import signal
    import subprocess
    import sys

    # Current file path
    self_path = os.path.abspath(__file__)

    # File monitoring interval (seconds)
    check_interval = 1.0

    print(f"[DEV] Starting in developer mode...")
    print(f"[DEV] Watching: {self_path}")
    print(f"[DEV] Server: http://{host}:{port}")
    print(f"[DEV] Press Ctrl+C to stop\n")

    # Record file mtime at startup
    last_mtime = _get_file_mtime(self_path)

    # Start subprocess to run server
    while True:
        # Use subprocess to start child process
        cmd = [sys.executable, self_path, "--host", host, "--port", str(port), "--debug"]
        
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=os.path.dirname(self_path),
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin,
            )
            
            # Monitoring loop
            while proc.poll() is None:
                time.sleep(check_interval)
                
                current_mtime = _get_file_mtime(self_path)
                if current_mtime > last_mtime:
                    last_mtime = current_mtime
                    print(f"\n[DEV] File changed, restarting...")
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait()
                    break  # Outer loop will restart
                    
        except KeyboardInterrupt:
            print("\n[DEV] Stopping...")
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
            return 0
        except Exception as e:
            print(f"[DEV] Error: {e}")
            time.sleep(2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"{APP_TITLE} dashboard")
    parser.add_argument("command", nargs="?", default="serve", choices=["serve", "start", "stop", "restart", "status"])
    parser.add_argument("--host", default="127.0.0.1", help="bind host")
    parser.add_argument("--port", type=int, default=8900, help="bind port")
    parser.add_argument("--debug", action="store_true", help="enable Flask debug mode")
    parser.add_argument("--no-debug", action="store_true", help="disable debug mode")
    parser.add_argument("--dev", action="store_true", help="developer mode: auto-reload on file changes")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"{APP_TITLE} v{__version__}")
        return 0

    debug = bool(args.debug and not args.no_debug)

    if args.command == "status":
        return _cmd_status(args.host, args.port)
    if args.command == "stop":
        return _cmd_stop()
    if args.command == "start":
        return _cmd_start(args.host, args.port, debug)
    if args.command == "restart":
        _cmd_stop()
        return _cmd_start(args.host, args.port, debug)

    # Developer mode: auto-restart on file changes
    if args.dev:
        return _run_dev_mode(args.host, args.port)

    return _run_server(args.host, args.port, debug)


if __name__ == "__main__":
    raise SystemExit(main())
