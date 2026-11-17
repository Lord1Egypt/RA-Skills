## Description:

Daily Social runs a structured 15-20 minute social media routine for indie developers and founders across Reddit, Twitter/X, LinkedIn, and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External users, indie developers, and founders use this skill to scan social media activity, identify engagement opportunities, draft daily action items, and log engagement outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access logged-in social media pages, notifications, profile metrics, and engagement context.

Mitigation: Run it only when that account context is acceptable to expose to the agent, and prefer scan-only behavior by default.

Risk: The skill may change social account state by accepting connections, posting comments, replying, or writing tracking data.

Mitigation: Require separate user confirmation before any action that posts, replies, accepts a connection, or writes tracking data.

## Reference(s):

- [Daily Social on ClawHub](https://clawhub.ai/phy041/skills/daily-social)
- [Canlah AI homepage](https://canlah.ai)
- [Publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown checklists, engagement logs, optional JSON tracking examples, and browser automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scan summaries, prioritized social tasks, engagement records, and optional weekly review summaries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
