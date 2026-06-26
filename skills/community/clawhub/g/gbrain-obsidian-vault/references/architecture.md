# Architecture — Obsidian × gbrain × OpenClaw memory

## Data flow

```
┌─────────────────────────────────────────────────────────────┐
│  Obsidian (GUI)                                              │
│  Graph · Backlinks · Unlinked mentions · Manual edits        │
└───────────────────────────┬─────────────────────────────────┘
                            │ reads/writes files only
┌───────────────────────────▼─────────────────────────────────┐
│  ~/wiki (git repo)                                           │
│  people/ projects/ concepts/ synthesis/ daily/ sessions/ …   │
│  memory/ → symlink → ~/.openclaw/workspace/memory/*.md       │
│  .obsidian/  (gitignored)                                    │
│  .raw/       (gitignored, gbrain export sidecars)            │
└───────┬───────────────────────────────┬─────────────────────┘
        │ git diff                      │ symlink (not in git)
        ▼                               ▼
┌───────────────┐                 ┌──────────────────┐
│ gbrain sync   │                 │ memory_search    │
│ embed extract │                 │ (*.sqlite)       │
│ Postgres      │                 │ OpenClaw agents  │
└───────────────┘                 └──────────────────┘
```

## Why memory symlink does not duplicate into gbrain

gbrain `sync` pipeline (`gbrain/src/core/sync.ts`):

1. Input: `git diff --name-status` since last sync
2. Filter: `isSyncable(path)` — must be `.md`, not in hidden dir, not `ops/`, etc.
3. Symlink `memory` in git is **one symlink entry**, not thousands of `.md` paths
4. Even if committed, `memory` is in `.gitignore` → never appears in diff

## Why `.obsidian/` is safe

`isSyncable` line 82-83: any path segment starting with `.` is skipped.

## Materialize gap (Postgres vs files) — **Plan B: auto-mirror**

`put_page` / `importFromContent` now **writes `~/wiki/<slug>.md` on every DB write** (`gbrain/src/core/wiki-mirror.ts`).
Obsidian sees new MCP pages immediately; `brain-link-maintenance` git-commits them on the next cron.

One-time backfill for legacy DB-only pages:

```bash
gbrain export --dir ~/wiki
```

## memory ↔ gbrain bridge without risky wikilinks

gbrain pages often cite sources as plain text:

```markdown
[Source: memory/2026-04-29.md]
```

Obsidian **Unlinked mentions** surfaces these in the backlink pane when you open `memory/2026-04-29.md`.

Upgrading to `[[memory/2026-04-29]]` creates real graph edges. **Plan B (enabled):** agents MUST use this wikilink form when citing daily memory from gbrain pages.

## Obsidian settings rationale

| Setting | Value | Why |
|---------|-------|-----|
| `useMarkdownLinks` | `false` | Keep `[[wikilink]]` compatible with gbrain |
| `newLinkFormat` | `absolute` | New links like `projects/foo` |
| `alwaysUpdateLinks` | `false` | Prevent mass rewrite of existing links |
