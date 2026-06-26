# State Lifecycle — 任务状态机

> 借鉴 A2A Protocol 的任务生命周期模型。所有 Agent 任务共享同一状态语义。

## 六种状态

```
submitted → working → completed
     ↘ input-required → (人类/上游响应) → working
     ↘ failed → (诊断后) → submitted (重试)
     ↘ canceled
```

| 状态 | 定义 | 谁操作 |
|------|------|--------|
| `submitted` | 任务已分发，接收者尚未开始 | 编排者（Orion/Leroy） |
| `working` | 接收者正在执行 | 执行 Agent |
| `input-required` | 需要人类决策或上游补充 | 执行 Agent（自动触发） |
| `completed` | 产出已交付且通过验证 | 编排者（验证后标记） |
| `failed` | 执行失败，含失败原因 | 执行 Agent |
| `canceled` | 人类主动取消 | 人类 |

## 状态转换规则

### submitted → working
- 触发条件：接收 Agent 读取了交接文档并开始执行
- 操作者：接收 Agent
- 副作用：更新 `PROJECT_STATE.yaml` 中对应任务的 `status: working`

### working → completed
- 触发条件：产出写入约定路径 + 验证通过
- 操作者：编排者（Orion）验证后标记
- 副作用：milestone 更新；通知下游 Agent

### working → input-required
- 触发条件：Agent 遇到 P0/P1 问题（见 Human 决策矩阵）
- 操作者：执行 Agent 自动设置
- 副作用：通知编排者（Orion）上报人类

### working → failed
- 触发条件：Agent 执行失败（工具故障/路径不存在/依赖缺失）
- 操作者：执行 Agent
- 副作用：记录失败原因到交接文档的 `failure_reason` 字段

### failed → submitted（重试）
- 触发条件：人类确认修复方案后重新分发
- 操作者：编排者
- 副作用：清空 `failure_reason`；重置计数器

## Human 决策矩阵（状态映射）

| 审核发现级别 | 状态转换 | 人类操作 |
|-------------|---------|---------|
| P2（格式/美化） | working → completed（自动） | 无需介入 |
| P1（语气/措辞） | working → input-required → working | Agent修复后人类复核 |
| P0（事实错误/禁用词泄漏） | working → input-required | 人类必须审批修复方案 |
| 框架方向变更 | 任意 → input-required | 人类确认后才能继续 |
| 工具阻塞（MCP故障） | working → input-required | 人类确认修复方案 |
| 迭代次数 > 3 | 任意 → input-required | 人类审批是否继续 |

## 阶段门控类型分类

项目阶段（Phase）转换有三种门控类型：

| 转换 | 门控类型 | 说明 |
|------|---------|------|
| INIT → RESEARCH | 🔴 HUMAN GATE | 必须等待人类明确确认才能继续 |
| RESEARCH → FRAMEWORK | 🔴 HUMAN GATE | 调研质量须人类审核 |
| FRAMEWORK → EXECUTION | 🔴 HUMAN GATE | 框架方向须人类确认 |
| EXECUTION → AUDIT | ⚡ AUTO GATE | 禁用词扫描通过即自动进入，不需要人类介入 |
| AUDIT → ITERATION | 📊 CALIBRATED GATE | 根据发现严重程度自动判断（P0→人类；P1→Agent+人类；P2→自动） |
| AUDIT → DELIVERY | 📊 CALIBRATED GATE | 无P0/P1发现时自动进入交付 |
| ITERATION → AUDIT | ⚡ AUTO GATE | 修订完成+扫描通过即自动回到审核 |
| DELIVERY → 完成 | 🔴 HUMAN GATE | 最终交付物须人类确认 |

## PROJECT_STATE.yaml 中的任务对象

```yaml
tasks:
  - id: "SG-EX-v4-build"          # 任务ID
    type: execution                # research | framework | execution | audit | iteration
    title: "PPT v4 构建"
    assignee: codex
    status: completed             # 当前状态
    status_history:               # 状态变更历史
      - status: submitted
        timestamp: "2026-04-10T13:00+08:00"
        actor: orion
      - status: working
        timestamp: "2026-04-10T13:05+08:00"
        actor: codex
      - status: completed
        timestamp: "2026-04-10T18:00+08:00"
        actor: orion
    handoff_doc: "00_pipeline/handoffs/SG-EX-to-AU-v4.md"
    output: "03_PPT框架协作包/08_v4审核收口版/"
    created: "2026-04-10T13:00+08:00"
    updated: "2026-04-10T18:00+08:00"
    failure_reason: null          # failed 时记录原因
    retry_count: 0
```
