# Ghost Mode Architecture

## State Machine

```
                  ┌──────────────────────────────────────────┐
                  │                                          │
                  ▼                                          │
            ┌──────────┐    archive    ┌───────────┐         │
            │  active  │─────────────►│ completed │─────────┐│
            └──────────┘              └───────────┘         ││
                 │                          │                ││
                 │ ghost off                │ archive cmd   ││
                 │ (triggers pipeline)      │ (cron/manual) ││
                 ▼                          ▼                ││
            ┌──────────┐    scrub     ┌───────────┐         ││
            │ archived │─────────────►│  scrubbed │─────────┐│
            └──────────┘              └───────────┘         ││
                                           │                  ││
                                           │ verify cmd       ││
                                           ▼                  ││
                                      ┌──────────┐           ││
                                      │ verified  │◄──────────┘│
                                      └──────────┘              │
                                           │                    │
                                           │ shred              │
                                           ▼                    │
                                      ┌──────────┐             │
                                      │  DONE    │◄────────────┘
                                      └──────────┘
```

Each transition is idempotent. Re-running a completed step is safe.

## Registry Format

`~/.openclaw/workspace/memory/.ghost-sessions.json`:

```json
{
  "sessions": {
    "<session-id>": {
      "sessionKey": "agent:main:telegram:direct:12345",
      "sessionId": "uuid",
      "activatedAt": "2026-04-24T01:04:00Z",
      "status": "active|completed|archived|scrubbed|verified",
      "archiveMode": "full",
      "archivedAt": null,
      "scrubbedAt": null,
      "verifiedAt": null
    }
  }
}
```

## File Layout

```
~/.openclaw/
├── workspace/
│   └── memory/
│       ├── .ghost-mode                    # Flag file (present = ghost active)
│       └── .ghost-sessions.json           # Registry
├── ghost-archive/                          # Temporary archive storage
│   └── YYYY-MM-DD/
│       └── <session-id>/
│           ├── <session-id>.jsonl          # Session transcript
│           └── <session-id>.checkpoint.*.jsonl
└── agents/
    └── main/
        └── sessions/                        # Source: session files live here
```

## Pipeline Stages

### 1. Archive (active → completed → archived)

- Finds session JSONL and checkpoint files in the sessions directory (`OPENCLAW_HOME/agents/<agent>/sessions/`)
- Copies them to `~/.openclaw/ghost-archive/YYYY-MM-DD/<session-id>/`
- If `archiveMode='full'`: removes originals after copy
- If `archiveMode='split'`: keeps primary JSONL, archives checkpoints only
- Updates registry status to `archived`

### 2. Scrub (archived → scrubbed)

**Daily logs** (`memory/YYYY-MM-DD.md`, `memory/YYYY-MM-DD-*.md`):
- Removes all entries whose timestamps fall within the ghost window
- Uses `mtime + timestamp-in-content` matching for accuracy

**Semantic memory** (`memory/semantic/*.md`):
- Removes entries attributed to the ghost session or with timestamps in the ghost window
- Atomic write: write to `.tmp`, then rename

**Episodic memory** (`memory/episodic/*.md`):
- Same approach as semantic

**MEMORY.md**:
- Removes promoted entries with ghost-window source citations
- Preserves non-ghost content

### 3. Index Cleanup

- Opens OpenClaw's SQLite memory index (`~/.openclaw/data/memory.db`)
- Deletes chunks whose file paths match ghost-affected files
- Does NOT force a full reindex (rely on natural index refresh)

### 4. Verify (scrubbed → verified)

7-layer verification:

1. Flag file removed
2. Registry shows correct final status
3. Session JSONL not at original path
4. Session checkpoints not at original path
5. Daily logs contain no ghost-window entries
6. Semantic files contain no ghost-window entries
7. Memory index contains no ghost paths

### 5. Shred (verified → done)

- `shred -u` on all archived files in `~/.openclaw/ghost-archive/`
- Removes empty date directories
- If `shred` unavailable: falls back to `rm` with stderr warning

## Ghost Window Calculation

The ghost window is `[activatedAt, deactivatedAt]` where:
- `activatedAt` comes from the registry entry
- `deactivatedAt` defaults to the current time if not explicitly recorded

All timestamps are ISO 8601 UTC. Matching uses both file mtime and content-embedded timestamps for accuracy.

## Edge Cases

- **Multiple ghost sessions on same day**: Scrubber handles overlapping windows correctly
- **Ghost session spanning midnight**: Window crosses day boundaries; all affected files are scrubbed
- **Stale flag (>24h)**: `force-cleanup-all` archives and scrubs all stale sessions automatically
- **Already-archived session**: Idempotent — skip and continue
- **Missing session files**: Verification marks as verified if archival was already completed