## Description:

2D volatility smile and skew analysis for a single expiration date that maps implied volatility across strikes and returns smile curve data, skew metrics, and shape classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading analysts use this skill to inspect a single-expiration volatility smile, compare put and call skew, classify smile shape, and generate options-market interpretation for a requested ticker and expiry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send requested ticker and expiry data to the configured AlphaGBM API endpoint.

Mitigation: Use it only when sharing those market-data requests with AlphaGBM is acceptable, and review the configured ALPHAGBM_BASE_URL before use.

Risk: The output may include trading ideas or market interpretation.

Mitigation: Treat results as analytical context and review them independently before making financial decisions.

Risk: Using live AlphaGBM data may require an API key.

Mitigation: Provide ALPHAGBM_API_KEY only in the intended environment and avoid exposing it in prompts, logs, or shared transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-vol-smile)
- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Guidance]

**Output Format:** [Markdown with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AlphaGBM API data for requested tickers and expiries; demo tickers are documented as available without an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
