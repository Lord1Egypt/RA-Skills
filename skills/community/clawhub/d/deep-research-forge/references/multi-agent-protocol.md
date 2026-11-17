# Multi-Agent Protocol

它定义的是从"谁负责什么研究维度"到"可验证的证据合并运行时合同"的完整链条：

- 角色分工与激活信号
- 研究任务状态机
- 实际 Agent 调度执行指南
- 冲突解决与失败重试
- 并行执行汇总

Prompt / Skill 仍然负责语义判断；本协议负责硬性运行纪律。

---

## 一、激活信号

使用 `parallel-research-sprint` 当满足以下信号之一：

- 用户明确要求 multi-agent、parallel、swarm、team 或"分头查"。
- 课题跨至少三个可分离轴（来源验证、时间线、竞品、用户信号、决策风险）。
- 证据易变或矛盾，需要独立交叉验证。
- 用户需要可复用资料包或可追溯证据覆盖。
- 研究截止时间有利于并发收集再合成。

**保持单线程当**：用户只要简短解释；研究问题尚未框定；主要阻塞是单一来源或单一决策上下文；并行工作会重复同一搜索。

---

## 二、角色定义

| 角色 | 职责 | 输出 |
| --- | --- | --- |
| `lead-integrator` | 研究问题、任务拆分、证据合并、最终合成 | 协调合成与最终产物 |
| `source-scout` | 主要来源、来源谱系、时效性、重复报道 | 来源地图与证据缺口 |
| `timeline-analyst` | 起源、里程碑、阶段变化、路径依赖 | 因果时间线笔记 |
| `competitive-analyst` | 直接竞品、替代品、用户选择、生态位置 | 竞品地图笔记 |
| `user-signal-analyst` | 评论、issue、论坛、社交反馈、重复抱怨 | 用户信号账本条目 |
| `dissent-reviewer` | 负面证据、矛盾、替代解释 | 最强反对意见与反转条件 |
| `decision-analyst` | 判决、置信度、风险、监控阈值 | 决策口径笔记 |
| `evidence-verifier` | 证据质量验证、pass/fail/hold 判决 | 验证报告 |
| `conflict-arbiter` | 证据冲突仲裁（Evidence-Verifier 触发） | 冲突解决报告 |

使用最小有效集合。大多数研究 sprint 需要 `lead-integrator` + 2-3 个专家角色，不需要全部角色。

角色级别的详细 dispatch card 见 [assets/agent-dispatch-cards.md](../assets/agent-dispatch-cards.md)。

---

## 三、执行合同

Lead Integrator 在派发前必须输出：

```text
Research question:
Output target:
Evidence window:
Parallel lanes:
Shared definitions:
Source priority:
Merge deadline:
Known gaps:
```

每个专家角色返回：

```text
Role:
Task:
Key findings:
Evidence IDs:
Confidence:
Contradictions:
What would change my view:
Hand-off notes:
```

### 独立性保证

**每个 Research Agent 必须是独立调用，不能是角色扮演。**

- ❌ 错误：`你现在扮演 source-scout 角色，查找来源：...`
- ✅ 正确：`[唤起独立 Agent - source-scout]` → 独立 prompt → `[等待输出]`

如果环境不支持多 Agent 并行，必须告知用户并降级为串行独立调用。串行独立调用比单 Agent 模拟多角色更准确，但执行时间约 N 倍。

### 证据账本隔离

每个 Agent 的证据账本条目保存为独立变量，再传给 Lead Integrator。所有证据必须有 `evidence_id` 和 `lane_id`。

### 并行配置

| 配置 | 角色数 | 适用场景 |
| --- | --- | --- |
| 最小 | 3（source-scout + 1 analyst + lead-integrator） | 简单研究 |
| 标准 | 5（source-scout + timeline + competitive + dissent + lead-integrator） | 推荐默认 |
| 完整 | 7（+ user-signal + decision-analyst） | 复杂课题 |

---

## 四、研究任务状态机

### 合法状态

- `planned`：已规划，未启动
- `spawned`：已派发给 Researcher
- `researching`：研究进行中
- `produced`：Researcher 产出完成
- `verifying`：Evidence-Verifier 验证中
- `conflict_arbitrating`：冲突仲裁中
- `retrying`：返工中
- `passed`：验证通过
- `failed`：验证失败
- `hold`：暂停（需补充信息）
- `escalated`：升级到人工
- `accepted`：Lead Integrator 接受

### 合法转移

