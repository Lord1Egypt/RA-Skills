## Description:

Native local memory for OpenClaw agents: Capture, Cue, Project, Recall, and Consolidate conversations into a private Helix-backed brain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moshik21](https://clawhub.ai/user/moshik21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Engram Memory to connect a local long-term memory service to agents, capture durable decisions, preferences, and context, and recall them across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unverified remote installer.

Mitigation: Review or pin the installer before execution, avoid sudo, and run it only in an environment where the resulting changes are acceptable.

Risk: The installer modifies OpenClaw MCP and skill configuration and creates persistent background processing.

Mitigation: Review the configuration changes, confirm how to disable the LaunchAgent or stop the server, and keep removal steps available before installation.

Risk: The local memory service stores and resurfaces conversation and project context over time.

Mitigation: Use it only for data appropriate for local long-term persistence, and confirm how stored memory data can be reviewed or deleted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moshik21/skills/engram-brain)
- [Publisher profile](https://clawhub.ai/user/moshik21)
- [Skill-declared homepage](https://github.com/Moshik21/engram)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, REST examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to use local MCP or REST memory operations and runtime checks.]

## Skill Version(s):

0.3.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
