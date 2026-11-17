## Description:

A Chinese-language local checker that recomputes certificate, licence, and special-equipment inspection ledger expiry dates and days-to-expiry, verifies status consistency, and flags reversed dates, non-positive cycles, duplicate certificate numbers, blanks, and unparseable values with source ledger line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, property, construction, and logistics compliance staff use this skill during monthly compliance checks and annual audits to verify copied certificate and special-equipment inspection ledger text. It helps identify arithmetic, date, status, duplicate-ID, blank-field, and parseability issues before renewal or inspection follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect direct spreadsheet ingestion, but this free release does not read .xlsx files.

Mitigation: Export or copy the ledger to text with headers, preferably tab-separated, or provide a JSON object with a text field.

Risk: Users may treat the output as legal or inspection authority advice.

Mitigation: Use the output only to check ledger arithmetic and internal consistency; confirm legal obligations, required inspection cycles, and equipment fitness with the applicable authority, certificate, or inspection report.

Risk: Users may assume the free version performs the full paid-tier review.

Mitigation: Review the checks_not_run list in the output; this release does not perform risk ranking, 30/60/90 day scheduling, missing inspection record checks, budget-difference checks, or treatment worklist generation.

Risk: Insufficient or malformed ledger input can prevent meaningful conclusions.

Mitigation: Provide the required columns, including a written inspection basis date, certificate or equipment name, certificate number, last inspection date, inspection cycle, expiry date, days to expiry, and status; the tool reports missing material instead of fabricating a result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/compliance-expiry-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or structured JSON containing executed checks, omitted checks, findings, source line references, scope notes, and disclaimers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on copied ledger text or a JSON object with a text field; does not read .xlsx directly and does not use network access.]

## Skill Version(s):

1.0.22 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
