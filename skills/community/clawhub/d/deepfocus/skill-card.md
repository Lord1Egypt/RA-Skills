## Description:

Deepfocus is a local command-line productivity toolkit for recording tasks, plans, reviews, streaks, reminders, and exporting or searching productivity entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Deepfocus to log focus work, tasks, plans, reviews, streaks, reminders, and search or export those local records from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form tasks, notes, reminders, reviews, and exports can contain sensitive personal or work details stored on local disk.

Mitigation: Avoid storing secrets or sensitive work details unless local account and file permissions are appropriate; use owner-only permissions and purge unneeded logs or exports.

Risk: The release is presented partly as a Pomodoro timer, but the security summary identifies it as a local productivity logger that records and exports entries.

Mitigation: Review the available commands before installation and treat the skill as a local logging and export tool rather than a strict timer.

## Reference(s):

- [Deepfocus ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/deepfocus)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Terminal text output with local log files and JSON, CSV, or TXT exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes free-form productivity entries under ~/.local/share/deepfocus/ and can export accumulated records.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
