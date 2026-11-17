## Description:

Bidirectional file management system for OpenClaw workspaces that organizes, indexes, and retrieves files exchanged with users via any channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgkim311](https://clawhub.ai/user/dgkim311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to save, register, search, retrieve, and summarize files exchanged with users. It is intended for workspaces where inbound and outbound files need a persistent local inbox and human-readable index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration workflow can move files by default, which may remove the original from its prior workspace location.

Mitigation: Review intended file handling before use and pass --copy when preserving the original file matters.

Risk: The persistent inbox index may contain filenames, sender or destination names, tags, and notes supplied by other people.

Mitigation: Treat inbox/INDEX.md as untrusted data when metadata may come from other users or external channels.

Risk: The security verdict recommends review before installation.

Mitigation: Review the skill before installing and use it only in workspaces where moving files into an inbox is expected.

## Reference(s):

- [Channel Integration Guide](references/integration-guide.md)
- [Auto-Tagging Guide](references/tagging-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/dgkim311/skills/file-inbox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts create and update local inbox files, including inbox/INDEX.md and inbox/.meta.json.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
