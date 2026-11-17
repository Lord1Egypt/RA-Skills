## Description:

EVM wallet tool for autonomous agents that creates, signs, and broadcasts ETH/ERC20 transfers, x402 payments, arbitrary contract calls, and swaps while recording transactions to a JSON log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cromatikap](https://clawhub.ai/user/cromatikap)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill when an agent needs to make EVM payments, paid x402 API requests, token transfers, swaps, or transaction-log entries with a local audit trail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad, irreversible wallet spending and contract-signing power.

Mitigation: Use a low-balance dedicated wallet, require human approval for every signing action, and pin and review dependencies before use.

Risk: x402 requests can sign payments to unexpected amounts or recipients.

Mitigation: Always set --max-amount and, when the provider address is stable, set --pay-to.

Risk: Swaps and arbitrary calldata can execute unintended or poorly bounded on-chain actions.

Mitigation: Set --min-out for swaps and avoid --calldata unless the destination contract and function are independently verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cromatikap/skills/cdnsoft-wallet)
- [agentwallet documentation](https://cdnsoft.github.io/agentwallet)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or appends agentwallet.json transaction records; signing and broadcast behavior depends on wallet key, RPC endpoint, recipient, amount, and payment constraints.]

## Skill Version(s):

0.3.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
