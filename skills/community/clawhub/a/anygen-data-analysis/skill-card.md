## Description: <br>
Data Analysis uses the AnyGen CLI to analyze datasets and create charts, dashboards, reports, and other visualizations through AnyGen's server-side service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill when an agent needs to analyze business, financial, product, experiment, or CSV-style data and produce summaries, charts, dashboards, or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Datasets may be sent to AnyGen's remote service for analysis. <br>
Mitigation: Use only datasets that the user is authorized to send to AnyGen and avoid sensitive, regulated, or confidential data unless that transfer is approved. <br>
Risk: The skill depends on an AnyGen API key. <br>
Mitigation: Keep API keys in environment variables or approved secret stores and avoid placing keys in prompts, chat logs, or shared files. <br>
Risk: The artifact tells the agent to install an additional anygen-workflow-generate skill if it is missing. <br>
Mitigation: Review and approve that dependency before allowing installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/logictortoise/anygen-data-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/logictortoise) <br>
- [AnyGen website](https://www.anygen.io) <br>
- [AnyGen CLI package](https://www.npmjs.com/package/@anygen/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce analysis guidance and visualization/report instructions that rely on AnyGen CLI execution.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
