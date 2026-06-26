# Agent 协同工作协议规范 v1.0

> **纯协议层** — 不包含任何业务域特定内容
> 任何业务域只需实现本协议即可接入

---

## 1. 抽象架构

### 1.1 通用三层模型

```
┌────────────────────────────────────────────┐
│              Layer 0: 总调度层              │
│  识别业务域 → 分派给对应 Manager → 验收     │
├────────────────────────────────────────────┤
│            Layer 1: 业务 Manager            │
│  需求理解 → 任务分解 → 分发 → 汇总          │
├────────────────────────────────────────────┤
│          Layer 2: 业务 Specialist           │
│  接收任务 → 执行 → 交付                     │
└────────────────────────────────────────────┘
```

### 1.2 层级契约

| 层级 | 角色 | 能否调子Agent | 与上下级通信方式 |
|------|------|:-----------:|:--------------:|
| L0 | 总调度 | ✅ 可调所有L1 Manager | L0→L1：自然语言任务描述 |
| L1 | Manager | ✅ 可调本域L2 Specialist | L1→L2：标准JSON任务包 |
| L2 | Specialist | ❌ 不可再分发 | L2→L1：`<agent-response>` 块 |

### 1.3 约束

| 参数 | 推荐值 | 说明 |
|------|:-----:|------|
| maxSpawnDepth | 3 | L0→L1→L2，最多3层 |
| maxChildrenPerAgent | 5 | 每Manager最多同时调5个Specialist |
| L1任务超时 | 1800s | Manager整体完成时限 |
| L2任务超时 | 600s | 单个Specialist完成时限 |

---

## 2. Agent 标识规范

### 2.1 ID 命名规则

```
{domain}-{role}[-{subrole}]

domain: 业务域标识，小写字母+连字符
role:   角色名，小写字母+连字符
```

**示例（非限定）：**
- `{domain}-manager` — 该域的 Manager
- `{domain}-{role}` — 该域的 Specialist

### 2.2 工作区路径规则

```
~/.openclaw/workspace/{domain}/{role}/
```

### 2.3 配置文件中的依赖声明

每个 Manager 在 `openclaw.json` 中声明其可调用的 Specialist：

```json
{
  "id": "{domain}-manager",
  "subagents": {
    "allowAgents": ["{domain}-{role1}", "{domain}-{role2}", ...]
  },
  "skills": ["subagents", "sessions-spawn", ...]
}
```

---

## 3. 任务契约格式

### 3.1 L1 → L2：Manager 下发任务给 Specialist

```json
{
  "protocol": "acp-v1",
  "task_id": "{domain}-{seq}-{random8}",
  "from": "{manager_id}",
  "to": "{specialist_id}",
  "type": "request",
  "created_at": "ISO-8601 时间戳",
  "ttl_seconds": 600,
  "manifest": {
    "project": "项目/任务名称",
    "context": "任务背景描述",
    "goals": ["目标1", "目标2"],
    "input": {
      "references": ["参考文档或前置交付物"],
      "constraints": ["约束条件"]
    },
    "deliverables": [
      {
        "name": "交付物名称",
        "format": "交付物格式",
        "expected_path": "output/{filename}"
      }
    ],
    "decision_points": ["需要 Specialist 决策的事项"]
  }
}
```

### 3.2 L2 → L1：Specialist 回复给 Manager

必须用 `<agent-response>` XML 块包裹：

```markdown
<agent-response>
agent_id: {specialist_id}
status: completed | failed | partial
task_id: {task_id}
duration_seconds: {耗时秒数}

## 执行摘要
简要说明做了什么、关键发现

## 交付物
- [交付物名称](output/{filename})

## 关键决策
1. 选择了 {方案A} 因为 {理由}

## 待办/风险
- [ ] 待确认事项
- ⚠️ 风险提醒
</agent-response>
```

### 3.3 L1 → L0：Manager 汇报给总调度

同样使用 `<agent-response>` 块：

```markdown
<agent-response>
status: completed | failed | partial
task_id: {task_id}
duration_seconds: {总耗时}

## 执行摘要
已完成{项目名}的整体分析和分发

## 子任务执行情况
| Specialist | 状态 | 交付物 |
|------------|:----:|--------|
| {role1} | ✅ | 链接 |
| {role2} | ❌ | 原因 |

## 关键决策
- {决策1}

## 最终交付物
- [汇总报告](output/summary.md)

## 待办/建议
- [ ] 需要用户确认的事项
</agent-response>
```

