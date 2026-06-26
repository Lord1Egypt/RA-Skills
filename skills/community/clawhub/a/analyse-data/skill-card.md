## Description: <br>
Use this skill to confirm and submit ChartGen requests for data analysis, charts, dashboards, diagrams, presentations, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to route spreadsheet or text analysis requests through ChartGen, then receive summarized insights and generated visual or document artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends confirmed prompts and selected spreadsheet files to ChartGen as an external cloud processor. <br>
Mitigation: Review each confirmation prompt and avoid uploading spreadsheets or prompts that cannot be shared with ChartGen. <br>
Risk: The skill requires a sensitive ChartGen API key. <br>
Mitigation: Use a dedicated ChartGen API key and do not expose it in prompts, logs, or generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chartgen-ai/analyse-data) <br>
- [ChartGen API setup](https://chartgen.ai/chat) <br>
- [ChartGen service](https://chartgen.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON result summaries, and local artifact file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >= 14 and CHARTGEN_API_KEY; supported uploads are CSV, TSV, XLS, and XLSX files.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
