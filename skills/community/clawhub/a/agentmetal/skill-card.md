## Description:

Guides agents through renting and operating Linux VPS instances with USDC or card payment, SSH access, and lease management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiscosio](https://clawhub.ai/user/luiscosio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to provision, connect to, manage, and retire rented Linux servers for deployments and hosted services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid provisioning, extensions, and add-ons can spend wallet funds.

Mitigation: Use a dedicated low-balance wallet, set a tight AGENTMETAL_MAX_USDC spend limit, and require human approval for paid actions.

Risk: Root command execution, reboot, or destruction can disrupt or erase a server.

Mitigation: Require human approval before root execution, reboot, or destruction; confirm the target server first.

Risk: Wallet private keys, account keys, and generated SSH private keys may be exposed.

Mitigation: Keep credentials out of logs and prompts, and store generated SSH private keys securely.

## Reference(s):

- [AgentMetal skill on ClawHub](https://clawhub.ai/luiscosio/skills/agentmetal)
- [AgentMetal homepage](https://agentmetal.dev)
- [AgentMetal agent documentation](https://api.agentmetal.dev/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include server identifiers, SSH connection details, and operational results.]

## Skill Version(s):

0.3.4 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
