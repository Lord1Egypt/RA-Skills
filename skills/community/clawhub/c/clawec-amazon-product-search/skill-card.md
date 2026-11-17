## Description:

This skill searches Amazon products through the ClawEC API across supported marketplace regions and returns product price, sales, rating, review, and link data for product research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to search Amazon marketplaces and compare products for product sourcing, keyword research, and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon search keywords, selected region, and a Clawec API token are sent to Clawec when the API is called.

Mitigation: Use the skill only when sharing those values with Clawec is acceptable, and prefer a restricted Clawec API key.

Risk: The shell helper uses the API token in a curl command, which can be exposed through process inspection or command-line logs on shared systems.

Mitigation: Run the helper only in controlled environments, avoid shared systems for token-bearing commands, and rotate the key if command-line logs may have captured it.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawEC API base URL](https://www.clawec.com/api)
- [Amazon product search endpoint](https://www.clawec.com/api/aigc/tool/amazon_product_search)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-product-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and tables; JSON from the shell helper/API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default summaries are in Chinese and may include product count, target region, comparison tables, sorting, and 2-3 observations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
