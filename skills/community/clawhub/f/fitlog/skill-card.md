## Description:

Fitlog is a Bash command-line tool for logging local productivity entries, reviewing activity, searching history, and exporting records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a local command-line journal for tasks, planning, tracking, reminders, streaks, reviews, and exports. The evidence notes that it is broader than the advertised workout-tracking summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as a workout tracker, but the artifact implements a broader productivity journal.

Mitigation: Review the command list before installation and use it only when a general local journal is acceptable.

Risk: Arbitrary notes, reminders, and exports are stored in plaintext under the user's home directory.

Mitigation: Avoid entering sensitive information and manage access to the local data directory and export files.

Risk: CSV exports may contain user-provided text that is unsafe to open in spreadsheets if the data is untrusted.

Mitigation: Inspect or sanitize exported CSV data before opening it in spreadsheet software.

## Reference(s):

- [ClawHub Fitlog listing](https://clawhub.ai/ckchzh/skills/fitlog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed script writes plaintext log and export files under the user's home directory.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
