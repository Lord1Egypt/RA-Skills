## Description:

Provides daily check-ins, streak tracking, and motivational support to help users stay consistent with learning goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinktankglobalbot](https://clawhub.ai/user/thinktankglobalbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as an accountability partner for learning goals, including daily check-ins, progress logging, streak tracking, and weekly review support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Progress notes may contain sensitive personal details because the skill stores learning goals, streaks, and check-in notes locally.

Mitigation: Avoid entering sensitive personal information in progress notes and review the local progress.json file before sharing logs or backups.

Risk: Broad accountability trigger phrases could activate the skill in conversations where progress tracking is not intended.

Mitigation: Narrow trigger phrases or invoke the skill explicitly when accidental activation would be disruptive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thinktankglobalbot/skills/accountability-buddy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell commands and local JSON progress data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store learning goals, streaks, and check-in notes locally in progress.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
