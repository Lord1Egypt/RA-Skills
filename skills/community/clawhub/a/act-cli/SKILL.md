---
name: act
description: Run ACT WebAssembly component tools via `act call`. Use when the user asks to use an ACT component, run a .wasm tool, or needs sandboxed tools (SQLite, HTTP, filesystem, etc.) without system dependencies. Also use when you see references to ghcr.io/actpkg/ or .wasm component files.
license: MIT-0
compatibility: Requires act CLI (npm i -g @actcore/act) and shell/terminal access.
allowed-tools: Bash(act:*)
metadata:
  author: actcore
  version: "0.1.0"
  openclaw:
    requires:
      bins:
        - act
---

# ACT Tools

Run self-contained WebAssembly component tools via the `act` CLI. No system dependencies, no Docker, no language runtimes — just `.wasm` binaries in a sandbox.

## Prerequisites

Check if `act` is available:

```bash
act --help
```

If not installed:

```bash
npm i -g @actcore/act
```

## Step 1: Discover tools

```bash
act info --tools --format json <component>
```

`<component>` is one of:
- OCI registry ref: `ghcr.io/actpkg/sqlite:0.1.0`
- HTTP URL: `https://example.com/component.wasm`
- Local file: `./component.wasm`

The output contains:
- `metadata_schema` — required configuration keys (pass via `--metadata`)
- `tools` — list of tool names, descriptions, and `parameters_schema`

Use `--format text` for a human-readable summary instead of JSON.

## Step 2: Call a tool

```bash
act call <component> <tool-name> --args '<json>' [options]
```

| Option | Purpose |
|--------|---------|
| `--args '<json>'` | Tool parameters (matches `parameters_schema`) |
| `--metadata '<json>'` | Component config (matches `metadata_schema`) |
| `--allow-dir guest:host` | Grant directory access to the sandbox |
| `--allow-fs` | Grant full filesystem access |

Output is JSON on stdout. Logs go to stderr.

Remote components are cached locally after first download.

## Example: SQLite

```bash
# Create a table
act call ghcr.io/actpkg/sqlite:0.1.0 execute-batch \
  --args '{"sql":"CREATE TABLE notes (id INTEGER PRIMARY KEY, text TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"}' \
  --metadata '{"database_path":"/data/notes.db"}' \
  --allow-dir /data:/tmp/act-data

# Insert
act call ghcr.io/actpkg/sqlite:0.1.0 execute \
  --args '{"sql":"INSERT INTO notes (text) VALUES (?1)","params":["Hello from ACT"]}' \
  --metadata '{"database_path":"/data/notes.db"}' \
  --allow-dir /data:/tmp/act-data

# Query
act call ghcr.io/actpkg/sqlite:0.1.0 query \
  --args '{"sql":"SELECT * FROM notes"}' \
  --metadata '{"database_path":"/data/notes.db"}' \
  --allow-dir /data:/tmp/act-data
```

## Important

- Always run `act info --tools` first to discover tool names and schemas
- Pass `--metadata` on every call (stateless — no session)
- Use `--allow-dir guest:host` only when the component needs filesystem access
- Components run sandboxed in WebAssembly — no host access unless explicitly granted
