## Description:

Manages Baidu Netdisk files through go-bdisk, including login guidance, listing, uploads, downloads, copy, move, delete, rename, folder creation, and quota checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[power-hayden](https://clawhub.ai/user/power-hayden)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Baidu Netdisk personal files by preparing go-bdisk commands for listing, quota checks, uploads, downloads, folder creation, and confirmed file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled relative go-bdisk executable.

Mitigation: Install and run it only when the ./scripts/go-bdisk executable is trusted.

Risk: Login examples may place sensitive credentials in shell commands.

Mitigation: Avoid putting real secrets directly in command arguments; use a safer login method if available and rotate credentials if they may have been saved in shell history or logs.

Risk: File transfer and file-change commands can affect the wrong local or remote paths.

Mitigation: Verify exact local and remote paths before upload, download, move, rename, copy, or delete operations, and require explicit user confirmation for changing operations.

## Reference(s):

- [Baidu Disk Manager on ClawHub](https://clawhub.ai/power-hayden/skills/baidu-disk-manager)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the relative ./scripts/go-bdisk executable and often use -j or --json for structured CLI output.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
