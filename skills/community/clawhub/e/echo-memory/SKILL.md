# Echo Memory

Sync OpenClaw markdown memory files to Supabase with Luhmann encoding. Parse, encode, embed, and upsert agent memories from local workspace to cloud storage.

## Commands

```bash
echo-memory sync          # Parse + encode + embed + upsert to Supabase
echo-memory restore       # Restore markdown files from Supabase
echo-memory status        # Show sync status and diff
```

## Options

- `--dry-run` — Preview changes without writing
- `--incremental` — Only sync changed files (via git diff)
