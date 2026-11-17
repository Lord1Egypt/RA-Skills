## Description: <br>
Excel Ninja Free helps agents run local Excel and CSV workflows for merging, converting, filtering, splitting, deduplicating, aggregating, validating, and selecting spreadsheet data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, developers, and automation teams use this skill to have an agent prepare spreadsheet-processing commands and workflows for routine Excel and CSV cleanup, reporting, conversion, and validation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python commands that read Excel or CSV files and create output files. <br>
Mitigation: Install it only when local spreadsheet automation is intended, use test copies of important files, and specify output filenames or directories clearly. <br>
Risk: Batch processing can apply spreadsheet transformations across multiple files. <br>
Mitigation: Review the batch plan before processing a folder and inspect output files before relying on the results. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks, plus generated .xlsx or .csv files when commands are executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local execution may read spreadsheet inputs and create output files in user-specified paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
