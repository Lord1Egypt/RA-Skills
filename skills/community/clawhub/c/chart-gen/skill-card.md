## Description: <br>
Creates ChartGen-backed visualizations, dashboards, diagrams, reports, PPTs, and data analyses from text prompts or spreadsheet files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to confirm a ChartGen request, submit prompts or spreadsheet files, poll for completion, and receive chart, report, PPT, or data-file artifacts with edit links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected spreadsheet files are sent to ChartGen as an external processor. <br>
Mitigation: Avoid confidential, regulated, or third-party data unless approved, and submit only after explicit user confirmation. <br>
Risk: The ChartGen API key or an overridden API URL could be mishandled. <br>
Mitigation: Keep CHARTGEN_API_KEY private and verify any CHARTGEN_API_URL override before use. <br>


## Reference(s): <br>
- [Chart Generator on ClawHub](https://clawhub.ai/chartgen-ai/chart-gen) <br>
- [ChartGen](https://chartgen.ai) <br>
- [ChartGen API setup](https://chartgen.ai/chat) <br>
- [Skill upgrade procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with Node.js command invocations and JSON task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local chart images, PPT files, spreadsheets, and ChartGen edit URLs after confirmed external processing.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence and tool version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
