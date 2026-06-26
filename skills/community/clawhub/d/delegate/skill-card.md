## Description: <br>
Route tasks to sub-agents with optimal model selection, error recovery, and result verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use Delegate to decide when to route research, implementation, analysis, review, and file-processing tasks to sub-agents, with model-tier selection, retry guidance, and result checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated coding or research work may be incorrect, incomplete, or based on missing context. <br>
Mitigation: Review sub-agent results, run tests or syntax checks for code, verify created files, and spot-check research sources before relying on the output. <br>
Risk: Retrying delegated tasks can repeat or amplify actions that have external side effects. <br>
Mitigation: Use the documented abort criteria, retry only when the task is safe to repeat, and review changes, tests, and commits before acceptance. <br>


## Reference(s): <br>
- [Delegate on ClawHub](https://clawhub.ai/ivangdavila/delegate) <br>
- [Error Recovery Patterns](errors.md) <br>
- [Spawn Templates](templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown instructions, checklists, and task templates with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegated outputs should be reviewed, tested, and checked against requested completion criteria before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
