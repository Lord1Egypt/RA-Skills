## Description:

Extract quantities from BIM/CAD data for cost estimation. Group by type, level, zone. Generate QTO reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction estimators, BIM coordinators, and project engineers use this skill to process BIM/CAD exports, group quantities by type, category, and level, and prepare quantity takeoff summaries for cost estimation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has filesystem access for BIM input files and generated report outputs.

Mitigation: Use intended project paths only, review output locations before export, and avoid overwriting important files.

Risk: Spreadsheet reports generated from untrusted BIM/CAD exports may include links, formulas, or external content that spreadsheet applications warn about.

Mitigation: Treat generated spreadsheets from untrusted inputs cautiously and do not enable links, formulas, or external content unless the source is trusted.

## Reference(s):

- [Data Driven Construction homepage](https://datadrivenconstruction.io)
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/bim-qto)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Structured Markdown tables, Python snippets, and optional Excel, CSV, or JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report exports when the user provides an intended output path.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
