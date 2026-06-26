## Description: <br>
Create and manage virtual AI employees with persistent memory, defined roles, and graduated autonomy. Hire, train, and delegate tasks to specialized workers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create, configure, train, and manage local AI employee profiles with scoped roles, persistent memory, routing rules, lifecycle commands, and graduated autonomy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local employee profiles may retain sensitive context in memory and logs. <br>
Mitigation: Keep fileAccess narrow, avoid training employees on secrets or regulated data, and periodically review ~/employee memory and logs. <br>
Risk: Delegation, auto-routing, spawning, or messaging could let an employee act beyond the user's intended scope. <br>
Mitigation: Start employees in shadow or draft-only mode, leave canSpawn and canMessage disabled unless needed, and require explicit approval before autonomous permissions or auto-delegation. <br>


## Reference(s): <br>
- [Employee skill definition](artifact/SKILL.md) <br>
- [Employee template](artifact/employee-template.md) <br>
- [Autonomy levels](artifact/autonomy.md) <br>
- [Lifecycle commands](artifact/lifecycle.md) <br>
- [Task routing](artifact/routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output for proposed employee profiles, memory/log templates, routing guidance, and lifecycle command plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
