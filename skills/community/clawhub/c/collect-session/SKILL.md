---
name: collect-session
description: Install and configure the collect-session hook for OpenClaw. Automatically captures session telemetry (turns, tool calls, model usage, cost) and generates a named Markdown summary whenever /new or /reset is issued. Use when: (1) setting up session collection for the first time, (2) configuring the output directory or LiteLLM credentials, (3) running a backfill sweep of uncollected sessions, (4) troubleshooting the /new pre-hook not firing. Requires LiteLLM running locally for cost data and LLM-powered session naming/summarization.
---

# collect-session

Captures every session when `/new` or `/reset` is issued and writes a rich Markdown summary to disk. Useful for session findability, cost tracking, and building a searchable history of agent work.

## What it produces

For each session:
- `<output-dir>/sessions/YYYY-MM-DD-<slug>.md` — full session report (turns, tool calls, model usage, cost, LLM-generated name + summary)
- `<output-dir>/SESSION-INDEX.md` — append-only table of all collected sessions
- `<output-dir>/session-log.jsonl` — machine-readable record for analytics

## Prerequisites

- **LiteLLM running locally** — required for cost derivation and LLM enrichment. Verify with: `curl http://localhost:4000/health`
- **Node.js** — `node` must be in PATH
- **OpenClaw `workspace.dir`** — must be set in `openclaw.json` so the hook can find the script

## Installation

### Step 1 — Copy the script

Copy `scripts/collect-session.mjs` to your workspace scripts directory:

```bash
cp collect-session.mjs <workspace-dir>/scripts/collect-session.mjs
chmod +x <workspace-dir>/scripts/collect-session.mjs
```

### Step 2 — Configure the script

Edit the CONFIG block at the top of `collect-session.mjs`. Three values must be set:

```js
// Agent: set to your workspace memory directory
const OUTPUT_DIR_DEFAULT = process.env.COLLECT_SESSION_OUTPUT_DIR
  || path.join(os.homedir(), 'workspace', 'memory');

// Agent: verify this matches your LiteLLM port (default 4000)
const LITELLM_BASE = process.env.LITELLM_BASE_URL || 'http://localhost:4000';

// Agent: find your LiteLLM virtual key.
// Check your LiteLLM dashboard at http://localhost:4000/ui, or retrieve from 1Password/secrets manager.
// Prefer a low-cost key (cron/batch budget) — enrichment costs ~$0.0001/session with Gemini Flash.
const LITELLM_KEY = process.env.LITELLM_API_KEY || 'YOUR_LITELLM_VIRTUAL_KEY';
```

Alternatively, set environment variables: `COLLECT_SESSION_OUTPUT_DIR`, `LITELLM_API_KEY`, `LITELLM_BASE_URL`.

### Step 3 — Install the hook

Copy `scripts/hook-handler.ts` to your OpenClaw hooks directory and register it:

```bash
mkdir -p ~/.openclaw/hooks/collect-session
cp hook-handler.ts ~/.openclaw/hooks/collect-session/handler.ts
```

Create `~/.openclaw/hooks/collect-session/HOOK.md`:

```markdown
---
name: collect-session
description: "Collect and persist the current session to memory/sessions/ when /new or /reset is issued"
metadata:
  { "openclaw": { "emoji": "📦", "events": ["command:new", "command:reset"], "requires": { "bins": ["node"], "config": ["workspace.dir"] } } }
---
```

Then enable it in `openclaw.json` under `hooks.internal.entries`:

```json
"collect-session": {
  "enabled": true
}
```

Restart the gateway after making config changes.

### Step 4 — Verify

Issue `/new` in any session. You should see `[collect-session] ✅ Session collected` in gateway logs.

To check manually:
```bash
node <workspace-dir>/scripts/collect-session.mjs --no-llm
```

## Output path

Default output is `~/workspace/memory/`. Override with:
- Environment variable: `COLLECT_SESSION_OUTPUT_DIR=/path/to/dir`
- CLI flag: `node collect-session.mjs --output-dir /path/to/dir`
- Edit `OUTPUT_DIR_DEFAULT` in the script CONFIG block

## Backfill sweep

To collect all existing uncollected sessions:

```bash
node <workspace-dir>/scripts/collect-session.mjs --sweep
```

Add `--no-llm` to skip LLM enrichment (faster, uses heuristic names).

## CLI reference

| Flag | Description |
|---|---|
| *(no args)* | Collect most recent completed session |
| `<session-id>` | Collect specific session by ID or path |
| `--current` | Collect the currently active session (hook use) |
| `--sweep` | Collect all uncollected sessions |
| `--no-llm` | Skip LLM enrichment, use heuristic title |
| `--force` | Re-collect even if already in session-log.jsonl |
| `--output-dir <path>` | Override output directory |

## Troubleshooting

**Hook not firing on /new:** Check that `collect-session` is enabled in `openclaw.json` and the gateway was restarted. Look for `[collect-session]` lines in gateway logs.

**`LITELLM_API_KEY not configured` warning:** Set `LITELLM_API_KEY` env var or edit the CONFIG block. The script will fall back to heuristic titles but still write session files.

**Sessions directory not found:** The default sessions path is `~/.openclaw/agents/main/sessions`. If you use a custom agent name, update `SESSIONS_DIR` in the CONFIG block.

**Cost shows $0.0000:** LiteLLM returns zero cost for some providers. The script derives cost from token counts using a built-in pricing table. Add missing models to `MODEL_PRICING` in the CONFIG block.
