## Description:

Daily Reflect provides morning intention-setting and evening review prompts for building a consistent journaling habit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate daily journaling prompts, morning intention-setting questions, and evening reflection check-ins in Chinese or English. It can also manage recurring push schedules for supported channels when users explicitly enable them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring morning and evening push messages can be created for external channels and cross-session delivery.

Mitigation: Confirm the user ID, channel, schedule, timezone, and disable or audit process before enabling push.

Risk: Per-user push settings are stored locally with limited top-level disclosure.

Mitigation: Review stored user settings and avoid enabling recurring push for users who only want one-off writing prompts.

## Reference(s):

- [Daily Reflect on ClawHub](https://clawhub.ai/jiajiaoy/skills/daily-reflect)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Bilingual prompt text and markdown guidance, with Node.js shell commands for push scheduling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recurring push setup can emit scheduler add or remove directives for supported channels.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
