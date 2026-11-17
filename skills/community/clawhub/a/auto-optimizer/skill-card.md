## Description:

Auto-Optimizer guides agents through iterative optimization loops for prompts, copy, websites, code, configurations, prediction strategies, and other artifacts using scalar metrics or binary evaluation criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmarji](https://clawhub.ai/user/rmarji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to improve a target file over repeated eval-mutate-select cycles, either by maximizing or minimizing a numeric metric or by scoring generated outputs against yes/no criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization sessions mutate the selected file and use git commits or checkout to keep or revert changes.

Mitigation: Run only in a disposable repository or isolated worktree, and inspect git status before creating any baseline commit.

Risk: Scalar mode runs user-provided metric commands, which can execute arbitrary shell behavior in the target environment.

Mitigation: Pass only reviewed metric scripts and avoid running against executable code without sandboxing.

Risk: Optimization prompts, metrics, or optional integrations may involve project data or live API access.

Mitigation: Keep secrets out of the target directory and connect live APIs or private analytics data only after explicitly approving that data flow.

## Reference(s):

- [Auto-Optimizer Setup Guide](SETUP.md)
- [Outreach & Copy Optimization](references/copy-optimization.md)
- [Prediction Market Strategy Optimization](references/prediction-market-optimization.md)
- [Prompt & Skill Optimization with Binary Evals](references/prompt-optimization.md)
- [Web Performance Optimization](references/web-optimization.md)
- [ClawHub Skill Page](https://clawhub.ai/rmarji/skills/auto-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; script runs also write report.md, best.md, results.tsv, and hypothesis_log.jsonl.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs iterative optimization sessions against a single mutable target file and stores per-session results under the skill results directory.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