```text
planned -> spawned
spawned -> researching
researching -> produced
produced -> verifying

verifying -> passed
verifying -> conflict_arbitrating
verifying -> retrying
verifying -> hold
verifying -> failed

conflict_arbitrating -> passed
conflict_arbitrating -> retrying
conflict_arbitrating -> escalated

retrying -> researching
passed -> accepted
hold -> escalated
failed -> escalated
```

### 硬规则

1. `accepted` 只能来自 `passed`
2. `retrying` 必须携带 `retry_patch`
3. `passed` 必须携带 `verification_report.verdict = pass`
4. `conflict_arbitrating` 必须携带 `conflict_summary`
5. `failed / hold` 必须携带 `blocker` 或 `escalation_reason`
6. `cycle_count > max_cycles` 时必须进入 `escalated`
7. 依赖任务未 `passed` 时，下游任务不得从 `planned` 进入 `spawned`

---

## 五、标准对象

### ResearchEnvelope（研究信封）

每个并行子任务需要一个 ResearchEnvelope，Schema 见 [research-envelope.schema.json](research-envelope.schema.json)。最小必填字段：

```yaml
research_envelope:
  task_id: "rt001"
  research_question: "具体研究问题"
  research_dimension: "ecosystem-mapping"
  researcher_role: "ecosystem-analyst"
  verifier_role: "evidence-verifier"
  evidence_quality_gates:
    - gate: "source_reliability"
      threshold: "至少 3 个独立来源"
  max_cycles: 3
  dependency_ids: []
  conflict_resolution_policy:
    strategy: "evidence-conflict-resolution-protocol"
    auto_resolve: true
  human_escalation_policy:
    escalate_on: ["max_cycles_reached", "unresolvable_conflict"]
```

完整模板见 [assets/research-envelope-template.md](../assets/research-envelope-template.md)。

### ResearcherOutput（研究产出）

```yaml
researcher_output:
  task_id: "rt001"
  researcher_role: "ecosystem-analyst"
  cycle_number: 1
  key_findings: [...]
  evidence_ledger_entries: [...]
  contradictions_found: [...]
  confidence_level: "medium"
  assumptions: [...]
  known_gaps: [...]
  self_reported_done: true
```

**禁止**：给自己最终 `pass/verified`；修改 Verifier 的 verdict；在 retry 时抹掉上一轮失败原因；发明证据。

### VerificationReport（验证报告）

Schema 见 [verification-report.schema.json](verification-report.schema.json)。完整模板见 [assets/verification-report-template.md](../assets/verification-report-template.md)。

关键字段：

- `verdict`: `pass` / `fail` / `hold`
- `verified_dimensions`: 5 维检查（source_reliability、recency、completeness、independence、corroboration）
- `confirmed_evidence_ids` / `rejected_evidence_ids` / `flagged_evidence_ids`
- `retry_patch`：verdict=fail 时必填
- `conflict_summary`：有冲突时必填

**验证维度**：

1. 来源可靠性：是否符合 source-strategy.md 分级标准
2. 时效性：是否在有效期内
3. 独立性：是否真正独立佐证（检查 upstream_source_id）
4. 完整性：是否回答了 ResearchEnvelope 中的研究问题
5. 冲突处理：是否识别并记录了所有证据冲突

**禁止**：替 Researcher 直接产出完整研究结论；用偏好替代证据；在未检查 evidence_quality_gates 时给 `pass`。

### ConflictResolutionReport（冲突解决报告）

Schema 见 [conflict-resolution-report.schema.json](conflict-resolution-report.schema.json)。

关键内容：

- 每个 conflict 的 `conflict_type`（time_difference / observation_angle / methodology / interest_bias / source_genealogy）
- `resolution_decision.strategy`（prefer_latest / prefer_most_reliable / preserve_both_with_context / prefer_independent_source / methodology_difference / unresolvable）
- `confidence_impact_summary`
- `escalation_needed`

### ResearchCycleReport（研究周期报告）

```yaml
research_cycle_report:
  research_sprint_id: "rs001"
  cycle_number: 1
  tasks_summary:
    total: 5
    completed: 3
    in_progress: 1
    blocked: 1
  completed_tasks: [...]
  blocked_tasks: [...]
  conflicts_resolved: 1
  conflicts_escalated: 0
  evidence_ledger_stats:
    total_entries: 47
    confirmed: 42
    rejected: 3
    flagged: 2
  merge_judgment:
    accepted_lanes: [...]
    downgraded_lanes: [...]
    rejected_lanes: [...]
  coverage_gaps:
    critical: [...]
    medium: [...]
    low: [...]
  next_action: "..."
  estimated_completion: "80%"
```

