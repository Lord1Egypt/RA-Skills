## Description: <br>
Engineering Mode guides an agent through a six-stage coding workflow for understanding, decomposing, isolating, editing, verifying, and recovering code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzzxiaoqiang520](https://clawhub.ai/user/zzzxiaoqiang520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to structure code-writing, code-modification, and refactoring tasks into staged analysis, planning, safety isolation, implementation, validation, and recovery steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to create branches, checkpoint commits, and perform hard Git rollbacks that can discard local work. <br>
Mitigation: Before any hard rollback or branch deletion, require the agent to show git status, identify the exact branch or checkpoint, summarize what would be lost, and get explicit user confirmation. <br>


## Reference(s): <br>
- [Pre-Edit Checklist](references/pre-edit-checklist.md) <br>
- [Validate Strategies](references/validate-strategies.md) <br>
- [Error Recovery](references/error-recovery.md) <br>
- [Commit Discipline](references/commit-discipline.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses conditional reference loading for pre-edit checks, validation strategy, error recovery, and commit discipline.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
