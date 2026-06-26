# claw-janitor

A safe, transparent, zero-dependency, multi-platform system cleaner for OpenClaw.

## Why this exists

`claw-janitor` is built for **paranoid-safe cleanup**:
- conservative defaults
- explicit safety boundaries
- no hidden dependencies
- auditable output

## Safety highlights

- **Blacklist sealing** for sensitive paths (`.ssh`, `.aws`, `.gnupg`, `.kube`, `.openclaw/workspace`, CWD tree, system roots)
- **Regex protection** for risky segments (`.git`, `.env`, `node_modules`, etc.)
- **Symlink protection** (never traverses/deletes through symlinks)
- **Mount-point protection** (never crosses filesystem device boundaries)
- **AI cache awareness**: Hugging Face/Ollama/Torch are scanned and alerted, **never auto-deleted**
- **Graceful degradation**: skips locked/denied targets without hard failure

For detailed boundaries, see [`SECURITY.md`](./SECURITY.md).

## Installation

```bash
clawhub install claw-janitor
```

## Usage

```bash
node /path/to/skills/claw-janitor/janitor.js [options]
```

### Common examples

```bash
# Safe cleanup
node janitor.js

# Preview only
node janitor.js --dry-run

# Deep cleanup (more aggressive docker/system pruning)
node janitor.js --deep

# JSON output for automation
node janitor.js --dry-run --json

# Disable color for CI logs
node janitor.js --dry-run --no-color

# Scope by group
node janitor.js --dry-run --only packages
node janitor.js --dry-run --skip docker

# Write audit report to file
node janitor.js --dry-run --json --report-file ./janitor-report.json
```

### Options

- `--dry-run` Preview only, no deletion
- `--deep` More aggressive cleanup
- `--json` Machine-readable output
- `--no-color` Disable ANSI colors
- `--report-file <path>` Write JSON report to file
- `--only <group>` Run only one group: `ai-scan|packages|docker|system`
- `--skip <group>` Skip one group: `ai-scan|packages|docker|system`
- `-h, --help` Show help

## Testing

```bash
npm test
npm run test:dry
```

## License

MIT
