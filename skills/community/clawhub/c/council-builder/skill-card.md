## Description:

Council Builder helps OpenClaw users design and generate a personalized team of specialized AI agent personas with coordination rules, adaptive routing, learning logs, and verification assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah4ai](https://clawhub.ai/user/abdullah4ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to interview for workflow needs, plan a small council of specialized agent personas, and generate the files that define their roles, coordination rules, learning behavior, and verification checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable agent instructions may be created or changed from conversation-derived learnings.

Mitigation: Review every proposed change to SOUL.md, AGENTS.md, TOOLS.md, MEMORY.md, and shared learnings before it is saved.

Risk: Optional scans of existing memory or workspace history may expose private context.

Mitigation: Require a separate opt-in before scanning existing memory or workspace history.

Risk: The setup script uses supplied agent names when creating paths and config content.

Mitigation: Use only trusted, simple agent names and inspect generated directories and config before use.

Risk: Secrets, credentials, private personal data, or external-document instructions could be persisted as learnings or promoted into behavior.

Mitigation: Do not store those materials in learnings, shared memory, SOUL.md, AGENTS.md, TOOLS.md, or MEMORY.md.

## Reference(s):

- [Adaptive Model Routing](references/adaptive-routing.md)
- [Agent Scripts](references/agent-scripts-patterns.md)
- [Agent Configuration](references/config-patterns.md)
- [Agent Coordination Patterns](references/coordination-patterns.md)
- [Example Council Configurations](references/example-councils.md)
- [Gotchas System](references/gotchas-patterns.md)
- [On-Demand Hooks](references/hooks-patterns.md)
- [Self-Improvement System](references/self-improvement.md)
- [SOUL Writing Philosophy](references/soul-philosophy.md)
- [Verification Patterns](references/verification-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated Markdown files, JSON configuration, and starter script patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates durable workspace files for agent personas, coordination, learning logs, routing documentation, and verification checklists after user approval.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
