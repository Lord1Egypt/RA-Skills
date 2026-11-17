## Description:

Blockchain Scanner queries EVM blockchain data, including native balances, ERC-20 token balances, transaction history, gas prices, and verified contract ABIs across supported networks through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query balances, token balances, transaction history, gas estimates, and verified contract ABIs across supported EVM networks through AgentPMT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote tool instructions or setup dependencies may change after installation.

Mitigation: Review the AgentPMT setup skills and current schema before production use, especially before running any npx install command.

Risk: Wallet addresses and transaction queries are sent to AgentPMT and may consume credits.

Mitigation: Send only the addresses and chain parameters required for the task, and confirm credit usage expectations before high-volume lookups.

Risk: Secrets such as private keys, mnemonics, signatures, account credentials, or payment headers could be exposed if included in prompts or logs.

Mitigation: Do not include secrets in tool inputs, prompts, examples, or logs; use the setup skills for credential handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/blockchain-scanner)
- [AgentPMT publisher profile](https://clawhub.ai/user/agentpmt)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/blockchain-scanner)
- [Blockchain Scanner schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON request examples and schema references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for invoking remote AgentPMT blockchain lookup actions; tool responses are expected as JSON from the remote service.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
