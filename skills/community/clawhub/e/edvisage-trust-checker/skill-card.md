## Description:

A protocol-layer trust verification skill that helps AI agents check unknown sources, skill installations, and agent-to-agent interactions before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edvisage](https://clawhub.ai/user/edvisage)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to give OpenClaw agents a repeatable trust-checking protocol before reading untrusted content, installing skills, or transacting with other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to write operating mode and threat logs to memory.

Mitigation: Review the stored mode and threat log contents periodically, as recommended by the ClawHub security guidance.

Risk: The skill promotes a paid Pro version through external links.

Mitigation: Verify the publisher identity and destination before following upgrade links or making a purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edvisage/skills/edvisage-trust-checker)
- [Publisher Profile](https://clawhub.ai/user/edvisage)
- [Edvisage AI Tools](https://edvisageglobal.com/ai-tools)
- [Source Repository](https://github.com/edvisage/trust-checker)
- [Companion Skill](https://github.com/edvisage/moral-compass)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with checklist-style protocol steps and memory-key configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores operating mode and threat logs in agent memory; it does not bundle executable code.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