支持跨会话恢复。

### 跨会话恢复约定

ResearchCycleReport 可持久化以支持中断后恢复：

- 保存路径：`.skill-iterations/{research_sprint_id}.json`
- 新会话启动时检查该目录是否存在未完成的 sprint
- 恢复时读取 `tasks` 中各任务 `state`，从最后已知状态继续
- 已 `accepted` 的任务无需重跑；`hold` 或 `escalated` 的任务需人工确认后继续

---

## 六、执行指南

### Agent Prompt 骨架

每个 Research Agent 使用以下骨架，按角色填充变量：

```text
你是{role_name}（{role_english}）。你的任务是为以下研究问题{task_description}。

研究问题：{research_question}
证据窗口：{evidence_window}
证据质量门禁：{evidence_quality_gates}

你的职责：
{role_responsibilities}

输出格式：JSON
{
  "role": "{role_key}",
  "task": "...",
  "key_findings": [...],
  "evidence_ledger_entries": [
    {
      "evidence_id": "...",
      "lane_id": "{role_key}",
      "source_type": "...",
      "source_url": "...",
      "source_title": "...",
      "published_at": "...",
      "accessed_at": "...",
      "reliability": "high|medium|low",
      "claim": "...",
      "status": "confirmed_fact|reported_claim|user_signal|inference|gap"
    }
  ],
  "confidence": "high|medium|low",
  "known_gaps": [...],
  "contradictions_found": [...]
}
```

**输出约束：**

- `evidence_ledger_entries` 最多 15 条；优先返回最强证据，弱证据合并为一条 `gap`
- `key_findings` 最多 5 条
- 如果证据超过 15 条，选择 citation_strength 最高的保留，其余写入 `known_gaps`

角色职责摘要（完整版见 [assets/agent-dispatch-cards.md](../assets/agent-dispatch-cards.md)）：

| 角色 | 核心职责 |
| --- | --- |
| source-scout | 找原始来源、来源谱系、时效性、重复报道 |
| timeline-analyst | 起源、里程碑、阶段变化、路径依赖 |
| competitive-analyst | 直接竞品、替代品、用户选择、生态位置 |
| user-signal-analyst | 评论、issue、论坛、社交反馈、重复抱怨 |
| dissent-reviewer | 负面证据、矛盾、替代解释、反转条件 |
| decision-analyst | 判决、置信度、风险、监控阈值 |

### Lead Integrator Prompt 骨架

```text
你是研究整合专家（Lead Integrator）。你收到了多个独立研究角色的报告。

{各角色报告 JSON}

任务：
1. 去重：合并引用同一上游来源的证据
2. 分级：区分硬事实 vs 社区信号
3. 冲突处理：保留矛盾并标记；单源降级为 reported_claim；多源印证晋升为 confirmed_fact
4. 覆盖缺口：列出所有角色都无法验证的内容
5. 置信度：评估整体研究置信度
6. 最终判断：回答研究问题

冲突解决规则：
- 官方文档 > 新闻报道 > 社区讨论
- 多方独立印证 > 单一来源
- 优先采纳最新信息（除非旧信息有历史价值）
- 矛盾保留：不要为了一致性而抹掉矛盾
```

### 执行检查清单

- [ ] 是否使用了独立 Agent 调用（非角色扮演）？
- [ ] 每个 Agent 是否有独立的 Prompt？
- [ ] 每个 Agent 的输出是否保存为独立变量？
- [ ] Lead Integrator 是否接收所有独立输出？
- [ ] 每个证据条目是否有 `evidence_id` 和 `lane_id`？
- [ ] 是否执行了证据去重和冲突解决？

---

## 七、冲突解决

### 触发条件

Evidence-Verifier 发现无法自动解决的证据冲突 → `verdict: hold` → 触发 Conflict Arbiter。

### Conflict Arbiter 职责

1. 分析冲突类型（time_difference / observation_angle / methodology / interest_bias / source_genealogy）
2. 应用 resolution strategy
3. 输出 ConflictResolutionReport
4. 降低置信度或标注 unresolved-conflict

### 冲突类型与解决策略

| 冲突类型 | 典型策略 | 说明 |
| --- | --- | --- |
| time_difference | prefer_latest | 时间差异导致的不同结论 |
| observation_angle | preserve_both_with_context | 观察角度不同 |
| methodology | methodology_difference | 方法论差异 |
| interest_bias | prefer_independent_source | 利益相关偏差 |
| source_genealogy | prefer_most_reliable | 同源转载 |

---

## 八、失败与重试

