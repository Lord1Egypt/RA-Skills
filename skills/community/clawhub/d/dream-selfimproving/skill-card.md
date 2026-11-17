## Description:

Dream Selfimproving helps an OpenClaw agent review conversations, distill long-term memory, generate daily reports, score skill usage, and draft new skills from capability gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain persistent agent memory, run scheduled memory distillation, review work, and generate skill-improvement drafts. It is intended for agents that manage local workspace state and produce operational reports or skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain conversation history and write long-term memory summaries that may include sensitive details.

Mitigation: Review memory directories and remove credentials, account details, or private user data before enabling scheduled runs or sharing generated reports.

Risk: The skill can edit OpenClaw cron jobs and scheduler messages.

Mitigation: Use the documented dry-run behavior first and require the explicit --confirm flag only after checking the current OpenClaw cron configuration.

Risk: The skill can generate new skill drafts and files under SharedSkills, which could introduce incorrect instructions or unsafe automation.

Mitigation: Review, test, and scan generated skill drafts before installing or invoking them.

Risk: Optional cloud synchronization may send memory-derived content to SwarmRecall when SWARMRECALL_API_KEY is configured.

Mitigation: Leave SWARMRECALL_API_KEY unset for local-only operation, or review synced memory content and service terms before configuring the key.

## Reference(s):

- [Diagnostic Checklist](references/diagnostic-checklist.md)
- [OpenClaw-Hermes Memory Sync](references/hermes-openclaw-memory-sync.md)
- [Multi-Agent Team Architecture](references/multi-agent-team-architecture.md)
- [Skill Evolution v5.0](references/skill-evolution-v50.md)
- [OpenClaw multi-agent team article](https://mp.weixin.qq.com/s/D33ScqwgpjiwI4PDN3vUaA)
- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/dream-selfimproving)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON memory files, generated SKILL.md drafts, Python scripts, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local OpenClaw memory, report, graph, registry, cron-related, and SharedSkills files when invoked with the relevant commands.]

## Skill Version(s):

5.1.0 (source: server release evidence; artifact package.json reports 4.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
