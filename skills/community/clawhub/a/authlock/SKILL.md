---
name: authlock
description: AuthLock (机密保护) - MFA-bound secret protection. Triggers when user mentions authlock, secret protection (机密保护), TOTP encryption, MFA binding (MFA绑定), password vault (密码保险箱), certificate encryption (证书加密).
---

# AuthLock - MFA-bound Secret Protection (机密保护)

Provides TOTP-based encryption for sensitive data (passwords, certificates, keys), requiring MFA verification for each decryption.

## Installation (安装)

```bash
# Install dependencies (安装依赖)
pip3 install --user cryptography pyotp qrcode
```

**Usage**:
```bash
# Direct call (recommended)
python3 <SKILL_DIR>/authlock_cli.py <command>

# Or add temporary alias (current shell only)
alias authlock='python3 <SKILL_DIR>/authlock_cli.py'
```

> `<SKILL_DIR>` is the skill installation directory, the parent folder of this SKILL.md file.

## Multi-tenant Support (多租户支持)

Achieve tenant isolation via different locations, internal structure remains unchanged.

### Location Levels (位置级别)

| Level | Location | Description |
|-------|----------|-------------|
| System (系统级) | `~/.authlock/` | Shared across all workspaces, default |
| Workspace (工作区级) | `<WORKSPACE>/.authlock/` | Independent for current workspace |
| User (用户级) | Custom path | User-specified location |

### Lookup Priority

```
User (--path/AUTHLOCK_HOME) → Workspace → System
```

- **User level highest**: Via `--path` parameter or `AUTHLOCK_HOME` env var
- **Workspace level medium**: Auto-detect `OPENCLAW_WORKSPACE` env or current directory
- **System level fallback**: Default `~/.authlock/`

### Initialize Level

```bash
# Interactive selection (recommended)
authlock init

# Specify level
authlock init --level system      # System level
authlock init --level workspace   # Workspace level
authlock init --level user --path /custom/path  # User level
```

### View Location

```bash
# Show current location and lookup paths
authlock which

# List all existing locations
authlock locations
```

### Location-specific Operations

```bash
# All commands support --path parameter
authlock seal secret.txt --name my-pass --path /custom/path
authlock open my-pass --code 123456 --path /custom/path
authlock list --path /custom/path
```

## Quick Start (快速开始)

### Initialize (初始化)

```bash
# Interactive level selection
authlock init

# Or specify level
authlock init --level system
authlock init --level workspace
authlock init --level user --path /custom/path

# Or import existing seed
authlock init --seed JBSWY3DPEHPK3PXP
```

Initialization displays QR code, scan with Microsoft Authenticator.

### Seal (Encrypt) / 封印（加密）

```bash
# Encrypt file
authlock seal ~/.ssh/id_rsa --name my-server-key

# Encrypt text (from pipe)
echo "super_secret_password" | authlock seal - --name db-password

# Encrypt with specified name
authlock seal ~/.ssh/server.pem --name prod-ssh-key
```

### Open (Decrypt) / 解密

```bash
# Decrypt to stdout
authlock open my-server-key --code 123456

# Decrypt to file
authlock open my-server-key --code 123456 --output ~/.ssh/id_rsa

# Decrypt and execute (SSH example)
authlock open prod-ssh-key --code 123456 --exec "ssh -i - user@host"
```

### Management

```bash
# List all sealed secrets
authlock list

# Delete secret
authlock delete old-password

# Show current location
authlock which

# List all locations
authlock locations
```

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    Encryption Flow                       │
│                                                         │
│  Sensitive data ──┐                                     │
│                   ├──► AES-256-GCM ──► Ciphertext       │
│  TOTP seed ───────┘                                     │
│       + salt                                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Decryption Flow                      │
│                                                         │
│  User enters TOTP code (123456)                         │
│        │                                                │
│        ▼                                                │
│  Code valid ✓ ──► Derive key ──► AES-256-GCM decrypt    │
│                  ──► Plaintext                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Configuration

### Optional PIN

Add second layer protection:

