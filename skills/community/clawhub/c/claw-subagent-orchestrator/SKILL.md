---
name: subagent-orchestrator
description: "Defines the collaboration protocol between main session and sub-agent sessions for executing heavy tasks (analysis, search, writing). Use when spawning sub-agents to reduce main-session context growth, managing task.md checklist workflows, coordinating multi-step delegated work with crash recovery, or optimizing skill workflows through retrospect analysis."
---

# Sub-agent Orchestrator

子 session 执行重任务（预估 >10K tokens），干完即消失（`cleanup=delete`），主 session 保持轻量。

---

## 适用场景

- 任务重（预估 >10K tokens 才能完成）
- 需要嵌套工具调用（多次 web_fetch / exec / API）
- 结果可结构化输出
- 不需要主 session 全程参与推理

## 不适用场景

- **轻任务**（查天气、简单定义、一问一答）— 不走子 session，spawn 开销 > 直接干
- **交互式 skill**（魔镜等每轮简短问答）— 每句话的 token 开销远低于 spawn 成本

---

## Spawn 协议（主 session 执行）

主 session 调用 `sessions_spawn` 时，必须传以下参数：

```python
sessions_spawn(
    task="[ROUTINE]\n协议: skills/subagent-orchestrator/SKILL.md\n技能: <skill-name>\n任务: <一句话描述>\n通知用户: true/false\n任务ID: <task-id>",
    mode="run",                    # 必须
    cleanup="delete",              # 必须 — 干完消失
    cwd="/path/workspace/<task-id>",  # 必须 — 独立工作区
    context="isolated"             # 推荐 — 不继承主 session 上下文
)
```

### task 字段格式

```
[ROUTINE]
协议: skills/subagent-orchestrator/SKILL.md
技能: <skill 名，决定工具链和输出格式>
任务: <一句话任务描述 — 原始需求原样传递>
通知用户: true/false  ← 主 session 决定（主 session 知道当前渠道）
任务ID: <task-id>     ← 主 session 生成
动作：<start / 接续>   ← 首次 start，崩溃恢复时 接续
```

### task-id 生成规则

```
task-YYYYMMDD-HHMMSS-<序号>
例：task-20260524-210600-001
```

主 session 用当前时间 + 递增序号保证唯一。`cwd` 指向 `workspace/<task-id>/`。

### 通知用户判定（主 session 负责）

| 条件 | 通知用户 | 说明 |
|------|---------|------|
| 结果独立完整，无需主 session 二次加工 | true | 子 session 拿到 message 权限，直发微信/Telegram |
| 结果是中间环节，需要主 session 合并/对比 | false | 子 session 不拿 message，结果回传给主 session |
| 当前渠道为本地终端（开 new session 写推文等） | false | 无外部投递目标 |

---

## 子 session 执行协议

### 启动顺序

```
收到 [ROUTINE]
  → 读 skills/subagent-orchestrator/SKILL.md（本文件）
  → 读 skills/<skill-name>/SKILL.md（任务技能）
  → 分析任务 → 拆解 checklist
  → 在工作区创建 task.md
```

### task.md 格式

文件位置：`workspace/<task-id>/task.md`

```
# Task: <任务名称>
## Status: <start / working / end>

[start done]
[working done] 步骤1
[working] 步骤2
[end]
```

- 只在状态切换时写入（见文件末尾的「写入规则」）
- 崩溃恢复时：从第一个 `[working]` 且无对应 `[working done]` 的位置继续

### 步骤记录文件

每个 `[working]` 对应一个同名 `.md` 文件：

```
workspace/<task-id>/
├── task.md               ← checklist 仅状态
├── 步骤1.md              ← 思考过程 + 工具调用
├── 步骤2.md              ← 同上
└── 步骤3.md              ← 同上
```

文件名和 `[working]` 行描述一致，无需 mapping。

### 写入规则

- **task.md**：仅状态切换时写（步骤开始 / 完成）
- **步骤文件**：直接 `write` 创建新文件（不 `read+edit`），节省 token
- 中间推理不写 task.md，写步骤文件

### 输出

```
通知用户: true + 可投递渠道：
  最后一步 → message 直发微信/Telegram + assistant reply 摘要
  主 session 收到 announce → 确认，不重复发

通知用户: true + 本地终端：
  不拿 message 权限，结果由主 session announce 呈现

通知用户: false：
  子 session 最后一步 → assistant reply 完整结果
  主 session 收到 announce → 转发或合并
```

---

## 崩溃恢复

### 检测

主 session 收到子 session announce：
- 正常完成（有 `[end]`）→ 可选择性跑 retrospect（见下节）
- 超时/失败（无 `[end]`）→ 进入恢复流程

### 恢复流程

```
旧子 session 崩溃
  ↓
主 session 检查 workspace/<task-id>/task.md
  ↓ 有 [end] → 正常退出，跳过
  ↓ 无 [end] → 恢复
  ↓
主 session 重新 spawn：
  sessions_spawn(
    task="[ROUTINE]\n...\n动作: 接续\n任务: 从 task.md 第一个未完成的 [working] 继续",
    mode="run", cleanup="delete",
    cwd="/path/workspace/<task-id>"
  )
  ↓
新子 session：
  → 读 task.md → 找第一个无对应 [working done] 的 [working]
  → 读对应步骤文件 → 了解已做的思考
  → 从失败点继续执行
  → 完成后追加 [working done] 和后续步骤
```

### 恢复优势

| 方案 | 成本 | 信息损耗 |
|------|------|---------|
| 主 session 重喂 | ~3.5K | 有（回忆不全） |
| 子 session 接续 | ~2.8K | 零（读 task.md + 步骤文件） |

---

## 技能优化闭环（Retrospect）

正常完成的任务可以跑一个轻量子 session 做回顾分析：

```
spawn 回顾子 session（同上协议，技能固定为 subagent-orchestrator）
  → 读工作区所有文件
  → 提取步骤耗时、异常类型和频率、是否需要更新 skill
  → 输出 task-retro.md（模板见 templates/task-retro.md）
```

如果同一 skill 的同一步骤多次出现同类错误 → 自动标记 skill 需要更新。

---

## 模板文件

- `templates/task.md` — checklist 模板
- `templates/task-retro.md` — 回顾分析模板
- `docs/protocol.md` — 完整设计文档（含更详细的设计决策）

---

## 约定总结

| 角色 | 职责 | 上下文增长 |
|------|------|-----------|
| 主 session | 路由、spawn、确认 announce | 低（每次 ~0.5K） |
| 子 session | 干重活、写文件、发消息 | 高（~20-50K），干完消失 |
| 回顾子 session | 复盘、优化分析 | 低（~5K），干完消失 |
