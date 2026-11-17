## Description:

Queries the ClawEC API for Shopee item trend time series, including sales, GMV, price, ratings, likes, and comments at monthly, quarterly, or yearly granularity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and analysts use this skill to review a single Shopee item's historical operating trend over a chosen date range. It helps compare sales, GMV, price, ratings, and engagement changes for competitive product observation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopee item IDs, date ranges, and the ClawEC API key are sent to clawec.com during live API calls.

Mitigation: Install and run the skill only when that data sharing is intended, and review the endpoint before using the helper script.

Risk: API keys can be exposed if pasted into chat logs or hard-coded into commands.

Mitigation: Store the ClawEC API key in an environment variable or secret store and avoid sharing it in conversation history.

## Reference(s):

- [Shopee item trend response schema](references/response-schema.md)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC Shopee item trend endpoint](https://www.clawec.com/api/aigc/ec/shopee/data/item/trend)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-item-trend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with trend tables and interpretation; live API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Shopee site code, item ID, granularity, date range, and a CLAWEC_API_KEY for live API calls.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
