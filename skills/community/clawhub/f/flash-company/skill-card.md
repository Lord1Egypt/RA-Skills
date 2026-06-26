## Description: <br>
临时虚拟公司 - 快速组建临时团队，即用即弃，轻量高效。无需预创建办公室，一个命令启动协作。支持预设团队和自定义配置。v1.1.0 新增记忆持久化系统。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to assemble short-lived role-based agent teams for development, content, business analysis, technical, or design tasks. It generates team-member context and shell commands for spawning temporary agents, with optional local memory for prior tasks and lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes unrelated absolute-loyalty and named-user rules that could conflict with normal agent instructions. <br>
Mitigation: Review the skill before installation and remove those rule-override instructions before operational use. <br>
Risk: The memory feature can persist task details locally under ~/.agent-memory/flash-company. <br>
Mitigation: Use the memory feature only with data suitable for local retention, avoid secrets or confidential project data, and define retention and deletion handling before use. <br>
Risk: Activation phrases and generated agent commands may create broader agent behavior than intended. <br>
Mitigation: Narrow activation phrases and review generated spawn commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/flash-company) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON memory files under ~/.agent-memory/flash-company when the memory scripts are used.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
