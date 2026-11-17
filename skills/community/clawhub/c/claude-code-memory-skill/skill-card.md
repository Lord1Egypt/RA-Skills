## Description:

Helps agents set up, maintain, and review a Claude Code style layered memory workflow with instruction memory, session memory, durable memory, and promotion of stable learnings into instruction files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indulgeback](https://clawhub.ai/user/indulgeback)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and maintain a repo-local memory workflow for coding agents, including durable rules, active session summaries, reusable context files, and memory cleanup reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory can accidentally retain secrets, regulated personal data, sensitive user attributes, or stale context.

Mitigation: Review `.agent-memory/` and instruction-file changes before accepting them, avoid saving sensitive data, and verify durable memories against the current repository before relying on them.

## Reference(s):

- [Layered Memory Architecture](references/architecture.md)
- [Host Tool Mapping](references/host-tool-mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/indulgeback/skills/claude-code-memory-skill)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with file layout examples and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, network payloads, hidden persistence, or credential handling are identified in the server security evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
