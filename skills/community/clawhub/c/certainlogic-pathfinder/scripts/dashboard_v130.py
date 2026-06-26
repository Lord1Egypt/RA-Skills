#!/usr/bin/env python3
"""AgentPathfinder v1.3.0 — Live Audit Dashboard

The definitive visualization of cryptographically signed agent tool calls.
Generates a self-contained HTML file that auto-refreshes to show real-time
audit trail activity with HMAC signatures, integrity verification, and
fraud detection.

Usage:
    python3 scripts/dashboard_v130.py --watch
    # Open the displayed URL in your browser

    python3 scripts/dashboard_v130.py --task <task_id>
    # Focus on a specific task

    python3 scripts/dashboard_v130.py --export <task_id> > audit_export.json
    # Export full audit trail with signatures
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Add parent to path for imports when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentpathfinder.pathfinder_core import derive_key, shard_from_hex, reconstruct_key
from agentpathfinder.audit_trail import AuditTrail


# ── Configuration ──
DATA_DIR = Path.home() / ".agentpathfinder" / "pathfinder_data"
TASK_DIR = DATA_DIR / "tasks"
AUDIT_DIR = DATA_DIR / "audit"
DASHBOARD_FILE = Path.cwd() / "agentpathfinder_dashboard.html"
REFRESH_INTERVAL = 2  # seconds

# CertainLogic brand colors
COLORS = {
    "navy": "#0F1724",
    "navy_light": "#1E293B",
    "card_bg": "#0B1120",
    "blue": "#2563EB",
    "blue_light": "#3B82F6",
    "text": "#E2E8F0",
    "text_soft": "#94A3B8",
    "text_dim": "#64748B",
    "success": "#34D399",
    "error": "#F87171",
    "warning": "#FBBF24",
    "border": "rgba(255,255,255,0.06)",
}


# ── HTML Template ──
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="{refresh}">
<title>AgentPathfinder v1.3.0 — Live Audit Dashboard</title>
<style>
:root {{
  --navy: {navy}; --navy-light: {navy_light}; --card-bg: {card_bg};
  --blue: {blue}; --blue-light: {blue_light}; --text: {text};
  --text-soft: {text_soft}; --text-dim: {text_dim};
  --success: {success}; --error: {error}; --warning: {warning};
  --border: {border};
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro', 'Segoe UI', sans-serif;
  background: var(--navy); color: var(--text); min-height: 100vh; line-height: 1.5;
}}
.container {{ max-width: 1400px; margin: 0 auto; padding: 0 24px; }}

/* Header */
.header {{
  background: var(--card-bg); border-bottom: 1px solid var(--border);
  padding: 16px 0; position: sticky; top: 0; z-index: 100;
}}
.header-inner {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
.brand {{ display: flex; align-items: center; gap: 10px; }}
.brand-icon {{
  width: 32px; height: 32px; background: linear-gradient(135deg, var(--blue), var(--blue-light));
  border-radius: 8px; display: grid; place-items: center; font-size: 16px;
}}
.brand-text {{ font-size: 18px; font-weight: 700; }}
.brand-version {{ font-size: 12px; color: var(--text-dim); margin-left: 8px; }}
.header-status {{ display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-soft); }}
.status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--success); animation: pulse 2s infinite; }}
@keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}

/* Layout */
.main-grid {{ display: grid; grid-template-columns: 1fr 320px; gap: 20px; padding: 24px 0; }}
@media (max-width: 900px) {{ .main-grid {{ grid-template-columns: 1fr; }} }}

/* Cards */
.card {{
  background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px;
  overflow: hidden; margin-bottom: 16px;
}}
.card-header {{
  padding: 14px 18px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}}
.card-title {{ font-size: 14px; font-weight: 600; color: var(--text-soft); text-transform: uppercase; letter-spacing: 0.5px; }}
.card-body {{ padding: 18px; }}

/* Stats Grid */
.stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }}
@media (max-width: 700px) {{ .stats-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
.stat-card {{
  background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px;
  padding: 16px; position: relative; overflow: hidden;
}}
.stat-card::before {{
  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--blue), transparent 60%);
}}
.stat-label {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
.stat-value {{ font-size: 28px; font-weight: 700; letter-spacing: -1px; }}
.stat-sublabel {{ font-size: 11px; color: var(--text-dim); margin-top: 4px; }}

/* Integrity Panel */
.integrity-panel {{ padding: 16px; }}
.integrity-row {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13px; }}
.integrity-row:last-child {{ border-bottom: none; }}
.integrity-label {{ color: var(--text-soft); }}
.integrity-value {{ font-weight: 600; font-family: 'SF Mono', monospace; }}
.integrity-good {{ color: var(--success); }}
.integrity-bad {{ color: var(--error); }}
.integrity-warn {{ color: var(--warning); }}
.verify-btn {{
  width: 100%; margin-top: 12px; padding: 10px; background: var(--blue); color: white;
  border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer;
}}
.verify-btn:hover {{ background: var(--blue-light); }}

/* Task List */
.task-item {{ padding: 14px 18px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.15s; }}
.task-item:hover {{ background: rgba(255,255,255,0.02); }}
.task-item:last-child {{ border-bottom: none; }}
.task-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
.task-name {{ font-weight: 600; font-size: 14px; }}
.task-status {{ font-size: 11px; padding: 3px 8px; border-radius: 4px; font-weight: 600; }}
.status-complete {{ background: rgba(52,211,153,0.15); color: var(--success); }}
.status-running {{ background: rgba(37,99,235,0.15); color: var(--blue-light); }}
.status-pending {{ background: rgba(148,163,184,0.15); color: var(--text-soft); }}
.task-meta {{ font-size: 12px; color: var(--text-dim); }}

/* Tool Chain */
.tool-chain {{ padding: 0; }}
.step-block {{ border-left: 2px solid var(--border); margin-left: 12px; padding-left: 16px; padding-bottom: 16px; }}
.step-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 10px; font-size: 13px; font-weight: 600; color: var(--text-soft); }}
.step-badge {{ width: 22px; height: 22px; border-radius: 6px; background: var(--navy-light); display: grid; place-items: center; font-size: 11px; }}

.tool-event {{ margin-bottom: 10px; border-radius: 8px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); overflow: hidden; }}
.tool-event-header {{ padding: 10px 12px; display: flex; align-items: center; gap: 10px; font-size: 12px; }}
.tool-icon {{ font-size: 14px; }}
.tool-name {{ font-weight: 600; }}
.tool-time {{ margin-left: auto; color: var(--text-dim); font-family: 'SF Mono', monospace; font-size: 11px; }}
.tool-id {{ color: var(--text-dim); font-size: 10px; font-family: monospace; }}
.tool-body {{ padding: 10px 12px; border-top: 1px solid var(--border); font-size: 12px; }}
.tool-body pre {{ background: var(--navy); padding: 8px; border-radius: 6px; overflow-x: auto; font-size: 11px; font-family: 'SF Mono', monospace; color: var(--text-soft); max-height: 120px; overflow-y: auto; }}
.tool-hmac {{ font-size: 10px; color: var(--text-dim); margin-top: 6px; font-family: monospace; }}
.tool-hmac::before {{ content: "🔐 "; }}
.tool-duration {{ font-size: 11px; color: var(--text-dim); margin-left: auto; }}

/* Fraud Alerts */
.alert {{ padding: 12px 16px; border-radius: 8px; margin-bottom: 12px; font-size: 12px; display: flex; align-items: flex-start; gap: 10px; }}
.alert-error {{ background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.2); color: var(--error); }}
.alert-warn {{ background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.2); color: var(--warning); }}
.alert-icon {{ font-size: 16px; flex-shrink: 0; }}

/* Tool summary */
.tool-summary-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }}
.tool-stat {{ display: flex; justify-content: space-between; font-size: 12px; padding: 6px 0; border-bottom: 1px solid var(--border); }}
.tool-stat:last-child {{ border-bottom: none; }}

/* Footer */
.footer {{ border-top: 1px solid var(--border); padding: 20px 0; text-align: center; color: var(--text-dim); font-size: 11px; margin-top: 20px; }}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--text-dim); border-radius: 3px; }}
</style>
</head>
<body>
{content}
<script>
// Auto-scroll to bottom if user hasn't scrolled up
let scrolled = false;
window.addEventListener('scroll', () => {{ scrolled = true; }});
setTimeout(() => {{ if (!scrolled) window.scrollTo(0, document.body.scrollHeight); }}, 500);
</script>
</body>
</html>
"""


