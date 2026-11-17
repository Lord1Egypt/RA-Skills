## Description:

环评报告知识库提炼工具 - 从环评报告表中提取结构化知识库文件，支持PDF/DOCX解析

This skill is ready for commercial/non-commercial use.

## Publisher:

[iasgu](https://clawhub.ai/user/iasgu)

### License/Terms of Use:

MIT-0

## Use Case:

Environmental consultants, analysts, and developers use this skill to parse Chinese environmental impact assessment report forms and generate structured knowledge-base files for pollutant factors, emission standards, and source-strength calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV files may contain formula-like cell values from untrusted reports.

Mitigation: Use a dedicated output directory and review or sanitize generated CSVs before opening them in spreadsheet software.

Risk: Dependencies are declared with lower bounds rather than pinned versions.

Mitigation: Use a reviewed lockfile or pinned dependency set before production deployment.

Risk: Some extraction modules are placeholders or documented as needing further optimization, so CSV completeness and accuracy can vary by report.

Mitigation: Review generated files against the source report and use the built-in validation report and processing summary before relying on the extracted data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iasgu/skills/eia-knowledge-extractor)
- [SKILL.md](artifact/SKILL.md)
- [requirements.txt](artifact/requirements.txt)
- [Example gas source CSV](artifact/reference/example_gas_source.csv)
- [Example water source CSV](artifact/reference/example_water_source.csv)
- [Example solid waste CSV](artifact/reference/example_solid_waste.csv)
- [Example noise source CSV](artifact/reference/example_noise_source.csv)
- [Example pollutant factor standard CSV](artifact/reference/example_pollutant_factor_standard.csv)
- [Example multi-project CSV](artifact/reference/example_multi_project.csv)

## Skill Output:

**Output Type(s):** [Files, CSV, Text, Shell commands, Guidance]

**Output Format:** [CSV knowledge-base files plus plain-text validation and processing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs to a user-selected local directory; expected CSV outputs cover pollutant factors, emission standards, gas, water, solid-waste, and noise source-strength records.]

## Skill Version(s):

2.3.0 (source: server release evidence; artifact frontmatter version 2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
