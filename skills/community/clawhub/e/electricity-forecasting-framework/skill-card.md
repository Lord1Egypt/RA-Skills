## Description: <br>
A comprehensive electricity load and demand forecasting framework for preparing time-series data, selecting statistical, machine learning, and deep learning models, evaluating forecasts, backtesting, quantifying uncertainty, and preparing deployment artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxy799](https://clawhub.ai/user/sxy799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data scientists, and energy engineers use this skill to build electricity load forecasting workflows for grid operations, energy trading, consumption analysis, and production forecasting pipelines with uncertainty estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted joblib model files may be unsafe to load. <br>
Mitigation: Load only model files created in a trusted environment and review model artifacts before using deployment or backtesting scripts. <br>
Risk: Generated deployment outputs can expose a forecasting API if launched on a network. <br>
Mitigation: Keep generated deployment files in a dedicated project folder and expose the API server only after intentional access control and network configuration. <br>
Risk: Forecasting datasets may contain operational or customer-sensitive electricity usage data. <br>
Mitigation: Use a clean virtual environment and dedicated data directory, and apply the organization's data handling controls before training, evaluation, or deployment. <br>


## Reference(s): <br>
- [Feature Engineering Guide](references/feature-engineering.md) <br>
- [Model Selection Guide](references/model-selection.md) <br>
- [Deep Learning Architectures](references/deep-learning-models.md) <br>
- [Uncertainty Quantification Guide](references/uncertainty.md) <br>
- [Deployment Guide](references/deployment.md) <br>
- [Datasets Reference](references/datasets.md) <br>
- [UCI Electric Load Diagrams](https://archive.ics.uci.edu/ml/datasets/ElectricLoadDiagrams20112014) <br>
- [PJM Interconnection Load Data](https://datatracker.pjm.com/) <br>
- [ISO-NE Load Data](https://www.iso-ne.com/isoexpress/) <br>
- [ERCOT Load Data](https://www.ercot.com/gridinfo/load) <br>
- [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local processed datasets, trained model artifacts, metrics, deployment wrappers, and API server files when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
