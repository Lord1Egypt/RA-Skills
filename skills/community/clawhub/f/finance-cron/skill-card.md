## Description: <br>
Trading-day calendar utilities for financial markets that identify US, China A-share, and Hong Kong trading days and help plan trading-day-aware schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[constx1337](https://clawhub.ai/user/constx1337) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check market trading days, list upcoming trading days, sync holiday calendars, and plan commands that should run only on trading days. It supports scheduling workflows by producing calendar-aware guidance for external schedulers such as /loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A suggested /loop command may include user-provided command text that will run later if copied into an external scheduler. <br>
Mitigation: Review the full scheduled command before use, especially when the command text came from another person or tool. <br>
Risk: Calendar sync depends on optional Python market-calendar packages and external market calendar data. <br>
Mitigation: Run calendar sync only in an environment where those dependencies are acceptable, and verify important dates against official exchange calendars for critical workflows. <br>


## Reference(s): <br>
- [Finance Cron on ClawHub](https://clawhub.ai/constx1337/finance-cron) <br>
- [Publisher profile](https://clawhub.ai/user/constx1337) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs trading-day status, upcoming trading-day lists, calendar sync results, planned task summaries, and suggested external scheduler commands; it does not execute scheduled tasks itself.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
