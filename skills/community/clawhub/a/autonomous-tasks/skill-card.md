## Description: <br>
Self-driven AI worker that reads saved goals, generates task lists, executes one round of work, and logs progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changye01](https://clawhub.ai/user/changye01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use this skill to maintain goal-driven local task state, decompose goals into actionable tasks, execute one work round, and record progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make local project file changes while executing saved goals. <br>
Mitigation: Keep goals specific, run the skill only from the intended project directory, and review the agents/ state files periodically. <br>
Risk: Scheduled execution can repeatedly invoke autonomous work. <br>
Mitigation: Enable the suggested cron schedule only when recurring autonomous execution is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/changye01/autonomous-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task files, local project files, and concise agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local agents/ state files and writes task outputs to the current working directory.] <br>

## Skill Version(s): <br>
10.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
