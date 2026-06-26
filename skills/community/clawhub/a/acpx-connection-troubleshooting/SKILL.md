---
name: "acpx-bridge-troubleshooting"
description: "用于排查 acpx 桥接连接失败、超时或初始化卡住的问题。当用户提到 acpx 无法连接、ACP 桥接超时、gateway.token 缺失、Claude Code 认证失败、initialize 阶段卡住、或尝试将微信/飞书渠道切换到 ACP 后端时触发。涵盖配置验证、令牌文件修复、模型端点检查及网络连通性测试。即使未明确说'acpx'，但描述'CLI 连不上网关'或'子代理调用失败'也应使用。"
metadata: {{ "openclaw": {{ "emoji": "tool" }} }}
---

# acpx 桥接连接问题排查与修复

本技能帮助诊断和修复 acpx 与 OpenClaw Gateway 或 Claude Code CLI 之间的连接问题，确保 ACP 桥接正常工作。

## 何时使用此技能

- 当 `acpx` 命令执行超时或卡在 `initialize` 阶段时
- 当用户尝试将渠道（微信/飞书）路由切换到 ACP 后端但失败时
- 当遇到 `gateway.token` 缺失或认证错误时
- 当 Claude Code CLI 配置与预期模型（如百炼 vs Anthropic）不匹配时
- 当需要验证 ACP 网关连通性或入口脚本路径时

## 步骤

### 1. 确认渠道支持性
检查目标渠道（如 wecom、feishu）是否在 ACP 支持列表中。
- **操作**：查阅 ACP 文档或当前绑定配置。
- **原因**：企业微信 (wecom) 可能不在默认支持列表（目前主要支持 Discord/Telegram），强行绑定会导致路由失败。

### 2. 验证 Claude Code CLI 配置
检查 `~/.claude/config.json` 中的 API 端点和模型配置。
- **操作**：查看配置是否指向正确的 API（Anthropic 或 阿里云百炼）。
- **原因**：acpx 调用的是本地 CLI 配置，若 API Key 失效或端点错误，会卡在认证阶段。

```json
// ~/.claude/config.json 示例
{
  "apiEndpoint": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
  "apiKey": "sk-sp-[REDACTED]",
  "model": "qwen3.5-plus"
}
```

### 3. 检查 Gateway Token 文件
确认 `~/.openclaw/gateway.token` 是否存在且内容正确。
- **操作**：若文件缺失，从 `openclaw.json` 中提取 token 并创建文件。
- **原因**：acpx 连接 OpenClaw Gateway 需要此令牌进行 WebSocket 认证，缺失会导致连接立即超时。

```bash
# 修复命令（替换为实际 token）
echo "5b56cfe28d8675390f3a39691e63999be50947e06dec1007" > ~/.openclaw/gateway.token
```

### 4. 分析 acpx 日志
运行命令时添加 verbose 模式或观察输出日志。
- **操作**：关注 `[client] initialize` 状态。
- **原因**：若卡在 `initialize` 说明网络或认证失败；若卡在 `session/new` 说明服务响应问题。

### 5. 测试替代方案
若 `acpx claude` 失败，尝试 `acpx openclaw` 或其他内置 agent。
- **操作**：`acpx openclaw exec 'status'`。
- **原因**：内置 agent 不依赖外部 CLI 配置，可隔离问题是出在桥接层还是模型层。

##  pitfalls and solutions

❌ **假设 wecom 渠道直接支持 ACP**
→ 为什么失败：ACP 可能未适配企业微信协议，导致路由无法建立。
✅ **正确做法**：先确认渠道兼容性，或使用 `echo agent` 内部调用 acpx 作为替代方案。

❌ **忽略 gateway.token 文件存在性**
→ 为什么失败：acpx 默认从该文件读取认证令牌，不存在则无法握手 Gateway。
✅ **正确做法**：手动创建 `~/.openclaw/gateway.token` 并写入 `openclaw.json` 中的 token 值。

❌ **混淆 Bailian 配置与 Anthropic 配置**
→ 为什么失败：Claude Code CLI 默认期望 Anthropic 端点，若配置为阿里云百炼需确保端点格式兼容。
✅ **正确做法**：验证 `~/.claude/config.json` 中的 `apiEndpoint` 是否可访问，或改用 `acpx openclaw` 绕过 CLI 配置。

❌ **遇到超时就放弃排查**
→ 为什么失败：超时可能是网络路由问题，也可能是入口脚本路径错误。
✅ **正确做法**：检查 Gateway 日志是否有连接记录，确认 ACP 服务端口（默认 18789）是否开放。

## 关键代码与配置

**ACP 绑定配置示例 (openclaw.json)**
```json
{
  "type": "acp",
  "agentId": "claude",
  "match": {
    "channel": "feishu-claude"
  },
  "acp": {
    "agent": "claude",
    "backend": "acpx",
    "mode": "persistent"
  }
}
```

**飞书多机器人配置示例**
```json
{
  "channels": {
    "feishu-claude": {
      "enabled": true,
      "appId": "新机器人的 App ID",
      "appSecret": "新机器人的 App Secret",
      "domain": "feishu",
      "connectionMode": "websocket",
      "webhookPath": "/feishu-claude/events"
    }
  }
}
```

**Gateway 认证修复**
```bash
# 确保目录存在
mkdir -p ~/.openclaw
# 写入 token
echo "YOUR_GATEWAY_TOKEN" > ~/.openclaw/gateway.token
chmod 600 ~/.openclaw/gateway.token
```

## 环境与前置条件

- **acpx 版本**: v0.3.0 或更高
- **OpenClaw Gateway**: 运行中，端口默认 18789
- **Claude Code CLI**: 已安装且可执行
- **配置文件**:
  - `~/.openclaw/openclaw.json` (Gateway 配置)
  - `~/.claude/config.json` (Claude Code 配置)
  - `~/.openclaw/gateway.token` (认证令牌)
- **网络**: 需能访问 API 端点及 Gateway WebSocket 地址

##  companion files

- `scripts/check_gateway.sh` — 检查 Gateway 端口及 token 文件状态的脚本
- `references/acp_channels.md` — ACP 支持的渠道列表及绑定示例

## 任务记录

**任务标题**: 微信渠道切换 acpx 配置及桥接问题排查
**关键发现**:
1. `acpx claude` 卡在初始化，原因是 Claude Code CLI 配置的百炼 API 连通性问题。
2. `acpx openclaw` 超时，根本原因是 `~/.openclaw/gateway.token` 文件缺失。
3. 企业微信 (wecom) 渠道可能不在 ACP 默认支持列表中。
**最终建议**: 若桥接调试成本过高，建议保持现有 `echo agent` 配置，或通过 subagent 内部调用 Claude Code。

## Companion files

- `references/acp-bridge-config-reference.md` — reference documentation