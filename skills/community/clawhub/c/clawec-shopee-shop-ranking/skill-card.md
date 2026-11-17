## Description:

Queries Shopee shop rankings through the Clawec API for bestseller and fast-rising lists by site, category, period, local or cross-border store type, and product type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and market researchers use this skill to query and interpret Shopee shop rankings for competitor research, shop benchmarking, category analysis, and site-level product selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Shopee ranking query parameters to clawec.com with the user's ClawEC API key.

Mitigation: Install only when ClawEC use is intended, review query contents before execution, and avoid submitting sensitive business research parameters unnecessarily.

Risk: The ClawEC API key could be exposed if copied into prompts, committed to files, or logged.

Mitigation: Store the key in the CLAWEC_API_KEY environment variable and avoid hardcoding or sharing it in prompts, scripts, logs, or generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-shop-ranking)
- [Shopee shop ranking response schema](references/response-schema.md)
- [ClawEC API base](https://www.clawec.com/api)
- [Shopee shop ranking API endpoint](https://www.clawec.com/api/aigc/ec/shopee/data/shop/ranking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown reports with ranking tables, query conditions, competitor observations, conclusions, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAWEC_API_KEY environment variable for live API calls; pageSize is limited to 10 by the skill documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
