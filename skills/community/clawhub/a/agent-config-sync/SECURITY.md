# Security Model & Permissions

## Permission Scope

`agent-config-sync` requires the following permissions:

### Required
| Permission | Reason | Scope |
|-----------|--------|-------|
| **File read** (master memory) | Read version files & CHANGELOG for sync dispatch | Master agent's `memory/` directory only |
| **File write** (agent workspaces) | Write `pending_sync_*.md` when agents are offline | Agent workspace root only |
| **File read** (agent workspaces) | Check for pending sync files on startup | Agent own workspace only |
| **File append** (agent configs) | Add sync check to BOOTSTRAP.md / HEARTBEAT.md | Agent own workspace only |

### Not Required
- ❌ Network access (no external API calls)
- ❌ Execute arbitrary commands
- ❌ Access outside `~/.openclaw/workspace-*`
- ❌ Read secrets or credentials
- ❌ Modify other installed skills

## Permission Boundaries

### Path Validation
All scripts validate that target paths start with `$workspace_root/workspace-$agent_id/`.
Paths outside this pattern are rejected with an error.

```
✅ ~/.openclaw/workspace-acode/BOOTSTRAP.md    → allowed
❌ /etc/passwd                                   → rejected
❌ ~/.openclaw/openclaw.json                     → rejected (not in a workspace)
```

### File Permission Requirements

**Critical: Sentinel files must be writable**

The version sentinel files (`.current_system_version`, `.last_sync_version`, `.sync_journal.jsonl`) **must be writable** (`rw-rw-r--` / 664).

If set to read-only (e.g., `r--r--r--` / 444), **all version writes silently fail**:
- No version changes are persisted — `.current_system_version` stays at the old value
- HEARTBEAT item 12 detects no difference and skips dispatch
- The sync system appears broken even though infrastructure is healthy
- No error is logged by the atomic write wrapper

**Fix**: `chmod 664 memory/.current_system_version memory/.last_sync_version memory/.sync_journal.jsonl`

**Verification** (run after init/force_sync):
```bash
ls -la memory/.current_system_version memory/.last_sync_version memory/.sync_journal.jsonl
# Should show -rw-rw-r-- not -r--r--r--
```

### User Consent Flow
```
Step 1: --dry-run (always available)
  → Preview every file that will be created/modified
  → No changes are made

Step 2: --confirm (required for write operations)
  → After --dry-run, user must re-run with --confirm
  → Short summary printed before execution

Step 3: Execution
  → Changes logged to stdout + sync journal
  → Backup created for modified existing files
```

## Cross-Agent Isolation
Each agent can only read/write its OWN workspace files.
AMaster (the coordination agent) can write pending_sync files to all agent workspaces,
but only as part of the two-phase commit journal flow.

## Update & Rollback
- All changes are journaled to `.sync_journal.jsonl`
- Backups created before modifying existing files
- Version sentinel files allow deterministic recovery

## Version Conflict Scenarios

### Master Agent Permissions During Conflict

During version conflicts (concurrent changes, offline agents, rollbacks), the Master agent:

| Action | Permission | Boundary |
|--------|:----------:|----------|
| Read `.sync_journal.jsonl` for loop detection | ✅ Allowed | Master `memory/` only |
| Read `pending_sync_*.md` from agent workspaces | ✅ Allowed | Only `~/.openclaw/workspace-*/` |
| Write `pending_sync_*.md` to agent workspaces | ✅ Allowed | Only `~/.openclaw/workspace-*/` |
| Write `revert_sync_*.md` to agent workspaces | ✅ Allowed | Only `~/.openclaw/workspace-*/` |
| Write `isolated_sync_*.md` for self-upgrade | ✅ Allowed | Master `memory/` only; dispatch via isolated flow |
| Create snapshot backups in agent workspaces | ✅ Allowed | Only `~/.openclaw/workspace-*/memory/.sync_snapshots/` |
| Read `.agent_sync_version` from agent workspaces | ✅ Allowed | Only `~/.openclaw/workspace-*/memory/` |
| Delete expired `pending_sync_*.md` files | ✅ Allowed | Only expired (> TTL) files in agent workspaces |

### Agent Permissions During Conflict

| Action | Permission | Boundary |
|--------|:----------:|----------|
| Read own `pending_sync_*.md` files | ✅ Allowed | Own workspace only |
| Read own `.agent_sync_version` | ✅ Allowed | Own `memory/` only |
| Create snapshots before applying sync | ✅ Allowed | Own `memory/.sync_snapshots/` only |
| Delete processed `pending_sync_*.md` files | ✅ Allowed | Own workspace only |
| Restore from snapshots during rollback | ✅ Allowed | Own `memory/.sync_snapshots/` only |
| Query Master for latest version | ✅ Allowed | Via `sessions_send` (existing channel) |

### Snapshot Directory Whitelist

The only allowed snapshot paths:

```
✅ ~/.openclaw/workspace-<agent>/memory/.sync_snapshots/<version>_pre/
✅ ~/.openclaw/workspace-<agent>/memory/.sync_snapshots/<version>_pre/snapshot_manifest.json
✅ ~/.openclaw/workspace-<agent>/memory/.sync_snapshots/<version>_pre/*.bak
❌ ~/.openclaw/workspace-<agent>/memory/.sync_snapshots/../../../etc/passwd
❌ /tmp/snapshots/
```

### Conflict-Related Security Guarantees

1. **No network access** — All conflict resolution is file-system-local (within `~/.openclaw/`)
2. **No credential access** — Conflict detection reads only sentinel files and journal metadata
3. **Atomic writes** — All sentinel file updates use `_atomic_write()` (tempfile + sync + mv)
4. **TTL gating** — Expired `pending_sync` files are deleted, never applied
5. **Loop detection** — Journal scanning prevents infinite sync loops (hard limit: 3 consecutive same-version records)
6. **Isolated self-upgrade** — agent-config-sync's own files are quarantined, never dispatched via normal flow
7. **Snapshot immutability** — Snapshots are read-only after creation; rollback reads from snapshot, never modifies it

## Rollback Security

### Snapshot Creation (Pre-Sync)

Before applying any sync change, the agent creates a snapshot:

1. **Directory**: `memory/.sync_snapshots/<VERSION>_pre/`
2. **Scope**: Only files listed in the CHANGELOG impact range (not a full workspace backup)
3. **Integrity**: Each file's SHA256 checksum recorded in `snapshot_manifest.json`
4. **Permissions**: Snapshots inherit the agent's own file permissions (no privilege escalation)

### Rollback Execution

1. **Trigger**: Master sets `.current_system_version` to a version < `.last_sync_version`
2. **Dispatch**: Generates `revert_sync_<from>_<to>_<sha>.md` — type=revert in journal
3. **Agent-side**: Restores files from snapshot directory, verifies SHA256 checksums
4. **Atomic restore**: All files restored or none (abort on first mismatch)
5. **Cleanup**: Revert file deleted after successful restore; journal marked reverted

### Rollback Attack Surface Mitigation

| Threat | Mitigation |
|--------|------------|
| Malicious revert targeting wrong version | SHA256 verification against snapshot manifest |
| Partial restore leaving mixed state | Atomic restore (all-or-nothing) |
| Infinite revert loops | Journal `type=revert` prevents re-dispatch; manual confirmation required |
| Snapshot tampering | SHA256 pre-computed at snapshot creation; verified at restore time |
| Unauthorized snapshot access | Snapshots inherit agent workspace permissions; no new paths created |


