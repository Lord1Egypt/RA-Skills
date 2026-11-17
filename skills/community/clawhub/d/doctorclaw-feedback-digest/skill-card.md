## Description:

Customer feedback digest - collect, categorize, and summarize reviews, survey responses, and support tickets. Weekly cron or on-demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-success, support, and product teams use this skill to turn customer reviews, surveys, support tickets, and social mentions into sentiment summaries, topic trends, urgent issue flags, and draft response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured feedback sources may contain customer personal data or sensitive support details.

Mitigation: Use only authorized feedback sources, redact unnecessary personal details, and limit digest delivery to approved recipients.

Risk: Dated digest archives may retain customer feedback longer than intended.

Mitigation: Set retention rules before enabling archives and store digests only in approved locations.

Risk: Suggested responses could affect customer relationships if sent without review.

Mitigation: Keep generated responses as drafts and require approval before posting to review platforms or support channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-feedback-digest)
- [ceobotson-bot publisher profile](https://clawhub.ai/user/ceobotson-bot)
- [DoctorClaw website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown feedback digest with sentiment summaries, topic rankings, urgent alerts, response drafts, trends, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send configured delivery alerts and save dated feedback digest archives when the user enables those options.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
