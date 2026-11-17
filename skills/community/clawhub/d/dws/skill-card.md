## Description:

Helps an agent manage DingTalk product workflows through the dws CLI, including AI tables, AI search, calendar, contacts, chats and bots, tasks, approvals, attendance, reports, DING messages, documents, drive files, meeting minutes, mail, spreadsheets, and knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyredm](https://clawhub.ai/user/flyredm)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to choose safe dws CLI workflows for DingTalk operations such as reading business records, creating meetings, sending messages, managing documents, and handling approvals. It is intended for environments where the dws CLI, account, and DingTalk tenant permissions are trusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private communications and sensitive business records through broad DingTalk workflows.

Mitigation: Install it only in trusted DingTalk tenant environments and use a least-privileged DingTalk account.

Risk: Some workflows can change, share, delete, approve, or upload business data.

Mitigation: Require explicit user confirmation before approvals, attendance changes, deletes, permission grants, messages, and file uploads.

Risk: Cross-source speaker matching or private chat analysis can expose sensitive personal or business context.

Mitigation: Use those workflows only when the affected data sources have been explicitly approved.

Risk: Runtime dependency installation can introduce uncontrolled package risk.

Mitigation: Preinstall dependencies in a controlled environment instead of allowing runtime pip installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyredm/skills/dws)
- [Publisher profile](https://clawhub.ai/user/flyredm)
- [Global reference](references/global-reference.md)
- [Intent guide](references/intent-guide.md)
- [Capability limits](references/capability-limits.md)
- [Recovery guide](references/recovery-guide.md)
- [URL patterns](references/url-patterns.md)
- [Error codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to use dws CLI commands with --format json, dry-run previews, scripts for supported multi-step workflows, and explicit confirmation for high-impact actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
