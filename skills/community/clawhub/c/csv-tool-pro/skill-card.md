## Description: <br>
CSV Tool Pro helps agents view, filter, sort, merge, split, deduplicate, convert, and analyze local CSV files using a pure-Python utility with no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and external users use this skill to ask an agent to inspect, clean, transform, and summarize local CSV datasets without opening a spreadsheet application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs expected local file reads and writes, so sort, merge, dedupe, and conversion requests may create or overwrite files. <br>
Mitigation: Use explicit input and output paths, keep backups for important datasets, and request previews before operations that change or replace files. <br>


## Reference(s): <br>
- [CSV Tool Pro ClawHub release](https://clawhub.ai/darbling/csv-tool-pro) <br>
- [CSV Tool Pro source link from skill text](https://github.com/darbling/clawhub-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with file paths, command examples, tabular previews, and generated data-file contents when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local CSV inputs and write converted or processed local files such as CSV, JSON, YAML, TSV, Markdown, or HTML.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
