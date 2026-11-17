## Description:

Give your agent an account in one command: twelve words that sign every call, hold a prepaid USDC balance and lock the vault, then compute, inference, phone, email and calls from the terminal or as MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage an Agentgates account, inspect its balance, and access compute, inference, phone, email, and call services through CLI commands or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The account's twelve-word recovery phrase grants access to its funds and signing identity.

Mitigation: Use a dedicated account and protect the recovery phrase; provide it only when the account owner authorizes it.

Risk: CLI operations can spend the owner's prepaid balance on paid services.

Mitigation: Get owner approval before spending or stay within an explicit spending budget; check prices before making paid calls.

Risk: The skill document's scan does not cover the downloaded CLI package implementation.

Mitigation: Review the CLI package and version before installing it globally.

## Reference(s):

- [Agentgates CLI on ClawHub](https://clawhub.ai/agentgates/skills/agentgates-cli)
- [Agentgates account API documentation](https://api.agentgates.ai/api/account/docs)
- [Agentgates product catalog and pricing](https://api.agentgates.ai/api/account/catalog)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell command examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create accounts, access paid services, or spend the account owner's prepaid balance.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
