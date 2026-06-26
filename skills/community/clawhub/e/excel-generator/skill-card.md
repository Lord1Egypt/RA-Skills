## Description: <br>
Generates professional Bloomberg-style Excel workbooks from natural language descriptions, including multi-sheet dashboards, KPI cards, charts, conditional formatting, and data tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synapsefirm-cmd](https://clawhub.ai/user/synapsefirm-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and business users use this skill to turn natural language workbook requests into formatted Excel dashboards, trackers, reports, and business templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to use a public shared password for client files. <br>
Mitigation: Use a unique password supplied or approved by the user for each sensitive workbook. <br>
Risk: The skill directs agents to run an unbundled local generator script from a fixed path. <br>
Mitigation: Inspect and trust the referenced local script before use, or replace it with a reviewed script in the user's workspace. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/synapsefirm-cmd/excel-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [XLSX files with Markdown explanations and optional Python/openpyxl code or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create multi-sheet workbooks with dashboard, data, and raw-data sheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
