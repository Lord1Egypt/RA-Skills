## Description:

OpenCode+OMO orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded available agents for search, reading, research, testing, review, and mutually exclusive writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-how](https://clawhub.ai/user/its-how)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route non-trivial OpenCode tasks through OMO capability discovery, bounded delegation, verification, and final integration while preserving confirmation and secret-handling boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upgrade instructions rely on mutable remote sources.

Mitigation: Review repository contents before installing or upgrading, and prefer a pinned commit or signed release instead of fetching the latest version blindly.

Risk: Delegation and worktree orchestration can expand task scope or expose sensitive session context if applied carelessly.

Mitigation: Keep confirmation gates and secret-handling boundaries in the primary session, assign bounded work sets, and treat delegated output as advisory evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/its-how/skills/aha-opencode-omo)
- [Aha orchestration repository](https://github.com/its-How/aha-orch)
- [Capability orchestration reference](references/capability-orchestration.md)
- [OpenCode](https://github.com/sst/opencode)
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and structured delegation criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing orchestration decisions, checks, and handoff guidance rather than executable payloads.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
