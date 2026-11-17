## Description:

A local checker for food-additive dosing and usage ledgers that runs six disclosed checks: usage ratio against recorded limits, inconsistent limit values, ingredient-label alignment, duplicate dosing rows, total recomputation, and invalid or missing fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Food production quality, production, and compliance teams use this skill to review copied ledger rows for additive dosing, label-record consistency, duplicate rows, totals, and field validity before internal checks, audits, or inspections. It reports only when the supplied table has enough material and cites source rows and batches for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food-safety or regulatory conclusions could be incomplete if users rely on the checker instead of the current GB 2760 standard or qualified review.

Mitigation: Use the output as a ledger review aid only, and independently verify conclusions against the current GB 2760 standard and qualified food-safety review.

Risk: The free version explicitly does not run advanced checks such as out-of-scope use, compound additive split calculations, carry-in principles, relative total over 100%, or grouped remediation summaries.

Mitigation: Treat the result as limited to the six disclosed checks and review omitted checks before relying on the output for audit or regulatory decisions.

Risk: Chinese-language documentation and output may be misread by reviewers who do not understand the source language.

Mitigation: Have Chinese-capable reviewers inspect inputs, findings, and any cited ledger rows before acting on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/food-additive-usage-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or structured JSON, with findings that cite source rows and batches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; materials are not sent over the network according to the artifact and security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
