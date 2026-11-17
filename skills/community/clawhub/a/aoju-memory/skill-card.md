## Description:

Long-term memory, learning, and self-evolution for the agent; it maintains durable memory files, daily logs, learnings, behavioral patterns, and optional memory reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaibaoqing](https://clawhub.ai/user/chaibaoqing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an OpenClaw-style agent durable cross-session memory, searchable learning records, memory health status, and behavior-improvement review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records user and project context across sessions.

Mitigation: Require explicit approval before storing personal, confidential, or project-sensitive details, and avoid saving secrets or credentials.

Risk: Evolution reviews can influence future agent behavior by suggesting updates to SOUL.md or AGENTS.md.

Mitigation: Review proposed behavior changes manually before applying them, and keep dry-run review as the default for untrusted or newly installed deployments.

Risk: Memory reports can expose accumulated user, project, and learning records.

Mitigation: Treat generated HTML reports as sensitive local artifacts and review them before sharing or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaibaoqing/skills/aoju-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with optional JSON search results, HTML reports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local memory files under the OpenClaw workspace; generated HTML reports may contain sensitive memory content.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
