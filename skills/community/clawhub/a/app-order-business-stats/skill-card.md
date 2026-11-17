## Description:

Calculates Jiushi Sports APP order metrics by time range and business segment, including users, orders, payment amount, refund amount, and net sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaggerliu](https://clawhub.ai/user/jaggerliu)

### License/Terms of Use:


## Use Case:

Authorized operations or business users use this skill to retrieve daily aggregated APP order sales and refund statistics by business segment for a confirmed time range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to query a live APP order database using an environment-backed password.

Mitigation: Install only for authorized users and prefer a brokered, allowlisted reporting tool over direct mysql access.

Risk: Generated reports expose aggregated payment, refund, and sales metrics.

Mitigation: Limit use to users approved to view these business metrics and review reports before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaggerliu/skills/app-order-business-stats)
- [Publisher profile](https://clawhub.ai/user/jaggerliu)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Markdown, Guidance]

**Output Format:** [Markdown with SQL and shell command snippets plus a Markdown results table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily aggregate results by business segment; hourly breakdowns are out of scope.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
