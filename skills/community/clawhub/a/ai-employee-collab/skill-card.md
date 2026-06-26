## Description: <br>
AI员工协作技能包 - 多AI角色配置、任务自动分配、进度监控、结果汇报。适合想要自动化运营的团队。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, project managers, independent builders, and small teams use this skill to configure AI employee roles, assign and track work, monitor team status, and generate work reports for automated operations workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reloads local memory about AI employee work, which could retain sensitive business details if users place them in notes or task records. <br>
Mitigation: Do not store credentials or sensitive business data in retained notes, review the memory directory before use, and periodically delete or archive memory that is no longer needed. <br>
Risk: The included employee manager creates and updates local configuration, template, and memory files relative to the skill directory. <br>
Mitigation: Run the skill in a controlled workspace and review the configured file paths before using it with important project data. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/gdp6539/ai-employee-collab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and local text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local configuration and memory files for AI employee roles.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
