## Description:

Date and time utility for common formatting, conversion, calendar, relative-time, and basic date arithmetic tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to request simple local date and time operations, including current time, format conversion, calendar display, countdowns, relative-time output, and basic date arithmetic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises advanced timezone conversion, precise month/year arithmetic, JSON output, and natural-language parsing beyond what the inspected implementation reliably supports.

Mitigation: Use the skill for simple local date/time helper tasks, test advanced date handling before relying on it, and validate important results against a trusted source.

Risk: Month and year arithmetic may be approximate rather than calendar-exact.

Mitigation: Avoid using month or year calculations for billing, compliance, scheduling commitments, or other precision-sensitive workflows without independent verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/datetime-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text date/time results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No network access is indicated by the inspected artifacts; some advertised advanced features are not fully supported by the implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