### 常见失败模式

| 失败类型 | Verifier 判决 | Retry Patch 内容 |
| --- | --- | --- |
| 证据不足 | `fail` | 补充搜索关键词、来源提示 |
| 来源可疑 | `fail` | 提升来源可靠性要求 |
| 时效性差 | `fail` | 限定时间范围 |
| 证据冲突 | `hold` | 触发 Conflict Arbiter |
| 完整性不足 | `fail` | 列出缺失维度 |

### Retry 流程

1. Verifier 输出 `retry_patch`
2. Engine 检查 `cycle_count < max_cycles`
3. 如果未超限 → 状态转为 `retrying`，Researcher 根据 `retry_patch` 重新研究
4. 如果超限 → 状态转为 `escalated`，升级到 Human

### Retry 策略变化建议

每次 retry 应递进调整策略，而不是重复相同的搜索：

| Cycle | 策略变化 | 示例 |
| --- | --- | --- |
| 1st retry | 扩大搜索范围 | 从仅搜 Reddit → 加官方文档、GitHub issues |
| 2nd retry | 提升来源要求 | 从 media → 要求 official/public_record |
| 3rd retry | 放松约束或换角度 | 无法找到 primary → 记录为 gap 并降低置信度 |

**禁止**：在 retry 中使用与上一轮完全相同的搜索关键词和来源策略。

### Human Escalation

触发条件：证据严重冲突且无法自动解决；`max_cycles` 耗尽；研究成本超出预期；研究问题需要重新框定；高风险决策。

必须接收：`human_escalation`、`escalation_reason`、`options`、`risk_if_continue`、`latest_cycle_report`、`evidence_summary`。

---

## 九、证据合并规则

Lead Integrator 在合并时必须：

1. 去重：追溯到同一源头的报道去重
2. 分级：只有有来源支持的声明才能进 `confirmed_fact`
3. 分离：社区信号与硬事实分开
4. 保留矛盾：不平滑矛盾，交给 Conflict Arbiter
5. 标注贡献：说明哪个 lane 对结论影响最大
6. 标记缺口：未解决的冲突标为 `gap` 或 `reported_claim`
7. 保留溯源：保留 `lane_id`、`agent_role`、`upstream_source_id`、`corroboration_group`
8. 统一输出：产出一份最终报告，不是多个 agent 的转录
9. 合并审计：高风险或矛盾多的研究必须附 `parallel-merge-audit-block`
10. 冲突解决追溯：每个解决的冲突必须记录解决策略和置信度影响
11. 证据账本版本控制：合并后的证据账本必须带版本号和合并时间戳

**不要让 agent 数量制造虚假共识。共识只在证据独立时才有效。**

---

## 十、并行执行汇总

完成并行研究后，必须包含此章节：

### 汇总表

| Role | Task | Main Contribution | Confidence | Cycles | Open Issue |
| --- | --- | --- | --- | --- | --- |

### 合并判断

- **接受的 lanes**：
- **降级的 lanes**：
- **拒绝的 lanes**：

### 冲突处理

- **已解决冲突**：
- **未解决冲突**：

### 覆盖缺口

- **Critical**：
- **Medium**：
- **Low**：

### Merge Audit（高风险/矛盾多时）

```text
Most conclusion-changing lane:
Accepted claims:
Downgraded claims:
Rejected claims:
Shared upstream sources deduplicated:
Remaining conflicts:
Final confidence adjustment:
```

---

## 十一、校验

交付前运行 [scripts/lint_research_output.py](../scripts/lint_research_output.py) 校验（支持 JSON + Markdown）：

- 证据账本完整性（confirmed_fact 有来源、reported_claim 有 corroboration 标记）
- 状态机合法转移（accepted 只来自 passed、retrying 有 retry_patch、max_cycles 超限进入 escalated）
- 质量门禁合规（verdict 与维度状态一致、fail 有 retry_patch）
- 并行执行结构（ResearchCycleReport 字段完整、evidence ID 不重复）
- JSON Schema 校验（自动检测输出类型，优先使用 jsonschema 库，fallback 到一致性检查）
- Markdown 校验（证据窗口声明、Evidence ID 引用、置信度声明、反转条件、空话标记词）

测试用例见 [scripts/test-fixtures/](../scripts/test-fixtures/)，运行 `python scripts/run_lint_tests.py` 验证。

---

**协议版本：** 2.1.0
**合并来源：** multi-agent-parallel-protocol.md + multi-agent-exec-guide.md + research-team-engine-protocol.md
**最后更新：** 2026-06-28
