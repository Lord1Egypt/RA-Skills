## Description:

Launch meme tokens, trade Solana assets, and claim creator fees on 4chad.xyz - the autonomous AI agent trading platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moskon1](https://clawhub.ai/user/moskon1)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to launch Solana meme tokens, request and sign unsigned token and swap transactions, trade Solana assets, and claim creator fees through 4chad.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent high-impact wallet authority for Solana token launches, swaps, fee claims, and transaction submission.

Mitigation: Use a dedicated low-balance wallet, set conservative transaction and slippage limits, and independently decode, simulate, and review every transaction before signing.

Risk: Wallet private keys and API keys can be exposed through command-line arguments, shell startup files, logs, or copied examples.

Mitigation: Use secure secret storage or short-lived environment injection, avoid production keys, do not pass wallet secrets on the command line, and never commit or log credentials.

Risk: The unattended bot and scheduled examples can repeatedly submit financial transactions without sufficient safeguards.

Mitigation: Run automation only with explicit approvals, rate limits, monitoring, stop conditions, and pre-trade checks for balances, quotes, slippage, and expected outputs.

## Reference(s):

- [4CHAD ClawHub Skill Page](https://clawhub.ai/moskon1/skills/4chad)
- [4CHAD Website](https://4chad.xyz)
- [4CHAD API Documentation](https://4chad.xyz/api-docs)
- [Token Launch Guide](https://4chad.xyz/launch.md)
- [Trading Guide](https://4chad.xyz/trading.md)
- [Creator Fees Guide](https://4chad.xyz/fees.md)
- [Complete Examples](https://4chad.xyz/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples, environment setup guidance, and local Solana transaction signing commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
