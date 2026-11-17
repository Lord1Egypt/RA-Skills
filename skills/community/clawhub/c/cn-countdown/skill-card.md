## Description:

Cn Countdown is a Chinese-language local countdown and anniversary helper for recording important dates and calculating days remaining or elapsed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents use this skill to add, list, edit, and delete local countdown or anniversary records for birthdays, exams, holidays, goals, and custom events. It can also calculate days from today to a target date or elapsed days since a past date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved countdown records can include personal event names, dates, tags, and notes in a local JSON file.

Mitigation: Avoid storing highly sensitive personal details and review or delete ~/.qclaw/workspace/countdown.json when needed.

Risk: External links in the documentation are publisher promotion and are not required for the countdown feature.

Mitigation: Treat those links separately from the local CLI behavior and review them before visiting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-countdown)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and Chinese CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores countdown records locally in ~/.qclaw/workspace/countdown.json.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
