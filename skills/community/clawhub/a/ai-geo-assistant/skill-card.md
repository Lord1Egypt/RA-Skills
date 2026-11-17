## Description:

AI建站GEO优化助手 audits websites for generative engine optimization, scores GEO readiness, and produces prioritized recommendations plus JSON-LD, FAQ, meta, and validation outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and GEO practitioners use this skill to audit website content for AI discoverability, entity clarity, structured data, FAQ coverage, citations, and trust signals. It can generate optimization plans, code snippets, shell commands, JSON reports, and validation guidance for read-only audits or reviewed CMS updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CMS credentials and write-back permissions may expose or modify live site content.

Mitigation: Use read-only audits when possible; for write-back, use a short-lived least-privilege token and require preview or diff review before publishing.

Risk: Persistent plaintext token storage can increase credential exposure.

Mitigation: Avoid persistent plaintext mcp.json storage where possible and keep credentials out of reports, logs, screenshots, and generated artifacts.

Risk: Direct JSON-RPC bypass paths can skip safer tool-mediated checks.

Mitigation: Do not use direct JSON-RPC bypass paths; use the documented MCP workflow with connectivity checks and explicit user confirmation.

Risk: Generated schema, FAQ, or metadata can mislead users or search systems if placeholder or unverified facts are published.

Mitigation: Review all generated snippets and replace placeholders with real source data before deployment.

## Reference(s):

- [GEO metrics reference](references/geo-metrics.md)
- [GEO scoring model](references/geo-scoring.md)
- [Risk classification and confirmation guidance](references/risk-classification.md)
- [CMS MCP write-back mapping](references/mcp-tools.md)
- [ClawHub skill page](https://clawhub.ai/hsqduron/skills/ai-geo-assistant)
- [Publisher profile](https://clawhub.ai/user/hsqduron)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON reports, JSON-LD and HTML snippets, and validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audits can run without CMS credentials; CMS write-back requires user-provided endpoint and token plus preview or diff review.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
