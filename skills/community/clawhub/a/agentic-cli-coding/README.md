# agentic_cli_coding

CLI code-editing toolkit for agentic coders. Provides the `oce` command — a unified, validation-aware, transaction-capable editing interface that backs up every change and rolls back on syntax failure.

## Quick start

```bash
# One-time per session — set up shorthand:
alias oce="bash /path/to/agentic_cli_coding/scripts/oce.sh"

# Verify:
oce doctor

# Use:
oce tree --depth 2
oce find "TODO" --type js
oce read src/server.js --around foo
oce replace src/server.js --old X --new Y
oce diff src/server.js
```

For the full skill description and methodology, see `SKILL.md`. For deeper docs:

- `references/json-schema.md` — output schema for every command
- `references/workflows.md` — worked examples
- `references/language-support.md` — what's validated/formatted per language
- `references/troubleshooting.md` — symptom-to-fix table

## Layout

```
agentic_cli_coding/
├── SKILL.md                    Skill instructions and methodology
├── scripts/
│   ├── oce.sh                  Main dispatcher — entry point
│   ├── oce-*.sh                Subcommand implementations
│   ├── lib/
│   │   ├── paths.sh            Path bootstrap (sourced by every script)
│   │   ├── common.sh           Shared shell helpers
│   │   └── ast-helper.js       JS/TS AST utilities (acorn)
│   └── install.sh              Optional: install an `oce` wrapper on PATH
├── references/                 Deeper docs loaded on demand
├── node_modules/               Bundled (acorn, acorn-walk, js-yaml)
└── package.json                Dependency manifest
```

## Optional install

```bash
bash scripts/install.sh                     # → ~/.local/bin/oce wrapper
bash scripts/install.sh /opt/local/bin      # custom location
```

The skill works without installing — invoke directly via `bash scripts/oce.sh <command>` or via an alias. The install script just creates a one-line wrapper for convenience.
