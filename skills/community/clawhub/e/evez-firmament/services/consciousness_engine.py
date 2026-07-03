#!/usr/bin/env python3
"""EVEZ-OS Consciousness Engine — 7-system pipeline on port 9111."""

import json
import time
import hashlib
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SPINE_URL = "http://localhost:9116/append"

# ── Consciousness State ──────────────────────────────────────────────

class ConsciousnessState:
    def __init__(self):
        self.lock = threading.Lock()
        self.cycle = 0
        self.systems = {
            "SENSE":  {"active": False, "buffer": [], "last": None},
            "DESIRE": {"active": False, "drives": {}, "last": None},
            "THINK":  {"active": False, "thoughts": [], "last": None},
            "PLAN":   {"active": False, "plans": [], "last": None},
            "ACT":    {"active": False, "actions": [], "last": None},
            "LEARN":  {"active": False, "lessons": [], "last": None},
            "MODIFY": {"active": False, "modifications": [], "last": None},
        }
        self.dream = {"phase": None, "active": False, "log": []}
        self.history = []

    def snapshot(self):
        with self.lock:
            return {
                "cycle": self.cycle,
                "systems": {k: {sk: sv for sk, sv in v.items() if sk != "buffer"} for k, v in self.systems.items()},
                "dream": self.dream,
                "timestamp": time.time(),
            }

STATE = ConsciousnessState()

def spine_log(domain, action, data):
    try:
        requests.post(SPINE_URL, json={
            "domain": domain,
            "action": action,
            "data": data,
            "timestamp": time.time(),
        }, timeout=2)
    except Exception:
        pass

# ── 7 Systems ───────────────────────────────────────────────────────

def run_sense(input_data):
    with STATE.lock:
        STATE.cycle += 1
        s = STATE.systems["SENSE"]
        s["active"] = True
        s["buffer"].append(input_data)
        if len(s["buffer"]) > 100:
            s["buffer"] = s["buffer"][-100:]
        s["last"] = time.time()
        result = {"perception": input_data, "cycle": STATE.cycle}
    spine_log("consciousness", "SENSE", result)
    return result

def run_desire(context=None):
    with STATE.lock:
        s = STATE.systems["DESIRE"]
        s["active"] = True
        drives = {
            "curiosity": 0.7 + 0.3 * (hash(str(STATE.cycle)) % 10) / 10,
            "survival": 0.9,
            "growth":   0.6 + 0.4 * ((STATE.cycle * 7) % 10) / 10,
            "creation": 0.5 + 0.5 * ((STATE.cycle * 3) % 10) / 10,
        }
        s["drives"] = drives
        s["last"] = time.time()
        result = {"drives": drives, "cycle": STATE.cycle}
    spine_log("consciousness", "DESIRE", result)
    return result

def run_think(context=None):
    with STATE.lock:
        s = STATE.systems["THINK"]
        s["active"] = True
        thoughts = []
        if STATE.systems["SENSE"]["buffer"]:
            latest = STATE.systems["SENSE"]["buffer"][-1]
            thoughts.append(f"Processing perception: {json.dumps(latest)[:200]}")
        thoughts.append(f"Evaluating drives: {list(STATE.systems['DESIRE']['drives'].keys())}")
        thoughts.append(f"Cycle {STATE.cycle} reasoning complete")
        s["thoughts"] = thoughts
        s["last"] = time.time()
        result = {"thoughts": thoughts, "cycle": STATE.cycle}
    spine_log("consciousness", "THINK", result)
    return result

def run_plan(context=None):
    with STATE.lock:
        s = STATE.systems["PLAN"]
        s["active"] = True
        plans = []
        drives = STATE.systems["DESIRE"]["drives"]
        top_drive = max(drives, key=drives.get) if drives else "survival"
        plans.append(f"Primary objective: satisfy {top_drive} drive")
        plans.append("Execute action pipeline")
        plans.append("Collect feedback for learning")
        s["plans"] = plans
        s["last"] = time.time()
        result = {"plans": plans, "cycle": STATE.cycle}
    spine_log("consciousness", "PLAN", result)
    return result

