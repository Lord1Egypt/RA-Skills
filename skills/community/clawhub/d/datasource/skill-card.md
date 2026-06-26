## Description: <br>
Guide AI to build NocoBase data models, including tables, fields, relations, and seed data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alexander-lq](https://clawhub.ai/user/Alexander-lq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and NocoBase administrators use this skill to design and implement NocoBase data models by planning entities, generating SQL DDL, registering collections, syncing fields, configuring interfaces, creating relations, and optionally adding seed data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to make persistent NocoBase database schema and data changes. <br>
Mitigation: Use it first on a development or backed-up database and review generated SQL before execution. <br>
Risk: Table creation, field sync, relation creation, and seed-data inserts can alter application behavior or stored data. <br>
Mitigation: Require explicit confirmation before running any table creation, field sync, relation creation, or seed-data insert. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Alexander-lq/datasource) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL and NocoBase tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides persistent schema, relation, field metadata, and seed-data changes that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
