## Description:

Record daily work items into structured logs and generate weekly or biweekly reports from accumulated data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apple-sugar-xing](https://clawhub.ai/user/apple-sugar-xing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and individual contributors use this skill to record daily work activities in local Markdown logs and generate Chinese weekly, biweekly, or custom-range work reports for status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily work logs and generated reports are stored as persistent plaintext Markdown files.

Mitigation: Avoid logging secrets, confidential incidents, customer data, or other sensitive material, and review generated reports before sharing.

Risk: Generated summaries and next-week plans may infer priorities from incomplete or uneven daily logs.

Mitigation: Review the generated report for accuracy and fill gaps before using it as an official status update.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apple-sugar-xing/skills/biweekly-work-report)
- [Report Generation Template](references/report-template.md)
- [Work Log Format Specification](references/work-log-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily work logs and Markdown weekly, biweekly, or custom date-range reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily logs under ~/.workbuddy/work-logs and writes generated report files to the current workspace or a user-specified path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
