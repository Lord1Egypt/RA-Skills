## Description: <br>
Alibaba Cloud Yunxiao DevOps MCP Server provides code management, project management, pipeline, application delivery, artifact management, and test management capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangbowen521](https://clawhub.ai/user/huangbowen521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to discover and call Alibaba Cloud Yunxiao MCP tools for repositories, merge requests, projects, work items, pipelines, deployments, applications, artifacts, and tests. It supports command-line workflows with mcporter and a token-backed Yunxiao connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad token-backed access can modify repositories, work items, pipelines, deployments, resources, ownership, applications, and test assets. <br>
Mitigation: Use a minimally scoped YUNXIAO_ACCESS_TOKEN and restrict the agent to the organizations, projects, and repositories required for the task. <br>
Risk: Delete, deploy, pipeline-run, resource-member, validation, and ownership-change actions can cause operational or access-control changes. <br>
Mitigation: Require explicit human approval before those actions and review tool names and parameters before execution. <br>
Risk: Tokens passed in prompts or logged shell commands can be exposed. <br>
Mitigation: Provide tokens through a secure environment mechanism and avoid pasting real tokens into prompts, chat history, or shared command logs. <br>
Risk: The skill invokes an external npm MCP package. <br>
Mitigation: Install only if you trust the external npm MCP package and are comfortable giving an agent access to Alibaba Cloud Yunxiao. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huangbowen521/alibaba-devops) <br>
- [Alibaba Cloud Yunxiao product documentation](https://help.aliyun.com/product/153China) <br>
- [Alibaba Cloud Yunxiao API documentation](https://help.aliyun.com/document_detail/China) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable guidance for YUNXIAO_ACCESS_TOKEN and examples for mcporter commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
