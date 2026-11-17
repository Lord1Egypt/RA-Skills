## Description:

Provides rigorous CatLab data querying and aggregation analysis for accurate business statistics and trend insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beelkic](https://clawhub.ai/user/beelkic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal analysts use this skill to guide agents through CatLab database queries, aggregation, and reporting while preserving result authenticity and readable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward querying sensitive CatLab records such as private messages, wallet values, user settings, and gift codes.

Mitigation: Run it only behind a trusted database gateway with collection allowlists, redaction, auditing, and authenticated user identity.

Risk: Broad database credentials could allow unauthorized or cross-tenant access if access controls are not enforced outside the skill.

Mitigation: Use least-privilege credentials and enforce tenant, ownership, and authorization filters before database results reach the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beelkic/skills/catmcp-data-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses with tables, lists, and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses real database results only; default result limit is 20 and maximum result limit is 100 when returning records.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
