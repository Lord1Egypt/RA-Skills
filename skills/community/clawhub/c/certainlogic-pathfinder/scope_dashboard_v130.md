# AgentPathfinder v1.3.0 Dashboard — Scope Document
**Date**: 2026-05-02  
**Status**: Scoped, awaiting Anton approval  
**Process**: PROCESS.md v2.0 — Design Phase → Construction → Documentation → Quality Verification → Pre-Publication Audit → Approval Gate → Publication

---

## 1. Purpose

A single-page HTML dashboard that visualizes AgentPathfinder v1.3.0's tool audit trail in real-time. Designed as the **YC demo centerpiece** — open a browser, run a task, watch the cryptographic proof unfold.

**What it proves**: That every tool call is HMAC-signed, tamper-evident, and auditable in real-time.

---

## 2. What It SHOWS (Not Just Tells)

### Main View: Live Task Execution

```
┌─────────────────────────────────────────────────────────────┐
│  AgentPathfinder v1.3.0 — Live Audit Dashboard              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Task: deploy_api                    Status: 🔄 Running     │
│  Agent: agent_1                     Started: 14:23:01 UTC   │
│                                                             │
│  Step 1: run_tests                                          │
│  ├── 🔧 TOOL_INVOKED  14:23:02  exec                        │
│  │   args: {command: "pytest tests/ --tb=short"}            │
│  │   tool_id: tl_a1b2c3d4e5f6                               │
│  │   🔐 HMAC: 7a3f... (truncated)                           │
│  │                                                          │
│  ├── ✅ TOOL_RESULT   14:23:03  420ms                       │
│  │   exit_code: 0                                           │
│  │   stdout: "3 passed, 0 failed"                            │
│  │   🔐 HMAC: 9e2b... (truncated)                           │
│  │                                                          │
│  ├── 🔧 TOOL_INVOKED  14:23:04  read_file                   │
│  │   args: {path: "/app/config.yml"}                        │
│  │                                                          │
│  └── ✅ TOOL_RESULT   14:23:04  8ms                         │
│      exit_code: 0                                           │
│      content_length: 256 bytes                              │
│                                                             │
│  Step 2: build_image                                        │
│  └── ⏳ (pending)                                           │
│                                                             │
│  Step 3: push_registry                                      │
│  └── ⏳ (pending)                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Sidebar: Cryptographic Integrity Panel

```
┌──────────────────────────────┐
│  🔐 Audit Trail Integrity    │
├──────────────────────────────┤
│                              │
│  Events:        13           │
│  Valid HMAC:    13/13 ✅     │
│  Tampered:      0            │
│  Corrupted:     0            │
│                              │
│  Last verified:              │
│  14:23:45 UTC                │
│                              │
│  [🔍 Verify Now]             │
│                              │
├──────────────────────────────┤
│  📊 Tool Summary             │
├──────────────────────────────┤
│  exec:     2 invoked         │
│            2 completed       │
│            0 errors          │
│                              │
│  read_file: 1 invoked        │
│             1 completed      │
│                              │
│  write_file: 0               │
│                              │
└──────────────────────────────┘
```

---

## 3. Exact Features

### Core Features (MVP — Phase 1)

| # | Feature | Description | Proves |
|---|---------|-------------|--------|
| 1 | **Live task status** | Which step is running, which are pending/complete | AgentPathfinder tracks task lifecycle |
| 2 | **Tool call stream** | Real-time display of TOOL_INVOKED events with full args | Full argument logging, not hashed |
| 3 | **Tool result stream** | Real-time display of TOOL_RESULT with exit codes, stdout, duration | Full output logging |
| 4 | **Sub-tool chain depth** | Visual indent for child tools (depth=1, 2, etc.) | Parent-child relationship tracking |
| 5 | **HMAC signature display** | Shows truncated HMAC next to each event | Cryptographic signing is real |
| 6 | **Integrity panel** | Total events, valid signatures, tampered count | `verify_integrity()` works |
| 7 | **Auto-refresh** | Polls JSONL file every 2 seconds for new events | Real-time capability |
| 8 | **Error highlighting** | Tool results with non-zero exit_code show red | Error capture |
| 9 | **Duration display** | Shows execution time per tool call | Performance tracking |
| 10 | **Tool category badges** | System command, filesystem, web automation, etc. | Tool categorization |

### Enhanced Features (Phase 2 — if approved)

| # | Feature | Description | Proves |
|---|---------|-------------|--------|
| 11 | **Interactive audit trail viewer** | Click an event to see full JSON + HMAC | Transparency |
| 12 | **Fraud detection alerts** | Detects step_claimed without preceding TOOL_RESULT | Anomaly detection preview |
| 13 | **Export to JSON** | Download full audit trail with signatures | Data portability |
| 14 | **Multi-task view** | Dashboard shows all tasks, not just one | Multi-task management |
| 15 | **Agent identity panel** | Shows which agent claimed which step | Multi-agent accountability |

---

## 4. Technical Architecture

### Approach: File-Watcher HTML Generator (No Server)

**Why no Flask server?**
- Simpler deployment (open HTML file in browser)
- No additional dependencies
- Works in any environment
- YC demo: just open the file

```
AgentPathfinder writes to: ~/.agentpathfinder/pathfinder_data/audit/{task_id}.jsonl
                                 ↑
Dashboard script watches:    (Python file watcher)
                                 ↓
Regenerates:                 dashboard.html every 2 seconds
                                 ↓
