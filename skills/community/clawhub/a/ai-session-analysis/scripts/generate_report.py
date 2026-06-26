#!/usr/bin/env python3
"""Generate an HTML report from AI coding session data.

Reads Claude Code, Codex, and Kimi Code session data directly from
their source paths and outputs a self-contained HTML file with
Chart.js visualizations.

Usage: python3 generate_report.py [output_path]
  Default output: ./ai-session-report.html
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import classify_shell_cmd, strip_home_prefix  # noqa: E402

HOME = Path.home()
NOW = datetime.now(timezone.utc)
RECENT_DAYS = 7  # default, overridden by --days
recent_cutoff = NOW - timedelta(days=RECENT_DAYS)


# ═══════════════════════════════════════════════════════════════
# Data Extraction
# ═══════════════════════════════════════════════════════════════


def extract_claude():
    """Extract all Claude Code statistics."""
    projects_dir = HOME / ".claude" / "projects"
    jsonl_files = list(projects_dir.rglob("*.jsonl")) if projects_dir.exists() else []

    tool_counts = Counter()
    daily_tools = Counter()
    projects = Counter()
    shell_cmds = []
    read_files = []
    write_files = []
    edit_files = []
    edit_sizes = []
    session_info = {}
    token_in = 0
    token_out = 0
    token_cache = 0
    failures = Counter()
    hour_bins = Counter()
    user_msg_count = 0
    sessions_with_tools = set()
    parse_errors = 0

    # Recent 7-day (collected in same pass)
    recent_daily = Counter()
    recent_projects = Counter()
    recent_tools = Counter()
    recent_sessions_set = set()

    session_epoch_ms = {}  # for scatter chart x-axis
    for jf in jsonl_files:
        sid = jf.stem
        proj = strip_home_prefix(str(jf.relative_to(projects_dir).parts[0]))
        first_ts = None
        last_ts = None
        tool_count = 0

        try:
            for line in jf.read_text().strip().splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                ts_str = d.get("timestamp", "")
                dt = None
                local_dt = None
                if ts_str:
                    try:
                        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        local_dt = dt.astimezone()  # convert to local time
                    except Exception:
                        pass

                typ = d.get("type", "")

                if typ == "user":
                    msg = d.get("message", {})
                    content = msg.get("content", "")
                    if isinstance(content, str) and content.strip():
                        user_msg_count += 1
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_result":
                                if block.get("is_error"):
                                    failures["tool_error"] += 1

                elif typ == "assistant":
                    content = d.get("message", {}).get("content", [])
                    if not isinstance(content, list):
                        continue

                    usage = d.get("message", {}).get("usage", {})
                    if usage:
                        token_in += usage.get("input_tokens", 0) or 0
                        token_out += usage.get("output_tokens", 0) or 0
                        token_cache += usage.get("cache_read_input_tokens", 0) or 0

                    for block in content:
                        if not isinstance(block, dict) or block.get("type") != "tool_use":
                            continue
                        tn = block.get("name", "?")
                        tool_counts[tn] += 1
                        projects[proj] += 1
                        tool_count += 1
                        sessions_with_tools.add(sid)

                        if local_dt:
                            date_key = local_dt.strftime("%Y-%m-%d")
                            daily_tools[date_key] += 1
                            hour_bins[local_dt.hour] += 1
                            if first_ts is None:
                                first_ts = local_dt
                                session_epoch_ms[sid] = int(local_dt.timestamp() * 1000)
                            last_ts = local_dt

                            if local_dt >= recent_cutoff:
                                recent_tools[tn] += 1
                                recent_projects[proj] += 1
                                recent_daily[date_key] += 1
                                recent_sessions_set.add(sid)

                        inp = block.get("input", {})
                        if not isinstance(inp, dict):
                            continue

                        if tn == "Bash":
                            cmd = inp.get("command", "")
                            if cmd:
                                shell_cmds.append(cmd)
                        elif tn == "Read":
                            read_files.append(inp.get("file_path", ""))
                        elif tn == "Write":
                            write_files.append(inp.get("file_path", ""))
                        elif tn == "Edit":
                            fp = inp.get("file_path", "")
                            edit_files.append(fp)
                            old_s = inp.get("old_string", "")
                            new_s = inp.get("new_string", "")
                            edit_sizes.append({
                                "file": fp,
                                "old_len": len(old_s),
                                "new_len": len(new_s),
                                "diff": len(new_s) - len(old_s),
                            })

        except Exception:
            parse_errors += 1

        if first_ts:
            session_info[sid] = {
                "first_ts": first_ts.isoformat(),
                "last_ts": last_ts.isoformat() if last_ts else first_ts.isoformat(),
                "duration_min": round((last_ts - first_ts).total_seconds() / 60, 1) if last_ts else 0,
                "project": proj,
                "tool_count": tool_count,
            }

    dates = sorted(daily_tools.keys())
    shell_cats = Counter()
    for cmd in shell_cmds:
        shell_cats[classify_shell_cmd(cmd)] += 1

    file_exts = Counter()
    for fp in read_files:
        ext = Path(fp).suffix if fp else "?"
        file_exts[ext or "(none)"] += 1

    durations = [v["duration_min"] for v in session_info.values() if v["duration_min"] > 0]
    dur_bins = {"<5min": 0, "5-15min": 0, "15-30min": 0, "30-60min": 0, "1-2hr": 0, "2hr+": 0}
    for d in durations:
        if d < 5:
            dur_bins["<5min"] += 1
        elif d < 15:
            dur_bins["5-15min"] += 1
        elif d < 30:
            dur_bins["15-30min"] += 1
        elif d < 60:
            dur_bins["30-60min"] += 1
        elif d < 120:
            dur_bins["1-2hr"] += 1
        else:
            dur_bins["2hr+"] += 1

    total_edit_diff = sum(e["diff"] for e in edit_sizes)

    return {
        "sessions": len(session_info),
        "sessions_with_tools": len(sessions_with_tools),
        "messages": user_msg_count,
        "tools": sum(tool_counts.values()),
        "tool_types": len(tool_counts),
        "tool_names": dict(tool_counts.most_common(20)),
        "daily": {d: daily_tools[d] for d in dates},
        "dates": dates,
        "projects": dict(projects.most_common(12)),
        "shell_categories": dict(shell_cats.most_common()),
        "shell_total": len(shell_cmds),
        "read_count": len(read_files),
        "write_count": len(write_files),
        "edit_count": len(edit_files),
        "file_types": dict(file_exts.most_common(10)),
        "token_in": token_in,
        "token_out": token_out,
        "token_cache": token_cache,
        "cache_hit_pct": round(token_cache / (token_in + token_cache) * 100, 1) if (token_in + token_cache) > 0 else 0,
        "hour_bins": {str(h): hour_bins[h] for h in range(24)},
        "duration_bins": dur_bins,
        "avg_duration_min": round(sum(durations) / len(durations), 1) if durations else 0,
        "failure_count": sum(failures.values()),
        "parse_errors": parse_errors,
        "total_edit_diff": total_edit_diff,
        "edit_count_total": len(edit_sizes),
        # Recent
        "recent_daily": dict(sorted(recent_daily.items())),
        "recent_projects": dict(recent_projects.most_common(8)),
        "recent_tools": dict(recent_tools.most_common(10)),
        "recent_sessions": len(recent_sessions_set),
        "recent_total": sum(recent_tools.values()),
        # Session scatter data
        "session_scatter": [
            {
                "date": v["first_ts"][:10],
                "epoch_ms": session_epoch_ms.get(sid, 0),
                "hour": datetime.fromisoformat(v["first_ts"]).hour,
                "tools": min(v["tool_count"], 200),
                "project": v["project"][:40],
            }
            for sid, v in session_info.items()
            if v["tool_count"] > 0
        ],
    }


def extract_codex():
    """Extract all Codex statistics."""
    sessions_dir = HOME / ".codex" / "sessions"
    jsonl_files = list(sessions_dir.rglob("*.jsonl")) if sessions_dir.exists() else []

    session_count = 0
    daily_sessions = Counter()
    hour_bins = Counter()
    shell_cmds = []
    exit_codes = Counter()
    patches_ok = 0
    patches_total = 0
    searches = []
    token_in = 0
    token_out = 0
    token_cache = 0
    errors = []
    models = Counter()
    event_counts = Counter()
    turn_count = 0
    parse_errors = 0
    recent_sessions = 0
    recent_daily = Counter()

    for sf in jsonl_files:
        # Per-file max values (Codex token_count events report cumulative
        # session totals, so we take the max per file and sum across files)
        file_ti = 0
        file_to = 0
        file_tc = 0
        try:
            for line in sf.read_text().strip().splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)

                if d.get("type") == "session_meta":
                    session_count += 1
                    p = d.get("payload", {})
                    models[p.get("model_provider", "?")] += 1
                    ts = p.get("timestamp", "")
                    if ts:
                        try:
                            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                            local_dt = dt.astimezone()
                            daily_sessions[local_dt.strftime("%Y-%m-%d")] += 1
                            hour_bins[local_dt.hour] += 1
                            if local_dt >= recent_cutoff:
                                recent_sessions += 1
                                recent_daily[local_dt.strftime("%Y-%m-%d")] += 1
                        except Exception:
                            pass

                elif d.get("type") == "event_msg":
                    p = d.get("payload", {})
                    et = p.get("type", "")
                    event_counts[et] += 1

                    if et == "exec_command_end":
                        cmd_arr = p.get("command", [])
                        cmd = " ".join(cmd_arr) if isinstance(cmd_arr, list) else str(cmd_arr)
                        shell_cmds.append(cmd)
                        ec = p.get("exit_code", -1)
                        exit_codes[str(ec)] += 1

                    elif et == "patch_apply_end":
                        patches_total += 1
                        if p.get("success"):
                            patches_ok += 1

                    elif et == "web_search_end":
                        searches.append(p.get("query", "")[:120])

                    elif et == "token_count":
                        info = p.get("info") or {}
                        if isinstance(info, dict):
                            tt = info.get("total_token_usage", {})
                            if tt:
                                file_ti = max(file_ti, tt.get("input_tokens", 0) or 0)
                                file_to = max(file_to, tt.get("output_tokens", 0) or 0)
                                file_tc = max(file_tc, tt.get("cached_input_tokens", 0) or 0)

                    elif et == "error":
                        errors.append(p.get("message", "")[:150])

                    elif et == "task_started":
                        turn_count += 1

        except Exception:
            parse_errors += 1
        token_in += file_ti
        token_out += file_to
        token_cache += file_tc

    shell_cats = Counter()
    for cmd in shell_cmds:
        shell_cats[classify_shell_cmd(cmd)] += 1

    return {
        "sessions": session_count,
        "turns": turn_count,
        "daily_sessions": dict(sorted(daily_sessions.items())),
        "shell_categories": dict(shell_cats.most_common()),
        "shell_total": len(shell_cmds),
        "exit_codes": dict(exit_codes.most_common(6)),
        "patches_total": patches_total,
        "patches_ok": patches_ok,
        "patches_fail": patches_total - patches_ok,
        "searches": searches[:10],
        "search_count": len(searches),
        "token_in": token_in,
        "token_out": token_out,
        "token_cache": token_cache,
        "cache_hit_pct": round(token_cache / token_in * 100, 1) if token_in > 0 else 0,
        "errors": errors[:5],
        "error_count": len(errors),
        "models": dict(models),
        "events": dict(event_counts.most_common(12)),
        "parse_errors": parse_errors,
        "hour_bins": {str(h): hour_bins[h] for h in range(24)},
        "recent_sessions": recent_sessions,
        "recent_daily": dict(sorted(recent_daily.items())),
    }


def extract_kimi():
    """Extract all Kimi Code statistics."""
    wire_files = list((HOME / ".kimi" / "sessions").rglob("wire.jsonl"))

    tool_counts = Counter()
    shell_cmds = []
    hour_bins = Counter()
    token_in = 0
    token_out = 0
    token_cache_read = 0
    session_count = 0
    failures = 0
    parse_errors = 0

    for wf in wire_files:
        has_tools = False
        try:
            for line in wf.read_text().strip().splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                msg = d.get("message", {})
                if not isinstance(msg, dict):
                    continue

                mtype = msg.get("type", "")

                # Track hour from timestamp if available
                ts_raw = d.get("timestamp", "")
                if ts_raw and mtype == "ToolCall":
                    try:
                        if isinstance(ts_raw, (int, float)):
                            dt = datetime.fromtimestamp(ts_raw, tz=timezone.utc)
                        else:
                            dt = datetime.fromisoformat(str(ts_raw).replace("Z", "+00:00"))
                        local_dt = dt.astimezone()
                        hour_bins[local_dt.hour] += 1
                    except Exception:
                        pass

                if mtype == "ToolCall":
                    func = msg.get("payload", {}).get("function", msg.get("function", {}))
                    tn = func.get("name", "?")
                    tool_counts[tn] += 1
                    has_tools = True

                    args_str = func.get("arguments", "{}")
                    try:
                        args = json.loads(args_str) if isinstance(args_str, str) else args_str
                        cmd = args.get("command", "")
                        if cmd:
                            shell_cmds.append(cmd)
                    except Exception:
                        pass

                elif mtype == "ToolResult":
                    rv = msg.get("payload", {}).get("return_value", {})
                    if rv.get("is_error"):
                        failures += 1

                elif mtype == "StatusUpdate":
                    tu = msg.get("payload", {}).get("token_usage", {})
                    if tu:
                        token_in += tu.get("input_other", 0) or 0
                        token_out += tu.get("output", 0) or 0
                        token_cache_read += tu.get("input_cache_read", 0) or 0

        except Exception:
            parse_errors += 1
        if has_tools:
            session_count += 1

    shell_cats = Counter()
    for cmd in shell_cmds:
        shell_cats[classify_shell_cmd(cmd)] += 1

    core_tools = {"Shell", "ReadFile", "Glob", "WriteFile", "StrReplaceFile", "Grep",
                  "AskUserQuestion", "Skill", "Agent", "TaskCreate", "TaskUpdate",
                  "EnterPlanMode", "ExitPlanMode", "Edit", "Write", "Read", "Bash",
                  "WebSearch", "WebFetch", "NotebookEdit", "List", "Monitor",
                  "TodoWrite", "Task", "CronCreate", "CronDelete", "CronList",
                  "ScheduleWakeup", "PushNotification", "RemoteTrigger",
                  "EnterWorktree", "ExitWorktree", "LSP"}
    domain_tools = {}
    for tn, cnt in tool_counts.items():
        if tn not in core_tools:
            domain_tools[tn] = cnt

    return {
        "sessions": session_count,
        "tools": sum(tool_counts.values()),
        "tool_types": len(tool_counts),
        "tool_names": dict(tool_counts.most_common(15)),
        "domain_tools": dict(sorted(domain_tools.items(), key=lambda x: x[1], reverse=True)[:15]),
        "shell_categories": dict(shell_cats.most_common()),
        "shell_total": len(shell_cmds),
        "token_in": token_in,
        "token_out": token_out,
        "token_cache": token_cache_read,
        "failure_count": failures,
        "parse_errors": parse_errors,
        "hour_bins": {str(h): hour_bins[h] for h in range(24)},
    }


# ═══════════════════════════════════════════════════════════════
# HTML Generation
# ═══════════════════════════════════════════════════════════════

CSS = """
:root {
  --bg: #0d1117;
  --card: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --muted: #8b949e;
  --accent: #58a6ff;
  --green: #3fb950;
  --orange: #d2991d;
  --red: #f85149;
  --purple: #a371f7;
  --cc-color: #58a6ff;
  --cx-color: #3fb950;
  --kc-color: #a371f7;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.5;
  max-width: 1280px; margin: 0 auto; padding: 24px;
}
h1 { font-size: 28px; margin-bottom: 4px; }
h2 { font-size: 22px; margin: 40px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
h3 { font-size: 18px; margin-bottom: 12px; color: var(--text); }
.subtitle { color: var(--muted); margin-bottom: 24px; font-size: 14px; }

/* Summary Cards */
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 24px; }
.card {
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 14px 16px; text-align: center;
}
.card .value { font-size: 28px; font-weight: 700; color: var(--accent); }
.card .label { font-size: 11px; color: var(--muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.card .sub { font-size: 12px; color: var(--muted); margin-top: 2px; }

/* Tool Sections */
.tool-section {
  background: var(--card); border: 1px solid var(--border); border-radius: 10px;
  padding: 20px 24px; margin-bottom: 28px;
}
.tool-section.claude { border-left: 3px solid var(--cc-color); }
.tool-section.codex  { border-left: 3px solid var(--cx-color); }
.tool-section.kimi   { border-left: 3px solid var(--kc-color); }
.tool-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.tool-header .dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.tool-header .dot.cc { background: var(--cc-color); }
.tool-header .dot.cx { background: var(--cx-color); }
.tool-header .dot.kc { background: var(--kc-color); }
.tool-header h2 { margin: 0; padding: 0; border: none; font-size: 20px; }

/* Chart wrapper */
.chart-wrap {
  background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
  padding: 16px; margin-bottom: 16px;
}
.chart-wrap canvas { max-height: 320px; }
.chart-wrap h4 { font-size: 13px; color: var(--muted); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
.row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.row3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
@media (max-width: 768px) { .row2, .row3 { grid-template-columns: 1fr; } }

/* Tables */
table { width: 100%; border-collapse: collapse; }
th, td { padding: 6px 12px; text-align: left; border-bottom: 1px solid var(--border); font-size: 13px; }
th { color: var(--muted); font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }
tr:hover { background: rgba(255,255,255,0.02); }

/* Token display */
.token-row { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; padding: 12px 0; }
.token-item { text-align: center; min-width: 100px; }
.token-item .val { font-size: 20px; font-weight: 700; }
.token-item .lbl { font-size: 11px; color: var(--muted); }
.token-item.cc .val { color: var(--cc-color); }
.token-item.cx .val { color: var(--cx-color); }
.token-item.kc .val { color: var(--kc-color); }

/* Stat pills */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
.stat-pill {
  background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 16px; text-align: center; min-width: 100px; flex: 1;
}
.stat-pill .val { font-size: 22px; font-weight: 700; }
.stat-pill .lbl { font-size: 11px; color: var(--muted); }

footer { text-align: center; color: var(--muted); font-size: 12px; margin-top: 48px; padding: 16px; border-top: 1px solid var(--border); }

/* Comparison bars */
.comparison-table td { font-size: 14px; }
.comparison-table .bar-cell { width: 200px; }
.comparison-table .bar-fill { height: 6px; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 8px; }
.comparison-table .bar-fill.cc { background: var(--cc-color); }
.comparison-table .bar-fill.cx { background: var(--cx-color); }
.comparison-table .bar-fill.kc { background: var(--kc-color); }
"""


def js_safe(obj):
    """Serialize Python object to JSON-safe JS embedded in HTML."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def _fmt(n):
    """Format large numbers compactly."""
    if n is None:
        return "—"
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def _pct(part, total):
    """Percentage string."""
    if not total:
        return "—"
    return f"{part/total*100:.1f}%"


def build_html(cc, cx, kc):
    """Generate complete HTML document."""

    # Aggregate stats
    all_dates = set(cc.get("dates", []))
    all_dates.update(cx.get("daily_sessions", {}).keys())
    total_sessions = cc["sessions"] + cx["sessions"] + kc["sessions"]
    total_tool_calls = cc["tools"] + cx["turns"] + kc["tools"]
    total_shell = cc["shell_total"] + cx["shell_total"] + kc["shell_total"]
    total_token_in = (cc["token_in"] or 0) + (cx["token_in"] or 0) + (kc["token_in"] or 0)
    total_token_out = (cc["token_out"] or 0) + (cx["token_out"] or 0) + (kc["token_out"] or 0)
    tools_with_data = sum(1 for t in [cc, cx, kc] if t["sessions"] > 0)

    data_js = f"""
const CC = {js_safe(cc)};
const CX = {js_safe(cx)};
const KC = {js_safe(kc)};
"""

    # Shared Chart.js init
    chart_init = """const COLORS = ['#58a6ff','#3fb950','#d2991d','#f85149','#a371f7','#79c0ff','#56d364','#e3b341','#ff7b72','#d2a8ff','#39d353','#f0883e','#c9d1d9','#8b949e','#6e7681'];
Chart.defaults.color = '#8b949e';
Chart.defaults.borderColor = '#21262d';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
function mk(id, cfg) { const c = document.getElementById(id); return c ? new Chart(c, cfg) : null; }"""

    # ── Build Per-Tool Section HTML ──

    def tool_section(label, cls, dot_cls, data, extra_html, chart_html):
        """Generate a consistent per-tool section."""
        return f"""
<!-- {label} -->
<div class="tool-section {cls}">
  <div class="tool-header">
    <div class="dot {dot_cls}"></div>
    <h2>{label}</h2>
  </div>
  <div class="stat-row">
    <div class="stat-pill"><div class="val" style="color:var(--{cls}-color)">{data['sessions']:,}</div><div class="lbl">Sessions</div></div>
    <div class="stat-pill"><div class="val" style="color:var(--{cls}-color)">{data['tools']:,}</div><div class="lbl">Tool Calls</div></div>
    <div class="stat-pill"><div class="val" style="color:var(--{cls}-color)">{data['tool_types']}</div><div class="lbl">Tool Types</div></div>
    <div class="stat-pill"><div class="val" style="color:var(--{cls}-color)">{_fmt(data['token_in'])}</div><div class="lbl">Token In</div></div>
    <div class="stat-pill"><div class="val" style="color:var(--{cls}-color)">{_fmt(data['shell_total'])}</div><div class="lbl">Shell Cmds</div></div>
  </div>
  {chart_html}
  {extra_html}
</div>"""

    # ── Claude Code section ──
    claude_charts = f"""
  <div class="row2">
    <div class="chart-wrap"><h4>Tool Distribution</h4><canvas id="ccTools"></canvas></div>
    <div class="chart-wrap"><h4>Shell Categories</h4><canvas id="ccShell"></canvas></div>
  </div>
  <div class="row2">
    <div class="chart-wrap"><h4>File Operations</h4><canvas id="ccFileOps"></canvas></div>
    <div class="chart-wrap"><h4>File Types Read</h4><canvas id="ccFileTypes"></canvas></div>
  </div>
  <div class="row2">
    <div class="chart-wrap"><h4>Projects</h4><canvas id="ccProjects"></canvas></div>
    <div class="chart-wrap"><h4>Activity by Hour (Local)</h4><canvas id="ccHours"></canvas></div>
  </div>
  <div class="row2">
    <div class="chart-wrap"><h4>Session Timeline</h4><canvas id="ccScatter"></canvas></div>
    <div class="chart-wrap"><h4>Session Duration</h4><canvas id="ccDuration"></canvas></div>
  </div>"""

    claude_extra = ""

    cc_data = {
        "sessions": cc["sessions"],
        "tools": cc["tools"],
        "tool_types": len(cc["tool_names"]),
        "token_in": cc["token_in"],
        "shell_total": cc["shell_total"],
    }

    claude_section = tool_section("Claude Code", "claude", "cc", cc_data, claude_extra, claude_charts)

    # ── Codex section ──
    codex_charts = f"""
  <div class="row2">
    <div class="chart-wrap"><h4>Event Types</h4><canvas id="cxEvents"></canvas></div>
    <div class="chart-wrap"><h4>Shell Categories</h4><canvas id="cxShell"></canvas></div>
  </div>
  <div class="row2">
    <div class="chart-wrap"><h4>Exit Codes</h4><canvas id="cxExitCodes"></canvas></div>
    <div class="chart-wrap"><h4>Daily Sessions</h4><canvas id="cxDaily"></canvas></div>
  </div>"""

    codex_extra = f"""
  <div class="row2">
    <div class="chart-wrap">
      <h4>Patches & Searches</h4>
      <div style="display:flex;gap:24px;justify-content:center;padding:12px 0;">
        <div style="text-align:center"><div style="font-size:28px;font-weight:700;color:var(--cx-color)">{cx['patches_total']}</div><div style="font-size:11px;color:var(--muted)">Patches ({cx['patches_ok']} ok, {cx['patches_fail']} fail)</div></div>
        <div style="text-align:center"><div style="font-size:28px;font-weight:700;color:var(--cx-color)">{cx['search_count']}</div><div style="font-size:11px;color:var(--muted)">Web Searches</div></div>
        <div style="text-align:center"><div style="font-size:28px;font-weight:700;color:var(--cx-color)">{cx['error_count']}</div><div style="font-size:11px;color:var(--muted)">Errors</div></div>
      </div>
    </div>
    <div class="chart-wrap">
      <h4>Top Web Searches</h4>
      <div style="max-height:200px;overflow-y:auto;font-size:12px;color:var(--muted);padding:8px;">
        {"".join(f'<div style="padding:2px 0;border-bottom:1px solid var(--border)">{s[:100]}</div>' for s in cx.get('searches', [])[:8])}
      </div>
    </div>
  </div>"""

    cx_data = {
        "sessions": cx["sessions"],
        "tools": cx["turns"],
        "tool_types": len(cx.get("events", {})),
        "token_in": cx["token_in"],
        "shell_total": cx["shell_total"],
    }

    codex_section = tool_section("Codex (OpenAI)", "codex", "cx", cx_data, codex_extra, codex_charts)

    # ── Kimi Code section ──
    kimi_charts = f"""
  <div class="row2">
    <div class="chart-wrap"><h4>Tool Distribution</h4><canvas id="kcTools"></canvas></div>
    <div class="chart-wrap"><h4>Shell Categories</h4><canvas id="kcShell"></canvas></div>
  </div>"""

    kimi_domain_html = ""
    if kc.get("domain_tools"):
        dt_items = "".join(
            f'<tr><td>{tn}</td><td>{cnt}</td></tr>'
            for tn, cnt in list(kc["domain_tools"].items())[:12]
        )
        kimi_domain_html = f"""
  <div class="chart-wrap">
    <h4>Domain-Specific Tools ({len(kc['domain_tools'])} types)</h4>
    <table><thead><tr><th>Tool Name</th><th>Calls</th></tr></thead><tbody>{dt_items}</tbody></table>
  </div>"""

    kimi_extra = kimi_domain_html

    kc_data = {
        "sessions": kc["sessions"],
        "tools": kc["tools"],
        "tool_types": kc["tool_types"],
        "token_in": kc["token_in"],
        "shell_total": kc["shell_total"],
    }

    kimi_section = tool_section("Kimi Code", "kimi", "kc", kc_data, kimi_extra, kimi_charts)

    # Build cross-tool sections (only if 2+ tools have data)
    cross_timeline = ""
    cross_hours = ""
    cross_comparison = ""
    token_comparison = ""
    if tools_with_data >= 2:
        cross_timeline = f"""
<h2>Cross-Tool Activity Timeline</h2>
<div class="chart-wrap"><canvas id="overviewTimeline"></canvas></div>"""

        cross_hours = """
<h2>24-Hour Activity (Combined)</h2>
<div class="chart-wrap"><canvas id="combinedHours"></canvas></div>"""

        cross_comparison = f"""
<h2>Cross-Tool Comparison</h2>
<div class="row2">
  <div class="chart-wrap"><h4>Scale Comparison</h4><canvas id="crossScale"></canvas></div>
  <div class="chart-wrap"><h4>Shell Command Mix</h4><canvas id="crossShell"></canvas></div>
</div>"""

        token_comparison = f"""
<h2>Token Usage Comparison</h2>
<div class="chart-wrap">
  <div class="token-row">
    {'<div class="token-item cc"><div class="val">' + _fmt(cc["token_in"]) + '</div><div class="lbl">Claude Input</div></div><div class="token-item cc"><div class="val">' + _fmt(cc["token_out"]) + '</div><div class="lbl">Claude Output</div></div><div class="token-item cc"><div class="val">' + str(cc["cache_hit_pct"]) + '%</div><div class="lbl">Cache Hit</div></div>' if cc["sessions"] > 0 else ""}
  </div>
  <div class="token-row">
    {'<div class="token-item cx"><div class="val">' + _fmt(cx["token_in"]) + '</div><div class="lbl">Codex Input</div></div><div class="token-item cx"><div class="val">' + _fmt(cx["token_out"]) + '</div><div class="lbl">Codex Output</div></div><div class="token-item cx"><div class="val">' + str(cx["cache_hit_pct"]) + '%</div><div class="lbl">Cache Hit</div></div>' if cx["sessions"] > 0 else ""}
  </div>
  <div class="token-row">
    {'<div class="token-item kc"><div class="val">' + _fmt(kc["token_in"]) + '</div><div class="lbl">Kimi Input</div></div><div class="token-item kc"><div class="val">' + _fmt(kc["token_out"]) + '</div><div class="lbl">Kimi Output</div></div>' if kc["sessions"] > 0 else ""}
  </div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Session Analysis Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>{CSS}</style>
</head>
<body>

<h1>AI Coding Session Report</h1>
<p class="subtitle">Claude Code · Codex · Kimi Code — Generated {NOW.strftime("%Y-%m-%d %H:%M UTC")}</p>

<!-- ═══════════════ OVERALL SUMMARY ═══════════════ -->
<h2>Overall Summary</h2>
<div class="cards">
  <div class="card">
    <div class="value">{total_sessions:,}</div>
    <div class="label">Total Sessions</div>
    <div class="sub">{'CC ' + str(cc['sessions']) if cc['sessions'] > 0 else ''}{' · Codex ' + str(cx['sessions']) if cx['sessions'] > 0 else ''}{' · Kimi ' + str(kc['sessions']) if kc['sessions'] > 0 else ''}</div>
  </div>
  <div class="card">
    <div class="value">{_fmt(total_tool_calls)}</div>
    <div class="label">Tool Calls / Turns</div>
  </div>
  <div class="card">
    <div class="value">{len(all_dates)}</div>
    <div class="label">Active Days</div>
  </div>
  <div class="card">
    <div class="value">{_fmt(total_shell)}</div>
    <div class="label">Shell Commands</div>
  </div>
  <div class="card">
    <div class="value">{_fmt(total_token_in)}</div>
    <div class="label">Total Token Input</div>
  </div>
  <div class="card">
    <div class="value">{_fmt(total_token_out)}</div>
    <div class="label">Total Token Output</div>
  </div>
</div>

{cross_timeline}
{cross_hours}
{cross_comparison}

<!-- ═══════════════ PER-TOOL SECTIONS ═══════════════ -->
{claude_section if cc['sessions'] > 0 else ''}
{codex_section if cx['sessions'] > 0 else ''}
{kimi_section if kc['sessions'] > 0 else ''}

{token_comparison}

<footer>Generated by ai-session-analysis skill · Data sourced from ~/.claude/projects/, ~/.codex/sessions/, ~/.kimi/sessions/</footer>

<script>
{data_js}
{chart_init}

// Sort data objects by value descending for consistent chart rendering
function sortObjDesc(obj) {{
  const sorted = {{}};
  Object.entries(obj).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => {{ sorted[k] = v; }});
  return sorted;
}}
if (CC.sessions > 0) {{
  CC.shell_categories = sortObjDesc(CC.shell_categories);
  CC.tool_names = sortObjDesc(CC.tool_names);
  CC.file_types = sortObjDesc(CC.file_types);
  CC.projects = sortObjDesc(CC.projects);
}}
if (CX.sessions > 0) {{
  CX.shell_categories = sortObjDesc(CX.shell_categories);
  CX.events = sortObjDesc(CX.events);
}}
if (KC.sessions > 0) {{
  KC.shell_categories = sortObjDesc(KC.shell_categories);
  KC.tool_names = sortObjDesc(KC.tool_names);
}}

// ── Overview Timeline ──
(function() {{
  const allDates = new Set();
  Object.keys(CC.daily).forEach(d => allDates.add(d));
  Object.keys(CX.daily_sessions || {{}}).forEach(d => allDates.add(d));
  const dates = Array.from(allDates).sort();
  mk('overviewTimeline', {{
    type: 'bar',
    data: {{
      labels: dates,
      datasets: [
        {{ label: 'Claude Code', data: dates.map(d => CC.daily[d] || 0), backgroundColor: '#58a6ff66', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 3, yAxisID: 'y' }},
        {{ label: 'Codex sessions', data: dates.map(d => (CX.daily_sessions||{{}})[d]||0), type: 'line', borderColor: '#3fb950', backgroundColor: '#3fb95000', pointRadius: 3, tension: 0.1, yAxisID: 'y1' }},
        {{ label: 'Kimi sessions', data: dates.map(d => 0), type: 'line', borderColor: '#a371f7', backgroundColor: '#a371f700', pointRadius: 0, borderWidth: 0, yAxisID: 'y1' }},
      ]
    }},
    options: {{
      responsive: true,
      interaction: {{ intersect: false, mode: 'index' }},
      scales: {{
        x: {{ grid: {{ display: false }} }},
        y: {{ title: {{ display: true, text: 'Tool Calls' }}, beginAtZero: true, position: 'left' }},
        y1: {{ title: {{ display: true, text: 'Sessions' }}, beginAtZero: true, position: 'right', grid: {{ display: false }} }},
      }}
    }}
  }});
}})();

// ── Cross-Tool Scale Comparison ──
mk('crossScale', {{
  type: 'bar',
  data: {{
    labels: ['Sessions', 'Tool Calls', 'Shell Cmds', 'Tool Types'],
    datasets: [
      {{ label: 'Claude Code', data: [{cc['sessions']}, {cc['tools']}, {cc['shell_total']}, {len(cc['tool_names'])}], backgroundColor: '#58a6ff88', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 4 }},
      {{ label: 'Codex', data: [{cx['sessions']}, {cx['turns']}, {cx['shell_total']}, {len(cx.get('events',{}))}], backgroundColor: '#3fb95088', borderColor: '#3fb950', borderWidth: 1, borderRadius: 4 }},
      {{ label: 'Kimi Code', data: [{kc['sessions']}, {kc['tools']}, {kc['shell_total']}, {kc['tool_types']}], backgroundColor: '#a371f788', borderColor: '#a371f7', borderWidth: 1, borderRadius: 4 }},
    ]
  }},
  options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }} }}
}});

// ── Cross-Tool Shell Mix ──
(function() {{
  const allCats = new Set();
  [CC.shell_categories, CX.shell_categories, KC.shell_categories].forEach(c => Object.keys(c||{{}}).forEach(k => allCats.add(k)));
  const cats = Array.from(allCats).sort((a, b) => {{
    const ta = (CC.shell_categories[a]||0) + (CX.shell_categories[a]||0) + (KC.shell_categories[a]||0);
    const tb = (CC.shell_categories[b]||0) + (CX.shell_categories[b]||0) + (KC.shell_categories[b]||0);
    return tb - ta;
  }});
  mk('crossShell', {{
    type: 'bar',
    data: {{
      labels: cats,
      datasets: [
        {{ label: 'Claude Code', data: cats.map(c => (CC.shell_categories||{{}})[c]||0), backgroundColor: '#58a6ff88', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 3 }},
        {{ label: 'Codex', data: cats.map(c => (CX.shell_categories||{{}})[c]||0), backgroundColor: '#3fb95088', borderColor: '#3fb950', borderWidth: 1, borderRadius: 3 }},
        {{ label: 'Kimi Code', data: cats.map(c => (KC.shell_categories||{{}})[c]||0), backgroundColor: '#a371f788', borderColor: '#a371f7', borderWidth: 1, borderRadius: 3 }},
      ]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true }} }} }}
  }});
}})();

	// ── Combined 24-Hour Activity ──
	(function() {{
	  const labels = Array.from({{length: 24}}, (_,i) => `${{i}}:00`);
	  const total = Array.from({{length: 24}}, (_,i) =>
	    ((CC.hour_bins||{{}})[String(i)]||0) + ((CX.hour_bins||{{}})[String(i)]||0) + ((KC.hour_bins||{{}})[String(i)]||0)
	  );
	  mk('combinedHours', {{
	    type: 'bar',
	    data: {{
	      labels,
	      datasets: [{{ data: total, backgroundColor: '#58a6ff88', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 4 }}]
	    }},
	    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ title: {{ display: true, text: 'Hour (Local)', color: '#8b949e' }} }}, y: {{ beginAtZero: true, title: {{ display: true, text: 'Tool Calls / Sessions', color: '#8b949e' }} }} }} }}
	  }});
	}})();

// ══════════ CLAUDE CODE CHARTS ══════════

mk('ccTools', {{
  type: 'doughnut',
  data: {{
    labels: Object.keys(CC.tool_names).slice(0,10),
    datasets: [{{ data: Object.values(CC.tool_names).slice(0,10), backgroundColor: COLORS, borderColor: '#0d1117', borderWidth: 2 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ font: {{ size: 11 }} }} }} }} }}
}});

mk('ccShell', {{
  type: 'bar',
  data: {{
    labels: Object.keys(CC.shell_categories),
    datasets: [{{ data: Object.values(CC.shell_categories), backgroundColor: '#58a6ff88', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

mk('ccFileOps', {{
  type: 'bar',
  data: {{
    labels: ['Read', 'Edit', 'Write'],
    datasets: [{{ data: [{cc['read_count']}, {cc['edit_count']}, {cc['write_count']}], backgroundColor: ['#58a6ff','#a371f7','#3fb950'], borderRadius: 6 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
}});

mk('ccFileTypes', {{
  type: 'bar',
  data: {{
    labels: Object.keys(CC.file_types),
    datasets: [{{ data: Object.values(CC.file_types), backgroundColor: '#58a6ff66', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
}});

mk('ccProjects', {{
  type: 'bar',
  data: {{
    labels: Object.keys(CC.projects).map(p => p.length > 35 ? p.slice(0,35)+'...' : p),
    datasets: [{{ data: Object.values(CC.projects), backgroundColor: COLORS, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

mk('ccHours', {{
  type: 'bar',
  data: {{
    labels: Array.from({{length: 24}}, (_,i) => `${{i}}:00`),
    datasets: [{{ data: Array.from({{length: 24}}, (_,i) => (CC.hour_bins||{{}})[String(i)]||0), backgroundColor: '#58a6ff66', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 3 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }}, x: {{ title: {{ display: true, text: 'Hour (Local)', color: '#8b949e' }} }} }} }}
}});

mk('ccScatter', {{
  type: 'scatter',
  data: {{
    datasets: [{{ label: 'Sessions', data: CC.session_scatter.map(s => ({{ x: s.epoch_ms, y: s.hour, r: Math.max(3, Math.sqrt(s.tools)*1.5) }})), backgroundColor: '#58a6ff66', borderColor: '#58a6ff', borderWidth: 1 }}]
  }},
  options: {{
    responsive: true,
    scales: {{
      x: {{ type: 'linear', ticks: {{ callback: v => new Date(v).toISOString().slice(0,10), maxTicksLimit: 12 }}, grid: {{ color: '#21262d' }} }},
      y: {{ min: 0, max: 23, ticks: {{ stepSize: 3, callback: v => v + ':00' }} }}
    }},
    plugins: {{ tooltip: {{ callbacks: {{ label: ctx => {{ const s = CC.session_scatter[ctx.dataIndex]; return s ? s.project + ' — ' + s.tools + ' tools' : ''; }} }} }} }}
  }}
}});

const durOrder = ['<5min','5-15min','15-30min','30-60min','1-2hr','2hr+'];
mk('ccDuration', {{
  type: 'bar',
  data: {{
    labels: durOrder,
    datasets: [{{ data: durOrder.map(k => (CC.duration_bins||{{}})[k]||0), backgroundColor: '#58a6ff88', borderColor: '#58a6ff', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Sessions' }} }} }} }}
}});

// ══════════ CODEX CHARTS ══════════

mk('cxEvents', {{
  type: 'bar',
  data: {{
    labels: Object.keys(CX.events),
    datasets: [{{ data: Object.values(CX.events), backgroundColor: '#3fb95088', borderColor: '#3fb950', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

mk('cxShell', {{
  type: 'bar',
  data: {{
    labels: Object.keys(CX.shell_categories),
    datasets: [{{ data: Object.values(CX.shell_categories), backgroundColor: '#3fb95088', borderColor: '#3fb950', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

mk('cxExitCodes', {{
  type: 'doughnut',
  data: {{
    labels: Object.keys(CX.exit_codes).map(k => `exit ${{k}}`),
    datasets: [{{ data: Object.values(CX.exit_codes), backgroundColor: ['#3fb950','#f85149','#d2991d','#a371f7','#8b949e','#c9d1d9'], borderColor: '#0d1117', borderWidth: 2 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ font: {{ size: 11 }} }} }} }} }}
}});

mk('cxDaily', {{
  type: 'bar',
  data: {{
    labels: Object.keys(CX.daily_sessions),
    datasets: [{{ data: Object.values(CX.daily_sessions), backgroundColor: '#3fb95088', borderColor: '#3fb950', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Sessions' }} }} }} }}
}});

// ══════════ KIMI CODE CHARTS ══════════

mk('kcTools', {{
  type: 'doughnut',
  data: {{
    labels: Object.keys(KC.tool_names).slice(0,10),
    datasets: [{{ data: Object.values(KC.tool_names).slice(0,10), backgroundColor: COLORS, borderColor: '#0d1117', borderWidth: 2 }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ font: {{ size: 11 }} }} }} }} }}
}});

mk('kcShell', {{
  type: 'bar',
  data: {{
    labels: Object.keys(KC.shell_categories),
    datasets: [{{ data: Object.values(KC.shell_categories), backgroundColor: '#a371f788', borderColor: '#a371f7', borderWidth: 1, borderRadius: 4 }}]
  }},
  options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
}});

</script>

</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate HTML report from AI coding session data")
    parser.add_argument("output", nargs="?", default="ai-session-report.html",
                        help="Output HTML file path")
    parser.add_argument("--days", type=int, default=7,
                        help="Recent activity window in days (default: 7)")
    parser.add_argument("--no-open", action="store_true",
                        help="Don't open the report in browser")
    args = parser.parse_args()

    global RECENT_DAYS, recent_cutoff
    RECENT_DAYS = args.days
    recent_cutoff = NOW - timedelta(days=RECENT_DAYS)

    output = Path(args.output)

    print("Extracting Claude Code data...")
    cc = extract_claude()
    print(f"  {cc['sessions']} sessions, {cc['tools']:,} tool calls")

    print("Extracting Codex data...")
    cx = extract_codex()
    print(f"  {cx['sessions']} sessions, {cx['shell_total']:,} shell commands")

    print("Extracting Kimi Code data...")
    kc = extract_kimi()
    print(f"  {kc['sessions']} sessions, {kc['tools']:,} tool calls")

    print(f"Generating HTML report → {output}")
    html = build_html(cc, cx, kc)
    output.write_text(html, encoding="utf-8")
    print(f"Done: {output} ({output.stat().st_size // 1024}KB)")
    if not args.no_open:
        import webbrowser
        webbrowser.open(str(output.resolve()))
        print(f"Opened: {output}")


if __name__ == "__main__":
    main()
