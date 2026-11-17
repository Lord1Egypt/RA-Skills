## Description:

Helps agents bootstrap and adapt a ModelScope Fourier Neural Operator workflow for CFD surrogate training, inference, and structured-grid PDE forecasting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onescience-ai](https://clawhub.ai/user/onescience-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare FNO model code, adapt dataset and model configuration, run smoke tests, train, and run inference on CFD or PDE structured-grid datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to contact ModelScope, install Python packages, cache remote code, and execute downloaded code locally.

Mitigation: Use an isolated environment, review or pin the ModelScope package and model revision, and avoid exposing credentials or sensitive datasets unless the upstream source is trusted.

Risk: Mutable remote model code can change between runs without strong integrity controls.

Mitigation: Pin the model revision when possible, inspect the resolved local directory, and verify expected entry points before training or inference.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onescience-ai/skills/cfd-model-run)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash snippets plus configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local dependency installation, ModelScope download or cache resolution, dataset adapter changes, training commands, and inference commands.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
