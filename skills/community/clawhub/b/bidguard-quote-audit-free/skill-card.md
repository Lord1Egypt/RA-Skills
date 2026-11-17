## Description:

Audits a single bid quotation locally for line-item arithmetic errors and missing quantity, unit-price, or amount fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, bidding, and bid-preparation users use this skill to pre-check quote tables for mechanical arithmetic mismatches and missing line-item fields before submission. It is an aid for local self-review, not an official bid evaluation or scoring decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact's English description suggests broader checks than the free version actually performs.

Mitigation: Treat this release as limited to line-item arithmetic and missing quantity, unit-price, or amount fields unless later evidence aligns the docs and code.

Risk: Users may mistake the output for an official bid evaluation or scoring decision.

Mitigation: Use the results only as a local self-review aid and keep final bid evaluation with the responsible reviewers or committee.

Risk: Incomplete or poorly structured quote input can prevent meaningful checks.

Mitigation: Provide quote text or structured items containing quantity, unit price, and amount fields, and treat insufficient-input output as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bidguard-quote-audit-free)
- [Publisher profile: chenqg618](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON results from local quote-audit checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports checks performed, withheld checks, arithmetic discrepancies, missing fields, insufficient-input status, and local-execution notes.]

## Skill Version(s):

1.0.54 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
