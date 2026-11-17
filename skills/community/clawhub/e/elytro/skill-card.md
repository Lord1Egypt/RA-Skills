## Description:

Elytro is an Ethereum EIP-4337 smart contract wallet skill for AI agents that supports account management, balance checks, and ETH transfer workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayden-sudo](https://clawhub.ai/user/jayden-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to connect an AI agent with Ethereum wallet operations, including account management, balance review, and ETH transfers. Review is especially important because the installed artifact redirects agents to a remote definition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled artifact is a remote redirect, so reviewed behavior can change after installation.

Mitigation: Review the skill before installing and prefer a package that vendors the full skill definition locally or pins remote content to an immutable commit with an integrity check.

Risk: The skill concerns Ethereum wallet activity, where mistaken or unauthorized actions can have financial impact.

Mitigation: Require explicit user approval for wallet operations, verify addresses and amounts, and test with low-value transactions before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayden-sudo/skills/elytro)
- [Remote skill definition referenced by artifact](https://raw.githubusercontent.com/Elytro-eth/skills/main/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to remote wallet instructions; review before use.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
