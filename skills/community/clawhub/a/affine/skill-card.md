## Description:

Command-line tool for managing AFFiNE documents, tags, folders, collections, files, databases, comments, journals, and workspaces on cloud or self-hosted deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodcoal](https://clawhub.ai/user/woodcoal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to ask an agent for affine-cli commands and configuration guidance for managing AFFiNE workspaces. It supports cloud and self-hosted workflows for documents, folders, tags, collections, files, databases, comments, and journals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or run an unpinned npm CLI that receives access to an AFFiNE workspace.

Mitigation: Use a pinned, reviewed affine-cli package version and install only from a trusted npm source.

Risk: AFFiNE API tokens may be exposed through shell history, local files, or repository commits.

Mitigation: Prefer environment variables or restricted-permission config files, avoid placing tokens directly in commands, and keep credential files out of repositories.

Risk: Generated commands may delete, permanently clean, bulk update, or publish AFFiNE workspace content.

Mitigation: Require explicit user confirmation before destructive, bulk mutation, cleanup, publish, or unpublish actions.

## Reference(s):

- [AFFiNE Skill on ClawHub](https://clawhub.ai/woodcoal/skills/affine)
- [Basic Commands](artifact/commands/basics.md)
- [Tags and Folders](artifact/commands/tags-folders.md)
- [Collections](artifact/commands/collections.md)
- [File Attachments](artifact/commands/files.md)
- [Databases](artifact/commands/databases.md)
- [Comments](artifact/commands/comments.md)
- [Journals](artifact/commands/journals.md)
- [AFFiNE Documentation](https://deepwiki.com/toeverything/AFFiNE)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AFFiNE API token handling, workspace identifiers, and commands that mutate, publish, or delete workspace content.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
