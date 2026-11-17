## Description:

Use when the user wants a periodic authority and backlink report - referring-domain movement, pillar state, prospect pipeline - as a document, from link exports or TrustGrowth authority data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, SEO operators, and developers use this skill to produce periodic authority and backlink reports from link exports, link databases, or TrustGrowth authority data. It summarizes referring-domain movement, pillar state, prospect pipeline status, evidence labels, and next actions without inventing unavailable measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reporting workflow requires running an unbundled local Groundcrew validator from a dynamically located skills directory, which could execute unsafe code if that validator is replaced or untrusted.

Mitigation: Install and run the Groundcrew validator only from a trusted, protected location before allowing an agent to execute local commands.

Risk: The package references a provider-selection file that is not included, which may leave source selection behavior underspecified.

Mitigation: Use the bundled connector guidance and block or ask for review when source selection is unclear.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)
- [Groundcrew WHY-NOT-SLOP doctrine](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md)
- [Groundcrew ETHICS doctrine](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with evidence labels, verdict, measured table, next actions, evidence, and not-measured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SHIP, FIX, BLOCK, or UNDECIDED verdicts and labels facts as Measured, User-provided, or Estimated.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
