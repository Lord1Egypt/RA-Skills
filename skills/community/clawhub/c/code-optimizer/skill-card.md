## Description:

Code Optimizer evaluates code quality with ML-based scoring and selects optimization strategies for code-generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to assess code quality, run standardized test cases, generate quality reports, and choose code-generation strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment script imports evaluator code from an external local path and may expose code that is not bundled in the release.

Mitigation: Run it only in a disposable or tightly controlled workspace, and prefer a release that bundles the evaluator source for review before execution.

Risk: The deployment script can install Python dependencies, update Hermes configuration, copy files into the skill package, and create a HOME/bin command link.

Mitigation: Review dependency pins and configuration diffs before use, and require explicit approval before modifying Hermes or user-level command paths.

Risk: Code-evaluation history and feedback-loop behavior may retain submitted code or task details.

Mitigation: Avoid evaluating sensitive code unless retention controls are configured, and review stored evaluation data regularly.

## Reference(s):

- [Code Optimizer ClawHub Page](https://clawhub.ai/clementgu/skills/code-optimizer)
- [ClawHub Skill Homepage](https://clawhub.ai/skills/code-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and optional generated quality reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include strategy recommendations such as balanced, emphasize_correctness, or extreme_correctness.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
