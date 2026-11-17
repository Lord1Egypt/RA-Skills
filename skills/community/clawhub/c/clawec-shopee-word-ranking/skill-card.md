## Description:

Queries the Clawec API for Shopee keyword ranking lists, including hot-selling and trending rankings by site, category, period, and ranking scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border ecommerce operators and agents use this skill to query Shopee hot keyword rankings, compare demand and competition metrics, and produce keyword selection guidance for product research and listing strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clawec API credentials and ranking parameters are sent to the Clawec service when the skill runs.

Mitigation: Store CLAWEC_API_KEY in an environment variable, do not hard-code credentials, and use the skill only for intended Shopee keyword research.

Risk: Failed API calls or invalid ranking parameters can lead to incomplete or misleading keyword analysis.

Mitigation: Check the top-level status and data.success fields before interpreting results, and surface errorCode and errorMessage when the API reports a failure.

## Reference(s):

- [Response Schema](references/response-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-word-ranking)
- [Clawec API](https://www.clawec.com/api)
- [Clawec API Key](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown report with ranking tables, metric interpretation, keyword recommendations, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses site, category, ranking type, period, ranking scope, pagination, optional date, and a CLAWEC_API_KEY credential.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
