---
name: agent-harness-architect
version: 1.0.0
description: "Diagnose and harden any long-running agent architecture. Describe your agent setup and get a complete harness optimization plan + auto-generated bridge artifacts (progress.json, session protocol, output gate). Based on Anthropic's 'Effective Harnesses for Long-Running Agents' research."
metadata:
  openclaw:
    emoji: "🏗️"
    homepage: "https://clawgamers.com/skills/agent-harness-architect"
---

# Agent Harness Architect 🏗️

> 基于 Anthropic《Effective Harnesses for Long-Running Agents》论文提炼。
> 把你的 agent 架构描述给它，输出完整 harness 诊断报告 + 可直接部署的 bridge artifact 文件。

---

## 核心主张

**模型是商品，harness 才是壁垒。**

再强的模型，没有好的 harness，长时间运行都会退化——过早宣告完成、环境退化、session 交接信息丢失。这个 skill 把 Anthropic 工程团队踩坑总结的最佳实践，变成你的 agent 可直接执行的升级方案。

---

## 触发条件

用户描述中出现以下任意一种：
- "我的 agent 跑着跑着就失败了 / 忘了之前做了什么"
- "每次新 session 都要重新开始"
- "帮我优化 agent 架构"
- "如何让 agent 跨 session 保持状态"
- 用户粘贴了自己的 CLAUDE.md / AGENTS.md / agent 配置

---

## 执行流程

### Step 1 — 架构摸底（必须先问，不能跳过）

向用户提以下问题（可一次性发出，不要逐条等待）：

```
要帮你把 agent 架构调到最优，我需要了解几个关键点：

1. **角色分工**：你有几个 agent？每个负责什么？（比如：一个规划、一个执行、一个监控）
2. **运行周期**：任务通常跑多久？是分钟级 session，还是需要跨多天？
3. **当前最大痛点**：session 中断丢进度？agent 以为做完了实际没做好？不知道上次跑到哪？
4. **现有状态管理**：有没有 progress 文件、日志、git commit？还是全靠模型上下文记忆？
5. **平台**：OpenClaw / Claude Code / 其他？操作系统？
```

### Step 2 — Harness 健康度诊断

根据用户回答，对照以下 8 个维度逐一打分（✅ 已有 / 🟡 部分 / ❌ 缺失）：

| 维度 | 诊断问题 |
|------|---------|
| **Session Bridge** | 每次新 session 启动时，有没有结构化文件（非纯文本）告知"上次做到哪了"？ |
| **固定启动序列** | agent 每次启动是否有强制执行的固定步骤顺序（不可跳过）？ |
| **Smoke Test** | 执行任务前，有没有先验证环境/依赖是否可用？ |
| **原子 Checkpoint** | 每完成一个最小单元，是否立即 commit/保存状态？ |
| **输出自验证** | agent 报告"完成"之前，有没有机制验证结果真的 OK？ |
| **状态文件格式** | 状态追踪用 JSON 还是 Markdown checkbox？（JSON 更防 agent 误改） |
| **Multi-Agent 编排** | 多个 agent 之间有没有明确的消息传递协议，还是靠文件系统凑合？ |
| **降级方案** | 某个依赖挂掉时，有没有明确的 fallback 行为？ |

输出诊断表，标出每个维度的分数和简要原因。

### Step 3 — 优先级排序

根据诊断结果，按 **影响 × 实现难度** 矩阵输出 P0/P1/P2 改进项：

**P0（立刻改，成本低收益高）**：通常是 Session Bridge + 固定启动序列
**P1（本周改）**：Smoke Test + 原子 Checkpoint
**P2（下阶段）**：输出自验证 + Multi-Agent 编排协议

### Step 4 — 生成 Bridge Artifacts

**必须生成以下文件内容**，用户可直接复制部署：

#### 4a. `agent-progress.json`（Session 状态桥）

```json
{
  "_说明": "Agent Session 状态桥。每次 session 启动时读取，结束时更新。JSON 格式防止 agent 误改结构。",
  "schemaVersion": "1.0",
  "lastSession": {
    "timestamp": null,
    "trigger": null,
    "summary": "首次初始化",
    "smokeTest": null,
    "result": "pending"
  },
  "taskTracking": {
    "_说明": "每完成一个任务后在此更新。status: pending|in_progress|done|failed",
    "recentCompleted": []
  },
  "environmentStatus": {
    "lastChecked": null,
    "result": null,
    "notes": null
  },
  "knownIssues": []
}
```

