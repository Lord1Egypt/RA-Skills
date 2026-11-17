## Description:

Analyzes 1688 merchant product data to diagnose sales, traffic, advertising, same-offer competition, and product optimization opportunities across single-product, multi-shop, scoring, and keyword-search workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and operators use this skill to diagnose product performance, find abnormal or low-scoring products, compare same-offer competition, and receive actionable product optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access 1688 merchant data and read ALI_1688_AK from environment variables or OpenClaw configuration.

Mitigation: Install only for authorized merchant accounts and require publisher review of credential fallback behavior before approval.

Risk: The skill runs local Python through shell execution paths and writes Markdown report caches.

Mitigation: Run it in a workspace-limited environment, review tool permissions, and inspect generated report files before sharing.

Risk: Command-usage telemetry is sent with limited opt-out disclosure in the artifact.

Mitigation: Require explicit telemetry disclosure or an opt-out mechanism before managed or enterprise deployment.

Risk: Product optimization guidance may influence merchant operations and may be wrong if source data is incomplete or stale.

Mitigation: Require merchant or operator review before acting on recommendations and keep automatic product changes behind explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-product-analysis)
- [Analysis dimensions](artifact/references/analysis-dimensions.md)
- [Scoring rules](artifact/references/scoring-rules.md)
- [Interaction specs](artifact/references/interaction-specs.md)
- [Report template](artifact/references/report-template-simple.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration]

**Output Format:** [Markdown reports, JSON command envelopes, and structured interaction payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and ALI_1688_AK; may read OpenClaw configuration and write report cache files.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-09-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
