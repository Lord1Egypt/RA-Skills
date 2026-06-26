## Description: <br>
Generates and reviews QZTC course objective achievement analysis reports from Excel grade files and DOCX templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alukardo](https://clawhub.ai/user/alukardo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QZTC staff and education workflow maintainers use this skill to generate course objective achievement reports from trusted grade spreadsheets, then review generated DOCX output for placeholder replacement, tables, charts, and analysis paragraphs. <br>

### Deployment Geography for Use: <br>
Global; intended for QZTC internal workflows. <br>

## Known Risks and Mitigations: <br>
Risk: Student-grade spreadsheets and generated reports may contain sensitive educational data. <br>
Mitigation: Run the skill only on trusted QZTC inputs and protect both source spreadsheets and generated DOCX reports according to local data-handling rules. <br>
Risk: An incorrect TEMPLATE_DIR can cause the generator to use the wrong local DOCX template. <br>
Mitigation: Review config.env before generation and confirm TEMPLATE_DIR points to the intended course template directory. <br>


## Reference(s): <br>
- [Grading formula reference](references/grading-formula.md) <br>
- [ClawHub skill page](https://clawhub.ai/alukardo/achievement-qztc) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are DOCX reports and structured review status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted Excel grade files and local DOCX templates configured through config.env.] <br>

## Skill Version(s): <br>
5.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
