## Description:

Uses the Clawec API to batch query Shopee item details and business metrics for up to 10 item IDs, including price, sales, GMV, ratings, likes, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, operators, and analysts use this skill to retrieve Shopee item details by site and item ID for SKU research, item comparison, competitive analysis, and batch item checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopee item IDs, site/date queries, and the Clawec API key are sent to an external Clawec API.

Mitigation: Use the skill only when that data sharing is acceptable, keep the API key in the CLAWEC_API_KEY environment variable, and avoid unnecessary sensitive research targets.

Risk: Automated use could run API requests without a fresh review of credential handling and query scope.

Mitigation: Review the script before automation and confirm that item IDs, site, date, and environment variables are appropriate for the workflow.

## Reference(s):

- [Shopee item detail response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-item-detail)
- [Clawec API base URL](https://www.clawec.com/api)
- [Clawec API key setup](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with optional JSON API response and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report language is Chinese; requests require a Shopee site, item IDs, and optional date.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
