## Description: <br>
CSV and delimited data processing toolkit for transforming, filtering, merging, validating, and converting data files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect, filter, sort, merge, join, clean, convert, and summarize CSV, TSV, and other delimited data files with Python standard-library utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The --where option is interpreted as Python expression syntax. <br>
Mitigation: Use only trusted filter strings; avoid filter text from downloaded files, prompts, or automation; prefer a release that replaces expression evaluation with a restricted comparison parser. <br>
Risk: The security verdict is suspicious because one helper evaluates filter text as Python code. <br>
Mitigation: Review the helper scripts before installation and restrict use to trusted local data-processing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/csv-data-processor) <br>
- [Publisher profile](https://clawhub.ai/user/ericlooi504) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV, JSON, SQL, or text output from the helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local file paths, delimiter and encoding options, optional output files, and filter or transformation arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
