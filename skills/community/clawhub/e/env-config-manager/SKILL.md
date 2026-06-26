# env-config-manager - 环境配置管理器

## Metadata

| Field | Value |
|-------|-------|
| **Name** | env-config-manager |
| **Slug** | env-config-manager |
| **Version** | 1.0.0 |
| **Homepage** | https://github.com/openclaw/env-config-manager |
| **Category** | development |
| **Tags** | env, config, dotenv, secrets, yaml, json, encryption, variables |

## Description

### English
A comprehensive environment configuration manager for handling `.env` files, YAML/JSON configs, secret encryption, and multi-environment switching. Supports key rotation, variable validation, and team-safe secret sharing.

### 中文
环境配置管理器，用于管理 `.env` 文件、YAML/JSON 配置、密钥加密和多环境切换。支持密钥轮换、变量验证和团队安全共享。

## Requirements

- Python 3.8+
- python-dotenv >= 1.0.0
- PyYAML >= 6.0
- cryptography >= 41.0.0
- click >= 8.0.0

## Configuration

### Environment Variables
```bash
ENV_MANAGER_KEY=your-master-encryption-key
ENV_MANAGER_ENV=development
```

## Usage

### Load and Switch Environments

```python
from env_config_manager import EnvManager

# Load .env file
env = EnvManager.load(".env")

# Switch to production config
env.switch("production")

# Get variable with fallback
db_url = env.get("DATABASE_URL", default="sqlite:///default.db")
```

### Encrypt Secrets

```python
from env_config_manager import SecretVault

vault = SecretVault(key="your-master-key")
encrypted = vault.encrypt("super-secret-api-key")
# Store encrypted in .env: API_KEY=ENC(vault,encrypted_value)

decrypted = vault.decrypt(encrypted)
```

### Validate Configuration

```python
from env_config_manager import ConfigValidator

schema = {
    "DATABASE_URL": {"required": True, "type": "url"},
    "PORT": {"required": True, "type": "int", "min": 1024, "max": 65535},
    "DEBUG": {"required": False, "type": "bool", "default": False}
}

validator = ConfigValidator(schema)
errors = validator.validate(env)
```

## API Reference

### EnvManager
- `load(path)` - Load environment from file
- `switch(env_name)` - Switch to named environment
- `get(key, default=None)` - Get variable value
- `set(key, value)` - Set variable
- `save(path)` - Save current state to file
- `diff(other_env)` - Compare two environments

### SecretVault
- `encrypt(plaintext)` - Encrypt a secret
- `decrypt(ciphertext)` - Decrypt a secret
- `rotate_key(new_key)` - Re-encrypt with new key

### ConfigValidator
- `validate(env)` - Validate environment against schema
- `add_rule(key, rule)` - Add validation rule

## Examples

See `examples/` directory for complete examples.

## Testing

```bash
cd /root/.openclaw/workspace/skills/env-config-manager
python -m pytest tests/ -v
```

## License

MIT License
