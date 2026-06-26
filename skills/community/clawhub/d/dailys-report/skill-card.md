## Description: <br>
Daily report generator that summarizes today's tasks from OpenClaw memory notes or user input and generates formatted daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youyancheng1](https://clawhub.ai/user/youyancheng1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and OpenClaw users can use this skill to turn dated memory notes or manually supplied task lists into daily work reports for review, sharing, or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain sensitive work details from dated OpenClaw memory notes. <br>
Mitigation: Review generated reports before sharing them and avoid writing sensitive reports to Desktop or synced folders unless that is intended. <br>
Risk: Word export requires installing the python-docx dependency. <br>
Mitigation: Install python-docx only from a trusted package source when .docx output is needed. <br>


## Reference(s): <br>
- [Daily Report Workflows](references/workflows.md) <br>
- [Daily Report Config Schema](references/config-schema.json) <br>
- [ClawHub skill page](https://clawhub.ai/youyancheng1/dailys-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text, Markdown, or Word report files, with shell command examples and JSON configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports date selection, optional statistics, configurable output paths, and optional python-docx dependency for Word export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
