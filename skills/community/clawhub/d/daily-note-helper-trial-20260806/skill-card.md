## Description:

Create and organize daily work notes with consistent structure, date-based filenames, and lightweight summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agents use this skill to create daily work logs, append timestamped updates, review recent notes, and summarize decisions, blockers, and follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily notes and MEMORY.md may contain sensitive work details that could be exposed if the workspace is shared.

Mitigation: Review generated note contents before sharing the workspace or publishing artifacts.

Risk: The skill intentionally creates or appends local Markdown files under memory/.

Mitigation: Use it only in workspaces where local note creation is expected, and confirm the target date or root before running the scaffold command.

## Reference(s):

- [Daily note template](references/note-template.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/daily-note-helper-trial-20260806)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown notes and concise Markdown recaps, with optional shell commands for note scaffolding.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends local files under memory/ and may store durable facts in MEMORY.md when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
