## Description:

Uses the ClawEC API to run Amazon product research by marketplace, month, category, keyword, and fastMode, with optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to research product opportunities, review top products and metrics, and optionally request AI analysis for product-selection decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon product-research queries and the CLAWEC_API_KEY are sent to ClawEC when the API scripts are used.

Mitigation: Use a dedicated API key when possible, keep it in the CLAWEC_API_KEY environment variable, and avoid submitting highly sensitive proprietary search terms unless appropriate.

Risk: Optional AI interpretation is asynchronous and may fail or time out while product data is still available.

Mitigation: Poll log details within the documented attempt limit, report timeout or failure clearly, and return the raw product-research data when AI analysis is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-product-research)
- [ClawEC API Base URL](https://www.clawec.com/api)
- [ClawEC API Key Page](https://www.clawec.com/api-key?source=q-clawhub)
- [Product Research Search Endpoint](https://www.clawec.com/api/aigc/ec/amazon/product_research/search)
- [Product Research Logs Endpoint](https://www.clawec.com/api/aigc/ec/amazon/product_research/search/logs)
- [Product Research Log Detail Endpoint](https://www.clawec.com/api/aigc/ec/amazon/product_research/search/log/detail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs Chinese summaries of search conditions, top products, metrics, and optional AI analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
