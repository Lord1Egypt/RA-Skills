## Description: <br>
Use binance-cli for Binance Spot, Futures (USD-S), Convert and many more. Requires auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to prepare Binance CLI commands, credential setup steps, and command references for Spot, Futures, Convert, wallet, margin, and related authenticated Binance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate authenticated Binance trading, wallet, raw signed API, leverage, subscription, redemption, withdrawal, and Travel Rule PII workflows. <br>
Mitigation: Use testnet or demo first, create least-privilege API keys, disable withdrawal permission unless absolutely required, and require explicit confirmation before high-risk account actions. <br>
Risk: Incorrect order, transfer, leverage, redemption, subscription, or signed request parameters can affect live account assets. <br>
Mitigation: Manually review every symbol, side, quantity, price, wallet, profile, environment, endpoint, and signed raw request parameter before execution. <br>
Risk: Binance API keys and secrets are sensitive credentials. <br>
Mitigation: Never echo or log raw credentials, avoid broad environment dumps, and inspect only specifically named credential variables when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binance-skills-hub/binance-skills) <br>
- [Publisher profile](https://clawhub.ai/user/binance-skills-hub) <br>
- [binance-cli npm package](https://www.npmjs.com/package/@binance/binance-cli) <br>
- [Authentication and security rules](references/auth.md) <br>
- [Spot trading commands](references/spot.md) <br>
- [USDS-M Futures commands](references/futures-usds.md) <br>
- [COIN-M Futures commands](references/futures-coin.md) <br>
- [Margin trading commands](references/margin-trading.md) <br>
- [Wallet commands](references/wallet.md) <br>
- [Spot trading streams](references/spot-streams.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to stdout and stderr from binance-cli; authenticated workflows require configured Binance API credentials.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, skill frontmatter, and changelog dated 2026-05-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
