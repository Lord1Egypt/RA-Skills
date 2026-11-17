## Description:

The agent's wallet. Use this skill to safely create a wallet the agent can use for transfers, swaps, and any EVM chain transaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to create an agent-operated EVM smart account wallet, retrieve balances, transfer tokens, perform swaps, and send smart contract transactions within owner-defined policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate an agent-controlled crypto wallet through a remote service.

Mitigation: Install only if remote wallet creation and operation are acceptable for the intended use case.

Risk: Default unrestricted transaction authority can allow transfers, swaps, or arbitrary EVM transactions before policies are configured.

Mitigation: Claim the wallet immediately, set restrictive policies before funding it, and require human approval for transactions.

Risk: The API key authenticates wallet operations and could enable unauthorized use if exposed.

Mitigation: Keep the API key secret and avoid mainnet or valuable assets until spending limits and approval flows have been verified.

## Reference(s):

- [Agent Wallet on ClawHub](https://clawhub.ai/glitch003/skills/agent-wallet)
- [SafeSkill API service](https://safeskill-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint examples, Bearer-token authentication guidance, and policy-status handling notes.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
