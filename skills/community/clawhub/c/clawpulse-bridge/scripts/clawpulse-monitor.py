#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import time
import urllib.request
import urllib.error
from threading import Lock
from datetime import datetime

BRIDGE_URL = os.environ.get("BRIDGE_URL", "http://127.0.0.1:8787/health")
BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "")
APP_TOKEN = os.environ.get("MONITOR_TOKEN", "")
BIND_HOST = os.environ.get("MONITOR_BIND_HOST", "0.0.0.0")
PORT = int(os.environ.get("MONITOR_PORT", "8788"))
POLL_SEC = float(os.environ.get("MONITOR_POLL_SEC", "5"))
FAIL_THRESHOLD = int(os.environ.get("MONITOR_FAIL_THRESHOLD", "3"))
RECOVER_THRESHOLD = int(os.environ.get("MONITOR_RECOVER_THRESHOLD", "2"))
COOLDOWN_SEC = int(os.environ.get("MONITOR_COOLDOWN_SEC", "30"))
TIMEOUT_SEC = float(os.environ.get("MONITOR_TIMEOUT_SEC", "8"))
WORK_BUSY_THRESHOLD = int(os.environ.get("MONITOR_WORK_BUSY_THRESHOLD", "1"))
WORK_IDLE_THRESHOLD = int(os.environ.get("MONITOR_WORK_IDLE_THRESHOLD", "3"))

state_lock = Lock()
state = {
    "online": False,
    "workStatus": "连接异常",
    "assistantName": "Athena",
    "tokenUsage": {"prompt": 0, "completion": 0, "total": 0},
    "thought": "监控器启动中。",
    "sourceCheckedAt": 0,
    "monitorCheckedAt": int(time.time() * 1000),
    "failCount": 0,
    "successCount": 0,
    "lastChangeAt": int(time.time() * 1000),
    "status": "offline",
    "workBusyHits": 0,
    "workIdleHits": 0,
    "dailyDate": datetime.now().strftime("%Y-%m-%d"),
    "dailyUsage": {"prompt": 0, "completion": 0, "total": 0},
    "lastRawUsage": {"prompt": 0, "completion": 0, "total": 0},
}

last_push = {"msg": "", "at": 0}

def fetch_bridge():
    req = urllib.request.Request(BRIDGE_URL)
    if BRIDGE_TOKEN:
        req.add_header("Authorization", f"Bearer {BRIDGE_TOKEN}")
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
        raw = r.read()
    obj = json.loads(raw.decode("utf-8"))
    return obj


