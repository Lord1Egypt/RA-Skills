# env-config-manager

## Overview

A comprehensive environment configuration manager for modern development workflows.

## Features

- **.env File Management**: Load, edit, save `.env` and `.env.*` files
- **Multi-Environment**: Switch between dev/staging/production configs instantly
- **Secret Encryption**: AES-256-GCM encryption for sensitive values
- **Schema Validation**: Validate required variables and their types
- **Diff & Merge**: Compare environments, merge changes safely
- **Team Sharing**: Export/import encrypted configs for team distribution

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Load current env
python scripts/env_manager.py load

# Switch to production
python scripts/env_manager.py switch production

# Encrypt a secret
python scripts/env_manager.py encrypt API_KEY "sk-12345"

# Validate config
python scripts/env_manager.py validate schema.json
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `load [file]` | Load environment file |
| `switch <env>` | Switch environment |
| `get <key>` | Get variable value |
| `set <key> <value>` | Set variable |
| `encrypt <key> <value>` | Encrypt and store secret |
| `decrypt <key>` | Decrypt secret |
| `validate <schema>` | Validate against schema |
| `diff <file1> <file2>` | Compare two env files |
| `export [file]` | Export to encrypted bundle |

## Examples

See `examples/basic_usage.py` for programmatic usage.

## Testing

```bash
python -m pytest tests/ -v
```

## 中文说明

环境配置管理器，支持 `.env` 文件管理、多环境切换、密钥加密和配置验证。

### 快速开始

```bash
python scripts/env_manager.py load .env
python scripts/env_manager.py switch production
python scripts/env_manager.py encrypt DB_PASSWORD "mysecret"
```

## License

MIT License
