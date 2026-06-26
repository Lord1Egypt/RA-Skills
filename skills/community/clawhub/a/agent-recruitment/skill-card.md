## Description: <br>
智能体招聘技能。完整覆盖新Agent从需求确认、创建隔离工作区、模型配置、路由绑定到交付清单的全流程，适用于OpenClaw agent造册与HR管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usewild2026](https://clawhub.ai/user/usewild2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators and agent operations teams use this skill to collect requirements, create isolated agent workspaces, configure models, bind Feishu routes, and produce a delivery checklist for newly registered or updated agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent OpenClaw agent workspaces and retained memory. <br>
Mitigation: Review generated files under ~/.openclaw/agents and document how to disable routes and delete retained memory before deployment. <br>
Risk: The skill can bind Feishu group routes so every group message is routed to a bot. <br>
Mitigation: Require explicit approval for each group route and prefer @mention-only routing unless all participants expect full-message processing. <br>


## Reference(s): <br>
- [Agent Recruitment on ClawHub](https://clawhub.ai/usewild2026/agent-recruitment) <br>
- [Publisher profile: usewild2026](https://clawhub.ai/user/usewild2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and structured delivery checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe workspace paths, model identifiers, route bindings, and agent role boundaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
