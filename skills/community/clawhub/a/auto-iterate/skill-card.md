## Description: <br>
Runs autonomous, metric-driven code optimization loops that edit a target file, execute an experiment command, evaluate the result, and keep or roll back changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawzhang](https://clawhub.ai/user/sawzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run repeated optimization experiments against a single target file and a user-specified metric, such as ML tuning, performance optimization, or prompt optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously edit code, run shell commands, and continue unattended without firm limits. <br>
Mitigation: Use a clean disposable branch or worktree, set explicit time and iteration limits, and confirm the run command cannot deploy, delete data, touch production systems, or incur unexpected costs. <br>
Risk: The workflow may change repository history through commits and hard resets. <br>
Mitigation: Commit or back up important local work before starting and restrict the skill to an isolated target file and experiment branch. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create experiment branches, commits, run logs, and untracked results.tsv records during agent execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
