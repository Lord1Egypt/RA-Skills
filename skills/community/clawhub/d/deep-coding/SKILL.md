---
name: deep-coding
description: "Deep coding multi-agent development system. Use when the user wants to build software projects using the Orchestrator to Builder to Reviewer workflow, mentions deep coding, multi-agent collaboration, orchestrator, spawn builder, spawn reviewer, or asks for complex coding projects that need module decomposition and iterative review. NOT for: simple one-liner fixes (just edit), reading code, or single-file changes."
---

## System Dependencies

This skill requires the following system capabilities:

| Dependency | Purpose | Required? | Check |
|-----------|---------|-----------|-------|
| `python3` | Dashboard server (port 8765) | Yes | `python3 --version` |
| `node` / `npm` | Project builds, Playwright | For web projects | `node -v`, `npm -v` |
| `playwright` | E2E browser testing (Reviewers) | Optional, for E2E | `npx playwright --version` |
| ACP runtime | Builder/Reviewer agent execution | Optional, see below | Platform-specific |

**No specific coding agent is required.** The default configuration uses ACP + qoder, but you can use any available agent runtime. See [First-Time Setup](#first-time-setup) for configuration options.

## Security Notes

**⚠️ Dashboard server (`server.py`)**:
- Binds to `127.0.0.1:8765` only — never expose to public network
- Serves files from the project directory — verify no secrets (API keys, tokens) are present
- Includes path traversal protection via `safe_path()` check

**⚠️ Code execution**:
- Builders and Reviewers will **execute and run arbitrary project code**
- For web projects: HTTP server serves project files locally
- E2E tests use Playwright to open and interact with pages in a real browser
- **Only run on machines where executing generated code is acceptable**
- Use containers/VMs for untrusted projects

## First-Time Setup

When a user installs this skill for the first time, guide them through the following steps:

### Step 1: Create Project Workspace

```bash
mkdir -p my-projects/{requests/done,logs}
cp <skill-dir>/assets/server.py my-projects/
cp <skill-dir>/assets/dashboard.html my-projects/
cd my-projects
```

This creates the project root with all required directories and the Dashboard assets.

### Step 2: Configure Orchestrator Agent

Create an Orchestrator agent in your `openclaw.json` (or equivalent config):

```json
{
  "id": "orchestrator",
  "name": "Orchestrator",
  "workspace": "<your-path>/my-projects"
}
```

Give the Orchestrator a heartbeat prompt that references `references/orchestrator-rules.md`.

### Step 3: Configure Builder Agent(s)

Choose your preferred coding agent(s). Options:

| Option | Configuration | Notes |
|--------|--------------|-------|
| **ACP + qoder** | `runtime: "acp"`, `agentId: "qoder"` | Default, requires acpx plugin |
| **ACP + claude** | `runtime: "acp"`, `agentId: "claude"` | Alternative ACP agent |
| **ACP + codex** | `runtime: "acp"`, `agentId: "codex"` | OpenAI Codex |
| **Subagent runtime** | `runtime: "subagent"` | Built-in, no extra setup |
| **PTY coding agents** | `exec` with PTY | Claude Code, Codex CLI, etc. |

The Orchestrator rules (`references/orchestrator-rules.md`) default to ACP + qoder, but you should update the agent ID to match your setup.

**Recommended: Set up a 3-tier fallback chain**
1. Primary: Your preferred coding agent (e.g., qoder, claude)
2. Fallback 1: Alternative ACP agent (e.g., claude if qoder is 429'd)
3. Fallback 2: Built-in subagent runtime

### Step 4: Allow Tool Access

Ensure your Orchestrator and Builder agents have access to:
- `read`, `write`, `edit` — for file operations
- `exec` — for running builds, tests, servers
- `sessions_spawn`, `sessions_send`, `sessions_list` — for agent communication
- `subagents` — for managing spawned agents

In `openclaw.json`:
```json
{
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "orchestrator", "qoder-dev", "claude-dev"]
    }
  },
  "acp": {
    "enabled": true,
    "backend": "acpx",
    "defaultAgent": "qoder",
    "allowedAgents": ["qoder", "claude", "codex"]
  }
}
```

### Step 5: Choose Your LLM

Set the default model for the Orchestrator and agents:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "your-provider/your-model"
      }
    }
  }
}
```

For coding agents (qoder, claude, codex), they use their own model — no LLM config needed.

### Step 6: Verify Setup

```bash
cd my-projects
python3 server.py
# Open http://localhost:8765 — should show empty dashboard
```

---

# Harness Deep Coding System

Multi-agent development: Orchestrator decomposes → Builders code → Reviewers verify → E2E test → deliver.

## Roles

### User-Facing Agent (you)
- Gather requirements through conversation
- Create request JSON at `projects/requests/TIMESTAMP.json` (use actual timestamp)
- Notify Orchestrator via `sessions_send` to `agent:orchestrator:main`
- Report progress every heartbeat when project is active

### Orchestrator
- Decomposes project into 2-4 modules + mandatory integration-test
- Creates `project-state.json` with module states
- Spawns Builders and Reviewers via `sessions_spawn`
- Monitors progress via heartbeat, handles failures
- Runs E2E smoke test after bugfix/feature accepted

### Builder
- Codes independently per module
- Uses configured agent runtime (ACP subagent, or fallback)
- Writes to `logs/builder-MODULE.log` (APPEND, UTC+8)

### Reviewer
- MUST actually test the application, not just read code
- For web projects: serve via HTTP, verify in browser
- Writes detailed review results to `review_history`
- Writes to `logs/reviewer-MODULE.log` (APPEND, UTC+8)

## User-Facing Workflow

### 1. Gather Requirements
- What to build, key features, constraints, tech stack
- Break into 2-4 logical modules (data → core → render → UI)
- Auto-add final `integration-test` module depending on ALL others

### 2. Create Request
```json
{
  "name": "Project Name",
  "description": "What it does",
  "owner": "user name",
  "tags": ["web", "game"]
}
```
Path: `<project-root>/requests/TIMESTAMP.json` (use actual timestamp)

### 3. Notify Orchestrator
Send to `agent:orchestrator:main`:
- Request file path
- Instructions to decompose into modules
- Create project-state.json
- Spawn Builder for first module
- Use per-agent logs, APPEND mode, UTC+8
- Run E2E smoke test after acceptance

### 4. Progress Reporting
Read `project-state.json` every heartbeat:
- Report completion % and module states
- Announce 100% completion

## Project Structure

All paths are relative to your project root directory:

```
<project-root>/
├── projects-registry.json          ← All projects overview
├── server.py                       ← Dashboard server (port 8765)
├── dashboard.html                  ← Dashboard UI
├── requests/
│   └── done/                       ← Processed requests
├── logs/                           ← Agent activity logs
├── PROJECT-SLUG/
│   ├── project-state.json           ← Module states, review history
│   ├── logs/
│   │   ├── orchestrator.log         ← Orchestrator decisions
│   │   ├── builder-MODULE.log       ← Each Builder writes own file
│   │   └── reviewer-MODULE.log      ← Each Reviewer writes own file
│   └── SOURCE CODE (generated files)
```

See `references/architecture.md` for full project structure, module lifecycle, and dashboard details.

## Module Lifecycle

```
pending → in_progress → ready_for_review → in_review → accepted
                        ↑                    |
                        └── needs_revision ──┘
```

### Critical Rules

| Rule | Description |
|------|-------------|
| One action per heartbeat | Never do multiple spawns in one cycle |
| Spawn Reviewer immediately | Never leave `ready_for_review` more than one cycle |
| Reviewer writes results | Must write to `review_history` array, never just change state |
| E2E smoke test | Mandatory for bugfixes and new features before delivery |
| No archive copies | DO NOT copy project-state.json to archive/ |

## Common Issues

| Issue | Fix |
|-------|-----|
| 429 rate limit | Wait, then re-spawn. Do NOT self-accept |
| Missing E2E | Bugfix/feature accepted → must spawn E2E Reviewer |
| Reviewer not spawned | Check sessions_list, spawn if missing |
| Builder timeout | Check if files exist, accept if complete |
| Archive duplicates | Orchestrator should NOT copy to archive/ |

## Dashboard

Dashboard is included in `assets/server.py` and `assets/dashboard.html`.

**Usage:**
1. Copy `assets/server.py` and `assets/dashboard.html` to your project root directory
2. Run: `python3 server.py`
3. Open: `http://localhost:8765`

**Security:** The server binds to `127.0.0.1` only and includes path traversal protection.

Features: project list, completion status, module states, agent activity timeline.
