# Command Paths - Apple Mail (MacOS)

Use this hierarchy so behavior stays deterministic and debuggable.

## Path 1: AppleScript via osascript (Primary)

Use `osascript` for read, draft, send, move, archive, and delete operations in Mail.app.

Quick probe:
```bash
osascript -e 'tell application "Mail" to return name of every account'
```

Use when:
- You need full control over Mail.app actions.
- You need deterministic write verification inside Mail.app.

## Path 2: Shortcuts CLI (Secondary)

Use `shortcuts` when AppleScript flows are packaged in reusable Shortcuts for orchestration and retries.

Quick probe:
```bash
shortcuts list | head
```

Use when:
- Team has shared Shortcuts for standardized mail operations.
- You need branch logic without large inline scripts.

## Path 3: sqlite3 Envelope Index (Read-Only Speed Path)

Use `sqlite3` only for read-oriented indexed lookup in Apple Mail metadata.
Never write to Mail databases directly.

Quick probe:
```bash
ls ~/Library/Mail/V*/MailData/Envelope\ Index
```

Use when:
- You need fast search or triage over large mailbox history.
- You can accept read-only metadata workflows.

## Optional Cross-Check Path

Use optional protocol tools like `himalaya`, `swaks`, or IMAP scripts only when user already uses them and asks for protocol-level verification.

## Command Path Selection Rule

1. Probe primary path (`osascript`).
2. If unavailable, probe `shortcuts`.
3. For read-heavy tasks, optionally add `sqlite3` lookup.
4. If no safe path works, stop and report one actionable fix.

## Traps

- Running write actions through unsupported path assumptions -> silent failures.
- Mixing multiple write paths in one operation -> hard-to-debug state drift.
- Querying stale metadata without a sync check -> incomplete results.
