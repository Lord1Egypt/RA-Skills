## Description: <br>
Fía Signals gives agents crypto market intelligence through shell commands and API lookups covering price predictions, technical indicators, gas prices, DeFi yields, wallet risk, MEV, and related market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Odds7](https://clawhub.ai/user/Odds7) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to query Fía Signals for crypto market data, technical signals, on-chain indicators, gas prices, DeFi yields, wallet risk, and premium x402-gated intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto lookup inputs such as wallet addresses, contract addresses, token symbols, and chain names are sent to Fía Signals. <br>
Mitigation: Use the skill only when those inputs are appropriate to share with Fía Signals, and do not provide private keys, seed phrases, wallet passwords, or unrelated sensitive data. <br>
Risk: Premium endpoints may lead to x402 USDC payment flows. <br>
Mitigation: Review endpoint pricing and payment links before authorizing or following any paid request. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/Odds7/fia-signals-skill) <br>
- [Fía Signals API](https://api.fiasignals.com) <br>
- [Fía Signals x402 Discovery](https://x402.fiasignals.com/.well-known/x402.json) <br>
- [Fía Signals x402 Gateway](https://x402.fiasignals.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown and terminal text with JSON responses from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free endpoints require no API key; premium endpoints may return x402 payment links before data is available.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
