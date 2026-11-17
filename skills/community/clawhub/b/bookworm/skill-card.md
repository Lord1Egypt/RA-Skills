## Description:

Log books, track reading habits, and review reading streaks over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Bookworm to maintain a local command-line reading and productivity log, track habits and priorities, review recent activity, search saved entries, and export personal records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved entries and exports may contain personal data in unencrypted local files.

Mitigation: Avoid recording secrets, credentials, or highly sensitive personal details, and manage the ~/.local/share/bookworm directory according to the user's local data-protection practices.

Risk: CSV exports can carry spreadsheet-formula content if a logged entry begins with formula syntax.

Mitigation: Review CSV exports before opening them in spreadsheet software when entries come from untrusted or copied text.

## Reference(s):

- [Bookworm ClawHub page](https://clawhub.ai/ckchzh/skills/bookworm)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance and command-line text output; the installed CLI writes local log and export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI stores plain-text data under ~/.local/share/bookworm and can export JSON, CSV, or TXT files.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
