## Description:

Curates reader-facing, citation-backed Markdown appendix tables for survey papers from in-scope evidence artifacts and existing BibTeX keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research writers, and survey-paper contributors use this skill to turn existing C4 evidence artifacts into publishable appendix tables. It is intended for workspaces that already contain evidence packs, anchor sheets, and citation keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom output paths can write outside the intended workspace.

Mitigation: Restrict --outputs to expected workspace-relative paths, run the skill in an isolated workspace, and review output locations before execution.

Risk: Bundled workflow tooling is broader than the appendix-table task.

Mitigation: Review or remove bundled pipeline, executor, and ideation tooling when only appendix-table generation is needed.

Risk: Generated tables can misrepresent sources if upstream evidence or citation keys are incomplete.

Mitigation: Require every row to cite keys present in citations/ref.bib and review table rows against the evidence packs and anchor sheet.

## Reference(s):

- [Appendix Table Writer on ClawHub](https://clawhub.ai/willoscar/skills/appendix-table-writer)
- [Table Cell Hygiene](references/table_cell_hygiene.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown appendix tables and a Markdown validation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outline/tables_appendix.md and output/TABLES_APPENDIX_REPORT.md in the target workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
