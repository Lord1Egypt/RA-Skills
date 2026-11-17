## Description:

Scans an OpenClaw environment for leaked secrets, including API keys, tokens, credentials in .env files, installed skills, and shell history, with silent startup checks and on-demand deep scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukiraman](https://clawhub.ai/user/sukiraman)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Canary to find exposed local credentials, understand the practical risk, and receive guided or permissioned remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local credential scanning can expose sensitive credential locations beyond the user's immediate intent.

Mitigation: Run deep scans only with explicit user intent, narrow scan paths where possible, and use exclusions for unrelated sensitive locations.

Risk: Pasted shell-history or file-content output can expose raw secrets in a hosted chat.

Mitigation: Redact secrets locally before pasting output, use prefix-only previews, and rotate any credential that was pasted into chat.

Risk: Auto-fix and backup workflows may modify or copy files that contain secrets.

Mitigation: Show the proposed change before execution, re-check file state immediately before applying fixes, and keep backups protected with owner-only access and short retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sukiraman/skills/canary)
- [README](artifact/README.md)
- [Claude Project setup guide](artifact/claude-project/project-instructions.md)
- [Claude Project system prompt](artifact/claude-project/system-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with concise scan reports and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secrets should be redacted or shown only as prefix-only previews; fixes require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
