## Description:

Fund Signal Monitor helps agents monitor user-selected funds for report releases, manager changes, asset-size shifts, unusual performance movement, and style drift, then produce concise alerts and follow-up analysis guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain fund watchlists, receive concise monitoring alerts, and hand off selected events for deeper fund analysis. It is intended for monitoring and informational workflows, not as standalone investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pushed fund alerts can reveal a user's investment interests.

Mitigation: Confirm the watchlist, notification channels, and removal path before enabling monitoring; route alerts only through channels the user accepts.

Risk: Users may treat monitoring alerts or suggested follow-up actions as investment advice.

Mitigation: Keep the included investment-risk disclaimer with reports and present alerts as informational signals that require independent review.

Risk: Fund data sources, schedules, and notification integrations may be stale, delayed, or unavailable in a deployment environment.

Mitigation: Verify official fund announcements and configured data sources before acting on an alert, and review monitoring frequency and watchlist settings during setup.

## Reference(s):

- [Fund Signal Monitor ClawHub page](https://clawhub.ai/lj22503/skills/fund-signal-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown alerts with optional shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes signal type, affected fund, monitoring cadence, follow-up actions, and investment-risk disclaimer guidance where applicable.]

## Skill Version(s):

1.1.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
