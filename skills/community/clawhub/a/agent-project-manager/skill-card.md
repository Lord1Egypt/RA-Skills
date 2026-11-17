## Description:

Project Manager helps agents preserve per-project context by creating and maintaining local status files, project indexes, optional checkpoints, Gantt summaries, risk reports, and conversation-summary logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krislu1221](https://clawhub.ai/user/krislu1221)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to keep AI-assisted project work recoverable across sessions by storing progress, decisions, todos, timelines, and risks in local project files. It is intended for project context management rather than application runtime execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional status synchronization and daily checks can create ongoing background monitoring and retention of conversation-derived summaries.

Mitigation: Enable synchronization only when explicitly needed, verify its expiration settings, and remove any scheduled tasks when the workflow is no longer desired.

Risk: Project status, memory, and conversation-log files may contain sensitive user or project details.

Mitigation: Avoid sharing secrets in conversations that may be summarized, and review local project and memory files before publishing or committing them.

Risk: Read-merge-write updates reduce accidental overwrite risk but do not prevent concurrent edits between read and write.

Mitigation: Review proposed file changes before accepting them and use version control or backups for important project records.

Risk: Optional full conversation archival can preserve more history than users expect.

Mitigation: Use MemPalace or conversation-log archival only when the workspace retention policy permits that level of history.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krislu1221/skills/agent-project-manager)
- [README](artifact/README.md)
- [Full Status Template](artifact/templates/STATUS-A.md)
- [Lightweight Status Template](artifact/templates/STATUS-B.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, JSON checkpoint configuration, and concise text status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local project and memory files after user confirmation; optional synchronization and logging can retain conversation-derived summaries.]

## Skill Version(s):

2.7.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
