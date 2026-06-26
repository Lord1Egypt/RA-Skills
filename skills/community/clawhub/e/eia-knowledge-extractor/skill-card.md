## Description: <br>
环评报告知识库提炼工具 - 从环评报告表中提取结构化知识库文件，支持PDF/DOCX解析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iasgu](https://clawhub.ai/user/iasgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Environmental assessment practitioners and developers use this skill to convert EIA report forms in PDF, DOCX, DOC, or TXT format into structured knowledge-base files for pollutant factors, emission standards, and source-strength calculations. Generated outputs should be reviewed against the source report before reuse or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CSV and text files may contain sensitive project information from the input environmental report. <br>
Mitigation: Use a dedicated output folder, review generated files before sharing, and handle outputs according to the report's confidentiality requirements. <br>
Risk: Extracted environmental data may be incomplete or imperfect, especially when parsing report tables or source-strength calculations. <br>
Mitigation: Compare generated records with the original report and run the documented completeness and consistency checks before downstream use. <br>
Risk: Local output files can overwrite same-named files in the chosen output directory. <br>
Mitigation: Run the skill with a new or empty output directory for each report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iasgu/eia-knowledge-extractor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Example pollutant factor standard CSV](artifact/reference/example_pollutant_factor_standard.csv) <br>
- [Example gas source CSV](artifact/reference/example_gas_source.csv) <br>
- [Example water source CSV](artifact/reference/example_water_source.csv) <br>
- [Example solid waste CSV](artifact/reference/example_solid_waste.csv) <br>
- [Example noise source CSV](artifact/reference/example_noise_source.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Files, CSV, Text, Shell commands, Guidance] <br>
**Output Format:** [CSV knowledge-base files plus text validation and processing reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local output files from a user-provided report; review generated files because they may contain sensitive project information or imperfect extracted data.] <br>

## Skill Version(s): <br>
2.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
