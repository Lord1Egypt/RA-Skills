## Description:

Queries the ClawEC API for Ozon category hot-ranking data, including GMV, sales, price sorting, sell-through rate, commissions, and cross-border share.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers, ecommerce analysts, and agent operators use this skill to query Ozon category rankings and turn ClawEC API results into Chinese market-research and category-selection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a ClawEC API key and sends Ozon category query parameters to an external ClawEC API.

Mitigation: Set CLAWEC_API_KEY in a secure environment, do not hard-code it, and rotate the key if exposure is suspected.

Risk: Credentialed helper execution on shared hosts may expose credentials or query parameters through local process inspection or monitoring.

Mitigation: Run credentialed queries only in trusted environments and avoid shared machines for sensitive API use.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-ozon-category-hot-ranking)
- [ClawEC API base](https://www.clawec.com/api)
- [Ozon category hot-ranking endpoint](https://www.clawec.com/api/aigc/ec/ozon/data/category/hot-ranking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown report with optional shell command and API response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawEC API key and produces paginated Ozon category-ranking analysis from API results.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
