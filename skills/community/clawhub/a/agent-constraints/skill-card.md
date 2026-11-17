## Description:

Helps coding-agent users decide whether a constraint belongs in hooks, AGENTS.md or CLAUDE.md, a Skill, a path-scoped rule, or the current prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsonz](https://clawhub.ai/user/snowsonz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to design, review, and maintain coding-agent constraints, especially when deciding how to prevent recurring agent mistakes or reduce oversized AGENTS.md or CLAUDE.md files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional SessionEnd hook can persistently record working directories, session identifiers, end reasons, and transcript paths.

Mitigation: Use project-local installation where possible, configure a project-scoped log path, keep the log permission-restricted, and periodically delete stale entries.

Risk: Review workflows may lead an agent to inspect prior transcript paths or auto-memory feedback from unrelated work.

Mitigation: Review what the hook records and confirm before allowing an agent to read historical transcript paths or unrelated memory files.

Risk: Several enforcement mechanisms and syntax examples are Claude Code-specific and may not transfer directly to other agents.

Mitigation: Apply Claude Code hooks and permissions only in Claude Code environments, and adapt the guidance before using it with Codex, Copilot, or other agent systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snowsonz/skills/agent-constraints)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Supporting evidence](artifact/EVIDENCE.md)
- [Layer 1 enforcement guide](artifact/LAYER1-ENFORCEMENT.md)
- [Layer 2 instruction guide](artifact/LAYER2-INSTRUCTIONS.md)
- [Layer 3 on-demand guide](artifact/LAYER3-ONDEMAND.md)
- [Session review hook guide](artifact/hooks/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code blocks, configuration snippets, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and may include concrete Claude Code hook, permission, Skill, path-scoped rule, AGENTS.md, or CLAUDE.md recommendations.]

## Skill Version(s):

0.1.5 (source: server release evidence and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
