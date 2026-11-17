## Description:

Bdpan Storage helps agents manage Baidu Netdisk files, including upload, download, transfer, sharing, listing, search, move, copy, rename, folder creation, login, logout, installation, update, and uninstall workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[may-yaha](https://clawhub.ai/user/may-yaha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent operate within a Baidu Netdisk application directory for file transfer, sharing, search, organization, and account session management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download and execute native installers or updates from Baidu-hosted endpoints.

Mitigation: Use it only when the publisher and Baidu-hosted endpoints are trusted, require human approval before first install and every update, and review downloaded binaries in security-sensitive environments.

Risk: Update and uninstall flows can modify or delete local skill, binary, and configuration files.

Mitigation: Avoid unattended update or uninstall options, keep install and config directories under user-controlled paths, and confirm destructive actions before running them.

Risk: Baidu Netdisk authorization and local token storage can expose account data if used on shared or untrusted machines.

Mitigation: Do not authorize accounts on shared or untrusted hosts, protect local configuration files, and log out after use on any machine that is not fully controlled.

## Reference(s):

- [Bdpan command reference](reference/bdpan-commands.md)
- [Authentication guide](reference/authentication.md)
- [Usage examples](reference/examples.md)
- [Troubleshooting guide](reference/troubleshooting.md)
- [Development notes and safety notices](reference/notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent actions may invoke local shell scripts and the bdpan CLI; file operations are intended to stay within the Baidu Netdisk application directory.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
