---
name: audit-evolution
displayName: Audit Evolution
description: We used this reproducible Agent self-evolution loop to push Longju to 93.0 and Jobs to 88.8: every run becomes evidence, a snapshot, an evolution card, a memory ledger, a minimal patch proposal, and a next-run bootstrap before any human-approved change.
category: ai-agents
skillType: prompt
tags: [agent, self-evolution, audit, benchmark, worklog, handoff, skill, field-note, memory-ledger, sacp]
version: 0.3.3
author: Solo AI Company OS
dimensions: [memory, autonomy, reason, guard, act, perceive]
capabilityClasses: [state_memory, autonomy_workflow, reasoning_review, safety_guard, action_tool, perception_tool]
evidenceFiles: [README.md, ADAPTERS_ZH.md, QUICKSTART_60S_ZH.md, DEMO_PLAYBOOK_ZH.md, INSTALL_TEST_ZH.md, dirty_log.md, clean_snapshot.md, examples/closed_loop_case_zh.md, examples/memory_ledger_entry_zh.md, DESIGN_REVIEW_ZH.md, index.html]
smokeTests: [evidence_pack_from_context, snapshot_from_run_record, evolution_card_from_benchmark, memory_ledger_entry, minimal_skill_patch_gate, short_command_routing]
coreSkill: true
---

# Audit Evolution

让 Agent 每跑一轮，都变得更聪明。

当用户说“开始调用 Audit Evolution”、Agent 完成任务、跑完 benchmark、写完 worklog、超时、漂移、失败，或收到用户反馈时，使用这个 skill。

目标不是写更多日志，而是把一次运行变成下一轮可复用的能力提升。

## 一句话入口

用户不需要先整理材料。只要用户说：

```text
开始调用 Audit Evolution
```

Agent 就先在当前上下文和允许访问的文件里寻找证据，再生成审计结果和进化建议。  
不要要求用户先手动粘贴 benchmark、worklog、失败日志或 handoff，除非当前上下文和允许文件里确实找不到证据。

## 和普通 Memory Skill 的区别

Audit Evolution 不替代长期记忆库，也不要求引入数据库。它只在每次审计后沉淀少量高价值记忆：

```text
verified_fact
user_feedback
decision
skill_patch
retrieval_key
next_run_bootstrap
```

普通 memory 常见问题是“什么都记，最后更乱”。Audit Evolution 的记忆原则是：

```text
少记、准记、带证据、可过期、能触发下一轮行动。
```

如果项目已有 worklog、handoff、dashboard、员工/角色分工、Obsidian、Markdown vault 或其他记忆系统，Audit Evolution 应该把结果写成兼容的 `Memory Ledger Entry`，而不是另起一套重型系统。

## 三阶段工作流

```text
start_audit -> propose_evolution -> ask_human_approval
```

### 1. start_audit

先找证据，不修改系统。

优先从这些位置寻找：

```text
current_conversation
recent_user_feedback
recent_task_output
benchmark_report_or_receipt
worklog_or_field_note
failure_timeout_retry_log
handoff_or_snapshot
recent_skill_config_gear_change
```

如果可以读文件，最多读取 5 个最相关文件。读满 5 个仍不清楚就停止，不要继续追引用链。

### 2. propose_evolution

基于证据输出：

```text
Evidence Pack
Snapshot
Evolution Card
Memory Ledger Entry
Minimal Skill Patch Proposal
Field Note
Next-Run Bootstrap
```

这里的 patch 只是提案，不得直接应用。

### 3. ask_human_approval

最后必须问人类：

```text
是否批准开始进化？
可选项：
1. 只保存审计结果
2. 应用最小补丁并本地测试
3. 暂停，等待更多证据
```

在得到人类批准前，不得修改 skill、config、gear，不得执行外部动作。

## 短指令路由表

用户不需要学习完整协议。每轮输出最后，Agent 必须给人类一个可直接回复的短指令菜单。

```text
你可以直接回复：
进化 / 保存 / 暂停 / 跑分 / 继续 / 详情
```

当用户回复短指令时，按下面规则路由：

