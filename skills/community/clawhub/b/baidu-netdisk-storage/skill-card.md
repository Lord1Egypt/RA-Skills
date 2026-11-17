## Description:

Baidu Drive enables agents to manage Baidu Netdisk files, including uploads, downloads, transfers, sharing, search, move, copy, rename, and folder creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[may-yaha](https://clawhub.ai/user/may-yaha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate files in a Baidu Drive app folder, including upload, download, transfer from share links, sharing, search, and file organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and update flows can run or replace code from Baidu-hosted remote endpoints with limited independent authenticity controls.

Mitigation: Review the skill before installing, use it only when the Baidu-hosted installer and update channel are trusted, and avoid automatic install or update modes in sensitive environments.

Risk: A shell-backed agent can affect the Baidu Drive app folder, local download paths, and share-link creation.

Mitigation: Confirm upload, download, and share destinations before execution, and avoid exposing local token or configuration files.

Risk: Uninstall behavior can delete the configured bdpan data directory when BDPAN_CONFIG_DIR is customized.

Mitigation: Verify the exact configured directory before running uninstall with a custom BDPAN_CONFIG_DIR value.

## Reference(s):

- [bdpan CLI Command Reference](reference/bdpan-commands.md)
- [Authentication Guide](reference/authentication.md)
- [Examples](reference/examples.md)
- [Troubleshooting Guide](reference/troubleshooting.md)
- [Development Notes](reference/notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and occasional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute bdpan CLI operations after the skill's confirmation checks; outputs can include links, paths, status text, or JSON from bdpan.]

## Skill Version(s):

1.4.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