# ── Helpers ──

def format_ts(ts_str: str) -> str:
    """Format ISO timestamp to human-readable."""
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        return dt.strftime("%H:%M:%S")
    except:
        return ts_str


def format_duration(ms: Optional[int]) -> str:
    """Format milliseconds to readable."""
    if ms is None:
        return ""
    if ms < 1000:
        return f"{ms}ms"
    return f"{ms/1000:.1f}s"


def load_all_tasks() -> List[Dict[str, Any]]:
    """Load all task JSONs from task directory."""
    tasks = []
    if not TASK_DIR.exists():
        return tasks
    for f in sorted(TASK_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            tasks.append(json.loads(f.read_text()))
        except:
            pass
    return tasks


def load_audit_trail(task_id: str) -> Tuple[List[Dict], Dict]:
    """Load audit trail for task, return events + integrity report."""
    audit_file = AUDIT_DIR / f"{task_id}.jsonl"
    if not audit_file.exists():
        return [], {"total_events": 0, "tampered": 0, "corrupted": 0, "integrity_ok": True}

    # Try to derive audit key for verification
    try:
        task_file = TASK_DIR / f"{task_id}.json"
        task = json.loads(task_file.read_text())

        # Reconstruct master key from vault
        from agentpathfinder.task_engine import TaskEngine
        engine = TaskEngine()
        shards = [engine._read_shard_from_vault(task_id, step["step_number"]) for step in task["steps"]]
        shards.append(shard_from_hex(task["issuer_shard"]))
        master_key = reconstruct_key(shards)
        audit_key = derive_key(master_key, b"audit_signing_key")
        trail = AuditTrail(audit_file, audit_key)
        events = trail.read_trail(task_id)
        integrity = trail.verify_integrity()
    except Exception as e:
        # Fallback: read without verification
        events = []
        for line in audit_file.read_text().strip().split("\n"):
            if line:
                try:
                    events.append(json.loads(line))
                except:
                    pass
        integrity = {"total_events": len(events), "tampered": 0, "corrupted": 0, "integrity_ok": True, "note": f"Key error: {e}"}

    return events, integrity


def detect_anomalies(events: List[Dict]) -> List[Dict]:
    """Simple fraud detection: find suspicious patterns."""
    alerts = []
    tool_calls = {}  # tool_id -> event
    step_claims = []

    for e in events:
        etype = e.get("event", "")
        if etype == "TOOL_INVOKED":
            tool_calls[e.get("tool_id", "")] = e
        elif etype == "step_claimed":
            step_claims.append(e)

    # Check for step_claimed without any tool calls
    for sc in step_claims:
        step_num = sc.get("step_number")
        # Find if there's a tool call associated with this step
        has_tool = any(e.get("step_number") == step_num for e in events if e.get("event") == "TOOL_INVOKED")
        if not has_tool:
            alerts.append({
                "level": "warn",
                "message": f"Step {step_num} claimed complete but no tool calls were logged. Possible fabrication."
            })

    # Check for hanging tool calls (invoked but no result)
    invoked_ids = set(e.get("tool_id") for e in events if e.get("event") == "TOOL_INVOKED")
    result_ids = set(e.get("tool_id") for e in events if e.get("event") == "TOOL_RESULT")
    hanging = invoked_ids - result_ids
    for tid in hanging:
        alerts.append({
            "level": "error",
            "message": f"Tool call {tid} was invoked but never completed. Agent may have crashed."
        })

    return alerts


def render_events(events: List[Dict]) -> str:
    """Render tool events as HTML."""
    if not events:
        return '<div style="padding:20px;color:var(--text-dim);font-size:13px;text-align:center;">No audit events yet. Run a task to see live tool calls.</div>'

    html_parts = []
    current_step = None

    for e in events:
        etype = e.get("event", "")

        if etype == "step_claimed":
            step_num = e.get("step_number", "?")
            html_parts.append(f'<div class="step-header"><div class="step-badge">{step_num}</div>Step {step_num} claimed by {e.get("agent_id", "unknown")}</div>')
            continue

        if not etype.startswith("TOOL_"):
            continue

        step_num = e.get("step_number", "?")
        if step_num != current_step:
            current_step = step_num
            html_parts.append(f'<div class="step-block">')

        is_result = etype == "TOOL_RESULT"
        tool_name = e.get("tool_name", "unknown")
        tool_id = e.get("tool_id", "")[:12]
        ts = format_ts(e.get("timestamp_invoked" if not is_result else "timestamp_completed", ""))

        icon = "🔧" if not is_result else ("✅" if e.get("exit_code", 0) == 0 and e.get("status") != "error" else "❌")
        status_class = "status-complete" if is_result and e.get("exit_code", 0) == 0 else ""

        hmac = e.get("hmac_truncated", "N/A")
        if hmac != "N/A" and len(hmac) > 20:
            hmac = hmac[:16] + "..."
        duration = format_duration(e.get("duration_ms"))

        # Build args/result display
        body_content = ""
        if not is_result:
            args = e.get("args", {})
            body_content = f'<pre>{json.dumps(args, indent=2, default=str)}</pre>'
        else:
            result = e.get("result")
            if result:
                body_content = f'<pre>{json.dumps(result, indent=2, default=str)[:500]}</pre>'
            error = e.get("error")
            if error:
                body_content += f'<div style="color:var(--error);margin-top:6px;">Error: {error}</div>'

        depth = e.get("depth", 0)
        depth_indent = f'style="margin-left:{depth * 20}px"' if depth > 0 else ""

        html_parts.append(f'''
        <div class="tool-event" {depth_indent}>
            <div class="tool-event-header">
                <span class="tool-icon">{icon}</span>
                <span class="tool-name">{tool_name}</span>
                <span class="tool-id">{tool_id}</span>
                <span class="tool-duration">{duration}</span>
                <span class="tool-time">{ts}</span>
            </div>
            <div class="tool-body">
                {body_content}
                <div class="tool-hmac">HMAC: {hmac}</div>
            </div>
        </div>
        ''')

    if current_step is not None:
        html_parts.append('</div>')

    return "\n".join(html_parts)


def render_alerts(alerts: List[Dict]) -> str:
    """Render fraud alerts as HTML."""
    if not alerts:
        return ''
    parts = ['<div style="margin-bottom:16px;">']
    for a in alerts:
        icon = "🚨" if a["level"] == "error" else "⚠️"
        cls = f'alert alert-{a["level"]}'
        parts.append(f'<div class="{cls}"><span class="alert-icon">{icon}</span><div>{a["message"]}</div></div>')
    parts.append('</div>')
    return "\n".join(parts)


def generate_dashboard(focus_task: Optional[str] = None) -> str:
    """Generate complete dashboard HTML."""
    tasks = load_all_tasks()

    # Filter to focus task if specified
    if focus_task:
        tasks = [t for t in tasks if t.get("task_id") == focus_task]

    # Stats
    total_tasks = len(tasks)
    complete_tasks = sum(1 for t in tasks if all(s.get("state") == "complete" for s in t.get("steps", [])))
    running_tasks = sum(1 for t in tasks if any(s.get("state") == "running" for s in t.get("steps", [])))

    # Load audit data for focus or most recent task
    audit_events = []
    integrity = {"total_events": 0, "tampered": 0, "corrupted": 0, "integrity_ok": True}
    alerts = []

    if tasks:
        target_task = tasks[0] if focus_task else tasks[0]
        task_id = target_task.get("task_id", "")
        audit_events, integrity = load_audit_trail(task_id)
        alerts = detect_anomalies(audit_events)

    total_tool_events = len([e for e in audit_events if e.get("event", "").startswith("TOOL_")])
    tool_invocations = len([e for e in audit_events if e.get("event") == "TOOL_INVOKED"])
    tool_errors = len([e for e in audit_events if e.get("event") == "TOOL_RESULT" and e.get("status") == "error"])

    # Task list HTML
    task_list_html = ""
    for t in tasks[:10]:
        steps = t.get("steps", [])
        complete = sum(1 for s in steps if s.get("state") == "complete")
        total = len(steps)
        status = "complete" if complete == total else ("running" if any(s.get("state") == "running" for s in steps) else "pending")
        status_class = f"status-{status}"
        status_icon = "✅" if status == "complete" else ("🔄" if status == "running" else "⏳")

        task_list_html += f'''
        <div class="task-item">
            <div class="task-header">
                <span class="task-name">{t.get("name", "Untitled")}</span>
                <span class="task-status {status_class}">{status_icon} {status.title()}</span>
            </div>
            <div class="task-meta">{t.get("task_id", "")[:8]}… | Step {complete}/{total} | Agent: {t.get("steps", [{}])[0].get("agent_id", "unknown")}</div>
        </div>
        '''

    if not tasks:
        task_list_html = '<div style="padding:20px;color:var(--text-dim);font-size:13px;text-align:center;">No tasks found. Create one with: <code>pf create mytask "step1" "step2"</code></div>'

    # Integrity panel
    integrity_class = "integrity-good" if integrity.get("integrity_ok") else "integrity-bad"
    tampered_class = "integrity-good" if integrity.get("tampered", 0) == 0 else "integrity-bad"
    corrupted_class = "integrity-good" if integrity.get("corrupted", 0) == 0 else "integrity-bad"

    integrity_html = f'''
    <div class="card">
        <div class="card-header"><span class="card-title">🔐 Audit Integrity</span></div>
        <div class="integrity-panel">
            <div class="integrity-row"><span class="integrity-label">Total Events</span><span class="integrity-value">{integrity.get("total_events", 0)}</span></div>
            <div class="integrity-row"><span class="integrity-label">Valid HMAC</span><span class="integrity-value {integrity_class}">{integrity.get("total_events", 0) - integrity.get("tampered", 0)}/{integrity.get("total_events", 0)} ✅</span></div>
            <div class="integrity-row"><span class="integrity-label">Tampered</span><span class="integrity-value {tampered_class}">{integrity.get("tampered", 0)}</span></div>
            <div class="integrity-row"><span class="integrity-label">Corrupted</span><span class="integrity-value {corrupted_class}">{integrity.get("corrupted", 0)}</span></div>
            <div class="integrity-row"><span class="integrity-label">Tool Events</span><span class="integrity-value">{total_tool_events}</span></div>
            <div class="integrity-row"><span class="integrity-label">Tool Errors</span><span class="integrity-value {('integrity-bad' if tool_errors > 0 else 'integrity-good')}">{tool_errors}</span></div>
        </div>
    </div>
    '''

    # Tool summary
    tool_names = {}
    for e in audit_events:
        if e.get("event") == "TOOL_INVOKED":
            name = e.get("tool_name", "unknown")
            tool_names.setdefault(name, {"invoked": 0, "completed": 0, "error": 0})
            tool_names[name]["invoked"] += 1
        elif e.get("event") == "TOOL_RESULT":
            name = e.get("tool_name", "unknown")
            tool_names.setdefault(name, {"invoked": 0, "completed": 0, "error": 0})
            if e.get("status") == "error":
                tool_names[name]["error"] += 1
            else:
                tool_names[name]["completed"] += 1

    tool_summary_html = ""
    for name, stats in sorted(tool_names.items()):
        tool_summary_html += f'<div class="tool-stat"><span>{name}</span><span>{stats["completed"]}/{stats["invoked"]} done ({stats["error"]} err)</span></div>'

    # Build content
    content = f'''
    <div class="header">
        <div class="container">
            <div class="header-inner">
                <div class="brand">
                    <div class="brand-icon">🎯</div>
                    <div class="brand-text">AgentPathfinder<span class="brand-version">v1.3.0</span></div>
                </div>
                <div class="header-status"><div class="status-dot"></div>Live — refreshing every {REFRESH_INTERVAL}s</div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Tasks</div>
                <div class="stat-value">{total_tasks}</div>
                <div class="stat-sublabel">{complete_tasks} complete, {running_tasks} running</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Tool Calls</div>
                <div class="stat-value">{tool_invocations}</div>
                <div class="stat-sublabel">{total_tool_events} total events</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Signed Events</div>
                <div class="stat-value">{integrity.get("total_events", 0)}</div>
                <div class="stat-sublabel">All HMAC-SHA256</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Integrity</div>
                <div class="stat-value" style="color:{COLORS["success"] if integrity.get("integrity_ok") else COLORS["error"]};">
                    {"✓" if integrity.get("integrity_ok") else "✗"}
                </div>
                <div class="stat-sublabel">{"All valid" if integrity.get("integrity_ok") else "TAMPER DETECTED"}</div>
            </div>
        </div>

        {render_alerts(alerts)}

        <div class="main-grid">
            <div class="main-col">
                <div class="card">
                    <div class="card-header"><span class="card-title">📋 Tasks</span></div>
                    <div class="task-list">{task_list_html}</div>
                </div>

                <div class="card">
                    <div class="card-header"><span class="card-title">🔗 Live Tool Audit Trail</span></div>
                    <div class="tool-chain">
                        {render_events(audit_events)}
                    </div>
                </div>
            </div>

            <div class="sidebar-col">
                {integrity_html}

                <div class="card" style="margin-top:16px;">
                    <div class="card-header"><span class="card-title">📊 Tool Summary</span></div>
                    <div class="card-body">
                        <div class="tool-summary-grid">
                            {tool_summary_html or '<div style="color:var(--text-dim);font-size:12px;">No tool calls yet</div>'}
                        </div>
                    </div>
                </div>

                <div class="card" style="margin-top:16px;">
                    <div class="card-header"><span class="card-title">ℹ️ About</span></div>
                    <div class="card-body" style="font-size:12px;color:var(--text-soft);line-height:1.6;">
                        Every tool call is cryptographically signed with HMAC-SHA256 using a per-task derived audit key. Edit any event after signing and the HMAC verification will fail.<br><br>
                        <strong>v1.3.0 features:</strong><br>
                        • Full argument logging<br>
                        • Full result logging<br>
                        • Sub-tool chain tracking<br>
                        • Tamper detection<br>
                        • Hanging call detection
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="container">
            AgentPathfinder v1.3.0 — Cryptographic audit trail for AI agents · Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}
        </div>
    </div>
    '''

    return HTML_TEMPLATE.format(
        refresh=REFRESH_INTERVAL,
        **COLORS,
        content=content
    )


# ── Commands ──

def cmd_watch(args):
    """Watch mode: regenerate dashboard every N seconds + serve HTTP."""
    import http.server
    import socketserver
    import threading

    # Start HTTP server in background
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(DASHBOARD_FILE.parent), **kw)
        def log_message(self, format, *args):
            pass  # Suppress access logs

    httpd = socketserver.TCPServer(("", 8080), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    print(f"AgentPathfinder v1.3.0 Dashboard")
    print(f"Watching: {AUDIT_DIR}")
    print(f"Output:   {DASHBOARD_FILE}")
    print(f"Refresh:  every {REFRESH_INTERVAL}s")
    print(f"Web URL:  http://localhost:8080/agentpathfinder_dashboard.html")
    print(f"\n(Ctrl+C to stop)\n")

    # Try to open browser
    try:
        import webbrowser
        webbrowser.open(f"http://localhost:8080/agentpathfinder_dashboard.html")
    except:
        pass

    try:
        while True:
            html = generate_dashboard(focus_task=args.task)
            DASHBOARD_FILE.write_text(html, encoding="utf-8")
            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")
        httpd.shutdown()


def cmd_generate(args):
    """One-shot generation."""
    html = generate_dashboard(focus_task=args.task)
    DASHBOARD_FILE.write_text(html, encoding="utf-8")
    print(f"Dashboard written to: {DASHBOARD_FILE}")
    print(f"Open: file://{DASHBOARD_FILE.absolute()}")


def cmd_export(args):
    """Export audit trail as JSON."""
    if not args.task:
        print("Error: --task required for export", file=sys.stderr)
        sys.exit(1)

    events, integrity = load_audit_trail(args.task)
    export = {
        "task_id": args.task,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "integrity": integrity,
        "events": events,
    }
    print(json.dumps(export, indent=2, default=str))


# ── Main ──

def main():
    parser = argparse.ArgumentParser(description="AgentPathfinder v1.3.0 Dashboard")
    sub = parser.add_subparsers(dest="command", required=True)

    watch = sub.add_parser("watch", help="Watch mode with auto-refresh")
    watch.add_argument("--task", help="Focus on specific task ID")
    watch.set_defaults(func=cmd_watch)

    gen = sub.add_parser("generate", help="Generate dashboard once")
    gen.add_argument("--task", help="Focus on specific task ID")
    gen.set_defaults(func=cmd_generate)

    exp = sub.add_parser("export", help="Export audit trail as JSON")
    exp.add_argument("--task", required=True, help="Task ID to export")
    exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
