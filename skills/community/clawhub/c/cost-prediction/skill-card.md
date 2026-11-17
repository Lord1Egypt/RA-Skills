## Description:

Predict construction project costs using Machine Learning. Use Linear Regression, K-Nearest Neighbors, and Random Forest models on historical project data. Train, evaluate, and deploy cost prediction models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

External developers, estimators, and construction analytics teams use this skill to prepare historical project data, train cost prediction models, compare model performance, and produce cost estimates with confidence ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loading pickle or joblib model files from untrusted sources can execute code.

Mitigation: Use only models created in a trusted local workflow, and do not load .pkl or joblib files received from email, downloads, shared folders, or other untrusted channels.

Risk: Historical construction datasets can contain sensitive commercial or project information.

Mitigation: Anonymize, minimize, and access-control project cost datasets before using them with the skill.

Risk: Cost predictions may be misleading when inputs fall outside the range or quality of the training data.

Mitigation: Report confidence ranges, review feature influence, and warn when extrapolating beyond observed training data.

## Reference(s):

- [Data-Driven Construction](https://datadrivenconstruction.io)
- [scikit-learn](https://scikit-learn.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python code snippets, metrics tables, feature-importance rankings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated cost ranges, model evaluation metrics, and warnings when predictions extrapolate beyond the training data range.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
