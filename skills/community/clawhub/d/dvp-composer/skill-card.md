## Description:

Guides users through a structured clinical trial Data Validation Plan workflow, from study material collection through check design, internal review, and Excel DVP generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unfallenwill](https://clawhub.ai/user/unfallenwill)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical data management teams, CRO staff, sponsors, and developers use this skill to draft and review Data Validation Plans for clinical studies. It helps collect study inputs, define validation scope, design executable check rules, align them against source materials, and produce a final Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite project files in dvp_workspace.

Mitigation: Keep backups of existing DVP work and review workspace contents before continuing a workflow.

Risk: Generated Excel workbooks may include content derived from untrusted study materials or templates.

Mitigation: Use trusted source materials and inspect generated XLSX files for unexpected formulas or links before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/unfallenwill/skills/dvp-composer)
- [Excel Output Specification](references/excel-spec.md)
- [DVP Document Structure Catalog](references/section-catalog.md)
- [Example DVP Output](references/example-output.md)
- [Phase 1: Collection](references/stages/phase-1-collection.md)
- [Phase 2: Scope & Strategy](references/stages/phase-2-strategy.md)
- [Phase 3: Design Check Content](references/stages/phase-3-design.md)
- [Phase 4: Alignment](references/stages/phase-4-alignment.md)
- [Phase 5: Draft](references/stages/phase-5-draft.md)
- [Phase 6: Internal Review](references/stages/phase-6-review.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Excel workbook, Shell commands, Guidance]

**Output Format:** [Markdown phase deliverables, JSON workbook input, structured review text, and .xlsx final DVP files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes workflow files under dvp_workspace and can generate DVP_<ProtocolNumber>_v1.0.xlsx from JSON input or a user-provided Excel template.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
