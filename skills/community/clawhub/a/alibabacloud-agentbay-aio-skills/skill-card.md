## Description: <br>
Execute code in a secure cloud sandbox via AgentBay SDK for Python, JavaScript, R, and Java code execution, plotting, scripts, and data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route code execution requests through Alibaba Cloud AgentBay rather than running untrusted code locally. It supports code evaluation, scripts, data analysis, and chart generation with structured output handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code and data submitted for execution are sent to the AgentBay cloud sandbox. <br>
Mitigation: Avoid running code that contains secrets or private data, and install the skill only when that cloud execution model is acceptable. <br>
Risk: The skill requires an AgentBay API key stored locally or supplied through an environment variable. <br>
Mitigation: Store the API key only in the documented config path or environment variable, and do not expose credential values in conversation replies or output files. <br>
Risk: Generated charts or images can be written as local files in the current directory. <br>
Mitigation: Use JSON mode for file extraction and verify generated files before reporting success. <br>


## Reference(s): <br>
- [AgentBay Console](https://agentbay.console.aliyun.com/service-management) <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-agentbay-aio-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local chart/image files from sandbox results; JSON mode returns success, result, logs, and error_message fields.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
