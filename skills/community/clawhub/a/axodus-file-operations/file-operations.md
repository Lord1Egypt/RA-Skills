# SKILL: file-operations

## Purpose
Perform safe, auditable file operations (read/write/update/delete/move/copy) in an MCP-enabled environment with path validation and backups.

## When to Use
- Any task requires editing files on disk.
- You need to ensure changes are safe and reversible.
- You must avoid accidental overwrites or destructive operations.

## Inputs
- `operation` (required, enum: `read|write|update|delete|move|copy`).
- `paths` (required, object):
  - `source` (optional, string)
  - `target` (optional, string)
  - `targets` (optional, string[])
- `content` (optional, string): for write/update.
- `backup` (optional, boolean, default: `true` for overwrite/delete).
- `constraints` (optional, string[]): e.g., “only within workspace”.

## Steps
1. Resolve absolute paths and normalize.
2. Validate scope:
   - operation stays inside the intended workspace root(s)
   - block path traversal/suspicious targets
3. Preflight:
   - confirm existence for read/update/delete
   - confirm non-existence (or allow overwrite explicitly) for write/move
4. If overwrite/delete and `backup=true`, create a backup copy (timestamped).
5. Execute the operation with explicit reporting (what changed).
6. Post-validate:
   - file exists where expected
   - content/diff matches expectation

## Validation
- Operation is reversible when possible (backup exists for destructive actions).
- The final target path is verified before execution.
- The operation result is explicitly reported (not silent).

## Output
```yaml
operation: "<operation>"
affected: ["<path>"]
backup_paths: ["<path>"]
result: "success|blocked|failed"
notes: ["..."]
```

## Safety Rules
- Never delete or overwrite recursively without explicit user confirmation.
- Never operate on computed paths without printing the resolved final paths first.
- Prefer patch-based updates over full-file rewrites when possible.

## Example
Update a config file:
- `operation`: `update`
- `paths`: `{ target: "apps/api/.env.example" }`
- Validation: backup created; diff is minimal; file still parses.

