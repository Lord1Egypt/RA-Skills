## Description: <br>
Autoresearch helps AI agents run systematic experiments by changing one variable at a time, measuring results, and keeping or discarding changes based on a configured metric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[admirobot](https://clawhub.ai/user/admirobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and run autonomous optimization, ablation, or configuration-search loops where an agent can modify approved files, run an experiment command, extract a metric, and summarize results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit code and run commands for extended autonomous experiment loops. <br>
Mitigation: Install and run it only in repositories where autonomous code changes and command execution are acceptable, with explicit scope and time limits. <br>
Risk: The protocol uses destructive git resets to discard failed or non-improving experiments, which can remove uncommitted work. <br>
Mitigation: Start from a clean git status on a disposable branch or worktree, and preserve important local changes before running the loop. <br>
Risk: Metric-driven optimization can overfit to a single metric or accidentally affect evaluation-adjacent behavior. <br>
Mitigation: Keep evaluation, data preparation, and measurement files read-only, and review kept commits before merging them into protected branches. <br>


## Reference(s): <br>
- [Autoresearch Reference](artifact/reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/admirobot/autoresearch-loop-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code edits, configuration files, run logs, and tab-separated experiment results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create autoresearch.config.md, results.tsv, run.log, git commits, and code changes during an experiment loop.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
