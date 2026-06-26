## Description: <br>
Data quality validation and profiling toolkit for tabular data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to profile tabular datasets, validate schemas, detect missing values, check constraints, and identify statistical anomalies before downstream analysis or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process private tabular datasets and produce reports containing sensitive fields or values. <br>
Mitigation: Handle input data and generated reports according to the user's privacy and data handling requirements. <br>
Risk: Unpinned pandas and numpy versions may produce non-reproducible results across environments. <br>
Mitigation: Install in a virtual environment and pin dependency versions when reproducible production results are required. <br>


## Reference(s): <br>
- [Validation Rules Reference](references/validation_rules.md) <br>
- [Data Validator Pro on ClawHub](https://clawhub.ai/kaiyuelv/data-validator-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and structured validation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill supports local pandas DataFrame profiling, schema validation errors, and anomaly reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
