## Description: <br>
Autonomous goal-directed iteration for optimization and improvement tasks, including metric-driven loops that make one focused change, verify it, keep or revert it, and repeat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantaclaw-ai](https://clawhub.ai/user/fantaclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to structure autonomous optimization work around a clear goal, measurable metric, bounded scope, baseline, verification command, rollback decision, and iteration log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run shell verification commands during iterative optimization. <br>
Mitigation: Use only trusted verification commands, set timeouts and maximum iterations, and review command behavior before execution. <br>
Risk: The skill encourages file-changing loops, including delegated or background execution. <br>
Mitigation: Define the exact editable scope, rollback rules, and whether subagents or background execution are allowed before starting a loop. <br>
Risk: Autonomous iterations may touch sensitive files or data if scope is too broad. <br>
Mitigation: Exclude secrets, production data, account settings, and broad home-directory paths unless they are explicitly in scope and will be reviewed. <br>


## Reference(s): <br>
- [Fanta Autoresearch ClawHub page](https://clawhub.ai/fantaclaw-ai/fanta-autoresearch) <br>
- [Autoresearch Workflows](references/workflows.md) <br>
- [Common Metrics for Autoresearch](references/metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command examples, templates, tables, and an optional Python loop executor script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an autoresearch TSV log when the bundled executor script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
