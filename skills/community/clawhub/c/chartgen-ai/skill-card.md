## Description: <br>
ChartGen AI helps agents create visualizations, dashboards, diagrams, Gantt charts, presentations, data analyses, and reports from text prompts or spreadsheet files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to prepare charts, dashboards, presentation files, and analysis reports. It is useful when the agent needs to process a prompt or selected CSV, TSV, XLS, or XLSX files through ChartGen and return the resulting report and artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts and spreadsheet files may be sent to ChartGen for processing. <br>
Mitigation: Use a dedicated ChartGen API key, avoid regulated or confidential spreadsheets unless approved, and leave CHARTGEN_API_URL unchanged unless an alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chartgen-ai/chartgen-ai) <br>
- [ChartGen chat and API key setup](https://chartgen.ai/chat) <br>
- [ChartGen skill homepage](https://github.com/chartgen-ai/chartgen-skill) <br>
- [Upgrade procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports with JSON task status, local artifact paths, edit URLs, and optional image or PPT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; sends confirmed prompts and selected spreadsheet files to ChartGen for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
