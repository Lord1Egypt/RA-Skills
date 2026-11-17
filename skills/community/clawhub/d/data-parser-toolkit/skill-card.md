## Description:

Parses and cleans CSV, JSON, Excel, Parquet, and SQL data files with encoding detection, common repair helpers, format conversion, and structured data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and agent workflows use this skill to inspect, parse, clean, convert, and sample tabular or semi-structured data files before downstream analysis or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL parsing can fetch arbitrary destinations.

Mitigation: Use URL parsing only for explicitly approved destinations and prefer local trusted files when possible.

Risk: Archive parsing and large data files can exhaust memory, disk, or processing resources.

Mitigation: Run the skill in an isolated environment, inspect archive contents first, and set operational limits for file size, extracted content, and processing time.

Risk: Conversion and export helpers can overwrite or create output files.

Mitigation: Use dedicated output directories, review target paths before execution, and keep backups of source data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/skills/data-parser-toolkit)
- [PyPI project page](https://pypi.org/project/data-parser-toolkit/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus parsed data objects or converted data files when the toolkit code is executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce pandas DataFrames, Python dictionaries or lists, warnings, statistics, and exported CSV or Excel files depending on the selected parser or conversion helper.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
