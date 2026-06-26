---
name: cs-qweather-jwtgen
description: 和风天气 JWT Token 生成工具。当需要生成、刷新和风天气 API 的 JWT 认证 Token 时使用此 skill。
---

# cs-qweather-jwtgen

**和风天气 JWT Token 生成工具** — 使用 EdDSA 算法生成认证 Token。

---

## 技能职责

当需要生成或刷新和风天气 API 的 JWT 认证 Token 时使用此 skill。

> Token 有效期 24 小时，过期后需要重新生成。

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `QWEATHER_SUB` | ✅ | 和风账户的用户标识（sub 字段） |
| `QWEATHER_KID` | ✅ | 和风账户的密钥 ID（kid 字段） |
| `QWEATHER_API_HOST` | 否 | 和风 API Host（生成脚本本身不需要，预警/天气脚本需要） |

> **自动加载**：脚本使用 `dotenv` 库自动从 `~/.openclaw/.env` 加载变量（`override=True`，强制读取最新值避免旧进程缓存干扰），在 OpenClaw 环境下可直接使用。

---

## 文件要求

### 私钥文件

必须位于 `~/.myjwtkey/ed25519-private.pem`，权限应为 `600`。

```bash
chmod 600 ~/.myjwtkey/ed25519-private.pem
```

### Token 输出文件

生成后自动保存到 `~/.myjwtkey/last-token.dat`（覆盖写入）。

其他和风天气脚本（如 `cs-qweather-alert`）会从此文件读取 Token。

---

## 使用方法

```bash
python3 cs-qweather-jwtgen/scripts/generateJWTtoken.py
```

### 示例输出

```
[22:50:53] Private key: ~/.myjwtkey/ed25519-private.pem
[22:50:53] Private key loaded (119 chars, masked)
[22:50:53] sub: 4G***ER
[22:50:53] kid: KJ***9T
[22:50:53] iat=1775746223, exp=1775830253, sub=4G***ER, kid=KJ***9T
[22:50:53] Generating JWT ...
[22:50:53] JWT generated [masked: ey***Bg]
[22:50:53] Token saved to: ~/.myjwtkey/last-token.dat

[JWT Token]
eyJhb...
```

---

## 日志

- 位置：`/tmp/cslog/generateJWTtoken-YYYYMMDD.log`
- 脱敏：sub、kid、JWT Token 均只显示前2后2位

---

## 依赖

- Python 3
- `pyjwt`：`pip install pyjwt`
