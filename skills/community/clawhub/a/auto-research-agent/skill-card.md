## Description:

Auto Research Agent provides an autonomous AI research workflow for iteratively designing experiments, editing training code, running training, evaluating metrics, and retaining better results under a fixed budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run structured model-training experiments, tune architectures and hyperparameters, compare validation metrics, and record iteration decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow directs an agent to iteratively edit and run local training code.

Mitigation: Use version control or a disposable project copy before starting the research loop.

Risk: Training experiments can consume CPU or GPU time.

Mitigation: Set and monitor fixed experiment budgets before running training commands.

Risk: The included training script is a demo-style transformer experiment over generated data.

Mitigation: Review the dataset, metrics, and experiment logs before treating results as meaningful for a real model or task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smseow001/skills/auto-research-agent)
- [Research Program Baseline](program.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code edits and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update train.py and experiment notes during iterative research runs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
