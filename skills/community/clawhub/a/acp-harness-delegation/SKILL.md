---
name: acp-harness-delegation
description: 通过 ACP runtime 委托 acpx-enabled harness（Claude Code / Codex 等）的标准协议。触发词：调用 Claude Code、通过 acp 调用、通过 acpx 调用、delegation to claude/codex、Coordinator 调用 Executor。
---

# Acpx Harness Delegation

通过 ACP runtime 委托 acpx-enabled harness（Claude Code / Codex 等）的标准协议。

## 触发条件（满足其一）
- "调用 Claude Code"
- "通过 acp 调用"
- "通过 acpx 调用"
- "delegation to claude"
- "delegation to codex"
- "Coordinator 调用 Executor"
- "spawn acpx harness"
- "用 acp 调用外部 agent"
- "通过 ACP 委托 harness"

---

## 核心调用方式

### ✅ 标准 sessions_spawn（结果自动推回父 channel）

```javascript
sessions_spawn({
  runtime: "acp",
  agentId: "claude",       // 或 codex / pi / opencode / gemini / kimi
  mode: "session",          // 关键：持久 session，不是 run
  thread: true,             // 关键：结果通过 parent channel 推送回来
  label: "executor",        // 固定 label，复用 session
  task: "任务描述"
})
```

**效果**：结果直接出现在 Coordinator 的聊天里，不需要跨 session 查。

### ❌ 错误方式（不要用）

```javascript
// 错误1：mode="run" 是 fire-and-forget，无法获取返回结果
sessions_spawn({ runtime: "acp", agentId: "claude", mode: "run", task: "..." })

// 错误2：sessions_send 跨 session 访问会被 visibility 限制
sessions_send({ sessionKey: "agent:claude:acp:...", message: "..." })
// → 报错：forbidden / Session visibility restricted

// 错误3：visibility=all 有安全风险，不推荐
// → CVE-2026-27004 相关风险
```

---

## 调用前必须满足的 3 个前提

### 1️⃣ 认证：ANTHROPIC_API_KEY 必须存在

acpx 调用 Claude adapter 时，runtime 会广告 `authMethods`，如果找不到凭据则报错 `RUNTIME: Authentication required`。

**检查方式：**
```bash
echo $ANTHROPIC_API_KEY
```

**配置方式（二选一）：**

**方式 A：环境变量（推荐用于测试）**
```bash
export ANTHROPIC_API_KEY=sk-...
# 然后调用
```

**方式 B：acpx 配置文件（推荐用于生产）**
在 `~/.acpx/config.json` 添加：
```json
{
  "authCredentials": {
    "ANTHROPIC_API_KEY": "sk-你的key"
  }
}
```

> 注意：`authPolicy: "skip"` 只能跳过认证检查，不能替代凭据。如果 Claude adapter 要求 API key 而找不到，会直接失败。

### 2️⃣ acpx 全局权限配置

`~/.acpx/config.json` 必须包含：
```json
{
  "defaultPermissions": "approve-all",
  "nonInteractivePermissions": "deny",
  "authPolicy": "skip"
}
```

这个配置让 acpx 在自动化环境下自动批准所有操作，不弹确认框。

### 3️⃣ Session 可用性验证（可选但推荐）

如果之前调用过同一个 label，可能需要先验证 session 是否健康：

```bash
acpx sessions list
```

如果看到某个 session 显示 `needs reconnect`，先修复：
```bash
acpx sessions ensure <session-name>
# 或重建
acpx sessions new claude
```

---

## 完整调用流程（推荐写入你的 Coordinator Agent prompt）

```
当需要调用 Claude Code 执行任务时：

1. 前置检查：确认 ANTHROPIC_API_KEY 环境变量存在
   （如果不存在，回复："请先配置 ANTHROPIC_API_KEY 环境变量"）

2. 调用 spawn：
   sessions_spawn(
     runtime="acp",
     agentId="claude",
     mode="session",
     thread=true,
     label="executor",
     task="具体任务描述"
   )

3. 等待结果：结果会通过 thread 自动推送回当前 channel
   不要使用 sessions_send 去跨 session 查结果

4. 如果结果未返回，检查：
   - acpx sessions list → 是否有 needs reconnect
   - echo $ANTHROPIC_API_KEY → API key 是否有效
```

---

## 已知问题记录

### 🔍 `unknown option '--cwd'` 排查

**已验证：** OpenClaw acpx runtime.ts（2026.3.13）构造命令时 `--cwd` 是放在 agent 之前的，顺序正确：
```
acpx --format json --json-strict --cwd /path claude prompt --session ...
```

**如果仍看到这个错误：** 说明调用方不是 OpenClaw runtime，而是外部脚本直接调用 `acpx claude --cwd /path`。检查那个脚本，把 `--cwd` 移到 `claude` 之前：
```
✅ acpx --cwd /path claude "prompt"
❌ acpx claude --cwd /path "prompt"
```

---

## 错误处理对照表

| 错误信息 | 根因 | 解决方法 |
|---------|------|---------|
| `unknown option '--cwd'` | OpenClaw acpx runtime bug，参数构造顺序错误 | 等待 OpenClaw 修复；当前可在 agent config 里 workaround |
| `agent needs reconnect` | acpx session 记录在但进程断了 | `acpx sessions ensure <name>` 或 `sessions new` |
| `RUNTIME: Resource not found` | session id 失效 | 不要复用旧 id，用新的 spawn |
| `RUNTIME: Authentication required` | 找不到 API key | 配 `ANTHROPIC_API_KEY` 环境变量或 `authCredentials` |
| `forbidden / Session visibility restricted` | `sessions_send` 跨 session 被限制 | 改用 `thread=true` 模式，结果自动推回 |

---

## Session 复用说明

使用固定 `label` 的好处：
- 第一次调用：创建 session
- 后续调用：自动 reconnect 到已有 session，保留上下文
- Session 有 30 天归档清理 + 500 条上限

不需要手动管理 session 生命周期，只要 label 固定，acpx 会自动处理。

---

## 关键澄清

- **`--dangerously-skip-permissions` 是 Claude Code CLI 的参数，不是 acpx 的参数**
- **acpx 的正确权限控制是 `defaultPermissions` 配置项**（见上方配置）
- **`mode:"session" + thread:true` 是唯一可靠的结果返回方式**
- **不要用 `visibility=all`**，有安全风险

---

## 相关文件

- Skill 配置：`~/.openclaw/skills/acp-harness-delegation/SKILL.md`
- Harness 列表：`~/.openclaw/skills/acp-harness-delegation/references/harness-list.md`
- acpx 全局配置：`~/.acpx/config.json`
- Claude API Key 配置：`~/.acpx/config.json` 的 `authCredentials` 字段
