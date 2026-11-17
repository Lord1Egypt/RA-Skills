## Description:

Captura erros, correções e aprendizados automaticamente. Promove melhorias para AGENTS.md, TOOLS.md e SKILL.md. Sistema de auto-melhoria em português.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users, especially Portuguese-speaking teams, use this skill to record agent errors, user corrections, learnings, and feature requests in structured Markdown notes. The skill helps turn repeated mistakes into reviewed improvements for future agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatically promoted learnings can change future agent behavior through AGENTS.md, TOOLS.md, or SKILL.md.

Mitigation: Require a human to review and approve the exact diff and destination before any promotion is applied.

Risk: Captured corrections and learnings may contain incorrect, stale, or unsafe guidance.

Mitigation: Treat captured notes as untrusted until they are validated against the current project context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engsathiago/skills/aprendizado-continuo)
- [Project homepage](https://github.com/eve-agent/aprendizado-continuo)
- [Support issues](https://github.com/eve-agent/aprendizado-continuo/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes and guidance with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose writes to .learnings/, AGENTS.md, TOOLS.md, and SKILL.md; review diffs before applying.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
