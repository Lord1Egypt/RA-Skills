# Security

## Threat Model

Decision Topology is a **local-only** conversation structure mapper. It runs inside an OpenClaw agent on the user's own machine. There is no server component, no cloud storage, and no network communication of any kind.

The primary threat surface is the host filesystem: the script reads and writes JSON tree files in a single configured directory. The user controls this directory and can inspect, move, or delete any file at any time.

## What This Skill Does NOT Do

- **No network access** — no HTTP/HTTPS requests, no WebSocket connections, no DNS lookups. The script works fully offline.
- **No external dependencies** — only Node.js built-in `fs` and `path` modules are used. No `node_modules/`, no `package.json`, no install step.
- **No `eval` or dynamic code execution** — no `eval()`, no `new Function()`, no `vm.runInContext()`.
- **No child process spawning** — no `child_process`, no `exec`, no `spawn`, no `execFile`.
- **No telemetry or analytics** — nothing is collected, reported, or phoned home.
- **No conversation content stored** — all persisted text fields are truncated at the code level (see "Content Guards" below). Nodes contain short structural summaries, never verbatim conversation quotes.
- **No data exfiltration path** — even if the filesystem were compromised, tree files contain only topic labels and structural metadata, not conversation content.

## Modules Used

| Module | Purpose |
|--------|---------|
| `fs` | Read/write JSON tree files and markdown companion files in the configured trees directory |
| `path` | Resolve file paths relative to the script location and trees directory |

That's it. No other modules are imported.

## Input Handling

All user-derived input (topics, summaries, queries, concept keywords) is passed via **stdin as JSON**. This prevents shell injection attacks that could occur if user content were embedded in shell command strings.

The script also accepts a JSON argument as `argv[3]` for programmatic use. Commands that take no arguments (`list`, `analyze`, `rebuild-index`) skip stdin entirely.

Input is parsed with `JSON.parse()` — malformed JSON produces an error message and `process.exit(1)`, nothing else.

## Filesystem Scope

The script reads and writes files in exactly one directory: the trees directory, determined by:

1. The `TOPOLOGY_TREES_DIR` environment variable (if set), or
2. `{script_directory}/../trees/` (default)

**Path containment is enforced at runtime.** At startup, the trees directory is canonicalized via `fs.realpathSync()`. Every user-supplied `file` argument is stripped to its basename with `path.basename()` and then resolved inside the canonical trees directory. This means:

- Absolute paths like `/etc/passwd` are rejected (basename extraction produces `passwd`, which won't exist in trees dir).
- Relative traversal like `../../etc/shadow` is rejected (basename extraction produces `shadow`).
- Symlinks are resolved by `realpathSync` — a symlink inside the trees directory that points outside it would need to already exist on disk, which the script never creates.

The `resolveSafePath()` function additionally verifies the resolved path starts with the canonical trees directory prefix before any read or write occurs. If the check fails, the script exits with an error.

No files outside this directory are read, written, or deleted.

## Content Guards

All text fields written to tree JSON and companion `.md` files are programmatically truncated before saving. This is enforced in code, not just in documentation policy.

| Field | Max length | Applied in |
|-------|-----------|------------|
| `topic` | 120 chars | `init()` |
| `summary` | 200 chars | `addNode()`, `merge()`, `fork()`, `initTree()` |
| `reasoning` | 300 chars | `addNode()`, `merge()`, `fork()` |
| `killed_by` | 200 chars | `killBranch()` |
| `concepts[]` | 50 chars each | `addNode()`, `merge()` |

Text exceeding these limits is silently truncated with a `...` suffix. The `truncate()` function handles this before any data reaches `saveTree()` or `writeMdCompanion()`.

These limits are generous enough for legitimate structural summaries (~30 words) but prevent verbatim conversation dumps. Even if the calling agent passes full conversation text, only the first portion would be stored — and that portion is too short to constitute useful conversation content.

## ID Generation

Node IDs are 6-character hex strings generated with `Math.random()`. These IDs only need to be unique within a single tree (typically 5-30 nodes). The `uniqueId()` function retries on collision. Cryptographic randomness is unnecessary for this use case.

## Vulnerability Reporting

If you find a security issue, please open an issue on the ClewHub skill page or contact the maintainer directly. There is no bug bounty — this is a local-only tool with no network surface — but reports are appreciated and will be addressed.
