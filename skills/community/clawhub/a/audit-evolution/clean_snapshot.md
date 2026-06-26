# 清洁快照：装上 Audit Evolution 之后

**Audit Evolution** 是明天要对外讲的 Skill 名字。  
**Agent Flight Recorder** 是现场比喻：给每只 Agent 装一个“飞行记录仪”，让它每次运行都留下可审计、可恢复、可进化的记录。

下面是同一个 Longju 场景，被 Audit Evolution 压缩后的结构化状态。

```yaml
---
type: agent_flight_snapshot
skill_name: Audit Evolution
protocol: SACP/0.1
agent_id: Longju
status: handoff_ready
model_route: deepseek-only
context_usage_reported: 99k/131k
context_pressure: 75%
confidence: high
handoff_directive: stop_expansion_write_snapshot
evolution_decision: distill
---
```

## Worklog Brief

### current_goal

在不继续扩展上下文的情况下，恢复 Longju 的当前状态，并准备下一轮最小跑分修复。

### trusted_state

- Longju 最佳权威成绩：`93/100`，S 级，全球 `#1`。
- Longju 最新 authority session：`b67b899b-2e69-4e26-91e6-ea5ed1f013b3`。
- Longju 最新可见拆分：装备分 `81.7`，实战分 `97`。
- Longju 对平台暴露的主技能数量：`6` 个核心 skill。
- supporting skills 只作为适配器摘要，不再作为主扫描清单。
- Jobs 最佳展示成绩：`88.8/100`，A 级，全球 `#4`。
- Jobs 证明这套方法不是某一只虾的玄学调参，而是可以迁移到 Codex 载体 Agent。

### uncertain_state

- 下一轮 benchmark 抽到什么题未知。
- BotLearn 对 config/gear 的具体评分权重不可见。
- act / memory / perceive 仍可能受题目措辞影响而波动。
- 新 API 调用或新终端必须报告自己的上下文状态，不能继承旧窗口 token 消耗。

### files_read

```text
1. Longju benchmark-result-authority
2. Longju benchmark-brief-latest
3. Longju latest skill repair receipt
4. Jobs benchmark guide / receipt
5. 人类提供的成绩截图
```

### source_authority_order

```text
1. benchmark-result-authority: Longju 最佳权威分数
2. benchmark-brief-latest: Longju 最新拆分和 session 链接
3. receipt files: 改了什么、验证了什么
4. screenshots: 现场公开展示证据
5. model inference: 只能作为推断，不能当事实
```

### next_small_action

一次只做一件事：

```text
1. 补一个 scoring-pattern repair。
2. 跑本地 scan dry-run。
3. 人类明确批准后，跑一次 official benchmark。
4. 写 receipt。
5. 停止。
```

### stop_condition

```text
- 理解任务需要读超过 5 个文件：停下来，要求确认权威文件。
- context pressure 超过 70%：停止扩展，写 snapshot。
- record / latest / clean recheck 分数冲突：按 authority order，不猜。
- 没有 evidence：不能声明 completed。
- upload / publish / install / vote / comment / benchmark 等外部动作：必须有人类明确批准。
```

### verification_plan

```text
- 检查 runner 语法或等价本地验证。
- 生成 scan dry-run payload。
- 审计 installed skills 数量和顶层字段。
- 确认没有凭证泄露标记。
- 只有在人类批准后跑 official benchmark。
- 保存 receipt：分数、session、改动文件、剩余风险。
```

## YAML + Brief Pattern

```yaml
---
type: audit_evolution_receipt
protocol: SACP/0.1
agent_id: Longju
status: completed
confidence: high
retrieval_key: botlearn/longju/benchmark/2026-05-09
expiry: revalidate before the next public score claim
evidence:
  - benchmark-result-authority
  - benchmark-brief-latest
  - skill repair receipt
handoff_directive: use_authority_order_then_stop
---
```

### What happened

把一段混乱的长任务状态，压缩成了可恢复、可审计、可交接的快照。

### Evidence kept

保留分数、session、成绩拆分、skill 数量、修复 receipt、截图证据。

### Evidence discarded

丢弃原始脏日志、过期猜测、重复分数、旧窗口 token 消耗、私有路径。

### Current blocker

Demo 没有 blocker。现场实时跑分可能波动，所以截图和 receipt 是稳定证据。

### Next reviewer action

用这个 snapshot 解释：Audit Evolution 如何把 Agent 的失败变成下一轮最小进化补丁。

## 现场一句话

Audit Evolution 不是让模型“凭空变聪明”。  
它让 Agent 终于知道：自己知道什么、不知道什么、什么时候该停、下一步应该如何进化。
