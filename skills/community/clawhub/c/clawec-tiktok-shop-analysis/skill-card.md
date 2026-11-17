## Description:

Uses the ClawEC API to analyze TikTok Shop products, including channel distribution, content format, paid versus organic traffic, daily trends, and optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to submit TikTok Shop product IDs or links to ClawEC and receive product-level analysis. It helps summarize product metrics, channel mix, content mix, paid versus organic traffic, trends, and optional AI interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product IDs, product links, region selections, log IDs, and authenticated requests are sent to clawec.com.

Mitigation: Submit only product data and URLs that are appropriate to share with ClawEC, and avoid sensitive or tracking-heavy URLs.

Risk: The skill depends on a CLAWEC_API_KEY-backed request flow.

Mitigation: Keep the API key in the CLAWEC_API_KEY environment variable and do not hardcode it in scripts, prompts, or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-tiktok-shop-analysis)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)
- [TikTok product analysis submit endpoint](https://www.clawec.com/api/aigc/ec/tiktok/product_analysis/search)
- [TikTok product analysis logs endpoint](https://www.clawec.com/api/aigc/ec/tiktok/product_analysis/search/logs)
- [TikTok product analysis detail endpoint](https://www.clawec.com/api/aigc/ec/tiktok/product_analysis/search/log/detail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with optional bash commands and API response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default summaries are in Chinese and may include AI analysis when requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
