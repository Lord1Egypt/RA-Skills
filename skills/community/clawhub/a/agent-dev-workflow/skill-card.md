## Description: <br>
Orchestrate coding agents to implement coding tasks through a structured workflow covering requirement analysis, specification, task planning, agent dispatch, monitoring, verification, and delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgYanami](https://clawhub.ai/user/lgYanami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate coding agents on feature work, bug fixes, GitHub issues, and other multi-step implementation tasks. It is intended for tasks that need structured requirements, task decomposition, agent execution, verification, and delivery notes rather than simple one-line edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can launch coding agents with broad local authority and may change project files automatically. <br>
Mitigation: Use it only in intended project worktrees, prefer a less privileged command configuration where practical, and inspect the final diff before merging or committing. <br>
Risk: Project documentation or agent configuration files such as llmdoc/ and CLAUDE.md may be created or modified during the workflow. <br>
Mitigation: Review documentation and configuration changes explicitly before relying on them or including them in a commit. <br>


## Reference(s): <br>
- [cc-plugin](https://github.com/TokenRollAI/cc-plugin) <br>
- [Requirement Template](references/requirement-template.md) <br>
- [Verification Template](references/verification-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with task cards, verification checklists, shell commands, and delivery summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured workflow instructions and review checkpoints for agent-assisted code changes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
