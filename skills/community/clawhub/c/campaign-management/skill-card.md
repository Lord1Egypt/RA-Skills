## Description:

Reads campaign packages, manages campaign state, and generates intelligence reports as the entry point for campaign operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nadavnaveh](https://clawhub.ai/user/nadavnaveh)

### License/Terms of Use:

MIT-0

## Use Case:

Campaign operators and go-to-market teams use this skill to validate campaign packages, track campaign progress, generate lead intelligence reports, and manage outreach or autonomous campaign workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outreach or autonomous modes could send email, LinkedIn messages, or social posts without sufficient review.

Mitigation: Require manual approval before any message or post is sent, and confirm the sending account or domain before enabling outreach.

Risk: Lead enrichment and campaign reports can involve personal contact data.

Mitigation: Define consent, privacy, retention, and deletion rules for lead files, enriched contact data, intelligence notes, and logs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nadavnaveh/skills/campaign-management)
- [ClawHub publisher profile](https://clawhub.ai/user/nadavnaveh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with example YAML, JSON, CSV, and report structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated campaign files including enriched leads, intelligence notes, outbox drafts, state tracking, logs, and reports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
