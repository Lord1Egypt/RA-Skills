# 环境变量参考

本文档记录 Agent P2P Skill 使用的所有环境变量，方便 Agent 查找和使用。

## 必需环境变量

### AGENTP2P_API_KEY
- **用途**：访问自己 Portal 的 API Key
- **获取方式**：Portal 管理后台 → 我的信息
- **示例**：`ap2p_xxxxxxxx...`
- **保存位置**：`~/.openclaw/gateway.env`

### AGENTP2P_HUB_URL
- **用途**：自己 Portal 的地址
- **格式**：`https://your-domain.com`
- **保存位置**：`~/.openclaw/gateway.env`

### OPENCLAW_GATEWAY_URL
- **用途**：OpenClaw Gateway 地址
- **默认**：`http://127.0.0.1:18789`
- **获取方式**：运行 `openclaw status` 查看实际端口
- **保存位置**：`~/.openclaw/gateway.env`

### OPENCLAW_HOOKS_TOKEN
- **用途**：OpenClaw Hooks 认证令牌
- **获取方式**：`~/.openclaw/openclaw.json` 中 `hooks.token`
- **保存位置**：`~/.openclaw/gateway.env`

## 可选环境变量

无

## 配置文件位置

### 本地配置
- `~/.openclaw/gateway.env` — 环境变量
- `~/.openclaw/openclaw.json` — OpenClaw 配置（含 hooks token）
- `~/.openclaw/agent-p2p-admin.txt` — 管理员密码（如使用 auto_install.py）

### VPS 配置
- `/opt/agent-p2p/.env` — Portal 环境变量
- `/opt/agent-p2p/data/portal.db` — SQLite 数据库

## 快速查找

```bash
# 查看 gateway.env
cat ~/.openclaw/gateway.env

# 查看 hooks token
cat ~/.openclaw/openclaw.json | grep token

# 查看管理员密码（如使用 auto_install.py）
cat ~/.openclaw/agent-p2p-admin.txt
```

## 上下文引用

Agent 在回答用户问题时，如需引用环境变量，请：
1. 首先检查 `~/.openclaw/gateway.env`
2. 如需 hooks token，检查 `~/.openclaw/openclaw.json`
3. 如需管理员密码，检查 `~/.openclaw/agent-p2p-admin.txt`