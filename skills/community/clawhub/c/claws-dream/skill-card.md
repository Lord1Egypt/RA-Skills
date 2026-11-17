## Description:

Deprecated OpenClaw memory consolidation skill that reviews recent logs, updates long-term memory files, computes memory health, and can trigger scheduled nightly runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunateadventurer](https://clawhub.ai/user/fortunateadventurer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this retired skill to consolidate interaction logs into structured memory files, generate memory health reports, and maintain a local memory index. The release notes and security guidance recommend preferring OpenClaw's built-in Dreaming feature for current use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The retired skill can continue running on an automatic schedule and modify local OpenClaw memory files.

Mitigation: Do not enable the scheduler unless ongoing memory modification is intended; prefer OpenClaw's built-in Dreaming feature.

Risk: Memory updates, backups, and generated dashboards affect local workspace state.

Mitigation: Require user-scoped scheduling, clear file permissions, uninstall instructions, backup cleanup, and HTML escaping before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fortunateadventurer/skills/claws-dream)
- [Nightly Dream Memory Consolidation Prompt](references/dream-prompt.md)
- [First Dream Initial Memory Setup](references/first-dream-prompt.md)
- [Dream Consolidation Prompts](references/dream-prompts.md)
- [Memory Templates](references/memory-template.md)
- [Memory Taxonomy](references/memory-types.md)
- [Scoring and Health Algorithms](references/scoring.md)
- [Memory Dashboard Template](references/dashboard-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and generated local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and modify MEMORY.md and files under memory/ when run; automatic scheduling can trigger repeated background memory updates.]

## Skill Version(s):

2.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
