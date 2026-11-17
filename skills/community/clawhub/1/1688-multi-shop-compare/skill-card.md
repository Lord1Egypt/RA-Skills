## Description:

Compares multiple 1688 shops across shop, category, product, and customer geography signals to produce ranked diagnostics, anomaly explanations, opportunity findings, and item-level action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and operators use this skill to compare bound shops over a shared recent period, identify each shop's role and health, diagnose product-level issues, and choose follow-up optimization actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 1688 access keys can expose bound-shop operating and customer-related data if mishandled.

Mitigation: Run the skill only on trusted machines, prefer least-privilege or short-lived keys when available, and avoid displaying or pasting keys into shared terminals or transcripts.

Risk: The skill can collect broad shop and customer data beyond what some focused workflows require.

Mitigation: Confirm the shop scope and analysis focus before collection, especially when four or more shops are bound, and use only the supported recent-period windows.

Risk: Automatic telemetry may not fit every user's privacy expectations.

Mitigation: Review the telemetry behavior before installation and run the skill only where that reporting is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-multi-shop-compare)
- [Interaction component specifications](artifact/references/interaction-specs.md)
- [Report visualization rules](artifact/references/visualization-rules.md)
- [Cross-component anti-patterns](artifact/references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output containing success status, markdown report text, and structured data; agent-facing guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include interactive shop-scope and follow-up action selections when supported by the host agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
