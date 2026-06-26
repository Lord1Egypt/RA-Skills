---
name: benchmark-store
description: "当需要初始化基准数据库、对比 skill 评分与历史基线、查看 Pareto front 是否有维度回退、或查阅质量分级标准时使用。不用于给候选打分（用 improvement-discriminator）或自动改进（用 improvement-learner）。"
license: MIT
triggers:
  - benchmark data
  - frozen tests
  - pareto front
  - evaluation standards
  - 基准数据
  - 质量分级
version: 0.1.0
author: OpenClaw Team
---

# Benchmark Store

Frozen benchmarks, hidden tests, Pareto front, and evaluation standards.

## When to Use

- 初始化或查询基准数据库
- 对比 skill 评分与冻结基线
- 检查 Pareto front（任何维度回退 >5% 即拒绝）
- 查阅质量分级标准（POWERFUL/SOLID/GENERIC/WEAK）
- 添加新的冻结测试用例到基准库
- 查看某个 skill 在所有维度上的历史最优分数
- 为 improvement-gate 的 RegressionGate 提供 Pareto 基线数据
- 在批量评估场景下列出所有已注册的 benchmark 条目

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`
- **自动改进** → use `improvement-learner`
- **全流程** → use `improvement-orchestrator`
- **执行变更** → use `improvement-executor`
- **门禁决策** → use `improvement-gate`（它消费 benchmark-store 的数据）

## Quality Tiers

| Tier | Score | Ship? |
|------|-------|-------|
| POWERFUL ⭐ | ≥ 85% | Marketplace ready |
| SOLID | 70–84% | GitHub |
| GENERIC | 55–69% | Needs iteration |
| WEAK | < 55% | Reject or rewrite |

分级基于所有维度的加权综合分。每个维度在 evaluation-standards.md 中有独立权重。accuracy 和 coverage 权重最高（各 0.2），security 权重 0.15，其余维度各 0.1-0.15。分级用于 improvement-orchestrator 决定是否继续迭代：POWERFUL 即停止，WEAK 必须重试。

## Why Pareto Front Instead of Weighted Average

**Tradeoff**: 用加权平均分来判断回退看似简单（一个数字对比），但它会隐藏维度间的此消彼长。例如 accuracy 从 0.9 降到 0.6 而 coverage 从 0.5 升到 0.8，加权平均可能持平甚至上升，但 accuracy 的大幅回退被掩盖了。Because Pareto front 逐维度检查，任何单一维度回退超过 5% 阈值都会触发拒绝，确保改进是真正的帕累托改进（没有维度变差）而非以牺牲某个维度为代价的伪改进。

这个设计的代价是改进更难被接受（通过率约 40-50%），但避免了"越改越偏"的漂移问题。在 autoloop 场景下，Pareto 保护是防止 LLM 在多轮迭代中逐步丢失已有优势的关键机制。

## Pareto Front

```python
ParetoFront.check_regression(new_scores) → {"regressed": bool, "regressions": [...]}
# 5% tolerance — minor fluctuations allowed
```

Pareto 回退检查的完整流程：加载历史最优分 → 逐维度对比 → 超过 5% 阈值的维度标记为 regression → 任何一个 regression 即判定整体 regressed=True。

```python
# Pareto regression check — full example
from lib.pareto import ParetoFront

pf = ParetoFront("state/pareto.json")
new_scores = {"accuracy": 0.82, "coverage": 0.90, "reliability": 1.0,
              "efficiency": 0.95, "security": 1.0, "trigger_quality": 0.75}
result = pf.check_regression(new_scores)
# result = {"regressed": True,
#           "regressions": [{"dim": "accuracy", "before": 0.90, "after": 0.82, "delta": -0.08}]}
# accuracy dropped 8% (> 5% threshold) → regression detected → candidate rejected
```

<example>
正确: 检查 Pareto front 是否有回退
$ python3 -c "from lib.pareto import ParetoFront; pf = ParetoFront('state/pareto.json'); print(pf.check_regression({'accuracy': 0.9, 'coverage': 0.8}))"
→ {"regressed": false, "regressions": []}  # 无回退，可以接受
</example>

<anti-example>
错误: 用 benchmark-store 给候选打分
→ benchmark-store 只存数据，打分用 improvement-discriminator
</anti-example>

## CLI

```bash
# List benchmarks
python3 scripts/benchmark_db.py --action list --db-path benchmarks.db

# Compare skill against baselines
python3 scripts/benchmark_db.py --action compare --skill-path /path/to/skill --category general --db-path benchmarks.db

# Add a benchmark
python3 scripts/benchmark_db.py --action add --category general --test-name "test1" --db-path benchmarks.db
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Init | SQLite database with schema |
| Compare | JSON comparison with per-dimension delta |
| Pareto check | JSON with regressed flag and details |
| List | All registered benchmarks with metadata |
| Add | Confirmation of new benchmark insertion |

Compare 输出包含每个维度的 before/after/delta 三元组，以及整体的 tier_before/tier_after 分级变化。当从 SOLID 升级到 POWERFUL 或从 GENERIC 降级到 WEAK 时会额外标注 tier_changed: true。

## Related Skills

- **improvement-learner**: Imports ParetoFront for self-improvement loop
- **improvement-gate**: RegressionGate uses Pareto data to block regressions
- **improvement-discriminator**: References evaluation standards for scoring context
- **improvement-orchestrator**: Full pipeline queries benchmark-store at gate stage
- **autoloop-controller**: Uses historical benchmark data to detect convergence plateau

## Data Files

- `data/evaluation-standards.md` — Quality tiers, dimensions, weights (v2.0.0)
- `data/fixtures/` — Frozen test fixtures
- `state/pareto.json` — Per-skill Pareto front historical best scores
- `benchmarks.db` — SQLite database storing all benchmark entries and results
