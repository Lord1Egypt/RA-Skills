## Description: <br>
Manage Apache Avro schemas by validating structure, checking forward and backward compatibility, planning schema evolution, auditing namespace conventions, reviewing registry configuration, and generating code stubs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to review Avro schema files and schema registry settings before schema changes reach production data pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect schema registry configuration or propose registry policy changes. <br>
Mitigation: Use read-only or least-privilege credentials for audits and require human approval before applying policy changes or deleting schema versions. <br>
Risk: Schema compatibility guidance can be incomplete if the agent is pointed at only part of a schema set. <br>
Mitigation: Point the agent at specific schema folders or registry subjects and provide both old and new schema versions for compatibility checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/charlie-morrison/avro-schema-manager) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with validation findings, compatibility matrices, migration plans, code generation guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations and proposed commands; registry policy changes and schema deletions should remain subject to human approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
