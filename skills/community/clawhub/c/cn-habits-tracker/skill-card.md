## Description:

Cn Habits Tracker helps Chinese-language users manage habit check-ins, local streaks, daily completion status, and weekly or monthly habit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals using an agent in Chinese can add habits, record daily check-ins, review what remains for the day, and generate weekly or monthly progress reports from local data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting a habit removes its stored records and the skill has no built-in undo or backup.

Mitigation: Back up ~/.qclaw/workspace/habits.json before deleting habits or before using the tracker for records that matter.

Risk: Reused habit IDs after deletions can affect local data integrity.

Mitigation: Review habit records after deletions and preserve a copy of the JSON data file before adding replacement habits.

## Reference(s):

- [Cn Habits Tracker ClawHub listing](https://clawhub.ai/freedompixels/skills/cn-habits-tracker)
- [freedompixels publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores habit definitions and records in a local JSON file at ~/.qclaw/workspace/habits.json.]

## Skill Version(s):

1.2.6 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
