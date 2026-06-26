## Description: <br>
This skill installs and configures the Tablestore Mem0 plugin for OpenClaw, using Alibaba Cloud Tablestore as a persistent vector store backend for AI agent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw long-term memory to Alibaba Cloud Tablestore, install the required plugin, configure OpenClaw, and verify that the memory backend loads correctly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may provision a new Alibaba Cloud Tablestore instance and incur cloud charges. <br>
Mitigation: Require explicit confirmation before creating an instance and have the user verify existing resources in the Tablestore console. <br>
Risk: The setup asks for broad Tablestore control and may enable public internet access when a VPC endpoint is unreachable. <br>
Mitigation: Prefer an ECS RAM role or custom least-privilege RAM policy, and require explicit approval before any public internet exposure. <br>
Risk: The workflow handles cloud credentials and an external npm package. <br>
Mitigation: Use environment variables instead of pasting long-lived secrets into chat, verify the npm package separately, and request consent before installation. <br>


## Reference(s): <br>
- [RAM Permissions Declaration](references/ram-policies.md) <br>
- [Alibaba Cloud ECS RAM Role Documentation](https://help.aliyun.com/zh/ecs/user-guide/attach-an-instance-ram-role-to-an-ecs-instance) <br>
- [Alibaba Cloud Tablestore RAM Access Reference](https://help.aliyun.com/zh/tablestore/developer-reference/access-tablestore-by-ram-user) <br>
- [Tablestore OpenClaw Mem0 npm Package](https://registry.npmjs.org/@tablestore%2fopenclaw-mem0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user confirmation prompts for external package installation and cloud resource provisioning.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
