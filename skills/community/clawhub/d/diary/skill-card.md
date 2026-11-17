## Description:

Diary is a local plaintext productivity logging toolkit for recording work notes, plans, progress, reminders, priorities, reviews, timelines, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to keep searchable local productivity logs and export journal-style activity records for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public diary description may overstate mood, photo, and monthly-summary behavior compared with the observed local productivity-log behavior.

Mitigation: Review the skill description before installation and align user-facing documentation with the actual logging commands.

Risk: Entries and exports are stored locally as plaintext and may contain sensitive personal or work information.

Mitigation: Avoid storing secrets, regulated data, or highly private content; protect, review, and delete exported JSON, CSV, and TXT files as sensitive records.

Risk: JSON and CSV exports may not safely encode arbitrary entry content.

Mitigation: Validate and fix export escaping before relying on exported files for automation, sharing, or archival workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/diary)
- [Publisher Profile](https://clawhub.ai/user/bytesagain1)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text command output with local JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores plaintext logs and exports under ~/.local/share/diary.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