Browser:                     Auto-reload via <meta http-equiv="refresh">
```

### File Structure

```
scripts/
├── dashboard_v130.py          # Main dashboard generator
├── dashboard_template.html    # HTML template (embedded in .py or separate)
└── watch_and_serve.py         # File watcher + optional mini HTTP server
```

### Data Flow

```python
# 1. Watch audit directory for changes
# 2. Read all .jsonl files in audit/
# 3. Parse JSONL into structured objects
# 4. Run verify_integrity() on each trail
# 5. Generate HTML with tool call tree
# 6. Write to dashboard.html
# 7. Browser auto-refreshes
```

### Key Implementation Details

| Problem | Solution |
|---------|----------|
| JSONL files grow large | Only read last N events (configurable, default 1000) |
| HMAC keys needed for verification | Read from vault shards (same as `verify_integrity()`) |
| Auto-refresh without server | `<meta http-equiv="refresh" content="2">` |
| Mobile responsive | CSS Grid + Flexbox, dark mode by default |
| No external CSS frameworks | Inline styles (self-contained single file) |

---

## 5. What It PROVES in a Demo

### During YC Interview — Live Demo Script

**Setup (before interview):**
```bash
$ pf create deploy_api "test" "build" "push"
```

**During interview:**
```bash
$ python3 scripts/dashboard_v130.py --watch
# Open http://localhost:8080 in browser
```

**You say:**
> "Watch this. My agent is about to run a task. Every tool call it makes will appear here in real-time, cryptographically signed."

**Agent runs:**
```python
audit = engine.get_tool_audit("deploy_api", 1)
executor = AuditedToolExecutor(audit)
result = executor.exec("echo 'hello world'")
```

**Dashboard shows:**
- 🔧 TOOL_INVOKED: exec, args: `{"command": "echo 'hello world'"}`
- ✅ TOOL_RESULT: 5ms, exit_code=0, stdout: "hello world\n"
- 🔐 HMAC signatures visible next to both events
- Integrity panel: "2 events, 2 valid, 0 tampered"

**You say:**
> "Now if someone edits this file, the HMAC won't match. We can detect tampering. Here's the actual verification running live."

**Click Verify Now:**
- Runs `verify_integrity()` 
- Shows green checkmark: "All signatures valid"

**You say:**
> "This is the first time anyone can watch an AI agent's actions with cryptographic proof in real-time. Not logs. Evidence."

---

## 6. What It Does NOT Do (Explicit Limits)

| Not Included | Why |
|--------------|-----|
| Multi-user authentication | Not a web app, local file only |
| Database backend | Reads from JSONL files only |
| Historical analytics over time | Shows current session only |
| Remote access | Runs locally (security boundary) |
| Write operations (can't create tasks) | Read-only dashboard |
| Real-time websockets | File polling is simpler, sufficient for demo |
| Pretty charts/graphs | Phase 2 (needs metrics aggregation) |

---

## 7. Time Estimate

| Phase | Effort | Deliverable |
|-------|--------|-------------|
| **MVP (Phase 1)** | **2-3 hours** | Single-page HTML dashboard with all 10 core features |
| **Polish** | **1 hour** | Mobile responsive, error handling, dark mode refinement |
| **Phase 2 enhancements** | **2-3 hours** | Interactive viewer, fraud alerts, export |
| **Integration test** | **30 min** | Verify dashboard refreshes as tasks run |
| **Documentation** | **30 min** | README section with screenshot |
| **Total MVP** | **~4 hours** | Demo-ready dashboard |
| **Total with Phase 2** | **~6-7 hours** | Feature-complete dashboard |

---

## 8. Files To Create

```
scripts/dashboard_v130.py          # ~200-300 lines
# OR (if separate template):
scripts/dashboard_v130.py          # ~150 lines (logic)
scripts/dashboard_template.html    # ~300 lines (template)
```

**No changes to existing files.** Purely additive.

---

## 9. Honest Assessment

### Strengths
- Visually proves everything we claim about v1.3.0
- Single command to run (`python3 scripts/dashboard_v130.py`)
- No dependencies beyond Python stdlib + AgentPathfinder
- Works in any browser
- Auto-refreshes, truly live

### Weaknesses
- Not a web server (opens file directly)
- No persistent history across sessions
- Limited to one task at a time (MVP)
- HTML file must be regenerated every 2 seconds (not websockets)

### Competitive Advantage
- LangSmith: Pretty traces, no crypto proof
- AgentPathfinder + Dashboard: Live cryptographic proof of every tool action
- **Nobody else shows HMAC signatures updating in real-time**

---

## 10. Approval Gate

**To build this, Anton must explicitly approve:**

**Option A: Build MVP (4 hours)** — Core 10 features, single-task view, file-watcher HTML generator. Demo-ready for YC.

**Option B: Build Full Feature Set (6-7 hours)** — All 15 features including interactive viewer, fraud detection alerts, multi-task view.

**Option C: Defer** — Skip dashboard for now, use CLI only for YC demo.

---

## 11. Integration with Publishing

If dashboard is built:
- Add `scripts/dashboard_v130.py` to repository
- Update README with dashboard section + screenshot
- Dashboard becomes part of ClawHub package when published
- Free tier includes dashboard (no license gating in v1.3.0)

---

**Scope prepared by:** Alex  
**Date:** 2026-05-02  
**Status:** Awaiting Anton approval before construction
