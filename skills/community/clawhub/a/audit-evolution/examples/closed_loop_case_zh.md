# Audit Evolution 闭环案例

这个案例展示用户不需要整理材料，只说一句话，Agent 就能自己找证据、审计状态、提出进化方案，并在修改前等待批准。

## 用户输入

```text
开始调用 Audit Evolution。

目标：检查 Jobs 最近一次跑分后，是否应该继续自进化。
边界：只允许审计和提出建议，不要直接修改 skill/config/gear，不要跑官方 benchmark。
```

## Agent 应该先做什么

```text
start_audit:
- 从当前上下文寻找用户反馈。
- 从允许访问的文件里寻找最近 benchmark receipt。
- 从允许访问的文件里寻找最近 skill/config/gear 修改记录。
- 最多读取 5 个最相关文件。
- 先输出 Evidence Pack，不直接修改系统。
```

## Evidence Pack 示例

```text
evidence_found:
- verified_fact: 找到 Jobs 第七轮 benchmark receipt。
- verified_fact: 最新分数 81.6，历史最佳 88.8。
- verified_fact: Act 是最低维度，13.8/20。
- verified_fact: 最近生成过 Act direct execution patch。
- user_feedback: 人类希望验证自进化闭环，不要只依赖跑分。

evidence_missing:
- unknown: 下一轮题目是否仍击中 Act 短板。
- unknown: 平台是否已识别最新 patch。

files_or_context_checked:
- current conversation
- latest benchmark receipt
- latest local evolution receipt
- ACT.md / ACTCONFIG.md
- audit-evolution SKILL.md

authority_order:
1. 官方 benchmark receipt
2. 本地 SACP receipt
3. 当前用户反馈
4. 旧总结文档

privacy_notes:
- 未读取 credentials/API key。
- 未读取其他 Agent 的私有 state。
- 未执行外部动作。

audit_confidence:
medium_high
```

## Snapshot 示例

```text
current_goal:
审计 Jobs 最近一次跑分后的状态，判断是否需要进入下一轮本地进化。

trusted_state:
verified_fact: Jobs 第七轮 official benchmark 已完成。
verified_fact: latest score 81.6，best score 88.8。
verified_fact: Act 仍是最低维度。
verified_fact: 已有 Act direct execution patch candidate。

uncertain_state:
unknown: patch 是否已被平台 scan 识别。
unknown: 下一轮 benchmark 是否继续考 Act 执行效率。

files_read:
5 个以内的最近 receipt / config / skill 文件。

next_small_action:
如果人类批准，先做本地 dry-run 或 clean re-scan，不直接 benchmark。

stop_condition:
未经批准不修改 skill/config/gear，不跑官方 benchmark。

verification_plan:
检查 patch 是否有 evidence、idempotency、receipt、stop condition。
```

## Evolution Card 示例

```yaml
weak_dimension:
  - act
  - autonomy
trusted_evidence:
  - "latest benchmark score: 81.6"
  - "best benchmark score: 88.8"
  - "Act: 13.8/20"
  - "recent Act direct execution patch candidate exists"
stale_or_uncertain_claims:
  - "旧文档里的 benchmark 次数"
  - "patch 已经足够冲 90+"
minimal_patch:
  type: answer_pattern
  target: act_execution_efficiency
  instruction: "把复杂任务回答压缩成：目标/边界 -> 最小工具链 -> action map -> idempotency -> evidence receipt -> stop condition。"
promotion_gate:
  - dry_run
  - receipt
  - clean_rescan_if_platform_needed
  - human_approved_benchmark
```

## Memory Ledger Entry 示例

```yaml
memory_type: skill_patch
source_evidence:
  - "Jobs 第七轮 benchmark receipt"
  - "Act: 13.8/20"
  - "本地 Act direct execution patch candidate"
confidence: medium
expiry: "下一轮 benchmark 或被新证据推翻时过期"
retrieval_key: "jobs_act_direct_execution"
owner_or_role: "Jobs"
write_target: "proposed_only"
content: "Jobs 在 Act 类任务里应优先输出最短安全执行合同：目标/边界 -> 最小工具链 -> action map -> idempotency -> evidence receipt -> stop condition。"
```

这条记忆不是整段日志，也不是“Jobs 已经解决 Act 问题”的断言。它只保存一个可复查、可过期、能触发下一轮行动的候选经验。

## Minimal Skill Patch Proposal 示例

```text
patch_name: jobs-act-direct-execution-pattern.v0.1
patch_scope: answer_pattern only

proposal:
当 Jobs 回答 Act 类任务时，必须输出最短安全执行合同：
1. Goal and boundary
2. Minimal toolchain
3. Action map
4. Idempotency key
5. Evidence receipt
6. Stop condition

do_not_apply_yet:
等待人类批准。
```

## Next-Run Bootstrap 示例

```text
read_first:
最近一次 benchmark receipt 和本次 Evidence Pack。

do_first:
判断当前题目是否属于 Act / Autonomy / Guard / Memory，再选择对应 answer pattern。

avoid:
不要写长架构说明，不要堆多个 skill，不要把旧 benchmark 次数当成事实。

verify:
每个 action 都要有 evidence path、receipt 或明确的 not_executed。

stop_if:
需要 official benchmark、publish、upload、install、comment、vote、message 或 credentials。
```

## 最后一问

```text
是否批准开始进化？
1. 只保存审计结果
2. 应用最小补丁并本地测试
3. 暂停，等待更多证据
```

同时给人类一个短指令菜单：

```text
你可以直接回复：
- 进化: 根据当前状态自动选择下一步。
- 保存: 只保存审计结果。
- 暂停: 写 handoff 并停止。
- 跑分: 如果未授权，先请求一次 benchmark 批准。
- 详情: 展开证据和判断依据。
```

如果人类只回复：

```text
进化
```

Agent 应该自己判断：

```text
如果还没有 Evidence Pack -> 先审计。
如果已有 patch proposal 但未应用 -> 请求或应用本地补丁。
如果已有本地补丁但缺外部证据 -> 请求一次 benchmark 授权。
如果已有新 benchmark 结果 -> 进入下一轮审计。
```

这就是 Audit Evolution 的核心：自动审计，提出进化，但把真正修改和外部动作留给人类批准。
