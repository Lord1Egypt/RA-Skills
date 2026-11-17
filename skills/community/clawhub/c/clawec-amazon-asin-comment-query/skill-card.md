## Description:

Queries Amazon product reviews by ASIN or product URL through the Clawec API for review retrieval and buyer-feedback analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and analysts use this skill to query Amazon review data by product URL or ASIN and region, then summarize review counts, ratings, individual comments, and recurring positive or negative buyer-feedback themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon product URLs or ASIN and region values are sent to Clawec with the user's Clawec API key.

Mitigation: Use the skill only for product identifiers suitable for disclosure to Clawec, avoid private or internal URLs, and keep the API key in an environment variable or secrets manager.

Risk: Documentation and default analysis guidance are primarily Chinese, which may affect reviewability for non-Chinese operators.

Mitigation: Ask the agent to translate or summarize outputs in the operator's preferred language before relying on the results.

## Reference(s):

- [Amazon ASIN Comment Query Response Schema](references/response-schema.md)
- [Clawec Amazon Review Query API Endpoint](https://www.clawec.com/api/aigc/tool/amazon_asin_comment_query)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-asin-comment-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional JSON excerpts and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAWEC_API_KEY and sends Amazon product URLs or ASIN and region values to Clawec.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
