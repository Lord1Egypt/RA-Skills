## Description:

成本与存货专家 routes pasted Chinese business and accounting tables to one of 24 local cost and inventory checks, then returns row-level conclusions with source-line support or reports the missing columns needed before drawing a conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Business, finance, accounting, and operations users use this skill to check pasted cost and inventory tables across cash counts, inventory counts, cost allocation, cutoff testing, provisions, scrap approvals, and related controls. It is intended to support review by surfacing reproducible findings and missing inputs, not to replace professional accounting, tax, legal, or audit judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance, tax, approval, and allocation conclusions may be mistaken for final professional advice.

Mitigation: Treat results as review prompts and require qualified human review before accounting, tax, legal, audit, or operational decisions.

Risk: The package keeps a local use counter and stops after five runs.

Mitigation: Install only where this local state and trial limit are acceptable, and document the behavior for users before deployment.

Risk: The skill operates on Chinese-language business and accounting tables and may fail or withhold conclusions when headers or required columns are absent.

Mitigation: Provide complete table headers and required fields, review any missing-column messages, and avoid relying on a pass result as proof that no issue exists outside the executed checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-cost-inventory-pub)
- [Skill source: SKILL.md](artifact/SKILL.md)
- [Sub-skill manifest](artifact/scripts/engine/expert-manifest.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON returned from command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may list unexecuted checks when required parameters are missing; local trial usage is counted on the user's machine.]

## Skill Version(s):

1.0.11 (source: server release evidence; artifact frontmatter is 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
