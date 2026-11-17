## Description:

APEX STACK bundles the APEX cognitive framework, MEMORIA persistent memory, and ARCHITECT goal execution engine into a Claude Code skill for reasoning, persistent context, and autonomous task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT

## Use Case:

Developers using Claude Code can add this skill to project, global, or per-session context to shape agent reasoning, memory handling, and goal-oriented execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project-level or global installation can change Claude Code behavior and memory across future sessions.

Mitigation: Prefer per-session or project-level installation, review the full skill text before appending it, and add clear begin/end markers when installing.

Risk: Project or global memory files can shape future agent behavior and may expose sensitive context if credentials are saved there.

Mitigation: Inspect .claude/memoria.md and ~/.claude/memoria.md content, and keep API keys, passwords, tokens, and other credentials out of memory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contrario/skills/apex-stack-claude-code)
- [Publisher profile: contrario](https://clawhub.ai/user/contrario)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and structured agent behavior guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Activates only when copied into CLAUDE.md or supplied as session context; no background process runs.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
