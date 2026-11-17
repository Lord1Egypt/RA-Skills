## Description:

Local Solana agent wallet with local infra for transfers (SOL, USDC, USDT), Jupiter swaps, and x402 purch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willmcdeezy](https://clawhub.ai/user/willmcdeezy)

### License/Terms of Use:


## Use Case:

Developers and agent builders use Fuego to create and operate a local Solana wallet workflow for balance checks, SOL/USDC/USDT transfers, Jupiter swap quotes and swaps, and x402 purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing mutable wallet software and operating a persistent hot wallet can expose real funds to unreviewed code or unintended transactions.

Mitigation: Review or trust the external fuego-cli code before use, pin and verify the package where possible, and keep only low balances in a dedicated wallet.

Risk: Transfers, swaps, and purchases can move funds on Solana mainnet without sufficient scoping or consent guardrails.

Mitigation: Test on devnet first and require explicit human approval for every transfer, swap, or purchase.

Risk: The x402 purchase flow can handle payment signing and sensitive shipping data in the local workflow.

Mitigation: Use stronger isolation and privacy controls before storing meaningful funds or sensitive shipping data in this workflow.

## Reference(s):

- [Fuego homepage](https://fuego.cash)
- [ClawHub skill page](https://clawhub.ai/willmcdeezy/skills/fuego)
- [Jupiter portal](https://portal.jup.ag)
- [Jupiter token list](https://jup.ag)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that install fuego-cli, configure a local wallet, start a localhost service, query balances, build transactions, submit signed transactions, and execute swaps or x402 purchases.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
