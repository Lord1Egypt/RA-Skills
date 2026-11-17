## Description:

Track reading progress, rate finished books, and manage your library. Use when logging books, reviewing reading stats, or planning reading goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Bookshelf to manage personal reading lists, plans, progress logs, reviews, tags, reminders, exports, and reading summaries from a local command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading notes, reminders, reviews, and exports are stored locally in plain text under ~/.local/share/bookshelf.

Mitigation: Avoid entering sensitive personal information and apply local file-system protections appropriate for personal reading data.

Risk: CSV exports may contain user-entered values that spreadsheet applications could interpret as formulas.

Mitigation: Review CSV exports before sharing or opening them in spreadsheet software, especially when entries were copied from untrusted sources.

## Reference(s):

- [Bookshelf on ClawHub](https://clawhub.ai/ckchzh/skills/bookshelf)
- [BytesAgain homepage](https://bytesagain.com)
- [Publisher profile](https://clawhub.ai/user/ckchzh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration, Guidance]

**Output Format:** [Plain text command output with local JSON, CSV, and TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists reading logs and exports under ~/.local/share/bookshelf.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
