## Description: <br>
Trade K-pop lightstick tokens on a bonding curve market using artist popularity, news trends, and price signals to guide buy and sell decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hans1329](https://clawhub.ai/user/hans1329) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading agents use this skill to inspect K-Trendz lightstick token prices, evaluate popularity and news signals, and submit authenticated buy or sell requests within stated trading limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real token buy and sell authority. <br>
Mitigation: Require explicit approval, budget caps, allowed-token lists, slippage limits, and loss limits before any trade. <br>
Risk: Trading depends on trust in the K-Trendz API operator and authenticated API access. <br>
Mitigation: Use this skill only with a trusted API operator and protect the bot API key from exposure. <br>
Risk: Price, trend, and news signals can change quickly and may lead to losses. <br>
Mitigation: Prefer price checks before trades and review current market data before submitting buy or sell requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hans1329/clawhub-skills) <br>
- [K-Trendz API base URL](https://jguylowswwgjvotdcsfj.supabase.co/functions/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, code, configuration] <br>
**Output Format:** [Markdown with JSON request and response examples and pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authenticated endpoint details, trading decision factors, rate limits, fees, slippage settings, and token identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
