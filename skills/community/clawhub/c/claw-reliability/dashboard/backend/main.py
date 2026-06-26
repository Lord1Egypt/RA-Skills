#!/usr/bin/env python3
"""claw-reliability: FastAPI dashboard backend."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import yaml, uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from store import MetricsStore

config_path = Path(__file__).parent.parent.parent / "config.yaml"
config = yaml.safe_load(open(config_path)) if config_path.exists() else {}
base_dir = Path(__file__).parent.parent.parent
db_path = base_dir / config.get("monitoring", {}).get("db_path", "data/metrics.db")

app = FastAPI(title="🦞 claw-reliability Dashboard", version="1.0.0")
dc = config.get("dashboard", {})
_host = dc.get("host", "127.0.0.1")
_port = dc.get("port", 8777)
_origins = [f"http://{_host}:{_port}"]
if _host == "127.0.0.1":
    _origins.append(f"http://localhost:{_port}")
app.add_middleware(CORSMiddleware, allow_origins=_origins, allow_methods=["GET"], allow_headers=["*"])

def get_store(): return MetricsStore(str(db_path))

@app.get("/api/summary")
def summary():
    s = get_store()
    try: return s.get_dashboard_summary()
    finally: s.close()

@app.get("/api/tools")
def tools(hours: int = 24):
    s = get_store()
    try: return {"tools": s.get_tool_stats(hours), "period_hours": hours}
    finally: s.close()

@app.get("/api/tools/{tool_name}/failures")
def tool_failures(tool_name: str, limit: int = 20):
    s = get_store()
    try: return {"tool": tool_name, "failures": s.get_recent_tool_failures(tool_name, limit)}
    finally: s.close()

@app.get("/api/costs")
def costs(hours: int = 24):
    s = get_store()
    try: return s.get_cost_summary(hours)
    finally: s.close()

@app.get("/api/alerts")
def alerts(limit: int = 50):
    s = get_store()
    try: return {"alerts": s.get_recent_alerts(limit)}
    finally: s.close()

@app.get("/api/sessions")
def sessions():
    s = get_store()
    try: return {"sessions": s.get_session_summary()}
    finally: s.close()

@app.get("/api/timeline")
def timeline(hours: int = 24, bucket_minutes: int = 30):
    s = get_store()
    try: return {"timeline": s.get_activity_timeline(hours, bucket_minutes)}
    finally: s.close()

@app.get("/api/health")
def health(): return {"status": "ok", "service": "claw-reliability"}

frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    @app.get("/")
    def index(): return FileResponse(str(frontend_dir / "index.html"))
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

if __name__ == "__main__":
    dc = config.get("dashboard", {})
    host, port = dc.get("host", "127.0.0.1"), dc.get("port", 8777)
    print(f"🦞 claw-reliability dashboard on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