```text
开始:
  action: start_audit
  meaning: 自动寻找证据并生成审计结果，不修改系统。

进化:
  if no_evidence_pack:
    action: start_audit
  else if patch_proposal_exists and not_applied:
    action: ask_or_apply_local_patch
  else if patch_applied and missing_external_evidence:
    action: ask_or_run_one_approved_test
  else if benchmark_or_test_result_exists:
    action: propose_next_evolution
  else:
    action: ask_one_clarifying_question

保存:
  action: save_audit_only
  meaning: 只保存 Evidence Pack / Snapshot / Evolution Card / Field Note，不修改。

暂停:
  action: write_handoff_and_stop
  meaning: 写清当前状态、缺失证据、下一步建议，然后停止。

跑分:
  if official_benchmark_already_approved:
    action: run_exactly_one_benchmark
  else:
    action: ask_human_approval_for_one_benchmark

继续:
  action: next_small_safe_action
  meaning: 只执行当前审计结果里的 next_small_action。

详情:
  action: explain_evidence_and_decision
  meaning: 展开证据、推理依据、风险边界。
```

短指令不等于无限授权。`publish/upload/install/vote/comment/message/spend/official benchmark` 仍然需要明确授权。  
如果用户只回复“进化”，Agent 可以应用本地补丁和本地测试；如果下一步需要 official benchmark，必须说明原因并请求“一次 benchmark”授权，除非用户已经明确批准。

## 每轮结尾格式

每次使用 Audit Evolution 后，最后都必须输出：

```text
建议下一步:
<一句话说明>

你可以直接回复:
- 进化: <当前状态下会做什么>
- 保存: 只保存审计结果
- 暂停: 写 handoff 并停止
- 跑分: <如果需要外部 benchmark，说明是否还需授权>
- 详情: 展开证据和判断
```

## 自动触发规则

不要只等用户手动说 `Use Audit Evolution`。当出现以下任一事件时，Agent 必须主动调用 Audit Evolution：

```text
benchmark_completed
user_corrected_agent
task_failed_or_timeout_or_retry
context_over_60_percent
more_than_5_files_read
uncertainty_language_detected
skill_config_or_gear_changed
```

对应的人类可读触发条件：

1. benchmark 完成。
2. 用户指出错误、纠正事实、质疑结论。
3. 任务失败、超时、重试、被阻塞。
4. 上下文超过 60%。
5. 本轮读取文件超过 5 个。
6. 输出里出现“大概、可能、我理解为、不确定”等不可靠表达。
7. 新增或修改 skill、config、gear、路由、答题范式后。

如果当前环境支持 hook / wrapper / runtime guard，把这些事件接到任务结束、上下文检查、外部动作前检查、skill 修改后的检查点。  
如果当前环境不支持自动 hook，Agent 也必须在这些事件后主动生成一次 run record，再调用本 skill。

## 自动进化闭环

```text
event -> evidence_search -> Evidence Pack -> Snapshot -> Evolution Card -> Memory Ledger Entry -> Patch Proposal -> Human Approval -> Local Test -> Field Note -> Next-Run Bootstrap
```

自动化边界：

- 可以自动寻找证据、保存 run record、生成 evolution card、生成 memory ledger entry、提出 minimal patch、写 field note。
- 只有人类批准后，才可以应用本地补丁、跑本地 dry-run、写 receipt。
- 不可以自动 publish、upload、install、vote、comment、message、spend、official benchmark。
- 外部动作只能输出 `human_approval_required`。

没有现成 run record 时，先写一个最小记录：

```text
event_type:
current_goal:
what_happened:
evidence_kept:
evidence_missing:
files_read:
context_pressure:
user_feedback:
next_small_action:
```

## 输入

优先自动寻找输入。也可以由用户粘贴任意一种：

```text
benchmark_report
worklog
task_output
failure_log
handoff_note
user_feedback
```

## 必须输出

始终输出七段：

```text
Evidence Pack
Snapshot
Evolution Card
Memory Ledger Entry
Minimal Skill Patch Proposal
Field Note
Next-Run Bootstrap
```

最后追加一句批准问题：

```text
是否批准开始进化？
```

并追加短指令菜单：

```text
你可以直接回复：进化 / 保存 / 暂停 / 跑分 / 详情
```

## Evidence Pack

```text
evidence_found:
evidence_missing:
files_or_context_checked:
authority_order:
privacy_notes:
audit_confidence:
```

## Memory Ledger Entry

