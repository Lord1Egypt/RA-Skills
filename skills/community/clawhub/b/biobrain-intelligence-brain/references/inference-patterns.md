# Cross-File Inference Patterns

The brain's highest-value output is not what it finds in any single document — it's what it infers across documents.

## WISDOM_GRAPH

A living knowledge graph where:
- **Nodes** = Key findings from departmental outputs
- **Edges** = Inferred relationships (causal, correlational, contradictory)

### Node Structure

```yaml
node:
  id: "WG-20260625-001"
  title: "小红书互动率下降"
  source: "品牌部日报_20260625"
  domain: "#brand #platform"
  classification: "🟡I"
  confidence: "high"  # verified by 3+ data points
  created: "2026-06-25"
  connections:
    - to: "WG-20260625-003"
      relation: "causes"
      confidence: "medium"
    - to: "WG-20260624-007"
      relation: "contradicts"
      confidence: "low"
```

### Edge Types

| Type | Meaning | Example |
|------|---------|---------|
| causes | A directly leads to B | 平台限流 → 内容触达下降 |
| correlates | A and B move together | 发布时间 × 互动率 |
| contradicts | A and B cannot both be true | 报告A说增长 / 报告B说下降 |
| supports | A provides evidence for B | 用户反馈支持定价调整 |
| suggests | A implies B should be considered | 趋势 → 策略调整 |
| replaces | A makes B obsolete | 新平台取代旧平台 |

### Graph Maintenance

- **Add**: When new information connects to 2+ existing nodes
- **Remove**: When a node is contradicted by 3+ newer, higher-confidence nodes
- **Prune**: Monthly — remove nodes with no connections and age > 30 days

## ACTION_PIPELINE

WISDOM_GRAPH inferences that convert to executable tasks.

### Priority Framework

```
P0 — Urgent, revenue/risk impact within 7 days. Max 4 items.
P1 — Important, revenue/risk impact within 30 days. Max 4 items.
P2 — Standard, quality/efficiency improvement. Max 4 items.
P3 — Background, long-term exploration. Max 4 items.
```

The 4-item cap per tier is non-negotiable. If a P0 item enters and the tier is full, something must be promoted, demoted, or killed. This is how the brain enforces focus.

### Pipeline Entry Format

```yaml
action:
  id: "AP-20260625-001"
  title: "AIGC内容标注合规检查"
  priority: "P0"
  source_inference: "WG-20260625-005 + 法务部合规审查"
  owner: "品牌部"
  deadline: "2026-06-28"
  success_criteria: "所有发布内容增加AIGC标注"
  status: "pending"
```

## ONE_MORE_THING

The highest-value inference category. These insights connect domains that nobody thought to connect.

### Pattern Recognition

```markdown
Pattern: Platform Dependency Risk

Files involved:
  - 品牌部日报: 小红书互动率↓15%
  - 品牌部日报: 小红书账号受限(-9136)
  - 销售部日报: 知识星球转化↑22%
  - 财务部日报: 收入¥0

Inference: 免费平台既是流量源也是单点故障。单一平台依赖 = 业务风险。
          需要至少3个并行流量渠道才能保证业务连续性。

ONE_MORE_THING: 小红书受限是短期问题，但暴露了长期架构缺陷。
                不解决多平台并行，下一次平台变动还会归零。
```

### Generation Triggers

The brain should attempt ONE_MORE_THING generation when:
1. 3+ departments report related changes in the same week
2. A metric crosses a threshold (any metric moving >20% in one direction)
3. A system failure reveals a structural pattern (not just a one-off bug)
4. An external event (platform policy change, competitor move) affects 2+ departments

### Quality Gate

A ONE_MORE_THING is valid only if:
- It connects at least 2 domains that normally don't interact
- It's not obvious from reading any single document
- It has actionable implications
- It can be stated in one sentence

Bad: "AI is important for business." (Obvious, not cross-domain, not actionable)
Good: "The finance department's cost data + the brand department's engagement data together suggest we're spending premium tokens on content that free models could produce at comparable quality." (Cross-domain, non-obvious, actionable, one sentence)

## Inference Validation

Every inference must be validated within its declared timeframe:

```
P0 inferences → Validate within 7 days (did the action produce results?)
P1 inferences → Validate within 30 days
P2/P3 inferences → Validate within 90 days
```

Invalidated inferences are not failures — they're learning. Log why the inference was wrong and feed it back into the pipeline as a calibration signal.
