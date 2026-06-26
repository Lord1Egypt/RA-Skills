## Description: <br>
Chart Generator Pro helps agents create visualizations, analyze spreadsheet data, and generate reports or PPTs through ChartGen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to ask an agent to submit confirmed charting, dashboard, diagram, spreadsheet-analysis, report, and PPT requests to ChartGen and return the generated artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed prompts and selected spreadsheet contents are sent to ChartGen for processing. <br>
Mitigation: Submit only data approved for ChartGen processing, avoid confidential or regulated data unless authorized, and keep the skill's confirmation step before any request. <br>
Risk: The skill depends on an API key for access to ChartGen. <br>
Mitigation: Use a dedicated revocable CHARTGEN_API_KEY and avoid exposing it in messages, logs, or generated artifacts. <br>
Risk: Changing CHARTGEN_API_URL can redirect requests and uploaded files to a different endpoint. <br>
Mitigation: Leave CHARTGEN_API_URL unset unless the deployment intentionally trusts the alternate endpoint. <br>


## Reference(s): <br>
- [ClawHub Chart Generator Pro skill page](https://clawhub.ai/chartgen-ai/chart-generator-pro) <br>
- [ChartGen chat and API key setup](https://chartgen.ai/chat) <br>
- [Skill upgrade procedure](references/upgrade-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus JSON tool responses that may reference saved image, PPT, Excel, or file artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include ChartGen text summaries, edit URLs, local image paths, PPT preview paths, and downloadable file paths after task polling completes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
