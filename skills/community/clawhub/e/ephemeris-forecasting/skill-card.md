## Description:

Helps agents forecast user-provided numeric time series with uncertainty intervals through Ephemeris.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can forecast supplied sales, demand, capacity, energy or other numeric series and review prediction intervals for planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted time-series values and covariates are sent to Ephemeris.

Mitigation: Avoid sensitive business or personal data unless account terms and privacy expectations permit sharing it.

Risk: Successful forecasts spend account credits.

Mitigation: Avoid unrequested forecasts or loops, check the balance before large batches, and reuse an idempotency key on retries.

Risk: Exposing the API key can allow unauthorized use.

Mitigation: Keep the key in a secret store or local configuration; do not paste it into chat or commit it.

## Reference(s):

- [Ephemeris documentation](https://ephemeris.cascade.industries/llms-full.txt)
- [Ephemeris homepage](https://ephemeris.cascade.industries)
- [ClawHub skill release](https://clawhub.ai/tensorlink-dev/skills/ephemeris-forecasting)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with forecast ranges and optional curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports uncertainty intervals, models used, notes and credits spent when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
