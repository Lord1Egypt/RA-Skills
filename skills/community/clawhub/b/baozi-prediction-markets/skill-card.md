## Description:

Access Solana prediction markets on Baozi. Use when user wants to check market odds, get betting quotes, list active markets, analyze opportunities, or place bets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aratox666-max](https://clawhub.ai/user/aratox666-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interact with Baozi prediction markets on Solana: listing active markets, checking odds and bet quotes, reviewing wallet positions, analyzing markets, and preparing bets for user signature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party MCP server code in a financial workflow.

Mitigation: Use a pinned and reviewed version of the Baozi MCP server, run it in a restricted environment, and review outputs before acting on them.

Risk: Transactions can affect funds even though the agent does not hold private keys.

Mitigation: Keep private keys and seed phrases out of the agent environment, verify every transaction in the wallet before signing, and test on devnet before live use.

Risk: The skill describes automatic wallet-address affiliate registration without clear opt-in.

Mitigation: Do not proceed unless wallet-address affiliate registration is acceptable or can be disabled.

## Reference(s):

- [Baozi REST API](https://baozi.bet/api/)
- [ClawHub skill page](https://clawhub.ai/aratox666-max/skills/baozi-prediction-markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market IDs, wallet addresses, quote amounts, environment variable guidance, and transaction-signing cautions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
