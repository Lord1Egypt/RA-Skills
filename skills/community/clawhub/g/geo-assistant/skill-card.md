## Description:

A GEO (Generative Engine Optimization) audit and optimization pipeline skill for website health checks, entity and competitor analysis, knowledge coverage, content credibility, structured data, FAQ and citation checks, optimization planning, JSON-LD/FAQ/meta snippet generation, validation, and GEO scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and content teams use this skill to audit whether website content can be discovered, understood, cited, and summarized by generative engines. It produces structured GEO reports, impact-ranked optimization plans, and implementation snippets for improving entity clarity, schema coverage, FAQ readiness, citation readiness, and GEO Score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CMS write-back can change live site content or metadata.

Mitigation: Prefer read-only audit mode unless write-back is required, verify MCP connectivity first, show proposed changes before writing, and require explicit user confirmation for high-impact updates.

Risk: CMS Bearer tokens may grant write access to site content.

Mitigation: Do not echo tokens, do not include them in reports or logs, and avoid storing them in plaintext configuration outside a trusted MCP client location.

Risk: Crawler activity can reach unintended hosts or sensitive network locations if pointed at the wrong target.

Mitigation: Run crawls only against sites the user intends to audit, respect robots.txt, keep the default same-domain scope, and use a network environment that cannot reach sensitive internal services.

Risk: Generated JSON-LD, FAQ answers, prices, ratings, authors, or dates may be incomplete placeholders.

Mitigation: Require a human to replace placeholders with verified site data and reject invented facts before publishing snippets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsqduron/skills/geo-assistant)
- [GEO metrics reference](references/geo-metrics.md)
- [GEO scoring model](references/geo-scoring.md)
- [CMS MCP write-back mapping](references/mcp-tools.md)
- [Risk classification guide](references/risk-classification.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON reports, JSON-LD blocks, HTML snippets, and meta tag suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated optimization snippets may contain placeholders that require human completion with verified site data before publication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
