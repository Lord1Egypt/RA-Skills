## Description: <br>
Compares table field differences between MySQL and ODPS databases and generates HiveSQL ALTER TABLE statements and DataX JSON field mappings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to compare MySQL and ODPS table schemas, identify field differences, and prepare synchronization artifacts. It generates reviewable ALTER TABLE statements and DataX get_json_object mappings without applying DDL itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may query database schemas and SSH-accessible ODPS environments. <br>
Mitigation: Use it only with databases and SSH hosts the user controls or is authorized to inspect, and prefer read-only credentials for schema checks. <br>
Risk: Generated ALTER TABLE statements could make unintended schema changes if applied without review. <br>
Mitigation: Review the generated DDL against the intended source and target environments before executing it. <br>
Risk: Ambiguous source or target names may cause the agent to compare the wrong environment or table. <br>
Mitigation: Provide explicit source and target environment names plus table scope for each comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexmayanjun-collab/db-table-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with SQL, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include field comparison notes, generated ALTER TABLE statements, and DataX JSON extraction expressions for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
