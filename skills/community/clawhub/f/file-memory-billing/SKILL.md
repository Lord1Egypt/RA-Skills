---
name: file-memory
description: 文件化记忆与任务归档工作流。用户提到“不要依赖上下文/建立md档案/会话接力/清理上下文/长期任务持续交接”时使用：先建任务档案，再把关键信息写入ops与memory文件，按文件而非聊天历史继续工作。
metadata: { "openclaw": { "requires": { "bins": ["node"] }, "primaryEnv": "SKILL_BILLING_API_KEY" } }
---

# File Memory Workflow

目标：不依赖长聊天上下文，靠文件稳定接力。

## Billing（SkillPay）

每次调用先尝试扣费（默认 10 tokens = 0.01 USDT）。

- 脚本：`{baseDir}/scripts/skillpay-charge.mjs`
- 必需环境变量：
  - `SKILL_BILLING_API_KEY`
  - `SKILL_ID`
- 可选环境变量：
  - `SKILL_BILLING_URL`（默认 `https://skillpay.me/api/v1/billing`）
  - `SKILL_BILLING_TOKENS`（默认 `10`）

示例：

```bash
node {baseDir}/scripts/skillpay-charge.mjs --user-id "<user-id>" --amount 10
```

返回：
- `charged: true` → 继续执行 skill
- `charged: false` 且有 `payment_url` → 把充值链接返回给用户

## 必做规则

1. 先建任务档案，再开始执行。
2. 每次阶段完成都更新档案，不留“只在聊天里”的关键信息。
3. 代码类任务完成后，记录 commit 与验证步骤。
4. 需要长期记忆时，写入 `MEMORY.md` 或 `memory/YYYY-MM-DD.md`。

## 标准目录

- 项目任务：`<repo>/ops/tasks/TASK-YYYYMMDD-HHMM.md`
- 项目交接：`<repo>/ops/HANDOFF.md`
- 过程日志：`<repo>/ops/WORKLOG.md`
- 后续计划：`<repo>/ops/NEXT_STEPS.md`
- 决策记录：`<repo>/ops/DECISIONS.md`
- 全局日记：`<workspace>/memory/YYYY-MM-DD.md`
- 长期记忆：`<workspace>/MEMORY.md`（仅主会话加载）

## 新任务流程

1. 创建任务档案 `TASK-*.md`，写：目标、验收标准、风险、执行记录。
2. 执行任务。
3. 完成后更新：
   - `ops/WORKLOG.md`（做了什么）
   - `ops/NEXT_STEPS.md`（下一步）
   - `ops/DECISIONS.md`（为什么这么做）
4. 若有代码改动：提交 commit，并在任务档案写明 commit hash。

## 回复用户格式

- 任务ID：`TASK-...`
- 状态：进行中/已完成
- 产出：文件/commit
- 下一步：一句话

## 注意

- 不把敏感信息写入仓库。
- 当用户要求“清上下文”时，不删历史事实，改为确保关键内容已文件化并从文件继续。