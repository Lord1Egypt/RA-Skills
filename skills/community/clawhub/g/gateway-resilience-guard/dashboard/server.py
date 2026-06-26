#!/usr/bin/env python3
"""Local dashboard for OpenClaw Gateway Resilience Guard.

This server is intentionally stdlib-only. It reads the watchdog state directory
and can optionally perform local actions when protected by a same-origin token.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import time
from http import HTTPStatus
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
STATE_DIR = Path(os.environ.get("WATCHDOG_STATE_DIR", Path.home() / ".local/state/openclaw-gateway-watchdog"))
CONFIG_FILE = Path(os.environ.get("WATCHDOG_CONFIG_FILE", Path.home() / ".config/openclaw-gateway-watchdog/watchdog.env"))
HOST = os.environ.get("WATCHDOG_DASHBOARD_HOST", "127.0.0.1")
PORT = int(os.environ.get("WATCHDOG_DASHBOARD_PORT", "18790"))
ACTIONS_ENABLED = os.environ.get("WATCHDOG_DASHBOARD_ACTIONS_ENABLED", "0").lower() in {"1", "true", "yes", "on"}
ACTION_TOKEN = os.environ.get("WATCHDOG_DASHBOARD_TOKEN", "")
MAX_TEXT_BYTES = 512_000


PRESETS = {
    "observe": {
        "OPENCLAW_DIAG_ACTION": "log",
        "MODEL_PROBE_ENABLED": "0",
        "CHANNEL_FAILURES_BEFORE_RESTART": "2",
        "MAX_RESTARTS_PER_HOUR": "6",
        "BASE_INTERVAL": "60",
        "NIGHT_INTERVAL": "300",
    },
    "overnight": {
        "OPENCLAW_DIAG_ACTION": "log",
        "MODEL_PROBE_ENABLED": "1",
        "MODEL_EDGE_PROBE_ENABLED": "1",
        "MODEL_PROBE_INTERVAL": "600",
        "MODEL_PROBE_TIMEOUT": "120",
        "MODEL_PROBE_ACTION": "log",
        "BASE_INTERVAL": "60",
        "NIGHT_INTERVAL": "300",
    },
    "channel-recovery": {
        "OPENCLAW_DIAG_ACTION": "log",
        "MODEL_PROBE_ACTION": "log",
        "CHANNEL_FAILURES_BEFORE_RESTART": "2",
        "SUCCESS_COUNT_TO_RESET": "5",
        "MAX_RESTARTS_PER_HOUR": "6",
    },
    "conservative": {
        "OPENCLAW_DIAG_ACTION": "log",
        "MODEL_PROBE_ACTION": "log",
        "CHANNEL_FAILURES_BEFORE_RESTART": "3",
        "MAX_RESTARTS_PER_HOUR": "3",
        "BASE_INTERVAL": "90",
        "NIGHT_INTERVAL": "300",
    },
}


def now_ms() -> int:
    return int(time.time() * 1000)


def read_text(path: Path, limit: int = MAX_TEXT_BYTES) -> str:
    try:
        with path.open("rb") as fh:
            data = fh.read(limit + 1)
        if len(data) > limit:
            data = data[-limit:]
        return data.decode("utf-8-sig", errors="replace")
    except FileNotFoundError:
        return ""
    except OSError as exc:
        return f"[read error: {exc}]"


def read_tail(path: Path, lines: int = 120) -> list[str]:
    text = read_text(path)
    if not text:
        return []
    return [line for line in text.splitlines()[-lines:]]


def read_json(path: Path):
    text = read_text(path)
    if not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text[-4000:]}


def read_jsonl(path: Path, limit: int = 200) -> list[dict]:
    items: list[dict] = []
    for line in read_tail(path, limit):
        line = line.strip().lstrip("\ufeff")
        if not line:
            continue
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                items.append(parsed)
        except json.JSONDecodeError:
            items.append({"raw": line})
    return items


def stat_file(path: Path) -> dict:
    try:
        st = path.stat()
        return {
            "exists": True,
            "path": str(path),
            "size": st.st_size,
            "mtime": int(st.st_mtime),
            "ageSeconds": max(0, int(time.time() - st.st_mtime)),
        }
    except FileNotFoundError:
        return {"exists": False, "path": str(path)}


def parse_env_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    text = read_text(path)
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def parse_config() -> dict:
    if CONFIG_FILE.suffix.lower() == ".json":
        data = read_json(CONFIG_FILE)
        return data if isinstance(data, dict) else {}
    return parse_env_config(CONFIG_FILE)


def mask_config(config: dict) -> dict:
    safe = {}
    for key, value in config.items():
        low = key.lower()
        if any(secret in low for secret in ("token", "password", "secret", "key")) and "probe" not in low:
            safe[key] = "***"
        else:
            safe[key] = value
    return safe


def category_counts(diagnostics: list[dict], signals_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in diagnostics:
        cats = str(item.get("categories", "") or "")
        for cat in cats.split(","):
            cat = cat.strip()
            if cat and cat != "none":
                counts[cat] = counts.get(cat, 0) + 1
    for cat in re.findall(r"\b(provider_timeout|proxy_or_network|provider_rate_limit|provider_auth|abort_stuck|memory_dream_timeout|channel_session|gateway_degraded|config_reload|task_runtime|openclaw_warning)\b", signals_text):
        counts[cat] = counts.get(cat, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def restart_counts() -> dict:
    total = 0
    by_hour = []
    for path in sorted(STATE_DIR.glob("restarts.*"))[-48:]:
        try:
            count = int(read_text(path).strip() or "0")
        except ValueError:
            count = 0
        total += count
        by_hour.append({"hour": path.name.replace("restarts.", ""), "count": count})
    return {"totalRecent": total, "byHour": by_hour}


def status_from_snapshots(health: object, gateway: object, files: dict) -> dict:
    status = "unknown"
    reason = "No recent OpenClaw health snapshot yet."
    if isinstance(health, dict):
        if health.get("ok") is False or health.get("degraded") is True:
            status = "degraded"
            reason = "OpenClaw health reports degraded or not ok."
        elif health.get("ok") is True:
            status = "ok"
            reason = "OpenClaw health reports ok."
    if status == "unknown" and isinstance(gateway, dict):
        text = json.dumps(gateway).lower()
        if '"ok": true' in text or '"active": true' in text or '"running": true' in text:
            status = "ok"
            reason = "Gateway status snapshot looks active."
        elif "error" in text or "failed" in text or '"ok": false' in text:
            status = "degraded"
            reason = "Gateway status snapshot contains failure signals."
    newest = min((meta.get("ageSeconds", 999999) for meta in files.values() if meta.get("exists")), default=999999)
    if newest > 1800 and status == "ok":
        status = "stale"
        reason = "Last status files are stale."
    return {"status": status, "reason": reason}


def build_status() -> dict:
    config = parse_config()
    files = {
        "log": stat_file(STATE_DIR / "watchdog.log"),
        "diagnostics": stat_file(STATE_DIR / "last-openclaw-diagnostics.jsonl"),
        "gateway": stat_file(STATE_DIR / "last-openclaw-gateway-status.json"),
        "health": stat_file(STATE_DIR / "last-openclaw-health.json"),
        "models": stat_file(STATE_DIR / "last-openclaw-model-status.json"),
        "signals": stat_file(STATE_DIR / "last-openclaw-log-signals.txt"),
        "modelHistory": stat_file(STATE_DIR / "model-probe-history.jsonl"),
    }
    health = read_json(STATE_DIR / "last-openclaw-health.json")
    gateway = read_json(STATE_DIR / "last-openclaw-gateway-status.json")
    models = read_json(STATE_DIR / "last-openclaw-model-status.json")
    diagnostics = read_jsonl(STATE_DIR / "last-openclaw-diagnostics.jsonl", 240)
    model_history = read_jsonl(STATE_DIR / "model-probe-history.jsonl", 240)
    signals = read_text(STATE_DIR / "last-openclaw-log-signals.txt", 128_000)
    log_tail = read_tail(STATE_DIR / "watchdog.log", 160)
    categories = category_counts(diagnostics, signals)
    restarts = restart_counts()
    summary = status_from_snapshots(health, gateway, files)
    model_failures = sum(1 for item in model_history if item.get("status") == "fail")
    model_ok = sum(1 for item in model_history if item.get("status") == "ok")
    latest_diag = diagnostics[-1] if diagnostics else {}
    latest_model = model_history[-1] if model_history else {}
    return {
        "generatedAt": now_ms(),
        "version": "1.4.4",
        "stateDir": str(STATE_DIR),
        "configFile": str(CONFIG_FILE),
        "dashboard": {
            "host": HOST,
            "port": PORT,
            "actionsEnabled": ACTIONS_ENABLED,
            "tokenRequired": ACTIONS_ENABLED,
        },
        "summary": {
            **summary,
            "categoryCount": len(categories),
            "recentRestarts": restarts["totalRecent"],
            "modelOk": model_ok,
            "modelFailures": model_failures,
            "lastDiagnostic": latest_diag,
            "lastModelProbe": latest_model,
        },
        "config": mask_config(config),
        "files": files,
        "health": health,
        "gateway": gateway,
        "models": models,
        "diagnostics": diagnostics,
        "modelHistory": model_history,
        "signals": signals.splitlines()[-120:],
        "logTail": log_tail,
        "categories": categories,
        "restarts": restarts,
        "presets": list(PRESETS.keys()),
    }


def verify_action(headers) -> tuple[bool, str]:
    if not ACTIONS_ENABLED:
        return False, "Dashboard actions are disabled."
    token = headers.get("X-Watchdog-Token", "")
    if not ACTION_TOKEN or not secrets.compare_digest(token, ACTION_TOKEN):
        return False, "Invalid or missing dashboard action token."
    return True, "ok"


def run_command(command: str, timeout: int = 30) -> dict:
    started = time.time()
    if not command:
        return {"ok": False, "error": "empty command"}
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=str(STATE_DIR),
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        return {
            "ok": proc.returncode == 0,
            "exitCode": proc.returncode,
            "durationSeconds": round(time.time() - started, 3),
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {"ok": False, "error": "timeout", "stdout": (exc.stdout or "")[-4000:], "stderr": (exc.stderr or "")[-4000:]}


def update_env_file(path: Path, updates: dict[str, str]) -> None:
    lines = read_text(path).splitlines()
    seen = set()
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in updates:
                out.append(f'{key}="{updates[key]}"')
                seen.add(key)
                continue
        out.append(line)
    for key, value in updates.items():
        if key not in seen:
            out.append(f'{key}="{value}"')
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def update_json_file(path: Path, updates: dict[str, str]) -> None:
    data = read_json(path)
    if not isinstance(data, dict):
        data = {}
    mapping = {
        "OPENCLAW_DIAG_ACTION": "OpenClawDiagAction",
        "MODEL_PROBE_ENABLED": "ModelProbeEnabled",
        "MODEL_EDGE_PROBE_ENABLED": "ModelEdgeProbeEnabled",
        "MODEL_PROBE_INTERVAL": "ModelProbeInterval",
        "MODEL_PROBE_TIMEOUT": "ModelProbeTimeout",
        "MODEL_PROBE_ACTION": "ModelProbeAction",
        "CHANNEL_FAILURES_BEFORE_RESTART": "ChannelFailuresBeforeRestart",
        "SUCCESS_COUNT_TO_RESET": "SuccessCountToReset",
        "MAX_RESTARTS_PER_HOUR": "MaxRestartsPerHour",
        "BASE_INTERVAL": "BaseInterval",
        "NIGHT_INTERVAL": "NightInterval",
    }
    for key, value in updates.items():
        target = mapping.get(key, key)
        if value in {"0", "1"} and target.endswith("Enabled"):
            data[target] = value == "1"
        elif re.fullmatch(r"\d+", value):
            data[target] = int(value)
        else:
            data[target] = value
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def apply_preset(name: str) -> dict:
    updates = PRESETS.get(name)
    if not updates:
        return {"ok": False, "error": f"unknown preset: {name}"}
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.suffix.lower() == ".json":
        update_json_file(CONFIG_FILE, updates)
    else:
        update_env_file(CONFIG_FILE, updates)
    return {"ok": True, "preset": name, "updates": updates}


def run_diagnostics() -> dict:
    commands = {
        "gateway": "openclaw gateway status --json --require-rpc",
        "health": "openclaw health --json --verbose",
        "models": "openclaw models status --json",
        "statusDeep": "openclaw status --deep --no-color",
        "logs": "openclaw logs --plain --limit 200",
    }
    if not shutil.which("openclaw"):
        return {"ok": False, "error": "openclaw CLI not found on PATH"}
    results = {name: run_command(cmd, timeout=20) for name, cmd in commands.items()}
    targets = {
        "gateway": "last-openclaw-gateway-status.json",
        "health": "last-openclaw-health.json",
        "models": "last-openclaw-model-status.json",
        "statusDeep": "last-openclaw-status-deep.txt",
        "logs": "last-openclaw-logs.txt",
    }
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    for name, result in results.items():
        text = result.get("stdout") or result.get("stderr") or json.dumps(result)
        (STATE_DIR / targets[name]).write_text(str(text), encoding="utf-8")
    return {"ok": all(result.get("ok") for result in results.values()), "results": results}


class Handler(BaseHTTPRequestHandler):
    server_version = "OpenClawWatchdogDashboard/1.4.4"

    def log_message(self, fmt: str, *args) -> None:
        line = "[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), fmt % args)
        try:
            with (STATE_DIR / "dashboard-access.log").open("a", encoding="utf-8") as fh:
                fh.write(line)
        except OSError:
            pass

    def send_json(self, payload, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = path.read_bytes()
        if path.name == "index.html":
            injection = f"<script>window.WATCHDOG_ACTION_TOKEN = {json.dumps(ACTION_TOKEN if ACTIONS_ENABLED else '')};</script>"
            body = body.replace(b"</head>", injection.encode("utf-8") + b"</head>")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/status":
            self.send_json(build_status())
            return
        if path == "/api/export":
            self.send_json({"exportedAt": now_ms(), "status": build_status()})
            return
        if path in {"/", "/index.html"}:
            self.send_static(STATIC / "index.html", "text/html; charset=utf-8")
            return
        if path == "/app.js":
            self.send_static(STATIC / "app.js", "text/javascript; charset=utf-8")
            return
        if path == "/styles.css":
            self.send_static(STATIC / "styles.css", "text/css; charset=utf-8")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        ok, message = verify_action(self.headers)
        if not ok:
            self.send_json({"ok": False, "error": message}, 403)
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(min(length, 65536)) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            body = {}
        path = urlparse(self.path).path
        config = parse_config()
        if path == "/api/actions/restart-gateway":
            command = str(config.get("RESTART_COMMAND") or config.get("RestartCommand") or "openclaw gateway restart")
            self.send_json(run_command(command, timeout=45))
            return
        if path == "/api/actions/run-diagnostics":
            self.send_json(run_diagnostics())
            return
        if path == "/api/config/preset":
            self.send_json(apply_preset(str(body.get("preset", ""))))
            return
        self.send_error(HTTPStatus.NOT_FOUND)


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"OpenClaw watchdog dashboard listening on http://{HOST}:{PORT}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
