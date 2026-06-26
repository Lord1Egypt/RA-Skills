## Description: <br>
Data Governance helps agents assess data quality, generate metadata, trace data lineage, define standards, and check compliance for database-backed data assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingjianliu0417](https://clawhub.ai/user/xingjianliu0417) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and governance reviewers use this skill to inspect authorized databases for data quality, schema metadata, lineage, and compliance findings. It produces structured reports that support data asset review and remediation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to user-specified databases and may inspect schema and selected table data. <br>
Mitigation: Install and run it only for databases the user owns or is authorized to inspect, using a dedicated read-only database account scoped to the needed tables. <br>
Risk: Database credentials can be exposed if passed in command-line connection strings or committed to configuration. <br>
Mitigation: Prefer environment variables for credentials and avoid placing real passwords in command-line arguments or persistent shell configuration. <br>
Risk: Generated reports can contain schema names, sensitive field names, and data-derived quality findings. <br>
Mitigation: Review and redact reports before sharing them outside the authorized team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingjianliu0417/data-governance) <br>
- [Publisher profile](https://clawhub.ai/user/xingjianliu0417) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON metadata, Mermaid lineage diagrams, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include schema names, sensitive field names, and sampled data-derived quality findings.] <br>

## Skill Version(s): <br>
1.10.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
