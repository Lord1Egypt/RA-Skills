---
name: baserow-cli
version: 0.1.0
description: "Baserow: Create, read, update, and delete rows, list tables and fields. Use when the user wants to interact with Baserow — querying data, creating or updating rows, inspecting table structure, or any database workflow."
metadata:
  openclaw:
    emoji: "🗄️"
    category: "productivity"
    requires:
      bins: ["baserow"]
      env: ["BASEROW_TOKEN", "BASEROW_URL"]
    cliHelp: "baserow --help"
---

# Baserow CLI

CLI for [Baserow](https://baserow.io) — the open-source Airtable alternative. Output is JSON by default — pipe to `jq` or consume directly.

## Setup

```bash
uv tool install baserow-cli   # or: pip install baserow-cli
baserow config init            # interactive setup wizard
```

Config: `~/.config/baserow-cli/config.toml`. All values can be set via env vars (`BASEROW_TOKEN`, `BASEROW_URL`, `BASEROW_TABLE`) or CLI flags.

## Command Discovery

Do not guess command names or options. Use `--help`:

```bash
baserow --help
baserow rows --help
baserow rows list --help
```

## Quick Reference

| Resource | Key commands |
|----------|-------------|
| `baserow tables` | `list`, `get <table-id>` |
| `baserow fields` | `list --table <id>` |
| `baserow rows` | `list`, `get`, `create`, `update`, `delete` |
| `baserow rows batch-*` | `batch-create`, `batch-update`, `batch-delete` |
| `baserow config` | `init`, `show`, `set` |

## Common Workflows

**Discover table structure:**
```bash
baserow tables list
baserow tables get 42
baserow fields list --table 42
```

**List and search rows:**
```bash
baserow rows list --table 42
baserow rows list --table 42 --search "quarterly" --size 50
baserow rows list --table 42 --filter "Status__equal=Done" --order-by "-Created"
```

**Create a row:**
```bash
baserow rows create --table 42 --json '{"Name": "New item", "Status": "Todo"}'
```

**Update a row:**
```bash
baserow rows update 1 --table 42 --json '{"Status": "Done"}'
```

**Batch operations:**
```bash
baserow rows batch-create --table 42 --json '[{"Name": "A"}, {"Name": "B"}]'
baserow rows batch-update --table 42 --json '[{"id": 1, "Status": "Done"}, {"id": 2, "Status": "Done"}]'
baserow rows batch-delete --table 42 --json '[3, 4, 5]' --yes
```

**Pipe JSON from stdin:**
```bash
cat data.json | baserow rows batch-create --table 42 --json -
```

## Important Conventions

- `--table` is optional when `defaults.table` is configured
- `--database` is optional when `defaults.database` is configured
- Destructive commands (`delete`, `batch-delete`) require `--yes` in non-TTY (agent) contexts
- `--json` accepts `-` to read from stdin
- Pagination via `--page` and `--size` (max 200 per page); default is page 1
- Errors go to stderr as JSON: `{"error": {"type": "...", "message": "...", "status_code": N}}`
- Exit codes: `0` success, `1` error, `2` rate-limited (retry safe)
- Field values in `--json` use field names (not IDs)

> [!CAUTION]
> `delete` and `batch-delete` commands are destructive — always confirm with the user before executing.
