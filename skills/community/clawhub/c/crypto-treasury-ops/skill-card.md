## Description:

Safely manage EVM treasury operations and native Hyperliquid trading for OpenClaw agents, including wallet balance checks, guarded token transfers, cross-chain USDC bridging, Hyperliquid deposits, destination gas top-ups, trading safety, and structured quoting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiowind](https://clawhub.ai/user/fiowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let OpenClaw agents quote, validate, and execute guarded treasury actions across Ethereum, Polygon, Arbitrum, Base, Solana bridge-source flows, and Hyperliquid perpetual accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign high-impact crypto transactions from hot-wallet keys.

Mitigation: Use a low-balance dedicated wallet, strict allowlists, small limits, dry runs, and preferably a vault, KMS, HSM, or delegated signer.

Risk: Treasury actions may rely on third-party transaction payloads and provider routes.

Mitigation: Review provider URLs, use fresh quotes, require explicit operator approval, and avoid primary treasury keys until transaction decoding, exact allowances, and endpoint allowlists are added.

Risk: Multi-stage bridge and Hyperliquid deposit flows can partially complete before an error.

Mitigation: Re-check source and destination balances, then re-run quote_operation with the remaining balance instead of replaying a stale amount.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fiowind/skills/crypto-treasury-ops)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON responses and Markdown documentation with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing operations support quote and dry-run flows before execution.]

## Skill Version(s):

0.1.7 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
