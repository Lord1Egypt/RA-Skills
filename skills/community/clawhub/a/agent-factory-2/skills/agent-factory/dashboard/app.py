#!/usr/bin/env python3
"""
Zero-Dependency Realtime Web Dashboard & API Server for OpenClaw Agent Factory.
Works immediately on standard Python 3 (using built-in http.server) with optional FastAPI support.
"""

import os
import sys
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Add scripts directory to path
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from telemetry import analyze_clusters, log_task
from synthesizer import generate_subagent
from evaluator import run_benchmark
from router import route_and_execute, list_active_agents
from lifecycle import audit_lifecycle
from semantic_cache import stats as cache_stats
from clustering_engine import discover_clusters

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
PORT = int(os.environ.get("PORT", 8000))


from finops import calculate_savings, get_finops_overview
from prompt_evolver import evolve_prompt
from dag_coordinator import DAGCoordinator, TaskNode
from mesh_sync import export_agent_bundle, list_federated_mesh


class DashboardHTTPHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type="application/json", status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status_code=204)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            self._serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
        elif path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            file_path = os.path.join(STATIC_DIR, rel_path)
            content_type = "text/plain"
            if file_path.endswith(".css"):
                content_type = "text/css"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            elif file_path.endswith(".html"):
                content_type = "text/html; charset=utf-8"
            self._serve_file(file_path, content_type)
        elif path == "/api/overview":
            self._handle_overview()
        elif path == "/api/finops":
            self._set_headers("application/json")
            self.wfile.write(json.dumps(get_finops_overview()).encode("utf-8"))
        elif path == "/api/federation":
            self._set_headers("application/json")
            self.wfile.write(json.dumps(list_federated_mesh()).encode("utf-8"))
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        if path == "/api/route":
            prompt = payload.get("prompt", "").strip()
            if not prompt:
                self._set_headers("application/json", 400)
                self.wfile.write(json.dumps({"error": "Prompt cannot be empty"}).encode("utf-8"))
                return
            result = route_and_execute(prompt)
            self._set_headers("application/json")
            self.wfile.write(json.dumps(result).encode("utf-8"))

        elif path == "/api/evolve-prompt":
            base_prompt = payload.get("prompt", "Tu es un agent spécialisé.")
            domain = payload.get("domain", "general")
            generations = payload.get("generations", 3)
            evolved = evolve_prompt(base_prompt, domain, generations=generations)
            self._set_headers("application/json")
            self.wfile.write(json.dumps(evolved).encode("utf-8"))

        elif path == "/api/execute-dag":
            tasks = payload.get("tasks", [])
            nodes = [TaskNode(t["id"], t["prompt"], t.get("depends_on", [])) for t in tasks]
            coordinator = DAGCoordinator()
            dag_result = coordinator.execute_dag(nodes)
            self._set_headers("application/json")
            self.wfile.write(json.dumps(dag_result).encode("utf-8"))

        elif path == "/api/trigger-cycle":
            clusters = analyze_clusters()
            if not clusters:
                discover_clusters(min_cluster_size=2)
                clusters = analyze_clusters(min_occurrences=2)

            eligible = [c for c in clusters if c.get("eligible")]
            target = eligible[0] if eligible else (clusters[0] if clusters else None)

            if not target:
                resp = {"status": "no_cluster_found"}
            else:
                synth_res = generate_subagent(target["domain_tag"], target)
                bench_ok, bench_rep = run_benchmark(synth_res["agent_id"], synth_res["version"])
                resp = {
                    "status": "cycle_completed",
                    "synthesized": synth_res,
                    "benchmark_passed": bench_ok,
                    "benchmark_report": bench_rep
                }

            self._set_headers("application/json")
            self.wfile.write(json.dumps(resp).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint Not Found")

    def _serve_file(self, file_path: str, content_type: str):
        if not os.path.exists(file_path):
            self.send_error(404, f"File not found: {file_path}")
            return
        with open(file_path, "rb") as f:
            data = f.read()
        self._set_headers(content_type)
        self.wfile.write(data)

    def _handle_overview(self):
        agents = list_active_agents()
        clusters = analyze_clusters()
        c_stats = cache_stats()
        finops = calculate_savings(
            total_cached_tokens=c_stats.get("total_tokens_saved", 0),
            specialized_calls_count=len(agents) * 10
        )

        data = {
            "active_subagents_count": len(agents),
            "discovered_clusters_count": len(clusters),
            "cached_entries": c_stats.get("total_cached_entries", 0),
            "tokens_saved": c_stats.get("total_tokens_saved", 0),
            "finops": finops,
            "agents": agents,
            "clusters": clusters
        }
        self._set_headers("application/json")
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def log_message(self, format, *args):
        # Clean server logging
        sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {format % args}\n")


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def run_server():
    global PORT
    server = None
    for attempt in range(5):
        try:
            server = ReusableHTTPServer(("0.0.0.0", PORT), DashboardHTTPHandler)
            break
        except OSError as e:
            if e.errno == 48:
                print(f"⚠️ Port {PORT} in use, attempting on port {PORT + 1}...")
                PORT += 1
            else:
                raise e

    if not server:
        print("❌ Could not bind to an available port.")
        return

    print(f"\n🚀 OpenClaw Dashboard started successfully!")
    print(f"👉 Web Access: http://localhost:{PORT}")
    print(f"   (Press Ctrl+C to stop)\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.server_close()


if __name__ == "__main__":
    run_server()
