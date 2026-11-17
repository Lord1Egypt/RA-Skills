## Description:

Analyzes Amazon subcategories through the ClawEC API, including market statistics and product, brand, and seller concentration, with optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to request ClawEC category research for selected marketplaces, category paths, and months, then review market metrics, concentration tables, and optional AI-generated interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends marketplace, category path, month, and analysis options to ClawEC using the user's API key.

Mitigation: Use the skill only when ClawEC's data-handling terms are acceptable, and avoid submitting proprietary category targets unless that sharing is approved.

Risk: The skill depends on a ClawEC API key for authenticated requests.

Mitigation: Read the key from the CLAWEC_API_KEY environment variable, avoid hardcoding it, and rotate the key if it is exposed.

Risk: Optional AI interpretation is asynchronous and can remain pending, fail, or time out.

Mitigation: Return the current status and raw category research data when AI interpretation is unavailable, and retry detail retrieval later if needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-category-research)
- [ClawEC API base URL](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional JSON API responses and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market statistics, concentration tables, response status fields, point usage, log IDs, AI status, and AI analysis when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
