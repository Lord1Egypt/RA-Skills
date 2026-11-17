## Description:

Generates a daily work summary from workspace memory and optional activity sources, saves it as Markdown, and can deliver it to configured notification channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rare](https://clawhub.ai/user/rare)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Employees and agent operators use this skill to compile end-of-day work notes into a structured daily report and deliver it to configured recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read workspace notes or optional conversation logs and send summaries to external chat recipients.

Mitigation: Use a narrowly scoped configuration, trusted pre-approved recipients, and explicit opt-in for conversation-log access.

Risk: Scheduled delivery can disclose sensitive work details before review.

Mitigation: Preview or redact reports before cron delivery and require confirmation when destinations change.

## Reference(s):

- [Configuration Example](references/config.example.md)
- [Daily Report Skill on ClawHub](https://clawhub.ai/rare/skills/daily-report-skill)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, API Calls, Guidance]

**Output Format:** [Markdown report with configuration-driven notification delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated report file and may send the report through configured chat channels.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
