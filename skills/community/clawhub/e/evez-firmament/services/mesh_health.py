#!/usr/bin/env python3
"""EVEZ-OS Mesh Health — Topology-aware health monitor on port 9117."""

import json
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SPINE_URL = "http://localhost:9116/append"

# ── Mesh Topology ───────────────────────────────────────────────────

MESH = {
    "consciousness_engine": {"port": 9111, "host": "localhost"},
    "daw_agent":           {"port": 9112, "host": "localhost"},
    "machine_voice":       {"port": 9113, "host": "localhost"},
    "cross_domain":        {"port": 9114, "host": "localhost"},
    "invariance":          {"port": 9115, "host": "localhost"},
    "event_spine":         {"port": 9116, "host": "localhost"},
    "mesh_health":          {"port": 9117, "host": "localhost"},
}

def spine_log(domain, action, data):
    try:
        requests.post(SPINE_URL, json={"domain": domain, "action": action, "data": data, "timestamp": time.time()}, timeout=2)
    except Exception:
        pass

def check_sibling(name, info, timeout=3):
    """Check health of a sibling service."""
    url = f"http://{info['host']}:{info['port']}/health"
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return {"name": name, "status": "alive", "port": info["port"], "response": r.json()}
        else:
            return {"name": name, "status": "degraded", "port": info["port"], "code": r.status_code}
    except requests.exceptions.ConnectionError:
        return {"name": name, "status": "down", "port": info["port"], "error": "connection refused"}
    except requests.exceptions.Timeout:
        return {"name": name, "status": "timeout", "port": info["port"], "error": "timeout"}
    except Exception as e:
        return {"name": name, "status": "error", "port": info["port"], "error": str(e)}

def heal_sibling(name, info):
    """Attempt to repair a downed sibling — log the attempt and return status."""
    result = {"name": name, "port": info["port"], "actions": []}

    # Step 1: re-check
    check = check_sibling(name, info, timeout=2)
    if check["status"] == "alive":
        result["actions"].append({"step": "recheck", "result": "already alive"})
        result["status"] = "alive"
        return result

    # Step 2: try a gentle nudge via health POST (some services accept POST /health)
    try:
        r = requests.post(f"http://{info['host']}:{info['port']}/health", timeout=3)
        result["actions"].append({"step": "health_post", "status": r.status_code})
    except Exception as e:
        result["actions"].append({"step": "health_post", "error": str(e)})

    # Step 3: re-check
    check2 = check_sibling(name, info, timeout=2)
    if check2["status"] == "alive":
        result["actions"].append({"step": "recheck_after_nudge", "result": "revived"})
        result["status"] = "revived"
        spine_log("mesh_health", "heal", {"name": name, "status": "revived"})
        return result

    # Cannot heal remotely — report
    result["status"] = "unhealable"
    result["actions"].append({"step": "final", "result": "service requires manual restart"})
    spine_log("mesh_health", "heal_failed", {"name": name})
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
            self._json(200, {"status": "alive", "service": "mesh_health", "port": 9117})
        elif self.path == "/siblings":
            results = []
            for name, info in MESH.items():
                if name == "mesh_health":
                    results.append({"name": name, "status": "alive", "port": info["port"], "self": True})
                else:
                    results.append(check_sibling(name, info))
            alive = sum(1 for r in results if r.get("status") == "alive")
            self._json(200, {"siblings": results, "total": len(results), "alive": alive, "dead": len(results) - alive})
        elif self.path == "/topology":
            topo = {name: {"port": info["port"], "host": info["host"]} for name, info in MESH.items()}
            self._json(200, {"mesh": topo, "node_count": len(MESH)})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "mesh_health", "port": 9117})
            return

        body = self._read_body()

        if self.path == "/heal":
            name = body.get("service")
            if not name or name not in MESH:
                self._json(400, {"error": "specify valid service name", "valid": list(MESH.keys())})
                return
            result = heal_sibling(name, MESH[name])
            self._json(200, result)
        elif self.path == "/siblings":
            # Full check via POST (more explicit)
            results = []
            for name, info in MESH.items():
                if name == "mesh_health":
                    results.append({"name": name, "status": "alive", "port": info["port"], "self": True})
                else:
                    results.append(check_sibling(name, info))
            alive = sum(1 for r in results if r.get("status") == "alive")
            self._json(200, {"siblings": results, "total": len(results), "alive": alive})
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9117), Handler)
    print("Mesh Health running on :9117")
    server.serve_forever()
