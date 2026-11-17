## Description:

费用与预算管控专家 routes pasted expense and budget table data to one of eight local checks and returns row-level, reproducible findings or missing-column notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, and business users can use this skill to check pasted expense, budget, reimbursement, shared-cost, software-license, travel-standard, and toll-fee tables. The skill routes by table headers, runs the matching local check, and reports line-level conclusions or the missing inputs needed before a conclusion can be made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be perceived as an unlimited free local tool, but running checks writes a local usage counter and enforces a five-use trial with a subscription prompt.

Mitigation: Review the trial behavior before installation and disclose the local usage counter and subscription gate to users.

Risk: Outputs are table-based checks and may be mistaken for audit, compliance, or financial assurance.

Mitigation: Treat results as review aids only, verify findings against source records, and have qualified personnel review any financial or compliance decisions.

Risk: Missing columns, ambiguous headers, or omitted parameters can leave checks unexecuted or prevent the skill from reaching a conclusion.

Mitigation: Provide complete table headers and required parameters, and review any missing-input or unexecuted-check messages before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-expense-budget-pub)
- [Artifact skill definition](artifact/SKILL.md)
- [Expert manifest](artifact/scripts/engine/expert-manifest.json)
- [Sample expense-budget input](artifact/templates/expense-budget-sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON with the selected sub-skill, sub-skill name, and check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on local table parsing and selected check rules; some checks may be skipped when required columns or parameters are missing.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
