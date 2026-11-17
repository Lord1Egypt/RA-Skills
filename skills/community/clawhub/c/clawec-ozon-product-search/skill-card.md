## Description:

Searches Ozon products through the ClawEC API and returns product prices, sales, ratings, market, links, and images for cross-border ecommerce research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, product researchers, and agent operators use this skill to search Ozon products and compare prices, sales, ratings, rankings, markets, links, and images for Russia and Eastern Europe product selection or competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to ClawEC and may reveal sensitive product plans or market research.

Mitigation: Use non-sensitive keywords unless approved, and review ClawEC service terms and data handling before sending confidential business information.

Risk: The skill requires a ClawEC API key for authenticated requests.

Mitigation: Read the key from the CLAWEC_API_KEY environment variable, do not hard-code it, and avoid exposing it in commands, logs, or files.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-ozon-product-search)
- [ClawEC API base URL](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown summaries and tables, with optional shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese summaries; output may include Ozon product names, prices, sales, ratings, rankings, markets, links, image URLs, and ClawEC point information.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
