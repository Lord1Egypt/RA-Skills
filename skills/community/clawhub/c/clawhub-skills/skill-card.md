## Description:

Trade K-pop lightstick tokens on a bonding curve market using artist popularity, news trends, and price signals to guide buy and sell decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hans1329](https://clawhub.ai/user/hans1329)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to query K-Trendz token prices and prepare API requests for buying or selling K-pop lightstick tokens based on trend, news, price, fee, and limit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to buy or sell real-value tokens using an API key.

Mitigation: Require explicit confirmation for every trade, including slippage, fees, daily limits, potential financial loss, and transaction finality.

Risk: The API key provides access to a trading account.

Mitigation: Use only an account and key intended for this skill, keep the key out of logs and shared outputs, and revoke it when no longer needed.

Risk: Trend, news, and price signals may be incomplete, stale, or misleading.

Mitigation: Review current market data and the proposed buy or sell rationale before allowing the agent to submit a transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hans1329/skills/clawhub-skills)
- [K-Trendz API Base URL](https://jguylowswwgjvotdcsfj.supabase.co/functions/v1/)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Code, Configuration]

**Output Format:** [Markdown with JSON request examples, response examples, and Python pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key; trade requests should be reviewed for slippage, fees, daily limits, and transaction finality before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
