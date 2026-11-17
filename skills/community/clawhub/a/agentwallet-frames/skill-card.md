## Description:

Wallets for AI agents with x402 payment signing, referral rewards, and policy-controlled actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[microchipgnu](https://clawhub.ai/user/microchipgnu)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use Agent Wallet to connect a server-custodied wallet, monitor balances and activity, and request policy-controlled wallet actions such as transfers, message signing, contract calls, and x402 paid API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact financial actions including transfers, contract calls, signatures, and paid API requests.

Mitigation: Require explicit human confirmation or dry-run review before transfers, contract calls, signatures, or paid x402 requests.

Risk: Wallet actions are server-custodied and proxied request data is handled by frames.ag.

Mitigation: Install and use the skill only when the operator trusts frames.ag to custody wallet actions and process proxied request data.

Risk: The heartbeat documentation includes remote self-update commands for persistent skill files.

Mitigation: Do not run the self-update commands as written; manually review updated skill files before replacing local instructions.

Risk: Forwarding broad request headers through x402/fetch can expose unrelated credentials.

Mitigation: Avoid forwarding Authorization, Cookie, or unrelated API-key headers through the payment proxy.

## Reference(s):

- [Agent Wallet on ClawHub](https://clawhub.ai/microchipgnu/skills/agentwallet-frames)
- [AgentWallet Homepage](https://frames.ag)
- [AgentWallet API Base](https://frames.ag/api)
- [AgentWallet Skill File](https://frames.ag/skill.md)
- [AgentWallet Heartbeat](https://frames.ag/heartbeat.md)
- [AgentWallet Skill Metadata](https://frames.ag/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API requests and wallet action payloads that require user-provided credentials.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact metadata reports 0.1.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
