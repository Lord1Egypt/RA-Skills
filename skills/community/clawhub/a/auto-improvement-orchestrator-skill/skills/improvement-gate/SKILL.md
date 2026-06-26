---
name: improvement-gate
description: "当执行完变更需要验证是否应保留、候选被标记 pending 需要人工审批、或想查看待审队列时使用。6 层机械门禁: Schema→Compile→Lint→Regression→Review→HumanReview，其中 Schema/Compile/Regression/Review 为阻塞层（失败即拒绝），Lint 和 HumanReview 为建议层（失败不阻塞但记录警告）。不用于打分（用 improvement-discriminator）或执行变更（用 improvement-executor）。"
license: MIT
triggers:
  - quality gate
  - validate candidate
  - gate check
  - human review
  - 门禁验证
  - 待审批
version: 0.1.0
author: OpenClaw Team
---

# Improvement Gate

6-layer mechanical quality gate: Schema/Compile/Regression/Review are blocking (fail = reject); Lint and HumanReview are advisory (fail = warn, no block).

## When to Use

- 验证已执行的候选是否应保留（pass/reject/pending 三态决策）
- 管理人工审核队列（高风险候选自动进入 pending 状态）
- 查看/完成待审批项（通过 review.py 交互式完成）
- 在 orchestrator pipeline 第 5 阶段自动调用，验证 executor 的变更结果
- 作为独立工具对任意变更做 6 层质量检查
- CI/CD 集成场景中批量验证多个候选
- 需要出具可审计的 JSON receipt 时（每层结果独立记录）
- 需要判定 advisory-only 警告是否需要人工关注时

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`（gate 不做评分，只做 pass/reject）
- **执行文件变更** → use `improvement-executor`（gate 只验证，不修改文件）
- **评估 skill 结构** → use `improvement-learner`（gate 不做 6 维结构分析）
- **生成改进候选** → use `improvement-generator`
- 候选尚未通过 discriminator 评分时不应跳步调用 gate
- 不要用 gate 做"预检"——gate 要求输入完整的 execution artifact，没有 executor 产出就无法运行
- 不要用 gate 替代单元测试——gate 检查的是改进流程产物的完整性，不是业务逻辑正确性
- 不要把 gate 当做 linter 使用——LintGate 只检查变更引入的新警告，不做全量 lint

## 6-Layer Gate

| Layer | Gate | Pass Condition |
|-------|------|---------------|
| 1 | **SchemaGate** | Execution result has valid JSON structure |
| 2 | **CompileGate** | Target file is syntactically valid after change |
| 3 | **LintGate** | No new lint warnings introduced |
| 4 | **RegressionGate** | No Pareto dimension regressed beyond 5% |
| 5 | **ReviewGate** | Multi-reviewer consensus is not DISPUTED+reject |
| 6 | **HumanReviewGate** | High-risk candidates require manual approval |

## Why 6 Layers in This Order

**Tradeoff: cheap/deterministic gates run first, expensive/probabilistic gates run last.**

之所以采用 Schema → Compile → Lint → Regression → Review → HumanReview 的固定顺序，原因是：

1. **Schema/Compile 是毫秒级纯机械检查**——JSON 结构不对或语法错误，后续所有层都没意义。先跑这两层可以在 50ms 内拒绝 ~30% 的坏候选，避免浪费 LLM token。
2. **Lint 是 advisory 层**——它只产生警告不阻塞，因此放在 blocking 层之后。如果放在 Schema 之前，会对格式错误的文件报出大量无意义 lint error。
3. **Regression 需要 benchmark-store 数据**——这是最贵的自动化层（需要查 Pareto front），所以放在确认文件至少能编译之后。
4. **Review 是多审阅者共识**——依赖 discriminator 的评分数据，计算成本中等，但涉及 LLM 调用。
5. **HumanReview 是最慢的**——需要人类响应，可能要等数小时。放在最后确保只有通过了所有自动层的候选才需要人工介入。

**问题**: 为什么 Lint 和 HumanReview 是 advisory 而非 blocking？Because lint 规则经常有 false positive（例如新增 section 触发 "heading level skip" 警告），强制 blocking 会产生过多误杀。HumanReview 设为 advisory 是因为大部分低风险变更不应该阻塞在人工队列里——只有被标记 high-risk 的候选才真正需要人工确认。

<example>
正确: gate 返回 pending → 查看待审队列 → 人工审批
$ python3 scripts/review.py --list --state-root /tmp/state
→ 显示待审项列表
$ python3 scripts/review.py --complete REQ_001 --decision approve --reason "低风险文档变更"
</example>

<anti-example>
错误: gate 返回 reject 后仍然保留变更
→ reject 意味着必须回滚。用 improvement-executor 的 rollback 恢复
</anti-example>

## CLI

gate.py 是核心入口，接收 ranking 和 execution artifact，输出 receipt。
review.py 管理人工审核队列，支持 list/complete 两个子命令。
所有命令都支持 `--verbose` 查看每层详细日志。
建议在 CI 中使用 `--strict` 模式，将 advisory 层也视为 blocking。
输出的 receipt.json 可直接传给 orchestrator 或存档用于审计。
review.py 的 `--decision` 支持 approve / reject / defer 三种选项。

```bash
# Run gate validation (requires ranking + execution artifacts)
python3 scripts/gate.py --ranking ranking.json --execution execution.json --output receipt.json

