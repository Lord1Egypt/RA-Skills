## Description:

Check a Nodary AirnodeHub crypto feed every five minutes against a retained alert baseline and announce an attested alert only after a 5% or greater change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub users can create a recurring alert for a chosen crypto price feed and receive a message when the price moves at least 5% from the retained baseline. Alerts are informational, not trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A five-minute automation continues contacting the public price endpoint and may announce qualifying changes until removed.

Mitigation: Review the requested feed and remove the automation when ongoing alerts are no longer wanted.

Risk: Crypto price alerts could be mistaken for trading recommendations.

Mitigation: Treat alerts as informational and verify prices independently before making financial decisions.

## Reference(s):

- [Nodary AirnodeHub documentation](https://airnode-v2-hub.api3.org/llms.txt)
- [Nodary price feed endpoint](https://airnode-nodary.fly.dev/)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance]

**Output Format:** [Short conversation announcement and automation setup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports feed, prices, percentage change, direction, source timestamp, and job ID; sends no message for non-qualifying checks.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
