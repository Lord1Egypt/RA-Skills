## Description: <br>
Predict construction project costs using machine learning models trained on historical project data, including Linear Regression, K-Nearest Neighbors, Random Forest, and Gradient Boosting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External construction estimators, cost managers, and developers use this skill to prepare historical project data, train local machine learning models, compare model performance, and produce cost predictions with confidence ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Construction cost predictions can be misleading when training data is sparse, outdated, low quality, or outside the new project's range. <br>
Mitigation: Require sufficient historical examples, adjust costs consistently, report confidence ranges, compare against benchmarks, and warn when extrapolating beyond the training data. <br>
Risk: Historical project datasets may contain confidential commercial or project information. <br>
Mitigation: Limit filesystem access to intended datasets and output folders, and remove unnecessary confidential columns before model training or analysis. <br>
Risk: Serialized model files can be unsafe or untrustworthy if loaded from unknown sources. <br>
Mitigation: Only load saved model files from trusted sources and review local files before using them in a prediction workflow. <br>


## Reference(s): <br>
- [Cost Prediction ClawHub release](https://clawhub.ai/datadrivenconstruction/cost-prediction) <br>
- [Data-Driven Construction](https://datadrivenconstruction.io) <br>
- [scikit-learn documentation](https://scikit-learn.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Python code snippets, metric tables, prediction ranges, and feature-importance summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local model training steps, evaluation metrics, and recommendations for selecting a prediction model.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release.version and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
