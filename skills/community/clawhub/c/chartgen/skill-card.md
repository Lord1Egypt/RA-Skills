## Description: <br>
Use this skill when the user wants to create visualizations, dashboards, diagrams, Gantt charts, PPTs, data analysis, or reports with ChartGen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use ChartGen to submit confirmed data visualization, spreadsheet analysis, report, dashboard, diagram, and presentation requests to the ChartGen service, then return generated text and artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed prompts and selected spreadsheet data are sent to the external ChartGen service for processing. <br>
Mitigation: Use the skill only with data that may be shared with ChartGen, and avoid sensitive or regulated data unless your policy permits it. <br>
Risk: The helper uses a ChartGen API key and can read it from environment or local config files. <br>
Mitigation: Use a ChartGen-specific API key, keep it out of chat transcripts and logs, and rotate it if exposure is suspected. <br>
Risk: A CHARTGEN_API_URL override can redirect API calls and result downloads to a different endpoint. <br>
Mitigation: Allow overrides only to trusted ChartGen-compatible endpoints and review endpoint configuration before deployment. <br>


## Reference(s): <br>
- [ChartGen Skill on ClawHub](https://clawhub.ai/chartgen-ai/chartgen) <br>
- [ChartGen Skill Homepage](https://github.com/chartgen-ai/chartgen-skill) <br>
- [ChartGen API Access](https://chartgen.ai/chat) <br>
- [Skill Upgrade Procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON tool results and local artifact file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce chart images, dashboards, PPT previews, PPTX files, spreadsheet/file downloads, edit URLs, and concise analysis summaries.] <br>

## Skill Version(s): <br>
1.0.22 (source: server release evidence and tool version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
