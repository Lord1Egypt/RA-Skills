## Description:

Use binance-cli for Binance Spot, Futures (USD-S), Convert and many more. Requires auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to have an agent prepare and run binance-cli commands for Binance market data, account, trading, streaming, wallet, loan, staking, and related workflows. Authenticated use can affect a live Binance account and should be limited to intentionally approved actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority over a live Binance account, including trading and other account-affecting actions.

Mitigation: Use testnet or demo first, create least-privilege API keys, disable withdrawals unless required, and require a fresh explicit confirmation for every trade, withdrawal, transfer, loan, staking, or permission change.

Risk: Credential handling can expose API keys or secrets if commands print or search environment data.

Mitigation: Avoid passing secrets in command arguments, never echo or log raw credentials, and follow the artifact authentication guidance for limiting environment inspection.

Risk: Arbitrary signed request URLs can expand the action surface beyond the listed helper commands.

Mitigation: Use signed request URLs only after independently verifying the destination is an intended Binance API endpoint.

Risk: Installation provenance is not backed by server-resolved GitHub import provenance for this version.

Mitigation: Install only when the user intentionally wants Binance account operation and verify the installed @binance/binance-cli package source before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binance-skills-hub/skills/binance-skills)
- [Skill Definition](artifact/SKILL.md)
- [Binance Authentication](artifact/references/auth.md)
- [Algo Trading](artifact/references/algo.md)
- [Alpha](artifact/references/alpha.md)
- [C2C](artifact/references/c2c.md)
- [Convert](artifact/references/convert.md)
- [Copy Trading](artifact/references/copy-trading.md)
- [Crypto Loan](artifact/references/crypto-loan.md)
- [Derivatives Options](artifact/references/derivatives-options.md)
- [Derivatives Options Streams](artifact/references/derivatives-options-streams.md)
- [Derivatives Portfolio Margin](artifact/references/derivatives-portfolio-margin.md)
- [Derivatives Portfolio Margin Streams](artifact/references/derivatives-portfolio-margin-streams.md)
- [Derivatives Portfolio Margin Pro](artifact/references/derivatives-portfolio-margin-pro.md)
- [Derivatives Portfolio Margin Pro Streams](artifact/references/derivatives-portfolio-margin-pro-streams.md)
- [Dual Investment](artifact/references/dual-investment.md)
- [Fiat](artifact/references/fiat.md)
- [COIN-M Futures](artifact/references/futures-coin.md)
- [COIN-M Futures Streams](artifact/references/futures-coin-streams.md)
- [USDS-M Futures](artifact/references/futures-usds.md)
- [USDS-M Futures Streams](artifact/references/futures-usds-streams.md)
- [Gift Card](artifact/references/gift-card.md)
- [Margin Trading](artifact/references/margin-trading.md)
- [Margin Trading Streams](artifact/references/margin-trading-streams.md)
- [Mining](artifact/references/mining.md)
- [Pay](artifact/references/pay.md)
- [Rebate](artifact/references/rebate.md)
- [Simple Earn](artifact/references/simple-earn.md)
- [Spot Trading](artifact/references/spot.md)
- [Spot Trading Streams](artifact/references/spot-streams.md)
- [Staking](artifact/references/staking.md)
- [Sub Account](artifact/references/sub-account.md)
- [VIP Loan](artifact/references/vip-loan.md)
- [Wallet](artifact/references/wallet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline binance-cli commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require Binance API credentials and explicit user confirmation before account-affecting actions.]

## Skill Version(s):

1.2.0 (source: frontmatter and changelog, released 2026-05-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
