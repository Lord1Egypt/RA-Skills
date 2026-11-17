## Description:

Generates 1688 shop daily operations reports for specified past dates, combining sales, traffic, buyer, advertising, and review signals with anomaly alerts and action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and their agents use this skill to review daily shop performance, compare bound shops, identify anomalies, and choose near-term operating actions. It supports single-shop and multi-shop reporting for operational sales, traffic, customer, advertising, and product review data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access-key material or bound-shop operational data may be exposed to the agent or user-facing output.

Mitigation: Sanitize bind-list and configuration flows so AK fields are never printed or passed to the agent, and limit visible output to shop names and reporting metrics.

Risk: Supplemental query capability can access broader shop data than a daily report requires.

Mitigation: Restrict supplemental data sources and API paths to an allowlist aligned with daily reporting use cases.

Risk: Full report exports can write operational data to caller-provided file paths.

Mitigation: Confine exports to a dedicated reports directory with appropriate access controls and retention rules.

Risk: Recurring daily-report setup may create repeated data access if it is not clearly controlled.

Mitigation: Make any recurring schedule explicit, documented, and reversible before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-shop-daily-report)
- [Capabilities reference](artifact/references/capabilities.md)
- [Interaction specifications](artifact/references/interaction-specs.md)
- [Wiki routing rules](artifact/references/wiki-routing-rules.md)
- [Factory profile reference](artifact/references/profiles/factory.md)
- [Trader profile reference](artifact/references/profiles/trader.md)
- [Integrated profile reference](artifact/references/profiles/integrated.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports with structured JSON command results and optional JSON report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are merchant-facing Chinese reports; report data is based on past dates because daily data is described as T+1.]

## Skill Version(s):

0.43.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
