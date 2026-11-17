## Description:

Design and simulate adaptive clinical trials with interim analyses, sample size re-estimation, and early stopping rules, and evaluate Type I error control, power, and expected sample size via Monte Carlo simulation before trial initiation.

This skill is for research and development only.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and biostatistics reviewers use this skill to configure and run Monte Carlo simulations for adaptive clinical trial planning. Its outputs can support exploratory design review, but clinical conclusions require qualified statistical validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical-trial design results may be incorrect or overtrusted because advertised capabilities and safety claims do not fully match the implementation.

Mitigation: Use results only for exploratory planning and require review by qualified biostatisticians and regulatory experts before applying conclusions to real trial design.

Risk: The script can overwrite files at a user-selected output path.

Mitigation: Run it in an isolated, nonprivileged environment and write outputs only to a disposable directory.

Risk: Drop-the-loser, optimization, and visualization behavior is identified as unvalidated in the security guidance.

Mitigation: Treat those features as experimental until implementation and tests are corrected, and independently verify outputs before use.

Risk: Unpinned dependencies can change numerical or plotting behavior over time.

Mitigation: Pin NumPy, SciPy, and Matplotlib versions in a controlled environment before relying on repeatable simulation outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/adaptive-trial-simulator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands; the bundled script writes JSON simulation results and can optionally write a PNG visualization.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-selected trial parameters, simulation count, output path, and optional visualization or optimization flags.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
