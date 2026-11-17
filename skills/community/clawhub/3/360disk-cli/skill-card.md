## Description:

360disk-cli helps an agent manage 360 AI Cloud Disk files through shell commands for browsing, search, upload, download, move, rename, delete, sharing, backups, restores, and JSON-based automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsoncm](https://clawhub.ai/user/jsoncm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to manage 360 AI Cloud Disk files from scripts, CI jobs, and command-line workflows. It is intended for cloud file operations that need structured JSON output and shell pipeline integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an external npm CLI that is unpinned by default.

Mitigation: Prefer a pinned, reviewed CLI version for repeatable or sensitive workflows.

Risk: The skill handles cloud credentials for 360 AI Cloud Disk.

Mitigation: Use safer secret handling such as environment variables or stored configuration, and do not paste API keys into chat or shell commands when avoidable.

Risk: Delete, clear-dir, restore, share, and auto-backup actions can expose, overwrite, or remove local and cloud files.

Mitigation: Require explicit confirmation before running destructive, sharing, restore, or background auto-backup commands.

Risk: The README includes an HTTP ZIP download path.

Mitigation: Avoid the HTTP ZIP install path and use a reviewed distribution source.

## Reference(s):

- [360disk CLI command reference](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/jsoncm/skills/360disk-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses API keys and local/cloud filesystem paths; default execution uses an external npm CLI unless a pinned reviewed version is selected.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
