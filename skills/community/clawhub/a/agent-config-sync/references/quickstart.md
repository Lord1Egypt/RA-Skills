# Quickstart — agent-config-sync for New Users

**5-minute setup** to keep configuration consistent across all your OpenClaw agents.

---

## Before You Start

You need:
- OpenClaw running with 2+ agents
- A "master" agent that coordinates others
- `clawhub` CLI installed

### Example Setup (Alice)

Alice has 3 agents:

| Agent ID | Purpose | Workspace |
|----------|---------|-----------|
| `alice-dev` | Software development | `~/.openclaw/workspace-alice-dev` |
| `alice-biz` | Business analysis | `~/.openclaw/workspace-alice-biz` |
| `alice-ops` | Operations & scheduling | `~/.openclaw/workspace-alice-ops` |

Alice uses `alice-ops` as her master/coordination agent.

We'll use Alice's setup as a concrete example throughout this guide.

---

## Step 1: Install the Skill

```bash
clawhub install agent-config-sync
```

This installs to `~/.openclaw/skills/agent-config-sync/`.

---

## Step 2: Customize the Agent Registry

Edit `~/.openclaw/skills/agent-config-sync/references/agent-registry.json` to match your agents:

```json
{
  "version": "1.2",
  "vars": {
    "workspace_root": "~/.openclaw",
    "master_agent": "alice-ops",
    "master_memory": "${vars.workspace_root}/workspace-${vars.master_agent}/memory"
  },
  "agents": {
    "alice-dev": {
      "name": "Alice Dev",
      "role": "Software Development",
      "workspace": "${vars.workspace_root}/workspace-alice-dev"
    },
    "alice-biz": {
      "name": "Alice Biz",
      "role": "Business Analysis",
      "workspace": "${vars.workspace_root}/workspace-alice-biz"
    },
    "alice-ops": {
      "name": "Alice Ops",
      "role": "Coordination",
      "workspace": "${vars.workspace_root}/workspace-alice-ops"
    }
  }
}
```

> **Key**: Change `master_agent` in `vars` and replace all agent entries under `agents`. Scripts read from this file — this is the **only place** you need to configure agent names.

---

## Step 3: Initialize Sync Infrastructure

```bash
cd ~/.openclaw/skills/agent-config-sync

# Preview what will be created (safe, makes no changes)
bash scripts/init_sync.sh --dry-run

# Run the actual setup
bash scripts/init_sync.sh
```

This creates:
- Version sentinel files in your master agent's `memory/` directory
- `CHANGELOG.md` with structured format
- `.sync_journal.jsonl` for sync atomicity
- `SYNC.md`, bootstrapped `BOOTSTRAP.md`, and `HEARTBEAT.md` sync checks in each agent workspace

---

## Step 4: Add HEARTBEAT Item to Master Agent

Add this to your master agent's `HEARTBEAT.md`:

```markdown
12. ⭐ **Config Change Sync** — Check for unsynchronized system/config changes
    - **Sentinel**: `memory/.last_sync_version`
    - Compare against `memory/.current_system_version` on every heartbeat
    - If version mismatch detected → dispatch to all downstream agents:
      a. Read latest section from `memory/CHANGELOG.md`
      b. `sessions_send` to each agent (or write `pending_sync_<VERSION>_<SHA>.md` as fallback)
      c. Record results in `.sync_journal.jsonl`
    - On success → update `memory/.last_sync_version` = `memory/.current_system_version`
    - Sync failure does NOT block heartbeat — logged to journal only
```

See `references/sync-setup.md` for the full specification.

---

## Step 5: Verify

```bash
# Check version files were created
cat ~/.openclaw/workspace-alice-ops/memory/.current_system_version
# Expected: v1.0

cat ~/.openclaw/workspace-alice-ops/memory/.last_sync_version
# Expected: v1.0

# Check agent sync files exist
ls ~/.openclaw/workspace-alice-dev/SYNC.md ~/.openclaw/workspace-alice-biz/SYNC.md
# Both should exist
```

---

## Step 6: Test a Sync

```bash
# Bump version to trigger sync on next heartbeat
echo "v1.1" > ~/.openclaw/workspace-alice-ops/memory/.current_system_version

# Or use the force_sync helper:
bash ~/.openclaw/skills/agent-config-sync/scripts/force_sync.sh \
  ~/.openclaw/workspace-alice-ops/memory v1.0 v1.1
```

The next heartbeat on your master agent will detect the version mismatch and dispatch config changes to all agents.

---

## Customizing Further

### Change master memory path

If your master agent stores memory elsewhere, update `vars.master_memory` in `.agent_registry`:

```json
"vars": {
  "master_memory": "/custom/path/to/memory"
}
```

### Use as non-master agent

The skill's sync reception is agent-side: each agent checks for `pending_sync_*.md` files on startup (BOOTSTRAP) and every heartbeat (HEARTBEAT). The `init_sync.sh` script sets this up automatically.

### Language

Scripts support Chinese and English output:

```bash
bash scripts/init_sync.sh --lang en    # English output
bash scripts/init_sync.sh --lang zh    # Chinese output (default)
```

---

## Troubleshooting

| Problem | Check |
|---------|-------|
| "Registry not found" in init_sync | Run from skill directory: `cd ~/.openclaw/skills/agent-config-sync` |
| Agents not receiving syncs | Verify master agent has HEARTBEAT item 12 |
| `pending_sync` files pile up | Agent may not have BOOTSTRAP sync check — re-run `init_sync.sh` |
| Path errors | Check `vars.workspace_root` in `agent-registry.json` — expand `~` to full path if needed |

---

## Next Steps

- Read `SKILL.md` for architecture overview and daily operations
- Read `references/sync-setup.md` for HEARTBEAT implementation details
- Read `references/sync-journal.md` for the two-phase commit mechanism
