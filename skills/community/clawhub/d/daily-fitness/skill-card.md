## Description:

Daily no-equipment workout - 5-15 min bodyweight routines (HIIT, yoga, core, mobility) with instructions and streak tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate short bilingual no-equipment workout routines with an interactive timer for home, office, or travel. It can also help configure daily morning and evening push reminders for workout planning, recap, and streak tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring push reminders can schedule messages to external channels and may continue until disabled.

Mitigation: Confirm the channel, recipient, morning and evening times, and Asia/Shanghai timezone before enabling; disable or remove scheduler jobs when reminders are no longer wanted.

Risk: Generated workout routines may be unsuitable for users with injuries, medical constraints, or limited mobility.

Mitigation: Review exercise choices, form tips, and easier modifications before use, and adapt or skip movements that are not appropriate.

## Reference(s):

- [Daily Fitness on ClawHub](https://clawhub.ai/jiajiaoy/skills/daily-fitness)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [HTML file with concise Markdown response and optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces /mnt/user-data/outputs/daily-fitness.html; push management can emit scheduler add/remove directives for configured external channels.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
