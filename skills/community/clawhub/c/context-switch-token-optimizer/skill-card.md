## Description:

Analyzes conversation topic continuity to manage context switches, compress drifting context, load relevant memory, and monitor token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicochow](https://clawhub.ai/user/nicochow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage long, multi-topic conversations by preserving relevant context, compressing weakly related history, and monitoring token budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation summaries and snippets can be retained locally in memory/context_switch_state.json.

Mitigation: Use the skill only in workspaces approved for local retention and avoid processing secrets or sensitive personal data through it.

Risk: The reset command may report that context was cleared while saved state remains on disk.

Mitigation: Verify or remove memory/context_switch_state.json when a true reset or deletion of retained summaries is required.

Risk: Matching files under memory/topic can be loaded into context.

Mitigation: Keep sensitive files out of memory/topic unless they are intended to be surfaced to the agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicochow/skills/context-switch-token-optimizer)
- [README Usage Guide](artifact/README.md)
- [Topic and Continuity Logic](artifact/docs/TOPIC_AND_CONTINUITY.md)
- [Security Review Source](evidence.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-style CLI output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local context state and load matching local memory files when used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
