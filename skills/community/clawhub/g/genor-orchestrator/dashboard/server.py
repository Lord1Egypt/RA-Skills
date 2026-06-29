#!/usr/bin/env python3
"""Orchestration Dashboard v3 — model CRUD, project docs, session tracking, price monitoring."""

import json, os, http.server, urllib.parse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("ORCHESTRATOR_DATA_DIR",
                          os.path.join(os.path.dirname(os.path.dirname(SKILL_DIR)), "orchestrator-data"))
PORT = int(os.environ.get("DASHBOARD_PORT", "8766"))
MODELS_FILE = os.path.join(DATA_DIR, "models.json")
CONFIG_FILE = os.path.join(DATA_DIR, "dashboard-config.json")

# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def read_file(path):
    if not os.path.exists(path): return None
    with open(path) as f: return f.read()

def load_config():
    content = read_file(CONFIG_FILE)
    if not content:
        default = {"free_only_mode": False, "theme": "dark", "auto_refresh_seconds": 30,
                   "disabled_models": [], "projects": {}}
        save_config(default)
        return default
    cfg = json.loads(content)
    cfg.setdefault("disabled_models", [])
    cfg.setdefault("projects", {})
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

def model_is_paid(m):
    return m.get("cost", {}).get("type", "") in ("subscription", "payg", "pay_per_token")

def model_is_disabled(m_id, cfg):
    return m_id in cfg.get("disabled_models", [])

def filter_models_by_config(models, cfg, project=None):
    result = list(models)
    if cfg.get("free_only_mode"):
        result = [m for m in result if not model_is_paid(m)]
    disabled = cfg.get("disabled_models", [])
    if disabled:
        result = [m for m in result if m.get("id") not in disabled]
    if project:
        proj_cfg = cfg.get("projects", {}).get(project, {})
        wl = proj_cfg.get("model_allowlist", [])
        if wl:
            result = [m for m in result if m.get("id") in wl]
        if proj_cfg.get("free_only"):
            result = [m for m in result if not model_is_paid(m)]
    return result

def model_summary(m):
    return {
        "id": m.get("id", "?"), "name": m.get("name", m.get("id", "?")),
        "provider": m.get("provider", m.get("host", "?")),
        "tier": m.get("tier", 0), "speed_rating": m.get("speed_rating", 0),
        "context_window": m.get("context_window", 0), "architecture": m.get("architecture", ""),
        "status": m.get("status", "active"), "agent_ready": m.get("agent_ready", True),
        "cost_type": m.get("cost", {}).get("type", "?"),
        "cost_amount": m.get("cost", {}).get("amount", 0),
        "cost_period": m.get("cost", {}).get("period", ""),
        "cost_limits": m.get("cost", {}).get("limits", ""),
        "cost_source": m.get("cost", {}).get("source_url", ""),
        "cost_last_checked": m.get("cost", {}).get("last_checked", ""),
        "capabilities": m.get("capabilities", {}), "user_notes": m.get("user_notes", ""),
        "research_notes": m.get("research_notes", ""),
        "research_sources": m.get("research_sources", []),
        "catalogued_by": m.get("catalogued_by", ""),
        "last_tested": m.get("last_tested", ""), "gpu": m.get("gpu", ""),
    }

# ── Project Doc CRUD ──────────────────────────────────────

def project_dir(name):
    pd = os.path.join(DATA_DIR, "projects", name)
    os.makedirs(pd, exist_ok=True)
    return pd

def _safe(name):
    return ".." not in name and "/" not in name and "\\" not in name

def list_project_docs(name):
    pd = project_dir(name)
    files = []
    for f in sorted(os.listdir(pd)):
        fp = os.path.join(pd, f)
        if os.path.isfile(fp):
            st = os.stat(fp)
            files.append({"name": f, "size": st.st_size, "modified": st.st_mtime,
                          "is_md": f.endswith(".md"), "is_json": f.endswith(".json")})
    return files

def read_project_doc(name, fn):
    if not _safe(fn): return None
    fp = os.path.join(project_dir(name), fn)
    if not os.path.exists(fp): return None
    with open(fp) as f: return f.read()

