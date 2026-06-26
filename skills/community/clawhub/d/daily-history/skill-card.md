## Description: <br>
Today in history: 3-5 major events on this date with context and lasting impact, delivered as a bilingual English/Chinese timeline card with daily morning push support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Daily History to generate shareable bilingual history timeline cards for the current date, including context and lasting impact. Developers or operators can optionally enable scheduled morning and evening push prompts across supported messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional push scheduling can send twice-daily notifications after a user enables it. <br>
Mitigation: Confirm the userId, channel, timezone, and morning/evening times before enabling push, and use the documented off command to remove scheduled jobs. <br>
Risk: Broad history-related trigger keywords may activate the skill from generic history requests in some agent routers. <br>
Mitigation: Require explicit invocation or narrow trigger routing when automatic skill activation is enabled. <br>
Risk: Generated historical summaries may omit context or include inaccuracies from retrieved sources. <br>
Mitigation: Review the selected events and supporting sources before publishing or sharing the timeline. <br>


## Reference(s): <br>
- [Daily History on ClawHub](https://clawhub.ai/jiajiaoy/daily-history) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Shell commands, Configuration] <br>
**Output Format:** [Single-file HTML artifact with bilingual timeline content, plus shell command output for optional push scheduling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The main artifact is saved as /mnt/user-data/outputs/daily-history.html; optional push scripts emit OpenClaw cron add/remove directives.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
