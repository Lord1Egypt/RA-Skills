# ACP 桥接配置隔离与渠道兼容性参考

本文档补充 acpx 桥接的系统架构细节、配置隔离说明及渠道兼容性实测数据，用于辅助排查连接问题前的架构确认。

## 1. 配置隔离说明
OpenClaw 系统中，主 Agent 与 acpx 桥接进程使用独立的配置文件，排查问题时需严格区分：

| 组件 | 配置文件路径 | 用途 | 常见误区 |
|------|--------------|------|----------|
| **OpenClaw 主 Agent** | `~/.openclaw/openclaw.json` | 控制主对话流、内置模型调用、路由绑定 | 误以为修改此处会影响 `acpx claude` 的模型行为 |
| **Claude Code CLI** | `~/.claude/config.json` | 控制 `acpx claude` 的模型后端、API Key 及端点 | 误以为主 Agent 能通则 CLI 也能通（Key 权限可能不同） |
| **Gateway 认证** | `~/.openclaw/gateway.token` | ACP 桥接握手令牌 (WebSocket 认证) | 文件缺失导致 `acpx openclaw` 直接超时，而非认证错误 |

**排查原则**：
- 若主 Agent 正常但 `acpx claude` 失败 → 重点检查 `~/.claude/config.json`。
- 若 `acpx openclaw` 失败 → 重点检查 `~/.openclaw/gateway.token`。

## 2. 渠道兼容性实测
基于 ACP v0.3.0+ 版本的兼容性测试状态：

| 渠道 | 支持状态 | 备注 |
|------|----------|------|
| **Feishu (飞书)** | ✅ 支持 | 支持多机器人配置，可通过不同 Webhook 隔离 Agent |
| **Discord** | ✅ 支持 | 原生支持，稳定性高 |
| **Telegram** | ✅ 支持 | 原生支持 |
| **Wecom (企业微信)** | ⚠️ 不确定 | 协议可能未完全适配，建议优先使用 Echo Agent 内部调用 |

**飞书多机器人策略**：
- **Bot A (主)**: 绑定默认 Agent (如 Qwen)，用于日常对话。
- **Bot B (副)**: 绑定 ACP/Claude Code，用于特定复杂任务。
- **配置要点**: 确保 `webhookPath` 不冲突 (例如 `/feishu` vs `/feishu-claude`)，且在 `bindings` 中通过 `channel` 字段精确匹配。

## 3. 阿里云百炼 (Bailian) 适配细节
当使用 Claude Code CLI 对接阿里云百炼时，需满足特定格式要求以兼容 CLI 的 Anthropic 协议封装：

- **API Endpoint**: 必须使用兼容 Anthropic 格式的代理端点。
  - ✅ 推荐：`https://coding.dashscope.aliyuncs.com/apps/anthropic`
  - ❌ 避免：直接使用百炼原生 SDK 端点（CLI 可能无法识别协议）
- **Model Name**: 需填写 CLI 认可的模型标识 (如 `qwen3.5-plus`)。
- **API Key**: 需确保 Key 有访问该特定端点的权限（有时与主配置 Key 权限范围不同）。

## 4. 常见故障特征对照

| 故障现象 | 可能原因 | 优先检查点 |
|----------|----------|------------|
| **卡在 initialize** | CLI 配置网络不通或 Key 无效 | `~/.claude/config.json` 连通性 |
| **acpx openclaw 超时** | Gateway 令牌缺失 | `~/.openclaw/gateway.token` 存在性 |
| **路由失败/无响应** | 渠道名称不匹配或协议不支持 | `openclaw.json` 中 `channel` 字段及渠道支持列表 |
| **InvalidApiKey** | Key 过期或权限不足 | 百炼控制台 Key 状态及端点白名单 |