#### 4b. Session 恢复协议（插入你的 CLAUDE.md / AGENTS.md）

```markdown
### Session 恢复协议（每次会话强制执行，顺序不可跳过）

**Step 1 — 读状态桥**：读 `agent-progress.json`，了解上次 session 执行到哪、哪些成功、哪些失败。

**Step 2 — 读任务队列**：读当前待办任务列表，确认优先级。

**Step 3 — Smoke Test**：验证核心环境可用（服务在线？API 可达？依赖存在？）。
不通过 → 先修复环境，不执行任何业务任务。

**Step 4 — 逐任务执行**：每次只执行一个任务，完成后立即：
  - 更新 agent-progress.json 中该任务状态为 done
  - git commit 一次（message 用任务编号）
  - 再执行下一个任务

**Step 5 — Session 结束**：更新 agent-progress.json 的 lastSession 字段，记录本次执行摘要。
```

#### 4c. Output Self-Verification Gate（输出自检，插入消息处理流程末尾）

```markdown
【output-gate】——准备发出任何内容前，内部思考检查（不输出）：
  ├── 是否包含应对外保密的系统内部术语？→ 有则重写
  ├── 是否把思考过程当成了结论发出？→ 有则删除过程只保留结论
  └── 当前上下文是否应该静默（规则明确不该回复的场景）？→ 是则 NO_REPLY
结论: 发出 / NO_REPLY / 已修改后发出
```

### Step 5 — 针对用户平台的定制建议

根据用户平台输出具体命令/配置，例如：

**OpenClaw 用户**：
```powershell
# 检查 gateway 状态（Smoke Test）
openclaw status

# 每个任务完成后立即 commit
git add -A && git commit -m "done: [任务编号] [任务描述]"
```

**Claude Code 用户**：
```bash
# 在 CLAUDE.md 中添加 session 恢复协议
# 使用 JSON 格式跟踪任务状态，而非 Markdown checkbox
```

**通用建议**：
- 状态文件用 JSON，不用 Markdown（agent 更不容易意外破坏结构）
- 每个 session 的前 N 步必须是固定的，写进系统提示，不可跳过
- "完成"报告前必须有端到端验证，不能只看代码改了

---

## 自动优化循环（Self-Improvement Protocol）

此 skill 内置进化机制：

### 触发条件
以下情况发生时，自动写入 `capability-radar` 或等效的学习日志：
- 用户描述的问题在本 skill 覆盖范围外 → 记录为功能缺口
- 用户反馈生成的方案不够具体 → 记录为精度缺口
- 同类架构问题出现 3 次以上 → 触发模式提炼，更新此 skill

### 版本演进规则
| 触发条件 | 动作 |
|---------|------|
| 新平台适配需求 ≥ 2 次 | 新增 Step 5 平台适配分支 |
| 某维度诊断误判 ≥ 2 次 | 优化该维度的诊断问题描述 |
| 生成的 artifact 被用户大幅修改 | 分析修改模式，更新模板 |

---

## 使用示例

**输入**：
> 我有一个 Claude Code agent，每天晚上 10 点自动跑，扫描 memory 文件、生成日记、检查 gateway 状态。但经常跑到一半挂掉，下次启动不知道上次做到哪了，重复做已经做过的事。

**输出**：
1. 诊断报告（Session Bridge ❌、固定启动序列 ❌、Smoke Test 🟡、Checkpoint ❌）
2. P0 改进：立即创建 `agent-progress.json` + 写固定 5 步启动协议
3. 生成完整的 `agent-progress.json` 初始文件
4. 生成可粘贴的 Session 恢复协议段落
5. 针对 Claude Code / Windows 的具体 PowerShell 命令

---

## 设计来源

核心模式来自：
- Anthropic 工程博客《Effective Harnesses for Long-Running Agents》（2025）
- OpenClaw 三引擎架构实战（2026）：Engine A 战略层 + Engine C 全执行层 + session bridge 落地经验

**核心洞察**：创造清晰的"上下文桥梁文件"（bridge artifacts），让每个新 session 能在最少 token 消耗内理解当前状态。这是模型无关的架构原则——无论用什么模型，harness 设计决定了 agent 能跑多远。
