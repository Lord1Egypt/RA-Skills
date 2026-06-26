## Description: <br>
管理和启动数字员工角色，支持创建角色、读取和更新角色记忆，以及在启动前检查角色是否存在。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cabbage1016](https://clawhub.ai/user/cabbage1016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team leads use this skill to maintain reusable digital employee roles, start role-specific sub-agents, and persist role memory for repeated project work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Role memory files may accumulate sensitive project details or stale instructions. <br>
Mitigation: Review workspace/agents and workspace/knowledge files periodically, avoid storing secrets, and update or remove outdated role memory. <br>
Risk: Automatic role detection and sub-agent launch can activate an unintended role if a request is ambiguous. <br>
Mitigation: Use explicit role commands and confirm creation or launch prompts before allowing the skill to create files or start a sub-agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cabbage1016/digital-team) <br>
- [Role template](artifact/TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with role files and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace role memory files and launch sub-agents when the user confirms role actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
