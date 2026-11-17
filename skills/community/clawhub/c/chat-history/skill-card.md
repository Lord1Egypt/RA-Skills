## Description:

Archives and searches local OpenClaw chat histories using manual commands, keyword triggers, and scheduled archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyfenwick1982](https://clawhub.ai/user/tonyfenwick1982)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to retain, search, and manage their own local conversation history across channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retains searchable local copies of sensitive conversation history.

Mitigation: Install it only when local retention is intended, review the archive location, and remove archives that should not persist.

Risk: Scheduled archive tasks may continue collecting conversations after initial setup.

Mitigation: Prefer explicit manual archiving unless automation is needed, and review or remove cron/OpenClaw cron tasks you do not want.

Risk: The release includes conflicting or under-scoped implementation paths.

Mitigation: Review the selected execution path before use and avoid the legacy main.py path unless it is fixed or removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonyfenwick1982/skills/chat-history)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Security utility assessment](artifact/SECURITY-UTILITY-ASSESSMENT.md)
- [Security notice](artifact/SECURITY-NOTICE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local archive files and scheduled archive tasks when enabled.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
