## Description:

Archives older daily memory notes into month folders to keep active memory lean and reduce prompt token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x3r081](https://clawhub.ai/user/x3r081)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to archive older daily memory files into month-based folders, reducing active memory clutter and prompt token overhead while preserving local notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The archiving script may replace an existing archived memory file with the same name.

Mitigation: Run with --dry-run first, inspect proposed moves for name collisions, and keep backups or verify archive contents before applying changes to important memory stores.

## Reference(s):

- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [ClawHub Skill Page](https://clawhub.ai/x3r081/skills/agent-memory-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON command output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script operates on local Markdown files and supports dry-run previews before moving files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
