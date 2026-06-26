## Description: <br>
Manipulate CSV files from the command line, including viewing, filtering, sorting, selecting columns, converting CSV to and from JSON, computing statistics, deduplicating rows, and merging files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agents use this skill to inspect, clean, transform, summarize, and combine local CSV data through Python command-line operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Output paths can overwrite existing local files. <br>
Mitigation: Review any -o or --output path before running commands, especially when processing important or sensitive datasets. <br>
Risk: CSV processing may expose sensitive local data through terminal output or generated files. <br>
Mitigation: Use the skill only on files intended for processing and avoid unnecessary sensitive datasets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/csv-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file outputs such as CSV, JSON, and plain text tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python standard library modules and supports custom delimiters, encodings, and optional output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
