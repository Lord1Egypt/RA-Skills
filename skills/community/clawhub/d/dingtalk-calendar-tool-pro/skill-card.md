## Description:

DingTalk Calendar Pro helps agents manage enterprise DingTalk calendars, including bulk event operations, organization-based availability checks, meeting room recommendations, recurring meeting management, and schedule analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, enterprise teams, and automation developers use this skill to configure an agent for DingTalk calendar tasks such as creating events, querying availability, managing rooms, and running batch calendar workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad file and command authority.

Mitigation: Limit command execution to reviewed mcporter DingTalk calendar commands and run the skill with the minimum file access needed for calendar workflows.

Risk: The skill can automate creating, updating, canceling, or bulk-inviting attendees to calendar events.

Mitigation: Require user confirmation before calendar mutations, attendee changes, cancellations, and large batch operations.

Risk: Webhook destinations and shared credentials can expose calendar or organization data if misconfigured.

Mitigation: Use trusted webhook endpoints, controlled credential stores, and access controls before enabling team or webhook configurations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/dingtalk-calendar-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON result structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mcporter calendar commands, configuration steps, and structured execution logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
