## Description:

Improvement Evaluator runs predefined YAML task suites against skill changes, judges pass/fail outcomes, and reports execution pass rate for comparing candidate and baseline performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate whether changes to a SKILL.md improve real task execution by running task suites, comparing against a baseline, and producing pass-rate metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Claude and pytest-based evaluations on skill and task content without clear sandbox or permission boundaries.

Mitigation: Install and run it only in a contained evaluation environment, prefer mock mode or a locked-down Claude CLI, and restrict filesystem and network access.

Risk: Task suites and candidate SKILL.md content are untrusted inputs that can influence prompts and local evaluation behavior.

Mitigation: Review task suites before execution, remove unrelated secrets from the environment, and keep pytest fixtures limited to intended evaluation files.

## Reference(s):

- [Task Suite Format](artifact/references/task-format.md)
- [Writing Effective Task Suites](artifact/references/writing-tasks-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/auto-improvement-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON evaluation artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pass/fail task results, execution pass rate, baseline pass rate, delta, and a verdict; mock mode is available for contained evaluation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
