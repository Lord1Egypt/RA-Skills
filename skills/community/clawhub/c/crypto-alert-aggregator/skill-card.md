## Description:

Aggregates real-time crypto market data and Twitter signals into actionable alerts for traders and researchers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackfeng0614-prog](https://clawhub.ai/user/jackfeng0614-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and researchers use this skill to aggregate crypto market movement and social sentiment signals into alert data for monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill presents random mock data as real crypto and Twitter alerts while reading credentials it does not actually use.

Mitigation: Do not rely on alerts for trading decisions; require verified live data retrieval before operational use.

Risk: The security guidance warns against providing real crypto, Twitter, or webhook credentials to this version.

Mitigation: Use synthetic or non-sensitive credentials only until the publisher documents and implements verifiable API and webhook handling.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Code, Configuration instructions]

**Output Format:** [JSON alert objects and JavaScript callback output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts include asset, type, value, change, Twitter mentions, sentiment, confidence, timestamp, and message fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
