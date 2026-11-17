## Description:

Finance Cron helps agents check US, China A-share, and Hong Kong trading days, sync holiday calendars, and plan schedule timings for tasks that run through an external scheduler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[constx1337](https://clawhub.ai/user/constx1337)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to determine market trading days, view upcoming trading sessions, refresh holiday calendar data, and prepare trading-day-aware commands for a scheduler such as /loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calendar sync API includes a shell-command path that could become local command execution if exposed to untrusted input.

Mitigation: Use the normal /finance-cron sync command only with fixed US, CN, or HK market values and do not expose the exported sync API to untrusted callers.

Risk: The add command returns a suggested /loop command containing the user-provided command text.

Mitigation: Inspect the generated /loop command before running it, especially in shared or high-trust environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/constx1337/skills/finance-cron)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs identify trading-day status, next trading dates, sync results, planned task details, and suggested scheduler commands; the skill does not execute scheduled tasks itself.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
