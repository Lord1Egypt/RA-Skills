## Description: <br>
Measures whether a skill improvement actually improves AI task execution by running YAML task suites, judging pass/fail results, and reporting execution_pass_rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run predefined task suites against a candidate SKILL.md, compare results with a baseline, and decide whether the change improves execution quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real evaluations can send skill content, task prompts, rubrics, and model outputs through the configured local Claude CLI. <br>
Mitigation: Use --mock or deterministic judges for sensitive or CI runs, and keep secrets or proprietary data out of task prompts, rubrics, and SKILL.md content. <br>
Risk: Evaluator runs local scripts and can write state, cache, and evaluation output files. <br>
Mitigation: Run only trusted task suites and write state, cache, and outputs to a dedicated workspace. <br>


## Reference(s): <br>
- [Task Suite Format](artifact/references/task-format.md) <br>
- [Writing Effective Task Suites](artifact/references/writing-tasks-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/auto-improvement-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON evaluation artifacts with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports execution_pass_rate, baseline_pass_rate, delta, verdict, per-task results, and output file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
