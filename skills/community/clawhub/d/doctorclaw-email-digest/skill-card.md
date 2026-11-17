## Description:

Smart email digest -- categorize unread emails by priority, draft replies for urgent ones, and run on demand or on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to triage unread email, identify urgent messages, extract action items, and prepare draft replies for review. It also supports scheduled digest setup for recurring inbox summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires read access to unread emails, which may expose sensitive inbox contents to the agent.

Mitigation: Install only when inbox read access is acceptable, use a narrow maximum email limit, and review the digest before acting on sensitive messages.

Risk: The skill can optionally deliver summaries through external channels or send approved replies.

Mitigation: Avoid external delivery channels for sensitive inboxes unless needed, and enable send access or scheduled runs only after confirming the intended approval and delivery behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-email-digest)
- [DoctorClaw Website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with prioritized email summaries, draft reply text, and optional scheduling or setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft replies are marked for review and should not be sent without user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