---

## 4. 错误处理协议

### 4.1 错误码与处理策略

| 场景 | 处理方式 | 返回状态 |
|------|---------|:--------:|
| Specialist 超时 | Manager 重试 1 次，仍超时则降级 | `partial` |
| Specialist 返回 failed | Manager 分析原因，修正后重发，最多 2 次 | `partial` / `failed` |
| Specialist spawn 失败 | Manager 跳过，报告中标注 | `partial` |
| Specialist spawn 被平台拦截（forbidden） | 不重试，直接报告配置错误，由 main 处理 | `failed` |
| 交付物不合格 | Manager 退回 + 修改意见，最多 2 次 | `partial` |
| 全部成功 | — | `completed` |

### 4.2 超时传递

```
L0 → Manager：1800s 超时
  Manager → Specialist1：600s 超时
  Manager → Specialist2：600s 超时
  Manager 汇总时间：600s
```

---

## 5. Manager 调用 Specialist 规范

Manager 有两种方式与 Specialist 通信，按需选择：

### 5.1 方式一：sessions_spawn（一次性任务）

适用于 Specialist **执行完即结束**的场景，如架构设计、编码、测试。

```javascript
sessions_spawn({
  agentId: "{specialist_id}",
  mode: "run",           // 一次性运行，完成后自动结束
  runtime: "subagent",
  task: JSON.stringify({
    protocol: "acp-v1",
    task_id: "{domain}-{seq}-{random8}",
    from: "{manager_id}",
    to: "{specialist_id}",
    type: "request",
    manifest: { /* 见第三节 */ }
  })
})
// 返回结果：子Agent运行完成后，自动将结果返回给调用方
```

**特点：**
- 子 Agent 执行完自动结束
- 调用方（Manager）通过 yield 等待结果回来
- 适合明确的一次性交付任务

---

### 5.2 方式二：sessions_send（多轮对话）

适用于需要与 Specialist **持续多轮交互**的场景，如需求讨论、方案评审、迭代修改。

#### 前置条件：Specialist 需以常驻会话方式存在

```javascript
// Step 1: 先用 sessions_spawn 创建常驻 Specialist 会话
const spawnResult = await sessions_spawn({
  agentId: "{specialist_id}",
  // 注意：不传 mode:"run"，创建的是持久的交互式会话
  task: "请准备就绪，等待接收任务指令"
});
// spawnResult 中会返回该会话的 sessionKey
const specialistSessionKey = spawnResult.childSessionKey;
```

#### 后续多轮对话

```javascript
// Step 2: 通过 sessions_send 持续交互
const reply = await sessions_send({
  sessionKey: "{specialistSessionKey}",
  message: JSON.stringify({
    protocol: "acp-v1",
    task_id: "{domain}-{seq}-{random8}",
    from: "{manager_id}",
    to: "{specialist_id}",
    type: "request | review | revise | approve",
    round: 1,              // 对话轮次，递增
    manifest: {
      project: "项目名",
      context: "任务背景",
      goals: ["目标"],
      action: "initial | revise | finalize",
      feedback: "（如果是修改轮次）修改意见"
    }
  }),
  timeoutSeconds: 300
});
```

**特点：**
- 可以多次发送消息，Specialist 保持上下文
- 适合迭代式工作：初稿 → 评审 → 修改 → 定稿
- 调用方（Manager）需记录 sessionKey
- 每次调用用 `round` 字段标记轮次

---

### 5.3 两种方式的对比

| 维度 | sessions_spawn（一次性） | sessions_send（多轮） |
|------|:-----------------------:|:--------------------:|
| 生命周期 | 执行完自动结束 | 持续存在，手动结束 |
| 交互次数 | 1次请求 → 1次回复 | 多次往返 |
| 适用场景 | 架构设计、编码、测试 | 需求讨论、方案评审、迭代修改 |
| 上下文保持 | 每次重新加载 | 跨轮次保持 |
| 调用方式 | spawn + yield 等待 | send → 回复 → send → 回复 |
| 资源消耗 | 低（用完即销毁） | 高（常驻内存） |

