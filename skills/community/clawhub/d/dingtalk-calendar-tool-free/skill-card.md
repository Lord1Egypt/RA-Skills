## Description:

Uses the mcporter CLI to manage DingTalk calendar events, including creating events, checking availability, and booking meeting rooms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individual users and lightweight business workflows use this skill to create, query, update, and delete DingTalk calendar events, check attendee availability, search contacts, and find or reserve meeting rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routing text includes database, SQL, and data-analysis triggers that do not accurately describe the DingTalk calendar workflow.

Mitigation: Use the skill only for DingTalk calendar, room, free/busy, and contact workflows, and disregard the unrelated trigger language.

Risk: Calendar updates, deletions, and room bookings can change user or team schedules.

Mitigation: Require explicit user confirmation before event updates, deletions, or meeting-room bookings.

Risk: The skill depends on mcporter and DingTalk endpoint configuration that may involve sensitive service URLs or credentials.

Mitigation: Review the mcporter package and endpoint configuration before use, and avoid storing secrets in plaintext config where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dingtalk-calendar-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON, text, or CSV command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke mcporter CLI calls for DingTalk calendar and contact operations.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter shows 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
