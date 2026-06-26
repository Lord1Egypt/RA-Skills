## Description: <br>
Guides users through configuring a Feishu multi-agent system with batch agent creation, credential validation, role templates, and automatic backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create and configure multiple Feishu bot-backed agents, validate Feishu credentials, generate role templates, and update local OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secrets may be stored in local OpenClaw configuration and backup files. <br>
Mitigation: Use a test OpenClaw environment first, avoid entering production secrets in chat, and protect or delete configuration backups that contain secrets. <br>
Risk: Agent-to-agent permissions may broaden access and shared context across configured agents. <br>
Mitigation: Enable inter-agent communication only for agents that should share access and context, and review the resulting ~/.openclaw/openclaw.json before restart. <br>
Risk: User-provided agent IDs affect generated paths and configuration entries. <br>
Mitigation: Use simple safe agent IDs and inspect generated workspace, agent, and binding paths before relying on the configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/feishu-multi-agent-manager) <br>
- [Feishu Cloud Document Tutorial](https://www.feishu.cn/docx/PYlXdsZoEoPPDbxyBRWc9HpRnIe) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and generated OpenClaw configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write OpenClaw configuration, workspace, agent, backup, and role-template files during use.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
