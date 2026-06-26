## Description: <br>
Alpha Finder (x402) provides prediction market intelligence for Polymarket and Kalshi research, probability assessments, market sentiment analysis, and arbitrage opportunity identification at $0.03 USDC per request on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TzannetosGiannis](https://clawhub.ai/user/TzannetosGiannis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Traders, researchers, and analysts use this skill to research prediction markets, compare odds and sentiment, and identify possible market inefficiencies or arbitrage opportunities across Polymarket, Kalshi, and related sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a raw Base wallet private key and exposes it to external npm code. <br>
Mitigation: Use only a dedicated low-balance Base wallet, avoid main wallet private keys, and restrict permissions on any x402 config file. <br>
Risk: Each request may charge $0.03 USDC via x402 on Base. <br>
Mitigation: Confirm the intended request before running the skill and keep only the spending amount needed in the dedicated wallet. <br>
Risk: The skill runs external npm code that is not pinned or fully reviewed in the bundle. <br>
Mitigation: Review the external package and command before use and run the skill in a constrained environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TzannetosGiannis/alpha-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [$0.03 USDC per request via x402 on Base; requires X402_PRIVATE_KEY or x402-config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
