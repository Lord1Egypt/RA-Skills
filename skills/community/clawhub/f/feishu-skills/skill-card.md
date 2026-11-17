## Description:

Feishu (Lark) skill pack installer that installs integration skills for OpenClaw and EnClaws, including bot setup, documents, calendar, tasks, bitable, chat, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hashstacs-hk](https://clawhub.ai/user/hashstacs-hk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill pack to install Feishu integrations that let agents authenticate with per-user OAuth and work with Feishu documents, wiki pages, chat, calendars, tasks, bitable apps, drive files, OCR, users, and spreadsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pack can access and mutate broad Feishu resources through local Node command execution.

Mitigation: Review Feishu app scopes before deployment and grant only the permissions needed for the intended workflows.

Risk: Persistent app secrets and OAuth tokens may expose Feishu data if local configuration or token files are mishandled.

Mitigation: Protect local credential files, delete stale config backups, and rotate app secrets or tokens when access is no longer needed.

Risk: Document extraction may rely on parser dependencies that affect file handling behavior.

Mitigation: Preinstall or pin document parser dependencies before enabling file extraction workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hashstacs-hk/skills/feishu-skills)
- [Feishu permissions guide](artifact/feishu-quick-setup/references/feishu-permissions.md)
- [Feishu troubleshooting guide](artifact/feishu-quick-setup/references/troubleshooting.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [EnClaws](https://github.com/hashSTACS-Global/EnClaws)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs local Node.js-based Feishu skill directories and relies on Feishu OAuth credentials and permissions for runtime operations.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
