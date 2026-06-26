---
name: "acpx-bridge-troubleshooting-guide"
description: "解决 acpx 桥接超时问题和 OpenClaw 飞书多账户配置。当遇到 acpx 连接 Gateway 超时、initialize 卡住、WebSocket 1005 错误、gateway.token 缺失、acpx 配置错误、飞书多机器人配置、ACP 协议解析失败、bindings 路由不生效等问题时使用。包括创建 token 文件、修复 acpx 配置、更新 acpx 版本、正确配置飞书多账户（使用 accounts 结构而非新建 channel）、使用 openclaw config set 命令而非 jq 直接修改 JSON 等关键步骤。"
metadata: { "openclaw": { "emoji": "🦞" } }
---

# acpx 桥接超时排查与飞书多账户配置指南

本技能帮助解决 acpx 桥接超时问题并正确配置 OpenClaw 飞书多账户，避免常见配置陷阱和协议兼容性问题。

## 何时使用此技能

- 当 acpx 连接 Gateway 时卡在 `initialize` 阶段或超时时
- 当需要配置多个飞书机器人连接到不同 AI 后端（如 Claude Code）时
- 当遇到 WebSocket 1005 错误、ACP 协议解析失败、Gateway 断开连接时
- 当需要修改 OpenClaw 配置但不确定正确命令方式时（避免直接用 jq 修改 JSON）

## 步骤

### 1. 检查并创建 Gateway Token 文件

**操作：**
```bash
# 检查文件是否存在
ls -la ~/.openclaw/gateway.token

# 如果不存在，从 openclaw.json 找到 token 并创建
echo "你的_gateway_token" > ~/.openclaw/gateway.token
```

**原因：** gateway.token 文件缺失是 acpx 超时的常见根本原因，Gateway 需要此文件进行身份验证。

### 2. 修复 acpx 配置文件

**操作：**
```bash
# 编辑 ~/.acpx/config.json
{
  "defaultAgent": "openclaw",
  "agents": {
    "openclaw": {
      "command": "openclaw",
      "args": ["acp", "client"]
    }
  }
}
```

**原因：** acpx 配置中的脚本路径必须指向实际存在的命令，`openclaw acp client` 是官方推荐的 ACP 入口，不需要 `--url` 和 `--token-file` 参数（会自动从 OpenClaw 配置读取）。

### 3. 更新 acpx 到最新版本

**操作：**
```bash
npm install -g acpx@latest
acpx --version  # 确认版本
```

**原因：** acpx 处于 alpha 阶段，更新频繁。新版本可能包含 ACP 协议错误处理的修复（如 0.4.0 修复了 -32601/-32602 错误处理）。

### 4. 配置飞书多账户（正确方式）

**操作：**
```bash
# 使用 openclaw config set 命令，不要用 jq 直接修改 JSON
openclaw config set 'channels.feishu.accounts.claude' '{"appId":"cli_xxx","appSecret":"xxx","domain":"feishu","connectionMode":"websocket"}'

# 验证配置
openclaw config validate

# 重启 Gateway
openclaw gateway restart
```

**原因：** 飞书多账户应使用 `channels.feishu.accounts` 结构，而不是创建新的 channel（如 feishu-claude）。使用官方命令可避免 JSON 格式错误。

### 5. 验证配置和连接

**操作：**
```bash
# 检查配置有效性
openclaw doctor

# 测试 ACP 连接
openclaw acp client

# 检查 Gateway 状态
openclaw gateway status
```

**原因：** 配置修改后必须验证有效性并重启 Gateway 才能生效。

## 陷阱与解决方案

❌ **直接用 jq 修改 openclaw.json** → JSON 格式可能出错（缩进、换行问题），导致配置无效 → ✅ **使用 `openclaw config set` 命令**

❌ **创建新 channel（如 feishu-claude）来添加第二个飞书机器人** → bindings 无法正确路由，配置结构错误 → ✅ **在 `channels.feishu.accounts` 下添加第二个账户**

❌ **acpx 配置中添加 `--url` 和 `--token-file` 参数** → `openclaw acp client` 会自动从配置读取，额外参数可能导致冲突 → ✅ **只配置 command 和 args，不添加 URL 和 token 参数**

