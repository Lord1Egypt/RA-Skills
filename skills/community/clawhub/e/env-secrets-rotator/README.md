# Environment Secrets Rotator

A CLI tool to rotate secrets in .env files and generate Vault commands for secret rotation workflows.

## Quick Start

```bash
# Rotate all secrets in .env file
./scripts/main.py rotate --file .env --keys "*"

# Generate Vault commands
./scripts/main.py vault --keys API_KEY,DB_PASSWORD --path secret/data/myapp

# Dry run (preview changes)
./scripts/main.py rotate --file .env --keys "*" --dry-run
```

## Features

- **Secure secret generation** - Cryptographically random values using Python's secrets module
- **Multiple algorithms** - Hex, base64, UUID, alphanumeric
- **Backup protection** - Automatic backups before modification
- **Vault command generation** - HashiCorp Vault CLI commands for easy integration
- **Batch processing** - Rotate multiple keys across multiple files
- **Validation** - Check .env file format and key existence

## Installation

This skill is installed via OpenClaw. Once installed, you can use it directly from your OpenClaw agent.

## Usage

### Rotation
```bash
./scripts/main.py rotate --file .env --keys API_KEY,DB_PASSWORD
```

### Vault Commands
```bash
./scripts/main.py vault --keys API_KEY,DB_PASSWORD --path secret/data/myapp
```

### Validation
```bash
./scripts/main.py validate --file .env --strict
```

## Output Formats

- **JSON** - Structured output with new values and metadata
- **Vault commands** - Ready-to-run HashiCorp Vault CLI commands
- **Human-readable** - Clear summaries of changes made

## Security

- Uses cryptographically secure random generation
- Creates backups before modification
- Dry-run mode for previewing changes
- No external dependencies for secret generation

## License

MIT