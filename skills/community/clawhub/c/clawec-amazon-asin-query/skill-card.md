## Description:

Clawec Amazon ASIN Query calls the Clawec API to look up Amazon product details from an ASIN or product URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to retrieve Amazon product-detail data for item research, competitor analysis, and product URL parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product URLs or ASINs and the selected region are sent to Clawec's API.

Mitigation: Avoid sensitive account-specific URLs and confirm the user is comfortable sending the query to Clawec before use.

Risk: The skill requires a user-provided CLAWEC_API_KEY to authenticate requests.

Mitigation: Read the key from the environment or ask the user for it at runtime; do not hard-code or store it in skill files.

Risk: Clawec returns dynamic product-detail fields that may vary by item or region.

Mitigation: Inspect the returned data object and avoid assuming a fixed response schema when summarizing results.

## Reference(s):

- [Amazon ASIN query response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-asin-query)
- [Clawec API base URL](https://www.clawec.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summaries with optional shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product detail fields are dynamic and should be displayed according to the Clawec API response.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
