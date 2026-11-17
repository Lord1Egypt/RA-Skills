## Description: <br>
Csv Insight Free helps agents inspect local CSV files, compute summaries, filter rows, detect statistical outliers, group records, and export CSV results using Python standard-library tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, developers, and operations users use this skill to quickly explore local CSV datasets, summarize columns, filter rows, find Z-Score outliers, aggregate groups, and export simple CSV results without installing pandas. It is not intended for real-time stream processing or the free edition's documented advanced analytics exclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local CSV files and write exported CSV results to user-selected paths. <br>
Mitigation: Review the exact command, input file, and output path before execution, especially when an existing file could be overwritten. <br>
Risk: The artifact references a script path but does not include the script or document overwrite behavior. <br>
Mitigation: Confirm the executable exists in the installed skill directory and inspect generated commands before running them. <br>


## Reference(s): <br>
- [Csv Insight Free on ClawHub](https://clawhub.ai/thcjp/skills/csv-insight-free) <br>
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, CSV files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional CSV file exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV inputs; exported CSV results depend on the command and output path selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
