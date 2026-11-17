## Description:

Uses the ClawEC API to retrieve Amazon Best Sellers rankings by category for bestseller, category hot-sale, and competitor research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, marketplace researchers, and agent developers use this skill to query Amazon Best Sellers data through ClawEC, optionally filtered by a documented category allowlist, and summarize ranking results for product selection or competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party ClawEC API key and sends the selected Amazon category value to clawec.com.

Mitigation: Set CLAWEC_API_KEY in the environment instead of pasting or hardcoding it, and disclose the third-party API call before use.

Risk: Invalid category names can cause failed or misleading requests.

Mitigation: Validate category names against the documented allowlist and fall back to the all-category query only when a user category cannot be mapped.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-best-seller)
- [ClawEC API base URL](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown summary with optional tables and raw JSON-derived fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the ClawEC API response shape; the artifact advises expanding nested product lists and preserving available ranking fields.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