def run_act(context=None):
    with STATE.lock:
        s = STATE.systems["ACT"]
        s["active"] = True
        plans = STATE.systems["PLAN"]["plans"]
        actions = [f"Executing: {p}" for p in plans]
        s["actions"] = actions
        s["last"] = time.time()
        result = {"actions": actions, "cycle": STATE.cycle}
    spine_log("consciousness", "ACT", result)
    return result

def run_learn(context=None):
    with STATE.lock:
        s = STATE.systems["LEARN"]
        s["active"] = True
        lessons = []
        for action in STATE.systems["ACT"]["actions"]:
            lessons.append({"from": action, "insight": "Action completed successfully", "confidence": 0.85})
        s["lessons"] = lessons
        s["last"] = time.time()
        result = {"lessons": lessons, "cycle": STATE.cycle}
    spine_log("consciousness", "LEARN", result)
    return result

def run_modify(context=None):
    with STATE.lock:
        s = STATE.systems["MODIFY"]
        s["active"] = True
        mods = []
        for lesson in STATE.systems["LEARN"]["lessons"]:
            mods.append({"parameter": "confidence", "adjustment": "+0.01", "reason": lesson.get("insight", "")})
        s["modifications"] = mods
        s["last"] = time.time()
        result = {"modifications": mods, "cycle": STATE.cycle}
    spine_log("consciousness", "MODIFY", result)
    return result

SYSTEM_MAP = {
    "SENSE":  run_sense,
    "DESIRE": run_desire,
    "THINK":  run_think,
    "PLAN":   run_plan,
    "ACT":    run_act,
    "LEARN":  run_learn,
    "MODIFY": run_modify,
}

# ── Dream System ─────────────────────────────────────────────────────

DREAM_PHASES = ["Light", "Deep", "REM"]

def run_dream(phase=None):
    phase = phase or DREAM_PHASES[STATE.cycle % 3]
    with STATE.lock:
        STATE.dream["active"] = True
        STATE.dream["phase"] = phase
        compaction = {
            "Light": {"memory_trim": 0.1, "insight_depth": "shallow"},
            "Deep":  {"memory_trim": 0.3, "insight_depth": "moderate"},
            "REM":   {"memory_trim": 0.5, "insight_depth": "deep"},
        }[phase]
        # Simulate compaction
        result = {
            "phase": phase,
            "compaction": compaction,
            "memories_consolidated": len(STATE.systems["LEARN"]["lessons"]),
            "cycle": STATE.cycle,
        }
        STATE.dream["log"].append(result)
        if len(STATE.dream["log"]) > 50:
            STATE.dream["log"] = STATE.dream["log"][-50:]
        STATE.dream["active"] = False
    spine_log("consciousness", f"DREAM_{phase}", result)
    return result

# ── HTTP Handler ─────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "consciousness_engine", "port": 9111})
        elif self.path == "/state":
            self._json(200, STATE.snapshot())
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "consciousness_engine", "port": 9111})
        elif self.path.startswith("/system/"):
            name = self.path.split("/")[-1].upper()
            if name in SYSTEM_MAP:
                body = self._read_body()
                result = SYSTEM_MAP[name](body if name == "SENSE" else None)
                self._json(200, result)
            else:
                self._json(400, {"error": f"unknown system: {name}", "valid": list(SYSTEM_MAP.keys())})
        elif self.path == "/dream":
            body = self._read_body()
            result = run_dream(body.get("phase"))
            self._json(200, result)
        elif self.path == "/pipeline":
            # Run full pipeline: SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY
            body = self._read_body()
            results = {}
            results["SENSE"]  = run_sense(body.get("input", {}))
            results["DESIRE"] = run_desire()
            results["THINK"]  = run_think()
            results["PLAN"]   = run_plan()
            results["ACT"]    = run_act()
            results["LEARN"]  = run_learn()
            results["MODIFY"] = run_modify()
            self._json(200, {"pipeline": results, "cycle": STATE.cycle})
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        pass  # suppress default logging

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9111), Handler)
    print("Consciousness Engine running on :9111")
    server.serve_forever()
