## Description:

Structured personal memory system that helps agents record daily events, consolidate long-term context, and recall relevant user preferences, decisions, and project history across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyucheneureka](https://clawhub.ai/user/xuyucheneureka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent structured cross-session memory for noteworthy events, user preferences, decisions, project context, and recall before future responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-session memory can capture sensitive, inferred, or unwanted personal context.

Mitigation: Define what may be stored before use, require confirmation for sensitive or inferred facts, and keep secrets and regulated data out of memory.

Risk: Stale or incorrect memories may be reused in future responses.

Mitigation: Review MEMORY.md and daily notes regularly, delete stale or unwanted entries, and avoid fabricating memories when recall is weak.

Risk: Helper scripts scan local memory directories and may surface personal context in reports.

Mitigation: Run scripts only against the intended memory directory and review generated reports before sharing them.

## Reference(s):

- [Autobiographical Memory ClawHub Release](https://clawhub.ai/xuyucheneureka/skills/autobiographical-memory)
- [Consolidation Reference](artifact/references/consolidation.md)
- [Recall Patterns Reference](artifact/references/recall-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline commands and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-capture, consolidation, recall, and review guidance for agent-maintained MEMORY.md and daily note files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
