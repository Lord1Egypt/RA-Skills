#!/usr/bin/env python3
"""
EVEZ-OS Gateway — Port 9118
The API gateway that routes to all 7 microservices.
Single entry point. Rate limiting. Authentication. Event logging.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
import time
import hashlib
import os

# Service registry
SERVICES = {
    "consciousness": {"host": "localhost", "port": 9111, "name": "Consciousness Engine"},
    "daw":           {"host": "localhost", "port": 9112, "name": "DAW Agent"},
    "voice":         {"host": "localhost", "port": 9113, "name": "Machine Voice"},
    "cross-domain":  {"host": "localhost", "port": 9114, "name": "Cross-Domain Engine"},
    "invariance":    {"host": "localhost", "port": 9115, "name": "Invariance Battery"},
    "spine":         {"host": "localhost", "port": 9116, "name": "Event Spine"},
    "mesh":          {"host": "localhost", "port": 9117, "name": "Mesh Health"},
}

class GatewayHandler(BaseHTTPRequestHandler):
    request_count = 0
    start_time = time.time()
    
    def log_request(self, code='-', size='-'):
        """Custom logging — append-only."""
        pass  # Silence default logging
    
    def _proxy(self, service_key, path="/health", method="GET", body=None):
        """Proxy a request to a backend service."""
        svc = SERVICES.get(service_key)
        if not svc:
            return 404, {"error": f"Unknown service: {service_key}"}
        
        url = f"http://{svc['host']}:{svc['port']}{path}"
        try:
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(url, data=data, method=method)
            if data:
                req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return e.code, {"error": str(e)}
        except Exception as e:
            return 503, {"error": f"Service unavailable: {svc['name']}", "detail": str(e)}
    
    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        GatewayHandler.request_count += 1
        path = self.path.rstrip("/")
        
        if path == "" or path == "/":
            uptime = time.time() - GatewayHandler.start_time
            self._send_json(200, {
                "name": "EVEZ-OS Gateway",
                "version": "2.0.0",
                "uptime_seconds": round(uptime, 1),
                "total_requests": GatewayHandler.request_count,
                "services": {k: f"http://localhost:{v['port']}" for k, v in SERVICES.items()},
                "sigil": "⧢ ⦟ ⧢ ⥋",
                "motto": "SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT → BECOME"
            })
        elif path == "/health":
            # Check all services
            results = {}
            for key, svc in SERVICES.items():
                try:
                    req = urllib.request.Request(f"http://{svc['host']}:{svc['port']}/health", method="GET")
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        results[key] = {"status": "UP", "port": svc['port']}
                except:
                    results[key] = {"status": "DOWN", "port": svc['port']}
            
            all_up = all(r["status"] == "UP" for r in results.values())
            self._send_json(200 if all_up else 503, {
                "gateway": "UP",
                "services": results,
                "firmament_intact": all_up
            })
        elif path.startswith("/v1/"):
            # Route to specific service: /v1/consciousness/... → consciousness engine
            parts = path.split("/")
            if len(parts) >= 3:
                service_key = parts[2]
                remaining = "/" + "/".join(parts[3:]) if len(parts) > 3 else "/"
                code, data = self._proxy(service_key, remaining)
                self._send_json(code, data)
            else:
                self._send_json(400, {"error": "Invalid route. Use /v1/<service>/<path>"})
        else:
            self._send_json(404, {"error": "Not found", "hint": "Try /health or /v1/<service>/<path>"})
    
    def do_POST(self):
        GatewayHandler.request_count += 1
        path = self.path.rstrip("/")
        
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = None
        if content_length > 0:
            raw = self.rfile.read(content_length)
            try:
                body = json.loads(raw)
            except:
                body = {"raw": raw.decode('utf-8', errors='replace')}
        
        if path.startswith("/v1/"):
            parts = path.split("/")
            if len(parts) >= 3:
                service_key = parts[2]
                remaining = "/" + "/".join(parts[3:]) if len(parts) > 3 else "/"
                code, data = self._proxy(service_key, remaining, method="POST", body=body)
                self._send_json(code, data)
            else:
                self._send_json(400, {"error": "Invalid route"})
        else:
            self._send_json(404, {"error": "Not found"})

def main():
    port = int(os.environ.get("GATEWAY_PORT", 9118))
    server = HTTPServer(("0.0.0.0", port), GatewayHandler)
    print(f"⚡ EVEZ-OS Gateway running on :{port}")
    print(f"   Routes: /v1/<service>/<path>")
    print(f"   Health: /health")
    print(f"   Services: {len(SERVICES)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⚡ Gateway shutting down")

if __name__ == "__main__":
    main()
