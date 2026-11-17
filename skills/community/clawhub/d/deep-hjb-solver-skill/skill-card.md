## Description:

Create or refactor code for solving HJB equations with this repository's TensorFlow DGM framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reedcgx](https://clawhub.ai/user/reedcgx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate or refactor TensorFlow Deep Galerkin Method training code for Hamilton-Jacobi-Bellman problems, including problem configs, loss functions, training scripts, plotting helpers, and repository-convention guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scaffold behavior can write outside intended project paths if given an unsafe problem name or run from the wrong directory.

Mitigation: Use simple snake_case problem slugs, run in a disposable or project-scoped directory, and inspect generated files before training.

Risk: Generated HJB problem and loss files include placeholders that may be mathematically incomplete until customized.

Mitigation: Replace TODO payoff, PDE residual, and control-objective code, then verify tensor shapes and required trainer return signatures before running training.

## Reference(s):

- [Repository Conventions](artifact/references/repo-conventions.md)
- [Training Output Contract](artifact/references/training-output-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/reedcgx/skills/deep-hjb-solver-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated Python project files when applied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained HJB problem folders, TensorFlow training scripts, config/loss/problem modules, plotting helpers, and CSV-output guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
