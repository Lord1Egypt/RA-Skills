## Description:

AgentDrive CLI helps agents manage 360 AI cloud-drive files through shell commands for browsing, searching, uploading, downloading, moving, deleting, sharing, configuration edits, backup, restore, and JSON-oriented automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsoncm](https://clawhub.ai/user/jsoncm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and automation maintainers use this skill to convert cloud-drive management requests into AgentDrive CLI commands and cross-platform shell pipelines. It is intended for file operations, authentication checks, JSON parsing with jq, and backup or restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run mutable remote CLI code and perform cloud-drive changes, including delete, clear-dir, overwrite, restore, and auto-backup enable operations.

Mitigation: Use a pinned, reviewed AgentDrive CLI version where reproducibility matters, and require explicit user confirmation before destructive or persistent operations.

Risk: Authentication commands may expose cloud-drive API keys if long-lived secrets are pasted directly into shell commands or logs.

Mitigation: Prefer short-lived or environment-scoped credentials, avoid pasting long-lived API keys into commands, and review shell history and logs for accidental secret exposure.

Risk: The README includes an HTTP ZIP download path that does not provide transport security.

Mitigation: Avoid the HTTP ZIP path and install only from a trusted, reviewed source or package version.

## Reference(s):

- [AgentDrive CLI command reference](artifact/references/commands.md)
- [ClawHub skill page](https://clawhub.ai/jsoncm/skills/agentdrive-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown, Code]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents toward structured JSON CLI output and jq-compatible pipelines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