```bash
# Set PIN
authlock config --set-pin

# Enable mandatory PIN
authlock config --require-pin

# Now each decryption needs TOTP + PIN
authlock open my-key --code 123456 --pin
```

## Security Notes (安全说明)

### ⚠️ TOTP 授权隔离原则

**每次解密都是独立事件，必须单独验证：**

| 禁止 | 说明 |
|------|------|
| ❌ 复用 TOTP code | "刚才已经提供过 code 了" |
| ❌ 缓存 code | 将 code 存储起来后续使用 |
| ❌ 批量授权 | 一次 code 覆盖多次解密 |

| 必须 | 说明 |
|------|------|
| ✅ 每次独立询问 | 每次 `open` 都询问当前有效的 TOTP |
| ✅ 验证时效性 | TOTP 有效期约 30 秒，过期必须重新获取 |
| ✅ 即用即弃 | 解密后明文仅用于当前操作，不保留 |

**Agent 执行流程：**

```
用户请求解密 AUTHLOCK-xxx
       ↓
询问："请提供当前有效的 TOTP code"
       ↓
用户提供 code (如: 123456)
       ↓
执行: authlock open xxx --code 123456
       ↓
使用明文执行操作 (SSH连接等)
       ↓
清除内存中的明文
```

**重要：** 即使对话中有过解密操作，下次请求时必须重新询问 TOTP code。

---

### ⛔ Absolute Prohibitions (绝对禁止事项)

**Never echo plaintext password in conversation! (绝对不能在会话中回显明文密码！)**

- Agent must **never** show decrypted plaintext in chat response
- Even with `--output` to file, don't echo file contents
- Plaintext input during `seal` operation also shouldn't be echoed
- To confirm success, only return "✅ Sealed/Decrypted", not content

**Example (wrong vs correct)**:

```
❌ Wrong: Decryption successful, password: super_secret_password
✅ Correct: ✅ Decrypted to specified file
```

### Session Security

- Decrypted result only for **in-memory operations** (SSH connection, DB connection)
- **Not written to chat history**
- **Not written to session cache files**
- Immediately clear plaintext from memory after operation

### Other Security Notes

1. **TOTP seed safety**: Seed stored in config file, backup carefully
2. **Time sync**: Ensure accurate system time, TOTP depends on time
3. **Memory safety**: Decrypted plaintext exists briefly in memory only
4. **Backup**: Backup corresponding `~/.authlock/` directory

## Trigger Keywords

authlock, secret protection, TOTP encryption, MFA binding, password vault, certificate encryption

## Secret Reference Convention

Use `AUTHLOCK-<NAME>` format in documents to reference encrypted secrets.

### Reference Format

```
AUTHLOCK-<UPPERNAME>
```

| Reference Example | Actual Secret Name | Description |
|-------------------|--------------------|-------------|
| `AUTHLOCK-TEST-HELLO` | `test-hello` | Test secret |
| `AUTHLOCK-DB-PASSWORD` | `db-password` | Database password |
| `AUTHLOCK-PROD-SSH-KEY` | `prod-ssh-key` | SSH private key |

**Naming rules**:
- Reference uses **uppercase letters** and **hyphens**
- Actual secret name: remove `AUTHLOCK-` prefix, convert to **lowercase**
- Example: `AUTHLOCK-DB-PASSWORD` → `db-password`

### Agent Usage Flow

1. **Discover reference**: Find `AUTHLOCK-xxx` format in document
2. **Request verification**: Ask user for current TOTP code
3. **Decrypt secret**: `python3 <SKILL_DIR>/authlock_cli.py open <name> --code <code>`
4. **In-memory use**: Keep decryption result in memory, **no disk write**
5. **Write file**: Only when user explicitly specifies output path

### Using in Documents

```markdown
# Server Configuration

- SSH Key: AUTHLOCK-PROD-SSH-KEY
- Database Password: AUTHLOCK-DB-PASSWORD
- API Token: AUTHLOCK-API-TOKEN
```

**Security principles**:
- Decrypted result should not be written to disk
- Agent should handle secret in memory only
- Only write to file when user explicitly specifies output path