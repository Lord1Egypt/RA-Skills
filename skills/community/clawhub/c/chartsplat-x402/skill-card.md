## Description:

Generates PNG charts through Chart Splat using x402 USDC micropayments on Base instead of an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbyg603](https://clawhub.ai/user/bobbyg603)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create line, bar, pie, doughnut, radar, polar area, candlestick, and OHLC charts as PNG files when they want wallet-based pay-per-call access rather than an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs npm CLI code with a wallet private key that can authorize payments.

Mitigation: Use a dedicated low-balance wallet, expose only X402_PRIVATE_KEY in a restricted environment, and prefer a pinned, reviewed CLI version.

Risk: Paid chart requests spend USDC on the advertised Base network.

Mitigation: Confirm the expected amount, network, token, and recipient before allowing paid requests.

Risk: Private keys can be exposed through chat, shell history, or command arguments.

Mitigation: Do not use a main wallet or paste a valuable private key into chat, shell history, or commands.

## Reference(s):

- [Chart Splat x402 Protocol Reference](references/x402-protocol.md)
- [Chart Splat Homepage](https://chartsplat.com)
- [Chart Splat Documentation](https://chartsplat.com/docs)
- [ClawHub Skill Page](https://clawhub.ai/bobbyg603/skills/chartsplat-x402)
- [x402 Protocol and SDKs](https://github.com/x402-foundation/x402)
- [x402 Facilitator](https://x402.org/facilitator)
- [EIP-3009 Transfer With Authorization](https://eips.ethereum.org/EIPS/eip-3009)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON chart configuration examples, and PNG file path outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated charts are saved as PNG files; paid requests require X402_PRIVATE_KEY and a low-balance USDC wallet on Base.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