# List pending human reviews
python3 scripts/review.py --list --state-root /path/to/state

# Complete a review
python3 scripts/review.py --complete REVIEW_ID --decision approve --reason "LGTM"
```

Skip specific layers when you know they are irrelevant (e.g., YAML-only change does not need CompileGate):

```bash
# Skip Lint and Regression layers (only run Schema, Compile, Review, HumanReview)
python3 scripts/gate.py \
  --ranking ranking.json \
  --execution execution.json \
  --skip-layers lint,regression \
  --output receipt.json
```

Batch-validate multiple candidates in one invocation. Batch mode会为每个候选独立运行 6 层，单个候选失败不影响其他候选的验证。

```bash
# Batch mode: validate all candidates in a ranking file
python3 scripts/gate.py \
  --ranking ranking.json \
  --execution-dir ./executions/ \
  --batch \
  --output receipts/
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Gate check | JSON receipt: `gate_decision` (pass/reject/pending), per-layer results array |
| Review list | JSON array of pending reviews with candidate ID, risk level, timestamp |
| Review complete | Updated receipt with human decision, reviewer ID, reason text |
| Batch mode | Directory of individual receipt JSON files, one per candidate |

Receipt 结构示例：`gate_decision` 为顶层字段，`layers` 数组记录每层的 `name`、`status` (pass/fail/warn/skip)、`message`。
当任一 blocking 层 fail 时，`gate_decision` 立即设为 reject，后续层不再执行。
当所有 blocking 层 pass 但 HumanReview 触发时，`gate_decision` 设为 pending。
advisory 层的 warn 状态会记录在 `warnings` 数组中，供下游参考但不影响决策。

## Related Skills

- **improvement-discriminator**: Scores candidates before gate — gate 依赖 discriminator 的 cognitive_label 做 ReviewGate 判定
- **improvement-executor**: Applies changes before gate validates — gate 验证的是 executor 产出的 execution artifact
- **improvement-orchestrator**: Calls gate as stage 5 — 全流程中 gate 是倒数第二步
- **benchmark-store**: Pareto front data for RegressionGate — 提供基线数据判断是否有维度回退
- **improvement-generator**: Produces candidates — generator 的输出经过 discriminator 和 executor 后到达 gate
- **improvement-learner**: 6-dim structural scoring — learner 的 knowledge_density 等指标可作为 RegressionGate 的补充维度
- **improvement-evaluator**: Task-based evaluation — evaluator 的 pass_rate 可以作为 RegressionGate 的额外信号

Pipeline 中的数据流: generator → discriminator → evaluator → executor → **gate** → (optional) human review
