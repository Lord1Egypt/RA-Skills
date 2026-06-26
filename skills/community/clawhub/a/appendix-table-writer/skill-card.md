## Description: <br>
Curates reader-facing appendix survey tables with concise layouts, citation-backed rows, and no invented facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate publishable appendix tables for survey or review work from existing evidence packs, anchor sheets, and citation keys. It is intended to produce compact Markdown tables suitable for downstream paper assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes broader research-pipeline files and runner code beyond the advertised appendix-table helper. <br>
Mitigation: Review the bundled workflow files before deployment, use the documented local table-generation path, and run it only in a workspace where changes to outline/, output/, UNITS.csv, STATUS.md, and DECISIONS.md are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/WILLOSCAR/appendix-table-writer) <br>
- [Table Cell Hygiene](references/table_cell_hygiene.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, guidance, shell commands] <br>
**Output Format:** [Markdown appendix tables and a Markdown validation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outline/tables_appendix.md and output/TABLES_APPENDIX_REPORT.md when run against a workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
