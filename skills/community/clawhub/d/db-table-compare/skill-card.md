## Description:

Compares MySQL and ODPS table schemas and generates HiveSQL ALTER TABLE statements and DataX JSON field mappings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect schema differences between MySQL and ODPS tables, then draft synchronization SQL and DataX JSON extraction mappings for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents direct database and SSH access in an internal environment.

Mitigation: Use it only in authorized environments, require confirmation before connecting, and prefer dedicated read-only schema-inspection accounts.

Risk: Credential examples could encourage unsafe handling of secrets.

Mitigation: Replace real infrastructure details with approved placeholders and avoid putting passwords in shell commands or generated output.

Risk: Generated schema synchronization statements could be incorrect or incomplete.

Mitigation: Review generated ALTER TABLE and DataX mappings before applying them, and execute DDL only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexmayanjun-collab/skills/db-table-compare)
- [ClawHub publisher profile](https://clawhub.ai/user/alexmayanjun-collab)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with SQL, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as reviewable proposals; DDL should be executed only after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
