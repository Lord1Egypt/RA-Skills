## Description: <br>
Autoresearch.Bak guides an agent through setup, iterative experiments, metric tracking, and analysis for optimization tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run disciplined one-variable-at-a-time experiments, optimize a defined metric, keep useful changes, discard regressions, and summarize results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous experiment runs can edit code, execute project commands, and change git history, including hard resets. <br>
Mitigation: Run only in a clean disposable branch, worktree, or clone; inspect autoresearch.config.md; approve exact target files and commands; require a clean git status before running. <br>
Risk: The experiment loop is designed to continue until the user stops it. <br>
Mitigation: Set a hard time or experiment limit before starting and monitor the run against that limit. <br>
Risk: Poorly scoped target files or metrics can let experiments modify evaluation logic or optimize the wrong behavior. <br>
Mitigation: Keep evaluation, data preparation, and metric extraction files read-only, and define one clear success metric with explicit constraints during setup. <br>


## Reference(s): <br>
- [Autoresearch Reference](artifact/reference.md) <br>
- [ClawHub Release Page](https://clawhub.ai/lean-zhouchao/autoresearch-bak) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, configuration files, TSV experiment logs, git commits, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify target files and repository history during experiment runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
