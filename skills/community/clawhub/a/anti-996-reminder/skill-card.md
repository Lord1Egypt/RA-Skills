## Description:

Schedules Chinese-language midday and bedtime wellness reminders for WeChat or QQ, with sleep check-ins, points, streak tracking, and a weekly summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devioslang](https://clawhub.ai/user/devioslang)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to set up recurring wellness prompts that encourage lunch breaks, rest, and earlier sleep. It also provides guidance for sleep check-ins, point tracking, and weekly progress summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled messages may be sent to the wrong account or WeChat recipient if the sample account, recipient, or channel values are reused.

Mitigation: Review each cron command before installation, replace the account, recipient, and channel values, and confirm how to list or remove scheduled tasks.

Risk: The points and check-in behavior may require additional OpenClaw handling beyond the included files.

Mitigation: Confirm the OpenClaw check-in flow and state updates in a controlled account before enabling recurring reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devioslang/skills/anti-996-reminder)
- [ClawHub publisher profile](https://clawhub.ai/user/devioslang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and Chinese reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cron scheduling guidance, JSON content pools, check-in state data, and recipient-configuration risk guidance.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
