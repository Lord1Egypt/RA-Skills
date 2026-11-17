## Description:

Uses analytics and product constraints to propose, critique, and rank two review-ready growth experiment variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT-0

## Use Case:

Growth teams, product managers, and developers use this skill to turn analytics and a product brief into two ranked, review-ready A/B test variants for landing pages, onboarding, or pricing. Live changes require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics snapshots may contain sensitive project or user data.

Mitigation: Use least-privilege analytics access and review local snapshots before sharing or committing them.

Risk: Proposed copy or an experiment may be inaccurate or change live product behavior.

Mitigation: Review claims and guardrails, and require explicit approval before changing product copy or wiring an experiment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dannyshmueli/skills/agent-analytics-autoresearch)
- [Autoresearch Growth template](https://github.com/Agent-Analytics/autoresearch-growth)
- [Agent Analytics](https://agentanalytics.sh)
- [Agent Analytics skill](https://github.com/Agent-Analytics/skills/tree/main/skills/agent-analytics)
- [Growth loop reference](references/program.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Code]

**Output Format:** [Markdown variant brief and tab-separated round results; optional implementation after approval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Two ranked variants with exact copy, rationale, risks, experiment shape, and data limitations; no live experiment by default.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
