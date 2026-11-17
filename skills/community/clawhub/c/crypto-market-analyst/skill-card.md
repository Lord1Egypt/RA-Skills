## Description:

Analyze Bitcoin, Ethereum, and major altcoins using real-time price, on-chain signals, and macro context from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to generate structured crypto market reports covering dominance, volatility, cycle position, altcoin performance, sentiment proxies, and positioning signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces crypto research and positioning signals that could be mistaken for personalized financial advice.

Mitigation: Treat outputs as market research only and require human review before making financial decisions.

Risk: The workflow requires a Finskills API key and sends market-data requests to Finskills endpoints.

Mitigation: Install only when the user is comfortable providing the API key and permitting those external market-data requests.

Risk: The documented workflow appears to rely on price, market, history, and macro proxy data rather than true on-chain metrics.

Mitigation: Avoid presenting the analysis as complete on-chain due diligence unless additional verified on-chain data sources are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/crypto-market-analyst)
- [Finskills API](https://finskills.net)
- [Skill homepage](https://github.com/finskills/crypto-market-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Structured Markdown market report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and uses Finskills market-data endpoints for crypto analysis.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
