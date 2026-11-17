## Description:

Sleep better tonight - personalized wind-down routine, breathing exercises, bedtime stories, and sleep hygiene tips. Daily evening push for better rest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Daily Sleep as a sleep-coaching assistant for morning wake-up checks, evening wind-down routines, breathing exercises, meditation prompts, sleep environment tips, and recurring reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling pushes creates recurring morning and evening scheduled messages through the selected third-party channel.

Mitigation: Choose the intended user ID and channel before enabling reminders, and use the documented off command when scheduled messages are no longer wanted.

## Reference(s):

- [Daily Sleep ClawHub Skill Page](https://clawhub.ai/jiajiaoy/skills/daily-sleep)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with shell command examples and scheduled-message configuration markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=18 for bundled push scripts; default reminders are morning 07:00 and evening 22:00, with telegram, feishu, slack, and discord channels documented.]

## Skill Version(s):

1.0.3 (source: server release metadata; package.json reports 1.0.2 and _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
