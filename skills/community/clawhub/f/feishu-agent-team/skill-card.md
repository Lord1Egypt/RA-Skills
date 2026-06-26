## Description: <br>
Feishu Agent Team helps OpenClaw users route Feishu group @mentions from a coordinator to configurable specialist agents for multi-agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to configure an OpenClaw coordinator that accepts Feishu group tasks, routes them by keyword to specialist agents, and tests team routing from the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Feishu group messages may be processed by multiple agents and routed beyond the original coordinator context. <br>
Mitigation: Limit enabled Feishu groups and specialist agents to the intended workspace, review routing keywords before deployment, and avoid sending secrets or sensitive content in routed chats. <br>
Risk: Group chat content may be retained in checkpoints or logs depending on the deployment configuration. <br>
Mitigation: Review retention and redaction controls before broad use, and keep checkpoint storage scoped to approved environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mars82311111/feishu-agent-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline YAML, JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces configuration and routing guidance for OpenClaw and Feishu multi-agent team setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
