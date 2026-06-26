## Description: <br>
Uses ChartGen to create visualizations, analyze spreadsheet or text data, and generate reports or PPT slides after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask ChartGen for charts, dashboards, diagrams, spreadsheet analysis, reports, and presentation outputs. The skill is suited for confirmed data-analysis and visualization requests where sending the selected prompt and files to ChartGen is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed prompts and selected spreadsheet files are sent to ChartGen under the user's API key. <br>
Mitigation: Review the confirmation text and file list before approving, and avoid submitting sensitive data unless ChartGen use is acceptable for the environment. <br>
Risk: Evidence.security reports that result downloads are not restricted to chartgen.ai-hosted URLs despite the stated chartgen.ai-only network boundary. <br>
Mitigation: Use extra caution on sensitive or locked-down networks, review downloaded artifacts before opening them, and prefer deployments that add host allowlisting and download limits. <br>


## Reference(s): <br>
- [ChartGen service](https://chartgen.ai) <br>
- [ChartGen API key page](https://chartgen.ai/chat) <br>
- [Skill upgrade procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown responses with JSON tool results, local image or file paths, and ChartGen edit links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; sends confirmed prompts and selected files to https://chartgen.ai.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and tool constant) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
