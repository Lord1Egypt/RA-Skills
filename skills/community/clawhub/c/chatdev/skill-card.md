## Description: <br>
Invoke ChatDev ability units through a local API to browse, inspect, run, and manage multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NA-Wen](https://clawhub.ai/user/NA-Wen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a trusted local ChatDev service, discover available ability units, run paper review or data visualization workflows, and manage workflow YAML or local function tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently upload, update, rename, copy, or delete ChatDev workflows and create or overwrite local tool code. <br>
Mitigation: Require explicit user approval before any write, delete, rename, copy, move, or overwrite action, and review generated YAML or code before sending it to the local service. <br>
Risk: Workflow runs and attachments may expose user data to the local ChatDev backend and its configured model provider. <br>
Mitigation: Use the skill only with a trusted local ChatDev service and avoid sensitive datasets unless the backend and model-provider data handling are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NA-Wen/chatdev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON API responses, YAML workflow templates, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow runs return a final_message when available and may also create output files in a local workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