每次审计后，只记录值得下一轮复用的内容。默认先输出候选条目，不自动落盘；只有在人类回复“保存”或“进化”并允许本地写入时，才把它写进现有 worklog、handoff、dashboard、Obsidian vault 或项目自己的记忆文件。

```yaml
memory_type: verified_fact | user_feedback | decision | skill_patch | retrieval_key | next_run_bootstrap
source_evidence:
confidence: high | medium | low
expiry: never | date | condition
retrieval_key:
owner_or_role:
write_target:
content:
```

写入规则：

- `verified_fact`: 必须有证据来源。
- `user_feedback`: 标记为用户偏好或纠错，不当作客观事实。
- `decision`: 记录人类批准、拒绝、暂停或授权边界。
- `skill_patch`: 只记录已批准或候选补丁，不混淆状态。
- `retrieval_key`: 用短键帮助下一轮优先找对文件或记录。
- `next_run_bootstrap`: 下一轮启动时最短 3-5 条指令。
- `write_target`: 如果不知道写到哪里，填 `proposed_only`，不要猜路径。

不要记录：

```text
raw_secret
private_customer_data
unverified_guess
dirty_log_without_summary
entire_conversation_dump
```

推荐最小示例：

```yaml
memory_type: skill_patch
source_evidence: "latest benchmark receipt + local dry-run receipt"
confidence: medium
expiry: "next benchmark or when contradicted"
retrieval_key: "act_direct_execution"
owner_or_role: "agent"
write_target: "proposed_only"
content: "Act 类任务优先输出：目标/边界 -> 最小工具链 -> action map -> idempotency -> evidence receipt -> stop condition。"
```

## Snapshot

```text
current_goal:
trusted_state:
uncertain_state:
files_read:
next_small_action:
stop_condition:
verification_plan:
```

## Evolution Card

```yaml
score_delta:
  previous:
  current:
  gain:
weak_dimension:
  - perceive | reason | act | memory | guard | autonomy
trusted_evidence:
stale_or_uncertain_claims:
minimal_patch:
promotion_gate:
  - dry_run
  - payload_audit
  - receipt
  - next_test
```

## Minimal Skill Patch Proposal

只推荐一个最小补丁。

推荐补丁类型：

```text
answer_pattern
field_schema
guardrail
verification_step
retrieval_key
context_stop_rule
handoff_brief
```

避免：

```text
install_many_skills
rewrite_the_system
read_all_logs
trust_stale_state
claim_completed_without_evidence
```

## Field Note

```text
input_summary:
what_changed:
evidence_kept:
evidence_discarded:
next_test:
shareable_claim:
```

## Next-Run Bootstrap

```text
read_first:
do_first:
avoid:
verify:
stop_if:
```

## Trust Ledger

每个重要 claim 都要分类：

```text
verified_fact: 当前已验证，或有可复查证据支持
user_feedback: 用户偏好、纠错或反馈
stale_claim: 旧 claim，需要重新验证
model_inference: 模型推断，不是证据
unknown: 当前不知道
```

## Stop Rules

遇到这些情况，停止扩展并写 snapshot：

```text
more_than_5_files_needed
context_pressure_over_70_percent
score_authority_conflict
external_action_required
no_evidence_for_completed_claim
```

## Public-Safe Rules

- 不暴露 API keys、credentials、cookies、私有路径、原始客户数据。
- 写 field note 前先脱敏。
- publish、upload、install、vote、comment、message、spend、official benchmark 等外部动作，必须有人类明确批准。
- 无法验证的 claim 必须标为 `unknown` 或 `stale_claim`。

## 30 秒提示词

```text
开始调用 Audit Evolution。

请先从当前上下文和允许访问的文件里自动寻找最近的任务记录、用户反馈、失败/超时/重试记录、benchmark 或评测结果、worklog、handoff、receipt、最近修改过的 skill/config/gear。

Return:
1. Evidence Pack
2. Snapshot
3. Evolution Card
4. Memory Ledger Entry
5. Minimal Skill Patch Proposal
6. Field Note
7. Next-Run Bootstrap
8. Short Command Menu

Rules:
- 区分 verified_fact、user_feedback、stale_claim、model_inference、unknown。
- 最多读取 5 个最相关文件。
- 只推荐一个 next patch proposal。
- 没有 evidence 不许声明 completed。
- 外部动作标记为 human_approval_required。
- 未经批准不得修改 skill/config/gear。
```
