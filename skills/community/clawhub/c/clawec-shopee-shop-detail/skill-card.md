## Description:

Queries ClawEC API for Shopee shop details in batches of up to 10 shop IDs, including sales volume, GMV, sales rate, followers, and primary category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agent users use this skill to look up Shopee shop details, compare competitor shops, and prepare concise operating observations from known shop IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Shopee shop IDs, site and date query details, and a ClawEC API bearer token to ClawEC.

Mitigation: Store the API key in CLAWEC_API_KEY, avoid pasting keys into chat or logs, and review ClawEC terms before using the skill for sensitive business research.

Risk: Large shop lists can exceed the API's documented batch limit.

Mitigation: Split requests into batches of no more than 10 shop IDs and keep each batch within a single Shopee site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-shopee-shop-detail)
- [Shopee shop detail response schema](references/response-schema.md)
- [ClawEC API base URL](https://www.clawec.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell commands and structured field summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a Chinese report summarizing query conditions, shop profile fields, operating metrics, and two to three actionable observations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
