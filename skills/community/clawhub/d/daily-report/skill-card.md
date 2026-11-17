## Description:

Daily Report helps an agent generate scheduled morning, end-of-day, weekly, and immediate alert reports for lead pipeline activity, outreach metrics, costs, priorities, and issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visualdeptcreative](https://clawhub.ai/user/visualdeptcreative)

### License/Terms of Use:


## Use Case:

Operators and business-development teams use this skill to keep structured daily and weekly summaries of lead generation, outreach production, budget status, blockers, and next priorities. It also defines immediate alert conditions for replies, budget depletion, API errors, completed runs, and blocked tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and memory logs may contain operational lead, outreach, cost, or blocker details.

Mitigation: Periodically review or delete local memory logs when they contain sensitive business information.

Risk: Telegram alerts may expose business data through an external notification channel.

Mitigation: Configure Telegram only when that channel is approved for the organization's business data.

Risk: The skill defines Spain-time reporting schedules that may not match every user's operating timezone.

Mitigation: Confirm the listed Spain-time schedule before installing or activating the reporting workflow.

## Reference(s):

- [Daily Report on ClawHub](https://clawhub.ai/visualdeptcreative/skills/daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown report templates and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Spain-time report schedules, memory log format, and Telegram alert trigger guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
