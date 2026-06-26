# Harness List — acpx 支持的 Harness 及配置

## 支持的 Harness（agentId）

| agentId | 默认命令 | 说明 |
|---------|---------|------|
| `claude` | `npx -y @zed-industries/claude-agent-acp@^0.21.0` | Claude Code ACP 适配器 |
| `codex` | `npx @zed-industries/codex-acp@^0.9.5` | OpenAI Codex ACP 适配器 |
| `pi` | `npx pi-acp@^0.0.22` | Pi agent |
| `opencode` | `npx -y opencode-ai acp` | OpenCode |
| `gemini` | `gemini --experimental-acp` | Google Gemini CLI |
| `kimi` | `kimi acp` | Kimi CLI |

来源：acpx 本机源码 `dist/cli.js` AGENT_REGISTRY

---

## 认证配置（必须）

### Claude（必须配置 ANTHROPIC_API_KEY）

Claude ACP adapter 需要 `ANTHROPIC_API_KEY` 环境变量。

**方式 A：环境变量**
```bash
export ANTHROPIC_API_KEY=sk-...
```

**方式 B：~/.acpx/config.json（推荐生产环境）**
```json
{
  "authCredentials": {
    "ANTHROPIC_API_KEY": "sk-..."
  }
}
```

### Codex

Codex 使用自己的认证机制（`OPENAI_API_KEY` 环境变量）。

### Gemini / Kimi / Pi / OpenCode

各自使用对应的 API key 环境变量。

---

## 自动化权限配置

`~/.acpx/config.json` 必须包含：
```json
{
  "defaultPermissions": "approve-all",
  "nonInteractivePermissions": "deny",
  "authPolicy": "skip",
  "agents": {}
}
```

**字段说明：**

| 字段 | 值 | 说明 |
|------|----|------|
| `defaultPermissions` | `"approve-all"` | 批准所有操作（含写入）【推荐自动化场景】 |
| `defaultPermissions` | `"approve-reads"` | 只批准读取操作 |
| `nonInteractivePermissions` | `"deny"` | 非交互时直接拒绝权限请求 |
| `authPolicy` | `"skip"` | 跳过认证流程（配合 authCredentials 使用） |

---

## Session 重建命令

当 session 显示 `needs reconnect` 时：

```bash
# 列出所有 session
acpx sessions list

# 修复指定 session
acpx sessions ensure <session-name>

# 新建 session
acpx sessions new claude
```

---

## 当前 Stone 环境状态

- acpx 版本：0.1.16
- 全局配置路径：`~/.acpx/config.json`
- 已配置：`defaultPermissions: "approve-all"`, `nonInteractivePermissions: "deny"`, `authPolicy: "skip"`
- 待配置：`authCredentials.ANTHROPIC_API_KEY`（如果调用 claude agent）
