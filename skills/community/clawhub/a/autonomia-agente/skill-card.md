## Description:

Helps AI agents act more proactively by maintaining local working notes, recovering context, and capturing learnings for continuous self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this Portuguese-language skill to make OpenClaw-style agents more proactive, persistent across context loss, and able to capture lessons for future interactions. It is intended for users who want local working notes and self-improvement patterns in agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to write local interaction notes under .autonomia, which can include sensitive conversation details.

Mitigation: Use it only where local note persistence is acceptable, and periodically review or delete .autonomia files.

Risk: Proactive check-ins and self-improvement behavior can produce unwanted or unexpected agent actions.

Mitigation: Review proposed behavior changes before relying on them and keep guardrails in place for agent evolution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engsathiago/skills/autonomia-agente)
- [Autonomia Agente Repository](https://github.com/eve-agent/autonomia-agente)
- [Autonomia Agente Support Issues](https://github.com/eve-agent/autonomia-agente/issues)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to keep local working notes under .autonomia.]

## Skill Version(s):

1.0.0 (source: evidence release, SKILL.md frontmatter, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
