---
name: claw-memory-manager
description: >
  Manage OpenClaw Agent's built-in memory features — enable/disable/configure
  Dreaming (Light→REM→Deep auto memory consolidation) and Active Memory
  (proactive memory injection with three style presets: conservative /
  balanced / aggressive). Auto-detects K8s ConfigMap mirrors, creates
  *.bak.<timestamp> backups before write, supports --dry-run preview,
  --style preset for active-memory, --half-life / --max-age / --timezone
  for dreaming, and triggers gateway restart automatically (opt-out via
  --no-restart). Triggers: "enable dreaming", "tune memory half-life",
  "configure agent memory", "enable active memory", "switch memory style",
  "conservative/balanced/aggressive memory mode".
---

# Claw Memory Manager

- **Version**: 1.1.1
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills

Manage [OpenClaw](https://docs.openclaw.ai) Agent's built-in memory features
through one safe CLI: enable/disable, tune parameters, preview with dry-run,
auto-backup, and auto-restart.

## What it does

OpenClaw Agent has two **built-in memory features**:

1. **Dreaming** — scheduled job (default 03:00 local time) that scans your
   daily memory signals, scores them, and **auto-promotes high-recall items
   to long-term `MEMORY.md`**.
2. **Active Memory** — lightweight sub-agent that runs before every turn,
   retrieves relevant memories, and **injects them into the model context
   window** for better recall.

Both require editing nested config trees, syncing to multiple paths in
managed environments, and restarting the gateway. This skill does it all
in one command, safely.

## Supported features

| Feature | What | CLI flags |
|---------|------|-----------|
| `dreaming` | Light→REM→Deep three-phase memory consolidation | `--half-life`, `--max-age`, `--timezone` |
| `active-memory` | Proactive memory injection with style presets | `--style {conservative,balanced,aggressive}` |

See `references/features.md` for full schema details.

## Quick start — Dreaming

```bash
# Check OpenClaw support
python3 scripts/agent_memory.py check dreaming

# See current state
python3 scripts/agent_memory.py status dreaming

# Enable with defaults (half-life 30d, max-age 60d, timezone UTC)
python3 scripts/agent_memory.py enable dreaming

# Custom tuning
python3 scripts/agent_memory.py enable dreaming --half-life 14 --timezone America/New_York

# Preview only
python3 scripts/agent_memory.py enable dreaming --dry-run

# Disable
python3 scripts/agent_memory.py disable dreaming
```

## Quick start — Active Memory

```bash
# Enable with default style (balanced)
python3 scripts/agent_memory.py enable active-memory

# Pick a style preset
python3 scripts/agent_memory.py enable active-memory --style conservative
python3 scripts/agent_memory.py enable active-memory --style aggressive

# Inspect current style + parameters
python3 scripts/agent_memory.py status active-memory

# Preview only
python3 scripts/agent_memory.py enable active-memory --style aggressive --dry-run

# Disable
python3 scripts/agent_memory.py disable active-memory
```

### Active Memory style presets

| Style | Use case | queryMode | promptStyle | Context window | Inject cap | Timeout | Thinking |
|-------|----------|-----------|-------------|----------------|------------|---------|----------|
| `conservative` | Fastest, precision-focused | `message` | `precision-heavy` | user 1×120 / assist 0 | 150 chars | 8 s | off |
| **`balanced`** (default) | Everyday use | `recent` | `balanced` | user 2×220 / assist 1×180 | 220 chars | 15 s | off |
| `aggressive` | Best recall, larger context | `full` | `recall-heavy` | user 4×500 / assist 2×400 | 500 chars | 25 s | minimal |

Style is inferred back from `queryMode` when running `status active-memory`.

## CLI flags

| Flag | Applies to | Purpose | Default |
|------|-----------|---------|---------|
| `--half-life N` | dreaming | Signal decay half-life (1-90 days) | `30` |
| `--max-age N` | dreaming | Signal hard expiry (1-90 days) | `60` |
| `--timezone TZ` | dreaming | IANA timezone for schedule | `UTC` |
| `--style NAME` | active-memory | `conservative` / `balanced` / `aggressive` | `balanced` |
| `--dry-run` | all | Print planned changes; do not write | off |
| `--no-backup` | all | Skip `*.bak.<timestamp>` creation | off (backup on) |
| `--no-restart` | all | Skip `openclaw gateway restart` after change | off (auto-restart on) |

## Safety features

| Layer | Behavior |
|-------|----------|
| **Auto-backup** | Every write creates `openclaw.json.bak.<YYYYMMDD_HHMMSS>` (use `--no-backup` to opt out) |
| **Dry-run** | `--dry-run` prints exact JSON change + sync targets + restart action without touching disk |
| **Managed-env auto-detect** | `/app/clawconfig/` and `/app/k8s-config/clawconfig/` auto-detected — synced if present, silently skipped if not |
| **Validation** | Half-life and max-age ranges enforced (1-90); `--style` enforced by argparse choices |
| **Verify after write** | Re-reads config to confirm change took effect before reporting success |

## Configuration sources

The script reads/writes:

1. **Runtime config**: `~/.openclaw/openclaw.json` (or `$OPENCLAW_CONFIG`)
2. **Managed-environment mirrors** (auto-detected, optional):
   - `/app/clawconfig/openclaw.json` (Pod restart source in K8s)
   - `/app/k8s-config/clawconfig/openclaw.json` (K8s ConfigMap source)

If you run OpenClaw locally (e.g. `npm install -g openclaw` on your laptop),
only the runtime config exists and the script does the right thing
automatically.

## Why use this skill

Without this skill, enabling Active Memory requires:

1. Reading the OpenClaw plugins config schema
2. Editing nested JSON under `plugins.entries.active-memory` with **10+ fields**
3. Picking sensible defaults for `queryMode` / `promptStyle` / context windows
4. Copying to 2 mirror paths (in K8s environments)
5. Running `openclaw gateway restart`
6. Manually verifying

This skill: **one command + a style preset**, with backup + dry-run + verify built in.

## Extending to new memory features

Add a new entry to the `FEATURES` dict at the top of `agent_memory.py`:

```python
FEATURES["my-feature"] = {
    "path": ["plugins", "entries", "my-plugin", "config"],
    "enable_patch": {"enabled": True, ...},
    "disable_patch": {"enabled": False},
    "check_key": "enabled",
    "status_key": "frequency",  # field shown in `status`
    "description": "What this feature does",
}
```

For features with preset-style choices (like active-memory), follow the
`ACTIVE_MEMORY_STYLES` pattern and set `supports_style: True` in the entry.

## Files

```
claw-memory-manager/
├── SKILL.md              ← agent entry point
├── README.md             ← this file
├── LICENSE               ← MIT
├── .gitignore
├── scripts/
│   └── agent_memory.py   ← single Python entry, zero external deps
└── references/
    └── features.md       ← feature catalog + schema reference
```

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
## See also

- `references/features.md` — full feature catalog, config schemas, and extension guide
- [OpenClaw docs](https://docs.openclaw.ai) — platform reference
