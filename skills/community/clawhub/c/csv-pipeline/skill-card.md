## Description: <br>
Process, transform, analyze, and report on CSV and JSON data files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data practitioners use this skill to inspect, clean, filter, join, aggregate, convert, validate, and report on local CSV, TSV, JSON, and JSON Lines files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated transformations or shell commands could overwrite important local data files. <br>
Mitigation: Provide explicit input and output paths, review commands before execution, and keep backups before writing over important files. <br>
Risk: CSV, TSV, JSON, or JSON Lines files may contain sensitive data that the agent could process or summarize. <br>
Mitigation: Use the skill only with data the user intentionally provides for local processing and avoid sensitive datasets unless that is the intended task. <br>
Risk: Malformed data, unexpected delimiters, encodings, or type conversions can produce incorrect analyses or reports. <br>
Mitigation: Inspect headers, row counts, encodings, and validation output before relying on transformed files or summaries. <br>


## Reference(s): <br>
- [CSV Data Pipeline on ClawHub](https://clawhub.ai/gitgoodordietrying/csv-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks; generated workflows may create CSV, TSV, JSON, JSON Lines, or Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files and standard command-line or Python tooling; no external service dependency is evidenced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
