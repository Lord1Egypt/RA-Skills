## Description: <br>
Use when the user wants to query the Codex Supergraph and the server returns a 402 challenge; it pays per query via the MPP 402 challenge flow and only supports queries, not mutations or subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nealo](https://clawhub.ai/user/nealo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to make paid Codex Supergraph GraphQL queries when the service returns an MPP 402 payment challenge. It guides wallet preflight, Tempo request handling, and query-only constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent into wallet login, payment credential signing, and paid USDC-backed requests. <br>
Mitigation: Use it only for intended paid Codex Supergraph queries, keep wallet balances limited, and require explicit user confirmation before login, signing, or retrying a paid request. <br>
Risk: Payment credentials, wallet state, and request headers are sensitive. <br>
Mitigation: Do not print raw credentials or private keys; rely on Tempo CLI wallet handling and run a wallet preflight check before paid requests. <br>
Risk: MPP mode supports queries only; mutation or subscription attempts fail or require a different authentication path. <br>
Mitigation: Use MPP only for GraphQL query operations and use API key or bearer authentication for non-query operations. <br>


## Reference(s): <br>
- [Codex Agentic Gateway on ClawHub](https://clawhub.ai/nealo/codex-gateway) <br>
- [Publisher Profile](https://clawhub.ai/user/nealo) <br>
- [Codex Website](https://www.codex.io) <br>
- [Codex Documentation](https://docs.codex.io) <br>
- [Codex API Key Signup](https://dashboard.codex.io/signup) <br>
- [Codex MPP Gotchas](references/gotchas.md) <br>
- [MPP Auth Flow Reference](references/mpp-flow.md) <br>
- [Wallet Reference](rules/wallets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run Tempo wallet and paid request commands for query-only Codex Supergraph access.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
