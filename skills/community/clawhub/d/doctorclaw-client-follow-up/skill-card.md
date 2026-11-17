## Description:

Automated client follow-up that scans a client list, identifies stale leads, drafts personalized outreach, and supports weekly or on-demand review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to scan client or lead records, prioritize stale contacts, draft follow-up messages for approval, and maintain outreach digests or logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client lists and follow-up logs may contain contact details, deal values, and communication history.

Mitigation: Grant access only to required data sources and periodically review or delete local follow-up logs.

Risk: Optional email, SMS, CRM, or messaging integrations can expose client data or trigger outreach through connected channels.

Mitigation: Enable only the integrations needed for the workflow and require user approval before any outbound follow-up is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-client-follow-up)
- [DoctorClaw website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown digest with draft outreach text and optional configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft outreach is intended for user review before sending.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
