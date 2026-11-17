## Description:

Provides JSON date and time utilities for current Asia/Shanghai time, Unix timestamp conversion, relative dates, date formatting, workday checks, ISO week calculations, and date differences without external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to obtain current time and perform date calculations for logs, reports, deadlines, timestamps, relative dates, workday checks, and week ranges. It is most appropriate when Asia/Shanghai date boundaries and Chinese output labels are expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Date calculations use Asia/Shanghai (UTC+8) boundaries and Chinese output labels, which can be wrong for local dates, deadlines, logs, or policy-sensitive timing in other locales.

Mitigation: Verify the required timezone before relying on results, or use a configurable timezone utility for the target locale.

Risk: Workday checks treat Monday through Friday as workdays and do not account for holidays or organization-specific calendars.

Mitigation: Confirm business-calendar requirements separately before using workday results for scheduling, payroll, compliance, or operational commitments.

Risk: Current-time answers depend on the host system clock.

Mitigation: Run the utility in an environment with a synchronized and trusted system clock when precise timing matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidongkl/skills/date-utils)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Asia/Shanghai (UTC+8), Chinese labels, and Python standard-library datetime calculations.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
