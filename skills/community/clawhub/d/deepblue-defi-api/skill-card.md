## Description: <br>
Use when an agent needs live DeFi data from Base, including ETH prices, trending pools, token scores, and wallet scans without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[error403agent](https://clawhub.ai/user/error403agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query live read-only DeFi research data for the Base network, including ETH pricing, pool discovery, token scoring, and wallet ERC20 holdings valuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet lookups and DeFi queries are sent to an external API, so wallet addresses should be treated as visible to deepbluebase.xyz despite no-logging claims. <br>
Mitigation: Use wallet scans only for addresses the user is comfortable sending to the external API. <br>
Risk: Deposit, withdrawal, claim, payment, or trading endpoints could affect assets if used outside the read-only research posture. <br>
Mitigation: Do not use any write, payment, trading, deposit, withdrawal, or claim endpoint unless it has separate review and explicit user direction. <br>
Risk: Live DeFi scores and market data can be incorrect, stale, or misleading if used as financial advice. <br>
Mitigation: Treat returned scores and market data as research signals only and verify important decisions against independent sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/error403agent/deepblue-defi-api) <br>
- [DeepBlue API Homepage](https://deepbluebase.xyz) <br>
- [DeepBlue Interactive API Docs](https://deepbluebase.xyz/docs) <br>
- [DeepBlue Pricing and Tiers](https://deepbluebase.xyz/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API Calls] <br>
**Output Format:** [Markdown with REST endpoint examples, curl commands, Python snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are read-only DeFi data requests and guidance for Base network API usage.] <br>

## Skill Version(s): <br>
1.4.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
