## Description:

Self-improvement through conversation analysis that extracts learnings from corrections and success patterns and proposes persistent updates to agent definitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmyg11](https://clawhub.ai/user/mmyg11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review recent conversations, identify corrections or successful patterns, and propose approved updates to agent instructions or new skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent instructions and create new skills from conversation-derived content.

Mitigation: Inspect the exact source quote, target path, and diff before approving any proposed change; avoid approving global changes or new skill creation unless intended.

Risk: Conversation-derived learnings can encode incorrect, overbroad, or unwanted guidance if accepted without review.

Mitigation: Approve only specific, verified learnings and keep auto-reflection disabled unless continuous reflection is deliberately needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmyg11/skills/agent-reflect-temp)
- [Signal Detection Patterns](artifact/signal_patterns.md)
- [Agent Mappings Reference](artifact/agent_mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with tables, diffs, file paths, status summaries, and approval prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update reflection logs, state files, metrics, agent instructions, and new skill files after explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