def write_project_doc(name, fn, content):
    if not _safe(fn): return False
    with open(os.path.join(project_dir(name), fn), "w") as f: f.write(content)
    return True

def delete_project_doc(name, fn):
    if not _safe(fn): return False
    fp = os.path.join(project_dir(name), fn)
    if os.path.exists(fp): os.remove(fp); return True
    return False

def get_project_state(name):
    pd = project_dir(name)
    cfg = load_config()
    proj_cfg = cfg.get("projects", {}).get(name, {})
    sessions = []
    sf = os.path.join(pd, "sessions.json")
    if os.path.exists(sf):
        try:
            with open(sf) as f: sessions = json.load(f).get("sessions", [])
        except: pass
    return {
        "name": name, "config": proj_cfg, "sessions": sessions,
        "session_count": len(sessions), "docs": list_project_docs(name),
        "state": read_project_doc(name, "STATE.md") or "",
        "roadmap": read_project_doc(name, "ROADMAP.md") or "",
        "context": read_project_doc(name, "CONTEXT.md") or "",
        "notes": read_project_doc(name, "NOTES.md") or "",
    }

# ═══════════════════════════════════════════════════════════
# DATA LOADERS
# ═══════════════════════════════════════════════════════════

def load_models_raw():
    c = read_file(MODELS_FILE)
    return json.loads(c) if c else {"models": []}

def save_models_raw(data):
    with open(MODELS_FILE, "w") as f: json.dump(data, f, indent=2, ensure_ascii=False)

def load_models(project=None):
    data = load_models_raw()
    cfg = load_config()
    filtered = filter_models_by_config(data.get("models", []), cfg, project)
    models = [model_summary(m) for m in filtered]
    active = sum(1 for m in models if m["agent_ready"] and m["status"] != "removed")
    broken = sum(1 for m in models if not m["agent_ready"])
    removed = sum(1 for m in models if m["status"] == "removed")
    return {"models": models, "total": len(models), "active": active, "broken": broken,
            "removed": removed, "free_only": cfg.get("free_only_mode", False),
            "disabled_count": len(cfg.get("disabled_models", [])), "project": project}