❌ **在 bindings 中手动添加 `accountId: "default"`** → 没有 accountId 的 binding 自动匹配 default account，手动添加可能导致匹配失败 → ✅ **让 default account 自动匹配，只给非 default 账户指定 accountId**

❌ **忽略 acpx 版本更新** → 旧版本可能存在 ACP 协议兼容性问题（如 0.3.0 的协议错误处理 bug） → ✅ **定期更新到最新版本，查看 release notes**

❌ **配置修改后不重启 Gateway** → 配置不会生效，问题难以排查 → ✅ **每次配置修改后执行 `openclaw gateway restart`**

## 关键代码和配置

### gateway.token 创建
```bash
echo "5b56cfe28d8675390f3a39691e63999be50947e06dec1007" > ~/.openclaw/gateway.token
```

### acpx 配置文件 (~/.acpx/config.json)
```json
{
  "defaultAgent": "openclaw",
  "timeout": 900,
  "agents": {
    "openclaw": {
      "command": "openclaw",
      "args": ["acp", "client"]
    },
    "claude": {
      "command": "claude"
    }
  }
}
```

### 飞书多账户配置结构（参考）
```json5
{
  channels: {
    feishu: {
      enabled: true,
      accounts: {
        default: {
          appId: "cli_a90d44041b38dcd4",
          appSecret: "[REDACTED]"
        },
        claude: {
          appId: "cli_a944379913b85ccb",
          appSecret: "[REDACTED]"
        }
      }
    }
  },
  bindings: [
    {
      agentId: "main",
      match: { channel: "feishu", accountId: "default" }
    },
    {
      type: "acp",
      agentId: "claude",
      match: { channel: "feishu", accountId: "claude" },
      acp: {
        agent: "claude",
        backend: "acpx",
        mode: "persistent"
      }
    }
  ]
}
```

### 配置命令示例
```bash
# 添加第二个飞书账户
openclaw config set 'channels.feishu.accounts.claude' '{"appId":"cli_a944379913b85ccb","appSecret":"[REDACTED]"}'

# 验证配置
openclaw config validate

# 重启 Gateway
openclaw gateway restart
```

## 环境和前提条件

- **acpx 版本**: 0.4.0+（推荐最新）
- **OpenClaw Gateway**: 正常运行，端口 18789
- **Node.js**: npm 可全局安装 acpx
- **配置文件路径**:
  - `~/.openclaw/gateway.token`
  - `~/.openclaw/openclaw.json`
  - `~/.acpx/config.json`
- **权限**: 需要读写上述配置文件的权限
- **已知限制**: 飞书多账户绑定路由功能尚未完全支持（issue #51467），bindings 无法区分同一用户的不同机器人

## 伴随文件

- `scripts/gateway-token-check.sh` — 检查 gateway.token 是否存在并验证格式
- `references/feishu-multi-account-config.md` — 飞书多账户配置详细文档和示例
- `references/acp-protocol-troubleshooting.md` — ACP 协议常见问题和调试方法

## 任务记录

**任务标题**: 解决 acpx 超时问题

**关键发现**:
- Gateway 的 ACP 后端将日志行和 JSON-RPC 消息混在同一个 WebSocket 流中发送，导致 acpx 解析失败
- bindings 只能匹配 `channel` 和 `peer`，无法区分同一用户的不同机器人（等待官方实现 `account` 字段绑定）
- 使用 `openclaw config set` 命令比直接用 jq 修改 JSON 更安全可靠

**最终状态**:
- gateway.token 创建 ✅
- acpx 配置修复 ✅
- acpx 版本更新 0.3.0 → 0.4.0 ✅
- ACP 连接测试 ⚠️ 部分成功（能连接但执行时 Gateway 断开 1005 错误）
- 飞书多账户配置 ❌ 不支持（bindings 无法区分 accountId）
- Gateway 运行状态 ✅ 正常（PID 105020, 端口 18789）

**建议方案**: 暂时放弃 acpx 桥接，继续使用 echo agent + qwen3.5-plus，飞书新机器人需等待官方实现多账户绑定路由功能。

## Companion files

- `scripts/fix_acpx_bridge.sh` — automation script
- `scripts/add_feishu_account.sh` — automation script
- `scripts/diagnose_acpx.sh` — automation script
- `references/acpx-配置参考.md` — reference documentation
- `references/openclaw-飞书多账户配置.md` — reference documentation
- `references/acp-协议故障排查.md` — reference documentation