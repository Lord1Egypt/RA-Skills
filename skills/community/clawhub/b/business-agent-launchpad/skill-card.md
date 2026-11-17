## Description:

Use when a user wants to initialize OpenClaw, Hermes, or another agent harness for ordinary business or office work by guiding business interviews, agent roles, object-based Markdown memory, tool permissions, model tiers, free/paid upgrade paths, and starter workspaces with the `agent-launchpad` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and developers use this skill to turn ordinary office workflows into starter OpenClaw or Hermes agent workspaces with role guidance, Markdown memory, permission plans, model-tier choices, and verification commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may run a global npm install from an unspecified local folder, which can install the wrong project or execute untrusted package scripts.

Mitigation: Verify the exact project directory, review package scripts before installation, and prefer a pinned local CLI install path.

Risk: Generated business-agent workspaces may touch sensitive legal, finance, HR, customer, executive, CRM, ERP, payment, or audit workflows.

Mitigation: Require explicit user approval before external actions or sensitive data storage, and keep regulated workflows as review-support rather than autonomous decision workflows.

## Reference(s):

- [Business Agent Launchpad on ClawHub](https://clawhub.ai/andyrenxu7255/skills/business-agent-launchpad)
- [Publisher profile: andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated workspace file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces starter workspace guidance for OpenClaw or Hermes business-agent setups.]

## Skill Version(s):

0.1.0 (source: server release evidence, SKILL.md frontmatter, clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
