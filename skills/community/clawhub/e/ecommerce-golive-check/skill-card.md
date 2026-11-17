## Description:

Orchestrates specialist skills into an evidence-based, blocking go-live checklist for ecommerce stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Store owners and developers use this skill to assess ecommerce launch readiness across transactions, order handling, compliance, consent, conversion, responsive behavior, SEO, and release hygiene. It records evidence in a blocking pass/fail gate and is not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gate may approve a launch with incomplete checks, and testing boundaries for real orders are unclear.

Mitigation: Independently verify every required check and waiver; use an isolated test store, payment-provider test mode, and a controlled inbox, and explicitly approve any production testing.

## Reference(s):

- [Block Catalog](artifact/references/block-catalog.md)
- [Gate Schema](artifact/references/gate-schema.md)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown gate with a summary table, blocking verdict, remediation list, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pass/fail status and evidence for checklist items; unavailable specialist skills are surfaced as needs-skill.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
