# claw-memory-manager

> One-command management of OpenClaw Agent's built-in memory features —
> Dreaming consolidation **and** Active Memory injection.

## Why

[OpenClaw](https://docs.openclaw.ai) ships with two memory features that
both ship **disabled** and require non-trivial config to turn on:

1. **Dreaming** — scheduled memory consolidation that auto-promotes
   high-recall signals to `MEMORY.md`
2. **Active Memory** — sub-agent that runs before every turn and
   **injects relevant memories into the model's context window**

Without this skill, enabling either requires editing a 3-level nested JSON
config, syncing to multiple paths on managed deployments, and restarting
the gateway. **This skill turns each into one command.**

## What's Dreaming?

Each session your agent accumulates memory signals (things it recalled,
files it read, concepts it tagged). Most decay. But high-recall, high-context
items deserve to be **promoted to long-term `MEMORY.md`** so they survive
context resets.

Dreaming is a scheduled job that does that promotion automatically:

```
Light phase  → scan today's signals, score them
REM phase    → simulate recall, weight by frequency × recency × diversity
Deep phase   → top-scoring signals get written into MEMORY.md
```

Default schedule: 03:00 daily. Default half-life: 30 days.

## Quick start

### Dreaming

```bash
# Check if your OpenClaw version supports dreaming
python3 scripts/agent_memory.py check dreaming

# See current state (enabled / disabled / params)
python3 scripts/agent_memory.py status dreaming

# Preview what enable would do (no writes)
python3 scripts/agent_memory.py enable dreaming --dry-run

# Enable with safe defaults (auto-backup, auto-restart)
python3 scripts/agent_memory.py enable dreaming

# Enable with custom params
python3 scripts/agent_memory.py enable dreaming \
    --half-life 14 \
    --max-age 30 \
    --timezone America/New_York

# Disable
python3 scripts/agent_memory.py disable dreaming
```

### Active Memory

```bash
# Enable with default style (balanced)
python3 scripts/agent_memory.py enable active-memory

# Pick a style preset
python3 scripts/agent_memory.py enable active-memory --style conservative
python3 scripts/agent_memory.py enable active-memory --style aggressive

# See current style + params
python3 scripts/agent_memory.py status active-memory

# Disable
python3 scripts/agent_memory.py disable active-memory
```

#### Style cheatsheet

| Style | When to use | Latency | Recall |
|-------|-------------|---------|--------|
| `conservative` | Fastest direct-chat, tight context budget | ~8 s | low |
| **`balanced`** (default) | Everyday dev / assistant | ~15 s | medium |
| `aggressive` | Long-context research / max-recall tasks | ~25 s | high |

See `references/features.md` for the full parameter matrix.

## Safety by default

| Layer | Behavior |
|-------|----------|
| **Backup** | Every write creates `openclaw.json.bak.<timestamp>` (opt out: `--no-backup`) |
| **Dry-run** | `--dry-run` shows exact JSON change + sync targets + restart plan |
| **Validate** | Half-life and max-age are range-checked (1-90 days) |
| **Auto-detect K8s** | Mirror paths (`/app/clawconfig/`, `/app/k8s-config/...`) auto-detected; no flag needed |
| **Verify** | After write, re-reads config to confirm before declaring success |
| **Restart** | Auto-runs `openclaw gateway restart` to apply (opt out: `--no-restart`) |

## Supported features

| Feature | Status | Style/preset support |
|---------|--------|----------------------|
| `dreaming` (memory consolidation) | ✅ Production | `--half-life` / `--max-age` / `--timezone` |
| `active-memory` (proactive injection) | ✅ Production (v1.1.0+) | `--style conservative\|balanced\|aggressive` |

To add a new feature, see the "Extending" section in
`references/features.md`.

## Requirements

- Python 3.8+
- OpenClaw 2026.4.24+ installed (`openclaw --version` to check)
- Write access to `~/.openclaw/openclaw.json`

Zero third-party Python dependencies (stdlib only).

## How it interacts with OpenClaw

The skill modifies one of three config files based on your environment:

| Environment | Path |
|-------------|------|
| Local install (`npm install -g openclaw`) | `~/.openclaw/openclaw.json` |
| Managed K8s Pod | Above + `/app/clawconfig/openclaw.json` + `/app/k8s-config/clawconfig/openclaw.json` |

The latter two mirrors exist because K8s Pods restore config from
ConfigMap on restart. The script syncs to all paths that exist, silently
skips ones that don't.

After write, it runs `openclaw gateway restart` to make changes take effect.

## Files

```
claw-memory-manager/
├── SKILL.md              ← agent-facing documentation
├── README.md             ← this file (human-facing)
├── LICENSE               ← MIT
└── scripts/
    └── agent_memory.py   ← single Python script, 400 LOC
└── references/
    └── features.md       ← feature catalog + schemas + extension guide
```

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
