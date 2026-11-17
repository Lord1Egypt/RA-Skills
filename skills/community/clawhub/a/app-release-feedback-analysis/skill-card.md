## Description:

Compare app review themes around documented releases using Crawlora version notes and live or stored reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams and developers use this skill to compare sampled App Store and Google Play review themes around documented releases and prepare a dated feedback brief with attribution limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App lookup terms, app IDs, review filters, and the API key are sent to Crawlora.

Mitigation: Confirm that the requested data can be shared with Crawlora and keep the API key private.

Risk: Review collection can consume more API credits than intended.

Mitigation: Set a bounded page count and credit budget before collecting reviews.

Risk: Sampled reviews may not represent all users or establish that a release caused a change.

Mitigation: Verify sampled reviews, disclose selection and attribution limits, and avoid causal claims.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/app-release-feedback-analysis)
- [Crawlora endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown feedback brief with release ledger, theme comparisons, and cited review excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review dates, sample sizes, version-attribution basis, missing data, and causal limitations.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
