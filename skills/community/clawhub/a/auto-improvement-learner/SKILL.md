---
name: improvement-learner
category: learning
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

- 查看一个 skill 在 6 个维度上的质量评分
- 运行自动改进循环（Pareto front 保护，不允许任何维度回退）
- 追踪 skill 评估分数的历史变化

## When NOT to Use

- **给改进候选打语义分** → use `improvement-discriminator`
- **跑全流程（生成→打分→门禁→执行）** → use `improvement-orchestrator`
- **只想改一个文件** → use `improvement-executor`

## 6 Evaluation Dimensions

| Dimension | Checks | Pure-text default |
|-----------|--------|-------------------|
| **accuracy** | 15 items: frontmatter(3), symptom-driven desc, When to Use/Not, code examples, Usage, few-shot, no vague language, min length, Related Skills, Output Artifacts, atomicity | — |
| **coverage** | SKILL.md = 60% base + scripts/references/tests/README bonuses | — |
| **reliability** | pytest pass=1.0, fail=0.5 | 1.0 (pure-text) |
| **efficiency** | Line count: ≤200=1.0, ≥1200=0.3 | — |
| **security** | No api_key/password/sk- in SKILL.md, no os.system()/exec() | — |
| **trigger_quality** | Description length, triggers field, disambiguation | — |

## Three-Layer Memory

| Layer | Capacity | Behavior |
|-------|----------|----------|
| **HOT** | ≤100 | Always loaded, frequently accessed patterns |
| **WARM** | Unlimited | Overflow from HOT, loaded on demand |
| **COLD** | Archive | >3 months inactive (future) |

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
# 评估（不改动，只看分数）
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

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Evaluate | JSON with 6-dimension scores (0.0-1.0 each) |
| Self-improve | JSON: iterations, kept/reverted/skipped, final_scores, memory stats |
| Track progress | JSON with historical scores and trend data |

## Related Skills

- **improvement-discriminator**: Semantic scoring (LLM judge); learner focuses on structural quality
- **improvement-orchestrator**: Full pipeline; learner provides standalone quality scoring used by autoloop-controller and self-improvement loop (not a stage in the orchestrator pipeline)
- **benchmark-store**: Pareto front data shared between learner and benchmark-store
