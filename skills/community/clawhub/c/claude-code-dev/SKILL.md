---
name: claude-code-dev
description: OpenClaw + Claude Code 编程工作流。当用户想用 Claude Code 写代码、调试、重构、做 PR review 时激活。支持两种模式：ACP 集成（推荐，通过飞书/Telegram/Discord 直接对话 Claude Code）和 PTY 后台模式（通过 exec 控制 Claude Code CLI）。不用于纯聊天问答（直接用主 agent）或 Kiro 开发（用 kiro-workflow skill）。
---

# OpenClaw + Claude Code 编程指南

让你的 OpenClaw 龙虾变成编程助手——通过消息平台直接驱动 Claude Code 写代码。

## 两种集成模式

| 模式 | 适合场景 | 优点 | 要求 |
|------|---------|------|------|
| **ACP 模式**（推荐） | 日常编程、持久会话 | 在飞书/Discord 里直接聊天编程，支持持久会话 | 安装 acpx 插件 |
| **PTY 后台模式** | 一次性任务、CI/CD | 灵活，不需要额外插件 | Claude Code CLI 已安装 |

---

## 一、ACP 模式（推荐）

### 前提安装

```bash
# 1. 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 2. 配置 API Key（二选一）
# 方式 A：Anthropic 官方 API（按量付费）
export ANTHROPIC_API_KEY="sk-ant-xxxxx"

# 方式 B：AWS Bedrock（如果有免费额度）
# Claude Code 支持 Bedrock，需配置 AWS 凭证
export ANTHROPIC_MODEL="us.anthropic.claude-sonnet-4-20250514"
export CLAUDE_CODE_USE_BEDROCK=1

# 3. 安装 OpenClaw acpx 插件
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true

# 4. 配置 ACP
openclaw config set acp.enabled true
openclaw config set acp.backend acpx
openclaw config set acp.defaultAgent claude
openclaw config set acp.allowedAgents '["claude","codex"]'

# 5. 设置权限（ACP 是非交互的，必须设）
openclaw config set plugins.entries.acpx.config.permissionMode approve-all

# 6. 重启 gateway
openclaw gateway restart
```

### 使用方式

**方式 1：从聊天界面直接 spawn**
```
/acp spawn claude --bind here --cwd /path/to/project
```
之后在这个对话里说的所有话都会发给 Claude Code。

**方式 2：agent 自动调用**
```json
{
  "task": "修复 src/api.js 里的 404 错误",
  "runtime": "acp",
  "agentId": "claude",
  "mode": "run"
}
```

**方式 3：持久会话 + 线程绑定（Discord/Telegram）**
```
/acp spawn claude --thread auto --mode persistent
```
创建一个线程，所有后续消息都在 Claude Code 会话里。

### ACP 常用命令

| 命令 | 用途 |
|------|------|
| `/acp spawn claude --bind here` | 把当前对话绑定到 Claude Code |
| `/acp status` | 查看当前会话状态 |
| `/acp model anthropic/claude-sonnet-4-6` | 切换模型（省钱用 Sonnet！） |
| `/acp cancel` | 取消当前正在跑的任务 |
| `/acp close` | 关闭会话 |
| `/acp steer 专注修 bug，不要重构` | 给正在跑的任务加指令 |

---

## 二、PTY 后台模式

不需要 acpx 插件，直接通过 exec 控制 Claude Code CLI。

### 前提

```bash
# 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 配置 API Key
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

### 一次性任务

```bash
# 用 PTY 模式运行（必须！）
exec pty=true workdir=/path/to/project command="claude 'Fix the failing test in auth.test.js'"
```

### 后台长任务

```bash
# 1. 启动后台任务
exec pty=true workdir=/path/to/project background=true command="claude 'Refactor the payment module to use async/await'"

# 2. 查看进度
process action=log sessionId=<id>

# 3. 发送输入（如果 Claude Code 在等确认）
process action=submit sessionId=<id> data="yes"

# 4. 任务完成通知（加在 prompt 末尾）
exec pty=true workdir=/project background=true command="claude 'Your task here. When done, run: openclaw gateway wake --text \"Done: summary\" --mode now'"
```

### 非交互模式（适合 CI/CD 和脚本）

```bash
# -p 参数 = print mode，单次输出后退出
claude -p "Analyze this code for security issues" --output-format json

