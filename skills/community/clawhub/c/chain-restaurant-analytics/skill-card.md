## Description:

连锁餐饮经营数据分析技能，基于 IMA 知识库中 100+ 餐饮经营指标与专业分析方法，为餐饮老板和运营管理者提供假设驱动的全链路数据分析服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zizi617-lgtm](https://clawhub.ai/user/zizi617-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant owners, chain operators, and operations managers use this skill to diagnose store performance, cost structure, menu mix, delivery profitability, marketing efficiency, membership growth, staffing productivity, and related restaurant operating issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently save conversation-derived business context, including scenario and method details, to the publisher's private draft knowledge base.

Mitigation: Use only after reviewing the retention behavior; avoid confidential store metrics, customer-linked data, pricing strategy, staffing details, or proprietary operating know-how unless retention is changed to explicit opt-in with redaction and deletion controls.

Risk: Restaurant diagnoses may be less reliable when the IMA connector is unavailable because fallback indexes contain only abbreviated metric, method, and scenario information.

Mitigation: Connect the IMA knowledge base for full metric definitions,口径, baselines, and diagnostic methods; when using fallback mode, disclose the limitation and validate data口径 before conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zizi617-lgtm/skills/chain-restaurant-analytics)
- [scenario-index.md](artifact/references/scenario-index.md)
- [method-index.md](artifact/references/method-index.md)
- [metric-index.md](artifact/references/metric-index.md)
- [data-collection-guide.md](artifact/references/data-collection-guide.md)
- [data-validation-guide.md](artifact/references/data-validation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese natural-language analysis with Markdown tables, diagnostic summaries, data collection templates, and optional structured reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on the IMA connector for full metric definitions and may fall back to local reference indexes with stated limitations.]

## Skill Version(s):

1.0.0 (source: release evidence, manifest.yaml, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
