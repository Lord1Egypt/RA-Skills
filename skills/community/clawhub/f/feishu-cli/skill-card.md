## Description:

Feishu CLI helps agents use the feishu-cli command line tool to convert between Markdown and Feishu documents and manage Feishu docs, wikis, sheets, messages, calendars, tasks, permissions, and cloud files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niesongyang](https://clawhub.ai/user/niesongyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Feishu workspaces through CLI commands, including document import/export, wiki and sheet access, message sending, calendar and task creation, permission changes, and cloud file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing a third-party CLI through a remote shell script.

Mitigation: Install from a pinned release and verify its checksum or signature before configuring credentials.

Risk: The CLI can perform sensitive Feishu workspace actions including exports, writes, message sends, calendar and task creation, and permission changes.

Mitigation: Grant only the minimum required Feishu app scopes and require explicit user confirmation before any sensitive or write operation.

Risk: Feishu app credentials may provide broad access if configured before the CLI and scopes are reviewed.

Mitigation: Configure credentials only after reviewing the CLI source or release artifact and confirming the required app permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niesongyang/skills/feishu-cli)
- [Publisher profile](https://clawhub.ai/user/niesongyang)
- [feishu-cli release downloads](https://github.com/riba2534/feishu-cli/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Feishu workspace write actions that require credentials, app scopes, and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
