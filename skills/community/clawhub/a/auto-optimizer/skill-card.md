## Description: <br>
Auto-Optimizer helps agents improve prompts, copy, code, configuration, websites, and prediction strategies through iterative metric- or eval-driven optimization loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmarji](https://clawhub.ai/user/rmarji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run repeatable optimization loops over mutable files, using scalar metric commands or binary yes/no evaluation criteria to decide whether to keep changes. It is suited to prompts, outreach copy, web performance work, code or configuration tuning, and prediction strategy refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to edit selected files, create git commits, and run local metric commands. <br>
Mitigation: Run it on a disposable branch or copy, inspect metric commands before execution, and review diffs before accepting results. <br>
Risk: Optimization result folders may contain private prompts, code, copy, or strategy data. <br>
Mitigation: Review generated reports and logs for sensitive content and delete saved result folders when they are no longer needed. <br>
Risk: Weak user-control guardrails may allow broad local changes if the target file, metric, or working tree is chosen carelessly. <br>
Mitigation: Limit runs to explicitly selected files, keep the working tree scoped, and avoid broad staging commands on real projects. <br>


## Reference(s): <br>
- [Auto-Optimizer on ClawHub](https://clawhub.ai/rmarji/auto-optimizer) <br>
- [Setup Guide](SETUP.md) <br>
- [Copy Optimization](references/copy-optimization.md) <br>
- [Prompt & Skill Optimization](references/prompt-optimization.md) <br>
- [Prediction Market Strategy Optimization](references/prediction-market-optimization.md) <br>
- [Web Performance Optimization](references/web-optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command output, modified file content, and generated result files such as report.md, results.tsv, best.md, and hypothesis_log.jsonl.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target file in a git repository and either a scalar metric command or binary eval criteria.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
