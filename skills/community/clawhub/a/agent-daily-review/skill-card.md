## Description:

Helps agents conduct structured end-of-day review, reflection, and documentation by scanning records, categorizing activities, analyzing progress, and generating Markdown review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to summarize daily work records, categorize progress and blockers, reflect on activity, and generate a Markdown daily review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read workspace memory and more entries than users expect.

Mitigation: Run it manually first with --no-memory and review what records it scans before scheduling it.

Risk: The skill writes persistent review reports and appends summaries to MEMORY.md by default.

Mitigation: Review generated reports before sharing them, and use --no-memory when persistent memory updates are not desired.

## Reference(s):

- [Agent Daily Review on ClawHub](https://clawhub.ai/openlark/skills/agent-daily-review)
- [OpenLark Publisher Profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown daily review report with command examples and optional memory summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write review files under reviews/ and append a summary to MEMORY.md unless run with --no-memory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
