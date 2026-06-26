## Description: <br>
Validates CSV, JSON, and JSONL data files for quality issues, including missing values, duplicates, type inconsistencies, outliers, format violations, whitespace problems, empty columns, and schema drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to inspect CSV, JSON, and JSONL datasets, generate quality reports, validate data against a schema, and create starter schemas from existing data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected local data files and generated reports may reveal dataset structure or quality issues. <br>
Mitigation: Run it only on files intended for inspection, choose output paths deliberately, and review reports before sharing them. <br>
Risk: Generated schemas and quality scores are heuristic outputs that may not capture domain-specific validation requirements. <br>
Mitigation: Review generated schemas and reported findings against the intended data contract before using them in CI or release gates. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Terminal text, Markdown reports, JSON reports, and JSON schema files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate clean, warning, or critical findings; reports may be written to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