# 限制预算（防止跑飞）
claude -p --max-budget-usd 5.00 "Run tests and fix failures"
```

---

## 三、省钱策略 💰

**核心思路：用 Sonnet 干活，Opus 只做关键决策。**

### 模型选择

| 任务类型 | 推荐模型 | 大约费用 |
|---------|---------|---------|
| 写新功能、重构 | Sonnet 4 | $3/MTok in, $15/MTok out |
| Bug 修复、简单改动 | Sonnet 4 | 同上 |
| 架构设计、复杂推理 | Opus 4 | $15/MTok in, $75/MTok out |
| PR Review | Sonnet 4 | 足够了 |
| 测试生成 | Haiku 4 | $0.25/MTok in, $1.25/MTok out |

### 省钱技巧

1. **默认用 Sonnet**：80% 的编程任务 Sonnet 完全够用
   ```
   /acp model anthropic/claude-sonnet-4-6
   ```

2. **用 Bedrock 走 AWS 免费额度**：如果你有 AWS 账号
   ```bash
   export CLAUDE_CODE_USE_BEDROCK=1
   export AWS_REGION=us-east-1
   ```

3. **设预算上限**：防止 Claude Code 陷入死循环
   ```bash
   claude -p --max-budget-usd 2.00 "Your task"
   ```

4. **用 compact 命令**：长会话时主动压缩上下文
   ```
   /compact
   ```

5. **任务拆细**：一个大任务拆成几个小任务，每个独立会话，避免上下文膨胀

### 费用对比参考

| 场景 | Opus | Sonnet | 省多少 |
|------|------|--------|--------|
| 修一个 bug（~10K token） | ~$0.90 | ~$0.18 | 80% |
| 写一个 API endpoint（~50K） | ~$4.50 | ~$0.90 | 80% |
| 大型重构（~200K） | ~$18.00 | ~$3.60 | 80% |
| 一天编程（~500K） | ~$45.00 | ~$9.00 | 80% |

---

## 四、项目配置建议

### Claude Code 的 CLAUDE.md

在项目根目录放一个 `CLAUDE.md`（类似 OpenClaw 的 AGENTS.md），Claude Code 每次启动会自动读取：

```markdown
# CLAUDE.md

## 项目概述
这是一个 XXX 项目，用 React + Node.js + PostgreSQL。

## 代码规范
- 用 TypeScript strict mode
- 函数用 JSDoc 注释
- 测试用 Jest
- commit message 用 conventional commits

## 重要提醒
- 不要修改 migrations/ 目录下已有的迁移文件
- API 路由在 src/routes/ 下
- 环境变量在 .env.example 里有模板
```

### 与 OpenClaw 的协作模式

```
用户 → 飞书/Telegram 消息
  → OpenClaw 主 agent（Sonnet/Opus）
    → 判断是否需要编程
      → 是 → spawn Claude Code ACP session
      → 否 → 直接回答
```

OpenClaw 主 agent 可以：
1. 接收用户需求
2. 分析需求，拆解任务
3. spawn Claude Code 去写代码
4. 检查 Claude Code 的输出
5. 汇报结果给用户

---

## 五、常见问题

### Q: Claude Code 和 OpenClaw 主 agent 有什么区别？
**A:** OpenClaw 主 agent 是你的全能助手（聊天、搜索、文档、日程等）。Claude Code 是专门的编程工具（读代码、写代码、跑命令）。通过 ACP，OpenClaw 可以在需要时调用 Claude Code。

### Q: 我没有 Anthropic API Key，能用吗？
**A:** 可以，有几个选项：
- **AWS Bedrock**：如果你有 AWS 账号，Claude 模型在 Bedrock 上可用
- **Claude Pro/Max 订阅**：Claude Code 支持用订阅额度（有使用上限）
- **OpenClaw ACP + 其他 harness**：也可以用 Codex（OpenAI）或 Gemini CLI（Google）

### Q: ACP 模式和 PTY 模式哪个好？
**A:** ACP 更好——持久会话、模型切换、权限控制、线程绑定都开箱即用。PTY 模式适合快速一次性任务或不想装 acpx 的场景。

### Q: 如何限制花费？
**A:** 三层防护：
1. Claude Code 的 `--max-budget-usd` 参数
2. Anthropic API 后台设置月度预算上限
3. 默认用 Sonnet，Opus 只在关键时刻用
