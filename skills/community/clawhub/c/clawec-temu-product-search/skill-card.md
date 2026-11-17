## Description:

Searches Temu products through the Clawec API and returns price, sales, rating, market, links, images, and related product data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, ecommerce operators, and sourcing researchers use this skill to search Temu products by keyword and compare returned product data for sourcing, product research, and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temu search keywords are sent to Clawec and may reveal sourcing intent or proprietary product research.

Mitigation: Use only search terms approved for Clawec, and avoid confidential product plans, customer names, or proprietary sourcing terms unless Clawec is approved for that data.

Risk: The skill requires a user-supplied Clawec API key.

Mitigation: Store the key in CLAWEC_API_KEY, do not hard-code it, and rotate it if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-temu-product-search)
- [Temu product search response schema](references/response-schema.md)
- [Clawec API base URL](https://www.clawec.com/api)

## Skill Output:

**Output Type(s):** [API calls, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and tables, with optional shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied Clawec API key and a keyword search term.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
