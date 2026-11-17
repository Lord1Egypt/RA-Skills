## Description:

Report Claude Code token consumption and costs using ccusage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to summarize local Claude Code token consumption, API costs, spending, and daily, weekly, or monthly usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an automatically fetched third-party ccusage CLI that reads local Claude Code session data.

Mitigation: Install only when the publisher and ccusage dependency are acceptable for the environment; for stronger assurance, pin and review the ccusage version before use.

Risk: Billing-sensitive daily totals can be affected by timezone choices.

Mitigation: Verify the timezone used for reports before relying on daily or period-specific cost totals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spideystreet/skills/ccusage-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown usage summary with shell command execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include daily, weekly, or monthly totals and optional per-model breakdowns.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
