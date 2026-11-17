## Description:

Production-grade memory system for OpenClaw agents that organizes notes into local topic files, preserves context across compaction, and runs daily and weekly memory maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzx666888](https://clawhub.ai/user/tzx666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up local Markdown-based agent memory, split existing MEMORY.md content into topic files, and maintain session, daily, and long-term notes through compaction prompts and scheduled cleanup jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently changes OpenClaw compaction behavior and creates recurring maintenance cron jobs.

Mitigation: Review the installer before running it, back up ~/.openclaw/openclaw.json, and inspect or remove the created OpenClaw cron entries after installation.

Risk: Conversation-derived notes are stored locally and may include sensitive information if users place secrets in chats or memory files.

Mitigation: Avoid storing secrets in conversations or memory files, and review generated Markdown memory content before retaining or sharing it.

Risk: The weekly deep-clean job can trim and rewrite topic memory in ways users may not want.

Mitigation: Disable the weekly deep-clean job or keep backups unless automatic trimming and rewriting of topic memory is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tzx666888/skills/beastxa-memory-pro)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local Markdown memory files, OpenClaw compaction settings, and recurring OpenClaw cron jobs when installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
