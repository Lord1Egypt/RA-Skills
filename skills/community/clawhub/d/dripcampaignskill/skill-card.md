## Description:

Agent-safe workflows for time-based nurture streams, branching logic, lead scoring hooks, and conversion analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, lifecycle, revenue, and operations teams use this agent skill to plan, review, implement, audit, or improve time-based email nurture workflows. It helps agents produce drip maps, nurture briefs, branch logic tables, scoring hooks, drop-off diagnoses, and conversion-focused rewrite plans with approval gates for live-system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations could affect real customer email workflows if applied directly.

Mitigation: Use human review before sends, imports, suppression changes, DNS or authentication updates, and production automation edits.

Risk: Incomplete audience, consent, suppression, or performance data could lead to poor campaign guidance.

Mitigation: Confirm source material and available platform fields before changing branches, scoring hooks, handoffs, or exit rules.

## Reference(s):

- [Operating Checklist](references/operating-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/polnikale/skills/dripcampaignskill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates analysis from live-system actions and requires explicit approval before customer-impacting email changes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
