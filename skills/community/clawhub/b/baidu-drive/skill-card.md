## Description:

Manages Baidu Drive files for upload, download, transfer, sharing, search, movement, copying, renaming, folder creation, and supported agent memory backup or restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidunetdiskaibot](https://clawhub.ai/user/baidunetdiskaibot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate files in a Baidu Drive account from an agent session. Supported Claw users can also use it to back up, list, and restore agent memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to a Baidu Drive account.

Mitigation: Install only when that account access is acceptable, review login prompts carefully, avoid untrusted environments, and log out when access is no longer needed.

Risk: Install, update, uninstall, and memory-restore paths have review-worthy risks around network-supplied code and persistent agent files.

Mitigation: Review install and update prompts, avoid unattended update or uninstall flows, and inspect restored memory backups before relying on them.

Risk: Restored memory backups and generated share links may expose sensitive information.

Mitigation: Treat memory archives and share links as sensitive, confirm destructive or overwrite operations, and choose limited link durations unless a permanent link is explicitly needed.

## Reference(s):

- [Authentication Guide](reference/authentication.md)
- [bdpan CLI Command Reference](reference/bdpan-commands.md)
- [Usage Examples](reference/examples.md)
- [Development Notes and Safety Notices](reference/notes.md)
- [Troubleshooting Guide](reference/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proposed file operations, authentication steps, share links, and memory backup or restore commands.]

## Skill Version(s):

1.6.0 (source: server release metadata and artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
