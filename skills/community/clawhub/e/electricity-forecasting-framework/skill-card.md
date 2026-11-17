## Description:

Comprehensive electricity load and demand forecasting framework for data preparation, feature engineering, statistical, machine learning, and deep learning models, evaluation, backtesting, uncertainty quantification, and deployment packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxy799](https://clawhub.ai/user/sxy799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and energy analytics teams use this skill to build electricity load forecasting workflows, including data preparation, feature engineering, model selection, training, evaluation, backtesting, uncertainty quantification, and deployment packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged unsafe production patterns in deployment guidance and scripts.

Mitigation: Review and harden deployment outputs before use, especially generated service code, scheduled jobs, and production runtime configuration.

Risk: Serialized model loading can execute unsafe content when model files are untrusted.

Mitigation: Load only trusted .joblib or PyTorch model files and keep model artifacts under controlled provenance and access checks.

Risk: Generated API services may be exposed without sufficient protections.

Mitigation: Add authentication, request limits, dependency pinning, and operational monitoring before exposing any forecasting API.

Risk: Scheduled forecasting or retraining jobs can run with excessive privileges.

Mitigation: Run scheduled jobs under a dedicated non-root account with least-privilege filesystem and network access.

## Reference(s):

- [Feature Engineering Guide](references/feature-engineering.md)
- [Model Selection Guide](references/model-selection.md)
- [Deep Learning Models for Electricity Forecasting](references/deep-learning-models.md)
- [Uncertainty Quantification Guide](references/uncertainty.md)
- [Deployment Guide](references/deployment.md)
- [Datasets Reference](references/datasets.md)
- [UCI Electric Load Diagrams](https://archive.ics.uci.edu/ml/datasets/ElectricLoadDiagrams20112014)
- [PJM Interconnection Load Data](https://datatracker.pjm.com/)
- [ISO New England ISO Express](https://www.iso-ne.com/isoexpress/)
- [ERCOT Load Data](https://www.ercot.com/gridinfo/load)
- [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce model training, evaluation, backtesting, deployment, and data preparation artifacts when the user runs the included scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
