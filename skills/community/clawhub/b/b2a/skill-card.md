## Description:

Sell to AI agents with machine-readable products, agent-optimized APIs, structured pricing, and discovery strategies for the agentic economy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, product teams, and ecommerce operators use this skill to prepare products and services for AI agents as customers. It guides agent-discoverable catalogs, agent-optimized APIs, structured pricing, autonomous purchase flows, and measurable trust signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous purchasing examples could lead to unintended spending or orders if implemented without user controls.

Mitigation: Require explicit user authorization, spending and quantity caps, clear notifications, easy cancellation, and per-agent action limits before enabling autonomous transactions.

Risk: Agent tracking and identity examples could expose user or agent identifiers beyond their intended scope.

Mitigation: Use scoped credentials, privacy controls, audit logging, and data minimization for user and agent identifiers.

Risk: Detailed inventory or catalog APIs can expose competitive intelligence when queried in bulk.

Mitigation: Require authentication for detailed data, rate-limit bulk queries, monitor scraping patterns, and avoid exposing supplier or inventory strategy details.

## Reference(s):

- [B2A discovery guidance](discovery.md)
- [B2A infrastructure guidance](infrastructure.md)
- [B2A retail and ecommerce guidance](retail.md)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, HTTP, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable requirements are declared.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
