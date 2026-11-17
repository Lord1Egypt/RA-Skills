## Description:

Execute BNB Chain EVM swing trades after importing a private key: buy when trigger price exceeds market condition, then place 5% take-profit and 3% stop-loss management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyrstudent](https://clawhub.ai/user/happyrstudent)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to configure and run a BNB Chain band-trading bot that monitors a trigger price and applies fixed take-profit and stop-loss thresholds. It is intended for wallet-key based trading workflows that should be dry-run and audited before any real funds are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide an EVM private key, and the security evidence flags this as sensitive for any real wallet.

Mitigation: Use a test or low-value wallet, keep the key only in a secret environment variable, and avoid funding the wallet until the trading flow is fully implemented and audited.

Risk: The included bot logs placeholder trades and does not implement production transaction signing, router integration, gas checks, balance checks, limits, or confirmation handling.

Mitigation: Run in dry-run mode first, wire and review the production quote and swap path, and validate slippage, gas, balance, limits, and confirmations before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happyrstudent/skills/evm-bnb-band-trader)
- [ClawHub publisher profile](https://clawhub.ai/user/happyrstudent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and Python script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment variables for wallet key, RPC endpoint, tokens, trigger price, position size, and polling settings.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
