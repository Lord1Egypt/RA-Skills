# Bundling Scripts in Skills

## One-off Commands

Reference existing tools directly without a scripts/ directory:

| Tool | Example | Notes |
|------|---------|-------|
| `uvx` | `uvx ruff@0.8.0 check .` | Python, isolated env, needs uv |
| `npx` | `npx eslint@9 --fix .` | Ships with Node.js |
| `bunx` | `bunx eslint@9 --fix .` | Bun's npx equivalent |
| `deno run` | `deno run npm:eslint@9 -- --fix .` | Needs permission flags |
| `go run` | `go run golang.org/x/tools/cmd/goimports@v0.28.0 .` | Ships with Go |

**Tips**: pin versions, state prerequisites, move complex commands into scripts/.

## Referencing Scripts

Use relative paths from skill directory root:

```markdown
## Available scripts
- **`scripts/validate.sh`** — Validates config files
- **`scripts/process.py`** — Processes input data

## Workflow
1. ```bash bash scripts/validate.sh "$INPUT_FILE"```
2. ```bash python3 scripts/process.py --input results.json```
```

## Self-contained Scripts

Declare dependencies inline, no separate manifest needed:

**Python (PEP 723)**: `# /// script` block with dependencies. Run: `uv run scripts/extract.py`

**Deno**: `import * as lib from "npm:pkg@1.0.0";`. Run: `deno run scripts/extract.ts`

**Bun**: `import * as lib from "pkg@1.0.0";`. Run: `bun run scripts/extract.ts`

**Ruby**: Use `bundler/inline` to declare gems.

## Agent-Friendly Script Design

- **Avoid interactive prompts**: agents run in non-interactive shells. All input via CLI flags/env/stdin. If it hangs → must have clear error with usage.
- **`--help` provides usage**: primary way agents learn your script's interface. Include brief description, flags, examples.
- **Write helpful errors**: "Error: --format must be one of: json, csv, table. Received: xml."
- **Use structured output**: JSON/CSV > aligned text. Data → stdout, diagnostics → stderr.
- **Idempotency**: agents may retry. "Create if not exists" > "create and error on duplicate".
- **Input constraints**: reject ambiguous input with clear guidance, use enums and closed sets.
- **Dry-run**: `--dry-run` flag for destructive/stateful operations.
- **Meaningful exit codes**: distinct codes for different failure types, documented in `--help`.
- **Safe defaults**: require explicit confirmation flags (`--confirm`) for destructive actions.
- **Predictable output size**: default to summary or limit for large output; support `--offset` for pagination or `--output` for file output.
