## Description:

AgentsBank provides a TypeScript and JavaScript SDK for agents to authenticate with AgentsBank, read multi-chain wallet data, sign messages, estimate fees, create wallets, and submit crypto transactions through the AgentsBank API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryruz](https://clawhub.ai/user/cryruz)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect agents to AgentsBank crypto wallet services for balance checks, transaction history, message signing, fee estimation, and user-approved wallet or transfer operations. It is intended for integrations where real credentials and funds may be involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SDK can submit real crypto transactions and wallet operations, which may cause irreversible fund movement.

Mitigation: Require explicit human review before write-capable calls and test with small amounts or testnet chains before using real funds.

Risk: Write-capable credentials exposed to autonomous agents could allow unintended transfers.

Mitigation: Use read-only or tightly scoped credentials where possible, keep secrets out of version control, and rotate exposed credentials.

Risk: Automatic retries on transfer operations could repeat financial actions if idempotency is not guaranteed.

Mitigation: Disable automatic retries for transfer operations unless server-side idempotency and transaction state handling are confirmed.

Risk: Documented client-side guardrails may not be an enforced security boundary.

Mitigation: Rely on server-side controls for spending limits, approvals, and endpoint restrictions; verify the service enforces those constraints.

## Reference(s):

- [ClawHub AgentsBank Skill Page](https://clawhub.ai/cryruz/skills/agentsbank)
- [AgentsBank SDK Documentation](https://docs.agentsbank.online/sdk)
- [AgentsBank API Reference](https://api.agentsbank.online/docs)
- [AgentsBank Security Guide](https://docs.agentsbank.online/security)
- [AgentsBank Website](https://agentsbank.online)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, environment-variable configuration, and API response objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SDK calls may return wallet, balance, transaction, signature, catalogue, health, and fee-estimate data from the AgentsBank API.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact package.json and CHANGELOG show 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
