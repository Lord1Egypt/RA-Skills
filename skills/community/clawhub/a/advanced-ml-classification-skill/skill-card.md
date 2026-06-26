## Description: <br>
Generates and runs machine learning classification workflows from CSV data, compares model accuracy, and returns generated code, metrics, visualization data, feature importance, and beginner-friendly Chinese interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bamboo9805](https://clawhub.ai/user/bamboo9805) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to benchmark classification algorithms on tabular CSV datasets, including preprocessing, optional cross-validation, optional hyperparameter search, feature-importance ranking, and result interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run remotely generated Python code locally when an OpenAI API key is available. <br>
Mitigation: Run it only in an isolated environment or container, unset OPENAI_API_KEY unless remote generation is intended, and review generated code before relying on its results. <br>
Risk: CSV datasets and uploaded files may contain sensitive data and temporary uploaded CSV files can remain on disk. <br>
Mitigation: Avoid sensitive datasets, use disposable working directories, and clean up temporary CSV files after using the Streamlit upload flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bamboo9805/advanced-ml-classification-skill) <br>
- [Publisher profile](https://clawhub.ai/user/bamboo9805) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, shell commands, guidance] <br>
**Output Format:** [JSON-like structured results with generated Python code, numeric metrics, visualization data, error text, and natural-language interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes accuracy results, optional cross-validation scores, optional parameter-search results, generated training code, feature-importance data, and chart-ready series.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
