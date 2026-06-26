# JSON Output Schema

Every `oce` command supports `--json`, which produces a single-line JSON object. Use this when parsing output programmatically.

## Universal fields

Every JSON response has at minimum:

| Field | Type | Description |
|---|---|---|
| `status` | string | `"success"`, `"error"`, `"warning"`, `"dry_run"`, `"no_match"`, `"ambiguous"` |
| `message` | string | Human-readable summary (always present on errors and warnings) |

Errors and warnings go to **stderr**. Successes go to **stdout**. Always check exit code first — non-zero means error.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success (or no-op like dry-run) |
| 1 | General error (file not found, validation failed, rolled back, etc.) |
| 2 | No match (oce replace with --old that doesn't appear in file) |
| 3 | Ambiguous match (oce replace with multiple matches and no --all) |
| 64 | Unknown command (dispatcher level) |

---

## Per-command schemas

### `oce read --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "language": "javascript",
  "total_lines": 247,
  "range": { "start": 45, "end": 80 },
  "lines": [
    { "line": 45, "content": "function handleAuth(req) {" },
    { "line": 46, "content": "  const token = req.headers.authorization;" }
  ]
}
```

### `oce find --json`

Without `--files-only`:
```json
{
  "status": "success",
  "count": 3,
  "matches": [
    { "file": "src/auth.js", "line": 12, "text": "  const token = req.headers.authorization;" },
    { "file": "src/auth.js", "line": 28, "text": "  authorization: 'Bearer ' + token," }
  ]
}
```

With `--files-only`:
```json
{ "status": "success", "mode": "files-only", "count": 2, "files": ["src/auth.js", "src/api.js"] }
```

### `oce grep-context --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "context": 5,
  "hits": [
    { "line": 10, "match": false, "text": "// some context line" },
    { "line": 12, "match": true,  "text": "the matching line" },
    { "line": 14, "match": false, "text": "// trailing context" }
  ]
}
```

### `oce tree --json`

```json
{
  "status": "success",
  "root": ".",
  "depth": 3,
  "tree": {
    "name": ".",
    "type": "dir",
    "children": [
      { "name": "src", "type": "dir", "children": [...] },
      { "name": "package.json", "type": "file", "children": [] }
    ]
  }
}
```

### `oce ast symbols`

```json
{
  "status": "success",
  "file": "src/auth.js",
  "symbols": [
    { "type": "function", "name": "validateToken", "line": 12, "end": 28 },
    { "type": "class",    "name": "AuthError",     "line": 35, "end": 52 },
    { "type": "method",   "name": "verify",        "line": 38, "end": 45 }
  ]
}
```

### `oce ast rename --json`

Success:
```json
{
  "status": "success",
  "file": "src/auth.js",
  "from": "validateToken",
  "to": "verifyToken",
  "replacements": 7,
  "backup": "/path/.oce/backups/__src__auth.js.20260427-180951.abc123def456.bak"
}
```

### `oce replace --json`

Success:
```json
{
  "status": "success",
  "file": "src/server.js",
  "replacements": 1,
  "backup": "/path/.oce/backups/__src__server.js.20260427-180951.abc123.bak",
  "message": "replaced 1 occurrence(s)"
}
```

Ambiguous (exit 3) — emitted to stderr:
```json
{ "status": "error", "message": "Found 5 matches; pass --all or make --old more unique" }
```

No match (exit 2) — emitted to stderr:
```json
{ "status": "error", "message": "No match found for --old in src/server.js" }
```

Dry-run:
```json
{ "status": "dry_run", "file": "src/server.js", "matches": 3, "message": "would replace 3 occurrence(s)" }
```

### `oce insert --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "target_line": 47,
  "inserted_lines": 4,
  "backup": "/path/.oce/backups/..."
}
```

### `oce delete --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "deleted_lines": 3,
  "backup": "/path/.oce/backups/..."
}
```

### `oce write --json`

```json
{
  "status": "success",
  "file": "src/new-module.js",
  "lines": 42,
  "backup": "",
  "message": "wrote src/new-module.js (42 lines)"
}
```

`backup` is empty string when the file didn't exist before the write.

### `oce validate --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "language": "javascript",
  "validator": "node --check",
  "valid": true,
  "output": ""
}
```

On failure (exit 1):
```json
{
  "status": "error",
  "file": "src/server.js",
  "language": "javascript",
  "validator": "node --check",
  "valid": false,
  "output": "src/server.js:45\n  return data\n             ^\nSyntaxError: Unexpected token..."
}
```

### `oce format --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "language": "javascript",
  "formatter": "prettier",
  "result": "reformatted"
}
```

Possible `result` values: `formatted` (already canonical, --check), `needs_format` (--check found differences), `reformatted` (write mode, file was changed), `failed` (formatter exited non-zero, rolled back), `not_run` (no formatter installed).

### `oce diff --json`

```json
{
  "status": "success",
  "file": "src/server.js",
  "backup": "/path/.oce/backups/...",
  "diff": "--- backup\n+++ current\n@@ -10,3 +10,3 @@\n..."
}
```

### `oce backup list --json`

```json
{
  "status": "success",
  "count": 4,
  "backups": [
    "/path/.oce/backups/__src__server.js.20260427-181234.abc.bak",
    "/path/.oce/backups/__src__server.js.20260427-180951.def.bak"
  ]
}
```

Newest first. Position 0 is the most recent.

### `oce doctor --json`

```json
{
  "status": "ok",
  "errors": 0,
  "warnings": 3,
  "home": "/home/user/.local/share/oce",
  "state_dir": "/cwd/.oce",
  "checks": {
    "node": "ok",
    "patch": "ok",
    "diff": "ok",
    "grep": "ok",
    "acorn": "ok",
    "prettier": "absent",
    "eslint": "absent",
    "tsc": "ok",
    "gofmt": "absent",
    "rustfmt": "absent",
    "php": "absent",
    "ruby": "absent",
    "python3": "ok",
    "rubocop": "absent",
    "black": "absent"
  }
}
```

Values: `"ok"` (found), `"missing"` (required, not found — causes `status: error`), `"absent"` (optional, not found — only causes warnings).

---

## Parsing in shell

Use Node since it's already a dependency:

```bash
RESULT=$(oce replace src/x.js --old foo --new bar --json 2>&1)
STATUS=$(echo "$RESULT" | node -e 'let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{try{process.stdout.write(JSON.parse(d).status)}catch{process.stdout.write("parse_error")}}')')
case "$STATUS" in
  success)   echo "edit applied" ;;
  dry_run)   echo "would have edited" ;;
  *)         echo "edit failed: $RESULT" ;;
esac
```

Or with `jq` if available:

```bash
oce find "TODO" --type ts --json | jq '.matches | length'
oce ast symbols src/auth.js | jq '.symbols[] | select(.type == "function") | .name'
```
