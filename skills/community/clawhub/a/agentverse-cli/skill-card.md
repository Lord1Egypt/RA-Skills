## Description:

Publish, discover, and manage AI skills, agents, workflows, souls and prompts from the AgentVerse marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate the agentverse CLI for marketplace discovery, publishing, authentication, social actions, benchmarking, and self-updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples execute remote shell or PowerShell scripts from a mutable branch.

Mitigation: Prefer versioned GitHub release binaries and verify checksums or signatures when available.

Risk: Authenticated marketplace commands may handle tokens or saved credentials.

Mitigation: Avoid passing real tokens directly on the command line and confirm where the CLI stores login credentials before use.

Risk: Self-update behavior can change the installed CLI after initial review.

Mitigation: Check the target version before updating and review release artifacts before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loonghao/skills/agentverse-cli)
- [AgentVerse Repository](https://github.com/loonghao/agentverse)
- [AgentVerse API Documentation](https://github.com/loonghao/agentverse#api-documentation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include marketplace artifact identifiers, authentication commands, server URL settings, and version-pinning examples.]

## Skill Version(s):

0.1.4 (source: evidence release metadata, SKILL.md frontmatter, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
