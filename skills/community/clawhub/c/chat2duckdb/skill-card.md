## Description: <br>
chat2duckdb helps agents analyze user-selected CSV, JSON, Parquet, and Excel data files with DuckDB SQL, descriptive profiling, sampling, SQL retry correction, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcba](https://clawhub.ai/user/cloudcba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect local tabular datasets, generate and run DuckDB SQL, summarize data quality, sample large files, and export query results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local DuckDB SQL against files selected by the user, so queries over sensitive datasets can reveal or transform sensitive records. <br>
Mitigation: Review SQL before execution, prefer SELECT-style analysis queries, and choose input files deliberately. <br>
Risk: Export and persistence options can save results or DuckDB tables to unintended locations. <br>
Mitigation: Check output and persistence paths before running commands and avoid writing sensitive results to shared or untrusted directories. <br>


## Reference(s): <br>
- [Data format support guide](references/data-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, SQL snippets, tabular text previews, and optional exported data files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create CSV, Excel, JSON, Parquet, DuckDB, or JSON report files when output or persistence paths are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
