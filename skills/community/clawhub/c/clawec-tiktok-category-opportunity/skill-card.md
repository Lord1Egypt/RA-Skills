## Description:

This skill uses the ClawEC API to analyze TikTok category and keyword opportunities, including opportunity score, creator trend, 30-day sales metrics, and radar-style multidimensional scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border ecommerce operators, category researchers, and agents use this skill to evaluate TikTok product category opportunities by keyword and region. It helps compare opportunity scores, creator activity trends, recent sales performance, and market radar dimensions before prioritizing categories or keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, selected TikTok region, table preference, and the ClawEC bearer token are sent to clawec.com during API calls.

Mitigation: Use a dedicated ClawEC API key, rotate it normally, and avoid submitting sensitive private data as analysis keywords.

Risk: API calls may consume ClawEC points or incur usage cost, especially when table output is enabled.

Mitigation: Review API costs or point usage before enabling table output and choose table=0 unless structured table data is needed.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-tiktok-category-opportunity)
- [Publisher profile](https://clawhub.ai/user/anyunzhong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese opportunity-analysis summaries by default; may include ranked keyword tables, trend interpretation, radar score breakdowns, and API error guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
