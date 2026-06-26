# devcontainer-validator

Validate `devcontainer.json` files for VS Code Dev Containers, GitHub Codespaces, and DevPod.

## What it does

Checks your `devcontainer.json` (JSONC — comments and trailing commas supported) for common mistakes across six areas:

- **Structure** — required fields, conflicts between image/dockerFile/dockerComposeFile, unknown keys
- **Features** — OCI reference format, duplicates, empty options
- **Ports & networking** — forwardPorts format, port ranges, portsAttributes consistency
- **Lifecycle scripts** — command types, empty commands, shell injection patterns
- **Customizations** — VS Code extensions format, settings type, extension ID validation
- **Best practices** — remoteUser, privileged mode, workspaceFolder, dangerous capabilities

### Rules (24+)

| Category | Rules | Examples |
|----------|-------|---------|
| Structure (6) | Invalid JSONC syntax, missing image source, unknown top-level keys, empty name, image+dockerFile conflict, dockerFile+compose conflict | `"image": "...", "dockerFile": "..."` both set |
| Features (4) | Invalid features format, feature ID not valid OCI ref, empty feature options, duplicate features | `"features": ["go"]` (should be object) |
| Ports & networking (4) | forwardPorts not array, invalid port numbers, port out of range, portsAttributes referencing unlisted ports | `"forwardPorts": [99999]` |
| Lifecycle scripts (4) | Invalid command type, empty commands, shell injection patterns, onCreateCommand usage hints | `"postCreateCommand": ""` |
| Customizations (3) | extensions not array of strings, invalid extension ID format, settings not object | `"extensions": [123]` |
| Best practices (3+) | Missing remoteUser (root warning), privileged: true, missing workspaceFolder, dangerous capAdd entries | `"capAdd": ["SYS_ADMIN"]` |

### Output formats

- **text** — human-readable with severity tags ([E] [W] [I])
- **json** — structured with summary counts
- **summary** — one-line PASS/WARN/FAIL

### Exit codes

- `0` — no errors (warnings/info allowed)
- `1` — errors found (or `--strict` with any issue)
- `2` — file not found or parse error

## Commands

### validate

Full validation of all rules.

```bash
python3 scripts/devcontainer_validator.py validate devcontainer.json
python3 scripts/devcontainer_validator.py validate --format json .devcontainer/devcontainer.json
python3 scripts/devcontainer_validator.py validate --strict devcontainer.json
```

### structure

Validate only structure rules (required fields, conflicts, unknown keys).

```bash
python3 scripts/devcontainer_validator.py structure devcontainer.json
```

### features

Validate only the features section.

```bash
python3 scripts/devcontainer_validator.py features devcontainer.json
```

### security

Validate only security-related rules (privileged, capAdd, shell injection, remoteUser).

```bash
python3 scripts/devcontainer_validator.py security --strict devcontainer.json
```

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--format` | text, json, summary | text | Output format |
| `--min-severity` | error, warning, info | info | Filter by minimum severity |
| `--strict` | flag | off | Exit 1 on any issue |

## Requirements

- Python 3.8+ (pure stdlib, no dependencies)

## Examples

```bash
# Quick check
python3 scripts/devcontainer_validator.py validate devcontainer.json

# CI pipeline
python3 scripts/devcontainer_validator.py validate --strict --format summary devcontainer.json

# Security audit only
python3 scripts/devcontainer_validator.py security --format json devcontainer.json

# Filter noise
python3 scripts/devcontainer_validator.py validate --min-severity warning devcontainer.json
```
