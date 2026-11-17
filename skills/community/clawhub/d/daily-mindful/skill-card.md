## Description:

Daily Mindful helps generate short mindfulness sessions with breathing guidance, meditation prompts, daily affirmations, and evening reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to create 3-5 minute bilingual mindfulness practices, including morning breathing exercises, guided reflection, affirmations, and an interactive HTML breathing page. When enabled, it can also create recurring morning and evening reminder prompts for a selected chat channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create indefinite recurring morning and evening reminder messages to external chat channels.

Mitigation: Review the selected user ID, channel, and reminder times before enabling push reminders; use the off command to remove scheduled jobs when reminders are no longer wanted.

Risk: The skill stores local per-user reminder settings.

Mitigation: Limit use to intended user IDs and review local settings when changing channels, schedules, or reminder status.

Risk: Generated pages may include an ad-ready placeholder and fixed ClawCode footer.

Mitigation: Review generated HTML before publishing or sharing it externally.

## Reference(s):

- [Daily Mindful ClawHub Skill Page](https://clawhub.ai/jiajiaoy/skills/daily-mindful)
- [Daily Mindful README](artifact/README.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, generated HTML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a single-file HTML artifact and may emit scheduler control commands when push reminders are enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
