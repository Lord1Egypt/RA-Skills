## Description:

Automl Skill helps data scientists and developers build low-code PyCaret machine learning workflows for classification, regression, clustering, anomaly detection, time series forecasting, NLP, association rules, and statistical inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

External data scientists, developers, and machine learning engineers use this skill to quickly prototype and document AutoML workflows with PyCaret, including preprocessing, model comparison, tuning, interpretation, statistical testing, and optional deployment steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example workflows can save models or experiment files using local output names.

Mitigation: Review and adjust output paths before running examples to avoid overwriting existing model or experiment artifacts.

Risk: Deployment, app, API, and Docker examples may create files, use cloud credentials, or expose model artifacts outside the local environment.

Mitigation: Run deployment-oriented examples only after confirming credential scope, target platform, generated files, and artifact exposure are appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yejinlei/skills/automl-skill)
- [PyCaret official documentation](https://pycaret.gitbook.io/docs)
- [PyCaret API documentation](https://pycaret.readthedocs.io/)
- [PyCaret Classification Module](artifact/references/classification.md)
- [PyCaret Regression Module](artifact/references/regression.md)
- [PyCaret Time Series Module](artifact/references/time_series.md)
- [PyCaret Clustering Module](artifact/references/clustering.md)
- [PyCaret Anomaly Detection Module](artifact/references/anomaly.md)
- [PyCaret NLP Module](artifact/references/nlp.md)
- [PyCaret Association Rules Module](artifact/references/association_rules.md)
- [PyCaret setup() Parameter Deep Dive](artifact/references/setup_parameters_deep_dive.md)
- [PyCaret Utility Functions](artifact/references/utilities.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python code examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill output; examples may name local files, cloud deployments, apps, APIs, or Docker artifacts for the user to review before execution.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
