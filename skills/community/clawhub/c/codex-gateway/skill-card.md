## Description:

Helps an agent query the Codex Supergraph through the MPP 402 payment challenge flow for query operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nealo](https://clawhub.ai/user/nealo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query the Codex Supergraph when a 402 Payment Required MPP challenge must be solved with a funded Tempo wallet. It is limited to GraphQL query operations and does not support mutations or subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Codex Supergraph queries can trigger wallet authentication and automatic payments without enough per-transaction user control.

Mitigation: Set wallet and session spending limits before use, review payment challenges where possible, and require explicit confirmation before wallet login, authentication recovery, or any paid request.

Risk: Payment credentials or wallet-sensitive details could be exposed if an agent prints or logs them.

Mitigation: Do not print raw credentials or private keys; rely on the Tempo CLI wallet and request extensions for signing and payment handling.

## Reference(s):

- [Codex Website](https://www.codex.io)
- [Codex Documentation](https://docs.codex.io)
- [Codex API Key Signup](https://dashboard.codex.io/signup)
- [Codex GraphQL Endpoint](https://graph.codex.io/graphql)
- [Codex MPP Gotchas](references/gotchas.md)
- [MPP Auth Flow Reference](references/mpp-flow.md)
- [Wallet Reference](rules/wallets.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid-request guidance and wallet preflight checks before executing Codex Supergraph queries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
