## Description: <br>
Use this skill when the user wants to create visualizations, analyze spreadsheet data, or generate reports with ChartGen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask ChartGen to create charts, dashboards, diagrams, PowerPoint slides, and analysis reports from text prompts or supported spreadsheet files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed prompts and selected spreadsheet files are sent to ChartGen's cloud service for processing. <br>
Mitigation: Use the skill only when ChartGen's terms and privacy practices are acceptable, and avoid uploading confidential or regulated spreadsheets unless approved. <br>
Risk: A CHARTGEN_API_URL override can route requests to a non-default service endpoint. <br>
Mitigation: Verify any CHARTGEN_API_URL override before use and prefer a dedicated ChartGen API key. <br>


## Reference(s): <br>
- [Chart AI on ClawHub](https://clawhub.ai/chartgen-ai/chartai) <br>
- [ChartGen skill homepage](https://github.com/chartgen-ai/chartgen-skill) <br>
- [ChartGen API setup](https://chartgen.ai/chat) <br>
- [Skill upgrade procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown reports with JSON tool results, local image or PPT artifact paths, and edit links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; supported uploads are CSV, XLS, XLSX, and TSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