**推荐原则：**
- 能用 `spawn` 就不要用 `send`——更轻量、更可靠
- 只有确实需要多轮讨论（如需求澄清、方案迭代）时才用 `send`

---

### 5.4 工作流模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **并行** | 同时 spawn 多个 Specialist | 无依赖关系的任务 |
| **串行** | 等上一个完成再调下一个 | 有依赖关系的任务 |
| **混合** | 先并行再串行 | 最常见模式 |
| **迭代** | 用 send 反复交互 | 需多轮讨论或修改 |

---

## 6. AGENTS.md 标准结构

所有 Agent 的 `AGENTS.md` 必须遵循以下结构，**且仅包含角色特定内容**：

```markdown
# {AGENT_NAME} · 操作手册

> 协议: ACP v1.0 | 版本: 2.0
> 参考: ~/.openclaw/protocol/AGENT_COLLAB_PROTOCOL.md

---

## 协议实现

| 协议章节 | 对本 agent 的具体要求 |
|---------|---------------------|
| §1 架构 | 我是 L_LEVEL_，{层级说明} |
| §3.1 任务格式 | {如何解析输入} |
| §3.2 回复格式 | {如何组织输出} |

---

## 1. 工作流程

### 阶段一：接收
{如何接收和理解任务}

### 阶段二：执行
{具体的执行步骤，编号列表}

### 阶段三：交付
{如何交付结果}

---

## 2. 输入/输出契约

| 方向 | 格式 | 说明 |
|------|------|------|
| 输入 | {JSON Task 包 / 自然语言} | {具体说明} |
| 输出 | `<agent-response>` Markdown 块 | 必须包含 agent_id、status、交付物、关键决策 |

---

## 3. 子Agent调度（仅 Manager 且有子Agent的 Specialist）

| 子Agent | 角色 | 调用时机 |
|---------|------|---------|
| {agent_id} | {角色} | {何时调用} |

**调用方式：** sessions_spawn，带标准 JSON Task 包（协议 §3.1）

---

## 4. 输出标准

- 交付物保存到 `output/` 目录
- 文件命名：`{文件名前缀}_{YYYYMMDD}.md`
- 必须包含 `<agent-response>` 块（含 agent_id 字段）

---

## 5. 反模式

- ❌ {绝对不该做的事1}
- ❌ {绝对不该做的事2}
- ❌ {绝对不该做的事3}
```

> 模板文件：`~/.openclaw/protocol/TEMPLATE_AGENTS.md`。新增 agent 时复制模板并填入 {} 中的变量。

---

## 7. 接入新业务域的步骤

任何新业务域只需完成以下 5 步即可接入协议：

| 步骤 | 操作 | 涉及文件 |
|:----:|------|---------|
| 1 | 在 openclaw.json 中定义 Manager 和 Specialist agents | openclaw.json |
| 2 | 为每个 agent 创建工作区目录 | workspace/{domain}/{role}/ |
| 3 | 编写每个 agent 的 AGENTS.md（遵循第6节模板） | workspace/{domain}/{role}/AGENTS.md |
| 4 | 将 Manager 加入 main 的 subagents.allowAgents | openclaw.json |
| 5 | 将 Specialist 加入 Manager 的 subagents.allowAgents | openclaw.json |

**不需要修改本协议文件。**

---

## 8. 故障排查清单

| # | 检查项 | 修复方式 |
|---|--------|---------|
| 1 | AGENTS.md 是否超过 12,000 字符？ | 精简，仅保留角色特有内容 |
| 2 | 子 Agent 在父 Agent 的 allowAgents 中？ | 更新 openclaw.json |
| 3 | Manager 有 subagents + sessions-spawn 技能？ | 添加到 skills 列表 |
| 4 | 调用深度超过 maxSpawnDepth？ | 调整层级或配置 |
| 5 | 并行数超过 maxChildrenPerAgent？ | 等待或调整配置 |
| 6 | Specialist 工作区目录存在？ | 创建目录 |
| 7 | JSON 格式是否符合第3节契约？ | 对照 schema 检查 |

---

## 9. 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-05-12 | 初始版本，纯协议层，不包含任何业务域特定内容 |
