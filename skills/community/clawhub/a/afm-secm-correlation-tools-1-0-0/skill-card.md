## Description: <br>
Analyzes and correlates AFM topography and SECM activity data to identify microscale structure-activity relationships in electrocatalysis research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrayxiaoruiyang-pixel](https://clawhub.ai/user/xrayxiaoruiyang-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and technical users use this skill to run local AFM-SECM correlation analyses, compare surface morphology with electrochemical activity, and generate figures, tables, and reports for electrocatalysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreadable AFM or SECM inputs may be silently replaced with synthetic data, producing plausible research outputs. <br>
Mitigation: Audit or modify fallback paths so unreadable inputs fail with a clear error; allow synthetic data only through an explicit demo mode and label demo outputs in plots, reports, CSV, and JSON. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/xrayxiaoruiyang-pixel/afm-secm-correlation-tools-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash examples and local analysis outputs including PNG, CSV, JSON, and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against AFM and SECM input files; results depend on input parsing and preprocessing choices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
