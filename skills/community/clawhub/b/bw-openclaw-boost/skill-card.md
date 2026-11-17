## Description:

OpenClaw Boost enhances OpenClaw efficiency with cost tracking, memory management, compaction, permission control, token budgeting, slash commands, and local task coordination tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bw520333](https://clawhub.ai/user/bw520333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor local agent cost, token budget, memory relevance, compaction status, permission rules, tool execution, and task coordination from a bundled launcher and Python tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory, compaction, and consolidation features can persist information and influence future agent context.

Mitigation: Audit local memory files and compaction behavior before use, and require clear user approval before injecting memory or compressed summaries into agent context.

Risk: Permission and coordination components can affect future tool approval decisions and task routing.

Mitigation: Review configured permission rules and task logs before installing or enabling the tools in sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bw520333/skills/bw-openclaw-boost)
- [Publisher profile](https://clawhub.ai/user/bw520333)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact version metadata](artifact/version.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, Markdown reports, shell commands, and JSON configuration or log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local status reports, memory snippets, compaction summaries, permission decisions, launcher commands, and configuration records.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
