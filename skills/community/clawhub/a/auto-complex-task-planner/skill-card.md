## Description: <br>
Auto Complex Task Planner analyzes task complexity, prioritizes work, and delegates complex research, development, documentation, and batch tasks to parallel sub-agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sixtysixsone](https://clawhub.ai/user/sixtysixsone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to route broad requests into prioritized sub-agent work for research, feature development, documentation, search, and batch-processing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically delegates broad tasks to sub-agents, which can reduce user control over sensitive, account-level, delete, or batch actions. <br>
Mitigation: Review generated sub-agent plans before execution and add explicit confirmation steps for credentials, sensitive business data, account operations, delete operations, and broad batch actions. <br>
Risk: The skill may store raw task details in local task-history records. <br>
Mitigation: Avoid entering credentials or sensitive business data, monitor created sub-agents, and periodically clear workspace memory records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sixtysixsone/auto-complex-task-planner) <br>
- [README.md](artifact/README.md) <br>
- [README_CN.md](artifact/README_CN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON task records, and generated task instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May delegate work to sub-agents and create local task-history records.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