def apply_state(raw_obj, ok):
    now_ms = int(time.time() * 1000)
    with state_lock:
        prev_online = bool(state.get("online", False))

        if ok:
            state["successCount"] = int(state.get("successCount", 0)) + 1
            state["failCount"] = 0
            if (not prev_online) and state["successCount"] >= RECOVER_THRESHOLD:
                state["online"] = True
                state["status"] = "online"
                state["lastChangeAt"] = now_ms
            elif prev_online:
                state["online"] = True
                state["status"] = "online"

            if isinstance(raw_obj, dict):
                state["assistantName"] = raw_obj.get("assistantName", state["assistantName"])
                state["tokenUsage"] = raw_obj.get("tokenUsage", state["tokenUsage"])
                state["thought"] = raw_obj.get("thought", state["thought"])
                state["sourceCheckedAt"] = int(raw_obj.get("checkedAt", now_ms) or now_ms)

                today = datetime.now().strftime("%Y-%m-%d")
                if state.get("dailyDate") != today:
                    state["dailyDate"] = today
                    state["dailyUsage"] = {"prompt": 0, "completion": 0, "total": 0}
                    state["lastRawUsage"] = {"prompt": 0, "completion": 0, "total": 0}

                raw_usage = raw_obj.get("tokenUsage", {}) if isinstance(raw_obj.get("tokenUsage", {}), dict) else {}
                cur_prompt = int(raw_usage.get("prompt", 0) or 0)
                cur_completion = int(raw_usage.get("completion", 0) or 0)
                cur_total = int(raw_usage.get("total", 0) or 0)

                last_raw = state.get("lastRawUsage", {"prompt": 0, "completion": 0, "total": 0})
                last_prompt = int(last_raw.get("prompt", 0) or 0)
                last_completion = int(last_raw.get("completion", 0) or 0)
                last_total = int(last_raw.get("total", 0) or 0)

                # If raw counters reset (e.g. session rollover), count current value as fresh increment.
                dp = cur_prompt - last_prompt if cur_prompt >= last_prompt else cur_prompt
                dc = cur_completion - last_completion if cur_completion >= last_completion else cur_completion
                dt = cur_total - last_total if cur_total >= last_total else cur_total

                daily = state.get("dailyUsage", {"prompt": 0, "completion": 0, "total": 0})
                daily["prompt"] = int(daily.get("prompt", 0) or 0) + max(0, dp)
                daily["completion"] = int(daily.get("completion", 0) or 0) + max(0, dc)
                daily["total"] = int(daily.get("total", 0) or 0) + max(0, dt)
                state["dailyUsage"] = daily
                state["lastRawUsage"] = {"prompt": cur_prompt, "completion": cur_completion, "total": cur_total}

                raw_work = str(raw_obj.get("workStatus", "")).strip()
                busy_signal = (raw_work == "工作中") or bool(raw_obj.get("activeTask", False))

                if state["online"]:
                    if busy_signal:
                        state["workBusyHits"] = int(state.get("workBusyHits", 0)) + 1
                        state["workIdleHits"] = 0
                        if state["workBusyHits"] >= WORK_BUSY_THRESHOLD:
                            state["workStatus"] = "工作中"
                    else:
                        state["workIdleHits"] = int(state.get("workIdleHits", 0)) + 1
                        state["workBusyHits"] = 0
                        if state["workIdleHits"] >= WORK_IDLE_THRESHOLD:
                            state["workStatus"] = "闲置"
        else:
            state["failCount"] = int(state.get("failCount", 0)) + 1
            state["successCount"] = 0
            if prev_online and state["failCount"] >= FAIL_THRESHOLD:
                state["online"] = False
                state["status"] = "offline"
                state["workStatus"] = "连接异常"
                state["workBusyHits"] = 0
                state["workIdleHits"] = 0
                state["thought"] = "监控器判定离线，等待恢复。"
                state["lastChangeAt"] = now_ms

        state["monitorCheckedAt"] = now_ms


def monitor_loop():
    while True:
        try:
            obj = fetch_bridge()
            apply_state(obj, True)
        except Exception:
            apply_state(None, False)
        time.sleep(max(1.0, POLL_SEC))


class H(BaseHTTPRequestHandler):
    def _json(self, code, payload):
        b = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/internal":
            with state_lock:
                self._json(200, dict(state))
            return

        if self.path not in ["/health", "/status"]:
            self._json(404, {"error": "not_found"})
            return

        auth = self.headers.get("Authorization", "")
        if APP_TOKEN and auth != f"Bearer {APP_TOKEN}":
            self._json(401, {"error": "unauthorized"})
            return

        with state_lock:
            out = {
                "online": state["online"],
                "status": state["status"],
                "assistantName": state["assistantName"],
                "workStatus": state["workStatus"],
                "tokenUsage": state["tokenUsage"],
                "tokenUsageDaily": state.get("dailyUsage", {"prompt": 0, "completion": 0, "total": 0}),
                "dailyDate": state.get("dailyDate"),
                "thought": state["thought"],
                "checkedAt": state["monitorCheckedAt"],
                "lastChangeAt": state["lastChangeAt"],
                "sourceCheckedAt": state["sourceCheckedAt"],
            }
        self._json(200, out)

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    if not APP_TOKEN:
        raise SystemExit("MONITOR_TOKEN is empty")
    import threading
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()
    ThreadingHTTPServer((BIND_HOST, PORT), H).serve_forever()
