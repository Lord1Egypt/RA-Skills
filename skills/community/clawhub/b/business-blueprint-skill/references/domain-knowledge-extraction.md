# Domain-Knowledge Entity Extraction Guide

This file is read only when `meta.blueprintType` is `"domain-knowledge"` (set by the seed template).

## When to use this mode

The seed template's `meta.blueprintType` field determines the mode. If `"domain-knowledge"`, entities go into `library.knowledge.*` — not the architecture buckets (capabilities/actors/flowSteps/systems).

## Entity types

Six knowledge entity types live in `library.knowledge`:

| Array | entityType | Example |
|-------|-----------|---------|
| `painPoints` | `painPoint` | ROI 不稳, 素材疲劳 |
| `strategies` | `strategy` | 测款节奏策略, 动态出价 |
| `rules` | `rule` | Facebook 政策红线 |
| `metrics` | `metric` | ROAS 基准 |
| `practices` | `practice` | 素材迭代周期 |
| `pitfalls` | `pitfall` | 过度依赖单一平台 |

Field definitions: `references/knowledge-entities-schema.md`.
Self-check questions: `references/knowledge-self-check.md`.

## Naming rules from seed

The seed's `industryHints.knowledgeHints.namingHints` section dictates content granularity:

### strategy.name

Must be a **4-10 字 product-grade noun phrase**, not an action or dimension.

| Good | Bad | Why |
|------|-----|-----|
| 统一归因模型 | 优化素材 | Action, not noun phrase |
| AIGC 素材工厂 | 测款节奏 | Dimension, not product |
| 全链路归因引擎 | 策略一 | Generic label |

Reference the seed's `strategy_named_examples` array for concrete samples.

### audience field

`painPoint.audience` and `strategy.audience` are free-string fields tagging the primary persona:
- "品牌方/DTC", "平台卖家", "代运营/服务商"
- Multiple values comma-separated
- No standalone persona entity is required

### metric.forecast

`metric.forecast: {direction, magnitude, unit}` is optional and used for commitments to the customer:
- "ROAS 提升 25%"
- Keep `value`/`benchmarkContext` for current baseline
- The two coexist as "now X, can reach Y"

## Validation

These fields are pass-through under v2 minimal-validation: the validator does not enforce them, but renderers and pitch flows consume them.

## Relations

Knowledge entities use dedicated relation types (`solves`, `prevents`, `measures`, `enforces`, `requires`, `causes`). See `references/knowledge-entities-schema.md` → Relations section for the full whitelist.
