## Description: <br>
Use this skill when the user wants to create visualizations, dashboards, diagrams, Gantt charts, PPTs, data analyses, or reports from natural-language requests or spreadsheet files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Chart AI to send confirmed visualization, spreadsheet analysis, report, or PPT generation requests to ChartGen and receive analysis text plus generated artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts and spreadsheet files are sent to the third-party ChartGen API. <br>
Mitigation: Use the skill only with data your policy allows to be shared with ChartGen, and avoid confidential or regulated data unless explicitly approved. <br>
Risk: API-returned artifacts can be downloaded and saved locally. <br>
Mitigation: Review generated artifact paths and contents before sharing or opening them in sensitive environments. <br>
Risk: The skill requires a ChartGen API key. <br>
Mitigation: Use a revocable API key and rotate or revoke it when access is no longer needed. <br>


## Reference(s): <br>
- [Chart AI ClawHub listing](https://clawhub.ai/chartgen-ai/chart-ai) <br>
- [ChartGen API key setup](https://chartgen.ai/chat) <br>
- [Skill Upgrade Procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, API Calls, Shell commands] <br>
**Output Format:** [Markdown text with JSON tool responses, local image/PPT artifact paths, and edit URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; supports CSV, XLS, XLSX, and TSV file inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
