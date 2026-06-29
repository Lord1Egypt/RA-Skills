# Binding Scripts in Skills

## One-Shot Commands

| Tool | Example | Notes |
|------|---------|-------|
| `uvx` | `uvx ruff@0.8.0 check .` | Python isolated env |
| `npx` | `npx eslint@9 --fix .` | Bundled with Node.js |
| `bunx` | `bunx eslint@9 --fix .` | Bun equivalent of npx |
| `deno run` | `deno run npm:eslint@9 -- --fix .` | Requires permission flags |
| `go run` | `go run golang.org/x/tools/cmd/goimports@v0.28.0 .` | Bundled with Go |

Lock versions, declare prerequisites, move complex commands to `scripts/`.

## Referencing Scripts

Relative paths from skill root directory:

```markdown
## Scripts
- `scripts/validate.sh` — Validates config
- `scripts/process.py` — Processes data

1. `bash scripts/validate.sh "$INPUT"`
2. `python3 scripts/process.py --input results.json`
```

## Self-Contained Scripts

- **Python (PEP 723):** `# /// script` + `# dependencies = [...]` + `# ///` → `uv run`
- **Deno:** `import from "npm:pkg@ver"` → `deno run`
- **Bun:** `import from "pkg@ver"` → `bun run`
- **Ruby:** `bundler/inline`

## Agent-Friendly Design

- Avoid interactive prompts; use CLI flags/env vars/stdin
- `--help` provides usage (primary way Agent learns interface)
- Structured output (JSON/CSV > aligned text); data → stdout, diagnostics → stderr
- Idempotent: "create if not exists" > "create then error on duplicate"
- Destructive ops: add `--dry-run` and `--confirm`
- Meaningful exit codes, documented in `--help`
- Large output: default to summary/limit, support `--offset` pagination