def parse_session_log():
    c = read_file(os.path.join(DATA_DIR, "session_log.md"))
    if not c: return {"sessions": [], "count": 0, "projects": []}
    sessions = []
    for line in c.split("\n"):
        line = line.strip()
        if line.startswith("|") and not line.startswith("|---") and not line.startswith("| Date"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 5:
                sessions.append({"date": parts[0], "project": parts[1], "task": parts[2],
                    "model": parts[3], "agent": parts[4] if len(parts) > 4 else "shell",
                    "status": parts[5] if len(parts) > 5 else "",
                    "duration": parts[6] if len(parts) > 6 else "",
                    "qa_done": "✓" in parts[7] if len(parts) > 7 else False,
                    "checked": "✓" in parts[8] if len(parts) > 8 else False,
                    "notes": parts[9] if len(parts) > 9 else ""})
    projects = list(dict.fromkeys(s["project"] for s in sessions))
    return {"sessions": sessions, "count": len(sessions), "projects": projects}

def parse_price_log():
    c = read_file(os.path.join(DATA_DIR, "price_changes.log"))
    if not c: return {"entries": [], "count": 0}
    entries = [{"text": l.strip()} for l in c.split("\n") if l.strip() and not l.startswith("#")]
    return {"entries": entries, "count": len(entries)}

def load_projects():
    pd = os.path.join(DATA_DIR, "projects")
    if not os.path.exists(pd): return {"projects": [], "count": 0}
    projects = []
    for name in sorted(os.listdir(pd)):
        pp = os.path.join(pd, name)
        if not os.path.isdir(pp): continue
        sf = os.path.join(pp, "sessions.json")
        sessions = []
        if os.path.exists(sf):
            try:
                with open(sf) as f: sessions = json.load(f).get("sessions", [])
            except: pass
        projects.append({"name": name, "session_count": len(sessions), "sessions": sessions[:5],
            "created": sessions[0]["timestamp"] if sessions else "N/A",
            "task_count": len(set(s["task"] for s in sessions))})
    return {"projects": projects, "count": len(projects)}

def enrich_projects(projects_data, cfg):
    for p in projects_data.get("projects", []):
        pc = cfg.get("projects", {}).get(p["name"], {})
        p["model_allowlist"] = pc.get("model_allowlist", [])
        p["allowlist_count"] = len(p["model_allowlist"])
        p["free_only"] = pc.get("free_only", False)
    return projects_data

# ═══════════════════════════════════════════════════════════
# HTTP HANDLER
# ═══════════════════════════════════════════════════════════

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)
        cfg = load_config()

        if path in ("/", "/index.html"):
            self.serve_file("index.html", "text/html")

        elif path == "/api/models":
            data = load_models_raw()
            project = qs.get("project", [None])[0]
            if "id" in qs:
                mid = qs["id"][0]
                for m in data.get("models", []):
                    if m.get("id") == mid:
                        ms = model_summary(m); ms["disabled"] = model_is_disabled(m["id"], cfg)
                        return self.send_json(ms)
                return self.send_error(404, json.dumps({"error": "Model not found"}))
            elif "all" in qs:
                all_m = [model_summary(m) for m in data.get("models", [])]
                for m in all_m: m["disabled"] = model_is_disabled(m["id"], cfg)
                return self.send_json({"models": all_m, "total": len(all_m)})
            else:
                return self.send_json(load_models(project=project))

        elif path == "/api/sessions":
            self.send_json(parse_session_log())

        elif path == "/api/prices":
            self.send_json(parse_price_log())

        elif path == "/api/projects":
            result = load_projects()
            self.send_json(enrich_projects(result, cfg))

        elif path == "/api/project-state":
            name = qs.get("name", [None])[0]
            if not name: return self.send_error(400, json.dumps({"error": "Missing name"}))
            self.send_json(get_project_state(name))

        elif path == "/api/project-doc":
            name = qs.get("name", [None])[0]
            fn = qs.get("file", [None])[0]
            if not name or not fn: return self.send_error(400, json.dumps({"error": "Missing name or file"}))
            content = read_project_doc(name, fn)
            if content is None: return self.send_error(404, json.dumps({"error": "Not found"}))
            self.send_json({"content": content, "name": name, "file": fn})

        elif path == "/api/status":
            pl = os.path.exists(os.path.join(DATA_DIR, "price_changes.log"))
            self.send_json({"nightly_price_check": "Configured (2 AM)" if pl else "Not configured",
                "price_log_exists": pl, "data_dir": DATA_DIR,
                "free_only_mode": cfg.get("free_only_mode", False),
                "disabled_models": len(cfg.get("disabled_models", [])),
                "projects_configured": len(cfg.get("projects", {}))})

        elif path == "/api/config":
            self.send_json(cfg)

        elif path == "/api/all":
            projects = load_projects()
            projects = enrich_projects(projects, cfg)
            self.send_json({"sessions": parse_session_log(), "models": load_models(),
                "prices": parse_price_log(), "projects": projects, "config": cfg,
                "status": {"nightly_price_check": "Configured (2 AM)",
                    "price_log_exists": os.path.exists(os.path.join(DATA_DIR, "price_changes.log")),
                    "data_dir": DATA_DIR, "free_only_mode": cfg.get("free_only_mode", False),
                    "disabled_models": len(cfg.get("disabled_models", [])),
                    "projects_configured": len(cfg.get("projects", {}))}})
        else:
            self.send_error(404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        cl = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(cl)

        try: data = json.loads(body)
        except: return self.send_error(400, json.dumps({"error": "Invalid JSON"}))

        if path == "/api/project-doc":
            name = data.get("name"); fn = data.get("file"); content = data.get("content", "")
            if not name or not fn: return self.send_error(400, json.dumps({"error": "Missing name or file"}))
            if write_project_doc(name, fn, content):
                self.send_json({"ok": True, "action": "saved", "name": name, "file": fn})
            else:
                self.send_error(400, json.dumps({"error": "Invalid filename"}))

        elif path == "/api/project-state":
            name = data.get("name")
            if not name: return self.send_error(400, json.dumps({"error": "Missing name"}))
            project_dir(name)
            if "config" in data:
                cfg = load_config()
                cfg.setdefault("projects", {})
                cfg["projects"].setdefault(name, {})
                cfg["projects"][name].update(data["config"])
                save_config(cfg)
            self.send_json({"ok": True, "action": "created", "name": name})

        elif path == "/api/config":
            cfg = load_config()
            for key in ("free_only_mode", "theme", "auto_refresh_seconds", "disabled_models"):
                if key in data: cfg[key] = data[key]
            if "projects" in data and isinstance(data["projects"], dict):
                for pn, pc in data["projects"].items():
                    cfg["projects"].setdefault(pn, {"model_allowlist": [], "free_only": False})
                    if "model_allowlist" in pc: cfg["projects"][pn]["model_allowlist"] = pc["model_allowlist"]
                    if "free_only" in pc: cfg["projects"][pn]["free_only"] = pc["free_only"]
            save_config(cfg)
            self.send_json({"ok": True, "config": cfg})

        elif path == "/api/models":
            model_id = data.get("id")
            if not model_id: return self.send_error(400, json.dumps({"error": "Missing id"}))
            mdata = load_models_raw()
            found_idx = None
            for i, m in enumerate(mdata.get("models", [])):
                if m.get("id") == model_id: found_idx = i; break
            if found_idx is not None:
                existing = mdata["models"][found_idx]
                for key, val in data.items():
                    if key == "cost" and isinstance(val, dict) and isinstance(existing.get("cost"), dict):
                        existing["cost"].update(val)
                    elif key == "capabilities" and isinstance(val, dict) and isinstance(existing.get("capabilities"), dict):
                        existing["capabilities"].update(val)
                    else: existing[key] = val
                mdata["models"][found_idx] = existing
                save_models_raw(mdata)
                ms = model_summary(existing); ms["disabled"] = model_is_disabled(existing["id"], load_config())
                self.send_json({"ok": True, "action": "updated", "model": ms})
            else:
                mdata.setdefault("models", []).append(data)
                save_models_raw(mdata)
                ms = model_summary(data); ms["disabled"] = model_is_disabled(data.get("id", ""), load_config())
                self.send_json({"ok": True, "action": "created", "model": ms})
        else:
            self.send_error(404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if path == "/api/models" and "id" in qs:
            mid = qs["id"][0]
            data = load_models_raw()
            orig = len(data.get("models", []))
            data["models"] = [m for m in data.get("models", []) if m.get("id") != mid]
            if len(data["models"]) < orig:
                save_models_raw(data)
                self.send_json({"ok": True, "action": "deleted", "id": mid})
            else:
                self.send_error(404, json.dumps({"error": "Not found"}))

        elif path == "/api/project-doc":
            name = qs.get("name", [None])[0]
            fn = qs.get("file", [None])[0]
            if not name or not fn: return self.send_error(400, json.dumps({"error": "Missing name or file"}))
            if delete_project_doc(name, fn):
                self.send_json({"ok": True, "action": "deleted", "name": name, "file": fn})
            else:
                self.send_error(404, json.dumps({"error": "Not found or invalid"}))
        else:
            self.send_error(404)

    def serve_file(self, name, ct):
        p = os.path.join(os.path.dirname(__file__), name)
        if not os.path.exists(p): return self.send_error(404)
        with open(p) as f: c = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(c.encode())

    def send_json(self, d):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(d, indent=2, ensure_ascii=False).encode())

    def send_error(self, code, body=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if body: self.wfile.write(body.encode() if isinstance(body, str) else body)
        else: self.wfile.write(json.dumps({"error": f"HTTP {code}"}).encode())

    def log_message(self, fmt, *a): print(f"[Dash] {a[0]} {a[1]} {a[2]}")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    print(f"Dashboard v3 — http://localhost:{PORT}  Data: {DATA_DIR}")
    s = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    try: s.serve_forever()
    except KeyboardInterrupt: print("\nStopped."); s.server_close()
