## Description:

How agentmemory wires into host coding agents via the connect command. Use when installing agentmemory into a specific agent, when asked which agents are supported, or when a connect adapter writes the wrong config path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect agentmemory to supported host coding agents and verify that the memory server tools are available. It is useful when installing agentmemory, checking supported agents, or troubleshooting an adapter that writes the wrong config path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A floating external skill installation command may install a different version than the one reviewed.

Mitigation: Review or pin the separate rohitg00/agentmemory action-skill install before relying on the npx command.

Risk: Running connect against the wrong host agent can modify an unintended agent configuration.

Mitigation: Run connect with an explicit supported agent name and confirm the target config path before installation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/rohitg00/agentmemory/tree/main/plugin/skills/agentmemory-agents)
- [ClawHub skill listing](https://clawhub.ai/rohitg00/skills/agentmemory-agents)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
