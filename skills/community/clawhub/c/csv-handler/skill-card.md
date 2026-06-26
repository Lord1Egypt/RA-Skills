## Description: <br>
Handle CSV files from construction software exports. Auto-detect delimiters, encodings, and clean messy data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction project teams and agents use this skill to profile, clean, merge, split, and export CSV data from construction software exports, including schedule and cost files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local file paths and can write exported or split CSV files. <br>
Mitigation: Use explicit input and output paths, validate user-supplied paths, and review generated files before using them in project workflows. <br>
Risk: Activation wording is broader than the CSV-processing implementation. <br>
Mitigation: Use it for CSV or closely related tabular-data tasks, and route unrelated construction project-management work to a more appropriate skill. <br>
Risk: Python examples may depend on pandas and chardet being installed separately. <br>
Mitigation: Confirm Python 3 and required packages are available in the intended environment before running the examples. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/csv-handler) <br>
- [Publisher Homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown with structured tables, Python code examples, and optional CSV, Excel, or JSON export guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local user-provided tabular data and Python 3; Python examples may require pandas and chardet to be installed separately.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
