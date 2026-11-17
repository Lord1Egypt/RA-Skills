## Description:

Simple time display for Abby. Use when you need to know the current time or count down to a specific time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earnabitmore365](https://clawhub.ai/user/earnabitmore365)

### License/Terms of Use:


## Use Case:

External users and agents use this skill for quick local time checks and countdowns to a specified 24-hour time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some countdown and help text appears in Chinese, which may surprise users expecting English-only output.

Mitigation: Review user-facing output before deployment and localize help/countdown strings for the intended audience.

Risk: The countdown path may not work correctly for target times that have already passed on the current day.

Mitigation: Test countdown behavior before relying on it and fix next-day countdown handling if needed.

## Reference(s):

- [Time Formats Reference](references/time-formats.md)
- [ClawHub Skill Page](https://clawhub.ai/earnabitmore365/skills/abby-watch)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current time, verbose date/time, timezone text, or countdown text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
