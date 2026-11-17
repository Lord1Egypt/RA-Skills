## Description:

Checks equipment maintenance ledgers and spare-part issue records for labor fees, spare-part amounts, monthly maintenance budget comparisons, total-row consistency, duplicate rows, missing fields, and negative values, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, property-management, and logistics equipment teams can use this skill before monthly close to check maintenance and spare-part ledgers for arithmetic, completeness, duplicate-row, and budget issues. It supports local review of exported text or JSON table data and reports insufficient input instead of claiming a clean result when required columns are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete maintenance-cost audit.

Mitigation: Review the listed checks not run before relying on the result; warranty-charge, outsource-over-quote, and over-issue decisions require separate review.

Risk: Ledger data may be incomplete, malformed, or exported without required headers.

Mitigation: Export the source table to text or JSON with headers and review any insufficient-input or missing-column report before drawing conclusions.

Risk: The checker does not verify external business facts such as warranty periods, contract terms, or reasonableness of labor and part prices.

Mitigation: Confirm warranty status, contract coverage, and pricing assumptions against authoritative business records outside the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenqg618/skills/equipment-maintenance-cost-check-free)
- [ClawHub Publisher Profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing findings, summaries, missing-input guidance, and source-row citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; sample mode can be used to inspect the executed checks.]

## Skill Version(s):

1.0.53 (source: evidence.json release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
