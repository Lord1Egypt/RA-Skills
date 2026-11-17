## Description:

Builds DVSA/Traffic Commissioner "show me" audit readiness checklists and evidence indexes for operator licence scrutiny.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

External compliance, transport operations, and fleet teams use this skill to prepare practical DVSA, Traffic Commissioner, or customer audit readiness materials for a specified depot, operating centre, fleet, and review period.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Generated audit readiness materials may be incomplete or misleading if the audit type, depot or fleet scope, review period, or internal policy text is missing.

Mitigation: Ask for the required audit context before generating artifacts, use user-provided policies where relevant, and mark unknown sources or owners as gaps for confirmation.

Risk: Users may treat operational checklist content as legal advice or as a source of retention duties.

Mitigation: Do not invent legal duties or retention periods; request precise records and internal policy text when legal status or retention rules are in scope.

## Reference(s):

- [Operator licence sensitivity placeholders](artifact/references/operator-licence-sensitivity-placeholders.md)
- [DVSA/TC show me checklist template](artifact/assets/dvsa-visit-today-checklist-template.md)
- [Audit evidence index template](artifact/assets/audit-evidence-index-template.md)
- [Gaps register template](artifact/assets/gaps-register-template.md)
- [ClawHub skill page](https://clawhub.ai/kowl64/skills/dvsa-tc-audit-readiness-operator-licence-uk)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files and Excel-ready Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a DVSA visit checklist, audit evidence index, and gaps register; marks unknown evidence as gaps for user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
