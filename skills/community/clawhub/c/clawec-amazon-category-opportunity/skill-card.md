## Description:

Uses the ClawEC API to analyze Amazon category and keyword opportunities, including opportunity scores, search ranking trends, 30-day sales and revenue signals, and radar-style multidimensional scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agent users use this skill to evaluate Amazon keyword and category opportunities across supported regional marketplaces. It helps summarize opportunity rankings, trend movement, sales signals, and radar score strengths or weaknesses in a Chinese analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search keywords, Amazon region, table option, and the ClawEC bearer token to clawec.com.

Mitigation: Use a dedicated ClawEC API key, avoid confidential product terms, and run the skill only when external ClawEC API processing is acceptable.

Risk: The helper script executes a curl request with the provided keyword and credentials.

Mitigation: Review the generated curl command or scripts/analyze.sh before running it, and keep CLAWEC_API_KEY in the environment rather than hardcoding it.

Risk: Opportunity scores and trends are third-party ecommerce analysis signals and may not be sufficient for final business decisions.

Mitigation: Treat the report as decision support and compare recommendations with marketplace data, supply constraints, and product economics before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-category-opportunity)
- [Amazon category opportunity response schema](references/response-schema.md)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC product search v2 endpoint](https://www.clawec.com/api/aigc/ec/product_search_v2)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables and concise Chinese narrative; may include shell commands or raw JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses keyword, Amazon region, and optional table flag; reports are sorted and interpreted from the returned keywordList.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
