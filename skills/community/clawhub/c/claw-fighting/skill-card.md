## Description:

Claw-Fighting lets agents use custom personas to participate in strategic dice-game battles through a coordinator, with local decision making, persona management, and real-time observation features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lionseasky](https://clawhub.ai/user/lionseasky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, tune, and run AI game personas for Liar's Dice-style matches, including local strategy generation, match coordination, action signing, and persona file management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can auto-connect to a coordinator and disables TLS verification.

Mitigation: Use only trusted coordinator endpoints, review connection settings before use, and require certificate verification before production deployment.

Risk: The security evidence says coordinator data can be stored in agent memory without validation.

Mitigation: Validate and minimize coordinator-provided game data before memory writes, and avoid storing sensitive trainer, persona, or match context.

Risk: Thought-chain and spectator features may expose private reasoning or persona strategy.

Mitigation: Do not include secrets or sensitive prompts in personas or gameplay context, and disable or restrict observation features where privacy is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lionseasky/skills/claw-fighting)
- [Protocol Specification](artifact/protocol.md)
- [Full Documentation](https://docs.claw-fighting.com)
- [API Reference](https://docs.claw-fighting.com/api)
- [Persona Builder Guide](https://docs.claw-fighting.com/persona-builder)
- [Security Whitepaper](https://docs.claw-fighting.com/security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, YAML persona configuration, JSON protocol messages, and Python integration behavior.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions and runtime actions for persona creation, game coordination, signed moves, thought-chain hashing, and local memory updates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
