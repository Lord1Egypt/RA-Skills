## Description:

Anamnesis Hub helps OpenClaw agents set up and operate a four-tier persistent memory system with local retrieval, working-memory files, long-term archives, optional MemOS Cloud sync, and automated extraction pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorqr](https://clawhub.ai/user/victorqr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure persistent memory for OpenClaw agents, including local semantic retrieval, daily memory files, long-term memory indexes, optional cloud synchronization, and scheduled extraction pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived data may be sent to MemOS services when optional cloud synchronization or recall is enabled.

Mitigation: Review the privacy tradeoffs before enabling MemOS Cloud, avoid sensitive workspaces unless approved, and skip cloud setup when local-only memory is required.

Risk: Setup and maintenance scripts can install remote components, change OpenClaw configuration, schedule jobs, persist memories, and alter workspace files.

Mitigation: Review scripts and configuration diffs before execution, use dry-run or manual setup where available, and back up OpenClaw workspace files before installation or reset operations.

Risk: Automatically extracted memories can be stale, incorrect, or overbroad if accepted without review.

Mitigation: Manually review generated memories, candidate queues, and long-term indexes before relying on them for agent context.

Risk: Cleanup and reset workflows can remove or archive session, memory, and configuration files.

Mitigation: Keep cleanup disabled until exact target files are reviewed, and create backups before running reset, migration, or uninstall steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/victorqr/skills/anamnesis-hub)
- [Documentation Index](references/INDEX.md)
- [Architecture](references/architecture.md)
- [Setup Guide](references/setup-guide.md)
- [Memory Directory](references/memory-directory.md)
- [Pipeline Stages](references/pipeline-stages.md)
- [Scripts Reference](references/scripts-reference.md)
- [MemOS Cloud Sync API](references/sync-api.md)
- [Candidates Review](references/candidates-review.md)
- [Upgrade and Reset](references/upgrade-reset.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and references to bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide setup steps that create or update OpenClaw memory files, SQLite databases, cron jobs, local configuration, and optional MemOS Cloud synchronization.]

## Skill Version(s):

v1.13.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
