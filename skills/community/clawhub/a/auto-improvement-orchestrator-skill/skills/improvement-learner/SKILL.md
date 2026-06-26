---
name: improvement-learner
description: "当需要检查 skill 质量评分、自动优化 SKILL.md 结构、追踪评估分数变化趋势、或「评分低了想知道哪里扣分」时使用。6维结构评估 + HOT/WARM/COLD 三层记忆 + Pareto front。不用于候选语义打分（用 improvement-discriminator）或全流程编排（用 improvement-orchestrator）。"
license: MIT
triggers:
  - evaluate skill
  - self-improve
  - skill quality check
  - 评估.*skill
  - 质量评分
  - 哪里扣分
  - 自动优化
---

# Improvement Learner

Real Karpathy self-improvement loop: evaluate → modify → re-evaluate → keep/revert → repeat.

## When to Use

- 查看一个 skill 在 9 个维度上的质量评分（accuracy/coverage/reliability/efficiency/security/trigger_quality/leakage/knowledge_density + 综合分）
- 运行自动改进循环（Pareto front 保护，不允许任何维度回退）
- 追踪 skill 评估分数的历史变化
- 诊断某个 skill 扣分原因（哪些 checklist item 未通过）
- 对比纯文本 skill 和带脚本 skill 的评分差异
- 为 autoloop-controller 提供收敛判断的分数数据
- 验证改进后分数是否真正提升（改前/改后对比）
- 使用 --mock 模式快速调试评分逻辑而不消耗 LLM tokens

## When NOT to Use

- **给改进候选打语义分** → use `improvement-discriminator`
- **跑全流程（生成→打分→门禁→执行）** → use `improvement-orchestrator`
- **只想改一个文件** → use `improvement-executor`
- **验证改进是否提升 AI 执行效果** → use `improvement-evaluator`

## Why 9 Dimensions Instead of a Single Score

**问题**: 早期版本用单一加权分（0-100）评估 skill 质量，但发现严重问题：一个 security 有漏洞的 skill 可以靠高 accuracy 和 coverage 拉高总分到 SOLID 级别。单一分数无法区分"全面优秀"和"偏科严重"。

**Tradeoff**: 9 维度增加了评估复杂度（每个维度需要独立的 checklist 和阈值），但让问题定位变得精确。当 accuracy=0.67 时，直接看哪些 checklist item 未通过就知道要加 Output Artifacts 还是 code examples。Because 维度正交设计（accuracy 管内容完整性，coverage 管文件覆盖度，security 管安全规范），同一个改进只影响 1-2 个维度，不会出现"改了 A 维度意外影响 B 维度"的耦合问题。

9 个维度中 leakage 和 knowledge_density 是后来加入的：leakage 解决内部项目路径泄露到公开 skill 的问题，knowledge_density 解决 SKILL.md 看似完整但每个 section 只有 2-3 行缺乏深度的问题。

## 9 Evaluation Dimensions

| Dimension | Checks | Pure-text default |
|-----------|--------|-------------------|
| **accuracy** | 15 items: frontmatter(3), symptom-driven desc, When to Use/Not, code examples, Usage, few-shot, no vague language, min length, Related Skills, Output Artifacts, atomicity | — |
| **coverage** | SKILL.md = 60% base + scripts/references/tests/README bonuses | — |
| **reliability** | pytest pass=1.0, fail=0.5 | 1.0 (pure-text) |
| **efficiency** | Line count: ≤200=1.0, ≥1200=0.3 | — |
| **security** | No api_key/password/sk- in SKILL.md, no os.system()/exec() | — |
| **trigger_quality** | Description length, triggers field, disambiguation | — |
| **leakage** | No internal project references (company-specific paths, internal URLs) | — |
| **knowledge_density** | Depth per section, actionable content ratio | — |

## Why LLM Judge for Accuracy Instead of Regex

**问题**: 最初 accuracy 维度完全用 regex 匹配（检查 SKILL.md 是否包含 "## When to Use"、是否有 code block 等），但 regex 的判断精度极低。一个 skill 写了 `## When to Use` 但内容是 "TBD" 也能通过 regex 检查。实测 regex 与人工评估的相关性 R²≈0.00 — 基本等于随机。

**Because** accuracy 需要判断内容的语义质量（description 是否 symptom-driven、code examples 是否与 skill 功能相关、是否有 vague language），这些都超出了 regex 的能力范围。LLM judge 对每个 checklist item 做 yes/no 判断，与人工评估的一致率约 85%。

