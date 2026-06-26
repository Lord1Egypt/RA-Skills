---
name: agent-config-sync
description: |-
  Synchronize configuration versions across OpenClaw multi-agent deployments.
  Tracks changes in a master workspace using sentinel version files and CHANGELOG,
  then dispatches to downstream agents via sessions_send or file-based pending_sync
  fallback. Each agent independently checks for updates on startup (BOOTSTRAP.md)
  and heartbeat (HEARTBEAT.md). Designed for users running 2+ specialized agents
  who need consistent system/agent/OpenClaw configurations.
  Triggers on: sync, configure, version management, multi-agent coordination.
---

# Agent Config Sync (v1.5)

Keep configuration consistent across multiple OpenClaw agents using version tracking, CHANGELOG-based change detection, and automatic sync dispatch with journal-backed two-phase commit.

> **⚡ Quick Start (30 seconds to running):**
> ```bash
> # Step 1: Install
> clawhub install agent-config-sync
>
> # Step 2: Run setup wizard (interactive, no manual editing needed)
> cd ~/.openclaw/skills/agent-config-sync
> bash scripts/wizard.sh
>
> # Step 3: Done! 🎉
> #    - Agent registry auto-detected
> #    - Sync infrastructure created
> #    - HEARTBEAT integration added
> #    - All agents ready to receive syncs
> ```
> 
> **Non-interactive?** Use `bash scripts/wizard.sh --auto` to auto-detect everything.
> 
> **Prefer manual?** See [Installation](#installation) below for step-by-step instructions.
>
> **New in v1.5**: Interactive setup wizard (`scripts/wizard.sh`), `--auto` mode for init_sync.sh (zero-config auto-detection), enhanced SYNC.md with quick start guide and cheat sheet, simplified onboarding.
>
> **New in v1.4**: Full version conflict management — dispatch lock, loop detection, self-upgrade isolation, batch mode, rollback snapshots, TTL-based expiry, offline catch-up, and agent-side version collapse. See [Version Conflict Management](#version-conflict-management-v14) for details.
>
> **Security**: This skill writes to agent workspaces across your OpenClaw deployment. Read the full [SECURITY.md](SECURITY.md) for permission scope, path validation, cross-agent isolation, and user consent flow. Key highlights:
> - All scripts require `--confirm` for write operations (use `--dry-run` to preview first)
> - Only paths under `~/.openclaw/workspace-*` are allowed (path validation enforced)
> - Each agent can only read/write its own workspace files
> - No network access, no external API calls, no credential access

## ⚙️ Customization Variables

**Option A (Recommended): Run the setup wizard**
```bash
cd ~/.openclaw/skills/agent-config-sync
bash scripts/wizard.sh
```
The wizard auto-detects your agents and generates `agent-registry.json` — no manual editing.

**Option B: Manual configuration**

Edit `references/agent-registry.json` — this is the only file you need to change for your deployment:

| Variable | Location | Example | Description |
|----------|----------|---------|-------------|
| `workspace_root` | `vars` in registry | `~/.openclaw` | Base path for all agent workspaces |
| `master_agent` | `vars` in registry | `amaster` | ID of your coordination/master agent |
| `master_memory` | `vars` in registry | `${workspace_root}/workspace-amaster/memory` | Path to master's memory directory |
| (each agent) | `agents` in registry | See below | Add/remove/rename agents to match your setup |

**Example** — after customization for user "Alice" with agents `alice-dev`, `alice-biz`, `alice-ops`:

```json
{
  "vars": {
    "workspace_root": "~/.openclaw",
    "master_agent": "alice-ops",
    "master_memory": "${vars.workspace_root}/workspace-${vars.master_agent}/memory"
  },
  "agents": {
    "alice-dev": { "name": "Alice Dev", "role": "Development",
      "workspace": "${vars.workspace_root}/workspace-alice-dev" },
    "alice-biz": { "name": "Alice Biz", "role": "Business",
      "workspace": "${vars.workspace_root}/workspace-alice-biz" },
    "alice-ops": { "name": "Alice Ops", "role": "Coordination",
      "workspace": "${vars.workspace_root}/workspace-alice-ops" }
  }
}
```

Scripts resolve `${vars.xxx}` placeholders at runtime — no hardcoded paths.

---

## Overview

### Architecture

```
┌─ Version Tracking ──────────────────────┐
│  .current_system_version  (monotonic)    │
│  .last_sync_version       (last synced)  │
│  CHANGELOG.md             (structured)   │
│  .sync_journal.jsonl      (atomicity)    │
└──────────────────────────────────────────┘
         │ version mismatch detected by HEARTBEAT
         ▼
┌─ Sync Journal (two-phase commit) ────────┐
│  PREPARE → journal entry written          │
│  DISPATCH → sessions_send / pending_sync  │
│  COMMIT → mark done or retry later        │
└──────────────────────────────────────────┘
         │ each agent processes independently
         ▼
┌─ Agent Side ────────────────────────────┐
│  BOOTSTRAP.md → ls pending_sync_*.md    │
│  HEARTBEAT.md → check + verify SHA256   │
│  SYNC.md → manual sync instructions     │
└──────────────────────────────────────────┘
```

### What it syncs

| Type | Examples |
|:----:|----------|
| 🖥️ System code | Quant system, price compare, data pipelines |
| 🤖 Agent config | SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md |
| ⚙️ OpenClaw config | Models, skills, service addresses, plugins |
| 🎯 Task config | API keys, cron jobs, data sources, ports |

---

## Installation

### Prerequisites

- OpenClaw with 2+ agents
- One designated "master" coordination agent
- `clawhub` CLI installed

### Option A: Interactive Wizard (Recommended for New Users)

```bash
clawhub install agent-config-sync
cd ~/.openclaw/skills/agent-config-sync
bash scripts/wizard.sh
```

The wizard walks you through:
1. Environment detection (auto-finds your agents)
2. Registry configuration (auto-generates from your workspace)
3. Infrastructure initialization (one click)
4. HEARTBEAT integration (auto-appended)
5. Completion report (status summary + next steps)

### Option B: One-Command Auto Setup

```bash
clawhub install agent-config-sync
bash ~/.openclaw/skills/agent-config-sync/scripts/init_sync.sh --auto
```

Auto-detects all agent workspaces, generates registry, and initializes everything — zero prompts.

### Option C: Manual Step-by-Step

#### Step 1: Install the Skill

```bash
clawhub install agent-config-sync
```

#### Step 2: Customize Agent Registry

Edit `~/.openclaw/skills/agent-config-sync/references/agent-registry.json`:

1. Change `vars.master_agent` to your coordination agent's ID
2. Replace the `agents` entries with your own agents
3. Adjust `vars.workspace_root` if your OpenClaw workspace is not `~/.openclaw`

See the [Customization Variables](#️-customization-variables) table above, or the English quickstart at `references/quickstart.md`.

#### Step 3: Initialize Sync Infrastructure

```bash
cd ~/.openclaw/skills/agent-config-sync

# Preview what will be created (safe, no changes required)
bash scripts/init_sync.sh --dry-run

# Run the real setup (--confirm required for write operations)
bash scripts/init_sync.sh --confirm
```

> ⚠️ **Safety**: `--confirm` is **required** for any write operation. Without it, the script exits with a prompt explaining how to preview with `--dry-run` first. `--dry-run` mode does not need `--confirm`.

This creates:
- Version sentinel files (`.current_system_version`, `.last_sync_version`) in master's `memory/`
- `CHANGELOG.md` with structured format
- `.sync_journal.jsonl` for sync atomicity
- `SYNC.md`, bootstrapped `BOOTSTRAP.md`, and `HEARTBEAT.md` sync checks in each agent workspace

#### Step 4: Add HEARTBEAT Item to Master Agent

Copy the HEARTBEAT item from `references/sync-setup.md` into your master agent's `HEARTBEAT.md`. This is **item 12** — the heartbeat check that detects version mismatches and dispatches syncs.

#### Step 5: Verify Setup

```bash
# Check version files
cat ~/.openclaw/workspace-<master>/memory/.current_system_version  # should be v1.0

# Check agent sync files
ls ~/.openclaw/workspace-*/SYNC.md
```

---

## Version Conflict Management (v1.4)

### Conflict Types

| Type | Scenario | Frequency | Impact |
|:-----|:---------|:---------:|:------:|
| **Concurrent Change** | Two agents submit version changes simultaneously | High | Medium |
| **Cross-Session Stale** | Agent restarts and finds outdated `pending_sync` files | Medium | Low |
| **Offline Catch-Up** | Agent misses one or more sync cycles | Medium | High |
| **Self-Reference (Self-Upgrade)** | agent-config-sync's own files need updating | Low | High |
| **Multi-Agent Coordination** | Change requires specific ordering across agents | Medium | Medium |
| **Rollback** | Need to revert a problematic version change | Low | High |

### Conflict Detection Mechanisms

| Mechanism | Location | What It Detects |
|:----------|:---------|:----------------|
| Version Sentinel Comparison | Master HEARTBEAT item 12 | `.current_system_version` ≠ `.last_sync_version` |
| Dispatch Lock | Master HEARTBEAT item 12 | Concurrent dispatch prevention (< 2min window) |
| Loop Detection | Master HEARTBEAT item 12 | 3+ consecutive same-version journal records |
| TTL Expiry Check | Agent BOOTSTRAP/HEARTBEAT | `now > 过期时间` → delete stale pending_sync |
| Version Folding | Agent side | Multiple `pending_sync_*.md` files → fold by version |
| `.agent_sync_version` Gap | Agent side | Local version < current system version → offline gap |
| Self-Protect Blacklist | Master dispatch | CHANGELOG impact range includes sync's own files |
| Snapshot Verification | Agent rollback | SHA256 checksums on restored files |

### Agent-Side Pending Sync Priority Matrix

When an agent discovers multiple `pending_sync_*.md` files, it processes them in this order:

```
Priority   Type              Handle
─────────  ────────────────  ──────────────────────────────
1 (first)  Expired files     Delete immediately (now > 过期时间)
2          Superseded files  Delete (lower version number, depends_on chain covered)
3          Isolated syncs    Must process before normal syncs (self-upgrade isolation)
4          Revert syncs      Revert to target version from snapshot
5 (last)   Normal syncs      Apply in version order, respecting depends_on chain
```

**Version Collapse Rule**: If multiple `pending_sync_v3.1`, `pending_sync_v3.2`, `pending_sync_v3.3` exist AND v3.3's `**前置**` chain covers all intermediate versions → apply only v3.3 and delete v3.1/v3.2.

### Version Folding Algorithm

```
Agent discovers pending_sync_*.md files:

1. 删除已过期的文件（生成时间 > TTL，默认 24h）
2. 删除已被 supersede 的文件（版本号更低，且被更新版本的 depends_on 链覆盖）
3. 对剩余文件按版本号排序 → 从最早的开始执行
4. 如果文件头包含 "前置" 依赖 → 先检查前置是否已处理
   - 若前置未处理 → 按依赖链逐步升级
   - 若前置已处理 → 可直接应用
5. 应用变更前创建前置快照（memory/.sync_snapshots/<VERSION>_pre/）
6. 应用变更后更新 .agent_sync_version
7. 删除已处理的 pending_sync 文件
```

---

## Agent-Side Version Collapse (v1.4)

### Overview

When an agent discovers multiple `pending_sync_*.md` files (e.g., after being offline or during a period of rapid changes), it uses version collapse to avoid processing every intermediate version. The goal is to safely "jump" from the agent's current version to the latest applicable version in a single step.

### Decision Flow

```
Agent discovers N pending_sync_*.md files (N ≥ 1):

1. PARSE all file headers:
   - Extract: 版本, 前置, 生成时间, 过期时间, 类型

2. CLEANUP expired:
   FOR EACH file:
     IF now > 过期时间:
       DELETE file
       LOG "Stale sync expired: <filename>"

3. DETECT superseded:
   SORT remaining files by 版本 DESC
   FOR EACH file from latest to earliest:
     Walk depends_on chain from latest version
     IF current version is in chain → all older files are superseded
     DELETE all files whose version < latest_version AND covered by chain

4. CLASSIFY remaining files:
   GROUP by 类型:
     - isolated_sync → process BEFORE normal syncs
     - revert_sync → restore from snapshot
     - pending_sync → normal version upgrade

5. ORDER execution:
   isolated_sync files (ascending version)
   ↓
   revert_sync files (ascending target version)
   ↓
   normal pending_sync files (ascending version, respecting depends_on chain)

6. EXECUTE each file:
   a. CHECK depends_on: IF 前置 > .agent_sync_version → ERROR (chain broken, request Master)
   b. CREATE snapshot: mkdir .sync_snapshots/<VERSION>_pre/ + backup affected files
   c. APPLY changes from CHANGELOG
   d. UPDATE .agent_sync_version = 版本
   e. DELETE processed file

7. VERIFY:
   Check .agent_sync_version matches latest processed version
   Confirm no remaining pending_sync files (or that remaining files have valid depends_on > current)
```

### Version Comparison

```
Version format: v<MAJOR>.<MINOR>[.<PATCH>]

is_newer("v3.2", "v3.1") → true   (MINOR increment)
is_newer("v3.2.1", "v3.2") → true (PATCH increment)
is_newer("v3.1", "v3.2") → false
is_newer("v4.0", "v3.9") → true   (MAJOR increment)
is_same("v3.1", "v3.1") → true
```

### Edge Cases

| Case | Behavior |
|------|----------|
| Single pending file | Direct application (no collapse needed) |
| Chain broken (v3.1, v3.3 but no v3.2 dependency) | Process v3.1 first, then v3.3 |
| Chain complete (v3.1 depends v3.0; v3.3 depends v3.1) | Jump directly to v3.3 |
| Mixed types (pending + revert) | Revert takes priority; if revert target > current, normal syncs after |
| Corrupt file (unparseable header) | Skip, log error, request Master re-dispatch |
| Same version, 2 files (duplicate) | Keep newest by 生成时间, delete older |

---

## Self-Upgrade Isolation (v1.4)

### Problem

agent-config-sync's own files (SKILL.md, scripts/, SECURITY.md, etc.) may need updating. But if the sync system dispatches changes to itself through normal channels, it can trigger self-referential sync loops.

### Solution: Isolated Sync Flow

When a CHANGELOG entry's impact range includes paths in the `self_protect.blacklist`:

1. **Detection**: Master HEARTBEAT item 12 checks if the change affects agent-config-sync itself
2. **Isolation**: Generates `isolated_sync_<VERSION>_<SHA>.md` in Master's `memory/` directory
3. **Notification**: Appends a notice to each agent's `BOOTSTRAP.md` (not dispatched via normal flow)
4. **Agent Action**: On next startup, agent detects the BOOTSTRAP notice and requests the isolated sync
5. **No sentinel file**: Does not use `pending_sync` file mechanism — avoids normal dispatch loop

### Configuration

Configured in `agent-registry.json`:

```json
"self_protect": {
  "enabled": true,
  "skip_agents": ["agent-config-sync"],
  "isolated_sync": true,
  "blacklist": ["HEARTBEAT.md", "BOOTSTRAP.md", "SKILL.md", "scripts/", "SECURITY.md", "references/"],
  "sync_own_version_file": "skills/agent-config-sync/.sync_own_version",
  "allow_bootstrap_only": true
}
```

### Self-Protect Blacklist

Paths listed in `blacklist` are quarantined from normal dispatch. Any CHANGELOG entry affecting these paths triggers the isolated sync flow instead.

---

## Batch Mode (v1.4)

### Overview

When multiple rapid changes occur within a time window, batch mode merges them into a single cumulative dispatch instead of triggering one sync per version.

### Configuration

```json
"batch": {
  "mode": "auto",
  "window_sec": 300
}
```

### Behavior

1. HEARTBEAT detects version mismatch
2. Instead of immediate dispatch, opens a batch window (default: 5 min)
3. All version bumps within the window are accumulated
4. When window closes → merge all changes into one `pending_sync` file
5. Uses highest version number among batched changes
6. Combines all CHANGELOG sections

### Merge Rules

- Sort all batched versions → use the highest version
- Concatenate CHANGELOG entries in version order
- Generate single SHA256 signature over combined content
- Single dispatch covers all intermediate changes

---

## Rollback Mechanism (v1.4)

### Overview

When a version change causes problems, the system supports controlled rollback to a previous version using pre-sync snapshots.

### Rollback Flow

```
1. TRIGGER (Master):
   - Set .current_system_version to the rollback target version
   - HEARTBEAT detects: current < last_sync → recognizes as rollback
   - Creates revert_sync_<FROM>_to_<TO>_<SHA>.md in each agent workspace

2. APPLY (Agent):
   - Detects revert_sync file on HEARTBEAT/BOOTSTRAP check
   - Restores files from memory/.sync_snapshots/<TARGET>_pre/
   - Verifies SHA256 checksums from snapshot_manifest.json
   - Updates .agent_sync_version to target version
   - Deletes revert_sync file

3. VERIFY (All):
   - .current_system_version == .last_sync_version (stable state)
   - No pending_sync or revert_sync files remain
```

### Snapshot Directory Structure

```
memory/.sync_snapshots/
├── v3.2_pre/
│   ├── TOOLS.md.bak
│   ├── SOUL.md.bak
│   ├── AGENTS.md.bak
│   └── snapshot_manifest.json
└── v3.3_pre/
    ├── config.json.bak
    └── snapshot_manifest.json
```

### snapshot_manifest.json Format

```json
{
  "sync_version": "v3.2",
  "snapshot_time": "2026-05-16T08:30:00Z",
  "previous_version": "v3.1",
  "files": {
    "TOOLS.md": "sha256:a1b2c3...",
    "SOUL.md": "sha256:d4e5f6..."
  }
}
```

### Rollback Safety

- **Pre-condition**: Agent must have a snapshot directory matching the target rollback version
- **SHA256 verification**: All restored files verified against snapshot manifests
- **No partial rollback**: Atomic restore (all files succeed or none)
- **Loop prevention**: Rollback records are `type=revert` — not re-triggered by normal dispatch
- **Manual confirmation**: Requires explicit version bump to trigger

---

## Configuration

### Agent Registry (`references/agent-registry.json`)

The single source of truth. Fields:

| Field | Description |
|-------|-------------|
| `vars.workspace_root` | Root directory for all agent workspaces |
| `vars.master_agent` | ID of the coordination agent (sends syncs) |
| `vars.master_memory` | Path to master's memory directory (uses placeholders) |
| `agents.<id>.name` | Display name (English) |
| `agents.<id>.name_zh` | Display name (Chinese) — optional |
| `agents.<id>.role` | Short role description |
| `agents.<id>.workspace` | Path to agent workspace (uses `${vars.workspace_root}`) |
| `sync.*` | Sync behavior config (sentinel filenames, prefix, limits) |

### CHANGELOG Format

All version entries must follow the structured format defined in `references/sync-setup.md`:

```markdown
## vX.Y (YYYY-MM-DD)
**Change Type**: <category>
**Affected Agents**: <which agents>
**Author**: <who made the change>
**Priority**: normal | high | critical

### Added / Changed / Deprecated
- <description>
```

### Language

Scripts support `--lang en` and `--lang zh` (default). Use `--lang en` for English output:

```bash
bash scripts/init_sync.sh --lang en
bash scripts/force_sync.sh --lang en ~/memory v1.0 v1.1
```

---

## Usage Scenarios

### Scenario A: Adding a new model to all agents

**Situation**: You want all agents to switch to a new default model.

1. Update `CHANGELOG.md` in master's memory directory:
   ```markdown
   ## v3.2 (2026-05-16)
   **Change Type**: ⚙️ OpenClaw Config
   **Affected Agents**: all
   **Author**: AMaster
   **Priority**: high

   ### Changed
   - Default model switched to deepseek-v4-pro for all agents
   - Fallback model set to deepseek-v3
   ```

2. Bump the version:
   ```bash
   echo "v3.2" > memory/.current_system_version
   ```

3. Next HEARTBEAT (every 5 min): version mismatch detected → dispatches to all agents. Agents update their model configs accordingly.

4. Agents delete their `pending_sync_v3.2_<sha>.md` after applying.

### Scenario B: Coordinated code deployment

**Situation**: You fix a bug in shared code used by multiple agents.

1. Fix the bug, tell the master agent to record the change.

2. Master updates `CHANGELOG.md` with the version entry, bumps `.current_system_version`.

3. HEARTBEAT dispatches. Online agents receive via `sessions_send`; offline agents get `pending_sync` files.

4. All agents verify version before running the shared system.

---

## Daily Operations

### Recording a Change

Whenever a config or system change affects multiple agents:

1. **Edit `CHANGELOG.md`** in master's `memory/` directory — add a new `## vX.Y` section
2. **Bump the version** — `echo "vX.Y" > memory/.current_system_version`
3. The change is dispatched automatically on the next master heartbeat

### Force-Syncing Immediately

```bash
cd ~/.openclaw/skills/agent-config-sync

# Preview the version change
bash scripts/force_sync.sh --dry-run ~/.openclaw/workspace-<master>/memory v3.0 v3.1

# Execute (--confirm required for write operations)
bash scripts/force_sync.sh --confirm ~/.openclaw/workspace-<master>/memory v3.0 v3.1
```

After running, the next heartbeat detects `current (v3.1) != last_sync (v3.0)` and dispatches.

### Checking Sync Status

```bash
# Check version sentinel files
cat ~/.openclaw/workspace-<master>/memory/.current_system_version
cat ~/.openclaw/workspace-<master>/memory/.last_sync_version

# Check journal for recent sync records
tail -5 ~/.openclaw/workspace-<master>/memory/.sync_journal.jsonl

# Check for pending syncs on an agent
ls ~/.openclaw/workspace-<agent>/pending_sync_*.md
```

### Demo Mode (Learning)

```bash
cd ~/.openclaw/skills/agent-config-sync
bash scripts/init_sync.sh --demo --lang en
```

Creates a complete demo deployment in `/tmp/` showing the full file structure without touching real workspaces.

---

## Manual Sync Trigger

```bash
bash skills/agent-config-sync/scripts/force_sync.sh \
  ~/.openclaw/workspace-amaster/memory v3.0 v3.1
```

This creates a version mismatch (old=3.0, new=3.1) — next heartbeat dispatches.

---

## Troubleshooting

### Agents Not Receiving Updates

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No dispatch on heartbeat | HEARTBEAT item 12 not added to master | Follow `references/sync-setup.md` exactly; verify grep `agent-config-sync` in master's HEARTBEAT.md |
| Dispatched but not processed | Agent missing BOOTSTRAP sync check | Re-run `init_sync.sh` for that agent's workspace |
| `pending_sync` files piling up | Agent never deletes after processing | Check agent's HEARTBEAT.md has sync check with delete step |
| Same version synced repeatedly | `.last_sync_version` not updated | Run `force_sync.sh` to reset, or check journal for stale records |
| Version sentinel files (`.current_system_version`, `.last_sync_version`) are read-only | Accidental `chmod 444` or permission inheritance | **All writes silently fail** — version appears unchanged. Fix: `chmod 664 memory/.current_system_version memory/.last_sync_version` |
| Dispatched but log says "permission denied" | Sentinel files or journal files have wrong ownership | `ls -la memory/.current_system_version memory/.last_sync_version memory/.sync_journal.jsonl` → verify writable by the user running OpenClaw |

### Version Conflicts

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Wrong version on agent | Partial sync interrupted | Check journal for `status=prepared` records; master re-dispatches on next heartbeat |
| Multiple `pending_sync` files | Back-to-back changes | Process latest version first; all files are cumulative |
| SHA256 verification fails | File tampered or truncated | Request master to re-dispatch that version |
| "Backup failed" in force_sync | Memory dir permission issue | `chmod 755 memory/` and retry |

### Journal Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Stale prepared records (>24h) | Agent was offline too long | Mark as abandoned in journal, re-trigger sync with `force_sync.sh` |
| Journal growing too large | Many sync records | Archive old `committed` entries periodically |
| Corrupt journal line | Partial write or disk issue | Delete the last line (corrupt), re-trigger sync |

### Rolling Back a Change

To undo a sync that was dispatched but shouldn't have been:

1. **Revert the version**: `echo "v3.0" > memory/.current_system_version` (back to previous)
2. **Revert the last_sync**: `echo "v3.0" > memory/.last_sync_version`
3. **Mark the journal record**: Edit `.sync_journal.jsonl`, find the record with `"to":"v3.1"` and change `status` to `"reverted"`
4. **Notify agents**: Agents check `pending_sync` files on heartbeat — delete old ones
5. **Verify**: `ls ~/.openclaw/workspace-*/pending_sync_*.md` should be empty

Alternatively, use `force_sync.sh` in "reverse":

```bash
bash scripts/force_sync.sh memory/ v3.0 v3.1   # created mismatch forward
bash scripts/force_sync.sh memory/ v3.1 v3.0   # reverse: current=v3.0, last=v3.1 → no dispatch (current < last)
```

> ⚠️ `force_sync.sh` only creates the version mismatch — actual rollback requires reverting the changes in CHANGELOG and agent configs manually.

---

## 🌐 Internationalization

This skill supports both **Chinese** and **English** environments:

| Resource | Chinese | English |
|----------|:---:|:---:|
| `SKILL.md` (this file) | — | ✅ Full English |
| `references/quickstart.md` | — | ✅ English quickstart for new users |
| `references/sync-setup.md` | ✅ Full Chinese | — (code pseudocode is language-agnostic) |
| `references/sync-journal.md` | ✅ Full Chinese | — (JSONL format is language-agnostic) |
| `scripts/init_sync.sh` | `--lang zh` (default) | `--lang en` |
| `scripts/force_sync.sh` | `--lang zh` (default) | `--lang en` |
| Registry agent names | `name_zh` field | `name` field |
| Generated SYNC.md | Chinese template | English template (via `--lang en`) |
| Generated CHANGELOG.md | Chinese template | English template (via `--lang en`) |

**Using English**:

```bash
# Install and initialize in English
bash scripts/init_sync.sh --lang en

# Demo in English
bash scripts/init_sync.sh --lang en --demo
```

New English-speaking users should start with `references/quickstart.md`.

---

## Upgrading

### From v1.0 to v1.1

- `agent-registry.json` introduced (previously agent list was hardcoded)
- `pending_sync` files now use version-named format (`pending_sync_v3.1_a1b2c3.md`) instead of single `pending_sync.md`
- Journal-based two-phase commit added
- No breaking changes — existing sentinel files and CHANGELOG format unchanged

### From v1.1 to v1.2

- **Registry is now single source of truth**: scripts read agent list from `agent-registry.json` instead of command-line args
- **Bilingual scripts**: `--lang en|zh` flag on both `init_sync.sh` and `force_sync.sh`
- **New flags**: `--dry-run` (preview), `--demo` (learning mode), `--help`
- **English quickstart**: `references/quickstart.md` added
- **`agent-registry.json` format changed**: added `vars` section with placeholders

#### Migration steps (v1.1 → v1.2)

1. **Update `agent-registry.json`**:
   ```json
   // Add this at the top of your existing agent-registry.json:
   "vars": {
     "workspace_root": "~/.openclaw",
     "master_agent": "amaster",
     "master_memory": "${vars.workspace_root}/workspace-${vars.master_agent}/memory"
   },
   // Update workspace paths to use placeholders:
   "agents": {
     "acode": {
       "workspace": "${vars.workspace_root}/workspace-acode"  // <-- use placeholder
     }
   }
   ```

2. **Verify** with dry-run: `bash scripts/init_sync.sh --dry-run`

3. **Re-run init**: `bash scripts/init_sync.sh` (safe — skips existing files)

#### Compatibility notes

- Existing `CHANGELOG.md`, sentinel files, and `.sync_journal.jsonl` are **fully compatible**
- Agent-side `pending_sync_*.md` / `SYNC.md` / `BOOTSTRAP.md` format unchanged
- `force_sync.sh` positional args unchanged; new flags are additive

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This skill definition |
| `SECURITY.md` | Security model, permissions, and user consent flow |
| `references/quickstart.md` | 🆕 English quickstart for new users |
| `references/sync-setup.md` | HEARTBEAT item 12 + structured CHANGELOG spec |
| `references/pending-sync-template.md` | pending_sync file template (version-named) |
| `references/sync-journal.md` | Journal-based two-phase commit mechanism |
| `references/agent-registry.json` | Single source of truth for agent IDs and workspaces |
| `scripts/init_sync.sh` | Full setup in one command (now reads registry; supports --auto) |
| `scripts/force_sync.sh` | Trigger immediate sync detection |
| `scripts/revert_sync.sh` | Trigger version rollback |
| `scripts/wizard.sh` | 🆕 Interactive setup wizard for new users |
