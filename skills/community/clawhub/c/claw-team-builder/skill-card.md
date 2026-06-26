## Description: <br>
Agent Team 构建器通过多轮交互澄清需求，并为 OpenClaw 自动创建 Agent 配置、工作空间和 Bootstrap 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8421bit](https://clawhub.ai/user/8421bit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to plan multi-agent setups, detect configuration conflicts, create agent workspaces and bootstrap files, and update OpenClaw routing after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently edit global OpenClaw configuration and create agent files. <br>
Mitigation: Review generated configuration changes before applying them, use simple safe agent IDs, and keep backups before modifying OpenClaw state. <br>
Risk: Config backups and channel settings may expose sensitive local or account information. <br>
Mitigation: Protect OpenClaw configuration backups and restrict channel allow-lists instead of accepting broad routing access. <br>
Risk: Mutating repair or restart commands can change the local OpenClaw environment. <br>
Mitigation: Run `openclaw doctor --fix` or gateway restart only when local OpenClaw changes are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/8421bit/claw-team-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration snippets, generated files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw configuration, workspaces, bootstrap files, and validation commands after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