**Tradeoff**: LLM judge 每次评估消耗约 2000-4000 tokens（约 $0.01-0.02），比 regex 的零成本高。但 --mock 模式可以跳过 LLM 调用，用确定性规则快速返回近似分数，适合调试和 CI 环境。

```python
# Regex vs LLM judge accuracy comparison (from internal benchmark)
# Regex: checks if "## When to Use" heading exists → yes/no
# LLM:   checks if content under heading is actionable, not just "TBD"
regex_score = 0.73   # passes because heading exists
llm_score   = 0.45   # fails because content is placeholder
human_score = 0.40   # agrees with LLM — heading with "TBD" is not useful
# R² correlation: regex vs human = 0.00, LLM vs human = 0.72
```

## Three-Layer Memory

| Layer | Capacity | Behavior |
|-------|----------|----------|
| **HOT** | ≤100 | Always loaded, frequently accessed patterns |
| **WARM** | Unlimited | Overflow from HOT, loaded on demand |
| **COLD** | Archive | >3 months inactive (future) |

HOT 层存储最近评估中频繁出现的失败模式（如"缺少 Output Artifacts"出现 5 次以上）。当 generator 请求改进方向时，HOT 层的高频失败模式会被优先推荐。WARM 层存储所有历史评估结果，按 skill_id 索引，用于趋势分析和回归检测。COLD 层目前未实现，规划中用于归档超过 3 个月未被访问的模式数据。

<example>
正确用法: 评估一个 skill 的质量
$ python3 scripts/self_improve.py --skill-path /path/to/skill --max-iterations 1
→ 输出 JSON:
  {"final_scores": {"accuracy": 0.83, "coverage": 1.0, "reliability": 1.0, ...}}
→ accuracy 0.83 说明 SKILL.md 缺少部分检查项（如 Output Artifacts 或 Related Skills）
</example>

<anti-example>
错误判读: 纯文本 skill 的 reliability=1.0 不代表质量好
→ 纯文本 skill 没有 scripts/，reliability 默认 1.0（没有代码就不需要测试）
→ 真正有意义的维度是 accuracy 和 trigger_quality
</anti-example>

## CLI

```bash
# 评估（不改动，只看分数）— 默认使用 LLM judge
python3 scripts/self_improve.py --skill-path /path/to/skill --max-iterations 1

# 自改进循环（5 轮）
python3 scripts/self_improve.py \
  --skill-path /path/to/skill \
  --max-iterations 5 \
  --memory-dir /path/to/memory \
  --state-root /path/to/state

# 追踪历史
python3 scripts/track_progress.py --skill-path /path/to/skill --output progress.json
```

### --mock 模式 vs 默认 LLM Judge

--mock 模式跳过所有 LLM 调用，用纯规则（regex + 结构检查）返回分数。适合快速调试评分逻辑、CI pipeline、或不想消耗 token 的场景。代价是 accuracy 维度的精度大幅下降（与人工评估相关性从 85% 降到约 30%）。

```bash
# --mock 模式：零 LLM 调用，纯规则评分，~1 秒完成
python3 scripts/self_improve.py --skill-path /path/to/skill --max-iterations 1 --mock
# → {"final_scores": {"accuracy": 0.73, ...}, "mode": "mock", "llm_calls": 0}

# 默认模式：LLM judge 评估 accuracy，~10 秒完成，消耗约 3000 tokens
python3 scripts/self_improve.py --skill-path /path/to/skill --max-iterations 1
# → {"final_scores": {"accuracy": 0.83, ...}, "mode": "llm", "llm_calls": 1}
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Evaluate | JSON with 9-dimension scores (0.0-1.0 each) |
| Self-improve | JSON: iterations, kept/reverted/skipped, final_scores, memory stats |
| Track progress | JSON with historical scores and trend data |
| Mock evaluate | Same format as Evaluate but with mode: "mock" and llm_calls: 0 |

Evaluate 输出还包含每个维度的详细 checklist 结果（哪些 item 通过、哪些未通过），方便定位具体扣分原因。Self-improve 输出包含每轮迭代的 diff（改了什么）、scores_before/scores_after（改前/改后分数）、decision（kept/reverted/skipped）。

## Related Skills

- **improvement-discriminator**: Semantic scoring (LLM judge); learner focuses on structural quality
- **improvement-orchestrator**: Full pipeline; learner provides standalone quality scoring used by autoloop-controller and self-improvement loop (not a stage in the orchestrator pipeline)
- **benchmark-store**: Pareto front data shared between learner and benchmark-store
- **improvement-evaluator**: Task-based execution evaluation; learner focuses on document structure quality
- **autoloop-controller**: Consumes learner scores to detect convergence plateau
