## Description: <br>
DeFi Risk Scanner helps agents assess Web3 and DeFi protocol or token risk using structured scoring, factor breakdowns, key metric interpretation, and actionable review guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emeraldring3134-netizen](https://clawhub.ai/user/emeraldring3134-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to screen DeFi protocols or token addresses for TVL, liquidity, market-cap, FDV, activity, and chain-diversity signals before deeper due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local bash helper that uses curl and jq and sends the target protocol slug or token address to public API services. <br>
Mitigation: Install only when that execution model and data sharing are acceptable, and review the script before use. <br>
Risk: The generated score can be mistaken for investment or safety advice. <br>
Mitigation: Treat the score as an educational screening aid and verify important conclusions with independent sources before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/emeraldring3134-netizen/defi-risk-scanner) <br>
- [Reference data sources and checklist](references/sources.md) <br>
- [DeFiLlama protocol API](https://api.llama.fi/protocol/{name}) <br>
- [DexScreener token API](https://api.dexscreener.com/latest/dex/tokens/{address}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Terminal text report with risk scores, metric summaries, factor breakdowns, and follow-up recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public DeFiLlama and DexScreener API data; results are screening guidance, not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
